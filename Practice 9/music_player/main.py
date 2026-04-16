import pygame
import sys
from player import MusicPlayer

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Music Player")
    font = pygame.font.Font(None, 36)

    player = MusicPlayer("music")

    running = True
    while running:
        screen.fill((0, 0, 0))

        if player.tracks:
            text = font.render(f"Now: {player.tracks[player.current_track]}", True, (255, 255, 255))
            screen.blit(text, (50, 150))

        controls = font.render("P=Play S=Stop N=Next B=Prev Q=Quit", True, (200, 200, 200))
        screen.blit(controls, (50, 300))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.previous_track()
                elif event.key == pygame.K_q:
                    running = False

    player.quit()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()