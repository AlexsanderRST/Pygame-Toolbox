"""
Alexsander Rosante's creation \n
Github: https://github.com/AlexsanderRST
"""

import pygame
from pygame.locals import *


fonts_dir = 'fonts/'


def set_fonts_dir(path):
    global fonts_dir
    fonts_dir = path


class SelectionText(pygame.sprite.Sprite):
    def __init__(self,
                 text='This is a Selection Text',
                 font='', font_size=32, font_color=Color('white'), font_aa=True,
                 bg_color=Color('black'),
                 outline=3, outline_color=Color('white'),
                 hoverline=3, hoverline_color=Color('yellow'),
                 padx=10, pady=10, border_radius=-1,
                 icon='', icon_dir='images/', icon_ext='.png', icon_pos='',
                 on_click=lambda: None):
        super().__init__()

        # font'n'text
        try:
            self.font = pygame.font.Font(f'{fonts_dir}{font}.ttf', font_size)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, font_size)
        self.font_size = font_size
        self.font_color = font_color

        # properties
        self.font_aa = font_aa
        self.padx, self.pady = padx, pady
        self.border_radius = border_radius
        self.bg_color = bg_color
        self.outline_width = 3
        self.outline_color = self.bg_color
        self.hoverline_width = hoverline
        self.hoverline_color = hoverline_color
        self.on_click = on_click

        # text rect
        self.text_surf = self.font.render(text, self.font_aa, self.font_color)
        self.text_rect = self.text_surf.get_rect(topleft=(self.padx, self.pady))

        # gets text size
        text_w, text_h = self.text_rect.size

        # icon
        self.icon = pygame.Surface((1, 1), SRCALPHA)
        self.icon_rect = pygame.Rect(self.padx, self.pady, 1, 1)
        icon_width = 0
        if icon:
            try:
                self.icon = pygame.image.load(f'{icon_dir}{icon}{icon_ext}').convert_alpha()
                self.icon = pygame.transform.smoothscale(self.icon, (text_h, text_h))
                icon_width = self.icon.get_width() + self.padx
                if icon_pos == 'right':
                    self.text_rect.left = self.padx
                    self.icon_rect.left = self.text_rect.right + self.padx
                else:
                    self.text_rect.left = self.padx + icon_width
            except FileNotFoundError:
                pass

        # width and height
        self.w = text_w + 2 * self.padx + icon_width
        self.h = text_h + 2 * self.pady

        # image'n'rect
        self.image = pygame.Surface((self.w, self.h))
        self.rect = self.image.get_rect()

        # outline setup
        if outline:
            self.outline_width = outline
            self.outline_color = outline_color

    def update(self):
        self.image = pygame.Surface((self.w, self.h), SRCALPHA)
        rect = [0, 0, self.w, self.h]
        pygame.draw.rect(self.image, self.bg_color, rect, 0, self.border_radius)
        self.image.blit(self.icon, self.icon_rect)
        self.image.blit(self.text_surf, self.text_rect)
        if self.hovered():
            pygame.draw.rect(self.image, self.hoverline_color, rect, self.hoverline_width, self.border_radius)
        else:
            pygame.draw.rect(self.image, self.outline_color, rect, self.outline_width, self.border_radius)

    def hovered(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False


class TypingText(pygame.sprite.Sprite):
    def __init__(self,
                 text="I'm an Animated Text!",
                 font='', font_size=32, font_color=Color('white'), font_aa=True,
                 bg_color=Color('black'),
                 padx=10, pady=10,
                 vel=1,
                 outline=0, outline_color=Color('white'),
                 start_at_init=True, finish_at_init=False,
                 on_end=lambda: None,
                 ):
        super().__init__()

        # font
        try:
            self.font = pygame.font.Font(f'{fonts_dir}{font}.ttf', font_size)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, font_size)

        # properties
        self.text = list(text)
        self.padx, self.pady = padx, pady
        self.frame = 0
        self.frame_counter = 0
        self.vel = vel
        self.bg_color = bg_color
        self.font_color = font_color
        self.font_aa = font_aa
        self.outline_width = 1
        self.outline_color = bg_color
        self.on_end = on_end

        # get text size
        text = self.font.render(''.join(self.text), self.font_aa, Color('black'))

        # image'n'rect
        self.image = pygame.Surface((text.get_width() + 2 * self.padx, text.get_height() + 2 * self.pady))
        self.rect = self.image.get_rect()

        # outline setup
        if outline:
            self.outline_width = outline
            self.outline_color = outline_color

        # initial state managment
        if finish_at_init:
            self.finish()
        elif start_at_init:
            self.start()

    def update(self):
        self.image.fill(self.bg_color)
        if self.frame < len(self.text) * self.vel:
            text = self.font.render(
                ''.join(self.text[:self.frame//self.vel]), self.font_aa, self.font_color, self.bg_color)
            self.frame += self.frame_counter
        else:
            self.end()
            text = self.font.render(
                ''.join(self.text), self.font_aa, self.font_color, self.bg_color)
        self.image.blit(text, (self.padx, self.pady))
        pygame.draw.rect(self.image, self.outline_color, [0, 0, *self.image.get_size()], self.outline_width)

    def start(self):
        self.frame_counter = 1

    def finish(self):
        self.frame = len(self.text) * self.vel

    def end(self):
        self.on_end()
        self.on_end = lambda: None
