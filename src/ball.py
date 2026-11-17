import pygame
from .constants import *
from . import sprites

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity_x = BALL_SPEED_X
        self.velocity_y = BALL_SPEED_Y
        self.on_ground = False
        self.gravity = GRAVITY
        self.frames = 0

    def draw(self, screen, camera_x):
        frame = 0
        if self.on_ground and (self.frames // 8) % 2 == 1:
            frame = 1
        image = pygame.transform.flip(sprites.hero_image(frame), True, self.gravity < 0)

        x = round(self.x) - image.get_width() // 2 - camera_x
        if self.gravity > 0:
            y = round(self.y) + BALL_RADIUS - image.get_height()
        else:
            y = round(self.y) - BALL_RADIUS
        screen.blit(image, (x, y))
    
    def jump(self):
        if self.on_ground:
            self.velocity_y = -JUMP if self.gravity > 0 else JUMP
            self.on_ground = False
            
    def update(self, platforms, objects):
        self.frames += 1
        self.x += self.velocity_x

        self.on_ground = False
        self.velocity_y += self.gravity
        self.velocity_y = max(-MAX_FALL, min(MAX_FALL, self.velocity_y))
        self.y += self.velocity_y

        for platform in platforms:
            if platform.check_collision(self) == "death":
                return "death"

        for level_object in objects:
            result = level_object.check_collision(self)
            if result is not None:
                return result

        return None
