from tkinter import *
from threading import *
from time import *
from random import *
from msgbox import *
from manager import *


class Snake(Thread):
    def play(self, dummy, obj):
        self.gobj = obj
        self.score = 0
        self.runing = True
        self.size = 720
        self.gui = Tk()
        self.gui.resizable(width=False, height=False)
        self.keybind()
        self.canvas = Canvas(self.gui, width=self.size, height=self.size)
        self.canvas.pack()
        self.draw = Draw()
        self.display = Thread(target=self.draw.display, name="display", args=(self.size, self))
        self.display.start()
        self.gui.mainloop()
        self.display.join()
        self.gobj.score = self.score

    def keybind(self):
        self.gui.bind("<Left>", self.keypressleft)
        self.gui.bind("<Right>", self.keypressright)
        self.gui.bind("<Up>", self.keypressup)
        self.gui.bind("<Down>", self.keypressdown)
        self.gui.bind("<a>", self.keypressleft)
        self.gui.bind("<d>", self.keypressright)
        self.gui.bind("<w>", self.keypressup)
        self.gui.bind("<s>", self.keypressdown)

    def keypressleft(self, e):
        if self.draw.dirsetion != "left" and self.draw.dirsetion != "right" and self.draw.canturn:
            self.draw.dirsetion = "left"
            self.draw.canturn = False

    def keypressright(self, e):
        if self.draw.dirsetion != "left" and self.draw.dirsetion != "right" and self.draw.canturn:
            self.draw.dirsetion = "right"
            self.draw.canturn = False

    def keypressup(self, e):
        if self.draw.dirsetion != "up" and self.draw.dirsetion != "down" and self.draw.canturn:
            self.draw.dirsetion = "up"
            self.draw.canturn = False

    def keypressdown(self, e):
        if self.draw.dirsetion != "up" and self.draw.dirsetion != "down" and self.draw.canturn:
            self.draw.dirsetion = "down"
            self.draw.canturn = False


class Draw(Thread):
    def display(self, size, obj):
        self.tick = 0
        self.food = ""
        self.ate = 0
        self.box = []
        self.mainobj = obj
        self.lis = [[340, 350], [350, 350], [360, 350], [370, 350]]
        while self.mainobj.runing:
            self.move()

    def move(self):
        self.dirsetion = "right"
        while self.mainobj.runing:
            start = time()
            if self.dirsetion == "right":
                self.lis.append([self.lis[len(self.lis) - 1][0] + 10, self.lis[len(self.lis) - 1][1]])
            elif self.dirsetion == "left":
                self.lis.append([self.lis[len(self.lis) - 1][0] - 10, self.lis[len(self.lis) - 1][1]])
            elif self.dirsetion == "up":
                self.lis.append([self.lis[len(self.lis) - 1][0], self.lis[len(self.lis) - 1][1] - 10])
            elif self.dirsetion == "down":
                self.lis.append([self.lis[len(self.lis) - 1][0], self.lis[len(self.lis) - 1][1] + 10])
            if self.ate > 0:
                self.ate -= 1
            else:
                self.lis.pop(0)
            self.ck(self.lis[len(self.lis) - 1])
            self.spawnfood()
            self.caneat(self.lis[-1][0], self.lis[-1][1])
            self.drawsnake()
            self.gameover()
            end = time()
            sleepTime = 0.2 - (end-start)
            sleep(sleepTime)
            self.canturn = True

    def drawsnake(self):
        for i in range(len(self.lis)):
            if i == len(self.lis) - 1:
                self.drawbox(self.lis[i][0], self.lis[i][1], "black")
            else:
                self.drawbox(self.lis[i][0], self.lis[i][1])

    def ck(self, head):
        if head[0] == 720:
            self.lis[len(self.lis) - 1][0] -= 720
        elif head[0] == -10:
            self.lis[len(self.lis) - 1][0] += 720
        elif head[1] == 720:
            self.lis[len(self.lis) - 1][1] -= 720
        elif head[1] == -10:
            self.lis[len(self.lis) - 1][1] += 720

    def spawnfood(self):
        if self.food == "":
            if self.tick % 5 == 0:
                foodcords = FoodSpawn.getCordsToSpawn(self.lis)
                x = foodcords[0]
                y = foodcords[1]
                size = foodcords[2]
                foodobj = ""
                if size == 1:
                    foodobj = self.mainobj.canvas.create_rectangle(x, y, x+10, y+10, fill="yellow")
                elif size == 2:
                    foodobj = self.mainobj.canvas.create_rectangle(x, y, x+10, y+10, fill="black")
                elif size == 4:
                    foodobj = self.mainobj.canvas.create_rectangle(x, y, x+20, y+20, fill="yellow")
                elif size == 8:
                    foodobj = self.mainobj.canvas.create_rectangle(x, y, x+20, y+20, fill="black")
                elif size == 9:
                    foodobj = self.mainobj.canvas.create_rectangle(x-10, y-10, x+20, y+20, fill="yellow")
                self.food = Food(x, y, foodobj, size)


    def caneat(self, headx, heady):
        try:
            foodhitbox = self.food.coordinates
            snakehead = [headx, heady]
            if snakehead in foodhitbox:
                self.mainobj.canvas.delete(self.food.obj)
                self.ate += self.food.size
                self.mainobj.score += self.food.size
                self.food = ""
        except BaseException:
            self.tick += randint(0, 1)

    def drawbox(self, x, y, colour="green"):
        if len(self.box) == len(self.lis):
            self.mainobj.canvas.delete(self.box.pop(0))
        self.box.append(self.mainobj.canvas.create_rectangle(x, y, x + 10, y + 10, fill=colour))

    def gameover(self):
        for i in range(0, len(self.lis) - 1):
            if self.lis[i] == self.lis[len(self.lis) - 1]:
                self.mainobj.runing = False
                self.mainobj.gui.quit()


class game():
    def __init__(self):
        self.run = "Yes"
        self.score = 0

    def start(self):
        while self.run == "Yes":
            self.snake = Snake()
            self.mb = Mb()
            self.count = 1
            self.snakethread = Thread(target=self.snake.play, name="snake{}".format(self.count), args=("", self))
            self.snakethread.start()
            self.snakethread.join()
            args = self, "Snake-game", "Your score is {} do you want to play again".format(self.score), "Yes", "No"
            showmsg = Thread(target=self.mb.showmsg, name="showmsg{}".format(self.count), args=(args))
            showmsg.start()
            showmsg.join()


gm = game()
gm.start()
