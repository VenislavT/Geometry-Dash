import pygame
from GD_constants import *

class Speed_portal:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y - TILE_SIZE
        self.type = type
        self.color = YELLOW if type == "speed_up" else PURPLE
        self.collided = False

    def draw(self, screen, camera_x):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x - camera_x, self.y, PORTAL_WIDTH, PORTAL_HEIGHT))
    
    def check_collision(self, ball):
        if (ball.x + BALL_RADIUS >= self.x and
            ball.x - BALL_RADIUS <= self.x + PORTAL_WIDTH and
            ball.y + BALL_RADIUS >= self.y and
            ball.y - BALL_RADIUS <= self.y + PORTAL_HEIGHT and
            not self.collided):

            if self.type == "speed_up":
                ball.velocityX *= 1.5

            elif self.type == "slow_down":
                ball.velocityX *= 0.5  

            self.collided = True
    