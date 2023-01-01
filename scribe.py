import os
import re
import time
from termcolor import colored
import requests
from bs4 import BeautifulSoup
from random import sample


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
        self.guess = ""
        self.answer = self.getWord()
        self.count = 0
        self.score = 0
        self.used = set()

    def getWord(self):
        page = requests.get("https://www.wordunscrambler.net/word-list/wordle-word-list")
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(id="form1")
        #print(results.prettify())
        words=[i.text.strip() for i in results.find_all(href=re.compile("unscramble")) if len(i.text.strip()) == 5]
#        dummy=[print(i.text.strip(), end="\n" * 2) for i in words if len(i.text.strip()) == 5]
        #term_ = [print(i, end="\n") for i in words]
        return sample(words, 1)[0]

    def getChar(self, pos):
        char = self.canvas[pos[0]][pos[1]]
        return char

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

    def drawGallows(self):
        self.jump([3, 12])
        gallows = [[self.right(i) for i in "x_..----------..x"], self.down(" "), self.right("~"), self.right("-"),
                   [self.down(i) for i in ".||`"], self.up(" ",), self.left('`',), self.down("."), [self.left(i) for i in '"-..____________..-"'[::-1]],
                   [self.up(i) for i in " |||"], [self.right(i) for i in ".-~"], [self.jump([self.pos[0] - 1, self.pos[1] - 1]) for i in "."],
                   [self.up(i) for i in "||||||||||"], [self.right(i) for i in "________________"],[self.down(i) for i in "_||||||||||"],
                   [self.jump([2, 14]) for i in "."], self.down("."), [self.right(i) for i in '\"-..____________..-\"|']]
        noose = [[self.jump([11, 3]) for i in "."],[self.down(i) for i in "::"], self.down(":"), self.right(" "), self.down("\\"), self.left("/"), self.left("_"), self.up("\\"), self.up("/")]

    def takeInput(self):
        self.guess = ""
        prompt=[self.jump([1, 20]), [self.right(i) for i in ("Pick up to " + str(5 - self.count) + " letter(s)!")]]
        while not self.guess.isalpha():
            self.guess = input()
            self.processInput()

    def processInput(self):
        self.guess = self.guess.lower()
        posLetters = [32, 10]
        for i in self.guess[:(5-self.count)]:
            letter=self.answer.find(i)
            if letter == -1 or i in self.used:
                self.count += 1
            while not letter == -1:
                self.jump([posLetters[0]+2*letter, posLetters[1]])
                self.right(i)
                if i not in self.used:
                    self.score += 1
                    prompt = [self.jump([1, 20]), [self.right(i) for i in "Right!"]]
                letter=self.answer.find(i, letter+1)
            self.used.add(i)
            self.jump([32, 14])
            used = [self.right(i) for i in self.used]

    def gameOver(self):
        if self.score >= 5:
            message = [self.jump([1, 20]), [self.right(i) for i in "You won!  ۜ\(סּںסּَ` )/ۜ"]]
            return True
        elif self.count >= 5:
            message = [self.jump([1, 20]), [self.right(i) for i in "You lost!  (╯°□°）╯︵ ┻━┻ "]]
            self.canvas.setPos([32,11], colored(" ".join(self.answer), "red"))
            self.canvas.print()
            return True
        else:
            return False

    def playHangman(self):
        self.drawGallows()
        self.jump([32, 10])
        gameboard = [self.right(i) for i in "_ _ _ _ _"]
        while self.gameOver() == (not True):
            self.takeInput()
            self.drawScore()

    def drawScore(self):
        heads = [[""], ["(ᵔᵕᵔ)"], ["(⊙.☉)"], ["(@_@)"], ["(ಥ⌣ಥ)" ], ["(✖╭╮✖)"] ]
        body=[""]
        armL=False
        armR=False
        legL=False
        legR=False
        if self.count > 0:
            head = [self.jump([9, 7]), [self.right(i) for i in heads[self.count][0]] ]
        if self.count >=2 and not armL:
            armL = [self.jump([7, 7]), self.right("\\"), self.down(" "), [self.right(i) for i in "\__|"] ]
        if self.count >=3 and not armR:
            armR = [ [self.right(i) for i in "__/"], self.up(" "), self.right("/")]
        if self.count >=4 and not legL:
            legL = [self.jump([11, 9]), [self.left(i) for i in "|__"], [self.down(i) for i in " /"], self.left(" "), self.left("/") ]
        if self.count >=5 and not legR:
            legL = [self.jump([11, 9]), [self.right(i) for i in "|__"], [self.down(i) for i in " \\"], self.right(" "), self.right("\\") ]




# Create a new Canvas instance that is 30 units wide by 30 units tall
canvas = Canvas(60, 22)

# Create a new scribe and give it the Canvas object
scribe = TerminalScribe(canvas)

# Draw a small square

# scribe.drawSquare(1)
# scribe.drawSquare(2)
# scribe.drawSquare(3)
#scribe.drawSquare(5)

#scribe.drawTriangle(9)
#scribe.drawSquare(13)
#scribe.drawSquare(21)

#scribe.drawGallows()

scribe.playHangman()
#canvas.dump()
#scribe.getWord()
#print([[""], ["(ᵔᵕᵔ)"], ["(⊙.☉)"], ["(@_@)"], ["(ಥ⌣ಥ)" ], ["(✖╭╮✖)"] ][1][0])
