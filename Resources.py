__author__ = 'User'

import pygame
import json
from Graphics.Scene import Scene
class ResourceManager:

    IMAGE = "img"
    FONT = "fnt"
    SOUND = "snd"

    def __init__(self):
        self.__fonts = {}
        self.__images = {}
        self.__sounds = {}

    def load(self, r_name, path, r_type):
        if r_type == ResourceManager.IMAGE:
            if r_name in self.__images:
                print "Resource name taken."
            else:
                self.__images[r_name] = pygame.image.load(path)

        elif r_type == ResourceManager.FONT:
            if r_name in self.__fonts:
                print "Resource name taken."
            else:
                self.__fonts[r_name] = pygame.image.load(path)

        elif r_type == ResourceManager.SOUND:
            if r_name in self.__sounds:
                print "Resource name taken."
            else:
                self.__sounds[r_name] = pygame.image.load(path)
        
        else:
            print "Unknown resource type: %s" % r_type

    def load_image(self, r_name, path):
        return self.load(r_name, path, ResourceManager.IMAGE)

    def load_font(self, r_name, path):
        return self.load(r_name, path, ResourceManager.FONT)

    def load_sound(self, r_name, path):
        return self.load(r_name, path, ResourceManager.SOUND)

    def load_scene(self, game, scene_name):
        scene_data = None
        with open("Scenes/%s.json"%scene_name) as raw_scene_data:
            scene_data = json.load(raw_scene_data)
        scene_obj = Scene(game)
        scene_obj.init_from_dict(scene_data)
        game.scenes[scene_obj.name] = scene_obj
        print "Finished loading %s.json" % scene_name

    def get(self, r_name, r_type):
        if r_name in self.__images and r_type == ResourceManager.IMAGE:
            return self.__images[r_name]

        if r_name in self.__fonts and r_type == ResourceManager.FONT:
            return self.__fonts[r_name]

        if r_name in self.__sounds and r_type == ResourceManager.SOUND:
            return self.__sounds[r_name]

        return None

    def get_image(self, r_name):
        return self.get(r_name, ResourceManager.IMAGE)

    def get_font(self, r_name):
        return self.get(r_name, ResourceManager.FONT)

    def get_sound(self, r_name):
        return self.get(r_name, ResourceManager.SOUND)

