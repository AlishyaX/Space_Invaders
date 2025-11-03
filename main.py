# Space Invaiders Game

import pygame
import random
import math


#initializing pygame
pygame.init()

#Set up display
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaiders")
pygame_icon = pygame.image.load('resources\\ufo-1.png')
#32x32 image
pygame.display.set_icon(pygame_icon)

class Bullet:
    def __init__(self, x=0, y=0):
        self.state = "ready"
        self.x = x
        self.y = y
        self.change = -1
        self.img = pygame.image.load('resources\\bullet.png')
        self.rotated = pygame.transform.rotate(self.img, 90)

    def shoot(self):
        screen.blit(self.rotated, (self.x, self.y))

    def move(self):
        self.y += self.change
        if self.y <= 0:
            self.state = "ready"
            



#player class
class Player:
    def __init__(self, x, change = 0):
        self.img = pygame.image.load('resources\\spaceship.png')
        self.x = x
        self.y = 600-69
        self.change = change
        
    
    def player_set(self):
        screen.blit(self.img, (self.x, self.y))  

    def move(self):
        self.x += self.change
        if self.x <= 0:
            self.x = 0
        elif self.x >= (800-64):
            self.x = 736



class Enemy:
    def __init__(self, x, y, change = 0):
        self.img = pygame.image.load('resources\\alien.png')
        self.x = x
        self.y = y
        self.x_change = 0.3
        self.y_change = 20

    def enemy_set(self):
        screen.blit(self.img, (self.x, self.y))  

    def move(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x_change = 0.3
            self.y_change += self.y_change
        elif self.x >= 800-64:
            self.x_change = -0.3
            self.y += self.y_change

    def is_hit(self, bullet):
        distance = math.sqrt((self.x - bullet.x)**2 + (self.y - bullet.y)**2)
        if distance < 27:
            pass



player = Player(370)
x = random.randint(0, 800-64)
y = random.randint(0, 300-64) 
bullet = Bullet()   
enemy = Enemy(x, y)




running = True
while running:
    screen.fill((0,0,0))

    #loop events
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_LEFT]:
                player.change = -0.3
            if keys[pygame.K_RIGHT]:
                player.change = 0.3
            if keys[pygame.K_SPACE]:
                if bullet.state == "ready":
                    bullet.x = player.x +16
                    bullet.y = player.y +18
                    bullet.state = "fire"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change = 0
    #Changes
    player.move()
    enemy.move()
    bullet.move()
    

    #show items
    player.player_set()
    enemy.enemy_set()
    if bullet.state == "fire":
        bullet.shoot()


    pygame.display.flip()

    
