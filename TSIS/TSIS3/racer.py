import pygame, random
def run_game(screen, settings):

    pygame.mixer.init()

    difficulty = settings.get("difficulty", "normal")
    car_color = settings.get("car_color", "default")

    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 600
    FPS = 60

    if difficulty == "hard":
        SPEED = 10
        PLAYER_SPEED = 7
    else:
        SPEED = 5
        PLAYER_SPEED = 5
    BASE_PLAYER_SPEED = 5

    COINS = 0
    SCORE = 0
    DISTANCE = 0
    lives = 1

    active_power = None
    power_timer = 0
    shield = False

    sound_on = settings.get("sound", True)

    clock = pygame.time.Clock()

    background = pygame.image.load("images/AnimatedStreet.png")
    font = pygame.font.SysFont("Verdana", 20)

    # ===== SOUNDS =====
    coin_sound = pygame.mixer.Sound("sounds/coin.mp3")
    crash_sound = pygame.mixer.Sound("sounds/crash.wav")
    power_sound = pygame.mixer.Sound("sounds/power.mp3")

    coin_sound.set_volume(0.3)
    crash_sound.set_volume(0.5)
    power_sound.set_volume(0.4)

    # ===== CLASSES =====

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("images/Player.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (40,60))

            if car_color == "red":
                self.image.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_MULT)


            self.rect = self.image.get_rect(center=(160,520))

        def move(self):
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.move_ip(-PLAYER_SPEED, 0)

            if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
                self.rect.move_ip(PLAYER_SPEED, 0)


    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("images/Enemy.png")
            self.image = pygame.transform.scale(self.image, (40,60))
            self.rect = self.image.get_rect()
            self.reset()

        def reset(self):
            self.rect.center = (random.randint(40,SCREEN_WIDTH-40), -60)

        def move(self):
            nonlocal SCORE
            self.rect.move_ip(0,SPEED)
            if self.rect.top > SCREEN_HEIGHT:
                SCORE += 1
                self.reset()


    class Coin(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("images/coin.png").convert_alpha()
            self.value = random.choice([1,2,3])
            size = 30 + self.value * 10
            self.image = pygame.transform.scale(self.image,(size,size))
            self.rect = self.image.get_rect(center=(random.randint(40,SCREEN_WIDTH-40), -40))

        def move(self):
            self.rect.move_ip(0,SPEED)
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()


    class Obstacle(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.type = random.choice(["barrier","oil"])
            self.image = pygame.Surface((40,40))

            if self.type == "barrier":
                self.image.fill((0,0,0))
            else:
                self.image.fill((80,80,80))

            self.rect = self.image.get_rect(center=(random.randint(40,SCREEN_WIDTH-40), -40))

        def move(self):
            self.rect.move_ip(0,SPEED)
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()


    class PowerUp(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.type = random.choice(["nitro","shield","repair"])
            self.image = pygame.Surface((30,30))

            if self.type == "nitro":
                self.image.fill((0,255,0))
            elif self.type == "shield":
                self.image.fill((0,0,255))
            else:
                self.image.fill((255,255,0))

            self.rect = self.image.get_rect(center=(random.randint(40,SCREEN_WIDTH-40), -40))

        def move(self):
            self.rect.move_ip(0,SPEED)
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()


    # ===== INIT =====

    P1 = Player()

    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group(P1)

    enemy_count = 4 if difficulty == "hard" else 2

    for _ in range(enemy_count):
        e = Enemy()
        enemies.add(e)
        all_sprites.add(e)

    # ===== EVENTS =====
    ADD_COIN = pygame.USEREVENT + 1
    ADD_OBS = pygame.USEREVENT + 2
    ADD_POWER = pygame.USEREVENT + 3
    SPEED_UP = pygame.USEREVENT + 4

    pygame.time.set_timer(ADD_COIN, 1500)
    pygame.time.set_timer(ADD_OBS, 2000)
    pygame.time.set_timer(ADD_POWER, 5000)
    pygame.time.set_timer(SPEED_UP, 3000)

    # ===== LOOP =====
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return SCORE, DISTANCE

            if event.type == ADD_COIN:
                if len(coins) < 2:
                    c = Coin()
                    coins.add(c)
                    all_sprites.add(c)

            if event.type == ADD_OBS:
                o = Obstacle()
                obstacles.add(o)
                all_sprites.add(o)

            if event.type == ADD_POWER:
                p = PowerUp()
                powerups.add(p)
                all_sprites.add(p)

            if event.type == SPEED_UP:
                SPEED += 0.5

        DISTANCE += 1

        screen.blit(background,(0,0))

        for entity in all_sprites:
            entity.move()
            screen.blit(entity.image, entity.rect)

        P1.move()

        # ===== COLLISIONS =====

        # ENEMY
        hits = pygame.sprite.spritecollide(P1, enemies, False)
        for enemy in hits:
            if shield:
                shield = False
                active_power = None  
                enemy.reset()

            elif lives > 0:
                lives -= 1
                enemy.reset()

            else:
                if sound_on:
                    crash_sound.play()
                pygame.time.delay(400)
                return SCORE, DISTANCE


        # OBSTACLE
        hits = pygame.sprite.spritecollide(P1, obstacles, True)
        for h in hits:
            if h.type == "barrier":
                if shield:
                    shield = False
                    active_power = None 

                elif lives > 0:
                    lives -= 1

                else:
                    if sound_on:
                        crash_sound.play()
                    pygame.time.delay(400)
                    return SCORE, DISTANCE

            elif h.type == "oil":
                P1.rect.move_ip(random.choice([-20,20]), 0)

        # COINS
        hits = pygame.sprite.spritecollide(P1, coins, True)
        for c in hits:
            COINS += c.value
            if sound_on:
                coin_sound.play()

        # POWERUPS
        hits = pygame.sprite.spritecollide(P1, powerups, True)
        for p in hits:

            #  REPAIR — instant effect
            if p.type == "repair":
                lives += 1
                if sound_on:
                    power_sound.play()
                continue

            #  остальные
            if active_power is None:
                active_power = p.type
                power_timer = pygame.time.get_ticks()

                if sound_on:
                    power_sound.play()

                if p.type == "shield":
                    shield = True

        # POWER LOGIC
        if active_power == "nitro":
            PLAYER_SPEED = BASE_PLAYER_SPEED + 5

            if pygame.time.get_ticks() - power_timer > 5000:
                PLAYER_SPEED = BASE_PLAYER_SPEED
                active_power = None

        # ===== UI =====
        screen.blit(font.render(f"Coins: {COINS}", True,(255,255,0)),(10,10))
        screen.blit(font.render(f"Distance: {DISTANCE}", True,(255,255,255)),(10,30))
        screen.blit(font.render(f"Lives: {lives}", True,(255,0,0)),(10,50))

        if active_power:
            screen.blit(font.render(f"Power: {active_power}", True,(255,255,255)),(10,70))

        if shield:
            pygame.draw.circle(screen,(0,0,255),P1.rect.center,40,3)

        pygame.display.update()
        clock.tick(FPS)