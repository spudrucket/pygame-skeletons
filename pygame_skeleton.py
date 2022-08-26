#allows platform independent file paths
import os
#allow us to generate random numbers
import random
#allows us to call the pygame class functions
import pygame

#set platform independant main directory for game files
main_dir = os.path.split(os.path.abspath(__file__))[0]
#set data folder for the game files
data_dir = os.path.join(main_dir, "data")

#set constants; height and width of screen; height and width of game objects
WIDTH = 640
HEIGHT = 480
SPRITE_WIDTH = 80
SPRITE_HEIGHT = 60
HERO_SPEED = 10

#Class for the hero object
class HeroObject(pygame.sprite.Sprite):
    def __init__(self, speed):
        pygame.sprite.Sprite.__init__(self) # call Sprite initializer
        # load all the sprites for moving and attacking
        self.image_front, self.rect_front = load_image("hero_front.gif") # rect is used for moving and detecting collisions
        self.image_back, self.rect_back = load_image("hero_back.gif")
        self.image_left, self.rect_left = load_image("hero_left.gif")
        self.image_right, self.rect_right = load_image("hero_right.gif")
        self.image_front_attack, self.rect_front_attack = load_image("hero_front_attack.gif")
        self.image_back_attack, self.rect_back_attack = load_image("hero_back_attack.gif")
        self.image_left_attack, self.rect_left_attack = load_image("hero_left_attack.gif")
        self.image_right_attack, self.rect_right_attack = load_image("hero_right_attack.gif")
        self.image = self.image_front # set the starting sprite
        self.rect = self.rect_front # set the sprite rect for moving and collision detection
        screen = pygame.display.get_surface() # get the screen surfact
        self.screenArea = screen.get_rect() # get the screen rect to fix the sprite within the boarder
        self.rect.center = self.screenArea.center # place the sprite in the center of the screen
        self.speed = speed
        self.attacking = False
        self.direction = 2 # 1=up 2=down 3=right 4=left
    
    def update(self, up=False, down=False, left=False, right=False):
        #moves the sprite based on the rect attribute tied to keyboard arrows
        if right:
            if self.attacking == True:
                self.image = self.image_right_attack #change the sprite image if attacking
            else:
                self.image = self.image_right
            self.direction = 3
            self.rect.x += self.speed #move the sprite along the x axis
        if left:
            if self.attacking == True:
                self.image = self.image_left_attack
            else:
                self.image = self.image_left
            self.direction = 4
            self.rect.x -= self.speed
        if down:
            if self.attacking == True:
                self.image = self.image_front_attack
            else:
                self.image = self.image_front
            self.direction = 2
            self.rect.y += self.speed
        if up:
            if self.attacking == True:
                self.image = self.image_back_attack
            else:
                self.image = self.image_back
            self.direction = 1
            self.rect.y -= self.speed
        self.rect.clamp_ip(self.screenArea) # keeps the sprite within the borders of the screen
        #changes the sprite image when not moving based on if attacking
        if self.attacking == True:
            if self.direction == 3 and self.image != self.image_right_attack:
                self.image = self.image_right_attack
            if self.direction == 4 and self.image != self.image_left_attack:
                self.image = self.image_left_attack
            if self.direction == 2 and self.image != self.image_front_attack:
                self.image = self.image_front_attack
            if self.direction == 1 and self.image != self.image_back_attack:
                self.image = self.image_back_attack
        if self.attacking == False:
            if self.direction == 3 and self.image != self.image_right:
                self.image = self.image_right
            if self.direction == 4 and self.image != self.image_left:
                self.image = self.image_left
            if self.direction == 2 and self.image != self.image_front:
                self.image = self.image_front
            if self.direction == 1 and self.image != self.image_back:
                self.image = self.image_back
       
    def heroDied(self):
        print("you died")

