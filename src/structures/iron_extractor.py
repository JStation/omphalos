from animation import ChainableAnimation
from constants import ANIM_LOOP
from game import game
from player import AssetQuantityTooLittle
import pyglet
from structure import Structure

image = pyglet.image.load('assets/structures/iron-extractor.png')


class IronExtractor(Structure):
    def __init__(self, *args, **kwargs):
        self.frame_size = (40, 64)
        self.asset = game.get_asset('iron_ore')
        self.power_per_second = 5
        self.asset_per_second = 2
        frame_period = 5
        sequences = {
            'idle': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(i*self.frame_size[0], self.frame_size[1], self.frame_size[0], self.frame_size[1]) for i in range(0,2)], frame_period),
            'inactive': ChainableAnimation.from_image_sequence(ANIM_LOOP, [image.get_region(i*self.frame_size[0], 0, self.frame_size[0], self.frame_size[1]) for i in range(0,2)], frame_period),

        }
        super(IronExtractor, self).__init__(sequences, *args, **kwargs)

    def upkeep(self, dt):
        # Consume power
        try:
            game.player.get_asset('power').subtract(self.power_per_second)
            self.structure_active = True
            self.play('idle')
        except (AssetQuantityTooLittle, AttributeError):
            print('Not enough power for this structure')
            self.play('inactive')
            self.structure_active = False

        # Add ore
        if self.structure_active:
            game.player.add_asset(self.asset.asset_id, self.asset_per_second*dt)
            print(self.asset.name, game.player.get_asset(self.asset.asset_id).quantity)
