"""
Alexsander Rosante's creation
Settings like screen width and height; or fps are imported
"""

from pygame.locals import *

import pygame

pygame.init()


class Scene:
    def __init__(self):
        self.color_bg = 'black'

    def update(self, events: list):
        pass

    def draw(self, surface: pygame.Surface):
        surface.fill(self.color_bg)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        pygame.display.set_caption(f'My Program ({version})')
        self.clock = pygame.time.Clock()
        self.events = pygame.event.get()
        self.loop = True
        self.hovered = pygame.sprite.Group()
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
    version = '0.1'
    screen_w = 1152
    screen_h = 648
    fps = 60

    game = Game()
    game.run()
