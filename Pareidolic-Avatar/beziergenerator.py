from drawinghandler import *
from random import randint, uniform
from bezier import Bezier
import colorsys

class BezierLine(object):

    def __init__(self):
        self._poscurve = Bezier([],[])
        self._hcurve = Bezier([],[])
        self._scurve = Bezier([],[])
        self._vcurve = Bezier([],[])
        self._radcurve = Bezier([],[])

    def setPos(self, xs, ys):
        self._poscurve = Bezier(xs,ys)

    def setHSV(self, hs, ss, vs):
        self._hcurve = Bezier(hs,[0]*len(hs))
        self._scurve = Bezier(ss,[0]*len(ss))
        self._vcurve = Bezier(vs,[0]*len(vs))

    def setRad(self, rads):
        self._radcurve = Bezier(rads,[0]*len(rads))

    def getPos(self, t):
        return self._poscurve(t)

    def getHSV(self, t):
        return self._hcurve(t)[0],self._scurve(t)[0],self._vcurve(t)[0]

    def getRGB(self, t):
        val = colorsys.hsv_to_rgb(self._hcurve(t)[0],self._scurve(t)[0],self._vcurve(t)[0])
        val2 = []
        for i in range(len(val)):
            val2 += [val[i]*256]
        return tuple(val2)

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

    def copy(self):
        bz = BezierLine()
        bz._poscurve = self._poscurve.copy()
        bz._hcurve = self._hcurve.copy()
        bz._scurve = self._scurve.copy()
        bz._vcurve = self._vcurve.copy()
        bz._radcurve = self._radcurve.copy()
        return bz

    def randomize(self, positionmax, colormax, radiusmax):
        self._poscurve.randomjostle(positionmax)
        self._hcurve.randomjostle(colormax)
        self._scurve.randomjostle(colormax)
        self._vcurve.randomjostle(colormax)
        self._radcurve.randomjostle(radiusmax)

    def redistributePoints(self, n):
        self._poscurve.redistributePoints(n)
        self._hcurve.redistributePoints(n)
        self._scurve.redistributePoints(n)
        self._vcurve.redistributePoints(n)
        self._radcurve.redistributePoints(n)


def testbezier(filename):
    drw = Drawing()
    bl = BezierLine()
    bl.setPos([20,256-20],[20,256-20])
    bl.setHSV([0,1],[1,1],[1,1])
    bl.setRad([4,4])
    bl.redistributePoints(10)
    bl.randomize(10,.07,1)#
    bl.draw(drw)# See if smoothness improves rainbow blending.
    
    #for i in range(10):
    #    bl2 = bl.copy()
    #    bl2._poscurve.shift(20*i,0)
    #    bl2.randomize(10,.07,1)
    #    bl2.draw(drw) # bl2 is changing bl. Look over bezier copy
    drw.toImage('./tests/bezier/'+filename+'.png',False)


testbezier(str(0))
