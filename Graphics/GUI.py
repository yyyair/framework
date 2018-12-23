__author__ = 'User'

import pygame
from pygame import transform
from Actor import Actor

class GuiManager:
    def __init__(self, game):
        self.game = game
        self.items = []
        self.focus = None
        self.father = None


    def add(self, item):
        if self.father is None:
            return -1
        self.items.append(item)
        n = "guiActor-%s" % len(self.items)
        if item.name is None:
            item.name = n
        else:
            item.name = str(item.name)
        #self.father.add(item, n)
        #self.game.mouse.onClick(0, self.handle_mouse_click)

    def get(self, name):
        for i in self.items:
            if i.Name == name:
                return i
        return None


    def draw(self):
        for item in self.items:
            item.draw()

    def handle_mouse_click(self):
        if self.game.current_scene != self.father.name:
            return
        x, y = self.game.mouse.X, self.game.mouse.Y
        clicked_any = False
        for guiActor in self.items:
            if guiActor.x < x < guiActor.x + guiActor.width and guiActor.y < y < guiActor.y + guiActor.height:
                print "Clicked %s " % guiActor
                clicked_any = True
                if self.focus != guiActor:
                    if self.focus is not None: self.focus.on_unfocus()
                    self.focus = guiActor
                    guiActor.on_focus()
                guiActor.click()
        if not clicked_any:
            if self.focus is not None: self.focus.on_unfocus()
            self.focus = None


class GuiActor(Actor):
    def __init__(self, game, **kwargs):
        Actor.__init__(self, game, **kwargs)
        '''self.height = h
        self.width = w
        self.x = _x
        self.y = _y'''
        self.Disabled = False
        self.Absolute = True
        self.focused = False
        self.Collision = False
        self.priority = -1

    def draw(self):
        tmp = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        tmp.fill((0,0,0))

        self.game.screen.blit(tmp, (self.x, self.y))

    def on_focus(self):
        print "%s is focused" % self
        self.focused = True

    def on_unfocus(self):
        print "%s is focused" % self
        self.focused = False

    def click(self):
        print "Clicked %s" % self


class Button(GuiActor):
    def __init__(self, game, **kwargs):
        GuiActor.__init__(self, game, **kwargs)
        def_args = {
            "text": ""
        }
        for (key, val) in def_args.iteritems():
            setattr(self, key, kwargs.get(key, val))

    def draw(self):
        tmp = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        tmp.fill((0,0,0))
        tmp.fill((255,255,255), rect=(1,1,self.width-2,self.height-2))
        text = self.game.default_font.render(self.text, 1, (0,0,0))
        tmp.blit(text, (self.width / 2 - text.get_width()/2, self.height / 2 - text.get_height()/2))

        self.game.screen.blit(tmp, (self.x, self.y))



class Textbox(GuiActor):
    def __init__(self, game, **kwargs):
        GuiActor.__init__(self, game, **kwargs)

        def_args = {
            "text": ""
        }
        for (key, val) in def_args.iteritems():
            setattr(self, key, kwargs.get(key, val))
        print self.text
        self.pointer = lambda: "|" if self.focused and self.game.frame % 100 > 50 else ""
        self.last_input_frame = game.frame
        self.delta_input_frame = 5

        game.keyboard.on_click_any(lambda e: self.do_input(e))
        game.keyboard.on("click", "BACKSPACE", lambda: self.do_input("BACKSPACE"))

    def do_input(self, e):
        # TODO: Implement more characters
        if self.focused and self.game.frame > self.last_input_frame + self.delta_input_frame:
            self.last_input_frame = self.game.frame
            if e == "BACKSPACE":
                self.text = self.text[0:-1]
            elif e == "SPACE":
                self.text += " "
            elif e in "ABCDEFGHIJKLMNOPQRSTVUWXYZ":
                self.text += e if self.game.keyboard.caps_lock else e.lower()

    def draw(self):
        tmp = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        tmp.fill((0,0,0))
        tmp.fill((255,255,255), rect=(1,1,self.width-2,self.height-2))
        text = self.game.default_font.render(self.text + self.pointer(), 1, (0,0,0))
        tmp.blit(text, (0, self.height / 2 - text.get_height()/2))

        self.game.screen.blit(tmp, (self.x, self.y))
    def on_focus(self):
        GuiActor.on_focus(self)

    def on_unfocus(self):
        GuiActor.on_unfocus(self)

class Label(GuiActor):
    def __init__(self, game, **kwargs):
        GuiActor.__init__(self, game, **kwargs)
        def_args = {
            "text": ""
        }
        for (key, val) in def_args.iteritems():
            setattr(self, key, kwargs.get(key, val))

    def draw(self):
        tmp = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        text = self.game.default_font.render(self.text, 1, (0,0,0))
        tmp.blit(text, (self.width / 2 - text.get_width()/2, self.height / 2 - text.get_height()/2))

        self.game.screen.blit(tmp, (self.x, self.y))

class Checkbox(GuiActor):
    def __init__(self, game, **kwargs):
        GuiActor.__init__(self, game, **kwargs)
        def_args = {
            "value": True
        }
        for (key, val) in def_args.iteritems():
            setattr(self, key, kwargs.get(key, val))

        self.click = self.toggle_value

    def toggle_value(self):
        self.value = not self.value

    def draw(self):
        tmp = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        tmp.fill((0,0,0))
        tmp.fill((255,255,255), rect=(1,1,self.width-2,self.height-2))
        if self.value:
            tmp.fill((0, 255, 0), rect=(self.width/2 - self.width / 4, self.height/2 - self.height / 4,self.width/2,self.height/2))

        self.game.screen.blit(tmp, (self.x, self.y))

GUI_Actors = {
    "Textbox":Textbox,
    "Label":Label,
    "Button":Button,
    "Checkbox":Checkbox
}