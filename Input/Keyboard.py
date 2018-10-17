"""
To add new key, add an entry to self.keys and pykey_to_key
No idea how any of this code works.
"""
import pygame

class Keyboard:

    DOWN = 1
    UP = 2
    CLICK = 3
    CLEAR = 4

    def __init__(self):
        # A dictionary to keep track of the state of each key
        self.keys = {
            "A":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "B":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "C":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "D":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "E":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "F":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "G":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "H":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "I":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "J":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "K":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "L":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "M":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "N":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "O":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "P":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "Q":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "R":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "S":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "T":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "U":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "V":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "W":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "X":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "Y":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "Z":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "UP_ARROW":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "DOWN_ARROW":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "RIGHT_ARROW":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "LEFT_ARROW":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "BACKSPACE":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "TAB":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}},
            "CAPS_LOCK":{"state": Keyboard.CLEAR, "events": {"down":[], "up":[], "click":[], "clear":[]}}

        }

        self.pressed_keys = []
        self.click_any = []
        # False = treat input as lower
        self.caps_lock = False
        self.on("click", "CAPS_LOCK", lambda: self.toggle_caps_lock())
    def toggle_caps_lock(self):
        self.caps_lock = not self.caps_lock
    # Called every tick by kernel update
    def handle(self, event):
        key = self.pykey_to_key(event.key)
        if key == -1:
            print "Unknown Key %s" % event.key
            return
        if event.type == pygame.KEYDOWN:
            if self.keys[key]["state"] == Keyboard.CLEAR:
                self.keys[key]["state"] = Keyboard.DOWN
                self.pressed_keys.insert(0, key)
                self.exec_list(self.keys[key]["events"]["down"])
        if event.type == pygame.KEYUP:
            if self.keys[key]["state"] == Keyboard.DOWN:
                self.keys[key]["state"] = Keyboard.CLEAR
                self.pressed_keys.remove(key)
                self.exec_list(self.keys[key]["events"]["up"])

        for key in self.pressed_keys:
            self.exec_list(self.keys[key]["events"]["click"])
            for e in self.click_any:
                e(key)

    '''
    key = A string or list of strings representing keys.
    func= A pointer to a function to be executed
    multiple= If set to true, treats every single character in string as a separate letter.
    '''
    def on(self, event, key, func, multiple=False):

        # check if event type exists
        if event not in ["up", "down", "click", "clear"]:
            return False

        if isinstance(key, str):
            key = key.upper()
            if multiple:
                for k in key:
                    self.keys[k]["events"][event].insert(0, func)
            else:
                self.keys[key]["events"][event].insert(0, func)
        if isinstance(key, list):
            for k in key:
                k = k.upper()
                self.keys[k]["events"][event].insert(0, func)

    def on_click_any(self, e):
        self.click_any.append(e)

    def pykey_to_key(self, pykey):

        keys = "abcdefghijklmnopqrstuvwxyz"
        if 97 <= pykey <= 122:
            return keys[pykey - 97].upper()

        if pykey == pygame.K_UP:
            return "UP_ARROW"
        if pykey == pygame.K_LEFT:
            return "LEFT_ARROW"
        if pykey == pygame.K_RIGHT:
            return "RIGHT_ARROW"
        if pykey == pygame.K_DOWN:
            return "DOWN_ARROW"
        if pykey == 8:
            return "BACKSPACE"
        if pykey == 9:
            return "TAB "
        if pykey == 301:
            return "CAPS_LOCK"
        return -1

    def exec_list(self, func_list):
        for func in func_list:
            func()
