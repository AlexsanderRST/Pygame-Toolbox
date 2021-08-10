"""
Alexsander Rosante's creation \n
Github: https://github.com/AlexsanderRST
"""

import pygame
from pygame.locals import *

font_directory = 'fonts/'
icon_directory = 'images/'


class Button(pygame.sprite.Sprite):

    def __init__(self,
                 game,
                 width=0,
                 height=0,
                 depth=10,
                 color=(178, 34, 34),
                 color_above=(193, 78, 78),
                 color_pressed=(142, 27, 27),
                 color_below=(65, 65, 65),
                 text='',
                 text_size=0,
                 text_color=(255, 255, 255),
                 text_font='',
                 text_sysfont='',
                 text_at_left=False,
                 text_at_right=False,
                 aatext=True,
                 icon='',
                 icon_size=0,
                 icon_fit=False,
                 icon_centered=True,
                 icon_at_left=True,
                 command=lambda: None,
                 interactive=True):
        super().__init__()
        self.game = game

        self.command = command

        if width <= 0:
            width = 240
        if height <= 0:
            height = 60
        border_dist = 5

        # transparent bg
        self.image = pygame.Surface((width, height + depth), SRCALPHA)
        self.rect = self.image.get_rect()

        # idle surf
        front = pygame.Surface((width, height))
        front.fill(color)
        front_rect = front.get_rect(top=depth)
        above = pygame.Surface((width, depth))
        above.fill(color_above)
        above_rect = above.get_rect()
        self.idle_surf = self.image.copy()
        self.idle_surf.blit(front, front_rect)
        self.idle_surf.blit(above, above_rect)

        # pushed surf
        front.fill(color_pressed)
        front_rect.top = 0
        below = pygame.Surface((width, depth))
        below.fill(color_below)
        below_rect = below.get_rect(top=height)
        self.pressed_surf = self.image.copy()
        self.pressed_surf.blit(front, front_rect)
        self.pressed_surf.blit(below, below_rect)

        # text and icon
        text_surf = pygame.Surface((1, 1))
        if text:
            # create text surf
            if not text_size:
                text_size = round(8 / 15 * height)
            # font load
            font = pygame.font.SysFont('Arial', text_size)
            if text_font:
                try:
                    font = pygame.font.Font('{0}{1}.ttf'.format(font_directory, text_font), text_size)
                except FileNotFoundError:
                    pass
            elif text_sysfont:
                font = pygame.font.SysFont(text_sysfont, text_size)

            text_surf = font.render(text, aatext, text_color)

        if icon:
            # create icon surf
            try:
                icon_surf = pygame.image.load('{0}{1}.png'.format(icon_directory, icon))
            except FileNotFoundError:
                icon_surf = pygame.Surface((10, 10), SRCALPHA)
            # resize icon surf to fit at button and create it's rect
            if not icon_size:
                icon_fit = True
            if icon_fit:
                if width > height:
                    icon_size = round(height - 2 * border_dist)
                else:
                    icon_size = round(width - 2 * border_dist)
            icon_surf = pygame.transform.smoothscale(icon_surf.copy(),
                                                     [icon_size for _ in range(2)])
            # icon_rect
            icon_rect = icon_surf.get_rect()

            if text:
                # resize text surf, if needed, to fit at button with icon surf
                text_size = width - icon_size - 3 * border_dist
                if text_surf.get_width() > text_size:
                    text_surf = pygame.transform.scale(text_surf.copy(),
                                                       (text_size, text_surf.get_height()))
                # text_rect
                text_rect = text_surf.get_rect()
                # icon and text position set
                for i in ((self.idle_surf, depth), (self.pressed_surf, 0)):
                    front_rect.top = i[1]
                    if icon_at_left:
                        icon_rect.left = border_dist
                        text_rect.centerx = width - text_size / 2 - border_dist
                    else:
                        icon_rect.right = width - border_dist
                        text_rect.centerx = text_size / 2 + border_dist
                    icon_rect.centery = front_rect.centery
                    text_rect.centery = front_rect.centery
                    i[0].blit(icon_surf, icon_rect)
                    i[0].blit(text_surf, text_rect)
            else:
                # icon surf position set
                for i in ((self.idle_surf, depth), (self.pressed_surf, 0)):
                    front_rect.top = i[1]
                    if icon_centered:
                        icon_rect.centerx = front_rect.centerx
                    elif icon_at_left:
                        icon_rect.left = border_dist
                    else:
                        icon_rect.right = width - border_dist
                    icon_rect.centery = front_rect.centery
                    i[0].blit(icon_surf, icon_rect)

        elif text:
            # resize text surf, if needed
            text_size = width - 2 * border_dist
            if text_surf.get_width() > text_size:
                text_surf = pygame.transform.scale(text_surf.copy(),
                                                   (text_size, text_surf.get_height()))
            # text rect
            text_rect = text_surf.get_rect()
            # text surf position set
            for i in ((self.idle_surf, depth), (self.pressed_surf, 0)):
                front_rect.top = i[1]
                if text_at_left:
                    text_rect.left = border_dist
                elif text_at_right:
                    text_rect.right = front_rect.right - border_dist
                else:
                    text_rect.centerx = front_rect.centerx
                text_rect.centery = front_rect.centery
                i[0].blit(text_surf, text_rect)

        # interaction
        self.interaction = lambda: None
        if interactive:
            self.interaction = self.interactive
            self.game.button_collision = pygame.sprite.Group()

        self.image = self.idle_surf.copy()

    def update(self):
        self.interaction()

    def interactive(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.game.button_collision.add(self)
            for event in self.game.events:
                if event.type == MOUSEBUTTONDOWN:
                    self.image = self.pressed_surf.copy()
                elif event.type == MOUSEBUTTONUP:
                    self.command()
                    self.image = self.idle_surf.copy()
        else:
            self.image = self.idle_surf.copy()
            self.game.button_collision.remove(self)
