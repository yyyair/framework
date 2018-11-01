__author__ = 'User'

from Graphics.GameComponent import Component
import pygame
class CollisionBox:
    def __init__(self, parent):
        self.x = 0
        self.y = 0
        self.height = 0
        self.width = 0
        self.parent = parent

        self.grid_cords = None
        self.name = "cb_any"

    def vertices(self):
        return [(self.x, self.y), (self.x + self.width, self.y + self.height),
                  (self.x + self.width, self.y), (self.x, self.y + self.height)]

    def contains(self, p):
        x = p[0]
        y = p[1]

        return self.x < x < self.x + self.width and self.y < y < self.y + self.height

    def collides(self, box):
        for p in box.vertices():
            if self.contains(p):
                return True
        for p in self.vertices():
            if box.contains(p):
                return True
        return False

    def calculate_grid_cords(self, slice_size):
        grid_x = int(self.x / slice_size)
        grid_y = int(self.y / slice_size)

        return grid_x, grid_y

    def draw(self, game):
        hitbox = pygame.Surface((self.width, self.height))
        hitbox.set_alpha(64)
        hitbox.fill((0, 0, 255))

        c_x = self.x - game.camera.X
        c_y = self.y - game.camera.Y

        game.screen.blit(hitbox, (c_x, c_y))


class CollisionManager(Component):
    def __init__(self, game):
        Component.__init__(self, game, name="Asset_Collision")
        self.game = game
        self.objects = []
        self.map_size = 640
        self.slice_size = 128

        self.grid_size = self.map_size/self.slice_size

        self.grid = [[[]] * self.grid_size] * self.grid_size
        self.used_cells = []

        self.walls = []

        self.debug = True

    def get_collision_list(self):
        collision = []
        for cell in self.used_cells:
            current_objects = self.grid[cell[0]][cell[1]]
            for i in range(len(current_objects)):
                object1 = current_objects[i]
                for j in range(i, len(current_objects)):
                    object2 = current_objects[j]
                    if object1.collides(object2):
                        collision.append((object1, object2))
        return collision

    def update(self):
        for obj in self.objects:
            org_cords = obj.grid_cords
            new_cords = obj.calculate_grid_cords(self.slice_size)
            #print org_cords, new_cords, obj
            if new_cords != org_cords:
                if org_cords is not None and obj in self.grid[org_cords[0]][org_cords[1]]:
                    self.grid[org_cords[0]][org_cords[1]].remove(obj)
                    if not len(self.grid[org_cords[0]][org_cords[1]]): self.used_cells.remove(org_cords)
                self.grid[new_cords[0]][new_cords[1]].append(obj)
                if new_cords not in self.used_cells:
                    self.used_cells.append(new_cords)
            obj.grid_cords = new_cords

        cols = self.get_collision_list()
        for col in cols:
            self.game.events.invoke(col[0].name, col[1])
            self.game.events.invoke(col[1].name, col[0])

    def add(self, obj, wall=False):
        self.objects.append(obj)
        if wall:
            self.walls.append(obj)

    def in_wall(self, obj):
        for wall in self.walls:
            if obj.collides(wall):
                return True
        return False

    def draw(self):
        if self.debug:
            for obj in self.objects:
                obj.draw(self.game)

