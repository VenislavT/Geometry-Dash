import pygame
import sys
import os
from GD_constants import *
import GD
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700

BUTTON_WIDTH = SCREEN_WIDTH // 3
BUTTON_HEIGHT = SCREEN_HEIGHT // 3

BIG_BUTTON_WIDTH = SCREEN_WIDTH // 2
BIG_BUTTON_HEIGHT = SCREEN_HEIGHT // 2

ARROW_WIDTH = SCREEN_WIDTH // 12
ARROW_HEIGHT = SCREEN_HEIGHT // 12

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("GOLF CHALLENGES")

class Button:
    def __init__(self, image, x, y, action = None):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.original_image = self.image
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
            self.action()


def start_menu():
    def start_game():
        level_menu()

    def exit_game():
        pygame.quit()
        sys.exit()

    play_image = pygame.image.load("menu_assets/play.png")
    exit_image = pygame.image.load("menu_assets/exit.png")

    play_image = pygame.transform.scale(play_image, (BUTTON_WIDTH - 15, BUTTON_HEIGHT))
    exit_image = pygame.transform.scale(exit_image, (BUTTON_WIDTH, BUTTON_HEIGHT))

    play_button = Button(play_image, (SCREEN_WIDTH - BUTTON_WIDTH) // 2, SCREEN_HEIGHT // 6, start_game)
    exit_button = Button(exit_image, (SCREEN_WIDTH - BUTTON_WIDTH - 12) // 2, SCREEN_HEIGHT // 2, exit_game)

    running = True
    while running:
        screen.fill((255, 255, 255))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                play_button.check_click(event.pos)
                exit_button.check_click(event.pos)
        
        play_button.draw(pygame.mouse.get_pos())
        exit_button.draw(pygame.mouse.get_pos())
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

def load_level_images(directory):
    level_images = []
    for filename in os.listdir(directory):
        if filename.endswith(".png"):
            image = pygame.image.load(os.path.join(directory, filename))
            scaled_image = pygame.transform.scale(image, (BIG_BUTTON_WIDTH, BIG_BUTTON_HEIGHT))  
            level_images.append(scaled_image)
    return level_images

def level_menu():

    level_images = load_level_images("menu_assets/levels")
    current_level = 0

    def next_level():
        nonlocal current_level
        current_level = (current_level + 1) % len(level_images)

    def previous_level():
        nonlocal current_level
        current_level = (current_level - 1) % len(level_images)

    def start_level():
        GD.game_loop(current_level + 1)

    arrow_right_image = pygame.image.load("menu_assets/arrow_right.png")
    arrow_left_image = pygame.image.load("menu_assets/arrow_left.png")

    arrow_right_image = pygame.transform.scale(arrow_right_image, (ARROW_WIDTH, ARROW_HEIGHT))
    arrow_left_image = pygame.transform.scale(arrow_left_image, (ARROW_WIDTH, ARROW_HEIGHT))

    arrow_right = Button(arrow_right_image, SCREEN_WIDTH - 150, SCREEN_HEIGHT // 2 - 50, next_level)
    arrow_left = Button(arrow_left_image, 50, SCREEN_HEIGHT // 2 - 50, previous_level)

    running = True
    while running:
        screen.fill((255, 255, 255))
        
        current_level_image = level_images[current_level]
        current_level_x = (screen.get_width() - current_level_image.get_width()) // 2
        current_level_y = (screen.get_height() - current_level_image.get_height()) // 2
        current_level_button = Button(level_images[current_level], current_level_x, current_level_y, start_level)
        current_level_button.draw(pygame.mouse.get_pos())

        arrow_right.draw(pygame.mouse.get_pos())
        arrow_left.draw(pygame.mouse.get_pos())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                arrow_left.check_click(event.pos)
                arrow_right.check_click(event.pos)
                current_level_button.check_click(event.pos)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

#if __name__ == "__main__":
#    start_menu()