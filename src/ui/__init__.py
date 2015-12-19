import json
import os
from player import AssetQuantityTooLittle
import pyglet
from pyglet_gui.constants import *
from pyglet_gui.document import Document
from pyglet_gui.gui import Frame, SectionHeader, FoldingSection

from pyglet_gui.manager import Manager
from pyglet_gui.buttons import OneTimeButton
from pyglet_gui.scrollable import Scrollable
from pyglet_gui.containers import VerticalContainer
from ui.themes import action_menu_theme, resource_menu_theme

from game import game


class UIAction(OneTimeButton):
    def __init__(self, manager, label, **kwargs):
        super(UIAction, self).__init__(label, self.do_action)
        self._ui_manager = manager
        self._type = kwargs.get('type', 'na')
        self._options = kwargs.get('options', [])
        self._kwargs = kwargs.get('kwargs', {})

    def do_action(self, event):
        if self._type in ['root', 'parent']:
            actions = []
            print('making back button')
            actions.append(UIAction(self._ui_manager, 'Back', type='back'))
            for option in self._options:
                print('making action from options array')
                actions.append(UIAction.from_json(self._ui_manager, option))

            self._ui_manager.set_action_menu_content(actions)
        elif self._type == 'back':
            self._ui_manager.open_action_menu_previous_content()
        elif self._type == 'resources':
            self._ui_manager.open_resource_list()
        elif self._type == 'build_action':
            self._ui_manager.start_build_action(**self._kwargs)

    @classmethod
    def from_json(cls, manager, data):
        return cls(manager, **data)


class UIResourceList(object):
    def __init__(self, window, batch):
        self.window = window
        self.batch = batch
        self._resource_menu = None

    def render(self):
        self.remove()

        content = Frame(
            Scrollable(
                VerticalContainer([SectionHeader("Resources"),
                    UIResourceSection('Primary Resources', 'primary', is_open=True),
                    UIResourceSection('Processed Material', 'processed_material', is_open=False),
                    UIResourceSection('Raw Material', 'raw_material', is_open=False),
                    OneTimeButton('Close', self.remove)
                ], align=HALIGN_LEFT),
            height=400)
        )

        self._resource_menu = Manager(
            content,
            window=self.window, batch=self.batch,
            anchor=ANCHOR_TOP_LEFT,
            theme=resource_menu_theme
        )

    def remove(self, *args):
        if self._resource_menu:
            self._resource_menu.delete()


class UIResourceSection(FoldingSection):
    def __init__(self, title, category, *args, **kwargs):
        self._category = category
        self._folding_content = None
        super(UIResourceSection, self).__init__(title, [], *args, **kwargs)

    @property
    def folding_content(self):
        if self._folding_content and self._folding_content.is_loaded:
            return self._folding_content
        content = self.get_assets()
        self._folding_content = content
        return content

    @folding_content.setter
    def folding_content(self, v):
        pass

    def get_assets(self):
        documents = []

        for pa in game.player.assets:
            asset = game.get_asset(pa.asset_id)
            if asset.category == self._category:
                documents.append(UIResourceItem(asset, pa, width=150))
        return VerticalContainer(documents)


class UIResourceItem(Document):
    def __init__(self, asset, player_asset, *args, **kwargs):
        self._asset = asset
        self._player_asset = player_asset
        super(UIResourceItem, self).__init__(self.get_display(), *args, **kwargs)
        game.to_update.add(self)

    def get_display(self):
        return "%s: %s" % (self._asset.name, int(self._player_asset.quantity))

    def update(self, dt):
        if self.is_loaded:
            self.set_text(self.get_display())

    def unload(self):
        game.to_update.remove(self)
        super(UIResourceItem, self).unload()




