"""Alexsander Rosante's Creation 2021"""

import pygame
from pygame.locals import *


fonts_dir = 'fonts/'


def set_fonts_dir(directory):
    global fonts_dir
    fonts_dir = directory


class SelectionText(pygame.sprite.Sprite):
    def __init__(self,
                 text='This is a Selection Text',
                 font_name='', font_size=32, font_color=Color('white'),
                 bg_color=Color('black'),
                 outline=3, outline_color=Color('white'),
                 hoverline=3, hoverline_color=Color('yellow'),
                 padx=10, pady=10,
                 on_click=lambda: None):
        super().__init__()

        # font'n'text
        try:
            self.font = pygame.font.Font(f'{fonts_dir}{font_name}.ttf', font_size)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, font_size)
        self.font_size = font_size
        self.font_color = font_color

        # properties
        self.text = text
        self.padx, self.pady = padx, pady
        text = self.font.render(self.text, True, self.font_color)
        self.w = text.get_width() + 2 * self.padx
        self.h = text.get_height() + 2 * self.pady
        self.bg_color = bg_color
        self.outline_width = 3
        self.outline_color = self.bg_color
        self.hoverline_width = hoverline
        self.hoverline_color = hoverline_color
        self.on_click = on_click

        # image and rect
        self.image = pygame.Surface((self.w, self.h))
        self.rect = self.image.get_rect()

        # outline setup
        if outline:
            self.outline_width = outline
            self.outline_color = outline_color

    def update(self):
        self.image = pygame.Surface((self.w, self.h))
        self.image.fill(self.bg_color)
        self.image.blit(self.font.render(self.text, True, self.font_color),
                        (self.padx, self.pady))
        if self.hovered():
            pygame.draw.rect(self.image, self.hoverline_color, (0, 0, self.w, self.h), self.hoverline_width)
        else:
            pygame.draw.rect(self.image, self.outline_color, (0, 0, self.w, self.h), self.outline_width)

    def hovered(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False


class AnimatedText(pygame.sprite.Sprite):
    def __init__(self,
                 text="I'm an Animated Text!",
                 font_name='', font_size=32, font_color=Color('white'),
                 bg_color=Color('black'),
                 padx=10, pady=10,
                 vel=1,
                 outline=0, outline_color=Color('white'),
                 on_end=lambda: None,
                 ):
        super().__init__()

        # font
        try:
            self.font = pygame.font.Font(f'{fonts_dir}{font_name}.ttf', font_size)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, font_size)

        # properties
        self.text = list(text)
        self.padx, self.pady = padx, pady
        self.frame = 0
        self.vel = vel
        self.bg_color = bg_color
        self.font_color = font_color
        self.outline_width = 1
        self.outline_color = bg_color
        self.on_end = on_end

        # get text size
        text = self.font.render(''.join(self.text), True, Color('black'))

        # image'n'rect
        self.image = pygame.Surface((text.get_width() + 2 * self.padx, text.get_height() + 2 * self.pady))
        self.rect = self.image.get_rect()

        # outline setup
        if outline:
            self.outline_width = outline
            self.outline_color = outline_color

    def update(self):
        self.image.fill(self.bg_color)
        if self.frame <= len(self.text) * self.vel:
            text = self.font.render(''.join(self.text[:self.frame//self.vel]), True, self.font_color, self.bg_color)
            self.frame += 1
        else:
            self.end()
            text = self.font.render(''.join(self.text), True, self.font_color, self.bg_color)
        self.image.blit(text, (self.padx, self.pady))
        pygame.draw.rect(self.image, self.outline_color, [0, 0, *self.image.get_size()], self.outline_width)

    def end(self):
        self.on_end()
        self.on_end = lambda: None
