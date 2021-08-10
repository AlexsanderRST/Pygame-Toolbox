"""
Alexsander Rosante's creation \n
Github: https://github.com/AlexsanderRST
"""

import pygame
from pygame.locals import *


class LoadingBar(pygame.sprite.Sprite):

    def __init__(self,
                 width=560,
                 height=80,
                 color=(0, 255, 0),
                 bg_color=(65, 65, 65),
                 border_size=0,
                 grow_vel=0,
                 end_command=lambda: False,
                 text_method='',
                 text_prefix='',
                 text_suffix='',
                 text_size=32,
                 max_items=1,
                 text_pos=''):
        super().__init__()

        self.color = color
        self.bg_color = bg_color
        self.border_size = border_size
        self.grow_vel = grow_vel

        # bg
        self.image = pygame.Surface((width, height))
        self.image.fill(self.bg_color)
        self.rect = self.image.get_rect()

        # loading bar
        self.width = 0.01
        self.max_width = width - 2 * self.border_size
        self.height = height - 2 * self.border_size

        # text
        if text_method:
            self.font = pygame.font.SysFont('Consolas', text_size)
            if text_method == 'percentage':
                self.text = self.get_percent
            elif text_method == 'item':
                self.max_items = max_items
                self.text = self.get_items_proportion
            if not text_pos or text_pos == 'center':
                self.blit_text = self.text_centered
        else:
            self.blit_text = lambda: None
        self.text_prefix = text_prefix
        self.text_suffix = text_suffix

        self.end_command = end_command

    def update(self):
        self.image.fill(self.bg_color)
        # bar
        if self.width < self.max_width:
            self.width += self.grow_vel
        else:
            self.width = self.max_width
            self.end_command()
        pygame.draw.rect(self.image, self.color, (self.border_size,
                                                  self.border_size,
                                                  self.width,
                                                  self.height))

        # texts
        self.blit_text()

    def add_percent(self, percent: float):
        self.width += self.max_width * percent

    def get_percent(self):
        return '{:.1%}'.format(self.width / self.max_width)

    def get_items_proportion(self):
        return '{}/{}'.format(round(self.width/self.max_width*self.max_items), self.max_items)

    def text_centered(self):
        text = '{} {} {}'.format(self.text_prefix, self.text(), self.text_suffix)
        text_surf = self.font.render(text, True, Color('white'))
        text_rect = text_surf.get_rect(center=(self.max_width / 2, self.height / 2))
        self.image.blit(text_surf, text_rect)
