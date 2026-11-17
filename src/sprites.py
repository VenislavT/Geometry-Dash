import os
import pygame
from .constants import *

ORIGINAL_TILE_SIZE = 18
SCALE = TILE_SIZE // ORIGINAL_TILE_SIZE

POSITIONS = ("single", "left", "middle", "right")

cache = {}

def load(path):
    if path not in cache:
        image = pygame.image.load(path).convert_alpha()
        width, height = image.get_size()
        cache[path] = pygame.transform.scale(image, (width * SCALE, height * SCALE))
    return cache[path]

def asset(name):
    return load(os.path.join(SHARED_DIR, name + ".png"))

def level_tile(tiles_directory, name):
    return load(os.path.join(tiles_directory, name + ".png"))

def hero_image(frame):
    return asset(f"hero_{frame + 1}")

def spike_image():
    return asset("spike")

def jump_orb_image():
    return asset("jump_orb")

def finish_flag_image():
    return asset("finish_flag")

def portal_image(color):
    key = ("portal", color)
    if key not in cache:
        size = ORIGINAL_TILE_SIZE * SCALE
        ring = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        ring.blit(asset("portal_top_left"), (0, 0))
        ring.blit(asset("portal_top_right"), (size, 0))
        ring.blit(asset("portal_bottom_left"), (0, size))
        ring.blit(asset("portal_bottom_right"), (size, size))
        image = pygame.transform.scale(ring, (TILE_SIZE, TILE_SIZE * 2))
        if color is not None:
            image = tinted(image, color)
        cache[key] = image
    return cache[key]

def tinted(image, color):
    result = pygame.transform.grayscale(image)
    tint = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    tint.fill(color + (255,))
    result.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    light = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    light.fill((60, 60, 60, 0))
    result.blit(light, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
    return result

def position(solid, row, column):
    left = solid(row, column - 1)
    right = solid(row, column + 1)

    if not left and not right:
        return "single"
    if not left:
        return "left"
    if not right:
        return "right"
    return "middle"

def cloud_name(cloud, row, column):
    return "cloud_" + position(cloud, row, column)

def platform_name(solid, row, column):
    up = solid(row - 1, column)
    down = solid(row + 1, column)
    side = position(solid, row, column)

    if not up:
        return "ground_" + side
    if down:
        return "dirt_" + side
    return "dirt_bottom_" + side
