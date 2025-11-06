# Space Invaiders Game(Notes)

'''

QUESTIONS:
How do you set up pygame?
- pip install pygame and import pygame and pygame.init()

What is the purpose of the "While running" loop?
- The "while running" loop is the main game loop that keeps the game running until the user decides to quit. It handles events, updates game state, and renders graphics.

How do you create a screen in pygame?
- You can create a screen in pygame using the pygame.display.set_mode() function, passing in a tuple with the desired width and height of the screen.

How are objects placed on the screen in pygame?
- Objects are placed on the screen in pygame using the blit() method, which draws an image or surface onto another surface at specified coordinates.

What events can I listen for in pygame? What do those events do?
- You can listen for various events in pygame, such as QUIT (to close the game), KEYDOWN (when a key is pressed), KEYUP (when a key is released), MOUSEBUTTONDOWN (when a mouse button is pressed), and MOUSEBUTTONUP (when a mouse button is released). These events allow you to handle user input and interactions within the game.

How can I detect collision with pygame?
- Collision detection in pygame can be done using bounding box methods like rect.colliderect() for rectangular objects or by calculating the distance between two objects for circular collisions.

How do you add sounds in pygame?
- You can add sounds in pygame using the pygame.mixer module. You can load sound files using mixer.Sound() for sound effects and mixer.music.load() for background music, and then play them using the play() method.

'''

import pygame
import random
import math
from pygame import mixer

#initializing pygame
pygame.init()

#Set up backround
background = pygame.image.load("resources\\background-1.jpg")
background = pygame.transform.scale(background, (800, 600))

#Background music
mixer.music.load("resources\\background.wav")
mixer.music.play(-1)

# Score Text
score_font = pygame.font.Font('freesansbold.ttf', 32)


#Set up display
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Invaiders")
pygame_icon = pygame.image.load('resources\\ufo-1.png')
#32x32 image
pygame.display.set_icon(pygame_icon)

class Button:
    def __init__(self, x, y, img, scale):
        self.x = x
        self.y = y
        width = pygame.image.load(img).get_width()
        height = pygame.image.load(img).get_height()
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (int(width * scale), int(height * scale)))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        pos = pygame.mouse.get_pos()
        action = True
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = False
                print("CLICKED")
            else:
                action = True

        screen.blit(self.img, (self.x, self.y))
        return action


class Bullet:
    def __init__(self, x=0, y=0):
        self.state = "ready"
        self.x = x
        self.y = y
        self.change = -1
        self.img = pygame.image.load('resources\\bullet.png')
        self.rotated = pygame.transform.rotate(self.img, 90)

    def shoot(self):
        self.change = -1
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
        self.score = 0
        
    
    def player_set(self):
        screen.blit(self.img, (self.x, self.y))  

    def move(self):
        self.x += self.change
        if self.x <= 0:
            self.x = 0
        elif self.x >= (800-64):
            self.x = 800-64



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
        if distance < 48:
            return True
        return False
    
    def lose(self):
        if self.y >= 440:
            return True
        return False



enemies = []
player = Player(370)
bullet = Bullet()   
for i in range(6):
    x = random.randint(0, 800-64)
    y = random.randint(0, 300-64) 
    enemies.append(Enemy(x, y))

game_over_font = pygame.font.Font('freesansbold.ttf', 64)
game_over_txt = game_over_font.render("GAME OVER", True, (255,255,255))
game_over = False

running = True
while running:
    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    score_display = score_font.render(f"Score: {player.score}", True, (255,255,255))
    screen.blit(score_display, (10,10))

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
                    mixer.Sound("resources\\laser.wav").play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change = 0
    #Changes
    player.move()

    for enemy in enemies:
        enemy.move()
        if enemy.lose():
            enemies = []
            game_over = True

    if game_over == False:

        bullet.move()
        
        for i, enemy in enumerate(enemies):
            if enemy.is_hit(bullet):
                bullet.state = "ready"
                mixer.Sound("resources\\explosion.wav").play()
                enemies.pop(i)
                bullet.x = player.x
                bullet.y = player.y
                bullet.change = 0
                player.score +=1
                if enemies == []:
                    for i in range(6):
                        x = random.randint(0,800-64)
                        y = random.randint(0,300-64)
                        enemies.append(Enemy(x,y))




        #show items
        for enemy in enemies:
            enemy.enemy_set()
        if bullet.state == "fire":
            bullet.shoot()
    else:
        screen.blit(game_over_txt, (200,250))
        button = Button(350, 350, "resources\\play.png", .25)
        game_over = button.draw()

    player.player_set()
        


    pygame.display.flip()

    
