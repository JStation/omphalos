from animation import MultipleAnimationSprite

structure_classes = {}


def register_structure(cls):
    structure_classes[cls.STRUCTURE_ID] = cls
    return cls


class Structure(MultipleAnimationSprite):
    STRUCTURE_FRAME_SIZE = (0, 0)
    STRUCTURE_ID = None

    def update(self, dt):
        pass

    @property
    def frame_size(self):
        return self.STRUCTURE_FRAME_SIZE

    @property
    def structure_id(self):
        return self.STRUCTURE_ID