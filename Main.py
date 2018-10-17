__author__ = 'Yair'

from Graphics.Scene import TestScene, Scene
from Graphics.GUI import Textbox, Label, Button
from Assets.TileEngine import TileEngine
from Assets.Player import  Player
def init(game):
    game.set_scene("main_menu")
    game.keyboard.on_click_any(lambda x: debug(x))

def debug(x):
    print x

def load(game):
    game.resources.load_image("player", "Textures/player.png")
    game.resources.load_scene(game, "main_menu")
    pass

def update(game):
    pass

if __name__ == "__main__":
    print "You need to run Kernel.py in order to run the game."

