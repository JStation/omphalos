from constants import ANIM_LOOP


class Frame(object):
    def __init__(self, sprite, visible=False):
        self.sprite = sprite
        self.sprite.visible = visible


class Sequence(object):
    def __init__(self, frames, next_sequence):
        self.frames = frames
        self.next_sequence = next_sequence


class Animation(object):
    def __init__(self, sequences, default_sequence='idle', **kwargs):
        self.sequences = sequences
        self.sequence_name = None
        self.sprite = None
        self.play(default_sequence)

    def play(self, sequence_name):
        """Start playing the given sequence at the beginning."""
        if sequence_name == self.sequence_name:
            return

        if self.sprite:
            self.sprite.visible = False

        self.sequence_name = sequence_name
        self.sprite = None
        self.current_frame = 0
        self.sequence = self.sequences[sequence_name]

    def next_frame(self, dt):
        """Called by the main game update loop."""

        if self.sprite:
            self.sprite.visible = False

        self.current_frame += 1
        if self.current_frame >= len(self.sequence.frames):
            next = self.sequence.next_sequence
            if next is ANIM_LOOP:
                self.current_frame = 0
            else:
                self.play(next)

        frame = self.sequence.frames[self.current_frame]
        self.sprite = frame.sprite
        self.sprite.visible = True
