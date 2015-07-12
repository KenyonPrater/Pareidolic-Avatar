from math import factorial
from random import uniform

#Based off pycurve, https://code.google.com/p/pycurve/,
#By Chandler Armstrong (omnirizon)
#Modified to work in 3.4 by Kenyon Prater

def _C(n, k):
    # binomial coefficient == n! / (i!(n - i)!)
    return factorial(n) / (factorial(k) * factorial(n - k))

class Bezier(object):

    def __init__(self, xs,ys):
        """
        construct bezier curve

        P == list of control points
        """
        self.X = xs
        self.Y = ys
        self._n = range(len(xs)) # control point iterator

    def copy(self):
        return Bezier(self.X, self.Y)

    def redistributePoints(self, n):
        xs = []
        ys = []
        for i in range(n):
           xs += [self(i*1.0/(n-1))[0]]
           ys += [self(i*1.0/(n-1))[1]]
        self.X = xs
        self.Y = ys
        self._n = range(len(xs))

    def randomjostle(self, maxrandom):
        for i in self._n:
            self.X[i] = self.X[i]+uniform(-maxrandom, maxrandom)
            self.Y[i] = self.Y[i]+uniform(-maxrandom, maxrandom)

    def shift(self,dx, dy):
        """shift entire bezier curve in a direction"""
        for i in self._n:
            self.X[i] = self.X[i]+dx
            self.Y[i] = self.Y[i]+dy



    def __call__(self, t):
        """
        domain t in [0, 1]

        return point on bezier curve at t
        """
        assert 0 <= t <= 1 # t in [0, 1]
        X, Y, _n = self.X, self.Y, self._n
        x, y, n = 0, 0, _n[-1] # initial x, y return values and n
        for i in _n:
            b_i = _C(n,i) * t**i * (1 - t)**(n - i) # bernstein polynomial
            # mult ith control point by ith bernsteim polynomial
            # t = 0 maps to first control point
            # t = 1 maps to nth control point
            x += X[i] * b_i
            y += Y[i] * b_i
        return x, y

