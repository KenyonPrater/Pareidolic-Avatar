import PIL.Image as Image

class Pixel():
    def __init__(self, r=0,g=0,b=0):
        self._r = r
        self._g = g
        self._b = b

    def setRGB(self,r,g,b):
        self._r = int(r)
        self._g = int(g)
        self._b = int(b)

    def getRGB(self,):
        return self._r,self._g,self._b

    def setR(self,r):
        self._r = int(r)

    def setG(self,g):
        self._g = int(g)

    def setB(self,b):
        self._b = int(b)

    def getR(self):
        return self._r

    def getG(self):
        return self._g

    def getB(self):
        return self._b

    def mixColor(self,r,g,b,a):
        """Weighted average of this pixel and the passed values."""
        af = a/256.0
        self._r = int(self._r * (1-af) + r*af)
        self._g = int(self._g * (1-af) + g*af)
        self._b = int(self._b * (1-af) + b*af)
        
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "pix(" + str(self._r)+ ','+str(self._g)+','+ str(self._b)+')'

class Drawing():
    def __init__(self,height = 256, width = 256):
        self._height = height
        self._width = width
        self._data = []
        for i in range(height):
            dat = []
            for j in range(width):
                dat += [Pixel()]
            self._data += [dat]

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height

    def toImage(self,filename = None, show=False):
        img = Image.new('RGB',(self._width, self._height))
        for i in range(self._height):
            for j in range(self._width):
                img.putpixel((i,j),self._data[i][j].getRGB())
        if show:
            img.show()
        if filename != None:
            img.save(filename)
        return img

    def brush(self,x,y,r,g,b,radius = 3,speed=1,alpha=1.0):
        for i in range(int(y-radius-1), int(y+radius+2)):
            for j in range(int(x-radius-1), int(x+radius+2)):
                if 0<=i<self._height and  0<=j<self._width:
                    weight = 256*alpha*(1-((i-y)**2 + (j-x)**2)/radius**2)*speed/radius
                    weight = min(weight, 255)
                    if weight > 0:
                        self._data[int(j)][int(i)].mixColor(r,g,b,weight)
