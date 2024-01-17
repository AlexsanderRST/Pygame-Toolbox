"""
Alexsander Rosante's creation
Settings like screen width and height; or fps are imported
"""

from pygame.locals import *
from toolbox.slidebar import SlideBar

import pygame

pygame.init()


class Scene:
    def __init__(self):
        # properties
        self.color_bg = '#fedc56'
        self.color = [255, 255, 255]

        # color retangle
        self.color_rect = pygame.Rect(0, .15 * screen_h, .25 * screen_h, .25 * screen_h)
        self.color_rect.centerx = screen_w / 2

        # general slide bars parameters
        bar_params = {
            'bar_hint_h': .05,
            'bar_outline': 4,
            'bar_color_outline': 'black',
            'slider_w': .085 * screen_h,
            'slider_h': .085 * screen_h,
            'slider_outline': 4,
            'slider_color_outline': 'black'
        }

        # set slide bars
        self.red = SlideBar(pos={'center': (screen_w / 2, screen_h * .575)}, slider_color='red', **bar_params)
        self.green = SlideBar(pos={'center': (screen_w / 2, screen_h * .725)}, slider_color='green', **bar_params)
        self.blue = SlideBar(pos={'center': (screen_w / 2, screen_h * .875)}, slider_color='blue', **bar_params)
        self.slide_bars = (self.red, self.green, self.blue)

    def check_hover_on_sliders(self):
        game.hovered.empty()
        for slide_bar in self.slide_bars:
            if slide_bar.slider_hovered():
                game.hovered.add(slide_bar.slider)

    def update_bar_colors(self):
        self.red.bar.color = (round(self.red.value * 255), 0, 0)
        self.green.bar.color = (0, round(self.green.value * 255), 0)
        self.blue.bar.color = (0, 0, round(self.blue.value * 255))
        self.red.set_bar_style()
        self.blue.set_bar_style()
        self.green.set_bar_style()

    def update_color(self):
        red = round(self.red.value * 255)
        green = round(self.green.value * 255)
        blue = round(self.blue.value * 255)
        self.color = red, green, blue
        self.update_bar_colors()

    def update(self, events: list):
        for slide_bar in self.slide_bars:
            slide_bar.update(events)

    def draw(self, surface: pygame.Surface):
        surface.fill(self.color_bg)

        # draws color rect
        self.update_color()
        pygame.draw.rect(surface, self.color, self.color_rect, border_radius=20)
        pygame.draw.rect(surface, 'black', self.color_rect, border_radius=20, width=4)

        # draws slide bars
        for slide_bar in self.slide_bars:
            slide_bar.draw(surface)

        self.check_hover_on_sliders()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        pygame.display.set_caption(f'Color Maker ({version})')
        self.clock = pygame.time.Clock()
        self.events = pygame.event.get()
        self.loop = True
        self.hovered = pygame.sprite.GroupSingle()
        self.scene = Scene()

    def cursor_by_context(self):
        pygame.mouse.set_cursor(
            {0: SYSTEM_CURSOR_ARROW, 1: SYSTEM_CURSOR_HAND}
            [len(self.hovered.sprites())])

    def check_events(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == QUIT:
                self.loop = False

    def run(self):
        while self.loop:
            self.check_events()
            self.cursor_by_context()
            self.scene.update(self.events)
            self.scene.draw(self.screen)
            pygame.display.update()
            self.clock.tick(fps)
        pygame.quit()


if __name__ == '__main__':
    # properties
    version = '1.0'
    screen_w = 364
    screen_h = 648
    fps = 60

    game = Game()
    game.run()
