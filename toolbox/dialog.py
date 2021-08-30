"""
Alexsander Rosante's creation \n
Github: https://github.com/AlexsanderRST
"""

import pygame
from pygame.locals import *
from codes.toolbox.text import TypingText, set_fonts_dir


class Box(pygame.sprite.Sprite):
    def __init__(self,
                 dialog=('Line 1', 'Line 2', 'Line 3', 'Line 4'),
                 font='', font_size=32, font_color=Color('white'), font_aa=True,
                 bg_color=Color('darkblue'),
                 width=0,
                 padx=10, pady=10, space=3, border_radius=-1,
                 outline=0, outline_color=Color('white'),
                 typing_vel=5,
                 on_end=lambda: None):
        super().__init__()

        # properties
        self.lines = pygame.sprite.Group()
        self.bg_color = bg_color
        self.padx, self.pady = padx, pady
        self.outline_width = 1
        self.outline_color = bg_color
        self.border_r = border_radius

        # default box
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
                if i == len(dialog) - 1:
                    line.on_end = on_end
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

    def set_on_end(self, new_function):
        self.lines.sprites()[-1].on_end = new_function

    def update(self):
        rect = pygame.Rect([0, 0, *self.rect.size])
        pygame.draw.rect(self.image, self.bg_color, rect, border_radius=self.border_r)
        pygame.draw.rect(self.image, self.outline_color, rect, self.outline_width, border_radius=self.border_r)
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


def get_speech_arrow_points(fix_point, rect, width):
    p1, p2, p3 = fix_point, 0, 0
    if rect.top > p1[1]:
        if rect.left > p1[0]:
            p2 = rect.topleft
            p3 = p2[0] + width, p2[1]
        elif rect.right < p1[0]:
            p2 = rect.topright
            p3 = p2[0] - width, p2[1]
        else:
            p2 = rect.centerx - width / 2, rect.top
            p3 = rect.centerx + width / 2, rect.top
    elif rect.bottom < p1[1]:
        if rect.left > p1[0]:
            p2 = rect.bottomleft
            p3 = p2[0] + width, p2[1]
        elif rect.right < p1[0]:
            p2 = rect.bottomright
            p3 = p2[0] - width, p2[1]
        else:
            p2 = rect.centerx - width / 2, rect.bottom
            p3 = rect.centerx + width / 2, rect.bottom
    else:
        if rect.left > p1[0]:
            p2 = rect.left, rect.centery - width / 2
            p3 = rect.left, rect.centery + width / 2
        elif rect.right < p1[0]:
            p2 = rect.right, rect.centery - width / 2
            p3 = rect.right, rect.centery + width / 2
        else:
            return False
    return p1, p2, p3


def draw_speech_arrow(display, fix_point, rect,
                      bg_color=Color('white'), outline_color=Color('black'),
                      width=50):
    try:
        p1, p2, p3 = get_speech_arrow_points(fix_point, rect, width)
        pygame.draw.polygon(display, bg_color, (p1, p2, p3))
        pygame.draw.polygon(display, outline_color, (p1, p2, p3), 3)
        pygame.draw.line(display, bg_color, p2, p3, 3)
    except TypeError:
        return
