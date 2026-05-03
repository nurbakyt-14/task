import pygame
import math
from datetime import datetime


def flood_fill(canvas, pos, target_color, replacement_color):
    if target_color == replacement_color:
        return False
    
    # Get canvas size
    canvas_width, canvas_height = canvas.get_size()
    
    # Check if position is inside canvas
    if pos[0] < 0 or pos[0] >= canvas_width or pos[1] < 0 or pos[1] >= canvas_height:
        return False
    
    # Use stack for flood fill
    stack = [pos]
    visited = set()
    
    while stack:
        x, y = stack.pop()
        
        # Check boundaries
        if x < 0 or x >= canvas_width or y < 0 or y >= canvas_height:
            continue
        
        # Skip if already visited
        if (x, y) in visited:
            continue
        
        # Get current pixel color
        current_color = canvas.get_at((x, y))[:3]
        
        # Skip if color doesn't match target
        if current_color != target_color:
            continue
        
        # Fill the pixel
        canvas.set_at((x, y), replacement_color)
        visited.add((x, y))
        
        # Add 4 neighbor pixels
        stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
    
    return True


def save_canvas(canvas):
    # Create filename with current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"canvas_{timestamp}.png"
    # Save canvas as PNG file
    pygame.image.save(canvas, filename)
    return filename


def place_text_on_canvas(canvas, text, position, color, font_size=24):
    # Create font and render text
    font = pygame.font.SysFont("Arial", font_size)
    text_surface = font.render(text, True, color)
    # Draw text on canvas
    canvas.blit(text_surface, position)
    return text_surface


def draw_line(canvas, start, end, color, size):
    # Draw straight line
    pygame.draw.line(canvas, color, start, end, size)


def preview_line(surface, start, end, color, size):
    # Create copy and draw line for preview
    temp = surface.copy()
    pygame.draw.line(temp, color, start, end, size)
    return temp


def preview_rectangle(surface, start, end, color, size):
    # Create copy and draw rectangle for preview
    temp = surface.copy()
    x1, y1 = start
    x2, y2 = end
    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
    pygame.draw.rect(temp, color, rect, size)
    return temp


def preview_circle(surface, start, end, color, size):
    # Create copy and draw circle for preview
    temp = surface.copy()
    x1, y1 = start
    x2, y2 = end
    radius = int(math.sqrt((x2 - x1)**2 + (y2 - y1)**2))
    pygame.draw.circle(temp, color, (x1, y1), radius, size)
    return temp


def preview_square(surface, start, end, color, size):
    # Create copy and draw square for preview
    temp = surface.copy()
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
        pygame.draw.rect(temp, color, rect, size)
    
    return temp


def preview_right_triangle(surface, start, end, color, size):
    # Create copy and draw right triangle for preview
    temp = surface.copy()
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(temp, color, points, size)
    return temp


def preview_equilateral_triangle(surface, start, end, color, size):
    # Create copy and draw equilateral triangle for preview
    temp = surface.copy()
    x1, y1 = start
    x2, y2 = end
    side = abs(x2 - x1)
    
    if side > 0:
        height = side * math.sqrt(3) / 2
        if y2 > y1:
            points = [(x1, y1), (x1 + side, y1), (x1 + side/2, y1 + height)]
        else:
            points = [(x1, y1), (x1 + side, y1), (x1 + side/2, y1 - height)]
        pygame.draw.polygon(temp, color, points, size)
    
    return temp


def preview_rhombus(surface, start, end, color, size):
    # Create copy and draw rhombus for preview
    temp = surface.copy()
    x1, y1 = start
    x2, y2 = end
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    width = abs(x2 - x1) // 2
    height = abs(y2 - y1) // 2
    
    if width > 0 and height > 0:
        points = [(center_x, center_y - height), (center_x + width, center_y),
                 (center_x, center_y + height), (center_x - width, center_y)]
        pygame.draw.polygon(temp, color, points, size)
    
    return temp