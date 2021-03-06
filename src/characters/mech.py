from animation import ChainableAnimation
from characters.human import Human
from characters.projectiles import Projectile
from characters.projectiles.laser_beam import LaserBeam
from constants import ANIM_LOOP
from utils import Vector2
from game import game
import pyglet
from character import Character
from structure import Structure

image = pyglet.image.load('assets/characters/mech_32.png')


class Mech(Character):
    def __init__(self, *args, **kwargs):
        self._width = 32
        self._height = 32
        self.frame_size = (self._width, self._height)
        frame_period = 0.024
        sequences = {
            'idle': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(12*self.frame_size[0], 0, self.frame_size[0], self.frame_size[1]), ], frame_period),
            'walk_sw': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(i*self.frame_size[0], 0, self.frame_size[1], self.frame_size[1]) for i in range(0,16)], frame_period),
            'walk_w': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(i*self.frame_size[0], self.frame_size[1], self.frame_size[0], self.frame_size[1]) for i in range(0,16)], frame_period),
            'walk_nw': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(i*self.frame_size[0], 2*self.frame_size[1], self.frame_size[0], self.frame_size[1]) for i in range(0,16)], frame_period),
            'walk_n': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(i*self.frame_size[0], 3*self.frame_size[1], self.frame_size[0], self.frame_size[1]) for i in range(0,16)], frame_period),
            'walk_ne': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(i*self.frame_size[0], 4*self.frame_size[1], self.frame_size[0], self.frame_size[1]) for i in range(0,16)], frame_period),
            'walk_e': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(i*self.frame_size[0], 5*self.frame_size[1], self.frame_size[0], self.frame_size[1]) for i in range(0,16)], frame_period),
            'walk_se': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(i*self.frame_size[0], 6*self.frame_size[1], self.frame_size[0], self.frame_size[1]) for i in range(0,16)], frame_period),
            'walk_s': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(i*self.frame_size[0], 7*self.frame_size[1], self.frame_size[0], self.frame_size[1]) for i in range(0,16)], frame_period),
        }
        super(Mech, self).__init__(sequences, *args, **kwargs)

        self.collides_with = [Human,Structure,]
        self._collision_modifier = 5

    @property
    def check_collisions(self):
        return self._sequence_name != 'idle'

    def update(self, dt):
        if self._sequence_name == 'walk_n':
            self._dx = 0
            self._dy = self._speed
        elif self._sequence_name == 'walk_ne':
            self._dx = self._speed
            self._dy = self._speed
        elif self._sequence_name == 'walk_e':
            self._dx = self._speed
            self._dy = 0
        elif self._sequence_name == 'walk_se':
            self._dx = self._speed
            self._dy = -self._speed
        elif self._sequence_name == 'walk_s':
            self._dx = 0
            self._dy = -self._speed
        elif self._sequence_name == 'walk_sw':
            self._dx = -self._speed
            self._dy = -self._speed
        elif self._sequence_name == 'walk_w':
            self._dx = -self._speed
            self._dy = 0
        elif self._sequence_name == 'walk_nw':
            self._dx = -self._speed
            self._dy = self._speed
        else:
            self._dx = 0
            self._dy = 0

        if game.will_collide(self, self._x+self._dx*dt, self._y+self._dy*dt):
            self._dx = 0
            self._dy = 0

        super(Mech, self).update(dt)

    def shoot(self, x,y):
        center = self.center()
        laser = LaserBeam(Vector2(center[0], center[1]), Vector2(x,y), Projectile(500), batch=game.projectile_batch)
        game.to_update.add(laser)
