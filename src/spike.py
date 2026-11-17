import math
import pygame
from .level_object import LevelObject
from .constants import *
from . import sprites

class Spike(LevelObject):
    color = RED
    flipped = False

    def corners(self):
        return [(self.x, self.y + TILE_SIZE), 
                (self.x + TILE_SIZE // 2, self.y), 
                (self.x + TILE_SIZE, self.y + TILE_SIZE)]

    def draw(self, screen, camera_x):
        image = sprites.spike_image()
        if self.flipped:
            image = pygame.transform.flip(image, False, True)
        screen.blit(image, (self.x - camera_x, self.y))

    def check_collision(self, ball):
        if circle_touches_triangle(ball.x, ball.y, BALL_RADIUS * SPIKE_HITBOX, self.corners()):
            return "death"
        return None

class InvertedSpike(Spike):
    flipped = True

    def corners(self):
        return [(self.x, self.y),
                (self.x + TILE_SIZE // 2, self.y + TILE_SIZE),
                (self.x + TILE_SIZE, self.y)]

def point_in_triangle(px, py, ax, ay, bx, by, cx, cy):
    def sign(x1, y1, x2, y2, x3, y3):
        return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)

    d1 = sign(px, py, ax, ay, bx, by)
    d2 = sign(px, py, bx, by, cx, cy)
    d3 = sign(px, py, cx, cy, ax, ay)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)

def distance_to_segment(px, py, ax, ay, bx, by):
    dx = bx - ax
    dy = by - ay
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))
    closest_x = ax + t * dx
    closest_y = ay + t * dy
    return math.hypot(px - closest_x, py - closest_y)

def circle_touches_triangle(x, y, radius, corners):
    (ax, ay), (bx, by), (cx, cy) = corners
    if point_in_triangle(x, y, ax, ay, bx, by, cx, cy):
        return True
    return (distance_to_segment(x, y, ax, ay, bx, by) < radius or
            distance_to_segment(x, y, bx, by, cx, cy) < radius or
            distance_to_segment(x, y, cx, cy, ax, ay) < radius)
