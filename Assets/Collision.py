__author__ = 'User'

from Graphics.GameComponent import Component
from Graphics.Actor import Actor
import pygame
class CollisionBox:
    def __init__(self, parent):
        self.x = 0
        self.y = 0
        self.height = 0
        self.width = 0
        self.parent = parent
        self.manager = None

        self.grid_cords = None
        self.name = "cb_any"
        self.debug_box = True

    # Returns a list of all vertices, with (self.x, self.y) being top-left vertex as reference
    def vertices(self):
        return [(self.x, self.y), (self.x + self.width, self.y + self.height),
                  (self.x + self.width, self.y), (self.x, self.y + self.height)]

    # Returns true if p is contained in rectangle self
    def contains(self, p):
        x = p[0]
        y = p[1]

        return self.x < x < self.x + self.width and self.y < y < self.y + self.height

    # Returns true if two rectangles collide
    def collides(self, box):
        for p in box.vertices():
            if self.contains(p):
                return True
        for p in self.vertices():
            if box.contains(p):
                return True
        return False

    # Returns a tuple (x, y) representing the coordinates
    def calculate_grid_cords(self, slice_size):
        grid_x = int(self.x / slice_size)
        grid_y = int(self.y / slice_size)

        return grid_x, grid_y

    # Draw hitbox. Can be disabled by setting self.debug_box = False
    def draw(self, game):
        if not self.debug_box:
            return
        hitbox = pygame.Surface((self.width, self.height))
        hitbox.set_alpha(64)
        hitbox.fill((0, 0, 255))

        c_x = self.x - game.camera.X
        c_y = self.y - game.camera.Y

        game.screen.blit(hitbox, (c_x, c_y))

    # Center of rectangle
    def center(self):
        return self.x + self.width / 2, self.y + self.height / 2

class CollisionActor(Actor):
    def __init__(self, game):
        Actor.__init__(self, game)
        self.collision_box = CollisionBox(self)
        self.name = "collision_actor"
        self.ghost = False

    def set_position(self, x, y):
        Actor.set_position(self, x, y)
        self.collision_box.x = x
        self.collision_box.y = y

    def kill(self):
        self.name = "dead"
        my_scene = self.game.get_scene()
        if my_scene.get_component(self.name) is not None:
            my_scene.remove_component(self.name)
        collision_manager = my_scene.get_component("Asset_Collision")
        if collision_manager is not None:
            tmp = [c for c in collision_manager.objects if c.parent.name == self.name]
            print tmp
            for c in tmp:
                grid_cords = c.calculate_grid_cords(collision_manager.slice_size)
                collision_manager.objects.remove(c)
                if c in collision_manager.grid[grid_cords[0]][grid_cords[1]]:
                    collision_manager.grid[grid_cords[0]][grid_cords[1]].remove(c)

        self.game.events.remove(self.collision_box.name)
        self.collision_box.parent = None
        self.collision_box.manager = None
        self.game = None


# Detects and alerts collision between CollisionBox objects.
# We check collision by comparing each rectangle and checking if one of their vertices is inside another.
# To attempt increase efficiency, we create a grid and compare only objects that are in the same cell.
# TODO: Allow objects to occupy more than one cell
class CollisionManager(Component):
    def __init__(self, game):
        Component.__init__(self, game, name="Asset_Collision")
        self.name = "Asset_Collision"
        self.game = game
        self.objects = []
        self.map_size = 2048
        self.slice_size = 128

        self.grid_size = self.map_size/self.slice_size

        self.grid = [[[]] * self.grid_size] * self.grid_size
        self.used_cells = []

        self.walls = []

        self.debug = True

    # Returns a list of all collisions
    def get_collision_list(self):
        collision = []
        # Each object is compared only with his cell mates
        for cell in self.used_cells:
            current_objects = self.grid[cell[0]][cell[1]]
            for i in range(len(current_objects)):
                object1 = current_objects[i]
                for j in range(i, len(current_objects)):
                    object2 = current_objects[j]
                    if object1.collides(object2):
                        collision.append((object1, object2))
        return collision

    # Maintain proper grid and calculate collisions
    def update(self):
        for obj in self.objects:
            org_cords = obj.grid_cords
            new_cords = obj.calculate_grid_cords(self.slice_size)
            if new_cords != org_cords:
                # Check if mismatch is because cords changed and if the object needs to be removed from a cell
                if org_cords is not None and obj in self.grid[org_cords[0]][org_cords[1]]:
                    self.grid[org_cords[0]][org_cords[1]].remove(obj)
                    if not len(self.grid[org_cords[0]][org_cords[1]]): self.used_cells.remove(org_cords)
                # Append object to new cell
                self.grid[new_cords[0]][new_cords[1]].append(obj)
                if new_cords not in self.used_cells:
                    self.used_cells.append(new_cords)
            obj.grid_cords = new_cords

        # Actual collision check
        cols = self.get_collision_list()
        # Invoke event for each collision. Event name is cb_%s, with the partameter being the collided object.
        for col in cols:
            if col[0] is not None and col[1] is not None and col[0].parent is not None and col[1].parent is not None:
                print "Triggered %s, %s" % (col[0].name, col[1].name)
                self.game.events.invoke(col[0].name, col[1])
            if col[0] is not None and col[1] is not None and col[0].parent is not None and col[1].parent is not None:
                print "Triggered %s, %s" % (col[1].name, col[0].name)
                self.game.events.invoke(col[1].name, col[0])

        #print [(e.parent.name, e.name) for e in self.objects]
        #print self.game.events.events

    # Adds a collision box. If wall is set to True, it will be checked by in_wall
    def add(self, obj, wall=False):
        i = 1
        base_name = obj.name
        while obj.name in [c.name for c in self.objects]:
            obj.name = base_name + str(i)
            i += 1
        self.objects.append(obj)
        if wall:
            self.walls.append(obj)

    # Checks if obj is inside a wall.
    # obj should be a dummy collision box, to prevent a player from going through obstacles.
    def in_wall(self, obj):
        for wall in self.walls:
            if obj.collides(wall):
                return True
        return False

    # Draws collision box for debugging. Can be disabled by setting self.debug = False
    def draw(self):
        if self.debug:
            for obj in self.objects:
                obj.draw(self.game)

