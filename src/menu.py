import pygame
import os
from .constants import *
from . import game_loop
from .game import find_levels, level_directory, load_level_assets
pygame.init()

SCREEN_WIDTH = WIDTH
SCREEN_HEIGHT = HEIGHT

BIG_BUTTON_WIDTH = SCREEN_WIDTH // 2
BIG_BUTTON_HEIGHT = SCREEN_HEIGHT // 2
ARROW_DISTANCE = 40

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Geometry Dash")

class Button:
    def __init__(self, image, x, y, action = None):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hovered_image = pygame.transform.scale(self.image, 
                                                    (int(self.rect.width * 1.1), 
                                                     int(self.rect.height * 1.1)))
        self.action = action

    def is_hovered(self, position):
        mouse_x, mouse_y = position
        return (mouse_x in range(self.x, self.x + self.rect.width) and 
                mouse_y in range(self.y, self.y + self.rect.height))
    
    def draw(self, position):
        if self.is_hovered(position):
            new_x = self.x - (self.hovered_image.get_width() - self.rect.width) // 2
            new_y = self.y - (self.hovered_image.get_height() - self.rect.height) // 2
            screen.blit(self.hovered_image, (new_x, new_y))

        else:
            screen.blit(self.image, (self.x, self.y))

    def check_click(self, position):
        if self.is_hovered(position) and self.action:
            return self.action()
        return None


def start_menu():
    def start_game():
        return level_menu()

    def exit_game():
        return "quit"

    background = pygame.image.load(os.path.join(MENU_DIR, "background.png")).convert()
    play_image = pygame.image.load(os.path.join(MENU_DIR, "play.png")).convert_alpha()
    exit_image = pygame.image.load(os.path.join(MENU_DIR, "exit.png")).convert_alpha()

    play_button = Button(play_image, (SCREEN_WIDTH - play_image.get_width()) // 2, 300, start_game)
    exit_button = Button(exit_image, (SCREEN_WIDTH - exit_image.get_width()) // 2, 420, exit_game)

    running = True
    while running:
        screen.blit(background, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_click(event.pos) == "quit":
                    running = False
                if exit_button.check_click(event.pos) == "quit":
                    running = False
                    
        play_button.draw(pygame.mouse.get_pos())
        exit_button.draw(pygame.mouse.get_pos())
        pygame.display.flip()
        
    pygame.quit()

def load_level_images(levels):
    level_images = []
    for level in levels:
        assets = load_level_assets(level_directory(level))
        image = pygame.image.load(assets[".png"])
        scaled_image = pygame.transform.scale(image, (BIG_BUTTON_WIDTH, BIG_BUTTON_HEIGHT))
        level_images.append(scaled_image)
    return level_images

current_level = 0
def level_menu():

    levels = find_levels()
    level_images = load_level_images(levels)

    def next_level():
        global current_level
        current_level = (current_level + 1) % len(level_images)

    def previous_level():
        global current_level
        current_level = (current_level - 1) % len(level_images)

    def start_level():
        return game_loop.game_loop(levels[current_level])


    background = pygame.image.load(os.path.join(MENU_DIR, "levels_background.png")).convert()
    arrow_right_image = pygame.image.load(os.path.join(MENU_DIR, "arrow_right.png")).convert_alpha()
    arrow_left_image = pygame.image.load(os.path.join(MENU_DIR, "arrow_left.png")).convert_alpha()

    arrow_y = (SCREEN_HEIGHT - arrow_right_image.get_height()) // 2
    arrow_right_x = (SCREEN_WIDTH + BIG_BUTTON_WIDTH) // 2 + ARROW_DISTANCE
    arrow_left_x = (SCREEN_WIDTH - BIG_BUTTON_WIDTH) // 2 - ARROW_DISTANCE - arrow_left_image.get_width()

    arrow_right = Button(arrow_right_image, arrow_right_x, arrow_y, next_level)
    arrow_left = Button(arrow_left_image, arrow_left_x, arrow_y, previous_level)

    running = True
    while running:
        screen.blit(background, (0, 0))
        
        current_level_image = level_images[current_level]
        current_level_x = (screen.get_width() - current_level_image.get_width()) // 2
        current_level_y = (screen.get_height() - current_level_image.get_height()) // 2
        current_level_button = Button(level_images[current_level], current_level_x, current_level_y, start_level)
        current_level_button.draw(pygame.mouse.get_pos())

        arrow_right.draw(pygame.mouse.get_pos())
        arrow_left.draw(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "back"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                arrow_left.check_click(event.pos)
                arrow_right.check_click(event.pos)
                if current_level_button.check_click(event.pos) == "quit":
                    return "quit"

        pygame.display.flip()


