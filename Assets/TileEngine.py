__author__ = 'User'

from Graphics.Actor import Actor
from Graphics.GameComponent import  Component
'''
Responsible for drawing tiles
'''

class Tile(Actor):
    def __init__(self, game, _id=0):
        Actor.__init__(self, game)
        self.id = _id

        self.height = 32
        self.width = 32
        self.texture_height = 32
        self.texture_width = 32

        self.crop = (32*self.id, 0, 32, 32)
        self.material = self.game.resources.get_image("tilemap")


class TileEngine(Component):
    def __init__(self, game):
        Component.__init__(self, game)
        self.tile_map = game.resources.load_image("tilemap", "Textures/tilemap.png")

        #test_tile = Tile(game)
        self.tiles = []

        self.priority = -10000

        for i in range(16):
            for j in range(16):
                tId = 3 if not (4 < i < 11) else (2 - i % 2 if i == 5 or i == 10 else 0)
                tile = Tile(game, _id=tId)
                tile.x = i * 32
                tile.y = j * 32
                self.tiles.append(tile)


    def draw(self):
        for tile in self.tiles:
            tile.draw()


