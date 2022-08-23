#allows platform independent file paths
import os
import pygame
from pygame.locals import *

#set main directory
main_dir = os.path.split(os.path.abspath(__file__))[0]
#set folder for the game files
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
        self.image, self.rect = load_image("hero.gif")
        self.speed = speed
        self.attacking = False
    
    def update(self, up=False, down=False, left=False, right=False):
        #moves the sprite based on the rect attribute
        if right:
            self.rect.x += self.speed
        if left:
            self.rect.x -= self.speed
        if down:
            self.rect.y += self.speed
        if up:
            self.rect.y -= self.speed
    
    def attack(self, target):
        #returns true if the hero collides with the target
        if not self.attacking:
            self.attacking = True
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)
    
    def stopAttack(self):
        self.attacking = False

#class for the enemy object
class EnemyObject(pygame.sprite.Sprite):    
    def __init__(self, startingPosition, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image("enemy.gif")
        screen = pygame.display.get_surface()
        self.screenArea = screen.get_rect()
        self.rect.topleft = 10, 90
        self.startingPosition = startingPosition
        self.speed = speed
        self.gotHit = False
        
    def update(self):
        if self.gotHit:
            self._spin()
        else:
            self._walk()
            
    def _walk(self):
        newPosition = self.rect.move((self.speed, 0))
        if not self.screenArea.contains(newPosition):
            if self.rect.left < self.screenArea.left or self.rect.right > self.screenArea.right:
                self.speed = -self.speed
                newPosition = self.rect.move((self.speed, 0))
                self.image = pygame.transform.flip(self.image, True, False)
        self.rect = newPosition
        
    def _spin(self):
        center = self.rect.center
        self.gotHit = self.gotHit + 12
        if self.gotHit >= 360:
            self.gotHit = False
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.gotHit)
        self.rect = self.image.get_rect(center=center)
        
    def attacked(self):
        if not self.gotHit == True:
            self.gotHit = True
            self.original = self.image
            
    def stopAttack(self):
        self.attacking = False
    
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
    #create an empty list to hold multiple game objects
    allSprites = pygame.sprite.RenderPlain()
    #instantiate the player using the 
    player = HeroObject(HERO_SPEED)
    allSprites.add(player)
    #instantiate enemies using the GameObject class and add them to the sprites list
    for x in range(5):
        enemy = EnemyObject(x * 40, x)
        allSprites.add(enemy)
    #main loop for the game
    going = True
    while going:
        #set the clock speed
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                going = False
        #event handler that takes keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.update(up=True)
        if keys[pygame.K_DOWN]:
            player.update(down=True)
        if keys[pygame.K_LEFT]:
            player.update(left=True)
        if keys[pygame.K_RIGHT]:
            player.update(right=True)
        if keys[pygame.K_SPACE]:
            if player.attack(enemy):
                enemy.attacked()
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            player.stopAttack()
        #update the sprites
        allSprites.update()
        #draw background and sprites in new positions
        screen.blit(background, (0, 0))
        allSprites.draw(screen)
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