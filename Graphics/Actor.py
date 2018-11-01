__author__ = 'User'
import pygame
from pygame import transform
from GameComponent import Component

class Actor(Component):
    def __init__(self, game, **kwargs):
        Component.__init__(self, game)
        def_args  = {
            "name":None,
            "height":32,
            "width":32,
            "texture_height":32,
            "texture_width":32,
            "material": game.resources.get_image("defaultTexture"),
            "absolute":False,
            "crop":(0, 0, 32, 32),
            "animated":False,
            "animation":None,
            "x":0,
            "y":0
        }
        for (key, val) in def_args.iteritems():
            setattr(self, key, kwargs.get(key, val))

    def draw(self):
        tmp = pygame.Surface((self.texture_width, self.texture_height), pygame.SRCALPHA)
        '''
        hitbox = pygame.Surface((self.CollisionBox.Width, self.CollisionBox.Height))
        hitbox.set_alpha(64)
        hitbox.fill((0, 0, 255))
        '''

        #tmp.fill((0,0,255))

        crop = self.crop
        if self.animated:
            if self.animation is not None and self.animation.current is not None:
                crop = self.animation.current.crop_tuple()

        tmp.blit(self.material, (0,0), area=crop)

        tmp = transform.scale(tmp, (self.width, self.height))
        # tmp.blit(hitbox, (self.CollisionBox.X, self.CollisionBox.Y))

        c_x = self.x
        c_y = self.y
        if not self.absolute:
            c_x = self.x - self.game.camera.X
            c_y = self.y - self.game.camera.Y

        self.game.screen.blit(tmp, (c_x, c_y))


