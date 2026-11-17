from .level_object import LevelObject
from .constants import *

class Tile(LevelObject):
    color = BLUE

    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = None

    def draw(self, screen, camera_x):
        if self.image is None:
            super().draw(screen, camera_x)
        else:
            screen.blit(self.image, (self.x - camera_x, self.y))

    def check_collision(self, ball):
        if ball.gravity > 0:
            if (ball.y + BALL_RADIUS > self.y and 
                ball.y - BALL_RADIUS < self.y and
                self.x < ball.x + BALL_RADIUS and
                ball.x - BALL_RADIUS < self.x + TILE_SIZE):

                ball.y = self.y - BALL_RADIUS
                ball.velocity_y = 0
                ball.on_ground = True

                return None

            if (ball.y - BALL_RADIUS < self.y + TILE_SIZE and
                ball.y + BALL_RADIUS > self.y + TILE_SIZE and
                self.x < ball.x < self.x + TILE_SIZE and 
                ball.velocity_y < 0):

                return "death"
        else:
            if (ball.y - BALL_RADIUS < self.y + TILE_SIZE and
                ball.y + BALL_RADIUS > self.y + TILE_SIZE and
                self.x < ball.x + BALL_RADIUS and
                ball.x - BALL_RADIUS < self.x + TILE_SIZE):
                
                ball.y = self.y + TILE_SIZE + BALL_RADIUS
                ball.velocity_y = 0
                ball.on_ground = True

                return None

            if (ball.y + BALL_RADIUS > self.y and
                ball.y - BALL_RADIUS < self.y and
                self.x < ball.x < self.x + TILE_SIZE and
                ball.velocity_y > 0):

                return "death"
                
        if (ball.x + BALL_RADIUS > self.x and
            ball.x - BALL_RADIUS < self.x and 
            self.y < ball.y < self.y + TILE_SIZE):
              
            return "death"
        
        return None   


class Cloud(Tile):
    color = WHITE
