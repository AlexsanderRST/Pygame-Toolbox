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
                 font='', font_size=32, font_color=Color('white'), font_aa=True,
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
        text_dict = {'font': font, 'font_size': font_size, 'font_color': font_color, 'font_aa': font_aa,
                     'bg_color': self.bg_color,
                     'vel': typing_vel,
                     'padx': 0, 'pady': 0}

        # lines
        last_line = None
        last_bottom = pady
        for i in range(len(dialog)):
            if i == 0:
                line = TypingText(text=dialog[i], **text_dict)
            else:
                line = TypingText(text=dialog[i], start_at_init=False, **text_dict)
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


class NameBox(pygame.sprite.Sprite):
    def __init__(self,
                 dialog=('Line 1', 'Line 2', 'Line 3', 'Line 4'),
                 font='', font_size=32, font_color=Color('white'), font_aa=True,
                 bg_color=Color('darkblue'),
                 width=0,
                 padx=10, pady=10, space=3,
                 outline=0, outline_color=Color('white'),
                 typing_vel=5,
                 name='', name_pos='',
                 name_font='', name_size=0, name_color=Color('white'),
                 name_bg=Color('blue'),
                 ):
        super().__init__()

        self.group = pygame.sprite.Group()

        # name
        name_height = 0
        if name:
            if not name_font:
                name_font = font
            if not name_size:
                name_size = font_size
            name = TypingText(text=name,
                              font=name_font, font_size=name_size, font_color=name_color,
                              bg_color=name_bg,
                              finish_at_init=True,
                              )
            name_height = name.rect.h
            self.group.add(name)

        # box
        box = Box(dialog,
                  font, font_size, font_color, font_aa,
                  bg_color,
                  width,
                  padx, pady, space,
                  outline, outline_color,
                  typing_vel)
        box.rect.top = name_height
        self.group.add(box)

        # gets surf width
        if name_height > 0:
            if box.rect.w > name.rect.w:
                width = box.rect.w
            else:
                width = name.rect.w

        self.image = pygame.Surface((width, box.rect.height + name_height), SRCALPHA)
        self.rect = self.image.get_rect()

    def update(self):
        self.group.update()
        self.group.draw(self.image)
