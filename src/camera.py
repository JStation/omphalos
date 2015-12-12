'''
Created on Feb 28, 2010
@author: Bryan
'''

class Camera:
    def __init__(self,width, height, offset=(0,0), threshold=(150,20)):
        self.width = width
        self.height = height
        self.offset = offset
        self.threshold = threshold

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


        self.move(self.offset[0]+dx, self.offset[1]+dy)

    def move(self, x,y):
        self.offset = (x,y)
