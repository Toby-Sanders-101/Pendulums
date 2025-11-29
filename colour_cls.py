#from typing import Self, List
import random
from vectors import *
        
#all_colours = []

class Colour:
    def __init__(self, r=-1, g=-1, b=-1, alpha=1):
#        count = 0
#        flag = True

        if r == -1 and g == -1 and b == -1:
            t = (Vector3(random.random(), random.random(), random.random()).norm*256).tuple
            self.r, self.g, self.b = int(t[0]), int(t[1]), int(t[2])
            self.alpha = alpha
        else:
            if r > 255:
                r = 255
            if r < 0:
                r = 0
            self.r = int(r)

            if g > 255:
                g = 255
            if g < 0:
                g = 0
            self.g = int(g)

            if b > 255:
                b = 255
            if b < 0:
                b = 0
            self.b = int(b)

            if alpha > 1:
                alpha = 1
            if alpha < 0:
                alpha = 0
            self.alpha = alpha

#        while flag and count < 20:
#            if count>0:
#                t = (Vector3(random.random(), random.random(), random.random()).norm*256).tuple
#                self.r, self.g, self.b = int(t[0]), int(t[1]), int(t[2])
#                self.alpha = alpha

#            flag = False
#            for colour in all_colours:
#                if self.compare_colour(colour):
#                    flag = True
#                    #print(f"flagged: {self.tuple}, {colour.tuple}")
            
#            count += 1

        #all_colours.append(self)
    
    @property
    def tuple(self) -> tuple:
        return (self.r, self.g, self.b)

    @property
    def asVector3(self) -> Vector3:
        return Vector3(self.r, self.g, self.b)

#    def compare_colour(self, other: Self) -> bool:
#        return (self.asVector3-other.asVector3).mag < 60

#all_colours = [Colour(0,0,0), Colour(255,255,255), Colour(127,127,127)]