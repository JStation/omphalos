# Import/Initialize
import pyglet
from pyglet import clock
from pyglet.window import Window

clock.set_fps_limit(60)

# Display
win = Window(width=640, height=480)


# Entities
fps_display = clock.ClockDisplay()

@win.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()

@win.event
def on_draw():
    win.clear()
    fps_display.draw()


# Action
    #print('FPS is %f' % clock.get_fps())
pyglet.app.run()