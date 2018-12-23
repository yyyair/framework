__author__ = 'User'

import pygame
from Graphics.GUI import Label
def make_bar_surface(height, width, empty_color=(255,255,255), full_color=(0,255,0), ratio=1, border=True):
    bar = pygame.Surface((width, height), pygame.SRCALPHA)
    bar.fill((0,0,0))
    if border:
        bar.fill(empty_color, rect=(1 ,1, width-2, height-2))
        bar.fill(full_color, rect=(1 ,1, width*ratio-2, height-2))
    else:
        bar.fill(empty_color, rect=(0,0, width, height))
        bar.fill(full_color, rect=(0,0, width*ratio, height))
    return bar

class Direction:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class FPSCounter(Label):
    def __init__(self, game):
        Label.__init__(self, game)

    def update(self):
        self.text = str(int(self.game.clock.get_fps()))