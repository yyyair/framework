__author__ = 'User'

'''
Base class for any game object.
'''
class Component:
    def __init__(self, game,name="component"):
        self.game = game
        self.name = name
        self.owners = []
        self.priority = 0

    def draw(self):
        pass

    def update(self):
        pass

    def load(self):
        pass

    def kill(self):
        my_scene = self.game.get_scene()
        if my_scene.get_component(self.name) is not None:
            my_scene.remove_component(self.name)

    def on_scene(self, s):
        pass

class MovingComponent(Component):
    def __init__(self, game):
        Component.__init__(self, game)
        self.x = 0
        self.y = 0
        self.name = "moving_component"

    def set_position(self, x, y):
        self.x = x
        self.y = y