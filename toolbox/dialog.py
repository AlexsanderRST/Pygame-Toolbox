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
                 font_name='', font_color=Color('white'),
                 bg_color=Color('darkblue'),
                 width=0,
                 padx=10, pady=10, space=3,
                 outline=0, outline_color=Color('white'),
                 typing_vel=5):
        super().__init__()

        # properties
        self.lines = pygame.sprite.Group()
        self.bg_color = bg_color
        self.padx, self.pady = padx, pady
        self.outline_width = 1
        self.outline_color = bg_color
        default_text = {'font_name': font_name, 'font_color': font_color,
                        'bg_color': self.bg_color,
                        'vel': typing_vel,
                        'padx': 0, 'pady': 0}

        # lines
        last_line = None
        last_bottom = pady
        for i in range(len(dialog)):
            if i == 0:
                line = TypingText(text=dialog[i], **default_text)
            else:
                line = TypingText(text=dialog[i], start_at_init=False, **default_text)
                last_line.on_end = line.start
            last_line = line
            line.rect.topleft = padx, last_bottom
            last_bottom = line.rect.bottom + space
            self.lines.add(line)

        # gets surf width
        if not width:
            for line in self.lines:
                if line.image.get_width() > width:
                    width = line.image.get_width()
            width += 2 * padx

        # gets surf height
        height = self.lines.sprites()[-1].rect.bottom - self.lines.sprites()[0].rect.top + 2 * pady

        # image'n'rect
        self.image = pygame.Surface((width, height), SRCALPHA)
        self.rect = self.image.get_rect()

        # outline
        if outline:
            self.outline_width = outline
            self.outline_color = outline_color

    def update(self):
        pygame.draw.rect(self.image, self.bg_color, [0, 0, *self.rect.size])
        pygame.draw.rect(self.image, self.outline_color, [0, 0, *self.rect.size], self.outline_width)
        self.lines.update()
        self.lines.draw(self.image)
