import json
import os
from asset import Asset
from player import Player

class Game(object):
    PATH_ASSETS = 'data/assets/'

    def __init__(self):
        self._assets = set()
        self._player = Player()

        self._load_assets()

    @property
    def player(self):
        return self._player

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
