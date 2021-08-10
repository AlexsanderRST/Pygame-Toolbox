"""
Alexsander Rosante's creation \n
Github: https://github.com/AlexsanderRST
"""

import pygame
from pygame.locals import *


class InputBox(pygame.sprite.Sprite):

    def __init__(self,
                 game,
                 width=240,
                 height=60,
                 inputext_color=(0, 0, 0),
                 inputbox_color=(255, 255, 255),
                 border_size=3,
                 border_color=(128, 128, 128),
                 previewtext='',
                 password_mode=False):
        super().__init__()
        self.game = game

        # configs
        self.height = height
        self.border_color = border_color
        self.password_mode = password_mode
        self.game.inputbox_collision = pygame.sprite.Group()

        # bg
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()

        # box
        self.box = pygame.Surface((width - 2 * border_size,
                                   height - 2 * border_size))
        self.box.fill(inputbox_color)
        self.box_rect = self.box.get_rect(left=border_size,
                                          centery=height / 2)

        # input text
        self.font = pygame.font.SysFont('Consolas', 32)
        self.text = ''
        self.blitable_text = str(self.text)

        # caret
        self.caret = self.Carret(self.font.get_height(), inputext_color, inputbox_color)

        # preview text
        self.previewtext = self.font.render(previewtext, True, inputext_color)
        self.previewtext.set_alpha(128)

    def update(self):
        self.image.fill(self.border_color)
        self.input_check()
        box = self.box.copy()

        # text
        text = self.font.render(self.blitable_text, True, (0, 0, 0))
        if text.get_width() < box.get_width():
            text_rect = text.get_rect(midleft=(5, box.get_height() / 2))
        else:
            text_rect = text.get_rect(midright=(box.get_width() - 5, box.get_height() / 2))
        if self.text:
            box.blit(text, text_rect)
        else:
            box.blit(self.previewtext, text_rect)

        # caret
        self.caret.rect.midleft = text_rect.midright
        self.caret.update()
        box.blit(self.caret.image, self.caret.rect)

        self.image.blit(box, self.box_rect)

    def input_check(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.game.inputbox_collision.add(self)
            for event in self.game.events:
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
            if self.password_mode:
                self.blitable_text = len(self.text) * '*'
            else:
                self.blitable_text = str(self.text)
        else:
            self.game.inputbox_collision.remove(self)

    def clean(self):
        self.text = ''
        self.blitable_text = str(self.text)

    class Carret(pygame.sprite.Sprite):
        def __init__(self, font_height, inputext_color, inputbox_color):
            pygame.sprite.Sprite.__init__(self)
            self.visible_color, self.hidden_color = inputext_color, inputbox_color
            self.image = pygame.Surface((3, font_height))
            self.rect = self.image.get_rect()
            self.frame = 0

        def update(self, blinkspeed=1):
            if self.frame < 30:
                self.image.fill(self.visible_color)
            elif self.frame < 60:
                self.image.fill(self.hidden_color)
            else:
                self.frame = 0
            self.frame += blinkspeed
