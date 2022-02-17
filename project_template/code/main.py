"""
2022 Alexsander Rosante's creation
https://github.com/AlexsanderRST
"""

from pygame.locals import *
from scene import Scene
from settings import *

import pygame


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        pygame.display.set_caption(f'{game_name} ({game_version})')
        self.clock = pygame.time.Clock()
        self.events = pygame.event.get()
        self.loop = True
        self.scene = Scene()

    def check_events(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == QUIT:
                self.loop = False

    def run(self):
        while self.loop:
            self.check_events()
            self.scene.update(self.events)
            self.scene.draw(self.screen)
            pygame.display.update()
            self.clock.tick(fps)
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
