import pygame
import sys
import math
from tools import (
    flood_fill, save_canvas, place_text_on_canvas,
    preview_line, preview_rectangle, preview_circle,
    preview_square, preview_right_triangle,
    preview_equilateral_triangle, preview_rhombus,
    draw_line
)

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
TOOLBAR_HEIGHT = 140
RIGHT_PANEL_WIDTH = 120

# Canvas size (drawing area)
CANVAS_WIDTH = SCREEN_WIDTH - RIGHT_PANEL_WIDTH
CANVAS_HEIGHT = SCREEN_HEIGHT - TOOLBAR_HEIGHT

# Color definitions
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
BROWN = (139, 69, 19)
LIME = (50, 205, 50)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
NAVY = (0, 0, 128)
MAROON = (128, 0, 0)
TEAL = (0, 128, 128)
LAVENDER = (230, 230, 250)

# List of all colors
ALL_COLORS = [
    BLACK, WHITE, RED, GREEN, BLUE, YELLOW, PURPLE, CYAN,
    ORANGE, PINK, BROWN, LIME, GOLD, SILVER, NAVY, MAROON, TEAL, LAVENDER
]

# Create screen and canvas
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint App - Extended")
canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
canvas.fill(WHITE)

# Current settings
current_tool = "brush"
current_color = BLACK
brush_size = 5

# Drawing state
drawing = False
start_pos = None
pencil_last_pos = None
brush_last_pos = None

# Text tool state
text_mode = False
text_position = None
text_input = ""
text_font = pygame.font.SysFont("Arial", 28)

# Notification
notification = None
notification_time = 0
notification_message = ""

# Fonts
font = pygame.font.SysFont("Arial", 14)

def draw_continuous_line(canvas_surface, pos1, pos2, color, size):
    """Draw continuous line between two points"""
    x1, y1 = pos1
    x2, y2 = pos2
    
    distance = int(math.hypot(x2 - x1, y2 - y1))
    
    if distance == 0:
        pygame.draw.circle(canvas_surface, color, pos1, size)
    else:
        for i in range(distance + 1):
            t = i / distance
            x = int(x1 + t * (x2 - x1))
            y = int(y1 + t * (y2 - y1))
            pygame.draw.circle(canvas_surface, color, (x, y), size)

def show_message(msg):
    global notification, notification_time, notification_message
    notification = True
    notification_message = msg
    notification_time = pygame.time.get_ticks()

def draw_notification():
    global notification
    if notification:
        current_time = pygame.time.get_ticks()
        if current_time - notification_time < 2000:
            text = font.render(notification_message, True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - TOOLBAR_HEIGHT - 20))
            bg_rect = text_rect.inflate(20, 10)
            pygame.draw.rect(screen, (200, 200, 200), bg_rect)
            pygame.draw.rect(screen, BLACK, bg_rect, 2)
            screen.blit(text, text_rect)
        else:
            notification = False

