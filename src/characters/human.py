from animation import ChainableAnimation
from constants import ANIM_LOOP
from player import AssetQuantityTooLittle
import pyglet
from random import randint, choice, random, sample
from character import Character
from structure import Structure

human_image = pyglet.image.load('assets/characters/human2.png')

blood1 = pyglet.image.load('assets/characters/blood.png')
blood2 = pyglet.image.load('assets/characters/blood2.png')
blood_images = [blood1, blood2]


class Human(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        from characters.mech import Mech
        super(Human, self).__init__(human_image, *args, **kwargs)
        self._set_destination()
        self._set_waiting()
        self.alive = True



        # stuff for collision
        self._height = self._get_height()
        self._width = self._get_width()
        self.hit_width = self._width
        self.hit_height = self._height
        self.does_not_collide_with = [Mech,]

    @property
    def check_collisions(self):
        return True

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

    def upkeep(self, dt):
        from game import game
        has_food = False
        mood = 0
        if game.player.has_asset('water'):
            try:
                game.player.get_asset('water').subtract(0.5)
                mood += 0.01
            except AssetQuantityTooLittle:
                mood -= 0.1
        else:
            mood -= 0.1

        if game.player.has_asset('food_healthy'):
            try:
                game.player.get_asset('food_healthy').subtract(5)
                mood += 0.05
                has_food = True
            except AssetQuantityTooLittle:
                mood -= 0.01

        if not has_food and game.player.has_asset('food_unhealthy'):
            try:
                game.player.get_asset('food_unhealthy').subtract(5)
                mood += 0.01
            except AssetQuantityTooLittle:
                mood -= 0.01
        else:
            mood -= 0.05

        if mood != 0:
            game._environment.add_to_variable('mood', mood)

    def _set_destination(self):
        from game import game
        structure = sample(game.structures, 1)[0]
        dest_x = structure.x  # temporary bounding box to prevent aimless wandering
        dest_y = structure.y
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

