__author__ = 'User'

from Actor import Actor
from GUI import GuiManager, GuiActor, GUI_Actors
class Scene:
    def __init__(self, game):
        self.game = game
        self.name = None
        self.components = []
        self.gui = GuiManager(game)
        self.gui.father = self
        self.components = []

        self.game.mouse.onClick(0, self.gui.handle_mouse_click)

    def draw(self):
        for component in self.components:
            component.draw()

    # Adds a component to the scene.
    def add(self, component, name=None):
        if name is not None:
            component.name = name
        if isinstance(component, GuiActor):
            self.gui.add(component)
        for i in range(len(self.components)):
            if self.components[i].priority < component.priority:
                self.components.insert(i-1, component)
                break
        self.components.insert(0, component)

    # Initiates scene from a given dictionary.
    def init_from_dict(self, dict):
        self.name = dict["name"]
        for guiActor in dict["gui"]:
            gui_type = guiActor["type"]
            if gui_type in GUI_Actors:
                actor = GUI_Actors[gui_type](self.game, **guiActor)
                self.add(actor)
        for component in dict["components"]:
            pass

    # Returns component with the name "name"
    def get_component(self, name):
        for c in self.components:
            if c.name == name:
                return c
        return None

class TestScene(Scene):
    def __init__(self, game):
        Scene.__init__(self, game)
        self.name = "testScene"
        test_act = Actor(game, height=32, width=32)
        self.components.append(test_act)
