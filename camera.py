from vectors import *
from colour_cls import *
from object_cls import *
from typing import List
import pygame
import constants as const

class Camera:
    def __init__(self, font, small_font, window):
        self.screen_size = Vector2(const.width,const.height)
        self.font = font
        self.small_font = small_font
        self.masses: List[Mass]
        self.strings: List[InelasticLightString]
        self.springs: List[Spring]
        self.window = window

    def display(self):
        for line in self.strings:
            pygame.draw.line(self.window, line.colour.tuple, line.start.pos.tuple, line.end.pos.tuple)
        for spring in self.springs:
            pygame.draw.line(self.window, spring.colour.tuple, spring.start.pos.tuple, spring.end.pos.tuple, width=1+int(spring.width))
        for mass in self.masses:
            pygame.draw.circle(self.window, mass.colour.tuple, mass.pos.tuple, mass.radius)
        