def draw_toolbar():
    # Draw bottom toolbar with buttons
    toolbar_rect = pygame.Rect(0, SCREEN_HEIGHT - TOOLBAR_HEIGHT, CANVAS_WIDTH, TOOLBAR_HEIGHT)
    pygame.draw.rect(screen, (200, 200, 200), toolbar_rect)
    pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT - TOOLBAR_HEIGHT), (CANVAS_WIDTH, SCREEN_HEIGHT - TOOLBAR_HEIGHT), 3)
    
    # Row 1 - Basic tools
    buttons_row1 = {
        "brush": (10, SCREEN_HEIGHT - 125, 55, 30),
        "rect": (70, SCREEN_HEIGHT - 125, 55, 30),
        "circle": (130, SCREEN_HEIGHT - 125, 55, 30),
        "eraser": (190, SCREEN_HEIGHT - 125, 55, 30),
        "pencil": (250, SCREEN_HEIGHT - 125, 55, 30),
        "line": (310, SCREEN_HEIGHT - 125, 55, 30),
    }
    
    # Row 2 - Shapes
    buttons_row2 = {
        "square": (10, SCREEN_HEIGHT - 90, 55, 28),
        "right_triangle": (70, SCREEN_HEIGHT - 90, 55, 28),
        "equilateral_triangle": (130, SCREEN_HEIGHT - 90, 55, 28),
        "rhombus": (190, SCREEN_HEIGHT - 90, 55, 28),
        "fill": (250, SCREEN_HEIGHT - 90, 55, 28),
        "text": (310, SCREEN_HEIGHT - 90, 55, 28),
    }
    
    # Row 3 - Utility
    buttons_row3 = {
        "clear": (10, SCREEN_HEIGHT - 55, 60, 28),
        "save": (75, SCREEN_HEIGHT - 55, 60, 28),
    }
    
    # Draw row 1 buttons
    for tool, rect in buttons_row1.items():
        if current_tool == tool:
            pygame.draw.rect(screen, (150, 150, 150), rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        if tool == "pencil":
            text = font.render("Pen", True, BLACK)
        elif tool == "line":
            text = font.render("Line", True, BLACK)
        else:
            text = font.render(tool[:4], True, BLACK)
        screen.blit(text, (rect[0] + 12, rect[1] + 8))
    
    # Draw row 2 buttons
    for tool, rect in buttons_row2.items():
        if current_tool == tool:
            pygame.draw.rect(screen, (150, 150, 150), rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        if tool == "square":
            text = font.render("Sq", True, BLACK)
        elif tool == "right_triangle":
            text = font.render("RTri", True, BLACK)
        elif tool == "equilateral_triangle":
            text = font.render("ETri", True, BLACK)
        elif tool == "rhombus":
            text = font.render("Rho", True, BLACK)
        elif tool == "fill":
            text = font.render("Fill", True, BLACK)
        elif tool == "text":
            text = font.render("Text", True, BLACK)
        else:
            text = font.render(tool[:4], True, BLACK)
        screen.blit(text, (rect[0] + 12, rect[1] + 6))
    
    # Draw row 3 buttons
    for tool, rect in buttons_row3.items():
        if current_tool == tool:
            pygame.draw.rect(screen, (150, 150, 150), rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        text = font.render(tool.capitalize(), True, BLACK)
        screen.blit(text, (rect[0] + 12, rect[1] + 6))
    
    # Show brush size
    size_text = font.render(f"Size: {brush_size}", True, BLACK)
    screen.blit(size_text, (400, SCREEN_HEIGHT - 55))
    
    # Instructions
    inst_text = font.render("+/-:Size | 1,2,3:Size | Ctrl+S:Save | Text:Click+Type", True, BLACK)
    screen.blit(inst_text, (400, SCREEN_HEIGHT - 35))

def draw_right_panel():
    # Draw right panel with color buttons
    panel_rect = pygame.Rect(CANVAS_WIDTH, 0, RIGHT_PANEL_WIDTH, SCREEN_HEIGHT)
    pygame.draw.rect(screen, (180, 180, 180), panel_rect)
    pygame.draw.line(screen, BLACK, (CANVAS_WIDTH, 0), (CANVAS_WIDTH, SCREEN_HEIGHT), 3)
    
    # Panel title
    title_font = pygame.font.SysFont("Arial", 16, bold=True)
    title = title_font.render("COLORS", True, BLACK)
    screen.blit(title, (CANVAS_WIDTH + 25, 10))
    pygame.draw.line(screen, BLACK, (CANVAS_WIDTH + 10, 35), (SCREEN_WIDTH - 10, 35), 1)
    
    # Draw color buttons in grid
    color_size = 35
    colors_per_row = 2
    start_x = CANVAS_WIDTH + 15
    start_y = 50
    spacing = color_size + 5
    
    # Store color buttons for click detection
    self.color_buttons = []
    
    for i, color in enumerate(ALL_COLORS):
        row = i // colors_per_row
        col = i % colors_per_row
        x = start_x + col * spacing
        y = start_y + row * spacing
        
        if y + color_size < SCREEN_HEIGHT - 10:
            rect = pygame.Rect(x, y, color_size, color_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            
            # Highlight current color
            if color == current_color:
                pygame.draw.rect(screen, YELLOW, rect, 3)
            
            self.color_buttons.append((rect, color))
    
    # Show brush size on panel
    size_y = SCREEN_HEIGHT - 80
    size_label = font.render("BRUSH", True, BLACK)
    screen.blit(size_label, (CANVAS_WIDTH + 30, size_y))
    size_value = font.render(str(brush_size), True, BLACK)
    screen.blit(size_value, (CANVAS_WIDTH + 40, size_y + 20))

def draw_square(start, end, color, thickness):
    x1, y1 = start
    x2, y2 = end
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

def draw_right_triangle(start, end, color, thickness):
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(canvas, color, points, thickness)

def draw_equilateral_triangle(start, end, color, thickness):
    x1, y1 = start
    x2, y2 = end
    side = abs(x2 - x1)
    
    if side > 0:
        height = side * math.sqrt(3) / 2
        if y2 > y1:
            points = [(x1, y1), (x1 + side, y1), (x1 + side/2, y1 + height)]
        else:
            points = [(x1, y1), (x1 + side, y1), (x1 + side/2, y1 - height)]
        pygame.draw.polygon(canvas, color, points, thickness)

def draw_rhombus(start, end, color, thickness):
    x1, y1 = start
    x2, y2 = end
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    width = abs(x2 - x1) // 2
    height = abs(y2 - y1) // 2
    
    if width > 0 and height > 0:
        points = [(center_x, center_y - height), (center_x + width, center_y),
                 (center_x, center_y + height), (center_x - width, center_y)]
        pygame.draw.polygon(canvas, color, points, thickness)

def draw_shape(start, end, shape, color):
    if shape == "rect":
        x1, y1 = start
        x2, y2 = end
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(canvas, color, rect, brush_size)
    elif shape == "circle":
        x1, y1 = start
        x2, y2 = end
        radius = int(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))
        pygame.draw.circle(canvas, color, (x1, y1), radius, brush_size)
    elif shape == "square":
        draw_square(start, end, color, brush_size)
    elif shape == "right_triangle":
        draw_right_triangle(start, end, color, brush_size)
    elif shape == "equilateral_triangle":
        draw_equilateral_triangle(start, end, color, brush_size)
    elif shape == "rhombus":
        draw_rhombus(start, end, color, brush_size)
    elif shape == "line":
        draw_line(canvas, start, end, color, brush_size)

def draw_brush(pos, color, size):
    pygame.draw.circle(canvas, color, pos, size)

def draw_eraser(pos, size):
    pygame.draw.circle(canvas, WHITE, pos, size)

def draw_preview():
    if drawing and current_tool in ["rect", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus", "line"] and start_pos:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y < SCREEN_HEIGHT - TOOLBAR_HEIGHT and mouse_x < CANVAS_WIDTH:
            end_pos = (mouse_x, mouse_y)
            
            if current_tool == "line":
                preview = preview_line(canvas, start_pos, end_pos, current_color, brush_size)
            elif current_tool == "rect":
                preview = preview_rectangle(canvas, start_pos, end_pos, current_color, brush_size)
            elif current_tool == "circle":
                preview = preview_circle(canvas, start_pos, end_pos, current_color, brush_size)
            elif current_tool == "square":
                preview = preview_square(canvas, start_pos, end_pos, current_color, brush_size)
            elif current_tool == "right_triangle":
                preview = preview_right_triangle(canvas, start_pos, end_pos, current_color, brush_size)
            elif current_tool == "equilateral_triangle":
                preview = preview_equilateral_triangle(canvas, start_pos, end_pos, current_color, brush_size)
            elif current_tool == "rhombus":
                preview = preview_rhombus(canvas, start_pos, end_pos, current_color, brush_size)
            else:
                return
            
            screen.blit(preview, (0, 0))
            draw_toolbar()
            draw_right_panel()

# Create temporary object for color buttons
class TempObj:
    pass

self = TempObj()
self.color_buttons = []

# Main game loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Text mode handling - priority over other events
        if text_mode:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if text_input and text_position:
                        place_text_on_canvas(canvas, text_input, text_position, current_color, 28)
                    text_mode = False
                    text_input = ""
                    text_position = None
                    current_tool = "brush"
                    show_message("Text placed")
                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text_input = ""
                    text_position = None
                    current_tool = "brush"
                    show_message("Text cancelled")
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                elif event.key == pygame.K_SPACE:
                    text_input += " "
                else:
                    if event.unicode and event.unicode.isprintable():
                        text_input += event.unicode
            continue  # Skip other events while in text mode
        
        # Keyboard shortcuts (only when not in text mode)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                filename = save_canvas(canvas)
                show_message(f"Saved: {filename}")
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                brush_size = min(brush_size + 1, 30)
                show_message(f"Brush size: {brush_size}")
            elif event.key == pygame.K_MINUS:
                brush_size = max(brush_size - 1, 1)
                show_message(f"Brush size: {brush_size}")
            elif event.key == pygame.K_1:
                brush_size = 2
                show_message("Brush size: 2")
            elif event.key == pygame.K_2:
                brush_size = 5
                show_message("Brush size: 5")
            elif event.key == pygame.K_3:
                brush_size = 10
                show_message("Brush size: 10")
        
        # Mouse events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            
            # Check if click is on right panel (colors)
            if mouse_x > CANVAS_WIDTH:
                for rect, color in self.color_buttons:
                    if rect.collidepoint(mouse_x, mouse_y):
                        current_color = color
                        show_message("Color selected")
                        break
            
            # Check if click is on toolbar
            elif mouse_y > SCREEN_HEIGHT - TOOLBAR_HEIGHT:
                # Row 1 buttons
                if SCREEN_HEIGHT - 125 <= mouse_y <= SCREEN_HEIGHT - 95:
                    if 10 <= mouse_x <= 65:
                        current_tool = "brush"
                        show_message("Tool: Brush")
                    elif 70 <= mouse_x <= 125:
                        current_tool = "rect"
                        show_message("Tool: Rectangle")
                    elif 130 <= mouse_x <= 185:
                        current_tool = "circle"
                        show_message("Tool: Circle")
                    elif 190 <= mouse_x <= 245:
                        current_tool = "eraser"
                        show_message("Tool: Eraser")
                        brush_last_pos = None
                    elif 250 <= mouse_x <= 305:
                        current_tool = "pencil"
                        show_message("Tool: Pencil")
                        pencil_last_pos = None
                    elif 310 <= mouse_x <= 365:
                        current_tool = "line"
                        show_message("Tool: Line")
                # Row 2 buttons
                elif SCREEN_HEIGHT - 90 <= mouse_y <= SCREEN_HEIGHT - 62:
                    if 10 <= mouse_x <= 65:
                        current_tool = "square"
                        show_message("Tool: Square")
                    elif 70 <= mouse_x <= 125:
                        current_tool = "right_triangle"
                        show_message("Tool: Right Triangle")
                    elif 130 <= mouse_x <= 185:
                        current_tool = "equilateral_triangle"
                        show_message("Tool: Equilateral Triangle")
                    elif 190 <= mouse_x <= 245:
                        current_tool = "rhombus"
                        show_message("Tool: Rhombus")
                    elif 250 <= mouse_x <= 305:
                        current_tool = "fill"
                        show_message("Tool: Flood Fill")
                    elif 310 <= mouse_x <= 365:
                        current_tool = "text"
                        show_message("Tool: Text - Click on canvas to type")
                # Row 3 buttons
                elif SCREEN_HEIGHT - 55 <= mouse_y <= SCREEN_HEIGHT - 27:
                    if 10 <= mouse_x <= 70:
                        canvas.fill(WHITE)
                        show_message("Canvas cleared")
                    elif 75 <= mouse_x <= 135:
                        filename = save_canvas(canvas)
                        show_message(f"Saved: {filename}")
            else:
                # Start drawing on canvas
                if mouse_x < CANVAS_WIDTH and mouse_y < SCREEN_HEIGHT - TOOLBAR_HEIGHT:
                    canvas_pos = (mouse_x, mouse_y)
                    start_pos = canvas_pos
                    pencil_last_pos = canvas_pos
                    brush_last_pos = canvas_pos
                    
                    # Text tool - activate text mode
                    if current_tool == "text":
                        text_mode = True
                        text_position = canvas_pos
                        text_input = ""
                        show_message("Type text, press Enter to place, ESC to cancel")
                    
                    # Flood fill tool
                    elif current_tool == "fill":
                        target_color = canvas.get_at(canvas_pos)[:3]
                        flood_fill(canvas, canvas_pos, target_color, current_color)
                        show_message("Area filled!")
                    
                    # Other tools
                    else:
                        drawing = True
                        if current_tool == "brush":
                            draw_brush(canvas_pos, current_color, brush_size)
                        elif current_tool == "eraser":
                            draw_eraser(canvas_pos, brush_size)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing and current_tool in ["rect", "circle", "square", "right_triangle", "equilateral_triangle", "rhombus", "line"]:
                end_pos = pygame.mouse.get_pos()
                if end_pos[1] < SCREEN_HEIGHT - TOOLBAR_HEIGHT and end_pos[0] < CANVAS_WIDTH:
                    if abs(end_pos[0] - start_pos[0]) > 3 or abs(end_pos[1] - start_pos[1]) > 3:
                        draw_shape(start_pos, end_pos, current_tool, current_color)
            drawing = False
            pencil_last_pos = None
            brush_last_pos = None
        
        elif event.type == pygame.MOUSEMOTION and drawing:
            mouse_x, mouse_y = event.pos
            if mouse_y < SCREEN_HEIGHT - TOOLBAR_HEIGHT and mouse_x < CANVAS_WIDTH:
                canvas_pos = (mouse_x, mouse_y)
                
                if current_tool == "brush":
                    if brush_last_pos:
                        draw_continuous_line(canvas, brush_last_pos, canvas_pos, current_color, brush_size)
                    draw_brush(canvas_pos, current_color, brush_size)
                    brush_last_pos = canvas_pos
                elif current_tool == "eraser":
                    if brush_last_pos:
                        draw_continuous_line(canvas, brush_last_pos, canvas_pos, WHITE, brush_size)
                    draw_eraser(canvas_pos, brush_size)
                    brush_last_pos = canvas_pos
                elif current_tool == "pencil":
                    if pencil_last_pos:
                        pygame.draw.line(canvas, current_color, pencil_last_pos, canvas_pos, brush_size)
                    pencil_last_pos = canvas_pos
    
    # Draw everything on screen
    screen.fill(WHITE)
    screen.blit(canvas, (0, 0))
    
    # Draw preview while dragging
    draw_preview()
    
    # Draw toolbar and color panel
    draw_toolbar()
    draw_right_panel()
    
    # Draw text preview if in text mode
    if text_mode and text_position:
        preview_text = text_input + "|"
        text_surface = text_font.render(preview_text, True, current_color)
        screen.blit(text_surface, text_position)
    
    draw_notification()
    
    pygame.display.update()

pygame.quit()
sys.exit()