# Imports
import pygame, sys
from pygame.locals import *
import random, time

# запускаем pygame
pygame.init()
pygame.mixer.init()

# FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# цвета
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# размеры окна
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# скорость врага
SPEED = 5

# счет
SCORE = 0

# количество монет
COINS = 0

# шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# фон
background = pygame.image.load("AnimatedStreet.png")

# фоновый звук машины
pygame.mixer.music.load("engine.mp3")
pygame.mixer.music.play(-1)   # -1 значит бесконечно

# создаем окно
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


# класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # картинка врага
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()

        # случайная позиция сверху
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE

        # враг едет вниз
        self.rect.move_ip(0, SPEED)

        # если вышел вниз экрана
        if self.rect.bottom > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


# класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # картинка игрока
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()

        # стартовая позиция
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        # влево
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)

        # вправо
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)


# класс монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # загружаем картинку монеты
        self.image = pygame.image.load("coin.png")

        # уменьшаем размер если картинка большая
        self.image = pygame.transform.scale(self.image, (30, 30))

        self.rect = self.image.get_rect()

        # сразу ставим монету в случайное место
        self.respawn()

    def respawn(self):
        # монета появляется сверху в случайном месте
        self.rect.center = (
            random.randint(30, SCREEN_WIDTH - 30),
            random.randint(-100, -40)
        )

    def move(self):
        # монета падает вниз
        self.rect.move_ip(0, 4)

        # если ушла вниз, создаем заново
        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()


# создаем объекты
P1 = Player()
E1 = Enemy()
C1 = Coin()

# группы
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# событие для увеличения скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# игровой цикл
while True:

    # события
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # рисуем фон
    DISPLAYSURF.blit(background, (0, 0))

    # показываем score слева сверху
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # показываем coins справа сверху
    coins_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    coin_rect = coins_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    DISPLAYSURF.blit(coins_text, coin_rect)

    # двигаем и рисуем все спрайты
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # если игрок собрал монету
    if pygame.sprite.spritecollideany(P1, coins):
        COINS += 1
        C1.respawn()

    # если столкновение с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop()   # останавливаем фоновый звук
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

    # обновляем экран
    pygame.display.update()
    FramePerSec.tick(FPS)