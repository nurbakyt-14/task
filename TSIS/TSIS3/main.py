import pygame
from ui import main_menu, input_name, leaderboard_screen, settings_screen, game_over_screen
from racer import run_game
from persistence import load_settings, save_score

pygame.init()
screen = pygame.display.set_mode((400,600))

settings = load_settings()

while True:
    action = main_menu(screen)

    if action == "play":
        name = input_name(screen)
        score, distance = run_game(screen, settings)
        save_score(name, score, distance)
        game_over_screen(screen, score, distance)

    elif action == "leaderboard":
        leaderboard_screen(screen)

    elif action == "settings":
        settings_screen(screen, settings)

    elif action == "quit":
        break