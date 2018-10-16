__author__ = 'User'

class Frame:
    def __init__(self, _x, _y, _height,_width, name=None):
        self.x = _x
        self.y = _y
        self.height = _height
        self.width = _width
        self.name = name
        self.time = 1

    def crop_tuple(self):
        return self.x, self.y, self.height, self.width

class Animation:
    def __init__(self, frames=[]):
        self.frames = frames
        self.current = None
        self.current_index = -1

    def jump(self, n):
        self.current_index = (self.current_index + n) % len(self.frames)
        self.current = self.frames[self.current_index]

    def next_frame(self):
        self.jump(1)

    def previous_frame(self):
        self.jump(-1)

    def go_to(self, name):
        for i in range(len(self.frames)):
            if self.frames[i].name == name:
                self.current_index = i
                self.current = self.frames[self.current_index]
                return self.current
        return False

    def start(self):
        self.jump(1)


