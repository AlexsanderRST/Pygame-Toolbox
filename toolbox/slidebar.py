"""
Alexsander Rosante's creation \n
Github: https://github.com/AlexsanderRST
"""

from pygame.locals import *

import pygame


class SlideBar(pygame.sprite.Group):
    def __init__(self,
                 pos: dict = None,
                 vertical=False,
                 inverted_value=False,
                 bar_surf: pygame.Surface = None,
                 bar_w=-1,
                 bar_h=-1,
                 bar_hint_w=.75,
                 bar_hint_h=.075,
                 bar_roundness=30,
                 bar_outline=-1,
                 bar_color='gray',
                 bar_color_outline='black',
                 slider_surf: pygame.Surface = None,
                 slider_w=100,
                 slider_h=100,
                 slider_shape='',
                 slider_outline=-1,
                 slider_color='white',
                 slider_color_outline='darkgray',
                 ):
        super().__init__()

        # properties
        self.value = 0.
        self.rect = pygame.Surface((1, 1)).get_rect(**pos if pos is not None else {'topleft': (0, 0)})
        self.vertical = vertical
        self.inverted_value = inverted_value

        # get screen size
        screen_w, screen_h = pygame.display.get_surface().get_rect().size

        # get the bar size
        if bar_surf:
            bar_w, bar_h = bar_surf.get_size()
        else:
            bar_w = bar_w if bar_w > 0 else bar_hint_w * screen_w
            bar_h = bar_h if bar_h > 0 else bar_hint_h * screen_h

        # get the slider size
        if slider_surf:
            slider_w, slider_h = slider_surf.get_size()

        # create the bar
        self.bar = pygame.sprite.Sprite()
        self.bar.size = bar_w, bar_h
        self.bar.roundness = bar_roundness
        self.bar.outline = bar_outline
        self.bar.color = bar_color
        self.bar.color_outline = bar_color_outline
        self.bar.surf = bar_surf
        self.bar.image = pygame.Surface(self.bar.size, SRCALPHA)
        self.bar.rect = self.bar.image.get_rect(center=self.rect.center)
        self.add(self.bar)

        # create the slide
        self.slider = pygame.sprite.Sprite()
        self.slider.size = slider_w, slider_h
        self.slider.color = slider_color
        self.slider.shape = slider_shape
        self.slider.outline = slider_outline
        self.slider.color_outline = slider_color_outline
        self.slider.surf = slider_surf
        self.slider.image = pygame.Surface(self.slider.size, SRCALPHA)
        self.slider.rect = self.slider.image.get_rect()
        self.slider.action = lambda: None
        self.add(self.slider)

        # set styles
        self.set_bar_style()
        self.set_slide_style()

        # set orientation
        if not vertical:
            self.follow_mouse = self._follow_mouse_x
            self.slider.rect.center = self.bar.rect.midleft
        else:
            self.follow_mouse = self._follow_mouse_y
            self.slider.rect.center = self.bar.rect.midtop

    def _follow_mouse_x(self):
        mouse_x = pygame.mouse.get_pos()[0]
        if mouse_x < self.bar.rect.left:
            self.slider.rect.centerx = self.bar.rect.left
            self.value = float(bool(self.inverted_value))
        elif mouse_x > self.bar.rect.right:
            self.slider.rect.centerx = self.bar.rect.right
            self.value = float(bool(not self.inverted_value))
        else:
            self.slider.rect.centerx = mouse_x
            value = (mouse_x - self.bar.rect.left) / self.bar.rect.w
            self.value = value if not self.inverted_value else 1 - value

    def _follow_mouse_y(self):
        mouse_y = pygame.mouse.get_pos()[1]
        if mouse_y < self.bar.rect.top:
            self.slider.rect.centery = self.bar.rect.top
            self.value = float(bool(self.inverted_value))
        elif mouse_y > self.bar.rect.bottom:
            self.slider.rect.centery = self.bar.rect.bottom
            self.value = float(bool(not self.inverted_value))
        else:
            self.slider.rect.centery = mouse_y
            value = (mouse_y - self.bar.rect.top) / self.bar.rect.h
            self.value = value if not self.inverted_value else 1 - value

    def set_bar_style(self):
        self.bar.image = pygame.Surface(self.bar.size, SRCALPHA)
        if self.bar.surf:
            self.bar.image.blit(self.bar.surf, (0, 0))
        else:
            bar_rect = [0, 0, *self.bar.rect.size]
            pygame.draw.rect(self.bar.image, self.bar.color, bar_rect, 0, self.bar.roundness)
            if self.bar.outline:
                pygame.draw.rect(self.bar.image, self.bar.color_outline, bar_rect, self.bar.outline, self.bar.roundness)

    def set_slide_style(self):
        self.slider.image = pygame.Surface(self.slider.size, SRCALPHA)
        if self.slider.surf:
            self.slider.image.blit(self.slider.surf, (0, 0))
        else:
            slider, slider_rect = self.slider, [0, 0, *self.slider.size]
            match slider.shape:
                case 'square':
                    draw_shape = pygame.draw.rect
                case _:
                    draw_shape = pygame.draw.ellipse
            draw_shape(slider.image, slider.color, slider_rect)
            if slider.outline:
                draw_shape(slider.image, slider.color_outline, slider_rect, slider.outline)

    def slider_hovered(self):
        return self.slider.rect.collidepoint(pygame.mouse.get_pos())

    def update(self, events: list):
        for event in events:
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.slider_hovered():
                self.slider.action = self.follow_mouse
            elif event.type == MOUSEBUTTONUP:
                self.slider.action = lambda: None
        self.slider.action()
