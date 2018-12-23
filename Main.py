"""
This is the file where you write your own game logic.
"""

from Assets.Player import Player
from Assets.TileEngine import TileEngine
from Game import Event
from Assets.Collision import CollisionManager, CollisionBox
from Assets.Structures import Tree
from Assets.Pickups import HealthPack, HealthPackGenerator, ForkBomb
from Graphics.Utility import FPSCounter
# Initialize your game. This method is called before the first frame, after loading resources.
def init(game):

    setup_world(game)

    btn = game.get_scene("main_menu").get_component("btn1")
    print [c.name for c in game.get_scene("main_menu").components]
    btn.click = lambda: game.set_scene("world")



    e = Event("test", lambda e: e)
    game.events.add(e)


    game.set_scene("main_menu")
    game.keyboard.on_click_any(lambda x: debug(x))

def setup_world(game):
    world = game.get_scene("world")

    collision = CollisionManager(game)
    world.add(collision)

    c = CollisionBox(collision)
    c.height = 32
    c.width = 32
    c.x = 128
    c.y = 128
    c.parent = collision
    collision.add(c, wall=True)

    player = Player(game)
    player.material = game.resources.get_image("player")

    tree = Tree(game)
    world.add(tree)

    hp_pack = ForkBomb(game)
    hp_pack.set_position(128, 256)
    world.add(hp_pack)

    hp_pack_gen = HealthPackGenerator(game)
    hp_pack_gen.set_position(128, 312)
    world.add(hp_pack_gen)

    world.add(player)

    te = TileEngine(game)
    world.add(te)

    label = FPSCounter(game)
    world.add(label)


# Why doesn't lambda: print work?
def debug(x):
    print x

# Load your resources!
def load(game):
    game.resources.load_image("player", "Textures/player.png")
    game.resources.load_image("trees", "Textures/trees.png")
    game.resources.load_image("items", "Textures/items.png")
    game.resources.load_image("fireball", "Textures/fireball.png")
    game.resources.load_scene(game, "main_menu")
    game.resources.load_scene(game, "world")
    pass

# Called every frame.
def update(game):
    pass

if __name__ == "__main__":
    print "Wrong file! Run Kernel.py"

