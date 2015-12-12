from constants import ANIM_LOOP
from pyglet import clock
from pyglet.image import Animation, AnimationFrame
from pyglet.sprite import Sprite


class MultipleAnimationSprite(Sprite):
    def __init__(self, sequences, default_sequence='idle', *args, **kwargs):
        self._animation_sequences = sequences
        self._sequence_name = default_sequence
        kwargs['img'] = self._animation_sequences[self._sequence_name]
        super(MultipleAnimationSprite, self).__init__(*args, **kwargs)

    def play(self, sequence_name):
        """Start playing the given sequence."""
        if sequence_name == self._sequence_name:
            return

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
