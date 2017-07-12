import sys
import pygame
from Rooms import * 
from GameFrame import Globals

pygame.init()
pygame.display.set_caption("My Awesome Game")
window_size = (Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT)
screen = pygame.display.set_mode(window_size,
                                 pygame.DOUBLEBUF, 32)

# - Track current level - #
start_screen, level_1, level_2, end_screen, game_over = 0, 1, 2, 3, 4
curr_level = start_screen

# - Set the starting number of lives - #
Globals.LIVES = 3

"""
  This loop controls progression through the levels.
  Allows multiple uses of a level if desired
  (may provide a parameter to a level to indicate a
   repeat visit for instance)
"""
while Globals.running:
    if curr_level == start_screen:
        curr_level = level_1
    elif curr_level == level_1:
        room = Room1(screen)
        exit_val = room.run()
        if exit_val is True or Globals.running is False:
            curr_level = end_screen
        else:
            curr_level = level_2
    elif curr_level == level_2:
        room = Room2(screen)
        room.run()
        curr_level = end_screen
    elif curr_level == end_screen:
        curr_level = game_over
    else:
        Globals.running = False
sys.exit()
