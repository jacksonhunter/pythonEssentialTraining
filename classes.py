import os
import time
import cmath
import math
from unicodedata import decimal

from termcolor import colored
import re
import numpy


# from collections import defaultdict
# from random import sample


# This is the Canvas class. It defines some height and width, and a 
# matrix of characters to keep track of where the TerminalScribes are moving
class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        self.framerate = 0.05
        # This is a grid that contains data about where the
        # TerminalScribes have visited
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]

    # Returns True if the given point is outside the boundaries of the Canvas
    def hitsWall(self, point):
        return point[0] < 0 or point[0] >= self._x or point[1] < 0 or point[1] >= self._y

        return normal

    # Set the given position to the provided character on the canvas
    def setPos(self, pos, mark):
        if not self.hitsWall(pos):
            self._canvas[pos[0]][pos[1]] = mark
        # Clear the terminal (used to create animation)

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # Clear the terminal and then print each line in the canvas
    def print(self):
        self.clear()
        for y in range(self._y):
            print(' '.join([self._canvas[x][y] for x in range(self._x)]))


class Crystal(Canvas):
    def __init__(self, width, height):
        super().__init(width, height)

        self.framerate = 0.02
        self._t = 0
        # self._crystal = [[[' ' for y in range(self._y)] for x in range(self._x)] for t in range(1000)]
        self._crystal = numpy.full((500, self._x, self._y), " ")

    def setPos(self, pos, mark):
        if not self.hitsWall(pos):
            self._canvas[pos[0]][pos[1]] = mark
            self._crystal[self._t::, pos[0], pos[1]] = mark
            # self._crystal[self._t][pos[0]][pos[1]] = mark
            self._t += 1
        # Clear the terminal (used to create animation)
        super().setPos(self, pos, mark)

        if not self.hitsWall(pos):
            self._crystal[self._t::, pos[0], pos[1]] = mark
            # self._crystal[self._t][pos[0]][pos[1]] = mark
            self._t += 1

    def animate(self):
        for t in range(0, 500):
            self.clear()
            for y in range(self._y):
                print(' '.join([self._crystal[t, x, y] for x in range(self._x)]))
            time.sleep(self.framerate)

    def resetCrystal(self):
        self._t = 0


class FloatingCanvas(Canvas):
    def __init__(self, width, height):
        super().__init__(width, height)

    def hitsWall(self, point):
        normal = (1 + 1e-16j if point[0] < 0 else -1 + 1e-16j if point[0] >= self._x else 1e-16 - 1j if point[
                                                                                                            1] < 0 else 1e-16 + 1j if
        point[1] >= self._y else False)

        return normal

    def setPos(self, pos, mark):
        ipos = [int(round(i, 0)) for i in pos]
        if not self.hitsWall(pos):
            self._canvas[ipos[0]][ipos[1]] = mark
        # Clear the terminal (used to create animation)


class TerminalScribe:
    def __init__(self, canvas):

        self.pos = [0, 0]
        self.canvas = canvas
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
        pos = [self.pos[0], self.pos[1] - 1]
        if not self.canvas.hitsWall(pos):
            self.draw(pos, trail)

    def down(self, trail="."):
        pos = [self.pos[0], self.pos[1] + 1]
        if not self.canvas.hitsWall(pos):
            self.draw(pos, trail)

    def right(self, trail=".", color="default"):
        pos = [self.pos[0] + 1, self.pos[1]]
        if not self.canvas.hitsWall(pos):
            self.draw(pos, trail, color)

    def left(self, trail="."):
        pos = [self.pos[0] - 1, self.pos[1]]
        if not self.canvas.hitsWall(pos):
            self.draw(pos, trail)

    def distance(self, posi, posf):
        return (int(round(math.dist(posi, posf))))

    def draw(self, pos, trail='.', mark='red', color='white'):
        self.trail = trail

        # Set the old position to the "trail" symbol
        self.canvas.setPos(self.pos, colored(self.trail, color))
        # Update position
        self.pos = pos
        # Set the new position to the "mark" symbol
        self.canvas.setPos(self.pos, colored(self.mark, mark))
        # Print everything to the screen
        self.canvas.print()
        # Sleep for a little bit to create the animation
        time.sleep(self.framerate)

    def c2v(self, c):
        return numpy.asarray([c.real, c.imag])

    def v2c(self, a):
        return a[0] + a[1] * 1j


