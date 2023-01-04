import os
import time
import cmath
import math
from termcolor import colored
#from random import sample


# This is the Canvas class. It defines some height and width, and a 
# matrix of characters to keep track of where the TerminalScribes are moving
class Canvas:
    def __init__(self, width, height):
        self._x = width
        self._y = height
        # This is a grid that contains data about where the 
        # TerminalScribes have visited
        self._canvas = [[' ' for y in range(self._y)] for x in range(self._x)]


    # Returns True if the given point is outside the boundaries of the Canvas
    def hitsWall(self, point):
        return point[0] < 0 or point[0] >= self._x or point[1] < 0 or point[1] >= self._y

    # Set the given position to the provided character on the canvas
    def setPos(self, pos, mark):
        self._canvas[pos[0]][pos[1]] = mark

        # Clear the terminal (used to create animation)
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    # Clear the terminal and then print each line in the canvas
    def print(self):
        self.clear()
        for y in range(self._y):
            print(' '.join([self._canvas[x][y] for x in range(self._x)]))

class TerminalScribe:
    def __init__(self, canvas):

        self.pos = [0,0]
        self.canvas=canvas
        self.mark = "*"
        self.framerate = 0.2

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

    def forward(self, phi, trail="."):
        unit = cmath.rect(1, math.radians(phi) )
        pos = [self.pos[0] + int(round(unit.real, 0)), self.pos[1] - int(round(unit.imag, 0))]
        if not self.canvas.hitsWall(pos):
            self.draw(pos, trail)
    def pfwd(self, r, phi, trail="."):
        complex=cmath.rect(r, math.radians(phi))
        unit = cmath.rect(1, math.radians(phi) )
        init = self.pos2c(self.pos)
        points = [self.c2pos(init + i*unit) for i in range(0, r) ]
        draw = [self.draw(i, trail) for i in points if not self.canvas.hitsWall(i)]

    def cfwd(self, complex, trail=".", n=0):
        polar=cmath.polar(complex)
        self.pfwd(polar[0], math.degrees(polar[1]), trail)
    def c2pos(self, complex):
        return [int(round(complex.real,0)), int(round(-complex.imag, 0))]
    def pos2c(self, pos=[0,0]):
        return pos[0]-pos[1]*1j
    def runForward(self, n, phi, trail="."):
        unit = cmath.rect(1, math.radians(phi) )
        init = self.pos2c(self.pos)
        i=1
        points = [self.pos]
        while len(points) <= n:
            p=self.c2pos(init + i*unit)
            if not p in points:
                points.append(p)
            i+=1
        draw = [self.draw(i, trail) for i in points if not self.canvas.hitsWall(i)]
        print(len(points))
        print(points)


# Create a new Canvas instance that is 30 units wide by 30 units tall
canvas = Canvas(60, 30)

# Create a new scribe and give it the Canvas object
scribe = TerminalScribe(canvas)
#scribe.framerate=0.02
# Move 1
#scribe.forward(-10, ".")
#scribe.forward(-20, ".")
#scribe.forward(-30, ".")
#scribe.forward(-35, "-")
#scribe.forward(-40, "-")
#scribe.forward(-60, "-")
#i=[scribe.forward(-70, "-") for i in "......."]
#scribe.runForward(10, -70)
scribe.runForward(20, -24)
scribe.runForward(7,45)
scribe.pfwd(7, -45)

#scribe.forward(-50, "+")
#move down and right vector 3
#scribe.pfwd(3,315, "'")

# Move 3 down
#scribe.pfwd(3, 270, "+")
# Move 3 right
#scribe.pfwd(3,0,"~")
#move 3 up and to the right
#scribe.pfwd(3, 45)
#  move 2 right and 4 down
#scribe.cfwd(2-4j, "+")
#move 1 left and 5 down
#scribe.cfwd(-1-5j,"-")

#3 left and 2 up
#scribe.cfwd(-3+2j,"x")
#4 down
#scribe.cfwd(0-4j)
# 3 left and 2 up
#scribe.cfwd(-3+2j, "t")
#16 at 24 degrees
#scribe.pfwd(16,24, "c")
#6 at 315
#scribe.pfwd(27,315, "x")
#scribe.forward(290)
#scribe.pfwd(3, -70)
