from animation import MultipleAnimationSprite, ChainableAnimation
from constants import ANIM_LOOP
from player import AssetQuantityTooLittle
import pyglet

images = {}


def get_image(image):
    if not image in images:
        images[image] = pyglet.image.load(image)
    return images[image]


class StructureFactory(object):
    def __init__(self, **kwargs):
        self._structure_id = kwargs['id']
        self._name = kwargs['name']
        self._build_requirements = kwargs.get('requires', {})
        self._produces = kwargs.get('produces', {})
        self._consumes = kwargs.get('consumes', {})
        self._environment = kwargs.get('environment', {})
        self._image = get_image(kwargs['image'])
        self._width = kwargs['width']
        self._height = kwargs['height']
        self._animation_speed = kwargs.get('animation_speed', 3)
        self._animation = kwargs.get('animations', {
            'idle':1
        })

        self._animation_sequences = {}
        y = len(self._animation) - 1
        # y is in reverse order, frames are read from bottom to top
        for name, frames in self._animation.items():
            self._animation_sequences[name] = ChainableAnimation.from_image_sequence(
                ANIM_LOOP, [
                    self._image.get_region(
                        self._width*x,
                        self._height*y,
                        self._width,
                        self._height
                    ) for x in range(0, frames)
                ], self._animation_speed)
            y -= 1


    @property
    def structure_id(self):
        return self._structure_id

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def produces(self):
        return self._produces

    @property
    def consumes(self):
        return self._consumes

    @property
    def environment(self):
        return self._environment

    @property
    def animation_sequences(self):
        return self._animation_sequences

    def build(self, *args, **kwargs):
        return Structure.from_factory(self, *args, **kwargs)

    @classmethod
    def from_json(cls, json_data):
        return cls(**json_data)

    def pay(self):
        from game import game
        for asset_id, amount in self._build_requirements.items():
            asset = game.get_asset(asset_id)
            player_asset = game.player.get_asset(asset_id)
            if not player_asset or amount > player_asset.quantity:
                raise AssetQuantityTooLittle('%s requires %s %s, you have %s' % (
                    self._name,
                    amount,
                    asset.name,
                    player_asset.quantity
                ))

        for asset_id, amount in self._build_requirements.items():
            game.player.get_asset(asset_id).subtract(amount)


class Structure(MultipleAnimationSprite):
    def __init__(self, sequences, *args, **kwargs):
        self._structure_active = True
        self._structure_id = kwargs['structure_id']
        del kwargs['structure_id']

        self._produces = kwargs.get('produces', {})
        self._consumes = kwargs.get('consumes', {})
        self._environment = kwargs.get('environment', {})
        del kwargs['produces']
        del kwargs['consumes']
        del kwargs['environment']

        self._width = kwargs['width']
        self._height = kwargs['height']
        del kwargs['width']
        del kwargs['height']

        super(Structure, self).__init__(sequences, *args, **kwargs)

    def update(self, dt):
        pass

    def upkeep(self, dt):
        if self.consume(dt):
            self.produce(dt)
            self.environment(dt)

    def center(self):
        return (self._x+(self._width/2), self._y+(self._height/2))

    def hit_test(self, obj, x, y):
        # return Math.abs(center.x - os.center.x) < width / 2 + os.width / 2
        #    && Math.abs(center.y - os.center.y) < height / 2 + os.width / 2;
        if self.center()[0] - obj.center()[0] < self._width / 2 + obj.width / 2 and self.center()[1] - obj.center()[1] < self._height / 2:
            print('hit %s x %s' % (x, y))

    def consume(self, dt):
        from game import game
        try:
            for asset_id, amount in self._consumes.items():
                amount *= dt
                player_asset = game.player.get_asset(asset_id)
                if not player_asset or  amount > player_asset.quantity:
                    raise AssetQuantityTooLittle()

            for asset_id, amount in self._consumes.items():
                amount *= dt
                game.player.get_asset(asset_id).subtract(amount)

            self._structure_active = True
            self.play('idle')
        except AssetQuantityTooLittle:
            self.play('inactive')
            self._structure_active = False
        return self._structure_active

    def produce(self, dt):
        from game import game
        for asset_id, amount in self._produces.items():
            game.player.add_asset(asset_id, amount*dt)

    def environment(self, dt):
        from game import game
        for environment_id, amount in self._environment.items():
            game.environment.add_to_variable(environment_id, amount*dt)

    @property
    def frame_size(self):
        return (self.width, self.height)

    @property
    def structure_id(self):
        return self._structure_id

    @classmethod
    def from_factory(cls, factory, *args, **kwargs):
        kwargs['structure_id'] = factory.structure_id
        kwargs['produces'] = dict(factory.produces)
        kwargs['consumes'] = dict(factory.consumes)
        kwargs['environment'] = dict(factory.environment)
        kwargs['width'] = factory.width
        kwargs['height'] = factory.height

        return cls(
            factory.animation_sequences,
            *args,
            **kwargs
        )
