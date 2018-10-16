__author__ = 'User'

class Component:
    def __init__(self, game, name=None):
        self.game = game
        self.name = name
        self.priority = 0

    def draw(self):
        pass

    def update(self):
        pass

    def load(self):
        pass
