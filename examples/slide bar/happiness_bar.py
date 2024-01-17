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
        self.color_bg = 'blue'

        # load the emojis as surfaces
        self.emoji_surfs, emojis_surf = {}, pygame.image.load('emojis.png').convert_alpha()
        for i in range(5):
            emoji_surf = pygame.Surface((150, 150), SRCALPHA)
            emoji_surf.blit(emojis_surf, (i * -150, 0))
            self.emoji_surfs[i] = emoji_surf

        # setup the slide bar
        self.slide_bar = SlideBar(
            pos={'center': (screen_w / 2, screen_h / 2)},
            bar_hint_w=.75,
            slider_surf=self.emoji_surfs[0])

    def check_hover(self):
        game.hovered.empty()
        if self.slide_bar.slider_hovered():
            game.hovered.add(self.slide_bar.slider)

    def set_bg_color(self):
        self.color_bg = (round((1 - self.slide_bar.value) * 255), round(self.slide_bar.value * 255), 0)

    def set_slider_emoji(self):
        if 0 <= self.slide_bar.value < .2:
            self.slide_bar.slider.surf = self.emoji_surfs[0]
        elif .2 <= self.slide_bar.value < .4:
            self.slide_bar.slider.surf = self.emoji_surfs[1]
        elif .4 <= self.slide_bar.value < .6:
            self.slide_bar.slider.surf = self.emoji_surfs[2]
        elif .6 <= self.slide_bar.value < .8:
            self.slide_bar.slider.surf = self.emoji_surfs[3]
        else:
            self.slide_bar.slider.surf = self.emoji_surfs[4]
        self.slide_bar.set_slide_style()

    def update(self, events: list):
        self.check_hover()
        self.set_bg_color()
        self.set_slider_emoji()
        self.slide_bar.update(events)

    def draw(self, surface: pygame.Surface):
        surface.fill(self.color_bg)
        self.slide_bar.draw(surface)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        pygame.display.set_caption(f'Happiness Bar ({version})')
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
    screen_w = 600
    screen_h = 300
    fps = 60

    game = Game()
    game.run()
