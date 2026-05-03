import pygame
from persistence import load_leaderboard, save_settings

WHITE = (255,255,255)
BLACK = (0,0,0)

def draw_text(screen, text, size, x, y):
    font = pygame.font.SysFont("Verdana", size)
    surf = font.render(text, True, BLACK)
    rect = surf.get_rect(center=(x,y))
    screen.blit(surf, rect)

# ========= MENU =========
def main_menu(screen):
    while True:
        screen.fill(WHITE)

        draw_text(screen, "RACER GAME", 40, 200, 100)
        draw_text(screen, "1 - Play", 25, 200, 200)
        draw_text(screen, "2 - Leaderboard", 25, 200, 250)
        draw_text(screen, "3 - Settings", 25, 200, 300)
        draw_text(screen, "ESC - Quit", 20, 200, 400)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "play"
                if event.key == pygame.K_2:
                    return "leaderboard"
                if event.key == pygame.K_3:
                    return "settings"
                if event.key == pygame.K_ESCAPE:
                    return "quit"

# ========= NAME INPUT =========
def input_name(screen):
    name = ""
    font = pygame.font.SysFont("Verdana", 30)

    while True:
        screen.fill(WHITE)
        draw_text(screen, "Enter name:", 30, 200, 150)
        draw_text(screen, name, 30, 200, 250)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10:
                        name += event.unicode

# ========= LEADERBOARD =========
def leaderboard_screen(screen):
    data = load_leaderboard()

    while True:
        screen.fill(WHITE)

        draw_text(screen, "TOP 10", 40, 200, 80)

        y = 150
        for i, row in enumerate(data):
            text = f"{i+1}. {row['name']} - {row['score']} ({row['distance']})"
            draw_text(screen, text, 20, 200, y)
            y += 30

        draw_text(screen, "ESC - Back", 20, 200, 550)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

# ========= SETTINGS =========
def settings_screen(screen, settings):
    while True:
        screen.fill(WHITE)

        draw_text(screen, "SETTINGS", 40, 200, 100)

        draw_text(screen, f"1 - Sound: {settings['sound']}", 25, 200, 200)
        draw_text(screen, f"2 - Difficulty: {settings['difficulty']}", 25, 200, 250)
        draw_text(screen, f"3 - Car Color: {settings['car_color']}", 25, 200, 300)

        draw_text(screen, "ESC - Back", 20, 200, 400)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    settings["sound"] = not settings["sound"]
                    save_settings(settings)

                if event.key == pygame.K_2:
                    if settings["difficulty"] == "normal":
                        settings["difficulty"] = "hard"
                    else:
                        settings["difficulty"] = "normal"
                    save_settings(settings)

                if event.key == pygame.K_3:
                    colors = ["default","red"]
                    idx = colors.index(settings["car_color"])
                    settings["car_color"] = colors[(idx+1) % len(colors)]
                    save_settings(settings)

                if event.key == pygame.K_ESCAPE:
                    return

# ========= GAME OVER =========
def game_over_screen(screen, score, distance):
    while True:
        screen.fill((255,0,0))
        draw_text(screen, "GAME OVER", 40, 200, 150)
        draw_text(screen, f"Score: {score}", 25, 200, 250)
        draw_text(screen, f"Distance: {distance}", 25, 200, 300)
        draw_text(screen, "R - Retry", 20, 200, 400)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return