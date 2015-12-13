import pyglet
from pyglet.media.riff import WAVEFormatException
from pyglet.gl import *
from tiledtmxloader import tmxreader
from tiledtmxloader.helperspyglet import ResourceLoaderPyglet
from pyglet.gl import glTranslatef, glLoadIdentity
from characters.mech import Mech
from characters.human import Human
from ui import ui_manager
from constants import WINDOW_WIDTH, WINDOW_HEIGHT

from labels import MessageHandler

from game import game

MAP_FILE = "maps/test2.tmx"
FULLSCREEN_MODE = False
# Sounds
pyglet.options['audio'] = ('openal', 'silent')
try:
    pass
    #pyglet.lib.load_library('lib/avbin.dll')
    #pyglet.have_avbin=True
    #bg_music = pyglet.media.load('assets/sound/bg_music.mp3', streaming=False)
except (WAVEFormatException, ImportError):
    pass

world_map = tmxreader.TileMapParser().parse_decode(MAP_FILE)

# delta is the x/y position of the map view.
# delta is a list so that it can be accessed from the on_draw method of
# window and the update function. Note that the position is in integers to
# match Pyglet Sprites. Using floating-point numbers causes graphical
# problems. See http://groups.google.com/group/pyglet-users/browse_thread/thread/52f9ae1ef7b0c8fa?pli=1
delta = [200, -world_map.pixel_height+150]
frames_per_sec = 1.0 / 30.0
window = pyglet.window.Window(width=WINDOW_WIDTH,height=WINDOW_HEIGHT, fullscreen=FULLSCREEN_MODE)

ui_manager.window = window
ui_manager.init_action_menu()

@window.event
def on_draw():
    window.clear()
    # Reset the "eye" back to the default location.
    glLoadIdentity()
    # Move the "eye" to the current location on the map.
    # glTranslatef(delta[0], delta[1], 0.0)
    offset = int(-mech.x+(window.width/2)-(mech.frame_size[0]/2)), int(-mech.y+(window.height/2)-(mech.frame_size[1]/2))
    glTranslatef(offset[0], offset[1], 0.0)
    ui_manager.frame_offset = offset

    # TODO: [21:03]	thorbjorn: DR0ID_: You can generally determine the range of tiles that are visible before your drawing loop, which is much faster than looping over all tiles and checking whether it is visible for each of them.
    # [21:06]	DR0ID_: probably would have to rewrite the pyglet demo to use a similar render loop as you mentioned
    # [21:06]	thorbjorn: Yeah.
    # [21:06]	DR0ID_: I'll keep your suggestion in mind, thanks
    # [21:06]	thorbjorn: I haven't written a specific OpenGL renderer yet, so not sure what's the best approach for a tile map.
    # [21:07]	thorbjorn: Best to create a single texture with all your tiles, bind it, set up your vertex arrays and fill it with the coordinates of the tiles currently on the screen, and then let OpenGL draw the bunch.
    # [21:08]	DR0ID_: for each layer?
    # [21:08]	DR0ID_: yeah, probably a good approach
    # [21:09]	thorbjorn: Ideally for all layers at the same time, if you don't have to draw anything in between.
    # [21:09]	DR0ID_: well, the NPC and other dynamic things need to be drawn in between, right?
    # [21:09]	thorbjorn: Right, so maybe once for the bottom layers, then your complicated stuff, and then another time for the layers on top.

    game.tiles.draw()
    game.humans.draw()
    game.structures.draw()
    game.characters.draw()
    message_queue.draw()

    glLoadIdentity()
    glTranslatef(0, 0, 0.0)
    ui_manager.batch.draw()

keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)
resources = ResourceLoaderPyglet()
resources.load(world_map)


@window.event
def on_mouse_press(x, y, button, modifiers):
    ui_manager.on_mouse_press(x, y, button, modifiers)

@window.event
def on_mouse_motion(x, y, dx, dy):
    ui_manager.on_mouse_motion(x, y, dx, dy)


def update(dt):
    if keys[pyglet.window.key.A] and keys[pyglet.window.key.W]:
        mech.play('walk_nw')
    elif keys[pyglet.window.key.W] and keys[pyglet.window.key.D]:
        mech.play('walk_ne')
    elif keys[pyglet.window.key.S] and keys[pyglet.window.key.D]:
        mech.play('walk_se')
    elif keys[pyglet.window.key.A] and keys[pyglet.window.key.S]:
        mech.play('walk_sw')
    elif keys[pyglet.window.key.A]:
        mech.play('walk_w')
    elif keys[pyglet.window.key.W]:
        mech.play('walk_n')
    elif keys[pyglet.window.key.D]:
        mech.play('walk_e')
    elif keys[pyglet.window.key.S]:
        mech.play('walk_s')
    elif keys[pyglet.window.key.M]:
        try:
            bg_music.play()
        except NameError:
            pass
    elif keys[pyglet.window.key.T]:
        message_queue.create_message('Another Message!')
    else:
        mech.play('idle')

    game.update(dt)


def upkeep(dt):
    game.upkeep(dt)

game.to_update.add(ui_manager)


# manually instantiated entities
mech = Mech(x=50,y=1500, batch=game.characters)
game.to_update.add(mech)

for n in range(100):
    h = Human(x=360, y=1220, batch=game.humans)
    game.to_update.add(h)

message_queue = MessageHandler(x=50, y=1500)
game.to_update.add(message_queue)

#test message
message_queue.create_message("Omphalos 2217")

for group_num, layer in enumerate(world_map.layers):
    if not layer.visible:
        continue
    if layer.is_object_group:
        # This is unimplemented in this minimal-case example code.
        # Should you as a user of tmxreader need this layer,
        # I hope to have a separate demo using objects as well.
        continue
    group = pyglet.graphics.OrderedGroup(group_num)
    for ytile in range(layer.height):
        for xtile in range(layer.width):
            image_id = layer.content2D[xtile][ytile]
            if image_id:
                image_file = resources.indexed_tiles[image_id][2]
                # The loader needed to load the images upside-down to match
                # the tiles to their correct images. This reversal must be
                # done again to render the rows in the correct order.
                game.sprites.append(pyglet.sprite.Sprite(image_file,
                    world_map.tilewidth * xtile,
                    world_map.tileheight * (layer.height - ytile),
                    batch=game.tiles, group=group))


pyglet.clock.schedule_interval(update, frames_per_sec)
pyglet.clock.schedule_interval(upkeep, 5)
pyglet.app.run()
