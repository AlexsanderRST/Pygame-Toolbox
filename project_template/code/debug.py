"""
2022 Alexsander Rosante's creation
https://github.com/AlexsanderRST
"""

import pygame

pygame.init()


def debug(info, y=0, x=0):
    info_surf = pygame.font.Font(None, 32).render(str(info), True, 'white', 'black')  # won't work when exe
    pygame.display.get_surface().blit(info_surf, (x, y))
