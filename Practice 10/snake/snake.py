import pygame
import random
import sys

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

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game with Levels")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)
big_font = pygame.font.SysFont("Arial", 50)  # NEW: for Game Over text

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

class Food:
    """Food class"""
    def __init__(self, snake_body, walls):
        self.position = self.get_random_position(snake_body, walls)
        
    def get_random_position(self, snake_body, walls):
        """Generate random position for food so that it does not fall on a wall or a snake - Task 2"""
        while True:
            x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            pos = (x, y)
            if pos not in snake_body and pos not in walls:
                return pos
                
    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

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

#NEW: GAME OVER MENU FUNCTION
def show_game_over_menu(score, level):
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

#NEW: RESET GAME FUNCTION
def reset_game():
    """Reset all game variables to initial state"""
    global snake, wall, food, score, level, speed
    
    snake = Snake()
    wall = Wall()
    score = 0
    level = 1
    speed = 8
    food = Food(snake.body, wall.positions)

# NEW: MAIN GAME FUNCTION (encapsulated) 
def run_game():
    """Main game function - returns "restart" or "quit"""
    global snake, wall, food, score, level, speed
    
    reset_game()
    
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
                elif event.key == pygame.K_ESCAPE:  # NEW: ESC to quit
                    result = show_game_over_menu(score, level)
                    return result
                    
        snake.move()
        
        # Check border collision - Task 1
        if wall.check_collision(snake.body[0]):
            result = show_game_over_menu(score, level)
            return result
            
        # Check self collision
        if snake.check_self_collision():
            result = show_game_over_menu(score, level)
            return result
            
        # Eat food
        if snake.body[0] == food.position:
            snake.grow()
            score += 10
            food = Food(snake.body, wall.positions)
            
            # Level system - Task 3 (every 30 points)
            if score % 30 == 0:
                level += 1
                speed += 2  # Task 4: Increase speed
                
        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        wall.draw(screen)
        show_score_and_level(score, level)
        
        pygame.display.update()
        clock.tick(speed)
    
    return "quit"

#NEW: MAIN PROGRAM LOOP WITH RESTART
while True:
    result = run_game()
    if result == "quit":
        break
    # If result == "restart", loop continues and game runs again

pygame.quit()
sys.exit()