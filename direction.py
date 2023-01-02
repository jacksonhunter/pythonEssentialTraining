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
        self._pallete =[["default" for y in range(self._y)] for x in range(self._x)]

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
            print(''.join([self._canvas[x][y] for x in range(self._x)]))

    def dump(self):
        for col in self._pallete:
            print(col)

class TerminalScribe:
    def __init__(self, canvas):

        self.pos = [0,0]
        self.canvas=canvas
        self.mark = "*"
        self.framerate = 0.005

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

    def dl(self, trail=".", firstTrail=""):
        pos = [self.pos[0]-1, self.pos[1]+1]
        if not self.canvas.hitsWall(pos):
            self.draw(pos, trail)

    def dr(self, trail=".", firstTrail=""):
        pos = [self.pos[0]+1, self.pos[1]+1]
        if not self.canvas.hitsWall(pos):
            self.draw(pos, trail)

    def ul(self, trail=".", firstTrail=""):
        pos = [self.pos[0]-1, self.pos[1]-1]
        if not self.canvas.hitsWall(pos):
            self.draw(pos, trail)

    def ur(self, trail=".", firstTrail=""):
        pos = [self.pos[0]+1, self.pos[1]-1]
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
        complex = cmath.rect(1, math.radians(phi) )
        self.cfwd(complex, trail)

    def pfwd(self, r, phi, trail="."):
        complex = cmath.rect(r, math.radians(phi))
        self.cfwd(complex, trail)

    def cfwd(self, complex, trail="."):
        polar=cmath.polar(complex)
        real = complex.real
        imag= complex.imag
        phi = polar[1]
        r = polar[0]
        pos = [self.pos[0]+int(real), self.pos[1]-int(imag)]
        u = cmath.rect(1, phi)
        for i in range(0, math.ceil(r)):
            if not self.canvas.hitsWall(pos):
                self.draw([self.pos[0] + int(round(u.real,0)), self.pos[1] - int(round(u.imag,0))], trail)



# Create a new Canvas instance that is 30 units wide by 30 units tall
canvas = Canvas(60, 22)

# Create a new scribe and give it the Canvas object
scribe = TerminalScribe(canvas)

# Move 1 down
scribe.forward(270)
# Move 3 down
scribe.pfwd(3, 270)
# Move 3 right
scribe.pfwd(3,0)
#move 3 up and to the right
scribe.pfwd(3, 45)
#  move 2 right and 4 down
scribe.cfwd(2.5-4j)
