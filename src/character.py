from animation import MultipleAnimationSprite


class Character(MultipleAnimationSprite):
    def __init__(self, sequences, default_sequence='idle', *args, **kwargs):
        super(Character, self).__init__(sequences, default_sequence, *args, **kwargs)
        self._speed = 50
        self._destination = None
        self._dx = 0
        self._dy = 0

    def update(self, dt):
        self.x += self._dx*dt
        self.y += self._dy*dt
