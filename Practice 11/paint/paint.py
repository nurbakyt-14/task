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
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint App - Draw Shapes (Extended)")

# Toolbar dimensions
TOOLBAR_HEIGHT = 80
canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

# Current tool and color
current_tool = "brush"
current_color = BLACK
brush_size = 5

# Drawing state
drawing = False
start_pos = None
last_pos = None
shape_start_pos = None

# Font
font = pygame.font.SysFont("Arial", 20)
small_font = pygame.font.SysFont("Arial", 14)

def draw_toolbar():
    """Draw the toolbar with buttons"""
    toolbar_rect = pygame.Rect(0, SCREEN_HEIGHT - TOOLBAR_HEIGHT, SCREEN_WIDTH, TOOLBAR_HEIGHT)
    pygame.draw.rect(screen, (200, 200, 200), toolbar_rect)
    pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT - TOOLBAR_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT - TOOLBAR_HEIGHT), 3)
    
    # Row 1: Basic tools (Y coordinate: SCREEN_HEIGHT - 65)
    buttons_row1 = {
        "brush": (10, SCREEN_HEIGHT - 65, 60, 30),
        "rect": (80, SCREEN_HEIGHT - 65, 60, 30),
        "circle": (150, SCREEN_HEIGHT - 65, 60, 30),
        "eraser": (220, SCREEN_HEIGHT - 65, 60, 30),
    }
    
    # Row 2: Extended shapes (Y coordinate: SCREEN_HEIGHT - 30)
    buttons_row2 = {
        "square": (10, SCREEN_HEIGHT - 30, 60, 25),
        "right_triangle": (80, SCREEN_HEIGHT - 30, 60, 25),
        "equilateral_triangle": (150, SCREEN_HEIGHT - 30, 60, 25),
        "rhombus": (220, SCREEN_HEIGHT - 30, 60, 25),
    }
    
    # Color buttons
    colors = {
        BLACK: (300, SCREEN_HEIGHT - 65, 35, 35),
        RED: (340, SCREEN_HEIGHT - 65, 35, 35),
        GREEN: (380, SCREEN_HEIGHT - 65, 35, 35),
        BLUE: (420, SCREEN_HEIGHT - 65, 35, 35),
        YELLOW: (460, SCREEN_HEIGHT - 65, 35, 35),
        PURPLE: (500, SCREEN_HEIGHT - 65, 35, 35),
        CYAN: (540, SCREEN_HEIGHT - 65, 35, 35),
        ORANGE: (580, SCREEN_HEIGHT - 65, 35, 35),
        PINK: (620, SCREEN_HEIGHT - 65, 35, 35),
    }
    
    # Draw row 1 buttons
    for tool, rect in buttons_row1.items():
        if current_tool == tool:
            pygame.draw.rect(screen, (150, 150, 150), rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        text = font.render(tool[:4], True, BLACK)
        screen.blit(text, (rect[0] + 10, rect[1] + 8))
    
    # Draw row 2 buttons (extended shapes)
    for tool, rect in buttons_row2.items():
        if current_tool == tool:
            pygame.draw.rect(screen, (150, 150, 150), rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        # Set appropriate text for each shape
        if tool == "square":
            text = font.render("Sq", True, BLACK)
        elif tool == "right_triangle":
            text = font.render("RTri", True, BLACK)
        elif tool == "equilateral_triangle":
            text = font.render("ETri", True, BLACK)
        elif tool == "rhombus":
            text = font.render("Rho", True, BLACK)
        else:
            text = font.render(tool[:4], True, BLACK)
        screen.blit(text, (rect[0] + 15, rect[1] + 5))
    
    # Draw color buttons
    for color, rect in colors.items():
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        if current_color == color:
            pygame.draw.rect(screen, (255, 255, 255), rect, 3)
    
    # Show brush size
    size_text = font.render(f"Size: {brush_size}", True, BLACK)
    screen.blit(size_text, (680, SCREEN_HEIGHT - 60))

    
    # Instructions
    inst_text = small_font.render("+/-:Size", True, BLACK)
    screen.blit(inst_text, (740, SCREEN_HEIGHT - 28))

def draw_square(start_pos, end_pos, color, thickness):
    """Draw a perfect square"""
    x1, y1 = start_pos
    x2, y2 = end_pos
    
    side = min(abs(x2 - x1), abs(y2 - y1))
    
    if side > 0:
        if x2 >= x1 and y2 >= y1:
            rect = pygame.Rect(x1, y1, side, side)
        elif x2 >= x1 and y2 < y1:
            rect = pygame.Rect(x1, y1 - side, side, side)
        elif x2 < x1 and y2 >= y1:
            rect = pygame.Rect(x1 - side, y1, side, side)
        else:
            rect = pygame.Rect(x1 - side, y1 - side, side, side)
        
        pygame.draw.rect(canvas, color, rect, thickness)

def draw_right_triangle(start_pos, end_pos, color, thickness):
    """Draw a right triangle"""
    x1, y1 = start_pos
    x2, y2 = end_pos
    
    points = [
        (x1, y1),
        (x1, y2),
        (x2, y2)
    ]
    
    pygame.draw.polygon(canvas, color, points, thickness)

def draw_equilateral_triangle(start_pos, end_pos, color, thickness):
    """Draw an equilateral triangle"""
    x1, y1 = start_pos
    x2, y2 = end_pos
    
    side = abs(x2 - x1)
    if side > 0:
        height = side * math.sqrt(3) / 2
        
        if y2 > y1:
            points = [
                (x1, y1),
                (x1 + side, y1),
                (x1 + side/2, y1 + height)
            ]
        else:
            points = [
                (x1, y1),
                (x1 + side, y1),
                (x1 + side/2, y1 - height)
            ]
        
        pygame.draw.polygon(canvas, color, points, thickness)

def draw_rhombus(start_pos, end_pos, color, thickness):
    """Draw a rhombus (diamond shape)"""
    x1, y1 = start_pos
    x2, y2 = end_pos
    
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    width = abs(x2 - x1) // 2
    height = abs(y2 - y1) // 2
    
    if width > 0 and height > 0:
        points = [
            (center_x, center_y - height),
            (center_x + width, center_y),
            (center_x, center_y + height),
            (center_x - width, center_y)
        ]
        
        pygame.draw.polygon(canvas, color, points, thickness)

def draw_shape(start_pos, end_pos, shape, color):
    """Draw selected shape"""
    if shape == "rect":
        x1, y1 = start_pos
        x2, y2 = end_pos
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(canvas, color, rect, brush_size)
    elif shape == "circle":
        x1, y1 = start_pos
        x2, y2 = end_pos
        radius = int(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))
        pygame.draw.circle(canvas, color, (x1, y1), radius, brush_size)
    elif shape == "square":
        draw_square(start_pos, end_pos, color, brush_size)
    elif shape == "right_triangle":
        draw_right_triangle(start_pos, end_pos, color, brush_size)
    elif shape == "equilateral_triangle":
        draw_equilateral_triangle(start_pos, end_pos, color, brush_size)
    elif shape == "rhombus":
        draw_rhombus(start_pos, end_pos, color, brush_size)

def draw_brush(pos, color, size):
    """Draw with brush"""
    pygame.draw.circle(canvas, color, pos, size)

def draw_eraser(pos, size):
    """Eraser tool"""
    pygame.draw.circle(canvas, WHITE, pos, size)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            # Check if clicking on toolbar
            if mouse_y > SCREEN_HEIGHT - TOOLBAR_HEIGHT:
                # Row 1 buttons (Y: SCREEN_HEIGHT - 65 to SCREEN_HEIGHT - 35)
                if SCREEN_HEIGHT - 65 <= mouse_y <= SCREEN_HEIGHT - 35:
                    if 10 <= mouse_x <= 70:
                        current_tool = "brush"
                    elif 80 <= mouse_x <= 140:
                        current_tool = "rect"
                    elif 150 <= mouse_x <= 210:
                        current_tool = "circle"
                    elif 220 <= mouse_x <= 280:
                        current_tool = "eraser"
                    # Color buttons
                    elif 300 <= mouse_x <= 335:
                        current_color = BLACK
                    elif 340 <= mouse_x <= 375:
                        current_color = RED
                    elif 380 <= mouse_x <= 415:
                        current_color = GREEN
                    elif 420 <= mouse_x <= 455:
                        current_color = BLUE
                    elif 460 <= mouse_x <= 495:
                        current_color = YELLOW
                    elif 500 <= mouse_x <= 535:
                        current_color = PURPLE
                    elif 540 <= mouse_x <= 575:
                        current_color = CYAN
                    elif 580 <= mouse_x <= 615:
                        current_color = ORANGE
                    elif 620 <= mouse_x <= 655:
                        current_color = PINK
                # Row 2 buttons (Y: SCREEN_HEIGHT - 30 to SCREEN_HEIGHT - 5)
                elif SCREEN_HEIGHT - 30 <= mouse_y <= SCREEN_HEIGHT - 5:
                    if 10 <= mouse_x <= 70:
                        current_tool = "square"
                    elif 80 <= mouse_x <= 140:
                        current_tool = "right_triangle"
                    elif 150 <= mouse_x <= 210:
                        current_tool = "equilateral_triangle"
                    elif 220 <= mouse_x <= 280:
                        current_tool = "rhombus"
                # Clear button
                if 680 <= mouse_x <= 730 and SCREEN_HEIGHT - 35 <= mouse_y <= SCREEN_HEIGHT - 5:
                    canvas.fill(WHITE)
            else:
                # Start drawing on canvas
                drawing = True
                start_pos = (mouse_x, mouse_y)
                shape_start_pos = (mouse_x, mouse_y)
                
                if current_tool == "brush":
                    draw_brush((mouse_x, mouse_y), current_color, brush_size)
                elif current_tool == "eraser":
                    draw_eraser((mouse_x, mouse_y), brush_size)
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            # Finish drawing shape
            if drawing and current_tool in ["rect", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus"]:
                end_pos = pygame.mouse.get_pos()
                if abs(end_pos[0] - start_pos[0]) > 3 or abs(end_pos[1] - start_pos[1]) > 3:
                    draw_shape(start_pos, end_pos, current_tool, current_color)
            drawing = False
            
        elif event.type == pygame.MOUSEMOTION and drawing:
            mouse_x, mouse_y = event.pos
            if mouse_y < SCREEN_HEIGHT - TOOLBAR_HEIGHT:
                if current_tool == "brush":
                    draw_brush((mouse_x, mouse_y), current_color, brush_size)
                elif current_tool == "eraser":
                    draw_eraser((mouse_x, mouse_y), brush_size)
                    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                brush_size = min(brush_size + 1, 30)
            elif event.key == pygame.K_MINUS:
                brush_size = max(brush_size - 1, 1)
    
    # Draw everything
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))
    draw_toolbar()
    
    pygame.display.update()
    
pygame.quit()
sys.exit()