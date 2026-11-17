from .level_object import LevelObject
from .constants import *
from . import sprites

class GravityPortal(LevelObject):
    width = PORTAL_WIDTH
    height = PORTAL_HEIGHT
    color = WHITE

    def __init__(self, x, y):
        super().__init__(x, y - TILE_SIZE)
        self.collided = False

    def draw(self, screen, camera_x):
        image = sprites.portal_image(None)
        screen.blit(image, (self.x - (TILE_SIZE - self.width) // 2 - camera_x, self.y))

    def check_collision(self, ball):
        if self.touches(ball) and not self.collided:
            ball.on_ground = False
            ball.gravity = -ball.gravity
            ball.velocity_y = 0
            self.collided = True
        return None
