__author__ = 'User'

from Actor import Actor
from GUI import GuiManager, GuiActor, GUI_Actors
from Assets.Collision import CollisionActor, CollisionManager
class Scene:
    def __init__(self, game):
        self.game = game
        self.name = None
        self.gui = GuiManager(game)
        self.gui.father = self
        self.components = []
        self.taken_names = []
        self.collision_manager = None
        self.game.mouse.on_click(0, self.gui.handle_mouse_click)

    def draw(self):
        for component in self.components:
            component.draw()

    def update(self):
        for component in self.components:
            component.update()

    # Adds a component to the scene.
    def add(self, component):
        # Make sure component has good name
        i = 1
        if component.name is None:
            component.name = "unnamed_component"
        real_name = component.name
        while component.name in self.taken_names:
            component.name = real_name + str(i)
            i += 1

        # Check if the new component manages collisions
        if isinstance(component, CollisionManager):
            if self.collision_manager is None:
                self.collision_manager = component

        # Check if we should add component to gui manager
        if isinstance(component, GuiActor):
            self.gui.add(component)

        # Check if we should add component to collision manager
        if isinstance(component, CollisionActor):
            component.collision_box.manager = self.collision_manager
            self.collision_manager.add(component.collision_box)

        self.taken_names.append(component.name)
        for i in range(len(self.components)):
            if self.components[i].priority < component.priority:
                self.components.insert(i-1, component)
                component.on_scene(self)
                return
        self.components.insert(0, component)
        component.on_scene(self)
        print [c.priority for c in self.components]

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

    # Remove component and return how many were removed
    def remove_component(self, name):
        tmp = []
        for c in self.components:
            if c.name == name:
                print "Removing %s" % c.name
                tmp.append(c)
        for c in tmp:
            if c in self.components:
                self.components.remove(c)
        return len(tmp)

class TestScene(Scene):
    def __init__(self, game):
        Scene.__init__(self, game)
        self.name = "testScene"
        test_act = Actor(game, height=32, width=32)
        self.components.append(test_act)
