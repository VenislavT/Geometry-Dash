from .level_object import LevelObject
from .constants import *
from . import sprites

class SpeedPortal(LevelObject):
    width = PORTAL_WIDTH
    height = PORTAL_HEIGHT
    speed_factor = 1
    sprite_color = None

    def __init__(self, x, y):
        super().__init__(x, y - TILE_SIZE)
        self.collided = False

    def draw(self, screen, camera_x):
        image = sprites.portal_image(self.sprite_color)
        screen.blit(image, (self.x - (TILE_SIZE - self.width) // 2 - camera_x, self.y))

    def check_collision(self, ball):
        if self.touches(ball) and not self.collided:
            ball.velocity_x *= self.speed_factor
            self.collided = True
        return None

class SpeedUpPortal(SpeedPortal):
    color = YELLOW
    speed_factor = 1.5
    sprite_color = (255, 200, 40)

class SlowDownPortal(SpeedPortal):
    color = PURPLE
    speed_factor = 0.5
    sprite_color = (190, 90, 255)
