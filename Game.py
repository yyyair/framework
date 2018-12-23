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
        self.events = EventManager()

        self.default_font = None

        self.resources = None

    def init(self):
        self.keyboard = Keyboard()
        self.mouse = Mouse()

    def get_scene(self, name=None):
        if name is not None and name in self.scenes:
            return self.scenes[name]
        elif self.current_scene in self.scenes:
            return self.scenes[self.current_scene]
        else:
            return None

    def set_scene(self, scene):
        if scene in self.scenes:
            self.events.invoke("set_scene", {"old": self.current_scene, "new": scene})
            self.current_scene = scene
            return True
        else:
            return False


class Event:
    def __init__(self, name, func):
        self.name = name
        self.func = self.default

        if func is not None:
            self.func = func


    def execute(self, data):
        self.func(data)

    def default(self, e):
        print("Executed event %s" % self.name)

class EventManager:
    def __init__(self):
        self.events = {}
        self.debug = True

    def add(self, event):
        if self.debug:
            print "Added %s" % event.name
        if event.name in self.events:
            self.events[event.name].append(event)
        else:
            self.events[event.name] = [event]

    def invoke(self, event_name, event_data):
        if event_name not in self.events:
            print "Tried invoking %s but no such event!" % event_name
            print self.events
            return
        if self.debug:
            print "Invoked %s with %s" % (event_name, self.events[event_name][0].func)
        if event_name  in self.events:
            for e in self.events[event_name]:
                e.execute(event_data)

    def remove(self, name):
        if name in self.events:
            del self.events[name]

