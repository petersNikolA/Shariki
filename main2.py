import pygame
from pygame.draw import *
from random import randint

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TEAL = (0, 128, 128)
OLIVE = (128, 128, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, TEAL, OLIVE]


class Ball:
    def __init__(self):
        self.x = randint(100, 700)
        self.y = randint(100, 500)
        self.r = randint(30, 50)
        self.color = COLORS[randint(0, 7)]
        self.speed_x = randint(-20, 20)
        self.speed_y = randint(-20, 20)
        self.n = 0

    def test(self):
        if self.speed_x == 0:
            self.speed_x += 1
        if self.speed_y == 0:
            self.speed_y += 1

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x + self.r >= 800 or self.x - self.r <= 50:
            self.speed_x *= -1
        if self.y + self.r >= 600 or self.y - self.r <= 50:
            self.speed_y *= -1

    def draw(self):
        circle(screen, self.color, (self.x, self.y), self.r)

    def counter(self):
        x1, y1 = pygame.mouse.get_pos()
        p = ((x1 - self.x) ** 2 + (y1 - self.y) ** 2) ** (1 / 2)
        if p <= float(self.r):
            self.n = 1

    def remover(self):
        if self.n == 1:
            self.x = 0
            self.y = 0
            self.r = 0


class Square:
    def __init__(self, lev):
        self.xs = randint(100, 700)
        self.ys = randint(100, 500)
        self.a = randint(60, 80)
        self.color1 = COLORS[randint(0, 7)]
        self.speed_xs = randint(-20, 20)
        self.speed_ys = randint(-20, 20)
        self.ax = randint(-2, 2)
        self.ay = randint(-2, 2)
        self.liv = lev * 2

    def test(self):
        if self.speed_xs == 0:
            self.speed_xs += 1
        if self.speed_ys == 0:
            self.speed_ys += 1
        if self.ax == 0:
            self.ax += 1
        if self.ay == 0:
            self.ay -= 1

    def move(self):
        self.xs += self.speed_xs
        self.ys += self.speed_ys
        self.speed_xs += self.ax
        self.speed_ys += self.ay
        if self.xs + self.a >= 800 or self.xs <= 50:
            self.speed_xs *= -1
            self.xs += self.speed_xs
        if self.ys + self.a >= 600 or self.ys <= 50:
            self.speed_ys *= -1
            self.ys += self.speed_ys
        if abs(self.speed_xs) >= 30:
            if self.speed_xs > 0:
                self.speed_xs = 30
            else:
                self.speed_xs = -30
        if abs(self.speed_ys) >= 30:
            if self.speed_ys > 0:
                self.speed_ys = 30
            else:
                self.speed_ys = -30

    def draw(self):
        rect(screen, self.color1, (self.xs, self.ys, self.a, self.a))

    def counter(self):
        x1, y1 = pygame.mouse.get_pos()
        if (x1 >= self.xs) and (x1 <= (self.xs + self.a)) and (y1 >= self.ys) and (y1 <= (self.ys + self.a)):
            self.liv -= 1
            self.color1 = COLORS[randint(0, 7)]

    def remover(self):
        if self.liv <= 0:
            self.xs = 0
            self.ys = 0
            self.a = 0


pygame.init()

FPS = 30
screen = pygame.display.set_mode((1000, 800))

name = input('write your name')
"""
you need to click right button in order to add you result to results table
"""
level: int = int(input('difficulty level 1-3'))
'''
1 - the easiest 
3 - the hardest (more balls)
'''
result = 0
missed = 0

text1 = pygame.font.Font(None, 100)
text3 = pygame.font.Font(None, 100)

rect(screen, WHITE, (50, 50, 750, 550))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

balls = []
squares = []

for i in range(level * 5):
    ball = Ball()
    balls.append(ball)
for j in range(level):
    square = Square(level)
    squares.append(square)


def ballloop():
    for k in range(level * 5):
        b = balls[k]
        b.test()
        b.move()
        b.draw()


def sqloop():
    for r in range(level):
        b = squares[r]
        b.test()
        b.move()
        b.draw()


def game(finish):
    while not finish:
        clock.tick(FPS)
        rect(screen, WHITE, (50, 50, 750, 550))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for l in range(level * 5):
                        balls[l].counter()
                        balls[l].remover()
                    for b in range(level):
                        squares[b].counter()
                        squares[b].remover()
                elif event.button == 3:
                    record = open('record.txt', 'a')
                    record.write(name + ' : ' + str(result) + '\n')
                    record.close()
                    finish = True
        sqloop()
        ballloop()
        pygame.display.update()
        text = "Score " + str(result)
        ttext = "click right button to finish"
        text2 = text1.render(text, True, WHITE, BLACK)
        text4 = text3.render(ttext, True, WHITE, BLACK)
        screen.fill(BLACK)
        screen.blit(text2, (50, 650))
        screen.blit(text4, (50, 720))


game(finished)
pygame.quit()
