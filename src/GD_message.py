import pygame
from GD_constants import *

class Message:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw(self, screen, camera_x):
        font = pygame.font.Font(None, 74)
        text_surface = font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.x - camera_x, self.y))