class UIManager(object):
    PATH_UI_ACTIONS = 'data/ui/actions.json'

    def __init__(self):
        self._batch = pyglet.graphics.Batch()
        self._window = None
        self._frame_offset = (0,0)
        self._actions = []
        self._action_content_previous = []
        self._action_menu = None
        self._resource_menu = None
        self._build_action_instance = None

    @property
    def batch(self):
        return self._batch

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, window):
        self._window = window

    @property
    def frame_offset(self):
        return self._frame_offset

    @frame_offset.setter
    def frame_offset(self, offset):
        self._frame_offset = offset

    def _load_ui_actions(self):
        with open(os.path.join(self.PATH_UI_ACTIONS)) as json_file_object:
            for base_action in json.load(json_file_object):
                action = UIAction.from_json(self, base_action)
                self._actions.append(action)

        action_menu_content = []
        for action in self._actions:
            action_menu_content.append(action)
        self.set_action_menu_content(action_menu_content)

    def update(self, dt):
        if not self._action_menu:
            return

        self._action_menu.offset = (self.window.width-self._action_menu.width, self.window.height/2)

    def init_action_menu(self):
        # Set up a Manager
        self.set_action_menu_content()
        self._load_ui_actions()

    def set_action_menu_content(self, content=[]):
        if self._action_menu and content:
            self._action_content_previous.append(content)

        if self._action_menu:
            self._action_menu.delete()

        self._action_menu = Manager(
            # an horizontal layout with two vertical layouts, each one with a slider.
            Scrollable(height=self.window.height, width=400, content=VerticalContainer(content=content, align=HALIGN_RIGHT)),
            window=self.window,
            batch=self.batch,
            theme=action_menu_theme
        )

    def open_action_menu_previous_content(self):
        try:
            # We have to remove the current content and then pop again to get the previous content
            self._action_content_previous.pop()
            content = self._action_content_previous.pop()
            self.set_action_menu_content(content)
        except IndexError:
            pass

    def open_resource_list(self):
        if self._resource_menu is None:
            self._resource_menu = UIResourceList(self.window, self.batch)
        self._resource_menu.render()

    def start_build_action(self, structure_id, **kwargs):
        if self._build_action_instance:
            game.to_update.remove(self._build_action_instance)
            self._build_action_instance.delete()
        structure_factory = game.get_structure(structure_id)
        self._build_action_instance = structure_factory.build(x=0, y=0, batch=game.structure_batch)
        self._build_action_instance.opacity = 150
        game.to_update.add(self._build_action_instance)

    def get_map_from_mouse_pos(self, x, y):
        return -(self._frame_offset[0]-x), -(self._frame_offset[1]-y)

    def on_mouse_motion(self, x, y, dx, dy):
        if self._build_action_instance:
            structure = self._build_action_instance
            structure.x=-(self._frame_offset[0]-x+(structure.frame_size[0]/2))
            structure.y=-(self._frame_offset[1]-y+(structure.frame_size[1]/2))
            # @todo give a red tint to structure if colliding with something else
            # game.will_collide(self._build_action_instance, self._build_action_instance.x, self._build_action_instance.y)

    def on_mouse_press(self, x, y, button, modifiers):
        if self._build_action_instance:
            structure_factory = game.get_structure(self._build_action_instance.structure_id)
            if game.will_collide(self._build_action_instance):
                return

            # Resource requirements
            if len(structure_factory.tile_requirements):
                x, y = self.get_map_from_mouse_pos(x, y)
                for layer, requirement in structure_factory.tile_requirements.items():
                    prop, val = requirement.split(':')
                    tile = game.get_tile_at(layer, x, y)
                    if not tile or tile.properties.get(prop, None) != val:
                        game.message_queue.create_message('This structure has to be place on %s ' % val)
                        return


            # Asset requirements
            try:
                structure_factory.pay()
            except AssetQuantityTooLittle as e:
                # Display labebl
                game.message_queue.create_message(str(e))
                return
            self._build_action_instance.opacity = 255

            game.structures.add(self._build_action_instance)
            game.collidable.add(self._build_action_instance)
            game.requires_upkeep.add(self._build_action_instance)

            if modifiers == pyglet.window.key.MOD_SHIFT:
                structure_id = self._build_action_instance.structure_id
                self._build_action_instance = None
                self.start_build_action(structure_id)
            else:
                self._build_action_instance = None
            return True
        else:
            return False


ui_manager = UIManager()