class VectorScribe(TerminalScribe):
    def __int__(self):
        super().__init__(canvas)

    def unitVector(self):
        return cmath.rect(1, math.radians(self.phi))

    def nextPoint(self):

        init = self.pos2c()
        delta = self.unitVector()

        while abs(round(delta.real, 0)) < 1 and abs(round(delta.imag, 0)) < 1:
            delta += self.unitVector()

        return [(init + delta).real, -(init + delta).imag]

    def forward(self, phi=None, trail=".", color="white", mark="red"):
        if type(phi) == str:
            trail = phi
            phi = None
        if phi == None:
            phi = self.phi
        self.phi = phi

        draw = [self.draw(self.nextPoint(), i, color=color) for i in trail]

    def runForward(self, n, phi=None, trail=".", color="white"):
        if type(phi) == str:
            trail = phi
            phi = None
        if phi == None:
            phi = self.phi
        self.phi = phi
        self.forward(trail=(trail * n)[:n], color=color)

    def setPhi(self, phi=None):
        if phi == None:
            phi = self.phi
        self.phi = phi

    def c2pos(self, complex=0 + 0j):
        return [int(numpy.round(complex.real, 0)), int(numpy.round(-complex.imag, 0))]

    def pos2c(self, pos=None):
        if pos == None:
            pos = self.pos
        return pos[0] - pos[1] * 1j


class FunctionScribe(VectorScribe):
    def __int__(self):
        super().__init__(canvas)

    def drawFunction(self, *args, title=None, xaxis="x-axis", yaxis="y axis", xrange=None, yrange=None):
        colors = ["yellow", "magenta", "red", "green", "white"] * 2
        marks = ["*", ".", "~"]
        self.framerate = 0.001
        xcanvas = list(range(self.canvas._x - 6))
        ycanvas = list(range(self.canvas._y - 3))
        if xrange == None:
            xrange = xcanvas
        if yrange == None:
            yrange = ycanvas
        if title == None:
            title = str("y = " + str(args))
        xstep = len(xrange) / (len(xcanvas))
        xdomain = [i * xstep for i in xcanvas]
        yfactor = len(yrange) / len(ycanvas)
        ydomain = [[eval(arg) for x in xdomain] for arg in args]
        o = [4, self.canvas._y - 4]
        ya = [self.jump([o[0] - 1, o[1] + 1]), self.forward(90, ("L||||||||+" + ("||||||||+" * 10))[:len(ycanvas) - 1])]
        xa = [self.jump([o[0], o[1] + 1]), self.forward(0, ("_________|" * 10)[:len(xcanvas) - 1])]

        yscaleloc = [[o[0] - 2, o[1] + 2]]
        xscaleloc = [[o[0] - 1, o[1] + 2]]

        for i in range(10, self.canvas._y - 3, 10):
            base = yscaleloc[0]
            yscaleloc.append([base[0], base[1] - i])
        for i in range(10, self.canvas._x - 6, 10):
            base = xscaleloc[0]
            xscaleloc.append([base[0] + i, base[1]])
        ys = []
        xs = []
        for i in yscaleloc:
            self.jump(i)
            y = len(yrange) / (self.canvas._y - 3) * 10 * (yscaleloc.index(i))
            y = f"{y:.0f}" if y >= 10 or y == 0 else f"{y:.1f}" if y >= 1 else f"{y:.2f}"
            ys.append(y)
            self.forward(180, y[::-1])

        for i in xscaleloc:
            self.jump(i)
            x = len(xrange) / (self.canvas._x - 6) * 10 * (xscaleloc.index(i))
            x = f"{x:.0f}" if x >= 10 or x == 0 else f"{x:.1f}" if x >= 1 else f"{x:.2f}"
            xs.append(x)
            self.forward(0, x)
        self.jump([0, yscaleloc[0][1]])
        self.forward(0, "(" + xs[0] + ", " + ys[0] + ")")

        ylabloc = [0, o[1] - int(len(ycanvas) / 2 + len(yaxis) / 2)]
        xlabloc = [o[0] + int(len(xcanvas) / 2 - len(xaxis) / 2), o[1] + 3]

        xlab = [self.jump(xlabloc), self.forward(0, xaxis)]
        ylab = [self.jump(ylabloc), self.forward(-90, yaxis)]

        self.framerate = 0.02

        fx = [[self.canvas.setPos([o[0] + xrange[i], o[1] - int(round(y[i] / yfactor, 0))],
                                  colored(marks[ydomain.index(y)], colors[ydomain.index(y)])) for y in ydomain] for i in
              xcanvas]
        titlestart = [int(len(xcanvas) / 2 - len(title) / 2) + 6, 4]
        # titlerange=[[i, 4] for i in range(titlestart, titlestart+len(title))]

        if str(args) in title:
            titlestart = [0, 4]  # indexes = [title.find(str(i)) for i in args]
            for i in args:
                titlestart[0] = int(len(xcanvas) / 2 - len(str(i)) / 2) + 6
                ttl = [self.jump(titlestart), self.forward(0, "y = " + str(i), color=colors[args.index(i)])]
                titlestart[1] += 1
        self.mark = " "
        self.draw(self.pos, " ")


