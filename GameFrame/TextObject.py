import pygame
from GameFrame import RoomObject, Level


class TextObject(RoomObject):
    def __init__(self, room: Level, x: int, y: int, text='Not Set', size=60,
                 font='Comic Sans MS', colour=(0, 0, 0), bold=False):
        RoomObject.__init__(self, room, x, y)

        self.rendered_text = 0
        self.rect = 0
        self.built_font = 0
        self.text = text
        self.size = size
        self.font = font
        self.colour = colour
        self.bold = bold
        self.update_text()

    def update_text(self):
        self.built_font = pygame.font.SysFont(self.font, self.size, self.bold)
        self.rendered_text = self.built_font.render(self.text, False, self.colour)
        self.image = self.rendered_text
        self.width, self.height = self.built_font.size(self.text)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
