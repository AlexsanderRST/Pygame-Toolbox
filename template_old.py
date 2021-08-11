"""Alexsander Rosante's creation"""

import pygame
from pygame.locals import *

pygame.init()


class Game:
    def __init__(self):
        self.display_w, self.display_h = 1024, 600
        display_flags = 0
        self.display = pygame.display.set_mode((self.display_w, self.display_h), display_flags)
        self.clock, self.fps = pygame.time.Clock(), 60
        self.events = pygame.event.get()
        self.loop = True

        #

        #

    def run(self):
        #

        #

        while self.loop:
            self.event_check()

            #

            #

            pygame.display.update()
            self.clock.tick(self.fps)
        pygame.quit()

    def event_check(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == QUIT:
                self.loop = False

            #

            #


if __name__ == '__main__':
    game = Game()
    game.run()
