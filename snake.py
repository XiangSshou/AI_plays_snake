import random
from pygame import draw
from brain import *


class snake:
    def __init__(self, width, height, brainLayer, size, head_x=40, head_y=40, random_weights=True, random_bases=True, random_start=False):
        self.list = []
        self.width = width
        self.height = height
        self.steps_taken = 0
        self.no_of_same_result = 0
        self.crash_wall = False
        self.crash_body = False
        self.crash_snake = False
        self.block = size
        self.moveCount = 0
        self.toIncrease = False
        self.score = 0
        self.Brain = brain(brainLayer, self.width, self.height,
                           self.block, random_weights, random_bases)
        if random_start:
            self.direction = random.choice(['east', 'north', 'west', 'east'])
            x = random.randint(3*size, width - 2*size)
            self.head_x = x - (x % size)
            y = random.randint(size, height - 2*size)
            self.head_y = y - (y % size)
        else:
            self.direction = 'east'
            self.head_x, self.head_y = head_x, head_y
            if head_x > width/2:
                self.direction = 'west'
        self.list.append((self.head_x, self.head_y))

    # draw the snake on the pygame screen
    def draw(self, screen, color):
        l = self.block
        for (x, y) in self.list:
            draw.rect(screen, color, (x, y, l, l), 1)
            draw.rect(screen, color, (x+3, y+3, l-6, l-6))
        return screen

    # returns true if snake is alive else false
    def isAlive(self):
        if not self.crash_wall and not self.crash_body and not self.crash_snake:
            return True
        else:
            return False

    # check if the snake need to increase
    def check_increase(self):
        if self.toIncrease:
            self.toIncrease = False
            self.moveCount = 0
        else:
            self.moveCount += 1
            self.list.pop()

    # sets the crash_wall and crash_body if unable to go north accordingly
    def check_north(self, snake):
        if self.head_y - self.block < self.block:
            self.crash_wall = True
        for i in range(len(self.list) - 1):
            if self.list[i][0] == self.head_x and self.list[i][1] == (self.head_y - self.block):
                self.crash_body = True
        for i in range(len(snake.list)):
            if snake.list[i][0] == self.head_x and snake.list[i][1] == (self.head_y - self.block):
                self.crash_snake = True

    # move the snake in north
    def move_north(self, snake):
        self.check_north(snake)
        if not (self.crash_wall or self.crash_body or self.crash_snake):
            self.direction = 'north'
            self.head_y = self.head_y - self.block
            self.list.insert(0, (self.head_x, self.head_y))
            self.check_increase()

    # sets the crash_wall and crash_body if unable to go south accordingly
    def check_south(self, snake):
        if self.head_y + self.block >= self.height - self.block:
            self.crash_wall = True
        for i in range(len(self.list) - 1):
            if self.list[i][0] == self.head_x and self.list[i][1] == (self.head_y + self.block):
                self.crash_body = True
        for i in range(len(snake.list)):
            if snake.list[i][0] == self.head_x and snake.list[i][1] == (self.head_y + self.block):
                self.crash_snake = True

    # move the snake in south
    def move_south(self, snake):
        self.check_south(snake)
        if not (self.crash_wall or self.crash_body or self.crash_snake):
            self.direction = 'south'
            self.head_y = self.head_y + self.block
            self.list.insert(0, (self.head_x, self.head_y))
            self.check_increase()

    # sets the crash_wall and crash_body if unable to go east accordingly
    def check_east(self, snake):
        if self.head_x + self.block >= self.width - self.block:
            self.crash_wall = True
        for i in range(len(self.list) - 1):
            if self.list[i][0] == (self.head_x + self.block) and self.list[i][1] == self.head_y:
                self.crash_body = True
        for i in range(len(snake.list)):
            if snake.list[i][0] == (self.head_x + self.block) and snake.list[i][1] == self.head_y:
                self.crash_snake = True

    # move the snake in east
    def move_east(self, snake):
        self.check_east(snake)
        if not (self.crash_wall or self.crash_body or self.crash_snake):
            self.direction = 'east'
            self.head_x = self.head_x + self.block
            self.list.insert(0, (self.head_x, self.head_y))
            self.check_increase()

    # sets the crash_wall and crash_body if unable to go west accordingly
    def check_west(self, snake):
        if self.head_x - self.block < self.block:
            self.crash_wall = True
        for i in range(len(self.list) - 1):
            if self.list[i][0] == (self.head_x - self.block) and self.list[i][1] == self.head_y:
                self.crash_body = True
        for i in range(len(snake.list)):
            if snake.list[i][0] == (self.head_x - self.block) and snake.list[i][1] == self.head_y:
                self.crash_snake = True

    # move the snake in west
    def move_west(self, snake):
        self.check_west(snake)
        if not (self.crash_wall or self.crash_body or self.crash_snake):
            self.direction = 'west'
            self.head_x = self.head_x - self.block
            self.list.insert(0, (self.head_x, self.head_y))
            self.check_increase()

    # returns the next head position and direction based on the result passed
    def next_position_direction(self, result):
        l = self.block
        x = self.head_x
        y = self.head_y
        direction = self.direction
        if direction == 'north':
            if result == 1:
                return (x, y - l), 'north'
            elif result == 2:
                return (x - l, y), 'west'
            else:
                return (x + l, y), 'east'
        elif direction == 'east':
            if result == 1:
                return (x + l, y), 'east'
            elif result == 2:
                return (x, y - l), 'north'
            else:
                return (x, y + l), 'south'
        elif direction == 'south':
            if result == 1:
                return (x, y + l), 'south'
            elif result == 2:
                return (x + l, y), 'east'
            else:
                return (x - l, y), 'west'
        else:
            if result == 1:
                return (x - l, y), 'west'
            elif result == 2:
                return (x, y + l), 'south'
            else:
                return (x, y - l), 'north'

    # returns true if x and y doesn't lie on the body of snake
    def onBody(self, x, y):
        for i in range(3, len(self.list) - 1):
            if self.list[i][0] == x and self.list[i][1] == y:
                return True
        return False

    # increase the size of the snake in the direction given by nn
    # def increaseSize(self, result, snake):
    #     pos, dir = self.next_position_direction(result)
    #     if (pos[0] != 0) and (pos[0] != self.width-self.block) and (pos[1] != 0) and (pos[1] != self.height-self.block) and (not self.onBody(pos[0], pos[1])) and (not snake.onBody(pos[0], pos[1])):
    #         self.head_x, self.head_y = pos[0], pos[1]
    #         self.list.insert(0, (self.head_x, self.head_y))
    #         self.direction = dir
    #         return True
    #     else:
    #         return False

    # move the snake based on the result provided
    def move(self, result, snake):
        if self.moveCount >= 10:
            self.score -= 1
            self.toIncrease = True
        if self.direction == 'north':
            if result == 1:
                self.move_north(snake)
            elif result == 2:
                self.move_west(snake)
            else:
                self.move_east(snake)
        elif self.direction == 'east':
            if result == 1:
                self.move_east(snake)
            elif result == 2:
                self.move_north(snake)
            else:
                self.move_south(snake)
        elif self.direction == 'south':
            if result == 1:
                self.move_south(snake)
            elif result == 2:
                self.move_east(snake)
            else:
                self.move_west(snake)
        else:
            if result == 1:
                self.move_west(snake)
            elif result == 2:
                self.move_south(snake)
            else:
                self.move_north(snake)
        self.steps_taken += 1
        return self.isAlive()

    def dirToRes(self, dir):
        if dir == 'north':
            if self.direction == 'north':
                return 1
            elif self.direction == 'south':
                return 1
            elif self.direction == 'east':
                return 2
            else:
                return 3
        elif dir == 'south':
            if self.direction == 'north':
                return 1
            elif self.direction == 'south':
                return 1
            elif self.direction == 'east':
                return 3
            else:
                return 2
        elif dir == 'east':
            if self.direction == 'north':
                return 3
            elif self.direction == 'south':
                return 2
            elif self.direction == 'east':
                return 1
            else:
                return 1
        else:
            if self.direction == 'north':
                return 2
            elif self.direction == 'south':
                return 3
            elif self.direction == 'east':
                return 1
            else:
                return 1
