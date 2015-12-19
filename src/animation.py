from constants import ANIM_LOOP
from pyglet import clock
from pyglet.image import Animation, AnimationFrame
from pyglet.sprite import Sprite


class MultipleAnimationSprite(Sprite):
    def __init__(self, sequences, default_sequence='idle', *args, **kwargs):
        self._collision_modifier = 0

        self._animation_sequences = sequences
        self._default_sequence = default_sequence
        self._sequence_name = default_sequence
        kwargs['img'] = self._animation_sequences[self._sequence_name]
        super(MultipleAnimationSprite, self).__init__(*args, **kwargs)

    def play(self, sequence_name):
        """Start playing the given sequence."""
        if sequence_name == self._sequence_name:
            return

        if not sequence_name in self._animation_sequences:
            # For development only, we don't always add all required animation sequences when creating new structures
            sequence_name = self._default_sequence

        self._frame_index = -1
        self._sequence_name = sequence_name
        self._animation = self._animation_sequences[sequence_name]

    def _animate(self, dt):
        self._frame_index += 1
        if self._frame_index >= len(self._animation.frames):
            self._frame_index = 0
            self.dispatch_event('on_animation_end')
            if self._vertex_list is None:
                return # Deleted in event handler.

        frame = self._animation.frames[self._frame_index]
        self._set_texture(frame.image.get_texture())

        if frame.duration is None and hasattr(frame, 'next_sequence'):
            if not frame.next_sequence == ANIM_LOOP:
                self._animation = self._animation_sequences[frame.next_sequence]
            self._frame_index = -1

        if frame.duration is not None:
            duration = frame.duration - (self._next_dt - dt)
            duration = min(max(0, duration), frame.duration)
            clock.schedule_once(self._animate, duration)
            self._next_dt = duration
        else:
            self.dispatch_event('on_animation_end')

    # @todo move these to a different class
    def center(self, at_x=None, at_y=None):
        x = at_x or self._x
        y = at_y or self._y
        return x+self._width / 2, y + self._height / 2

    def hit_center(self, at_x=None, at_y=None):
        if not hasattr(self, '_hit_box'):
            return self.center(at_x, at_y)
        x = at_x or self._x
        y = at_y or self._y
        return x+self._hit_box[0] / 2, y + self._hit_box[1] / 2

    def hit_test(self, obj, at_x=None, at_y=None):
        obj_center = obj.hit_center(at_x, at_y)
        if abs(self.hit_center()[0] - obj_center[0]) < self.hit_width / 2 + obj.hit_width / 2 and \
                        abs(self.hit_center()[1] - obj_center[1]) < self.hit_height / 2 + obj.hit_height / 2:
            return True

    @property
    def hit_width(self):
        if hasattr(self, '_hit_box'):
            return self._hit_box[0]
        return self._width - self._collision_modifier

    @property
    def hit_height(self):
        if hasattr(self, '_hit_box'):
            return self._hit_box[1]
        return self._height - self._collision_modifier

    @property
    def check_collisions(self):
        return True

class ChainableAnimation(Animation):
    def __init__(self, next_sequence, default_period, *args, **kwargs):
        self.next_sequence = next_sequence
        self.default_period = default_period
        super(ChainableAnimation, self).__init__(*args, **kwargs)

    @classmethod
    def from_image_sequence(cls, next_sequence, sequence, period, loop=True):
        frames = [AnimationFrame(image, period) for image in sequence]
        if not loop:
            frames[-1].duration = None
        return cls(next_sequence, period, frames)
