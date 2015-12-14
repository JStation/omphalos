from characters.human import Human
from collections import OrderedDict
import json
from environment import Environment, EnvironmentVariable
from labels import MessageHandler
import os
from asset import Asset
from player import Player
import pyglet
import random
from structure import StructureFactory


class Game(object):
    PATH_ASSETS = 'data/assets/'
    PATH_ENVIRONMENT_VARIABLES = 'data/environment/'
    PATH_STRUCTURES = 'data/structures/'

    def __init__(self):
        self._collidable = set()
        self._assets = set()
        self._structure_builders = set()
        self._environment = Environment(self._get_environment_variables())
        self._player = Player()
        self._ui_actions = []

        self._world_map = None

        self._load_assets()
        self._load_structures()

        self._to_update = set()
        self._requires_upkeep = set()

        self._tiles = pyglet.graphics.Batch()
        self._humans = pyglet.graphics.Batch()
        self._characters = pyglet.graphics.Batch()

        self._structures = set()
        self._structure_batch = pyglet.graphics.Batch()
        self._sprites = []

        # Default Player Assets
        self._player.add_asset('power', 1150)
        self._player.add_asset('money', 500)
        self._player.add_asset('food_unhealthy', 200)
        self._player.add_asset('iron', 1500)
        self._player.add_asset('water', 100)

        # Message Queue
        self._message_queue = MessageHandler(x=15, y=15)
        self._to_update.add(self._message_queue)

        # Game message
        self._message_queue.create_message("Omphalos 2217")

        # Temp variable
        self._water_requirement = 100

    @property
    def message_queue(self):
        return self._message_queue

    @property
    def world_map(self):
        return self._world_map

    @world_map.setter
    def world_map(self, world_map):
        if self.world_map:
            return
        self._world_map = world_map

    def get_tile_at(self, layer_name, x, y):
        return self.world_map.get_tile_from_layer_at(layer_name, x, y)

    @property
    def player(self):
        return self._player

    @property
    def collidable(self):
        return self._collidable

    def will_collide(self, to_check, at_x=None, at_y=None):
        for obj in self.collidable:
            if obj == to_check:
                continue
            if obj.hit_test(to_check, at_x, at_y):
                return True

    @property
    def environment(self):
        return self._environment

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
    def structure_batch(self):
        return self._structure_batch

    @property
    def sprites(self):
        return self._sprites

    def update(self, dt):
        for obj in self._to_update:
            obj.update(dt)

    def upkeep(self, dt):
        for obj in self._requires_upkeep:
            obj.upkeep(dt)

        self.message_queue.create_message('The mood of your people is %s.' % self._environment.get_variable('mood').value)

        if self.player.has_asset('water') and self.player.get_asset('water').quantity > self._water_requirement:
            for structure in self.structures:
                if structure.structure_id == 'teleportation_chamber':
                    self.message_queue.create_message("YOU HAVE ENOUGH WATER FOR LIFE!")
                    self._water_requirement *= 2
                    for n in range(0, random.randint(self._water_requirement/20, self._water_requirement/10)):
                        h = Human(x=structure.x, y=structure.y, batch=game.humans)
                        # game.collidable.add(h)
                        self.to_update.add(h)
                        self.requires_upkeep.add(h)


    def _load_assets(self):
        for asset in Game.load_json_objects(self.PATH_ASSETS):
            self._assets.add(Asset.from_json(asset))

    def get_asset(self, asset_id):
        for asset in self._assets:
            if asset_id == asset.asset_id:
                return asset
        return None

    def _load_structures(self):
        for structure in Game.load_json_objects(self.PATH_STRUCTURES):
            self._structure_builders.add(StructureFactory.from_json(structure))

    def get_structure(self, structure_id):
        for structure in self._structure_builders:
            if structure_id == structure.structure_id:
                return structure

    def _get_environment_variables(self):
        variables = set()
        for variable in Game.load_json_objects(self.PATH_ENVIRONMENT_VARIABLES):
            variables.add(EnvironmentVariable.from_json(variable))
        return variables

    @staticmethod
    def load_json_objects(json_path):
        objects = []
        json_files = [json_file for json_file in os.listdir(json_path) if json_file.endswith('.json')]
        for json_file in json_files:
            with open(os.path.join(json_path, json_file)) as json_file_object:
                objects.append(json.load(json_file_object, object_pairs_hook=OrderedDict))
        return objects

game = Game()
