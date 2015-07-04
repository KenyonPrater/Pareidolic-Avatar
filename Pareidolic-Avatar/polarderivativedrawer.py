from drawinghandler import *
from random import randint, uniform
from math import sin, cos, radians

class DerivativeTurtle:
    def __init__(self, x=0, y=0, rot=0, vel=0, drot=0, r=256,g=256,b=256,dr=0,dg=0,db=0,radius=3):
        self._x = x
        self._y = y
        self._rot = rot
        self._vel = vel
        self._drot = 0
        self._r = r
        self._g = g
        self._b = b
        self._dr = dr
        self._dg = dg
        self._db = db
        self._radius = radius

    def randomize(self):
        self._x = uniform(0,255)
        self._y = uniform(0,255)
        self._rot = uniform(0,360)
        self._drot = uniform(-10,10)
        self._vel = uniform(-8,8)
        self._r = randint(0,256)
        self._g = randint(0,256)
        self._b = randint(0,256)
        while (self._r+self._g+self._b < 120): #Dark colors are kinda boring
            print ('rejected color for borrringg')
            self._r = randint(0,256)
            self._g = randint(0,256)
            self._b = randint(0,256)
        self._dr = randint(-5,5)
        self._dg = randint(-5,5)
        self._db = randint(-5,5)
        self._radius = uniform(2,5)

    def move(self,time = 1.0):
        self._x += (self._vel * cos(radians(self._rot)))*time
        self._y += (self._vel * sin(radians(self._rot)))*time
        self._rot += (self._drot)*time
        self._r += (self._dr)*time
        self._r = min(255,max(0,self._r)) #clamp to 0-255
        self._g += (self._dg)*time
        self._g = min(255,max(0,self._g))
        self._b += (self._db)*time
        self._b = min(255,max(0,self._b))

    def randomwalk(self, time = 1.0):
        self._drot += (uniform(-1,1))*time
        self._vel += (uniform(-1,1))*time
        self._radius += (uniform(-.1,.1))*time
        self._dr += (uniform(-1,1))*time
        self._dg += (uniform(-1,1))*time
        self._db += (uniform(-1,1))*time
        

    def draw(self, drw, time=1.0, mirror=True):
        drw.brush(self._x,self._y, int(self._r),int(self._g),int(self._b),self._radius, abs(time*self._vel))
        if mirror:
            drw.brush(self._x,drw.getWidth() - self._y, int(self._r),int(self._g),int(self._b),self._radius, abs(time*self._vel))

def createColorSchemeParidolia(filename):
    drw = Drawing()
    dominantColor = [randint(0,255),randint(0,255),randint(0,255)]
    highlight = [randint(0,255),randint(0,255),randint(0,255)]
    for i in range(randint(7,10)):
        turt = DerivativeTurtle()
        turt.randomize()
        turt._r = dominantColor[0] + randint(-20,20)
        turt._g = dominantColor[1] + randint(-20,20)
        turt._b = dominantColor[1] + randint(-20,20)
        lifetime = randint(15,50)
        for t  in range(lifetime):
            for sub in range(4):
                turt.move(.25)
                turt.randomwalk(.25)
                turt.draw(drw,.25)
    for i in range(randint(1,3)):
        turt = DerivativeTurtle()
        turt.randomize()
        turt._r = highlight[0] + randint(-20,20)
        turt._g = highlight[1] + randint(-20,20)
        turt._b = highlight[1] + randint(-20,20)
        lifetime = randint(10,30)
        for t  in range(lifetime):
            for sub in range(4):
                turt.move(.25)
                turt.randomwalk(.25)
                turt.draw(drw,.25)
    drw.toImage('./tests/polarderivativeturtle/'+filename+'.png',False)

for i in range(5):
    createColorSchemeParidolia('derivativetest-'+str(i))
