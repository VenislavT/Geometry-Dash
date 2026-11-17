import pygame
import os
from .constants import *
from .ball import Ball
from .tile import Tile, Cloud
from .gravity_portal import GravityPortal
from .speed_portal import SpeedUpPortal, SlowDownPortal
from .jump_orb import JumpOrb
from .spike import Spike, InvertedSpike
from .finish_line import FinishLine
from .message import Message
from . import sprites

LEVEL_OBJECTS = {
    "F": FinishLine,
    "P": GravityPortal,
    "S": SpeedUpPortal,
    "D": SlowDownPortal,
    "J": JumpOrb,
    "^": Spike,
    "v": InvertedSpike,
}

def level_directory(level):
    return os.path.join(LEVELS_DIR, f"level{level}")

def find_levels():
    levels = []
    level = 1
    while os.path.isdir(level_directory(level)):
        levels.append(level)
        level += 1
    return levels

def load_level_assets(directory):
    assets = {}
    for file in sorted(os.listdir(directory)):
        extension = os.path.splitext(file)[1]
        assets[extension] = os.path.join(directory, file)
    return assets

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.ball = None
        self.platforms = []
        self.objects = []
        self.finish_line = None
        self.camera_x = 0
        self.attempts = 0
        self.messages = []
        self.level_complete = False
        self.current_level = 1
        self.level_height = 0
        self.level_top = 0
        self.tiles_directory = None
        self.world = None
        self.background = None
        self.music_file = None

    def load_level(self, level):
        self.current_level = level
        self.platforms.clear()
        self.objects.clear()
        self.messages.clear()
        self.level_complete = False

        assets = load_level_assets(level_directory(level))
        self.tiles_directory = os.path.join(level_directory(level), "tiles")
        level_file = assets[".txt"]
        music_file = assets[".mp3"]

        with open(level_file, 'r') as f:
            level_data = f.readlines()
        level_data = [line.rstrip("\n") for line in level_data]
        self.level_height = len(level_data) * TILE_SIZE
        self.level_top = (HEIGHT - self.level_height) // 2

        for y, line in enumerate(level_data):
            for x, char in enumerate(line):
                if char == "#":
                    self.platforms.append(Tile(x * TILE_SIZE, y * TILE_SIZE))
                elif char == "C":
                    self.platforms.append(Cloud(x * TILE_SIZE, y * TILE_SIZE))
                elif char == "B":
                    self.ball = Ball(x * TILE_SIZE, y * TILE_SIZE)
                elif char in LEVEL_OBJECTS:
                    level_object = LEVEL_OBJECTS[char](x * TILE_SIZE, y * TILE_SIZE)
                    self.objects.append(level_object)
                    if char == "F":
                        self.finish_line = level_object
                elif char == "M":
                    self.messages.append(Message(x * TILE_SIZE, y * TILE_SIZE, f"Attempt {self.attempts + 1}"))

        self.place_ball_on_nearest_platform()
        self.attempts += 1

        self.choose_platform_images(level_data)
        self.world = self.screen.subsurface((0, self.level_top, WIDTH, self.level_height))
        self.background = self.make_background()

        if music_file != self.music_file:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            self.music_file = music_file
        pygame.mixer.music.play()

    def choose_platform_images(self, level_data):
        def solid(row, column):
            if row < 0 or row >= len(level_data) or column < 0:
                return True
            return column < len(level_data[row]) and level_data[row][column] == "#"

        def cloud(row, column):
            return 0 <= column < len(level_data[row]) and level_data[row][column] == "C"

        for platform in self.platforms:
            row = platform.y // TILE_SIZE
            column = platform.x // TILE_SIZE
            if isinstance(platform, Cloud):
                name = sprites.cloud_name(cloud, row, column)
            else:
                name = sprites.platform_name(solid, row, column)
            platform.image = sprites.level_tile(self.tiles_directory, name)

    def visible(self, level_object):
        return (level_object.x + level_object.width + TILE_SIZE > self.camera_x and
                level_object.x - TILE_SIZE < self.camera_x + WIDTH)

    def make_background(self):
        sky = sprites.level_tile(self.tiles_directory, "background_sky")
        hills = sprites.level_tile(self.tiles_directory, "background_hills")
        ground = sprites.level_tile(self.tiles_directory, "background_ground")
        size = sky.get_width()

        background = pygame.Surface((WIDTH + size, HEIGHT))
        level_bottom = self.level_top + self.level_height
        for y in range(0, HEIGHT, size):
            if y + size <= level_bottom - 2 * size:
                image = sky
            elif y + size <= level_bottom - size:
                image = hills
            else:
                image = ground
            for x in range(0, WIDTH + size, size):
                background.blit(image, (x, y))
        return background

    def draw_ground(self):
        dirt = sprites.level_tile(self.tiles_directory, "dirt_middle")
        start = -(int(self.camera_x) % TILE_SIZE)
        for x in range(start, WIDTH, TILE_SIZE):
            for y in range(self.level_top - TILE_SIZE, -TILE_SIZE, -TILE_SIZE):
                self.screen.blit(dirt, (x, y))
            for y in range(self.level_top + self.level_height, HEIGHT, TILE_SIZE):
                self.screen.blit(dirt, (x, y))

    def place_ball_on_nearest_platform(self):
        for platform in self.platforms:
            if (self.ball.x + BALL_RADIUS > platform.x and
                self.ball.x - BALL_RADIUS < platform.x + TILE_SIZE and
                self.ball.y <= platform.y):
                self.ball.y = platform.y - BALL_RADIUS
                self.ball.velocity_y = 0
                self.ball.on_ground = True
                break

    def reset_level(self):
        self.ball = None
        self.finish_line = None
        self.load_level(self.current_level)

    def draw(self):
        size = self.background.get_width() - WIDTH
        self.screen.blit(self.background, (-(int(self.camera_x * 0.3) % size), 0))
        self.draw_ground()

        for platform in self.platforms:
            if self.visible(platform):
                platform.draw(self.world, self.camera_x)

        for level_object in self.objects:
            if self.visible(level_object):
                level_object.draw(self.world, self.camera_x)

        self.ball.draw(self.world, self.camera_x)

        for message in self.messages:
            message.draw(self.world, self.camera_x)

    def ball_out_of_level(self):
        return self.ball.y < -TILE_SIZE or self.ball.y > self.level_height + TILE_SIZE

    def update(self):
        if self.level_complete:
            pygame.mixer.music.stop()
            pygame.time.wait(2000)
            return "menu"

        result = self.ball.update(self.platforms, self.objects)
        if result == "finish":
            self.messages.clear()
            self.messages.append(Message(self.finish_line.x, self.finish_line.y - TILE_SIZE * 8, "Level Complete!"))
            self.level_complete = True

        elif result == "death" or self.ball_out_of_level():
            self.reset_level()

        self.camera_x = max(0, round(self.ball.x) - WIDTH // 3)
        return None

    def handle_events(self):
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_SPACE] and self.ball.on_ground: 
            self.ball.jump()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return "menu"

        return None