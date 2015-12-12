# Import/Initialize
import pyglet

from tiledtmxloader import helperspyglet

#TODO: make relative path access work
#_default_loader.path= ['.maps',]
#_default_loader.reindex()


# Display



# Entities



# @win.event
# def on_key_press(symbol, modifiers):
#     if symbol == pyglet.window.key.ESCAPE:
#             pyglet.app.exit()
#     elif symbol == pyglet.window.key.T:
#             print("t has been pressed")

# @win.event
# def on_draw():
#     pass

# Action
    #print('FPS is %f' % clock.get_fps())

if __name__ == '__main__':
    helperspyglet.demo_pyglet('maps/test2.tmx')