from animation import ChainableAnimation
from constants import ANIM_LOOP
import pyglet
from random import randint
from character import Character

human_image = pyglet.image.load('assets/characters/human2.png')


class Human(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(Human, self).__init__(human_image, *args, **kwargs)
        self._set_destination()
        self._set_waiting()

    def update(self, dt):
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