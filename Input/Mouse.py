__author__ = 'User'
import pygame

class Mouse:

    UP = pygame.MOUSEBUTTONUP
    DOWN = pygame.MOUSEBUTTONDOWN
    CLICK = 7

    def __init__(self):
        self.X = 0
        self.Y = 0
        self._onclick = [[]] * 3
        self._ondown = [[]] * 3
        self._onup = [[]] * 3

        self.current = Mouse.UP

    def handle(self, event):
        location = pygame.mouse.get_pos()
        self.X = location[0]
        self.Y = location[1]

        if self.current == Mouse.DOWN and event.type == Mouse.UP:
            self.click(event.button-1)
        self.current = event.type
        '''
        states = pygame.mouse.get_pressed()
        if states[0]:
            self.click(0)
        if states[1]:
            self.click(1)
        if states[2]:
            self.click(2)'''

    def on_click(self, n, event):
        self._onclick[n].insert(0, event)

    def click(self, n):
        self.exec_list(self._onclick[n])

    def exec_list(self, func_list):
        for func in func_list:
            func()
