"""
Alexsander Rosante's creation \n
Github: https://github.com/AlexsanderRST
"""

import pygame
from pygame.locals import *
from toolbox.text import TypingText


class Box(pygame.sprite.Sprite):
    def __init__(self,
                 dialog=('Line 1', 'Line 2', 'Line 3', 'Line 4'),
                 width=0,
                 font_name='',
                 typing_vel=5):
        super().__init__()

        # properties
        self.bg_color = Color('darkblue')
        self.lines = pygame.sprite.Group()
        default_text = {'font_name': font_name,
                        'bg_color': self.bg_color,
                        'vel': typing_vel,
                        'pady': 5}

        # lines
        last_line = None
        last_bottom = 0
        for i in range(len(dialog)):
            if i == 0:
                line = TypingText(text=dialog[i], **default_text)
            else:
                line = TypingText(text=dialog[i], start_at_init=False, **default_text)
                last_line.on_end = line.start
            last_line = line
            line.rect.topleft = 0, last_bottom
            last_bottom = line.rect.bottom
            self.lines.add(line)

        # gets surf width
        if not width:
            for line in self.lines:
                if line.image.get_width() > width:
                    width = line.image.get_width()

        # gets surf height
        height = sum([line.image.get_height() for line in self.lines])

        # image'n'rect
        self.image = pygame.Surface((width, height), SRCALPHA)
        self.rect = self.image.get_rect()

    def update(self):
        pygame.draw.rect(self.image, self.bg_color, [0, 0, *self.rect.size])
        self.lines.update()
        self.lines.draw(self.image)
