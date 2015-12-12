from animation import ChainableAnimation
from constants import ANIM_LOOP
import pyglet
from structure import Structure

image = pyglet.image.load('assets/structures/power-plant.png')

class PowerPlant(Structure):
    def __init__(self, *args, **kwargs):
        self.frame_size = (40, 44)
        frame_period = 3.5
        sequences = {
            'idle': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(i*self.frame_size[0], 0, self.frame_size[0], self.frame_size[1]) for i in range(0,2)], frame_period),
        }
        super(PowerPlant, self).__init__(sequences, *args, **kwargs)
