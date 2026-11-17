import pygame
from .constants import *

class Message:
    font = None

    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text

    def draw(self, screen, camera_x):
        if Message.font is None:
            Message.font = pygame.font.Font(None, 74)
        text_surface = Message.font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.x - camera_x, self.y))
