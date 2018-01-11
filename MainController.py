#!/usr/bin/python3

import sys
import pygame
from GameFrame import Globals

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()
pygame.font.init()

pygame.display.set_caption(Globals.window_name)
window_size = (Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT)
screen = pygame.display.set_mode(window_size,
                                 pygame.DOUBLEBUF, 32)

next_level = Globals.start_level
levels = Globals.levels

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

        next_level = Globals.end_game_level

        if len(levels) == 1:
            break

    if Globals.exiting:
        break

sys.exit()
