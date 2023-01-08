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
        return point[0] < 0 or point[0] >= self._x or point[1] < 0 or point[1] >= self._y

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
        self.canvas.setPos(pos, colored(self.mark, "green"))
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
        self.canvas.setPos(self.pos, colored(self.mark, color))
        # Print everything to the screen
        self.canvas.print()
        # Sleep for a little bit to create the animation
        time.sleep(self.framerate)

    def forward(self, phi=None, trail=".", color = "red"):
        if type(phi) == str:
            trail = phi
            phi = None
        if phi == None:
            phi = self.phi
        self.phi = phi
        unit = cmath.rect(1, math.radians(self.phi) )
        init=self.pos2c()
        points = []
        i=1
        while len(points) <= len(trail):
            p = self.c2pos(init + i * unit)
            if not p in points:
                points.append(p)
            i += 1
        draw = [self.draw(points[i], trail[i], color=color) for i in range(0, len(trail)) if not self.canvas.hitsWall(points[i])]

    def cfwd(self, complex, trail="."):
        polar = cmath.polar(complex)
        self.pfwd(polar[0], math.degrees(polar[1]), trail)

    def c2pos(self, complex=0 + 0j):
        return [int(numpy.round(complex.real, 0)), int(numpy.round(-complex.imag, 0))]

    def pos2c(self, pos=None):
        if pos == None:
            pos = self.pos
        return pos[0] - pos[1] * 1j

    def c2v(self, c):
        return numpy.asarray([c.real, c.imag])

    def v2c(self, a):
        return a[0] + a[1] * 1j

    def runForward(self, n, phi=None, trail="."):
        if phi == None:
            phi = self.phi
        self.phi = phi
        self.forward(trail=trail * n)
    def drawFunction(self, *args, Title="Title", xaxis="x-axis", yaxis="y:axis", xrange=None, yrange=None ):
        self.framerate=0.001
        if xrange == None:
            xrange=list(range(self.canvas._x-4))
        if yrange == None:
            yrange=list(range(self.canvas._y-3))
        domain = [[eval(arg) for x in xrange] for arg in args]
        o = [3, self.canvas._y - 4]
        ya = [self.jump([o[0]-1, o[1] + 1] ), self.forward(90, "L" + ("||||||||+" * 10)[:len(yrange)-1])]
        xa = [self.jump([o[0], o[1] + 1] ), self.forward(0, ("_________|" * 10)[:len(xrange)-1])]

        ylabloc= [0, o[1] - int(len(yrange)/2 - len(yaxis)/2)]
        xlabloc= [o[0] + int(len(xrange)/2 - len(xaxis)/2), o[1]+3]

        xlab=[self.jump(xlabloc), self.forward(0, xaxis)]
        ylab = [self.jump(ylabloc), self.forward(-90, yaxis)]

        yscaleloc = [[o[0] - 3, o[1]-2]]
        xscaleloc = [[o[0] - 2, o[1]]]

        print(yscaleloc)
        for i in range(10, self.canvas._y-3, 10):
                base=yscaleloc[0]
                yscaleloc.append([base[0], base[1] + i])
        for i in range(10, self.canvas._x-4, 10):
                xscaleloc.append([[0]+ i, o[1]])
        for i in range(len(yscaleloc)):
            self.jump(yscaleloc[i])
            self.up(trail=yrange[i*int(round(len(yrange)/self.canvas._y-3),0)])

        fx=[self.jump(o), [[self.draw([o[0] + xrange[i], o[1] - int(round(domain[i], 0))]) for domain in domain] for i in xrange]]

        print(args)

canvas = Canvas(60, 30)
funkScribe = TerminalScribe(canvas)

funkScribe.drawFunction("x","0.5*x")
#funkScribe.jump([3, canvas._y-3])
#funkScribe.forward("......")

