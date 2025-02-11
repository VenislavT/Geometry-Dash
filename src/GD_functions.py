import pygame
import menu
import os
from GD_constants import *
from GD_ball import Ball
from GD_tile import Tile
from GD_gravity_portal import Gravity_portal
from GD_speed_portal import Speed_portal
from GD_jump_orb import JumpOrb
from GD_spike import Spike, InvertedSpike
from GD_finish_line import FinishLine
from GD_message import Message

def load_level_assets(directory):
    level_file = None
    music_file = None

    for file in os.listdir(directory):
        if file.endswith(".txt"): 
            level_file = os.path.join(directory, file)
        elif file.endswith(".mp3"):
            music_file = os.path.join(directory, file)

    return level_file, music_file

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.ball = None
        self.platforms = []
        self.portals = []
        self.speed_portals = []
        self.jumping_orbs = []
        self.spikes = []
        self.inverted_spikes = []
        self.finish_line = None
        self.camera_x = 0
        self.attempts = 0
        self.messages = []
        self.level_complete = False
        self.current_level = 1

    def load_level(self, level):
        self.current_level = level
        self.platforms.clear()
        self.portals.clear()
        self.speed_portals.clear()
        self.jumping_orbs.clear()
        self.spikes.clear()
        self.messages.clear()
        self.inverted_spikes.clear()
        self.level_complete = False

        level_directory = f"level{level}"
        level_file, music_file = load_level_assets(level_directory)

        with open(level_file, 'r') as f:
            level_data = f.readlines()

        for y, line in enumerate(level_data):
            for x, char in enumerate(line):
                if char == "#":
                    self.platforms.append(Tile(x * TILE_SIZE, y * TILE_SIZE))
                elif char == "B":
                    self.ball = Ball(x * TILE_SIZE, y * TILE_SIZE)
                elif char == "F":
                    self.finish_line = FinishLine(x * TILE_SIZE, y * TILE_SIZE)
                elif char == "P":
                    self.portals.append(Gravity_portal(x * TILE_SIZE, y * TILE_SIZE))
                elif char == "S":
                    self.speed_portals.append(Speed_portal(x * TILE_SIZE, y * TILE_SIZE, "speed_up"))
                elif char == "D":
                    self.speed_portals.append(Speed_portal(x * TILE_SIZE, y * TILE_SIZE, "slow_down"))
                elif char == "J":
                    self.jumping_orbs.append(JumpOrb(x * TILE_SIZE, y * TILE_SIZE))
                elif char == "^":
                    self.spikes.append(Spike(x * TILE_SIZE, y * TILE_SIZE))
                elif char == "v":
                    self.inverted_spikes.append(InvertedSpike(x * TILE_SIZE, y * TILE_SIZE))
                elif char == "M":
                    self.messages.append(Message(x * TILE_SIZE, y * TILE_SIZE, f"Attempt {self.attempts + 1}"))

        self.place_ball_on_nearest_platform()
        self.attempts += 1

        # Пускане на музиката при зареждане на нивото
        pygame.mixer.music.load(music_file)

        if self.current_level == 1:
            pygame.mixer.music.set_volume(0.5) 
        if self.current_level == 2:
            pygame.mixer.music.set_volume(0.1)

        pygame.mixer.music.play()

    def place_ball_on_nearest_platform(self):
        for platform in self.platforms:
            if (self.ball.x + BALL_RADIUS > platform.x and
                self.ball.x - BALL_RADIUS < platform.x + TILE_SIZE and
                self.ball.y <= platform.y):
                self.ball.y = platform.y - BALL_RADIUS
                self.ball.velocityY = 0
                self.ball.on_ground = True
                break

    def reset_level(self):
        self.ball = None
        self.finish_line = None
        self.load_level(self.current_level)

        pygame.mixer.music.stop()
        pygame.mixer.music.play()

    def draw(self):
        self.ball.draw(self.screen, self.camera_x)
        self.finish_line.draw(self.screen, self.camera_x)
        self.draw_platforms()
        self.draw_portals()
        self.draw_speed_portals()
        self.draw_jumping_orbs()
        self.draw_spikes()
        self.draw_inverted_spikes()
        self.draw_messages()

    def draw_platforms(self):
        for platform in self.platforms:
            platform.draw(self.screen, self.camera_x)

    def draw_portals(self):
        for portal in self.portals:
            portal.draw(self.screen, self.camera_x)

    def draw_speed_portals(self):
        for speed_portal in self.speed_portals:
            speed_portal.draw(self.screen, self.camera_x)

    def draw_jumping_orbs(self):
        for orb in self.jumping_orbs:
            orb.draw(self.screen, self.camera_x)

    def draw_spikes(self):
        for spike in self.spikes:
            spike.draw(self.screen, self.camera_x)
    
    def draw_inverted_spikes(self):
        for inverted_spike in self.inverted_spikes:
            inverted_spike.draw(self.screen, self.camera_x)

    def draw_messages(self):
        for message in self.messages:
            message.draw(self.screen, self.camera_x)

    def update(self):
        if self.level_complete:
            pygame.mixer.music.stop()
            pygame.time.wait(2000)

            menu.level_menu()
            return

        result = self.ball.update(self.platforms, self.portals, self.speed_portals, self.jumping_orbs, self.spikes, self.inverted_spikes, self.finish_line)
        if result == "finish":
            self.messages.clear()
            self.messages.append(Message(self.finish_line.x, self.finish_line.y - TILE_SIZE * 8, "Level Complete!"))
            self.level_complete = True

        elif result:
            self.reset_level()

        self.camera_x = max(0, self.ball.x - WIDTH // 3)

    def handle_events(self):
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_SPACE] and self.ball.on_ground: 
            self.ball.jump()  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    menu.level_menu()
                    return False
        
        return True