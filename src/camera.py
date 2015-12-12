'''
Created on Feb 28, 2010
@author: Bryan
'''

class Camera:
    def __init__(self,width, height, offset=(0,0), tile_size=16):
        self.width = width
        self.height = height
        self.offset = offset
        self.tile_size = tile_size

        self.grid_width = self.width / self.tile_size
        self.grid_height = self.height / self.tile_size

    def get_visible_range(self):
        start_x = self.offset[0]/self.tile_size
        start_y = self.offset[1]/self.tile_size
        end_x = self.grid_width + start_x
        end_y = self.grid_height + start_y
        return int(start_x-1), int(start_y-1), int(end_x+1), int(end_y+1)

    def grid_to_px(self, x, y):
        return x*self.tile_size-self.offset[0], y*self.tile_size-self.offset[1]

    def translate(self,x,y):
        return x-self.offset[0], y-self.offset[1]

    def reverse_translate(self,x,y):
        return x+self.offset[0], y+self.offset[1]

    def update(self,x,y):
        # if this point is inside the bounding rectangle, don't move
        xs,ys = self.translate(x, y)
        dx = 0
        dy = 0
        if xs > (self.width - self.threshold[0]):
            dx = xs -(self.width - self.threshold[0])
        elif xs < self.threshold[0]:
            dx = xs - self.threshold[0]
        if ys > (self.height - self.threshold[1]):
            dy = ys -(self.height - self.threshold[1])
        elif ys < self.threshold[1]:
            dy = ys - self.threshold[1]


        self.goto(self.offset[0]+dx, self.offset[1]+dy)

    def move(self, x,y):
        self.changed = True
        ox,oy = self.offset
        ox += x
        oy += y
        self.offset = (ox, oy)


    def goto(self, x,y):
        self.offset = (x,y)
