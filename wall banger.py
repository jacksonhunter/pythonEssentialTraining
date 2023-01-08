import os
import time
import cmath
import math
from termcolor import colored
import re
import numpy
#from collections import defaultdict
#from random import sample


# This is the Canvas class. It defines some height and width, and a 
# matrix of characters to keep track of where the TerminalScribes are moving
class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        self._t = 0

        # This is a grid that contains data about where the 
        # TerminalScribes have visited
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]
        #self._crystal = [[[' ' for y in range(self._y)] for x in range(self._x)] for t in range(1000)]
        self._crystal = numpy.full((500,self._x, self._y), " ")

    # Returns True if the given point is outside the boundaries of the Canvas
    def hitsWall(self, point):

        normal = (1+1e-16j if point[0] < 0 else -1+1e-16j if point[0] >= self._x else 1e-16-1j if point[1] < 0 else 1e-16+1j if point[1] >= self._y else False)

        return normal

    # Set the given position to the provided character on the canvas
    def setPos(self, pos, mark):
        if not self.hitsWall(pos):
            self._canvas[pos[0]][pos[1]] = mark
            self._crystal[self._t::, pos[0], pos[1]]= mark
            #self._crystal[self._t][pos[0]][pos[1]] = mark
            self._t+=1
        # Clear the terminal (used to create animation)
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # Clear the terminal and then print each line in the canvas
    def print(self):
        self.clear()
        for y in range(self._y):
            print(' '.join([self._canvas[x][y] for x in range(self._x)]))

    def animate(self):
        for t in range(0, 500):
            self.clear()
            for y in range(self._y):
                print(' '.join([self._crystal[t, x, y] for x in range(self._x)]))
            time.sleep(0.2)



    def resetCrystal(self):
        self._t = 0


class TerminalScribe:
    def __init__(self, canvas):

        self.pos = [0,0]
        self.canvas=canvas
        self.mark = "*"
        self.framerate = 0.2
        self.phi = math.degrees(0)

    def jump(self, pos):
        self.canvas.setPos(self.pos, " ")
        self.pos = pos
        self.canvas.setPos(pos, self.mark) #colored(self.mark, "green"))
        self.canvas.print()
        time.sleep(self.framerate)



    def up(self, trail="."):
        pos = [self.pos[0], self.pos[1]-1]
        if not self.canvas.hitsWall(pos):
            self.draw(pos, trail)
    def down(self, trail="."):
        pos = [self.pos[0], self.pos[1]+1]
        if not self.canvas.hitsWall(pos):
            self.draw(pos, trail)

    def right(self, trail=".", color="default"):
        pos = [self.pos[0]+1, self.pos[1]]
        if not self.canvas.hitsWall(pos):
            self.draw(pos, trail, color)

    def left(self, trail="."):
        pos = [self.pos[0]-1, self.pos[1]]
        if not self.canvas.hitsWall(pos):
            self.draw(pos, trail)

    def distance(self, posi, posf):
        return(int(round(math.dist(posi, posf))))

    def draw(self, pos, trail='.', mark='*', framerate=0.2, color='red'):
        self.trail = trail

        # Set the old position to the "trail" symbol
        self.canvas.setPos(self.pos, self.trail)
        # Update position
        self.pos = pos
        # Set the new position to the "mark" symbol
        self.canvas.setPos(self.pos, mark)#colored(self.mark, color))
        # Print everything to the screen
        self.canvas.print()
        # Sleep for a little bit to create the animation
        time.sleep(self.framerate)

    def drawSquare(self, size):
        for i in range(0, 5):
            self.right( " ")
        for i in range(0, size):
            self.right()
            self.right(" ")
        for i in range(0, size):
            self.down()
        for i in range(0, size):
            self.left()
            self.left(" ")
        for i in range(0, size):
            self.up()
    def drawTriangle(self, size):
        half = int(size/2+1)
        for i in range(0, half):
            self.right(" ")
        for i in range(0, half-1):
            self.down()
            self.right(" ")
        for i in range(0, size+1):
            self.left()
        for i in range(0, half):
            self.right(" ")
            self.up()

    def forward(self, phi=None, trail="."):
        if type(phi)==str:
            trail=phi
            phi=None
        if phi == None:
            phi = self.phi
        self.phi = phi
        unit = cmath.rect(1, math.radians(self.phi) )
        init=self.pos2c()
        points = []
        i=1
        while len(points) <= len(trail):
            p = init + i * unit
            if self.canvas.hitsWall(self.c2pos(p)):
                n=self.c2v((self.canvas.hitsWall(self.c2pos(p))))
                d=self.c2v(unit)
                ra=d-2*numpy.dot(d,n)*n
                r=self.v2c(ra)
                p= init +i * unit + r
                init = round(p,0)
                unit = r
                self.phi = math.degrees(cmath.polar(r)[1])
                i=0
            if not p in points:
                points.append(p)
            i += 1
        points = [ self.c2pos(i) for i in points]
        draw = [self.draw(points[i], trail[i]) for i in range(0, len(trail))]

    def pfwd(self, r, phi, trail="."):
        if phi == None:
            phi = self.phi
        self.phi = phi
        complex=cmath.rect(r, math.radians(self.phi))
        unit = cmath.rect(1, math.radians(self.phi) )
        init = self.pos2c(self.pos)
        points = [self.c2pos(init + i*unit) for i in range(0, int(round(r,0)))]
        draw = [self.draw(i, trail) for i in points if not self.canvas.hitsWall(i)]

    def cfwd(self, complex, trail="."):
        polar=cmath.polar(complex)
        self.pfwd(polar[0], math.degrees(polar[1]), trail)
    def c2pos(self, complex=0+0j):
        return [int(numpy.round(complex.real,0)), int(numpy.round(-complex.imag, 0))]
    def pos2c(self, pos=None):
        if pos == None:
            pos=self.pos
        return pos[0]-pos[1]*1j
    def c2v(self,c):
        return numpy.asarray([c.real, c.imag])
    def v2c(self,a):
        return a[0]+a[1]*1j
    def runForward(self, n, phi=None, trail="."):
        if phi == None:
            phi = self.phi
        self.phi = phi
        self.forward(trail=trail*n)
