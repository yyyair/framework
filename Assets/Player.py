__author__ = 'User'
import pygame
from Graphics.Actor import Actor
from Graphics.Animation import Frame, Animation
from Collision import CollisionBox, CollisionActor
from Graphics.Utility import make_bar_surface
from Game import Event
from Assets.Projectiles import Fireball
from Graphics.Utility import Direction
class Player(CollisionActor):
    def __init__(self, game):
        CollisionActor.__init__(self, game)

        self.height = 64
        self.width = 64
        self.name = "player"

        self.x_velocity = 1.0
        self.y_velocity = 1.0

        self.animated = True

        self.collision_box.width = 64
        self.collision_box.height = 64
        self.collision_box.name = "cb_player"

        e = Event("cb_player", self.on_collision)

        self.game.events.add(e)

        left_frame = Frame(32, 0, 32, 32, "left_1")
        right_frame = Frame(32, 64, 32, 32, "right_1")
        up_frame = Frame(0, 0, 32, 32, "up_1")
        down_frame = Frame(0, 64, 32, 32, "down_1")

        left_frame_2 = Frame(32, 32, 32, 32, "left_2")
        right_frame_2 = Frame(32, 96, 32, 32, "right_2")
        up_frame_2 = Frame(0, 32, 32, 32, "up_2")
        down_frame_2 = Frame(0, 96, 32, 32, "down_2")

        walking_animation = Animation(frames=[
            left_frame, right_frame, up_frame, down_frame, up_frame_2, down_frame_2, left_frame_2, right_frame_2])
        self.animation = walking_animation

        self.animation.start()
        self.direction = Direction.LEFT

        self.bind_movement_keys()

        self.ghost = False

        # HP / Mana
        self.max_hp = 1000
        self.hp = 700
        self.max_mana = 500
        self.mana = 300

        self.attack_cooldown = 100
        self.last_attack_frame = -150

        self.show_bars = True

    def move(self, dir, n=0.1):
        dt = 1 * n * self.game.clock.get_time()
        dx = self.x_velocity * dt * dir[0]
        dy = self.y_velocity * dt * dir[1]
        self.collision_box.x += dx
        self.collision_box.y += dy
        if not self.ghost and self.collision_box.manager.in_wall(self.collision_box):
            self.collision_box.x -= dx
            self.collision_box.y -= dy
            return

        self.x += dx
        self.y += dy

    def move_up(self):

        phase = "1" if self.game.frame % 20 > 9 else "2"
        self.animation.go_to("up_"+phase)
        self.direction = Direction.UP
        self.move((0, -1))

    def move_down(self):
        phase = "1" if self.game.frame % 20 > 9 else "2"
        self.animation.go_to("down_"+phase)
        self.direction = Direction.DOWN
        self.move((0, 1))

    def move_left(self):
        phase = "1" if self.game.frame % 20 > 9 else "2"
        self.animation.go_to("left_"+phase)
        self.direction = Direction.LEFT
        self.move((-1, 0))

    def move_right(self):
        phase = "1" if self.game.frame % 20 > 9 else "2"
        self.animation.go_to("right_"+phase)
        self.direction = Direction.RIGHT
        self.move((1, 0))

    def bind_movement_keys(self):
        self.game.keyboard.on("click", "W", self.move_up)
        self.game.keyboard.on("click", "S", self.move_down)
        self.game.keyboard.on("click", "A", self.move_left)
        self.game.keyboard.on("click", "D", self.move_right)
        self.game.keyboard.on("click", "SPACE", self.attack)

    def on_collision(self, e):
        print "Collided with %s" % e.parent.name

    def attack(self):
        if self.game.frame > self.last_attack_frame + self.attack_cooldown and self.mana > 100:
            attack_projectile = Fireball(self.game)
            attack_projectile.set_position(self.x + self.width/32, self.y+self.height/2)

            attack_projectile.direction = self.direction
            if self.direction == Direction.UP:
                attack_projectile.crop = (64, 0, 32, 32)
            elif self.direction == Direction.DOWN:
                attack_projectile.crop = (96, 0, 32, 32)
            elif self.direction == Direction.LEFT:
                attack_projectile.crop = (0, 0, 32, 32)
            elif self.direction == Direction.RIGHT:
                attack_projectile.crop = (32, 0, 32, 32)

            self.mana -= 100

            self.last_attack_frame = self.game.frame
            self.game.get_scene().add(attack_projectile)

    def draw(self):
        Actor.draw(self)
        bar_height = self.height / 10
        bar_width = self.width
        hp_bar = make_bar_surface(bar_height, bar_width, ratio=float(self.hp)/self.max_hp, full_color=(0,255,0), empty_color=(255,0,0))
        self.game.screen.blit(hp_bar, (self.x, self.y-12))

        mana_bar = make_bar_surface(bar_height, bar_width, ratio=float(self.mana)/self.max_mana, empty_color=(0,25,255), full_color=(100,255,255))
        self.game.screen.blit(mana_bar, (self.x, self.y-4))


