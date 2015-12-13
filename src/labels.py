from game import game
from pyglet import font
font.add_directory('assets/fonts/')
mini57 = font.load('Minimal5x7', 18)




class resourceLabel(font.Text):

    def __init__(self, asset_name, *args, **kwargs):
        self.asset = game.get_asset(asset_name)
        super(resourceLabel, self).__init__(font=mini57, *args, **kwargs)

    def draw(self):
        self._set_text(game.player.get_asset(self.asset.asset_id).quantity)
        super(resourceLabel, self).draw()





if __name__ == '__main__':

    import pyglet
    win = pyglet.window.Window(width=640, height=480)

    powerLabel = resourceLabel('power', text='test')

    @win.event
    def on_update(dt):
        powerLabel.update(dt)

    @win.event
    def on_draw():
        win.clear()
        powerLabel.draw()


    @win.event()
    def on_key_press(symbol, modifiers):
        powerLabel._set_text(str(symbol))

    pyglet.app.run()

