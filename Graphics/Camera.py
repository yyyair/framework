__author__ = 'User'

class Camera:
    def __init__(self):
        self.X = 0
        self.Y = 0
        self.Zoom = 1.0

        self.X_Velocity = 0.2
        self.Y_Velocity = 0.2

        self.Angle = 0
        self.Angular_Velocity = 0
        self.Lock = False

    def left(self, amount = None):
        if not self.Lock:
            self.X -= self.X_Velocity if amount is None else amount

    def right(self, amount = None):
        if not self.Lock:
            self.X += self.X_Velocity if amount is None else amount

    def down(self, amount = None):
        if not self.Lock:
            self.Y += self.Y_Velocity if amount is None else amount

    def up(self, amount = None):
        if not self.Lock:
            self.Y -= self.Y_Velocity if amount is None else amount