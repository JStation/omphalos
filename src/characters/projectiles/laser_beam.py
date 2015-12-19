import math
import pyglet
from game import game

laser = pyglet.image.load('assets/img/laser-red.png')


class LaserBeam(pyglet.sprite.Sprite):
    def __init__(self, start, target, projectile, *args, **kwargs):
        self._projectile = projectile
        super(LaserBeam, self).__init__(laser, x=start.x, y=start.y, *args, **kwargs)

        direction = math.atan2(target.y - start.y, target.x - start.x) * 180 / math.pi

        self._dx = math.cos(direction * math.pi / 180) * projectile.speed
        self._dy = math.sin(direction * math.pi / 180) * projectile.speed

        self._ticks = 0

    def update(self, dt):
        self.x += self._dx * dt
        self.y += self._dy * dt
        self._ticks += 1
        if self._ticks > 25:
            game.to_update_remove.add(self)
            self.delete()
