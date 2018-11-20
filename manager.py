from random import *


# food class to manage food
class Food:
    def __init__(self, x, y, obj, size):
        self.size = size  # size of a food
        self.obj = obj  # obj of food
        self.coordinates = self.setxy(x, y, size)  # full cords of food hit box

    @classmethod
    def setxy(cls, x, y, size=1):  # to get food full hit box cords for its size
        if size == 1 or size == 2:
            return [[x, y]]
        elif size == 4 or size == 8:
            return [[x, y], [x + 10, y], [x, y + 10], [x + 10, y + 10]]
        elif size == 9:
            return [[x - 10, y - 10], [x - 10, y], [x, y - 10], [x - 10, y + 10], [x + 10, y - 10], [x, y], [x + 10, y],
                    [x, y + 10], [x + 10, y + 10]]


class FoodSpawn:
    @classmethod
    def getfoodspawn(cls, snakeList):  # gets random cords where to spawn food
        return cls.getCordsToSpawn(snakeList)

    @classmethod
    def getSize(cls):  # gets random size for size for food to spawn
        tempSize = randint(1, 100)
        if tempSize < 50:
            return 1
        elif tempSize < 75:
            return 2
        elif tempSize < 90:
            return 4
        elif tempSize < 98:
            return 8
        else:
            return 9

    @classmethod
    def getCordsToSpawn(cls, snake):  # gets cords on where to spawn food
        size = cls.getSize()
        while True:
            breakout = True
            x, y = 0, 0
            if size == 1 or size == 2:  # gets where to spawn food
                x = (randint(0, 71) * 10)
                y = (randint(0, 71) * 10)
            elif size == 4 or size == 8:
                x = (randint(0, 70) * 10)
                y = (randint(0, 70) * 10)
            elif size == 9:
                x = (randint(1, 70) * 10)
                y = (randint(1, 70) * 10)
            food = Food.setxy(x, y, size)  # gets full hit box of where to spawn food
            breakout = cls.breakout(snake, food)
            if breakout:  # returns x, y and size if the is place to spawn
                return [x, y, size]

    @classmethod
    def breakout(cls, snake, food):
        for e in food:  # checks if food hit box is not on snake hit box
            if e in snake:
                return False  # returns false if hit box collide with food
        return True
