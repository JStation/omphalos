from animation import ChainableAnimation
from constants import ANIM_LOOP
import pyglet
from character import Character

image = pyglet.image.load('assets/characters/mech.png')


class Mech(Character):
    def __init__(self, *args, **kwargs):
        frame_size = 64
        fram_period = 0.024
        sequences = {
            'idle': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(12*frame_size, 0, frame_size, frame_size), ], fram_period),
            'walk_sw': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(i*frame_size, 0, frame_size, frame_size) for i in range(0,16)], fram_period),
            'walk_w': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(i*frame_size, frame_size, frame_size, frame_size) for i in range(0,16)], fram_period),
            'walk_nw': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(i*frame_size, 2*frame_size, frame_size, frame_size) for i in range(0,16)], fram_period),
            'walk_n': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(i*frame_size, 3*frame_size, frame_size, frame_size) for i in range(0,16)], fram_period),
            'walk_ne': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(i*frame_size, 4*frame_size, frame_size, frame_size) for i in range(0,16)], fram_period),
            'walk_e': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(i*frame_size, 5*frame_size, frame_size, frame_size) for i in range(0,16)], fram_period),
            'walk_se': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(i*frame_size, 6*frame_size, frame_size, frame_size) for i in range(0,16)], fram_period),
            'walk_s': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(i*frame_size, 7*frame_size, frame_size, frame_size) for i in range(0,16)], fram_period),
        }
        super(Mech, self).__init__(sequences, *args, **kwargs)

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
        super(Mech, self).update(dt)
