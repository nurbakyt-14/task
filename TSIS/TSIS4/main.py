import pygame
import sys
import time
import os
from config import Config
from db import Database
from game import Game, SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game - Advanced")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)
big_font = pygame.font.SysFont("Arial", 50)
medium_font = pygame.font.SysFont("Arial", 35)
small_font = pygame.font.SysFont("Arial", 15)

# Initialize config and database
config = Config()
db = Database()

# Load sound
sound_path = os.path.join("assets", "sound.mp3")
if os.path.exists(sound_path):
    pygame.mixer.music.load(sound_path)

def play_sound():
    if config.get("sound_enabled") and os.path.exists(sound_path):
        pygame.mixer.music.play()

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
    
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class TextInput:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = config.get("username")
        self.active = False
        self.color_inactive = (128, 128, 128)
        self.color_active = (255, 255, 255)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 20:
                    self.text += event.unicode
            config.set("username", self.text)
    
    def draw(self, screen):
        color = self.color_active if self.active else self.color_inactive
        pygame.draw.rect(screen, color, self.rect, 2)
        text_surface = font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
        
        if self.active:
            pygame.draw.line(screen, (255, 255, 255), 
                           (self.rect.x + 5 + text_surface.get_width(), self.rect.y + 5),
                           (self.rect.x + 5 + text_surface.get_width(), self.rect.y + 30), 2)

