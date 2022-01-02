"""
Alexsander Rosante's creation \n
Github: https://github.com/AlexsanderRST
"""

from pygame.locals import *

import pygame

font_directory = 'fonts/'
icon_directory = 'images/'


hovered = pygame.sprite.Group()


def unhovered_all():
    global hovered
    hovered.empty()


class Pressing(pygame.sprite.Sprite):
    def __init__(self,
                 width=0,
                 height=0,
                 depth=10,
                 color='#b22222',
                 color_above='#c14e4e',
                 color_pressed='#8e1b1b',
                 color_below='#414141',
                 font_path='',
                 sysfont='',
                 text='',
                 text_color='white',
                 text_size=0,
                 text_at_left=False,
                 text_at_right=False,
                 aatext=True,
                 icon_path='',
                 icon_size=0,
                 icon_fit=False,
                 icon_centered=True,
                 icon_at_left=True,
                 on_click=lambda: None,
                 interactive=True):
        super().__init__()

        self.on_click = on_click

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
        self.surf_idle = self.image.copy()
        self.surf_idle.blit(front, front_rect)
        self.surf_idle.blit(above, above_rect)

        # pushed surf
        front.fill(color_pressed)
        front_rect.top = 0
        below = pygame.Surface((width, depth))
        below.fill(color_below)
        below_rect = below.get_rect(top=height)
        self.surf_pressed = self.image.copy()
        self.surf_pressed.blit(front, front_rect)
        self.surf_pressed.blit(below, below_rect)

        # text and icon
        text_surf = pygame.Surface((1, 1))
        if text:
            # create text surf
            if not text_size:
                text_size = round(8 / 15 * height)
            # font load
            font = pygame.font.Font(None, text_size)
            if font_path:
                try:
                    font = pygame.font.Font(font_path, text_size)
                except FileNotFoundError:
                    pass
            elif sysfont:
                font = pygame.font.SysFont(sysfont, text_size)
            text_surf = font.render(text, aatext, text_color)

        if icon_path:
            # create icon surf
            try:
                icon_surf = pygame.image.load(icon_path)
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
                for i in ((self.surf_idle, depth), (self.surf_pressed, 0)):
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
                for i in ((self.surf_idle, depth), (self.surf_pressed, 0)):
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
            for i in ((self.surf_idle, depth), (self.surf_pressed, 0)):
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

        # define image
        self.image = self.surf_idle.copy()

    def update(self, events):
        self.interaction(events)

    def interactive(self, events):
        global hovered
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.surf_idle.copy()
            hovered.remove(self)
        else:
            for event in events:
                if event.type == MOUSEBUTTONDOWN:
                    self.image = self.surf_pressed.copy()
                elif event.type == MOUSEBUTTONUP:
                    self.image = self.surf_idle.copy()
                    self.on_click()
            hovered.add(self)


class Hover(pygame.sprite.Sprite):
    def __init__(self,
                 width=250,
                 height=100,
                 color='#cc0000',
                 color_hovered='#f20000',
                 text='',
                 text_color='white',
                 text_size=32,
                 font_path=None,
                 on_click=lambda: None):
        super().__init__()
        self.surf_idle = pygame.Surface((width, height))
        self.surf_idle.fill(color)
        self.surf_hovered = pygame.Surface((width, height))
        self.surf_hovered.fill(color_hovered)
        self.image = self.surf_idle
        self.rect = self.image.get_rect()
        self.on_click = on_click

        # text
        if text:
            font = pygame.font.Font(font_path, text_size)
            text = font.render(text, True, text_color)
            text_rect = text.get_rect(center=(width/2, height/2))
            self.surf_idle.blit(text, text_rect)
            self.surf_hovered.blit(text, text_rect)

    def update(self, events):
        global hovered
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.surf_hovered
            hovered.add(self)
            for event in events:
                if event.type == MOUSEBUTTONUP and event.button == 1:
                    self.on_click()
        else:
            self.image = self.surf_idle
            hovered.remove(self)


class Underline(pygame.sprite.Sprite):
    def __init__(self,
                 text,
                 text_color='gray',
                 text_color_hovered='white',
                 text_size=32,
                 color='black',
                 offset=10,
                 line_height=1,
                 line_color='white',
                 line_spaccing=3,
                 font_path=None,
                 on_click=lambda: None):
        super().__init__()
        font = pygame.font.Font(font_path, round(text_size))
        width = font.size(text)[0] + offset * 2
        height = font.size(text)[1] + offset * 2 + line_spaccing + line_height
        self.surf_idle = pygame.Surface((width, height))
        self.surf_idle.fill(color)
        self.surf_hovered = self.surf_idle.copy()
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(topleft=(offset, offset))
        self.surf_idle.blit(text_surf, text_rect)
        text_surf = font.render(text, True, text_color_hovered)
        self.surf_hovered.blit(text_surf, text_rect)
        line = pygame.Surface((text_rect.width, line_height))
        line.fill(line_color)
        line_rect = line.get_rect(topleft=(offset, text_rect.bottom + line_spaccing))
        self.surf_hovered.blit(line, line_rect)
        self.image = self.surf_idle.copy()
        self.rect = self.image.get_rect()
        self.on_click = on_click

    def update(self, events):
        global hovered
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.surf_hovered
            hovered.add(self)
            for event in events:
                if event.type == MOUSEBUTTONUP and event.button == 1:
                    self.on_click()
        else:
            self.image = self.surf_idle
            hovered.remove(self)
