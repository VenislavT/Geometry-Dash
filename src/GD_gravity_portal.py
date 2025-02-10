import pygame
from GD_constants import *

class Gravity_portal:
    def __init__(self, x, y):
        self.x = x
        self.y = y - TILE_SIZE
        self.collided = False
    
    def draw(self, screen, camera_x):
        pygame.draw.rect(screen, WHITE, pygame.Rect(self.x - camera_x, self.y, PORTAL_WIDTH, PORTAL_HEIGHT))
   
    def check_collision(self, ball):
        if (ball.x + BALL_RADIUS >= self.x and
            ball.x - BALL_RADIUS <= self.x + PORTAL_WIDTH and
            ball.y + BALL_RADIUS >= self.y and
            ball.y - BALL_RADIUS <= self.y + PORTAL_HEIGHT and
            not self.collided):
            ball.on_ground = False
            ball.gravity = -ball.gravity
            ball.velocityY = 0
            self.collided = True