import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint App - Draw Shapes")

# Toolbar dimensions
TOOLBAR_HEIGHT = 80
canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

# Current tool and color
current_tool = "brush"  # brush, rect, circle, eraser
current_color = BLACK
brush_size = 5

# Font
font = pygame.font.SysFont("Arial", 20)

def draw_toolbar():
    """Draw the toolbar with buttons"""
    toolbar_rect = pygame.Rect(0, SCREEN_HEIGHT - TOOLBAR_HEIGHT, SCREEN_WIDTH, TOOLBAR_HEIGHT)
    pygame.draw.rect(screen, (200, 200, 200), toolbar_rect)
    pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT - TOOLBAR_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT - TOOLBAR_HEIGHT), 3)
    
    # Tool buttons
    buttons = {
        "brush": (10, SCREEN_HEIGHT - 65, 60, 50),
        "rect": (80, SCREEN_HEIGHT - 65, 60, 50),
        "circle": (150, SCREEN_HEIGHT - 65, 60, 50),
        "eraser": (220, SCREEN_HEIGHT - 65, 60, 50),
    }
    
    # Color buttons - Task 4: Color selection
    colors = {
        BLACK: (300, SCREEN_HEIGHT - 65, 40, 40),
        RED: (350, SCREEN_HEIGHT - 65, 40, 40),
        GREEN: (400, SCREEN_HEIGHT - 65, 40, 40),
        BLUE: (450, SCREEN_HEIGHT - 65, 40, 40),
        YELLOW: (500, SCREEN_HEIGHT - 65, 40, 40),
        PURPLE: (550, SCREEN_HEIGHT - 65, 40, 40),
        CYAN: (600, SCREEN_HEIGHT - 65, 40, 40),
    }
    
    # Draw tool buttons
    for tool, rect in buttons.items():
        if current_tool == tool:
            pygame.draw.rect(screen, (150, 150, 150), rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        # Add text to button
        text = font.render(tool[:3], True, BLACK)
        screen.blit(text, (rect[0] + 10, rect[1] + 15))
        
    # Draw color buttons - Task 4
    for color, rect in colors.items():
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        if current_color == color:
            pygame.draw.rect(screen, (255, 255, 255), rect, 3)
            
    # Show brush size
    size_text = font.render(f"Size: {brush_size}", True, BLACK)
    screen.blit(size_text, (680, SCREEN_HEIGHT - 60))
    
    # Instructions
    inst_text = font.render("+ / -", True, BLACK)
    screen.blit(inst_text, (680,  SCREEN_HEIGHT - 30))

def draw_shape(start_pos, end_pos, shape, color):
    """Draw rectangle or circle"""
    x1, y1 = start_pos
    x2, y2 = end_pos
    
    if shape == "rect":
        # Task 1: Draw rectangle
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(canvas, color, rect, 2)
    elif shape == "circle":
        # Task 2: Draw circle
        radius = int(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))
        center = (x1, y1)
        pygame.draw.circle(canvas, color, center, radius, 2)

def draw_brush(pos, color, size):
    """Draw with brush"""
    pygame.draw.circle(canvas, color, pos, size)

def draw_eraser(pos, size):
    """Eraser tool - Task 3"""
    pygame.draw.circle(canvas, WHITE, pos, size)

# Game variables
drawing = False
start_pos = None
last_pos = None

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            # Check if clicking on toolbar buttons
            if mouse_y > SCREEN_HEIGHT - TOOLBAR_HEIGHT:
                # Check tool buttons
                if 10 <= mouse_x <= 70:
                    current_tool = "brush"
                elif 80 <= mouse_x <= 140:
                    current_tool = "rect"
                elif 150 <= mouse_x <= 210:
                    current_tool = "circle"
                elif 220 <= mouse_x <= 280:
                    current_tool = "eraser"
                # Check color buttons - Task 4
                elif 300 <= mouse_x <= 340:
                    current_color = BLACK
                elif 350 <= mouse_x <= 390:
                    current_color = RED
                elif 400 <= mouse_x <= 440:
                    current_color = GREEN
                elif 450 <= mouse_x <= 490:
                    current_color = BLUE
                elif 500 <= mouse_x <= 540:
                    current_color = YELLOW
                elif 550 <= mouse_x <= 590:
                    current_color = PURPLE
                elif 600 <= mouse_x <= 640:
                    current_color = CYAN
            else:
                # Start drawing on canvas
                drawing = True
                start_pos = (mouse_x, mouse_y)
                last_pos = (mouse_x, mouse_y)
                
                # For brush and eraser, draw single dot
                if current_tool == "brush":
                    draw_brush((mouse_x, mouse_y), current_color, brush_size)
                elif current_tool == "eraser":
                    draw_eraser((mouse_x, mouse_y), brush_size)
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            # Finish drawing shape
            if drawing and current_tool in ["rect", "circle"]:
                end_pos = pygame.mouse.get_pos()
                draw_shape(start_pos, end_pos, current_tool, current_color)
            drawing = False
            
        elif event.type == pygame.MOUSEMOTION and drawing:
            mouse_x, mouse_y = event.pos
            # Don't draw if mouse is on toolbar
            if mouse_y < SCREEN_HEIGHT - TOOLBAR_HEIGHT:
                if current_tool == "brush":
                    draw_brush((mouse_x, mouse_y), current_color, brush_size)
                elif current_tool == "eraser":
                    draw_eraser((mouse_x, mouse_y), brush_size)
                    
        elif event.type == pygame.KEYDOWN:
            # Change brush size with +/- keys
            if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                brush_size = min(brush_size + 1, 30)
            elif event.key == pygame.K_MINUS:
                brush_size = max(brush_size - 1, 1)
                
    # Draw everything
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))
    draw_toolbar()
    
    # Update display
    pygame.display.update()
    
pygame.quit()
sys.exit()