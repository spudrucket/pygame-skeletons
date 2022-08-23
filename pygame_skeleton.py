import os
import pygame
from pygame.locals import *

#set main directory
main_dir = os.path.split(os.path.abspath(__file__))[0]

#set constants; height and width of screen; height and width of game objects
WIDTH = 640
HEIGHT = 480
SPRITE_WIDTH = 80
SPRITE_HEIGHT = 60

#Class for the game object
class GameObject:
    def __init__(self, image, height, speed):
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(0, height)
    
    #function for moving the object
    def move(self, up=False, down=False, left=False, right=False):
        if right:
            self.pos.right += self.speed
        if left:
            self.pos.right -= self.speed
        if down:
            self.pos.top += self.speed
        if up:
            self.pos.top -= self.speed
        #keeps the object within the screen
        if self.pos.right > WIDTH:
            self.pos.left = 0
        if self.pos.top > HEIGHT - SPRITE_HEIGHT:
            self.pos.top = 0
        if self.pos.right < SPRITE_WIDTH:
            self.pos.right = WIDTH
        if self.pos.top < 0:
            self.pos.top = HEIGHT - SPRITE_HEIGHT
    
#function to load an image
def load_image(image_name):
    #appends file name to the end of the path; add necessary folder names to 
    path = os.path.join(main_dir, image_name)
    return pygame.image.load(path).convert()

#main function
def main():
    #start the game, start the clock, set the screen
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
    #load the background and sprites using the Load_image function above
    hero_image = load_image("hero.gif")
    enemy_image = load_image("enemy.gif")
    background = load_image("background.bmp")
    #scale the background image; secondly overwrite the old sprite position
    #background = pygame.transform.scale2x(background)
    #background = pygame.transform.scale2x(background)
    #draw the background to the screen
    screen.blit(background, (0, 0))
    #create an empty list to hold multiple game objects, here enemies
    objects = []
    #instantiate the player using the GameObject class (image, height, speed)
    player = GameObject(hero_image, 10, 3)
    #instantiate enemies using the GameObject class and add them to the objects list
    for x in range(5):
        enemy = GameObject(enemy_image, x * 40, x)
        objects.append(enemy)
    #add text to the screen
    pygame.display.set_caption("Move It!")
    #main loop for the game
    while True:
        #event handler that takes keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move(up=True)
        if keys[pygame.K_DOWN]:
            player.move(down=True)
        if keys[pygame.K_LEFT]:
            player.move(left=True)
        if keys[pygame.K_RIGHT]:
            player.move(right=True)
        #draw background after moving sprite
        screen.blit(background, (0, 0))
        #quit the game on screen exit
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
        #draw enemies on screen
        for o in objects:
            screen.blit(background, o.pos, o.pos)
        #move enemies on screen
        for o in objects:
            o.move(right=True)
            screen.blit(o.image, o.pos)
        #draw hero on the screen
        screen.blit(player.image, player.pos)
        #set the clock speed?
        clock.tick(60)
        #update the screen
        pygame.display.update()
        #slow down the game
        pygame.time.delay(100)

#starts the main loop
if __name__ == "__main__":
    main()
    #quits the game
    pygame.quit()