import pygame
from .game import Game
from .constants import *

def game_loop(level):
    screen = pygame.display.get_surface()
    game = Game(screen)
    clock = pygame.time.Clock()
    game.load_level(level)

    while True:
        screen.fill(BLACK)

        action = game.handle_events()
        if action is None:
            action = game.update()
        if action is not None:
            return action

        game.draw()

        pygame.display.flip()
        clock.tick_busy_loop(FPS)


