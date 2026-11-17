from .level_object import LevelObject
from .constants import *
from . import sprites

class FinishLine(LevelObject):
    color = GREEN
   
    def draw(self, screen, camera_x):
        screen.blit(sprites.finish_flag_image(), (self.x - camera_x, self.y))

    def check_collision(self, ball):
        if self.touches(ball):
            return "finish"
        return None
  
