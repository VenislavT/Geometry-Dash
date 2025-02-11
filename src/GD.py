import pygame
from GD_functions import Game
from GD_constants import *

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Geometry Dash')

#pygame.mixer.music.load('Panda Eyes - Colorblind.mp3')
#pygame.mixer.music.set_volume(0.5) 

def game_loop(level):
    game = Game(screen)
    running = True
    clock = pygame.time.Clock()
    game.load_level(level)
    while running:
        screen.fill(BLACK)
        running = game.handle_events()

        game.update()

        game.draw()

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


