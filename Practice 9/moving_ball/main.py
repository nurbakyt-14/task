import pygame
import sys
from ball import Ball

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Moving Ball")
    clock = pygame.time.Clock()

    ball = Ball(400, 300, 25, (255, 0, 0))

    running = True
    while running:
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    ball.move(0, -20, 800, 600)
                elif event.key == pygame.K_DOWN:
                    ball.move(0, 20, 800, 600)
                elif event.key == pygame.K_LEFT:
                    ball.move(-20, 0, 800, 600)
                elif event.key == pygame.K_RIGHT:
                    ball.move(20, 0, 800, 600)

        ball.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()