"""Alexsander Rosante's creation"""

import pygame
from pygame.locals import *
from settings import *
import scene

pygame.init()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        pygame.display.set_caption(f"{game_name} ({game_version}) - {game_creator}'s creation")
        self.clock, self.fps = pygame.time.Clock(), 60
        self.events = pygame.event.get()
        self.loop = True

        #
        self.scene = scene.Basic()
        #

    def run(self):
        while self.loop:
            self.event_check()

            #
            self.scene.run(self.screen, self.events)
            #

            pygame.display.update()
            self.clock.tick(self.fps)
        pygame.quit()

    def event_check(self):
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == KEYDOWN and event.key == K_ESCAPE or event.type == QUIT:
                self.loop = False


if __name__ == '__main__':
    game = Game()
    game.run()
