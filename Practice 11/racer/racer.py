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
GOLD = (255, 215, 0)      # Extra: Gold color for heavy coin
SILVER = (192, 192, 192)  # Extra: Silver color for medium coin
BRONZE = (205, 127, 50)   # Extra: Bronze color for light coin
YELLOW = (255, 222, 23)

# screen size
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# enemy speed
SPEED = 5

SCORE = 0

COINS = 0

# Extra: Track number of coins for speed increase
COINS_FOR_SPEED_INCREASE = 5  # Increase enemy speed every 5 coins
BASE_ENEMY_SPEED = 5

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

# background car sound
try:
    pygame.mixer.music.load("engine.mp3")
    pygame.mixer.music.play(-1)   # -1 значит бесконечно
except:
    print("Engine sound file not found")

# create surface
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


# enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        try:
            self.image = pygame.image.load("Enemy.png")
        except:
            self.image = pygame.Surface((50, 80))
            self.image.fill(RED)
        
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

        try:
            self.image = pygame.image.load("Player.png")
        except:
            self.image = pygame.Surface((50, 80))
            self.image.fill(GREEN)
        
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


# Extra: Weighted Coin class with different weights
class Coin(pygame.sprite.Sprite):
    # Extra: Coin weight types
    WEIGHT_LIGHT = 1    # Bronze coin - 1 point
    WEIGHT_MEDIUM = 2   # Silver coin - 2 points
    WEIGHT_HEAVY = 3    # Gold coin - 3 points
    
    def __init__(self):
        super().__init__()

        # Load coin image
        try:
            self.original_image = pygame.image.load("coin.png")
        except:
            self.original_image = pygame.Surface((30, 30))
            self.original_image.fill(YELLOW)
        
        # Extra: Randomly assign weight with different probabilities
        weight_choice = random.random()
        if weight_choice < 0.6:  # 60% chance for light coins
            self.weight = self.WEIGHT_LIGHT
            self.value = 1
            self.color = BRONZE
            # Tint the coin with bronze color
            self.image = self.original_image.copy()
            self.image.fill(BRONZE, special_flags=pygame.BLEND_RGB_MULT)
        elif weight_choice < 0.85:  # 25% chance for medium coins
            self.weight = self.WEIGHT_MEDIUM
            self.value = 2
            self.color = SILVER
            # Tint the coin with silver color
            self.image = self.original_image.copy()
            self.image.fill(SILVER, special_flags=pygame.BLEND_RGB_MULT)
        else:  # 15% chance for heavy coins
            self.weight = self.WEIGHT_HEAVY
            self.value = 3
            self.color = GOLD
            # Keep original gold color
            self.image = self.original_image.copy()

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

# Extra: Function to increase enemy speed based on collected coins
def update_enemy_speed():
    global SPEED, BASE_ENEMY_SPEED, COINS_FOR_SPEED_INCREASE
    
    # Calculate speed increase: base speed + (coins collected / coins needed for increase)
    # Speed increases by 0.5 for every N coins collected
    speed_increase = (COINS // COINS_FOR_SPEED_INCREASE) * 0.5
    
    # Cap maximum speed to prevent impossible gameplay
    max_speed = 15
    new_speed = BASE_ENEMY_SPEED + speed_increase
    
    if new_speed <= max_speed:
        SPEED = new_speed
    else:
        SPEED = max_speed

# Extra: Variable to track previous coin count for speed update
previous_coin_count = 0

# Game loop
while True:
    for event in pygame.event.get():
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
    
    # Extra: Show current enemy speed
    speed_text = font_small.render("Speed: " + str(int(SPEED * 10) / 10), True, BLACK)
    speed_rect = speed_text.get_rect(topright=(SCREEN_WIDTH - 10, 35))
    DISPLAYSURF.blit(speed_text, speed_rect)

    # Draw and move all sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # if player collide coin (collect) - Extra: Now with weighted values
    if pygame.sprite.spritecollideany(P1, coins):
        # Add coin value based on weight
        COINS += C1.value
        
        # Extra: Update enemy speed when coins are collected
        if COINS != previous_coin_count:
            update_enemy_speed()
            previous_coin_count = COINS
        
        # Extra: Display collected coin value in console
        print(f"Collected coin! +{C1.value} points (Total: {COINS})")
        
        # Respawn with new random weight
        C1.kill()  # Remove old coin
        C1 = Coin()  # Create new weighted coin
        coins.add(C1)
        all_sprites.add(C1)

    # if collide with enemy
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.music.stop() 
        try:
            pygame.mixer.Sound("crash.wav").play()
        except:
            print("Crash sound file not found")
        time.sleep(1)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        
        # Extra: Display final stats
        final_coins_text = font_small.render("Coins collected: " + str(COINS), True, WHITE)
        final_coins_rect = final_coins_text.get_rect(center=(200, 350))
        DISPLAYSURF.blit(final_coins_text, final_coins_rect)
        
        # Extra: Display final score
        final_score_text = font_small.render("Score: " + str(SCORE), True, WHITE)
        final_score_rect = final_score_text.get_rect(center=(200, 380))
        DISPLAYSURF.blit(final_score_text, final_score_rect)

        pygame.display.update()

        for entity in all_sprites:
            entity.kill()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)