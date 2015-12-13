from pyglet import font
font.add_directory('assets/fonts/')
mini57 = font.load('Minimal5x7', 18)

class MessageHandler:
    """
    Container for display messages
    """
    def __init__(self, x=0, y=0):
        self.messages = []
        self.x = x
        self.y = y

    def create_message(self, text, *args, **kwargs):
        """
        text: text to display
        timer: length of time to display (optional, has default)
        """
        m = Message(text, x=self.x, y=self.y, *args, **kwargs)
        self.add_message(m)

    def add_message(self, msg):
        self.messages.append(msg)
        #pyglet.clock.schedule_once(self.del_message(msg), msg.timer)

    def del_message(self, msg):
        self.messages.remove(msg)

    def update(self, dt):
        for msg in self.messages[:]:
            msg.update(dt)
            if msg.expired:
                self.messages.remove(msg)

    def draw(self):
        offset = 0
        for msg in self.messages:
            msg.draw(y=offset)
            offset += 13




class Message(font.Text):
    """
    Displays a message for a specified duration
    """
    DEFAULT_TIME_TO_DISPLAY = 5.0

    def __init__(self, text, timer=DEFAULT_TIME_TO_DISPLAY, *args, **kwargs):
        self.timer = timer
        self.expired = False
        super(Message, self).__init__(font=mini57, text=text, *args, **kwargs)

    def update(self, dt):
        self.timer = self.timer - dt
        self.check_timer()

    def draw(self, x=None, y=None):
        "x and y are optional offsets"
        old_coords = self.x, self.y
        if x:
            self.x += x
        if y:
            self.y += y
        super(Message, self).draw()
        self.x, self.y = old_coords

    def set_text(self, text):
        self._set_text(str(text))

    def check_timer(self):
        if self.timer < 0:
            self.expired = True





if __name__ == '__main__':

    import pyglet
    win = pyglet.window.Window(width=640, height=480)
    clock = pyglet.clock.Clock()

    queue = MessageHandler()
    msg = Message('text!', 5)
    queue.add_message(msg)


    @win.event
    def on_update(dt):
        queue.update(dt)

    @win.event
    def on_draw():
        win.clear()
        queue.draw()


    @win.event()
    def on_key_press(symbol, modifiers):
        #m = Message(str(symbol))
        queue.create_message(str(symbol), 1)

    pyglet.clock.schedule_interval(queue.update, .2)
    pyglet.app.run()

