from drawinghandler import *
from random import randint, uniform

class Turtle:
    def __init__(self, x=0, y=0, dx=0, dy=0, r=256,g=256,b=256,radius=3):
        self._x = x
        self._y = y
        self._dx = dx
        self._dy = dy
        self._r = r
        self._g = g
        self._b = b
        self._radius = radius

    def randomize(self):
        self._x = uniform(0,255)
        self._y = uniform(0,255)
        self._dx = uniform(-1,1)
        self._dy = uniform(-1,1)
        self._r = randint(0,256)
        self._g = randint(0,256)
        self._b = randint(0,256)
        self._radius = uniform(2,5)

    def move(self):
        self._x += self._dx
        self._y += self._dy

    def randomwalk(self):
        self._dx += uniform(-.1,.1)
        self._dy += uniform(-.1,.1)
        self._radius += uniform(-.1,.1)
        self._r += randint(-10,10)
        self._r = min(255,max(0,self._r)) #clamp to 0-255
        self._g += randint(-10,10)
        self._g = min(255,max(0,self._g))
        self._b += randint(-10,10)
        self._b = min(255,max(0,self._b))

    def draw(self, drw, mirror=True):
        speed = (self._dx **2 + self._dy **2)**.5
        drw.brush(self._x,self._y, self._r,self._g,self._b,self._radius, speed)
        if mirror:
            drw.brush(self._x,drw.getWidth() - self._y, self._r,self._g,self._b,self._radius, speed)

def createTurtleParidolia(filename):
    drw = Drawing()
    for i in range(randint(5,10)):
        turt = Turtle()
        turt.randomize()
        lifetime = randint(30,100)
        for t  in range(lifetime):
            turt.move()
            turt.randomwalk()
            turt.draw(drw)
    drw.toImage('./tests/basicturtle/'+filename+'.png',True)

for i in range(10):
    createTurtleParidolia('basictest-'+str(i))
