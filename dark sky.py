import pygame
import time
from settings import Settings

ai_settings = Settings()
screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))

screen.fill(ai_settings.bg_color)

pygame.init()
image = pygame.image.load('images/ship.bmp')
rect = image.get_rect()
screen_rect = screen.get_rect()
rect.centerx= screen_rect.centerx
rect.bottom = screen_rect.centery
screen.blit(image, rect)

#make the most recently drawnscreen visible
pygame.display.flip()
time.sleep(2)