canvas = Canvas(61, 30)
scribes = [
    { "name" : "sinScribe", "position" : [0,15], "trail" : "~", "color" : "green", "speed" : 0.02, "draw":  lambda : [int(round(math.sin(math.radians(i))*10, 0)) for i in range(0,360*5,18)],},
    { "name" : "circleScribe", "position" : [34,22], "trail" : "o", "color" : "blue", "speed" : 0.02, "forward" : lambda : [(i) for i in range(0, 360*4,18)],},
    { "name" : "parseScribe", "position" : [0,0], "color" : "orange", "speed" : 0.02, "parse" : "300abcdefghijklmno330pqrs0tuv30wxyzABCDEFG60HIJKLMN90OPQ45RSTUVWXYZ330zyxwv",}
    ]
for dic in scribes:
    dic['scribe'] = TerminalScribe(canvas)
    dic['scribe'].jump(dic['position'])
    dic['scribe'].framerate=dic["speed"]
    if "draw" in dic.keys():
        draw = [dic['scribe'].draw([i+dic['position'][0], dic['position'][1]+dic["draw"]()[i]], dic["trail"]) for i in range (0, len(dic["draw"]())) if not dic['scribe'].canvas.hitsWall([i+dic['position'][0], dic['position'][1]+dic["draw"]()[i]])]
        canvas.resetCrystal()
    if "forward" in dic.keys():
        print([dic["forward"]()[i] for i in range(0, len(dic["forward"]()))])
        forward = [dic["scribe"].forward(dic["forward"]()[i], trail=dic["trail"]) for i in range(0, len(dic["forward"]()))]
        canvas.resetCrystal()
    if "parse" in dic.keys():
        for i in re.split(r"(\d+)", dic["parse"]):
            if i.isnumeric():
                dic["scribe"].phi = float(i)
            else:
                parse = [dic["scribe"].forward(trail=i)]
        canvas.resetCrystal()

#canvas.animate()

scribe = TerminalScribe(canvas)
scribe.framerate=0.02
#scribe.forward(-45, trail="..............................................................................................")
#scribe.jump([16,3])
#scribe.forward(45,"..............................................................................................")
#scribe.runForward(240, 20)
#scribe.forward("*"*70)
#split = re.split(r"(\d+)", 'foofo21gar-15')
#print(split)


#sinScribe = TerminalScribe(canvas)
# circleScribe = TerminalScribe(canvas)
#sinScribe.framerate=0.2
# circleScribe.framerate=0.001
#
#
# degrees = list(range(0,360*5))
# #print(degrees)
#sin = [math.sin(math.radians(i)) for i in range(0,360*5,18)]
# #print(sin)
# #circleScribe.jump([24,12])
# #circlescribe = [circleScribe.forward(i) for i in degrees[::18]*10]
# #sinScribe.jump([0,15])
#test2 = [sinScribe.draw([i, 15+int(round([math.sin(math.radians(i)) for i in range(0,360*5,18)][i] * 10, 0))], color="green") for i in range(0, 60)]
# #scribeBrain = defaultdict(list)
# ##scribeBrain[sinScribe].append(TerminalScribe)
# #scribeBrain[sinScribe].append(sinScribe.jump())
#
# # Create a new Canvas instance that is 30 units wide by 30 units tall
#
#
# # Create a new scribe and give it the Canvas object
# scribe = TerminalScribe(canvas)
#
