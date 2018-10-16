__author__ = 'User'

from Input.Keyboard import Keyboard
from Input.Mouse import Mouse

class GameObject:

    INIT = 0
    LOADING = 1
    READY = 2

    def __init__(self, **kwargs):
        def_args = {
            "height":480,
            "width":720,
            "name":"My game"
        }
        for (key, val) in def_args.iteritems():
            setattr(self, key, kwargs.get(key, val))

        self.status = GameObject.INIT

        self.scenes = {}
        self.current_scene = None

        self.keyboard = None
        self.mouse = None

        self.clock = None
        self.frame = -1

        self.screen = None
        self.background = None
        self.camera = None

        self.default_font = None

        self.resources = None

    def init(self):
        self.keyboard = Keyboard()
        self.mouse = Mouse()

    def get_scene(self):
        if self.current_scene in self.scenes:
            return self.scenes[self.current_scene]
        else:
            return None

    def set_scene(self, scene):
        if scene in self.scenes:
            self.current_scene = scene
            return True
        else:
            return False