def main_menu():
    buttons = [
        Button(SCREEN_WIDTH//2 - 100, 250, 200, 50, "PLAY", (0, 255, 0), (0, 100, 0)),
        Button(SCREEN_WIDTH//2 - 100, 320, 200, 50, "LEADERBOARD", (0, 0, 255), (0, 0, 100)),
        Button(SCREEN_WIDTH//2 - 100, 390, 200, 50, "SETTINGS", (255, 165, 0), (139, 69, 19)),
        Button(SCREEN_WIDTH//2 - 100, 460, 200, 50, "QUIT", (255, 0, 0), (139, 0, 0))
    ]
    
    username_input = TextInput(SCREEN_WIDTH//2 - 100, 180, 200, 40)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            username_input.handle_event(event)
            
            for button in buttons:
                if button.handle_event(event):
                    if button.text == "PLAY":
                        return "play"
                    elif button.text == "LEADERBOARD":
                        show_leaderboard()
                    elif button.text == "SETTINGS":
                        show_settings()
                    elif button.text == "QUIT":
                        return "quit"
        
        screen.fill((0, 0, 0))
        
        title_text = big_font.render("SNAKE GAME", True, (255, 255, 255))
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 80))
        
        username_label = font.render("Username:", True, (255, 255, 255))
        screen.blit(username_label, (SCREEN_WIDTH//2 - 100, 150))
        
        username_input.draw(screen)
        
        for button in buttons:
            button.draw(screen)
        
        pygame.display.update()
        clock.tick(60)

def show_leaderboard():
    leaders = db.get_leaderboard()
    
    back_button = Button(SCREEN_WIDTH//2 - 75, SCREEN_HEIGHT - 80, 150, 40, "BACK", (255, 0, 0), (139, 0, 0))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if back_button.handle_event(event):
                return
        
        screen.fill((0, 0, 0))
        
        title_text = big_font.render("LEADERBOARD", True, (255, 255, 0))
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 30))
        
        if leaders:
            headers = ["Rank", "Username", "Score", "Level", "Date"]
            y = 100
            for i, header in enumerate(headers):
                text = font.render(header, True, (255, 255, 255))
                screen.blit(text, (50 + i * 150, y))
            
            y += 30
            for idx, (username, score, level, played_at) in enumerate(leaders[:10], 1):
                rank_text = font.render(str(idx), True, (255, 255, 255))
                username_text = font.render(username[:15], True, (255, 255, 255))
                score_text = font.render(str(score), True, (0, 255, 0) if idx == 1 else (255, 255, 255))
                level_text = font.render(str(level), True, (255, 255, 255))
                date_text = font.render(played_at.strftime("%Y-%m-%d"), True, (128, 128, 128))
                
                screen.blit(rank_text, (50, y))
                screen.blit(username_text, (200, y))
                screen.blit(score_text, (350, y))
                screen.blit(level_text, (500, y))
                screen.blit(date_text, (600, y))
                y += 25
                
                if y > SCREEN_HEIGHT - 100:
                    break
        else:
            no_data_text = font.render("No scores yet. Play the game!", True, (128, 128, 128))
            screen.blit(no_data_text, (SCREEN_WIDTH//2 - no_data_text.get_width()//2, SCREEN_HEIGHT//2))
        
        back_button.draw(screen)
        pygame.display.update()
        clock.tick(60)

def show_settings():
    colors = [
        ([0, 255, 0], "Green"),
        ([255, 0, 0], "Red"),
        ([0, 0, 255], "Blue"),
        ([255, 255, 0], "Yellow"),
        ([255, 0, 255], "Purple"),
        ([0, 255, 255], "Cyan")
    ]
    
    color_buttons = []
    for i, (color, name) in enumerate(colors):
        btn = Button(100 + (i % 3) * 120, 180 + (i // 3) * 60, 100, 40, name, tuple(color), tuple(c//2 for c in color))
        color_buttons.append((btn, color))
    
    grid_button = Button(SCREEN_WIDTH//2 - 150, 300, 130, 40, "Grid: " + ("ON" if config.get("grid_overlay") else "OFF"), 
                         (0, 255, 0) if config.get("grid_overlay") else (255, 0, 0), 
                         (0, 100, 0) if config.get("grid_overlay") else (139, 0, 0))
    
    sound_button = Button(SCREEN_WIDTH//2 + 20, 300, 130, 40, "Sound: " + ("ON" if config.get("sound_enabled") else "OFF"),
                          (0, 255, 0) if config.get("sound_enabled") else (255, 0, 0),
                          (0, 100, 0) if config.get("sound_enabled") else (139, 0, 0))
    
    back_button = Button(SCREEN_WIDTH//2 - 75, SCREEN_HEIGHT - 80, 150, 40, "SAVE & BACK", (0, 255, 0), (0, 100, 0))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            for btn, color in color_buttons:
                if btn.handle_event(event):
                    config.set("snake_color", color)
            
            if grid_button.handle_event(event):
                config.set("grid_overlay", not config.get("grid_overlay"))
                grid_button.text = "Grid: " + ("ON" if config.get("grid_overlay") else "OFF")
                grid_button.color = (0, 255, 0) if config.get("grid_overlay") else (255, 0, 0)
            
            if sound_button.handle_event(event):
                config.set("sound_enabled", not config.get("sound_enabled"))
                sound_button.text = "Sound: " + ("ON" if config.get("sound_enabled") else "OFF")
                sound_button.color = (0, 255, 0) if config.get("sound_enabled") else (255, 0, 0)
                # Stop sound when disabled
                if not config.get("sound_enabled"):
                    pygame.mixer.music.stop()
            
            if back_button.handle_event(event):
                return
        
        screen.fill((0, 0, 0))
        
        title_text = big_font.render("SETTINGS", True, (255, 255, 255))
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 50))
        
        color_label = font.render("Snake Color:", True, (255, 255, 255))
        screen.blit(color_label, (SCREEN_WIDTH//2 - color_label.get_width()//2, 140))
        
        for btn, _ in color_buttons:
            btn.draw(screen)
        
        grid_button.draw(screen)
        sound_button.draw(screen)
        back_button.draw(screen)
        
        pygame.display.update()
        clock.tick(60)

def show_game_over(score, level):
    personal_best = db.get_personal_best(config.get("username"))
    
    retry_button = Button(SCREEN_WIDTH//2 - 160, SCREEN_HEIGHT//2 + 80, 150, 50, "RETRY", (0, 255, 0), (0, 100, 0))
    menu_button = Button(SCREEN_WIDTH//2 + 10, SCREEN_HEIGHT//2 + 80, 150, 50, "MAIN MENU", (0, 0, 255), (0, 0, 100))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if retry_button.handle_event(event):
                return "retry"
            if menu_button.handle_event(event):
                return "menu"
        
        screen.fill((0, 0, 0))
        
        game_over_text = big_font.render("GAME OVER", True, (255, 0, 0))
        final_score_text = medium_font.render(f"Final Score: {score}", True, (255, 255, 255))
        final_level_text = medium_font.render(f"Level Reached: {level}", True, (255, 255, 255))
        
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 120))
        screen.blit(final_score_text, (SCREEN_WIDTH//2 - final_score_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(final_level_text, (SCREEN_WIDTH//2 - final_level_text.get_width()//2, SCREEN_HEIGHT//2))
        
        if personal_best < score:
            best_text = font.render("NEW PERSONAL BEST!", True, (255, 255, 0))
        else:
            best_text = font.render(f"Personal Best: {personal_best}", True, (255, 255, 255))
        screen.blit(best_text, (SCREEN_WIDTH//2 - best_text.get_width()//2, SCREEN_HEIGHT//2 + 30))
        
        retry_button.draw(screen)
        menu_button.draw(screen)
        
        pygame.display.update()
        clock.tick(60)

def play_sound():
    if config.get("sound_enabled") and os.path.exists(os.path.join("assets", "sound.mp3")):
        pygame.mixer.music.play()

# Main game loop
while True:
    menu_result = main_menu()
    
    if menu_result == "quit":
        db.close()
        pygame.quit()
        sys.exit()
    elif menu_result == "play":
        game = Game(config, config.get("username"))
        running = True
        
        last_move = time.time()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    db.close()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game.snake.change_direction((0, -20))
                    elif event.key == pygame.K_DOWN:
                        game.snake.change_direction((0, 20))
                    elif event.key == pygame.K_LEFT:
                        game.snake.change_direction((-20, 0))
                    elif event.key == pygame.K_RIGHT:
                        game.snake.change_direction((20, 0))
                    elif event.key == pygame.K_ESCAPE:
                        game.game_over = True
            
            current_time = time.time()
            if current_time - last_move > 1.0 / game.get_current_speed():
                # Play sound when food is eaten (check if score increased)
                old_score = game.score
                game.update(db)
                if game.score > old_score and config.get("sound_enabled"):
                    play_sound()
                last_move = current_time
            
            game.draw(screen, font, small_font)
            
            # Display personal best
            personal_best = db.get_personal_best(config.get("username"))
            if personal_best > 0:
                best_text = small_font.render(f"Best: {personal_best}", True, (255, 255, 0))
                screen.blit(best_text, (10, 40))
            
            if game.game_over:
                result = show_game_over(game.score, game.level)
                if result == "retry":
                    game = Game(config, config.get("username"))
                else:
                    running = False
            
            pygame.display.update()
            clock.tick(60)