#!/usr/bin/python3

import sys

import pygame

from GameFrame import Globals

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
pygame.font.init()

# - Set the Window Title for the game - #
pygame.display.set_caption("GF Game")
window_size = (Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT)
screen = pygame.display.set_mode(window_size,
                                 pygame.DOUBLEBUF, 32)


# - Set the starting number of lives - #
Globals.LIVES = 3

# - Set the order of the rooms - #
levels = ["Level_1", "Level_2", "Level_3"]
# - Set the starting level - #
next_level = 0


# - Main Game Loop. Steps through the levels defined in levels[] - #
while Globals.running:

    curr_level = next_level
    next_level += 1
    next_level %= len(levels)
    mod_name = "Rooms.{}".format(levels[curr_level])
    mod = __import__(mod_name)
    class_name = getattr(mod, levels[curr_level])
    room = class_name(screen)
    exit_val = room.run()

    if exit_val is True or Globals.running is False:

        # - Set this number to the level you want to jump to when the game ends - #
        next_level = 0

        if len(levels) == 1:
            break

sys.exit()
