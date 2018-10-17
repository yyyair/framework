"""
This is the file where you write your own game logic.
"""

# Initialize your game. This method is called before the first frame, after loading resources.
def init(game):

    btn = game.get_scene("main_menu").get_component("btn1")
    print [c.name for c in game.get_scene("main_menu").components]
    btn.click = lambda: debug("x")

    game.set_scene("main_menu")
    game.keyboard.on_click_any(lambda x: debug(x))

# Why doesn't lambda: print work?
def debug(x):
    print x

# Load your resources!
def load(game):
    game.resources.load_image("player", "Textures/player.png")
    game.resources.load_scene(game, "main_menu")
    pass

# Called every frame.
def update(game):
    pass

if __name__ == "__main__":
    print "Wrong file! Run Kernel.py"

