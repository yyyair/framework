__author__ = 'User'

from Graphics.Actor import Actor

class Tree(Actor):
    def __init__(self, game):
        Actor.__init__(self, game)
        self.material = self.game.resources.get_image("trees")
        self.height = 256
        self.width = 128

        self.texture_height = 96
        self.texture_width = 48

        self.crop = (0, 0, 64, 128)
