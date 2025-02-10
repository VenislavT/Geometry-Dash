import pygame
from GD_constants import *
class JumpOrb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collided = False

    def draw(self, screen, camera_x): 
        pygame.draw.circle(screen, RED, (self.x - camera_x, self.y), BALL_RADIUS)

    def check_collision(self, ball):
        if (ball.x + BALL_RADIUS > self.x - BALL_RADIUS and
            ball.x - BALL_RADIUS < self.x + BALL_RADIUS and
            ball.y + BALL_RADIUS > self.y - BALL_RADIUS and
            ball.y - BALL_RADIUS < self.y + BALL_RADIUS):
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                ball.velocityY = -JUMP if ball.gravity > 0 else JUMP
                self.collided = True
    