"""Alexsander Rosante's creation"""

import pygame
from pygame.locals import *

pygame.init()


class Game:
    def __init__(self):
        self.display = pygame.display.set_mode((display_w, display_h))
        self.clock, self.fps = pygame.time.Clock(), 60
        self.events = pygame.event.get()
        self.loop = True

    def check_events(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == QUIT:
                self.loop = False

    def run(self):
        while self.loop:
            self.check_events()
            self.display.fill('black')
            pygame.display.update()
            self.clock.tick(self.fps)
        pygame.quit()


if __name__ == '__main__':
    display_w, display_h = 1152, 648
    game = Game()
    game.run()
