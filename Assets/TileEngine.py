__author__ = 'User'

from Graphics.Actor import Actor
from Graphics.GameComponent import  Component
'''
Responsible for drawing tiles
'''

class Tile(Actor):
    def __init__(self, game):
        Actor.__init__(self, game)
        self.id = 0

        self.height = 32
        self.width = 32
        self.texture_height = 32
        self.texture_width = 32


class TileEngine(Component):
    def __init__(self, game):
        Component.__init__(self, game)
        #self.tile_map = game.resources.load_image("tilemap")

        #test_tile = Tile(game)
        self.tiles = []

        for i in range(16):
            for j in range(16):
                tile = Tile(game)
                tile.x = i * 32
                tile.y = j * 32
                self.tiles.append(tile)


    def draw(self):
        for tile in self.tiles:
            tile.draw()


