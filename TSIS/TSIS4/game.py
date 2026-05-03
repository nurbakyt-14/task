import pygame
import random
import time

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
DARK_RED = (139, 0, 0)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)

class Snake:
    def __init__(self):
        start_x = GRID_WIDTH // 2 * CELL_SIZE
        start_y = GRID_HEIGHT // 2 * CELL_SIZE
        self.body = [(start_x, start_y)]
        self.direction = (CELL_SIZE, 0)
        self.grow_flag = False
        
    def move(self):
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False
            
    def change_direction(self, new_dir):
        if (new_dir[0] == -self.direction[0] and new_dir[1] == -self.direction[1]):
            return
        self.direction = new_dir
        
    def grow(self):
        self.grow_flag = True
        
    def shrink(self, amount=2):
        for _ in range(amount):
            if len(self.body) > 1:
                self.body.pop()
        
    def check_self_collision(self):
        head = self.body[0]
        return head in self.body[1:]
        
    def draw(self, screen, snake_color):
        for segment in self.body:
            pygame.draw.rect(screen, snake_color, (segment[0], segment[1], CELL_SIZE-2, CELL_SIZE-2))
    
    def get_length(self):
        return len(self.body)

class WeightedFood:
    WEIGHT_LIGHT = 1
    WEIGHT_MEDIUM = 2
    WEIGHT_HEAVY = 3
    
    def __init__(self, snake_body, walls, obstacles):
        self.is_poison = random.random() < 0.15
        
        if not self.is_poison:
            weight_choice = random.random()
            if weight_choice < 0.5:
                self.weight = self.WEIGHT_LIGHT
                self.value = 1
                self.color = RED
                self.duration = 6
            elif weight_choice < 0.75:
                self.weight = self.WEIGHT_MEDIUM
                self.value = 2
                self.color = ORANGE
                self.duration = 5
            else:
                self.weight = self.WEIGHT_HEAVY
                self.value = 3
                self.color = PURPLE
                self.duration = 4
        else:
            self.value = -2
            self.color = DARK_RED
            self.duration = 5
        
        self.spawn_time = time.time()
        self.position = self.get_random_position(snake_body, walls, obstacles)
        
    def get_random_position(self, snake_body, walls, obstacles):
        max_attempts = 100
        for _ in range(max_attempts):
            x = random.randint(0, GRID_WIDTH - 1) * CELL_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
            pos = (x, y)
            if pos not in snake_body and pos not in walls and pos not in obstacles:
                return pos
        return (CELL_SIZE, CELL_SIZE)
                
    def is_expired(self):
        return time.time() - self.spawn_time > self.duration
    
    def get_remaining_time(self):
        remaining = max(0, self.duration - (time.time() - self.spawn_time))
        return remaining
                
    def draw(self, screen, small_font):
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], CELL_SIZE-2, CELL_SIZE-2))
        
        remaining_percent = self.get_remaining_time() / self.duration
        bar_height = 3
        bar_width = int(CELL_SIZE * remaining_percent)
        bar_rect = pygame.Rect(self.position[0], self.position[1], bar_width, bar_height)
        pygame.draw.rect(screen, YELLOW, bar_rect)
        
        if not self.is_poison:
            value_text = small_font.render(str(self.value), True, WHITE)
        else:
            value_text = small_font.render("!", True, WHITE)
        text_rect = value_text.get_rect(center=(self.position[0] + CELL_SIZE//2, 
                                                 self.position[1] + CELL_SIZE//2))
        screen.blit(value_text, text_rect)

class PowerUp:
    TYPES = ["speed_boost", "slow_motion", "shield"]
    
    def __init__(self, snake_body, walls, obstacles):
        self.type = random.choice(self.TYPES)
        self.position = self.get_random_position(snake_body, walls, obstacles)
        self.spawn_time = time.time()
        self.duration = 8
        self.effect_duration = 5
        
        self.colors = {
            "speed_boost": CYAN,
            "slow_motion": PURPLE,
            "shield": BLUE
        }
    
    def get_random_position(self, snake_body, walls, obstacles):
        max_attempts = 100
        for _ in range(max_attempts):
            x = random.randint(0, GRID_WIDTH - 1) * CELL_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
            pos = (x, y)
            if pos not in snake_body and pos not in walls and pos not in obstacles:
                return pos
        return (CELL_SIZE, CELL_SIZE)
    
    def draw(self, screen, small_font):
        pygame.draw.rect(screen, self.colors[self.type], 
                        (self.position[0], self.position[1], CELL_SIZE-2, CELL_SIZE-2))
        center = (self.position[0] + CELL_SIZE//2, self.position[1] + CELL_SIZE//2)
        
    
    def is_expired(self):
        return time.time() - self.spawn_time > self.duration

class Obstacle:
    def __init__(self, x, y):
        self.position = (x, y)
    
    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, 
                        (self.position[0], self.position[1], CELL_SIZE-2, CELL_SIZE-2))
        pygame.draw.rect(screen, BLACK, 
                        (self.position[0], self.position[1], CELL_SIZE-2, CELL_SIZE-2), 1)

class Wall:
    def __init__(self):
        self.positions = []
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            self.positions.append((x, 0))
            self.positions.append((x, SCREEN_HEIGHT - CELL_SIZE))
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            self.positions.append((0, y))
            self.positions.append((SCREEN_WIDTH - CELL_SIZE, y))
            
    def check_collision(self, head):
        return head in self.positions
        
    def draw(self, screen):
        for pos in self.positions:
            pygame.draw.rect(screen, BLUE, (pos[0], pos[1], CELL_SIZE-2, CELL_SIZE-2))

class Game:
    def __init__(self, config, username):
        self.config = config
        self.username = username
        self.reset()
    
    def reset(self):
        self.snake = Snake()
        self.wall = Wall()
        self.obstacles = []
        self.foods = []
        self.power_ups = []
        self.score = 0
        self.level = 1
        self.speed = 8
        self.last_food_spawn = time.time()
        self.last_power_up_spawn = time.time()
        self.game_over = False
        self.active_effects = {"speed_boost": 0, "slow_motion": 0, "shield": 0}
        
        self.foods.append(WeightedFood(self.snake.body, self.wall.positions, 
                                       [obs.position for obs in self.obstacles]))
        
        if self.level >= 3:
            self.spawn_obstacles()
    
    def spawn_obstacles(self):
        num_obstacles = min(5 + self.level, 20)
        self.obstacles = []
        
        for _ in range(num_obstacles):
            max_attempts = 50
            for _ in range(max_attempts):
                x = random.randint(1, GRID_WIDTH - 2) * CELL_SIZE
                y = random.randint(1, GRID_HEIGHT - 2) * CELL_SIZE
                pos = (x, y)
                
                if (pos not in self.snake.body and 
                    pos not in self.wall.positions and
                    pos not in [obs.position for obs in self.obstacles]):
                    
                    head = self.snake.body[0]
                    if abs(head[0] - x) // CELL_SIZE > 2 or abs(head[1] - y) // CELL_SIZE > 2:
                        self.obstacles.append(Obstacle(x, y))
                        break
    
    def check_obstacle_collision(self, head):
        for obstacle in self.obstacles:
            if head == obstacle.position:
                return True
        return False
    
    def update_effects(self):
        current_time = time.time()
        if current_time > self.active_effects["speed_boost"]:
            self.active_effects["speed_boost"] = 0
        if current_time > self.active_effects["slow_motion"]:
            self.active_effects["slow_motion"] = 0
    
    def get_current_speed(self):
        speed_multiplier = 1
        if self.active_effects["speed_boost"] > 0:
            speed_multiplier = 1.5
        elif self.active_effects["slow_motion"] > 0:
            speed_multiplier = 0.5
        return int(self.speed * speed_multiplier)
    
    def update(self, db):
        if self.game_over:
            return
        
        self.update_effects()
        
        self.snake.move()
        
        head = self.snake.body[0]
        
        if self.wall.check_collision(head) or self.snake.check_self_collision():
                self.game_over = True
                db.save_game_result(self.username, self.score, self.level)
                return
        
        if self.check_obstacle_collision(head):
            if self.active_effects["shield"] > 0:
                self.active_effects["shield"] = 0
            else:
                self.game_over = True
                db.save_game_result(self.username, self.score, self.level)
                return
        
        for food in self.foods[:]:
            if head == food.position:
                if food.is_poison:
                    self.snake.shrink(2)
                    if self.snake.get_length() <= 1:
                        self.game_over = True
                        db.save_game_result(self.username, self.score, self.level)
                        return
                else:
                    self.score += food.value
                    self.snake.grow()
                
                self.foods.remove(food)
                
                if self.score >= self.level * 5:
                    self.level += 1
                    self.speed = min(8 + (self.level - 1) * 2, 30)
                    if self.level >= 3:
                        self.spawn_obstacles()
                break
        
        for power_up in self.power_ups[:]:
            if head == power_up.position:
                current_time = time.time()
                if power_up.type == "speed_boost":
                    self.active_effects["speed_boost"] = current_time + power_up.effect_duration
                elif power_up.type == "slow_motion":
                    self.active_effects["slow_motion"] = current_time + power_up.effect_duration
                elif power_up.type == "shield":
                    self.active_effects["shield"] = current_time + power_up.effect_duration
                self.power_ups.remove(power_up)
                break
        
        self.foods = [f for f in self.foods if not f.is_expired()]
        self.power_ups = [p for p in self.power_ups if not p.is_expired()]
        
        if time.time() - self.last_food_spawn > 3 and len(self.foods) < 5:
            self.foods.append(WeightedFood(self.snake.body, self.wall.positions,
                                          [obs.position for obs in self.obstacles]))
            self.last_food_spawn = time.time()
        
        if len(self.power_ups) == 0 and time.time() - self.last_power_up_spawn > 12:
            self.power_ups.append(PowerUp(self.snake.body, self.wall.positions,
                                         [obs.position for obs in self.obstacles]))
            self.last_power_up_spawn = time.time()
    
    def draw(self, screen, font, small_font):
        screen.fill(BLACK)
        
        if self.config.get("grid_overlay"):
            for x in range(0, SCREEN_WIDTH, CELL_SIZE):
                pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
            for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
                pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))
        
        for food in self.foods:
            food.draw(screen, small_font)
        
        for power_up in self.power_ups:
            power_up.draw(screen, small_font)
        
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        
        self.wall.draw(screen)
        self.snake.draw(screen, tuple(self.config.get("snake_color")))
        
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (SCREEN_WIDTH - 100, 10))
        
        y_offset = 70
        if self.active_effects["speed_boost"] > 0:
            effect_text = small_font.render("SPEED BOOST ACTIVE", True, CYAN)
            screen.blit(effect_text, (10, y_offset))
            y_offset += 20
        if self.active_effects["slow_motion"] > 0:
            effect_text = small_font.render("SLOW MOTION ACTIVE", True, PURPLE)
            screen.blit(effect_text, (10, y_offset))
            y_offset += 20
        if self.active_effects["shield"] > 0:
            remaining = int(self.active_effects["shield"] - time.time())
            effect_text = small_font.render(f"SHIELD ACTIVE: {remaining}s", True, BLUE)
            screen.blit(effect_text, (10, y_offset))