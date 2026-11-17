import pygame
from .level_object import LevelObject
from .constants import *
from . import sprites

class JumpOrb(LevelObject):
    width = BALL_RADIUS * 2
    height = BALL_RADIUS * 2
    color = RED

    def __init__(self, x, y):
        super().__init__(x - BALL_RADIUS, y - BALL_RADIUS)
        self.used = False

    def draw(self, screen, camera_x):
        image = sprites.jump_orb_image()
        x = self.x + BALL_RADIUS - image.get_width() // 2 - camera_x
        y = self.y + BALL_RADIUS - image.get_height() // 2
        screen.blit(image, (x, y))

    def check_collision(self, ball):
        if self.touches(ball) and not self.used and pygame.key.get_pressed()[pygame.K_SPACE]:
            ball.velocity_y = -JUMP if ball.gravity > 0 else JUMP
            ball.on_ground = False
            self.used = True
        return None