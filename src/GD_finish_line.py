import pygame
from GD_constants import *
class FinishLine:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen, camera_x):
        pygame.draw.rect(screen, GREEN, pygame.Rect(self.x - camera_x, self.y, TILE_SIZE,TILE_SIZE))
    
    def check_collision(self, ball):
        if (ball.x + BALL_RADIUS > self.x and
            ball.x - BALL_RADIUS < self.x + TILE_SIZE and
            ball.y + BALL_RADIUS > self.y and
            ball.y - BALL_RADIUS < self.y + TILE_SIZE):
            return True
        return False
  