#class for the enemy object
class EnemyObject(pygame.sprite.Sprite):
    def __init__(self, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("enemy.gif")
        screen = pygame.display.get_surface()
        self.screenArea = screen.get_rect()
        self.speed = speed
        self.gotHit = False
        self.distance = 0
        self.direction = 0 # 1=up 2=down 3=right 4=left
        
    def update(self, enemy_group):
        if self.gotHit:
            self._spin(enemy_group)
        else:
            self._walk()
            
    def _walk(self):
        #a random number from 5 to 50 for the number of frames the sprite will travel
        if self.distance == 0:
            self.distance = random.randrange(5, 50)
            #flip the sprite when there is a change
            self.image = pygame.transform.flip(self.image, True, False)
        #generate a random number from 1 to 4 for a direction 1=down 2=up 3=right 4=left
        if self.direction == 0:
            self.direction = random.randrange(1, 4)
        if self.direction == 1:
            newPosition = self.rect.move((0, self.speed))
            self.distance -= 1 #counts down from the distance to 0
        elif self.direction == 2:
            newPosition = self.rect.move((0, -self.speed))
            self.distance -= 1
        elif self.direction == 3:
            newPosition = self.rect.move((self.speed, 0))
            self.distance -= 1
        elif self.direction == 4:
            newPosition = self.rect.move((-self.speed, 0))
            self.distance -= 1
        if self.distance == 0:
            self.direction = 0
        #reverses the direction of sprite when it hits an edge and resets the distance
        if not self.screenArea.contains(newPosition):
            if self.rect.left < self.screenArea.left:
                self.direction = 3
                self.distance = 0
            elif self.rect.right > self.screenArea.right:
                self.direction = 4
                self.distance = 0
            elif self.rect.bottom < self.screenArea.bottom:
                self.direction = 1
                self.distance = 0
            elif self.rect.top > self.screenArea.top:
                self.direction = 2
                self.distance = 0
        self.rect = newPosition

    #spins the enemy around when hit, counts down, then deletes the sprite from the enemies group
    def _spin(self, enemy_group):
        center = self.rect.center
        self.gotHit = self.gotHit + 12
        if self.gotHit >= 360:
            self.gotHit = False
            enemy_group.remove(self)
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.gotHit)
        self.rect = self.image.get_rect(center=center)
        
    def attacked(self):
        if not self.gotHit == True:
            self.gotHit = True
            self.original = self.image
    
#function to load an image
def load_image(image_name):
    #appends file name to the end of the path; add necessary folder names to 
    full_path = os.path.join(data_dir, image_name)
    #load the image
    image = pygame.image.load(full_path)
    #optional scale the image "image = pygame.transform.scale(image, [size])"
    #convert matches color format and depth to match the display
    image = image.convert()
    return image, image.get_rect()

#function to load sounds
def load_sound(sound_name):
    #if there is no sound module, then the game will work
    class NoSound:
        def play(self):
            pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoSound()
    #load the sound if the sound module exists
    full_path = os.path.join(data_dir, sound_name)
    sound = pygame.mixer.Sound(full_path)
    return sound

#main function
def main():
    #start the game, start the clock, set the screen
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    #add text to the window bar
    pygame.display.set_caption("Get the Skeletons!")
    #load the background using the Load_image function above
    background = pygame.image.load(os.path.join(data_dir, "background.bmp"))
    background = background.convert()
    #draw the background to the screen
    screen.blit(background, (0, 0))
    pygame.display.flip()
    #instantiate the player using the 
    player = HeroObject(HERO_SPEED)
    playerSprites = pygame.sprite.Group(player)
    #create a group to hold multiple game objects
    enemySprites = pygame.sprite.Group()
    #instantiate enemies using the GameObject class and add them to the sprites list
    for x in range(10):
        enemy = EnemyObject(5)
        enemySprites.add(enemy)
    #main loop for the game
    going = True
    while going:
        #set the clock speed
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            #quit the game when escape key is pressed
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                going = False
            #KEYDOWN and KEYUP only give input once when the key is pressed and again when released
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.attacking = True
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                player.attacking = False
        #get_pressed() gives input when the key is held down
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.update(up=True)
        if keys[pygame.K_DOWN]:
            player.update(down=True)
        if keys[pygame.K_LEFT]:
            player.update(left=True)
        if keys[pygame.K_RIGHT]:
            player.update(right=True)
        #check for collisions between the player and any sprites in the enemy group
        #spritecollideany() returns None or the collided with sprite from the gorup
        hitSprite = pygame.sprite.spritecollideany(player, enemySprites)
        #check if the player attacked an enemy sprite
        if hitSprite != None and player.attacking == True:
            if hitSprite.gotHit == False:
                hitSprite.attacked()
        #check if the enemy hit the player
        elif hitSprite != None and hitSprite.gotHit == False:
            player.heroDied()
        #update the sprites
        playerSprites.update()
        enemySprites.update(enemySprites)
        #draw background and sprites in new positions
        screen.blit(background, (0, 0))
        playerSprites.draw(screen)
        enemySprites.draw(screen)
        pygame.display.flip()
        #quit the game on screen exit
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
        #slow down the game
        pygame.time.delay(100)

#starts the main loop
if __name__ == "__main__":
    main()
    #quits the game
    pygame.quit()
