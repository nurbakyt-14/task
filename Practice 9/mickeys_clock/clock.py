import pygame
import datetime

class MickeyClock:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.center = (width // 2, height // 2)
        
        # Load images
        self.clock_face = pygame.image.load("images/clock.png").convert_alpha()
        self.mickey_body = pygame.image.load("images/mickey.png").convert_alpha()
        self.right_hand = pygame.image.load("images/right_hand_fixed.png").convert_alpha()
        self.left_hand = pygame.image.load("images/left_hand_fixed.png").convert_alpha()
        
        # Scale all to fit screen
        self.clock_face = pygame.transform.scale(self.clock_face, (width, height))
        mickey_width = width // 2
        mickey_height = height // 2
        self.mickey_body = pygame.transform.scale(self.mickey_body, (mickey_width, mickey_height))
        
        # Scale hands
        self.right_hand = pygame.transform.scale(self.right_hand, (200, 300))
        self.left_hand = pygame.transform.scale(self.left_hand, (200, 300))
        
        self.mickey_rect = self.mickey_body.get_rect(center=self.center)
        self.hand_offset_y = 0
    
    def render(self, screen):
        now = datetime.datetime.now()
        
        minute_angle = now.minute * 6
        second_angle = now.second * 6
        
        right_rotated = pygame.transform.rotate(self.right_hand, -minute_angle)
        left_rotated = pygame.transform.rotate(self.left_hand, -second_angle)
        
        right_rect = right_rotated.get_rect(center=(self.center[0], self.center[1] + self.hand_offset_y))
        left_rect = left_rotated.get_rect(center=(self.center[0], self.center[1] + self.hand_offset_y))
        
        screen.blit(self.clock_face, (0, 0))
        screen.blit(self.mickey_body, self.mickey_rect)
        screen.blit(right_rotated, right_rect)
        screen.blit(left_rotated, left_rect)