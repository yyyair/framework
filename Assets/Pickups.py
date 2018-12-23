__author__ = 'User'

from Graphics.Actor import Actor
from Collision import CollisionActor
from Game import Event
import random
class Pickup(CollisionActor):
    def __init__(self, game):
        CollisionActor.__init__(self, game)

        self.height = 32
        self.width = 32
        self.generator = None

        self.collision_box.width = 32
        self.collision_box.height = 32
        self.collision_box.name = "cb_pickup"
        self.name = "pickup"

        self.material = self.game.resources.get_image("defaultTexture")
        self.crop = (0, 0, 32, 32)

        self.can_pickup = []

    def on_scene(self, s):
        e = Event(self.collision_box.name, self.on_collision)
        self.game.events.add(e)

    def on_collision(self, e):
        if e.parent.name in self.can_pickup and self.name != "dead":
            if self.on_pickup(e.parent):
                return

    # Returns true and kills the pickup if it was picked up
    def on_pickup(self, picker):
        self.kill()
        return True

    def kill(self):
        if self.generator is not None:
            self.game.events.invoke(self.generator.name+"_died", self)
        CollisionActor.kill(self)

class PickupGenerator(CollisionActor):
    def __init__(self, game):
        CollisionActor.__init__(self, game)
        self.name = "pickup_generator"
        self.pickup_class = Pickup

        self.generate_range = 100
        self.last_generate_frame = -300
        self.generate_cooldown = 150

        self.max_generations = float("inf")
        self.max_at_once = 2
        self.current_alive = 0

    def on_scene(self, s):
        e = Event(self.name+"_died", self.pickup_died)
        self.game.events.add(e)

    def pickup_died(self, e):
        self.current_alive -= 1

    def update(self):
        if self.game.frame > self.generate_cooldown + self.last_generate_frame and self.max_at_once > self.current_alive:
            self.last_generate_frame = self.game.frame
            pkup = self.pickup_class(self.game)
            pkup.generator = self
            x = self.x + random.randint(0, self.generate_range)
            y = self.y + random.randint(0, self.generate_range)
            pkup.set_position(x, y)
            if not isinstance(pkup, Pickup):
                print "Tried to generate bad pickup"
            print "Generated %s" % pkup.name
            self.current_alive += 1
            self.game.get_scene().add(pkup)

class HealthPack(Pickup):
    def __init__(self, game):
        Pickup.__init__(self, game)

        self.collision_box.name = "cb_hp_pack"
        self.name = "hp_pack"
        self.material = self.game.resources.get_image("items")

        self.crop = (0, 0, 32, 32)

        self.hp_amount = 50
        self.mana_amount = 50

        self.can_pickup = ["player"]

    def on_pickup(self, picker):
        print "%s tries to pikcup %s" % (picker.name, self.name)
        picker.hp = min(picker.max_hp, picker.hp + self.hp_amount)
        picker.mana = min(picker.max_mana, picker.mana + self.mana_amount)

        self.kill()
        return True

class HealthPackGenerator(PickupGenerator):
    def __init__(self, game):
        PickupGenerator.__init__(self, game)
        self.pickup_class = HealthPack

# Fork bomb

class ForkBomb(Pickup):
    def __init__(self, game):
        Pickup.__init__(self, game)
        self.collision_box.name = "cb_fork_bomb"
        self.name = "fork_bomb"
        self.can_pickup = ["player"]

    def on_pickup(self, picker):
        fork1 = ForkBomb(self.game)
        fork2 = ForkBomb(self.game)
        self.game.get_scene().add(fork1)
        self.game.get_scene().add(fork2)

        self.kill()
        return True