class BounceScribe(VectorScribe):
    def __int__(self):
        super().__init__(canvas)

    def nextPoint(self):

        init = self.pos2c()
        delta = self.unitVector()

        while abs(round(delta.real, 0)) < 1 and abs(round(delta.imag, 0)) < 1:
            delta += self.unitVector()
        next = init + delta  # [(init + delta).real, -(init + delta).imag]
        bounceNormal = canvas.hitsWall(self.c2pos(next))
        if bounceNormal:
            next = self.bounce(bounceNormal, delta)
        return [next.real, -next.imag]

    def bounce(self, n, d=None):
        if d == None:
            d = self.unitVector()
        vn = self.c2v(n)
        vd = self.c2v(d)
        vr = vd - 2 * numpy.dot(vd, vn) * vn
        r = self.v2c(vr)
        next = self.pos2c() + d + r
        self.setPhi(math.degrees(cmath.polar(r)[1]))
        return (next)


class RainbowScribe(BounceScribe):
    def __int__(self):
        super().__init__(canvas)

    def forward(self, phi=None, trail=".", colors=["red", "yellow", "green", "blue", "magenta"]):
        if type(phi) == str:
            trail = phi
            phi = None
        if phi == None:
            phi = self.phi
        self.phi = phi
        marks = colors[::-1]
        draw = [self.draw(self.nextPoint(), trail[i], color=(colors * len(trail))[i], mark=(marks * len(trail))[i]) for
                i in range(len(trail))]

    def runForward(self, n, phi=None, trail=".", colors=["red", "yellow", "green", "blue", "magenta"]):
        if type(phi) == str:
            trail = phi
            phi = None
        if phi == None:
            phi = self.phi
        self.phi = phi
        self.forward(trail=(trail * n)[:n], colors=colors)


class ParseScribe(RainbowScribe):
    def __int__(self):
        super().__init__(canvas)

    def parse(self, str):
        for i in re.split(r"(\d+)", str):
            if i.isnumeric():
                self.phi = float(i)
            else:
                self.forward(trail=i)


canvas = FloatingCanvas(60, 30)
funkScribe = FunctionScribe(canvas)

funkScribe.drawFunction("90*math.sin(math.radians(x))+90", "x", xrange=list(range(0, 360)), xaxis="degrees",
                        yrange=list(range(0, 200)))
bounceScribe = RainbowScribe(canvas)
bounceScribe.jump([6, 27])
bounceScribe.framerate = .02
bounceScribe.forward(30, "~" * 7)
bounceScribe.runForward(300, 30, "1232")
bounceScribe.setPhi(0)
bounceScribe.runForward(7, "green")

parseScribe = ParseScribe(canvas)
parseScribe.parse("300abcdefghijklmno330pqrs0tuv30wxyzABCDEFG60HIJKLMN90OPQ30RSTUVWX0YZ330zyxwv" * 30)

# funkScribe.jump([3, canvas._y-3])
# funkScribe.forward("......")
