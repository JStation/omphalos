from animation import Sequence, Frame
from constants import ANIM_LOOP
import pyglet
from character import Character

image = pyglet.image.load('assets/characters/mech.png')


class Mech(Character):
    def __init__(self, position, batch, group=None):

        frame_size = 64
        sequences = {
            'idle': Sequence([
                Frame(pyglet.sprite.Sprite(image.get_region(12*frame_size, 0, frame_size, frame_size),
                        0, 0, batch=batch, group=group))
            ], ANIM_LOOP),
            'walk_sw': Sequence([
                Frame(pyglet.sprite.Sprite(image.get_region(i*frame_size, 0, frame_size, frame_size),
                        0, 0, batch=batch, group=group)) for i in range(0,16)], ANIM_LOOP),
            'walk_w': Sequence([
                Frame(pyglet.sprite.Sprite(image.get_region(i*frame_size, 1*frame_size, frame_size, frame_size),
                        0, 0, batch=batch, group=group)) for i in range(0,16)], ANIM_LOOP),
            'walk_nw': Sequence([
                Frame(pyglet.sprite.Sprite(image.get_region(i*frame_size, 2*frame_size, frame_size, frame_size),
                        0, 0, batch=batch, group=group)) for i in range(0,16)], ANIM_LOOP),
            'walk_n': Sequence([
                Frame(pyglet.sprite.Sprite(image.get_region(i*frame_size, 3*frame_size, frame_size, frame_size),
                        0, 0, batch=batch, group=group)) for i in range(0,16)], ANIM_LOOP),
            'walk_ne': Sequence([
                Frame(pyglet.sprite.Sprite(image.get_region(i*frame_size, 4*frame_size, frame_size, frame_size),
                        0, 0, batch=batch, group=group)) for i in range(0,16)], ANIM_LOOP),
            'walk_e': Sequence([
                Frame(pyglet.sprite.Sprite(image.get_region(i*frame_size, 5*frame_size, frame_size, frame_size),
                        0, 0, batch=batch, group=group)) for i in range(0,16)], ANIM_LOOP),
            'walk_se': Sequence([
                Frame(pyglet.sprite.Sprite(image.get_region(i*frame_size, 6*frame_size, frame_size, frame_size),
                        0, 0, batch=batch, group=group)) for i in range(0,16)], ANIM_LOOP),
            'walk_s': Sequence([
                Frame(pyglet.sprite.Sprite(image.get_region(i*frame_size, 7*frame_size, frame_size, frame_size),
                        0, 0, batch=batch, group=group)) for i in range(0,16)], ANIM_LOOP),
        }
        super(Mech, self).__init__(position=position, sequences=sequences)

    def update(self, dt):
        if self.sequence_name == 'walk_n':
            self._dx = 0
            self._dy = self._speed
        elif self.sequence_name == 'walk_ne':
            self._dx = self._speed
            self._dy = self._speed
        elif self.sequence_name == 'walk_e':
            self._dx = self._speed
            self._dy = 0
        elif self.sequence_name == 'walk_se':
            self._dx = self._speed
            self._dy = -self._speed
        elif self.sequence_name == 'walk_s':
            self._dx = 0
            self._dy = -self._speed
        elif self.sequence_name == 'walk_sw':
            self._dx = -self._speed
            self._dy = -self._speed
        elif self.sequence_name == 'walk_w':
            self._dx = -self._speed
            self._dy = 0
        elif self.sequence_name == 'walk_nw':
            self._dx = -self._speed
            self._dy = self._speed
        else:
            self._dx = 0
            self._dy = 0
        super(Mech, self).update(dt)
