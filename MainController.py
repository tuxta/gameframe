#!/usr/bin/python3

import sys

import pygame

from GameFrame import Globals
from Rooms import *

pygame.init()
pygame.font.init()
pygame.display.set_caption("My Awesome Game")
window_size = (Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT)
screen = pygame.display.set_mode(window_size,
                                 pygame.DOUBLEBUF, 32)


# - Set the starting number of lives - #
Globals.LIVES = 3




"""
  This is an Example loop that controls progression through levels.
  Allows multiple uses of a level if desired
  (may provide a parameter to a level to indicate a
   repeat visit for instance)

# - Track current level - #
start_screen, level_1, level_2, level_3, end_screen, game_over = 0, 1, 2, 3, 4, 5
curr_level = start_screen

def run_level(room):
    exit_val = room.run()
    if exit_val is True or Globals.running is False:
        global curr_level
        global end_screen
        curr_level = end_screen

while Globals.running:

    if curr_level == start_screen:
        curr_level = level_1
        run_level(ScrollingShooter(screen))

    elif curr_level == level_1:
        curr_level = level_2
        run_level(Maze(screen))

    elif curr_level == level_2:
        curr_level = level_3
        run_level(BreakOutL1(screen))

    elif curr_level == level_3:
        curr_level = end_screen
        run_level(BreakOutL2(screen))

    elif curr_level == end_screen:
        curr_level = game_over

    else:
        Globals.running = False
"""

sys.exit()
