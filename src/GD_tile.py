import pygame
from GD_constants import *

class Tile:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.color = BLUE
        
    def draw(self, screen, camera_x): 
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x - camera_x, self.y, TILE_SIZE, TILE_SIZE))
    
    def check_collision(self, ball):
                
        if ball.gravity > 0:
            if (ball.y + BALL_RADIUS > self.y and 
                ball.y - BALL_RADIUS < self.y and
                self.x < ball.x + BALL_RADIUS and
                ball.x - BALL_RADIUS < self.x + TILE_SIZE):

                ball.y = self.y - BALL_RADIUS
                ball.velocityY = 0
                ball.on_ground = True
                self.collided = True

            if (ball.y - BALL_RADIUS < self.y + TILE_SIZE and
                ball.y + BALL_RADIUS > self.y + TILE_SIZE and
                self.x < ball.x < self.x + TILE_SIZE and 
                ball.velocityY < 0):

                self.collided = True
                return True
        else:
            if (ball.y - BALL_RADIUS < self.y + TILE_SIZE and
                ball.y + BALL_RADIUS > self.y + TILE_SIZE and
                self.x < ball.x < self.x + TILE_SIZE):
                
                ball.y = self.y + TILE_SIZE + BALL_RADIUS
                ball.velocityY = 0
                ball.on_ground = True
                self.collided = True

            if (ball.y + BALL_RADIUS > self.y and
                ball.y - BALL_RADIUS < self.y and
                self.x < ball.x < self.x + TILE_SIZE and
                ball.velocityY > 0):
                self.collided = True
                return True
                
        if (ball.x + BALL_RADIUS > self.x and
            ball.x - BALL_RADIUS < self.x and 
            self.y < ball.y < self.y + TILE_SIZE):
              
            self.collided = True
            return True
        
        return False   
