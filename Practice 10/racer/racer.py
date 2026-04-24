# Imports
import pygame, sys
from pygame.locals import *
import random, time

pygame.init()
pygame.mixer.init()

# FPS
FPS = 60
FramePerSec = pygame.time.Clock()

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# screen size
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# enemy speed
SPEED = 5

SCORE = 0

COINS = 0

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

# background car sound
pygame.mixer.music.load("engine.mp3")
pygame.mixer.music.play(-1)   # -1 значит бесконечно

# create surface
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


# enemy classx
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()

        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE

        # enemy goes down
        self.rect.move_ip(0, SPEED)

        if self.rect.bottom > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


# player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()

        # start position
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


# coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("coin.png")

        self.image = pygame.transform.scale(self.image, (30, 30))

        self.rect = self.image.get_rect()
        self.respawn()

    def respawn(self):
        self.rect.center = (
            random.randint(30, SCREEN_WIDTH - 30),
            random.randint(-100, -40)
        )

    def move(self):
        self.rect.move_ip(0, 4)
        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()


# create objects
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# increase speed
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # draw background
    DISPLAYSURF.blit(background, (0, 0))

    # show score
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # show coins
    coins_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    coin_rect = coins_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    DISPLAYSURF.blit(coins_text, coin_rect)

    # draw and move sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # if player collide coin(collect)
    if pygame.sprite.spritecollideany(P1, coins):
        COINS += 1
        C1.respawn()

    # if collide with enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop() 
        pygame.mixer.Sound("crash.wav").play()
        time.sleep(1)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()

        for entity in all_sprites:
            entity.kill()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)