import pygame
import sys
from player import MusicPlayer

def format_time(seconds):
    """Convert seconds to MM:SS format"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 550))
    pygame.display.set_caption("Music Player")
    
    # Fonts
    font_title = pygame.font.Font(None, 48)
    font_artist = pygame.font.Font(None, 36)
    font_time = pygame.font.Font(None, 48)
    font_status = pygame.font.Font(None, 32)
    font_controls = pygame.font.Font(None, 28)
    
    player = MusicPlayer("music")
    clock = pygame.time.Clock()
    
    running = True
    while running:
        screen.fill((30, 30, 40))  
        
        player.update()
        
        if player.tracks:
            title, artist = player.get_current_track_info()
            
            # Display song title
            title_text = font_title.render(title, True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(300, 80))
            screen.blit(title_text, title_rect)
            
            # Display artist name
            artist_text = font_artist.render(f" {artist}", True, (255, 255, 255))
            artist_rect = artist_text.get_rect(center=(300, 140))
            screen.blit(artist_text, artist_rect)
            
            
            current_time = format_time(player.current_position)
            time_text = font_time.render(current_time, True, (255, 255, 255))
            time_rect = time_text.get_rect(center=(300, 270))
            screen.blit(time_text, time_rect)
            
            
            bar_width = 400
            bar_height = 8
            bar_x = 100
            bar_y = 310
            progress = min(player.current_position / 300.0, 1.0)  # 5 minutes max
            
            
            pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (128, 0, 128), (bar_x, bar_y, int(bar_width * progress), bar_height))
        
    
        if player.playing:
            status_text = font_status.render(" PLAYING", True, (255, 255, 255))
        else:
            status_text = font_status.render(" STOPPED", True, (255, 255, 255))
        status_rect = status_text.get_rect(center=(300, 360))
        screen.blit(status_text, status_rect)
        
        
        # Controls info
        controls = font_controls.render("P=Play  S=Stop  N=Next  B=Prev  Q=Quit", True, (200, 200, 200))
        controls_rect = controls.get_rect(center=(300, 490))
        screen.blit(controls, controls_rect)
        
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
        
        clock.tick(60) 

    player.quit()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()