__author__ = 'User'

from Graphics.Actor import Actor
from Graphics.Animation import Frame, Animation
from Collision import CollisionBox
from Game import Event
class Player(Actor):
    def __init__(self, game):
        Actor.__init__(self, game)

        self.height = 64
        self.width = 64

        self.x_velocity = 1.0
        self.y_velocity = 1.0

        self.animated = True

        self.collision_box = CollisionBox(None)
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

        self.bind_movement_keys()

        self.ghost = False

    def move(self, dir, n=0.1):
        dt = 1 * n * self.game.clock.get_time()
        dx = self.x_velocity * dt * dir[0]
        dy = self.y_velocity * dt * dir[1]
        self.collision_box.x += dx
        self.collision_box.y += dy
        if not self.ghost and self.collision_box.parent.in_wall(self.collision_box):
            self.collision_box.x -= dx
            self.collision_box.y -= dy
            return

        self.x += dx
        self.y += dy

    def move_up(self):

        phase = "1" if self.game.frame % 20 > 9 else "2"
        self.animation.go_to("up_"+phase)
        self.move((0, -1))

    def move_down(self):
        phase = "1" if self.game.frame % 20 > 9 else "2"
        self.animation.go_to("down_"+phase)
        self.move((0, 1))

    def move_left(self):
        phase = "1" if self.game.frame % 20 > 9 else "2"
        self.animation.go_to("left_"+phase)
        self.move((-1, 0))

    def move_right(self):
        phase = "1" if self.game.frame % 20 > 9 else "2"
        self.animation.go_to("right_"+phase)
        self.move((1, 0))

    def bind_movement_keys(self):
        self.game.keyboard.on("click", "W", self.move_up)
        self.game.keyboard.on("click", "S", self.move_down)
        self.game.keyboard.on("click", "A", self.move_left)
        self.game.keyboard.on("click", "D", self.move_right)

    def on_collision(self, e):
        pass



