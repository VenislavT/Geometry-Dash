import pygame
from GD_constants import *

class Spike:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collided = False

    def draw(self, screen ,camera_x):
        points = [(self.x - camera_x, self.y + TILE_SIZE), 
                  (self.x + TILE_SIZE // 2 - camera_x, self.y), 
                  (self.x + TILE_SIZE - camera_x, self.y + TILE_SIZE)]
        pygame.draw.polygon(screen, RED, points)

    def check_collision(self, ball):

        ax, ay = self.x, self.y + TILE_SIZE  # Ляв долен ъгъл
        bx, by = self.x + TILE_SIZE // 2, self.y  # Връх на триъгълника
        cx, cy = self.x + TILE_SIZE, self.y + TILE_SIZE  # Десен долен ъгъл
  
        if (point_in_triangle(ball.x + BALL_RADIUS, ball.y, ax, ay, bx, by, cx, cy) or
            point_in_triangle(ball.x - BALL_RADIUS, ball.y, ax, ay, bx, by, cx, cy) or
            point_in_triangle(ball.x, ball.y + BALL_RADIUS, ax, ay, bx, by, cx, cy) or
            point_in_triangle(ball.x, ball.y - BALL_RADIUS, ax, ay, bx, by, cx, cy)):
            return True
        return False
    
class InvertedSpike:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collided = False

    def draw(self, screen, camera_x):
        points = [(self.x - camera_x, self.y), 
                  (self.x + TILE_SIZE // 2 - camera_x, self.y + TILE_SIZE), 
                  (self.x + TILE_SIZE - camera_x, self.y)]
        pygame.draw.polygon(screen, RED, points)

    def check_collision(self, ball):
        ax, ay = self.x, self.y 
        bx, by = self.x + TILE_SIZE // 2, self.y + TILE_SIZE  
        cx, cy = self.x + TILE_SIZE, self.y

        if (point_in_triangle(ball.x + BALL_RADIUS, ball.y, ax, ay, bx, by, cx, cy) or
            point_in_triangle(ball.x - BALL_RADIUS, ball.y, ax, ay, bx, by, cx, cy) or
            point_in_triangle(ball.x, ball.y + BALL_RADIUS, ax, ay, bx, by, cx, cy) or
            point_in_triangle(ball.x, ball.y - BALL_RADIUS, ax, ay, bx, by, cx, cy)):
            return True
        return False

def point_in_triangle(px, py, ax, ay, bx, by, cx, cy):
    """ Проверява дали точка (px, py) е вътре в триъгълника (ax, ay), (bx, by), (cx, cy) """
    def sign(x1, y1, x2, y2, x3, y3):
        return (x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)

    d1 = sign(px, py, ax, ay, bx, by)
    d2 = sign(px, py, bx, by, cx, cy)
    d3 = sign(px, py, cx, cy, ax, ay)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)  # Ако всички знаци са еднакви -> точката е в триъгълника
