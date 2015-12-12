import pyglet
from tiledtmxloader import tmxreader
from tiledtmxloader.helperspyglet import ResourceLoaderPyglet
from pyglet.gl import glTranslatef, glLoadIdentity
from characters.mech import Mech

MAP_FILE = "maps/test2.tmx"

# Sounds
pyglet.options['audio'] = ('openal', 'silent')
bg_music = pyglet.media.load('assets/sound/bg_music.mp3', streaming=False)

world_map = tmxreader.TileMapParser().parse_decode(MAP_FILE)

# delta is the x/y position of the map view.
# delta is a list so that it can be accessed from the on_draw method of
# window and the update function. Note that the position is in integers to
# match Pyglet Sprites. Using floating-point numbers causes graphical
# problems. See http://groups.google.com/group/pyglet-users/browse_thread/thread/52f9ae1ef7b0c8fa?pli=1
delta = [200, -world_map.pixel_height+150]
frames_per_sec = 1.0 / 30.0
window = pyglet.window.Window()

@window.event
def on_draw():
    window.clear()
    # Reset the "eye" back to the default location.
    glLoadIdentity()
    # Move the "eye" to the current location on the map.
    # glTranslatef(delta[0], delta[1], 0.0)
    glTranslatef(int(-mech.x+(window.width/2)), int(-mech.y+(window.height/2)), 0.0)

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

    batch.draw()
    characters.draw()

keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)
resources = ResourceLoaderPyglet()
resources.load(world_map)


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
        bg_music.play()
    else:
        mech.play('idle')

    for obj in to_update:
        obj.update(dt)

# Generate the graphics for every visible tile.
batch = pyglet.graphics.Batch()
sprites = []
characters = pyglet.graphics.Batch()
to_update = set()

mech = Mech(x=50,y=1500, batch=characters)
to_update.add(mech)


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
                sprites.append(pyglet.sprite.Sprite(image_file,
                    world_map.tilewidth * xtile,
                    world_map.tileheight * (layer.height - ytile),
                    batch=batch, group=group))




pyglet.clock.schedule_interval(update, frames_per_sec)
pyglet.app.run()