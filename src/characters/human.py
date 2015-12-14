from animation import ChainableAnimation
from constants import ANIM_LOOP
import pyglet
from random import randint, choice
from character import Character

human_image = pyglet.image.load('assets/characters/human2.png')

blood1 = pyglet.image.load('assets/characters/blood.png')
blood2 = pyglet.image.load('assets/characters/blood2.png')
blood_images = [blood1, blood2]

class Human(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(Human, self).__init__(human_image, *args, **kwargs)
        self._set_destination()
        self._set_waiting()
        self.alive = True



        # stuff for collision
        self._height = self._get_height()
        self._width = self._get_width()
        self.hit_width = self._width
        self.hit_height = self._height

    def update(self, dt):
        if not self.alive:
            return

        arrived = self._at_destination()
        if arrived:
            # print("arrived!")
            self._set_destination()

        elif self.waiting > 0:
            self.waiting -= 1

        else:
            if self._seeking_x:
                if self.destination[0] > self.x:
                    self.x += 1
                else:
                    self.x -= 1
            if self._seeking_y:
                if self.destination[1] > self.y:
                    self.y += 1
                else:
                    self.y -= 1
        #print("location: %s, %s" % (self.x, self.y))

    def _set_destination(self):
        dest_x = randint(0, 1000)  # temporary bounding box to prevent aimless wandering
        dest_y = randint(1000,1600)
        self.destination = (dest_x, dest_y)
        #print("new destination: %s" % (str(self.destination)))

    def _at_destination(self):
        x = abs(self.x - self.destination[0])
        self._seeking_x = (x>=1)
        y = abs(self.y - self.destination[1])
        self._seeking_y = (y>=1)

        return (not self._seeking_x and not self._seeking_y)

    def _set_waiting(self):
        self.waiting = randint(5,240)

    def center(self, at_x=None, at_y=None):
        x = at_x or self._x
        y = at_y or self._y
        return x+self._width / 2, y + self._height / 2

    # copied from Animation
    def hit_center(self, at_x=None, at_y=None):
        if not hasattr(self, '_hit_box'):
            return self.center(at_x, at_y)
        x = at_x or self._x
        y = at_y or self._y
        return x+self._hit_box[0] / 2, y + self._hit_box[1] / 2

    def hit_test(self, obj, at_x=None, at_y=None):
        if not self.alive:
            return False
        obj_center = obj.hit_center(at_x, at_y)
        if abs(self.hit_center()[0] - obj_center[0]) < self.hit_width / 2 + obj.hit_width / 2 and \
                        abs(self.hit_center()[1] - obj_center[1]) < self.hit_height / 2 + obj.hit_height / 2:
            self.die()
            return True

    def die(self):
        self._set_image(choice(blood_images))
        self.alive = False

