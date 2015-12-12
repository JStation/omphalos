#/usr/bin/env python

import pyglet
from map import Map
from pyglet.resource import _default_loader

_default_loader.path= ['maps',]

window = pyglet.window.Window()

# load the map
fd = pyglet.resource.file('test.json', 'rt')
m = Map.load_json(fd)

# set the viewport to the window dimensions
m.set_viewport(0, 0, window.width, window.height)

@window.event
def on_draw():
    window.clear()
    m.draw()

pyglet.app.run()
