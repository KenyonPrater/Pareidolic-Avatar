from drawinghandler import *
from random import randint, uniform
from bezier import Bezier

class BezierLine(object):

    def __init__(self):
        self._poscurve = Bezier([],[])
        self._rcurve = Bezier([],[])
        self._gcurve = Bezier([],[])
        self._bcurve = Bezier([],[])
        self._radcurve = Bezier([],[])

    def setPos(self, xs, ys):
        self._poscurve = Bezier(xs,ys)

    def setRGB(self, rs, gs, bs):
        self._rcurve = Bezier(rs,[0]*len(rs))
        self._gcurve = Bezier(gs,[0]*len(gs))
        self._bcurve = Bezier(bs,[0]*len(bs))

    def setRad(self, rads):
        self._radcurve = Bezier(rads,[0]*len(rads))

    def getPos(self, t):
        return self._poscurve(t)

    def getRGB(self, t):
        return self._rcurve(t)[0],self._gcurve(t)[0],self._bcurve(t)[0]

    def getRad(self, t):
        return self._radcurve(t)[0]

    def draw(self, drw, mirror=True):
        time = 0
        dt = .01
        xold,yold = self.getPos(time)
        x,y = self.getPos(time +dt)
        speed = ((x-xold)**2 + (y-yold)**2)**.5
        rad = self.getRad(0)
        dt = (rad*dt)/(2*speed)
        time += dt
        while time < 1:
            x,y = self.getPos(time)
            speed = (x-xold)**2 + (y-yold)**2
            rad = self.getRad(0)
            r,g,b = self.getRGB(time)
            drw.brush(x,y, r,g,b, rad, speed)
            if mirror:
                drw.brush(drw.getWidth()-x, y, r,g,b,rad, speed)
            
            dt = (rad/2)/speed *dt
            time += dt
            xold, yold = x, y


def testbezier(filename):
    drw = Drawing()
    bl = BezierLine()
    bl.setPos([50,200],[50,200])
    bl.setRGB([255,255],[0,255],[255,0])
    bl.setRad([4,4])
    bl._poscurve.redistributePoints(21)
    
   # bl.draw(drw)
    bl._poscurve.shift(0,20)
    bl._poscurve.randomjostle(20)
    bl.draw(drw)
    drw.toImage('./tests/bezier/'+filename+'.png',False)

testbezier('0')
