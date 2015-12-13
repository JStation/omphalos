import json
import os
from asset import Asset
from player import Player
import pyglet


class Game(object):
    PATH_ASSETS = 'data/assets/'

    def __init__(self):
        self._assets = set()
        self._player = Player()
        self._ui_actions = []

        self._load_assets()

        self._to_update = set()
        self._requires_upkeep = set()

        self._tiles = pyglet.graphics.Batch()
        self._humans = pyglet.graphics.Batch()
        self._characters = pyglet.graphics.Batch()
        self._structures = pyglet.graphics.Batch()
        self._sprites = []

    @property
    def player(self):
        return self._player

    @property
    def requires_upkeep(self):
        return self._requires_upkeep

    @property
    def to_update(self):
        return self._to_update

    @property
    def tiles(self):
        return self._tiles

    @property
    def humans(self):
        return self._humans

    @property
    def characters(self):
        return self._characters

    @property
    def structures(self):
        return self._structures

    @property
    def sprites(self):
        return self._sprites

    def update(self, dt):
        for obj in self._to_update:
            obj.update(dt)

    def upkeep(self, dt):
        for obj in self._requires_upkeep:
            obj.upkeep(dt)

    def _load_assets(self):
        for asset in Game.load_json_objects(self.PATH_ASSETS):
            self._assets.add(Asset.from_json(asset))

    def get_asset(self, asset_id):
        for asset in self._assets:
            if asset_id == asset.asset_id:
                return asset
        return None

    @staticmethod
    def load_json_objects(json_path):
        objects = []
        json_files = [json_file for json_file in os.listdir(json_path) if json_file.endswith('.json')]
        for json_file in json_files:
            with open(os.path.join(json_path, json_file)) as json_file_object:
                objects.append(json.load(json_file_object))
        return objects

game = Game()
