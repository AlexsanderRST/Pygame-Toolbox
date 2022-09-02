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
        self.updatables = pygame.sprite.Group()
        self.drawables = pygame.sprite.Group()

    def add(self, sprite: pygame.sprite.Sprite):
        self.updatables.add(sprite)
        self.drawables.add(sprite)

    def draw(self, surface: pygame.Surface):
        surface.fill(self.color_bg)
        self.drawables.draw(surface)

    def update(self, events: list):
        self.updatables.update()
