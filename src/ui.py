import pyglet
from pyglet.gl import glTranslated
from pyglet_gui.constants import HALIGN_RIGHT

from pyglet_gui.manager import Manager
from pyglet_gui.buttons import Button, OneTimeButton
from pyglet_gui.scrollable import Scrollable
from pyglet_gui.containers import VerticalContainer
from pyglet_gui.theme import Theme


class UIManager(object):
    def __init__(self):
        self._batch = pyglet.graphics.Batch()
        self._window = None
        self._frame_offset = (0,0)

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

    def update(self, dt):
        if not self.manager:
            return

        self.manager.offset = (self.window.width-self.manager.width, self.window.height/2)

    def test_window(self):
        theme = Theme({"font": "Lucida Grande",
               "font_size": 10,
               "text_color": [255, 255, 255, 255],
               "gui_color": [255, 0, 0, 255],
               "button": {
                   "down": {
                       "image": {
                           "source": "button-down.png",
                           "frame": [8, 6, 2, 2],
                           "padding": [18, 18, 8, 6]
                       },
                       "text_color": [0, 0, 0, 255]
                   },
                   "up": {
                       "image": {
                           "source": "button.png",
                           "frame": [6, 5, 6, 3],
                           "padding": [18, 18, 8, 6]
                       }
                   }
               },
               "vscrollbar": {
                   "knob": {
                       "image": {
                           "source": "vscrollbar.png",
                           "region": [0, 16, 16, 16],
                           "frame": [0, 6, 16, 4],
                           "padding": [0, 0, 0, 0]
                       },
                       "offset": [0, 0]
                   },
                   "bar": {
                       "image": {
                           "source": "vscrollbar.png",
                           "region": [0, 64, 16, 16]
                       },
                       "padding": [0, 0, 0, 0]
                   }
               }
              }, resources_path='theme/')

        # Set up a Manager
        self.manager = Manager(
            # an horizontal layout with two vertical layouts, each one with a slider.
            Scrollable(height=self.window.height, width=200, content=VerticalContainer(content=[OneTimeButton('Power Plant'), OneTimeButton('Iron Extractor'),], align=HALIGN_RIGHT)),
            window=self.window,
            batch=self.batch,
            theme=theme)

ui_manager = UIManager()
