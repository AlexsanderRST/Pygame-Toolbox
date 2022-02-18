"""
2022 Alexsander Rosante's creation
https://github.com/AlexsanderRST
"""


from pygame.locals import *
from .debug import debug
from .settings import *


import pygame


class Scene:
    def __init__(self):
        self.color_bg = 'black'

    def update(self, events: list):
        pass

    def draw(self, surface: pygame.Surface):
        surface.fill(self.color_bg)
        debug('Hello to all mothers :D')
