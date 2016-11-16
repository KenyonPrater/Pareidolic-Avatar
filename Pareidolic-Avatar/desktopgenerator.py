from drawinghandler import *
from random import randint, uniform, seed
from bezier import Bezier
import colorsys
from math import sin, cos, radians
from PIL import Image
import subprocess
import os

class BezierLine(object):

    def __init__(self):
        self._poscurve = Bezier([],[])
        self._hcurve = Bezier([],[])
        self._scurve = Bezier([],[])
        self._vcurve = Bezier([],[])
        self._radcurve = Bezier([],[])
        self._alphacurve = Bezier([],[])

    def setPos(self, xs, ys):
        self._poscurve = Bezier(xs,ys)

    def setHSV(self, hs, ss, vs):
        self._hcurve = Bezier(hs,[0]*len(hs))
        self._scurve = Bezier(ss,[0]*len(ss))
        self._vcurve = Bezier(vs,[0]*len(vs))

    def setRad(self, rads):
        self._radcurve = Bezier(rads,[0]*len(rads))

    def setAlpha(self, alpha):
        self._alphacurve = Bezier(alpha,[0]*len(alpha))

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

    def getAlpha(self, t):
        return self._alphacurve(t)[0]

    def draw(self, drw, mirror=True):
        time = 0
        dt = .005
        xold,yold = self.getPos(time)
        x,y = self.getPos(time +dt)
        ds = ((x-xold)**2 + (y-yold)**2)**.5
        rad = self.getRad(0)
        time += dt
        while time < 1:
            x,y = self.getPos(time)
            alpha = self.getAlpha(time)
            ds = ((x-xold)**2 + (y-yold)**2)**.5
            rad = self.getRad(0)
            r,g,b = self.getRGB(time)
            drw.brush(x,y, r,g,b, rad, ds,alpha)
            if mirror:
                drw.brush(drw.getWidth()-x, y, r,g,b,rad, ds, alpha)

            time += dt
            xold, yold = x, y

    def copy(self):
        bz = BezierLine()
        bz._poscurve = self._poscurve.copy()
        bz._hcurve = self._hcurve.copy()
        bz._scurve = self._scurve.copy()
        bz._vcurve = self._vcurve.copy()
        bz._radcurve = self._radcurve.copy()
        bz._alphacurve = self._alphacurve.copy()
        return bz

    def randomize(self, positionmax=0, colormax=0, radiusmax=0,alphamax=0):
        self._poscurve.randomjostle(positionmax)
        self._hcurve.randomjostle(colormax)
        self._scurve.randomjostle(colormax)
        self._vcurve.randomjostle(colormax)
        self._radcurve.randomjostle(radiusmax)
        self._alphacurve.randomjostle(alphamax)

    def redistributePoints(self, n):
        self._poscurve.redistributePoints(n)
        self._hcurve.redistributePoints(n)
        self._scurve.redistributePoints(n)
        self._vcurve.redistributePoints(n)
        self._radcurve.redistributePoints(n)
        self._alphacurve.redistributePoints(n)

def generateDominantBezier(hsvDominant, linkNum = 7, linkdist = 200, linkAngle = 180, radius = 5, hsvChange = .1, radiusChange = 1):
    bl = BezierLine()
    bl.setPos([0,0],[0,0])
    bl.setHSV([hsvDominant[0]+uniform(-hsvChange,hsvChange),hsvDominant[0]+uniform(-hsvChange,hsvChange)],[hsvDominant[1]+uniform(-hsvChange,hsvChange),hsvDominant[1]+uniform(-hsvChange,hsvChange)],[hsvDominant[2]+uniform(-hsvChange,hsvChange),hsvDominant[2]+uniform(-hsvChange,hsvChange)])
    bl.setRad([radius+uniform(-radiusChange, radiusChange),radius+uniform(-radiusChange, radiusChange)]*5)
    bl.setAlpha([0,1,1,1,1,1,0])
    bl.redistributePoints(linkNum)
    bl.randomize(0,hsvChange,radiusChange)
    xs = []
    ys = []
    x = uniform(10,245)
    y = uniform(10,245)
    theta = uniform(0,360)
    for i in range(linkNum):
        xs += [x]
        ys += [y]

        dist = uniform(0, linkdist)
        x += cos(radians(theta))*dist
        y += sin(radians(theta))*dist
        y = min(245, max(10,y))
        x = min(245, max(10,x))
        theta += uniform(-linkAngle, linkAngle)
    bl.setPos(xs, ys)
    return bl

