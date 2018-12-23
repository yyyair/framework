__author__ = 'User'

from Graphics.Actor import Actor
from Collision import CollisionActor

class HealthPack(CollisionActor):
    def __init__(self, game):
        CollisionActor.__init__(self, game)

        self.height = 32
        self.width = 32

        self.animated = True

        self.collision_box.width = 32
        self.collision_box.height = 32
        self.collision_box.name = "cb_hp_pack"
        self.name = "hp_pack"

        self.material = self.game.resources.get_image("items")
        self.crop = (0, 0, 32, 32)

        self.hp_amount = 50
        self.mana_amount = 50

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.collision_box.x = x
        self.collision_box.y = y


