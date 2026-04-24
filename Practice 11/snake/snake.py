import pygame
import random
import sys
import time  # Extra: For timer functionality

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 20

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)    # Extra: For medium food
PURPLE = (128, 0, 128)    # Extra: For heavy food
YELLOW = (255, 255, 0)    # Extra: For special timed food

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game with Levels and Weighted Food")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)
big_font = pygame.font.SysFont("Arial", 50)
small_font = pygame.font.SysFont("Arial", 15)  # Extra: For timer text

class Snake:
    """Snake class"""
    def __init__(self):
        self.body = [(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)]
        self.direction = (CELL_SIZE, 0)  # Start moving right
        self.grow_flag = False
        
    def move(self):
        """Move the snake"""
        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        self.body.insert(0, new_head)
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False
            
    def change_direction(self, new_dir):
        """Control: up, down, left, right"""
        # Cannot reverse direction
        if (new_dir[0] == -self.direction[0] and new_dir[1] == -self.direction[1]):
            return
        self.direction = new_dir
        
    def grow(self):
        """Make snake grow"""
        self.grow_flag = True
        
    def check_self_collision(self):
        """Check if snake collides with itself"""
        head = self.body[0]
        return head in self.body[1:]
        
    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

# Extra: Weighted Food class with different weights and timers
class WeightedFood:
    """Food class with different weights and disappearing timer"""
    
    # Extra: Food weight types
    WEIGHT_LIGHT = 1    # Light food - 1 point, stays 5 seconds
    WEIGHT_MEDIUM = 2   # Medium food - 2 points, stays 3 seconds
    WEIGHT_HEAVY = 3    # Heavy food - 3 points, stays 2 seconds
    
    def __init__(self, snake_body, walls):
        # Extra: Randomly assign weight with different probabilities
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
        
        self.spawn_time = time.time()
        self.position = self.get_random_position(snake_body, walls)
        
    def get_random_position(self, snake_body, walls):
        """Generate random position for food so that it does not fall on a wall or a snake"""
        while True:
            x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            pos = (x, y)
            if pos not in snake_body and pos not in walls:
                return pos
                
    def is_expired(self):
        """Extra: Check if food has expired based on its duration"""
        return time.time() - self.spawn_time > self.duration
    
    def get_remaining_time(self):
        """Extra: Get remaining time in seconds"""
        remaining = max(0, self.duration - (time.time() - self.spawn_time))
        return remaining
                
    def draw(self, screen):
        """Draw food with timer indicator"""
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))
        
        # Extra: Draw timer indicator (thin bar at the top of food)
        remaining_percent = self.get_remaining_time() / self.duration
        bar_height = 3
        bar_width = int(CELL_SIZE * remaining_percent)
        bar_rect = pygame.Rect(self.position[0], self.position[1], bar_width, bar_height)
        pygame.draw.rect(screen, YELLOW, bar_rect)
        
        # Extra: Draw value text on food
        value_text = small_font.render(str(self.value), True, WHITE)
        text_rect = value_text.get_rect(center=(self.position[0] + CELL_SIZE//2, 
                                                 self.position[1] + CELL_SIZE//2))
        screen.blit(value_text, text_rect)

class Wall:
    """Wall class - Task 1: border collision detection"""
    def __init__(self):
        self.positions = []
        # Border walls
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            self.positions.append((x, 0))  # Top wall
            self.positions.append((x, SCREEN_HEIGHT - CELL_SIZE))  # Bottom wall
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            self.positions.append((0, y))  # Left wall
            self.positions.append((SCREEN_WIDTH - CELL_SIZE, y))  # Right wall
            
    def check_collision(self, head):
        """Check collision with wall - Task 1"""
        return head in self.positions
        
    def draw(self, screen):
        for pos in self.positions:
            pygame.draw.rect(screen, BLUE, (pos[0], pos[1], CELL_SIZE, CELL_SIZE))

def show_score_and_level(score, level):
    """Display score and level counter - Task 5"""
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (SCREEN_WIDTH - 100, 10))

# Extra: Show food info on screen
def show_food_info(food_count, expired_count):
    """Display active foods and expired foods count"""
    food_text = small_font.render(f"Active Foods: {food_count}", True, WHITE)
    expired_text = small_font.render(f"Expired: {expired_count}", True, WHITE)
    screen.blit(food_text, (10, 40))
    screen.blit(expired_text, (10, 60))

def show_game_over_menu(score, level, expired_foods=0):
    """
    Show Game Over menu with Restart and Quit options
    Returns: "restart" or "quit"
    """
    # Darken the background
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # Game Over text
    game_over_text = big_font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                                  SCREEN_HEIGHT//2 - 100))
    
    # Final statistics
    final_score_text = font.render(f"Final Score: {score}", True, WHITE)
    final_level_text = font.render(f"Level Reached: {level}", True, WHITE)
    
    screen.blit(final_score_text, (SCREEN_WIDTH//2 - final_score_text.get_width()//2, 
                                    SCREEN_HEIGHT//2 - 20))
    screen.blit(final_level_text, (SCREEN_WIDTH//2 - final_level_text.get_width()//2, 
                                    SCREEN_HEIGHT//2 + 20))
    
    # Extra: Show expired foods count
    expired_text = small_font.render(f"Foods Expired: {expired_foods}", True, YELLOW)
    screen.blit(expired_text, (SCREEN_WIDTH//2 - expired_text.get_width()//2, 
                                SCREEN_HEIGHT//2 + 50))
    
    # Button dimensions
    button_width = 150
    button_height = 50
    restart_btn = pygame.Rect(SCREEN_WIDTH//2 - button_width - 20, 
                               SCREEN_HEIGHT//2 + 100, 
                               button_width, button_height)
    quit_btn = pygame.Rect(SCREEN_WIDTH//2 + 20, 
                           SCREEN_HEIGHT//2 + 100, 
                           button_width, button_height)
    
    # Draw buttons
    pygame.draw.rect(screen, GREEN, restart_btn)
    pygame.draw.rect(screen, RED, quit_btn)
    pygame.draw.rect(screen, WHITE, restart_btn, 2)
    pygame.draw.rect(screen, WHITE, quit_btn, 2)
    
    # Button text
    restart_text = font.render("RESTART", True, BLACK)
    quit_text = font.render("QUIT", True, WHITE)
    
    screen.blit(restart_text, (restart_btn.x + restart_btn.width//2 - restart_text.get_width()//2,
                                restart_btn.y + restart_btn.height//2 - restart_text.get_height()//2))
    screen.blit(quit_text, (quit_btn.x + quit_btn.width//2 - quit_text.get_width()//2,
                            quit_btn.y + quit_btn.height//2 - quit_text.get_height()//2))
    
    # Instruction text
    inst_text = font.render("Press R to Restart, Q to Quit", True, WHITE)
    screen.blit(inst_text, (SCREEN_WIDTH//2 - inst_text.get_width()//2, 
                            SCREEN_HEIGHT//2 + 170))
    
    pygame.display.update()
    
    # Wait for user input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if restart_btn.collidepoint(mouse_pos):
                    return "restart"
                elif quit_btn.collidepoint(mouse_pos):
                    return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                elif event.key == pygame.K_q:
                    return "quit"
        clock.tick(60)

def reset_game():
    """Reset all game variables to initial state"""
    global snake, wall, foods, score, level, speed, expired_foods_count, last_food_spawn
    
    snake = Snake()
    wall = Wall()
    score = 0
    level = 1
    speed = 8
    expired_foods_count = 0  # Extra: Track expired foods
    last_food_spawn = time.time()  # Extra: Track last food spawn time
    foods = [WeightedFood(snake.body, wall.positions)]  # Extra: List of foods

def run_game():
    """Main game function - returns "restart" or "quit"""
    global snake, wall, foods, score, level, speed, expired_foods_count, last_food_spawn
    
    reset_game()
    
    # Extra: Food spawn delay
    FOOD_SPAWN_DELAY = 3  # Spawn new food every 3 seconds
    MAX_FOODS = 5  # Maximum foods on screen
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -CELL_SIZE))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, CELL_SIZE))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-CELL_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((CELL_SIZE, 0))
                elif event.key == pygame.K_ESCAPE:
                    result = show_game_over_menu(score, level, expired_foods_count)
                    return result
        
        # Extra: Spawn new foods periodically
        if time.time() - last_food_spawn > FOOD_SPAWN_DELAY and len(foods) < MAX_FOODS:
            foods.append(WeightedFood(snake.body, wall.positions))
            last_food_spawn = time.time()
        
        # Extra: Check for expired foods and remove them
        for food in foods[:]:
            if food.is_expired():
                foods.remove(food)
                expired_foods_count += 1
                print(f"Food expired! +{food.value} point lost")  # Debug message
                
        snake.move()
        
        # Check border collision - Task 1
        if wall.check_collision(snake.body[0]):
            result = show_game_over_menu(score, level, expired_foods_count)
            return result
            
        # Check self collision
        if snake.check_self_collision():
            result = show_game_over_menu(score, level, expired_foods_count)
            return result
            
        # Extra: Check collision with any food
        for food in foods[:]:
            if snake.body[0] == food.position:
                snake.grow()
                score += food.value  # Add weighted value
                foods.remove(food)
                print(f"Food eaten! +{food.value} points")  # Debug message
                
                # Level system - Task 3 (every 30 points)
                if score % 10 == 0 and score > 0:
                    level += 1
                    speed += 2  # Task 4: Increase speed
                    
        screen.fill(BLACK)
        snake.draw(screen)
        
        # Extra: Draw all foods
        for food in foods:
            food.draw(screen)
            
        wall.draw(screen)
        show_score_and_level(score, level)
        
        # Extra: Show food information
        show_food_info(len(foods), expired_foods_count)
        
        # Extra: Show instructions for weighted food
        inst_text = small_font.render("Food: Red=1pt(5s) Orange=2pt(3s) Purple=3pt(2s)", True, WHITE)
        screen.blit(inst_text, (10, SCREEN_HEIGHT - 30))
        
        pygame.display.update()
        clock.tick(speed)
    
    return "quit"

# Main program loop with restart
while True:
    result = run_game()
    if result == "quit":
        break

pygame.quit()
sys.exit()