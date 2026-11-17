import pygame
from .constants import *

class LevelObject:
    width = TILE_SIZE
    height = TILE_SIZE
    color = WHITE

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen, camera_x):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x - camera_x, self.y, self.width, self.height))

    def touches(self, ball):
        return (ball.x + BALL_RADIUS > self.x and
                ball.x - BALL_RADIUS < self.x + self.width and
                ball.y + BALL_RADIUS > self.y and
                ball.y - BALL_RADIUS < self.y + self.height)

    def check_collision(self, ball):
        return None
