"""
This is tested on pyglet 1.2 and python 2.7.
Leif Theden "bitcraft", 2012-2014
Rendering demo for the TMXLoader.
This should be considered --alpha-- quality.  I'm including it as a
proof-of-concept for now and will improve on it in the future.
Notice: slow!  no transparency!
"""
import logging
from time import sleep
from pyglet.gl import GLException
from pyglet.window import mouse
from pyglet import clock
from pymunk import Vec2d
import pymunk as pm

import numpy as np

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)
logger.setLevel(logging.INFO)

from pytmx import *
from pytmx.util_pyglet import load_pyglet
import pyglet
from camera import Camera

class TiledRenderer(object):
    """
    Super simple way to render a tiled map with pyglet
    no shape drawing yet
    """
    def __init__(self, filename, camera):
        tm = load_pyglet(filename)
        self.camera = camera
        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tile_size = tm.tilewidth
        self.tmx_data = tm
        self.batches = []   # list of batches, e.g. layers
        self.sprites = []  # container for tiles
        self.np_indexes = []
        self.generate_sprites()

    def draw_rect(self, color, rect, width):
        pass

    def draw_lines(self, color, closed, points, width):
        pass

    def get_visible_sprites(self, sprites, start_x, start_y, end_x, end_y):
        for sprite in sprites:
            if start_x <= sprite.tile_coord['x'] <= end_x \
                    and start_y <= sprite.tile_coord['y'] <= end_y:
                sprite.visible = True
                yield sprite
            else:
                sprite.visible = False

    def generate_sprites(self):
        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        mw = self.tmx_data.width
        mh = self.tmx_data.height - 1
        pixel_height = (mh + 1) * th
        draw_rect = self.draw_rect
        draw_lines = self.draw_lines

        rect_color = (255, 0, 0)
        poly_color = (0, 255, 0)

        for layer in self.tmx_data.visible_layers:
            batch = pyglet.graphics.Batch() # create a new batch
            self.batches.append(batch)      # add the batch to the list
            # draw map tile layers
            np_index = np.zeros((100,100), np.int32)
            self.np_indexes.append(np_index)

            if isinstance(layer, TiledTileLayer):

                # iterate over the tiles in the layer
                for x, y, image in layer.tiles():
                    print(x,y)
                    tile_coord = {
                        'x':x,
                        'y':y,
                        'image':image
                    }
                    y = mh - y
                    x = x * tw
                    y = y * th
                    sprite = pyglet.sprite.Sprite(
                        image, batch=batch, x=x, y=y
                    )
                    sprite.tile_coord = tile_coord
                    self.sprites.append(sprite)
                    np_index[tile_coord['x'],tile_coord['y']] = self.sprites.index(sprite)

            # draw object layers
            elif isinstance(layer, TiledObjectGroup):

                # iterate over all the objects in the layer
                for obj in layer:
                    logger.info(obj)

                    # objects with points are polygons or lines
                    if hasattr(obj, 'points'):
                        draw_lines(poly_color, obj.closed, obj.points, 3)

                    # some object have an image
                    elif obj.image:
                        try:
                            obj.image.blit(obj.x, pixel_height - obj.y)
                        except GLException: # Not sure this is being raised on Windows
                            pass

                    # draw a rect for everything else
                    else:
                        draw_rect(rect_color,
                                  (obj.x, obj.y, obj.width, obj.height), 3)

            # draw image layers
            elif isinstance(layer, TiledImageLayer):
                if layer.image:
                    x = mw // 2  # centers image
                    y = mh // 2
                    sprite = pyglet.sprite.Sprite(
                        layer.image, batch=batch, x=x, y=y
                    )
                    self.sprites.append(sprite)


    def draw(self):
        self.camera.move(0,-1)
        start_x, start_y, end_x, end_y = self.camera.get_visible_range()

        for index in self.np_indexes:
            for x in range(start_x, end_x):
                for y in range(start_y, end_y):
                    sprite_id = index[x,y]
                    if sprite_id > 0:
                        sprite = self.sprites[sprite_id]
                        _x,_y = self.camera.grid_to_px(sprite.tile_coord['x'], sprite.tile_coord['y'])
                        sprite.x = _x
                        sprite.y = _y

        for b in self.batches:
            b.draw()


    def drawx(self):
        self.camera.move(0,-1)
        start_x, start_y, end_x, end_y = self.camera.get_visible_range()
        for sprite in self.get_visible_sprites(self.sprites, start_x, start_y, end_x, end_y):
            x,y = self.camera.grid_to_px(sprite.tile_coord['x'], sprite.tile_coord['y'])
            sprite.x = x
            sprite.y = y

        self.camera.changed = False

        for b in self.batches:
            b.draw()


class SimpleTest(object):
    def __init__(self, filename, camera):
        self.camera = camera
        self.renderer = None
        self.running = False
        self.dirty = False
        self.exit_status = 0
        self.load_map(filename)

    def load_map(self, filename):
        self.renderer = TiledRenderer(filename, self.camera)

        logger.info("Objects in map:")
        for obj in self.renderer.tmx_data.objects:
            logger.info(obj)
            for k, v in obj.properties.items():
                logger.info("%s\t%s", k, v)

        logger.info("GID (tile) properties:")
        for k, v in self.renderer.tmx_data.tile_properties.items():
            logger.info("%s\t%s", k, v)

    def draw(self):
        self.renderer.draw()


def all_filenames():
    import os.path
    import glob
    _list = glob.glob(os.path.join('maps', '*.tmx'))
    try:
        while _list:
            yield _list.pop(0)
    except IndexError:
        pyglet.app.exit()


class TestWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(TestWindow, self).__init__(*args, **kwargs)
        self.alive = True
        self.camera = Camera(1000, 1000, offset=(2,2))
        #pm.init_pymunk()
        self.mouse_body = pm.Body(pm.inf, pm.inf)
        self.mouse_shape = pm.Circle(self.mouse_body, 3, Vec2d(0,0))
        clock.set_fps_limit(60)
        pyglet.clock.schedule_interval(self.update, 1.0/60.0)
        self.fps_display = clock.ClockDisplay()
        if not hasattr(self, 'filenames'):
            self.filenames = all_filenames()
            self.next_map()
        self.run()

    # You need the dt argument there to prevent errors,
    # it does nothing as far as I know.
    def update(self, dt):
        pass

    def on_draw(self):
        self.render()

    def render(self):
        self.clear()
        self.fps_display.draw()
        self.contents.draw()

    def run(self):
        while self.alive:
            self.render()
            event = self.dispatch_events()
            sleep(1.0/60.0)

    def next_map(self):
        try:
            self.contents = SimpleTest(next(self.filenames), self.camera)
        except StopIteration:
            pyglet.app.exit()

    def on_key_press(self, symbol, mod):
        if symbol == pyglet.window.key.ESCAPE:
            self.alive = False
            pyglet.app.exit()
        elif symbol == pyglet.window.key.RIGHT:
            print("right arrow")
            self.camera.move(5,0)
        elif symbol == pyglet.window.key.LEFT:
            print("left")
            self.camera.move(-5,0)
        elif symbol == pyglet.window.key.DOWN:
            print("down")
            self.camera.move(0,-5)
        elif symbol == pyglet.window.key.UP:
            print("up")
            self.camera.move(0,5)
        else:
            self.next_map()

if __name__ == '__main__':
    window = TestWindow(1000, 1000)
    pyglet.app.run()
