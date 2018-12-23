__author__ = 'User'

import pygame
from Collision import CollisionActor
from Graphics.Utility import Direction

class Projectile(CollisionActor):
    def __init__(self, game):
        CollisionActor.__init__(self, game)
        self.name = "projectile"
        self.material = game.resources.get_image("fireball")

        self.collision_box.height = 16
        self.collision_box.width = 16

        self.height = 16
        self.width = 16

        self.original_x = None
        self.original_y = None

        self.direction = Direction.LEFT
        self.max_distance = 500
        self.speed = 2
        self.damage = 100

    def move(self, dir, n=0.1):
        dt = 1 * n * self.game.clock.get_time()
        dx = self.speed * dt * dir[0]
        dy = self.speed * dt * dir[1]
        self.collision_box.x += dx
        self.collision_box.y += dy
        if not self.ghost and self.collision_box.manager.in_wall(self.collision_box):
            self.collision_box.x -= dx
            self.collision_box.y -= dy
            return

        self.x += dx
        self.y += dy

    def move_up(self):
        self.move((0, -1))

    def move_down(self):
        self.move((0, 1))

    def move_left(self):
        self.move((-1, 0))

    def move_right(self):
        self.move((1, 0))

    def update(self):
        print self.x, self.y
        if self.original_x is None or self.original_y is None:
            self.original_x = self.x
            self.original_y = self.y
        if (self.original_x-self.x)**2 + (self.original_y-self.y)**2 > self.max_distance**2:
            self.kill()
            return
        if self.direction == Direction.DOWN:
            self.move_down()
        elif self.direction == Direction.UP:
            self.move_up()
        elif self.direction == Direction.RIGHT:
            self.move_right()
        elif self.direction == Direction.LEFT:
            self.move_left()

class Fireball(Projectile):
    def __init__(self, game):
        Projectile.__init__(self, game)
        self.name = "projectile_fireball"
        self.material = game.resources.get_image("fireball")
        self.crop = (0, 0, 32, 32)
        self.direction = Direction.LEFT
        self.max_distance = 300
        self.speed = 2
        self.damage = 100