def generateAccentBezier(hsvAccent, linkNum = 3, linkdist = 100, linkAngle = 180, radius = 2, hsvChange = .1, radiusChange = .5):
    bl = BezierLine()
    bl.setPos([0,0],[0,0])
    bl.setHSV([hsvAccent[0]+uniform(-hsvChange,hsvChange),hsvAccent[0]+uniform(-hsvChange,hsvChange)],[hsvAccent[1]+uniform(-hsvChange,hsvChange),hsvAccent[1]+uniform(-hsvChange,hsvChange)],[hsvAccent[2]+uniform(-hsvChange,hsvChange),hsvAccent[2]+uniform(-hsvChange,hsvChange)])
    bl.setRad([radius+uniform(-radiusChange, radiusChange),radius+uniform(-radiusChange, radiusChange)]*5)
    bl.setAlpha([0,1,1,1,1,1,0])
    bl.redistributePoints(linkNum)
    bl.randomize(0,hsvChange,radiusChange)
    xs = []
    ys = []
    x = uniform(10,245)
    y = uniform(10,245)
    theta = uniform(0,360)
    for i in range(linkNum):
        xs += [x]
        ys += [y]

        dist = uniform(0, linkdist)
        x += cos(radians(theta))*dist
        y += sin(radians(theta))*dist
        y = min(245, max(10,y))
        x = min(245, max(10,x))
        theta += uniform(-linkAngle, linkAngle)
    bl.setPos(xs, ys)
    return bl

def testbezier(filename):
    drw = Drawing()
    bl = BezierLine()
    bl.setPos([20,256-20],[20,256-20])
    bl.setHSV([0,1],[1,1],[1,1])
    bl.setRad([4,4])
    bl.redistributePoints(10)
    bl.randomize(10,.07,1)#
    bl.draw(drw)

    #for i in range(10):
    #    bl2 = bl.copy()
    #    bl2._poscurve.shift(20*i,0)
    #    bl2.randomize(10,.07,1)
    #    bl2.draw(drw) # bl2 is changing bl. Look over bezier copy
    drw.toImage('./tests/bezier/'+filename+'.png',False)

def tint(image, rgb):
    R,G,B = uniform(0,1), uniform(0,1), uniform(0,1)
    for i in range(image.width):
        for j in range(image.height):
            r,g,b = image.getpixel((i, j))
            image.putpixel((i,j), (int(r*R), int(g*G), int(b*B)))

def testRandom():
    drw = Drawing()
    h,s,v = uniform(0,1), uniform(0,1), uniform(.3,.9)
    for i in range(3):
        bl = generateDominantBezier((h,s,v))
        bl.draw(drw)
    h,s,v = uniform(0,1), uniform(0,1), uniform(.3,.9)
    for i in range(3):
        bl = generateAccentBezier((h,s,v))
        bl.draw(drw)
    im = drw.toImage()
    desktop = Image.open("./tests/desktop/background.png")
    color = colorsys.hsv_to_rgb(uniform(0,1), uniform(0,1), uniform(0,1))
    tint(desktop, color)
    desktop.paste(im, ((1920/2 - 256/2), (1080/2 - 256/2)))
    desktop.save("./tests/desktop/background1.png")
    subprocess.call(["dconf", "write", "/org/gnome/desktop/background/picture-uri", "'file://"+ (os.path.dirname(os.path.abspath(__file__))) +"/tests/desktop/background1.png'"])

testRandom()
