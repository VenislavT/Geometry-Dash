import pygame
from GD_constants import *

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocityX = BALL_SPEED_X
        self.velocityY = BALL_SPEED_Y
        self.on_ground = False
        self.gravity = GRAVITY

    def draw(self, screen, camera_x):
        pygame.draw.circle(screen, RED, (int(self.x - camera_x), int(self.y)), BALL_RADIUS)
    
    def jump(self):
        if self.on_ground:
            self.velocityY = -JUMP if self.gravity > 0 else JUMP
            self.on_ground = False
            
    def update(self, platforms, gravity_portals, speed_portals, jumping_orbs, spikes, inverted_spikes, finish_line):
        self.x += self.velocityX

        self.on_ground = False

        if not self.on_ground:
            self.velocityY += self.gravity
            self.y += self.velocityY

        for platform in platforms:
            if platform.check_collision(self):
                self.on_ground = True
                return True

        for gravity_portal in gravity_portals:
            gravity_portal.check_collision(self)

        for speed_portal in speed_portals:
            speed_portal.check_collision(self)

        for orb in jumping_orbs:
            orb.check_collision(self)

        for spike in spikes:
            if spike.check_collision(self):
                return True

        for inverted_spike in inverted_spikes:
            if inverted_spike.check_collision(self):
                return True

        if finish_line.check_collision(self):
            return "finish"

        return False

    