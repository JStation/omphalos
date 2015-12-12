from animation import Animation


class Character(Animation):
    def __init__(self, position, **kwargs):
        super(Character, self).__init__(**kwargs)
        self._position = position
        self._speed = 25
        self._destination = None
        self._dx = 0
        self._dy = 0

    @property
    def x(self):
        return self._position[0]

    @x.setter
    def x(self, x):
        self._position = (x, self.y)

    @property
    def y(self):
        return self._position[1]

    @y.setter
    def y(self, y):
        self._position = (self.x, y)

    def update(self, dt):
        self.next_frame(dt)
        self.x += self._dx*dt
        self.y += self._dy*dt
        self.sprite.x = self.x
        self.sprite.y = self.y
