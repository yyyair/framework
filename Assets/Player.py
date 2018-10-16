__author__ = 'User'

from Graphics.Actor import Actor
from Graphics.Animation import Frame, Animation
class Player(Actor):
    def __init__(self, game):
        Actor.__init__(self, game)

        self.height = 64
        self.width = 64

        self.x_velocity = 1.0
        self.y_velocity = 1.0

        self.animated = True

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

    def move(self, dir, n=1):
        # TODO: Multiply dt by time since last tick
        dt = 1 * n
        self.x += self.x_velocity * dt * dir[0]
        self.y += self.y_velocity * dt * dir[1]

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


