import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Folders with the images, music and levels
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
LEVELS_DIR = os.path.join(ASSETS_DIR, "levels")
MENU_DIR = os.path.join(ASSETS_DIR, "menu")
SHARED_DIR = os.path.join(ASSETS_DIR, "shared")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Screen size
WIDTH = 1200
HEIGHT = 700

# Size of one tile in pixels and frames per second
TILE_SIZE = 36
FPS = 60

# Player settings, in tiles and seconds
SPEED = 12.75           # tiles per second
JUMP_HEIGHT = 2.2       # tiles
JUMP_TIME = 0.375       # seconds in the air for one jump
MAX_FALL_SPEED = 0.75   # tiles per frame
SPIKE_HITBOX = 0.8      # part of the ball radius that counts when touching a spike

# Calculated from the settings above, in pixels per frame
BALL_RADIUS = TILE_SIZE // 2
BALL_SPEED_X = SPEED * TILE_SIZE / FPS
BALL_SPEED_Y = 0
FRAMES_TO_TOP = JUMP_TIME * FPS / 2
GRAVITY = 2 * JUMP_HEIGHT * TILE_SIZE / FRAMES_TO_TOP ** 2
JUMP = 2 * JUMP_HEIGHT * TILE_SIZE / FRAMES_TO_TOP
MAX_FALL = MAX_FALL_SPEED * TILE_SIZE

# Portal size
PORTAL_WIDTH = TILE_SIZE // 2
PORTAL_HEIGHT = TILE_SIZE * 2

# Music volume, from 0 to 1
MUSIC_VOLUME = 0.3
