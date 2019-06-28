import pygame
from GameFrame import TextObject, Globals, Level


class EntryTextObject(TextObject):
    def __init__(self, room: Level, x: int, y: int, max_len=4):
        TextObject.__init__(self, room, x, y, '')
        self.max_len = max_len
        self.handle_key_events = True
        self.accepting_input = True
        self.active = True

    def accept_input(self):
        self.accepting_input = True

    def set_focus(self, in_focus: bool):
        self.active = in_focus

    def key_pressed(self, key):
        if self.accepting_input and self.active:

            key_recognised = False
            if key[pygame.K_a]:
                self.text += 'A'
                key_recognised = True
            elif key[pygame.K_b]:
                self.text += 'B'
                key_recognised = True
            elif key[pygame.K_c]:
                self.text += 'C'
                key_recognised = True
            elif key[pygame.K_d]:
                self.text += 'D'
                key_recognised = True
            elif key[pygame.K_e]:
                self.text += 'E'
                key_recognised = True
            elif key[pygame.K_f]:
                self.text += 'F'
                key_recognised = True
            elif key[pygame.K_g]:
                self.text += 'G'
                key_recognised = True
            elif key[pygame.K_h]:
                self.text += 'H'
                key_recognised = True
            elif key[pygame.K_i]:
                self.text += 'I'
                key_recognised = True
            elif key[pygame.K_j]:
                self.text += 'J'
                key_recognised = True
            elif key[pygame.K_k]:
                self.text += 'K'
                key_recognised = True
            elif key[pygame.K_l]:
                self.text += 'L'
                key_recognised = True
            elif key[pygame.K_m]:
                self.text += 'M'
                key_recognised = True
            elif key[pygame.K_n]:
                self.text += 'N'
                key_recognised = True
            elif key[pygame.K_o]:
                self.text += 'O'
                key_recognised = True
            elif key[pygame.K_p]:
                self.text += 'P'
                key_recognised = True
            elif key[pygame.K_q]:
                self.text += 'Q'
                key_recognised = True
            elif key[pygame.K_r]:
                self.text += 'R'
                key_recognised = True
            elif key[pygame.K_s]:
                self.text += 'S'
                key_recognised = True
            elif key[pygame.K_t]:
                self.text += 'T'
                key_recognised = True
            elif key[pygame.K_u]:
                self.text += 'U'
                key_recognised = True
            elif key[pygame.K_v]:
                self.text += 'V'
                key_recognised = True
            elif key[pygame.K_w]:
                self.text += 'W'
                key_recognised = True
            elif key[pygame.K_x]:
                self.text += 'X'
                key_recognised = True
            elif key[pygame.K_y]:
                self.text += 'Y'
                key_recognised = True
            elif key[pygame.K_z]:
                self.text += 'Z'
                key_recognised = True
            elif key[pygame.K_SPACE]:
                self.text += ' '
                key_recognised = True
            elif key[pygame.K_1]:
                self.text += '1'
                key_recognised = True
            elif key[pygame.K_2]:
                self.text += '2'
                key_recognised = True
            elif key[pygame.K_3]:
                self.text += '3'
                key_recognised = True
            elif key[pygame.K_4]:
                self.text += '4'
                key_recognised = True
            elif key[pygame.K_5]:
                self.text += '5'
                key_recognised = True
            elif key[pygame.K_6]:
                self.text += '6'
                key_recognised = True
            elif key[pygame.K_7]:
                self.text += '7'
                key_recognised = True
            elif key[pygame.K_8]:
                self.text += '8'
                key_recognised = True
            elif key[pygame.K_9]:
                self.text += '9'
                key_recognised = True
            elif key[pygame.K_0]:
                self.text += '0'
                key_recognised = True
            elif key[pygame.K_BACKSPACE]:
                if len(self.text) > 0:
                    self.text = self.text[:-1]
                    key_recognised = True

            if key_recognised:
                if len(self.text) > self.max_len:
                    self.text = self.text[:-1]
                self.update_text()
                Globals.player_name = self.text
                self.accepting_input = False
                self.set_timer(5, self.accept_input)
