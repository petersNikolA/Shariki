import pygame
from pygame.draw import *
from random import randint

pygame.init()

FPS = 30
screen = pygame.display.set_mode((1000, 800))

name = input('write your name')
"""
you need to click right button in order to add you result to results table
"""
level = int(input('difficulty level 1-3'))
'''
1 - the easiest 
3 - the hardest (more balls)
'''
result = 0
missed = 0

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

text1 = pygame.font.Font(None, 100)
text3 = pygame.font.Font(None, 100)

liv = []
color1 = []
x = []
y = []
r = []
color = []
speed_x = []
speed_y = []
n = []
level1 = level * 5
a = []
xs = []
ys = []
ay = []
ax = []
speed_xs = []
speed_ys = []


def generator():
    """
    generates random parameters for balls and squares
    :return: x, y - coordinates; r - size; speed_x, speed_y - axial speed of balls
            xs, ys - coordinates, a - size, speed_xs, speed_ys - axial speed of squares
            ax, ay - axial acceleration of squares
    """
    for j in range(level1):
        n.append(0)
        x.append(randint(100, 700))
        y.append(randint(100, 500))
        r.append(randint(30, 50))
        color.append(COLORS[randint(0, 7)])
        speed_x.append(randint(-20, 20))
        speed_y.append(randint(-20, 20))
    for q in range(level):
        liv.append(level * 2)
        color1.append(COLORS[randint(0, 7)])
        a.append(randint(60, 80))
        xs.append(randint(100, 700))
        ys.append(randint(100, 500))
        speed_xs.append(randint(-20, 20))
        speed_ys.append(randint(-20, 20))
        ax.append(randint(-2, 2))
        ay.append(randint(-2, 2))


def test():
    """
    deletes 0 speed and acceleration
    :return: new speed
    """
    for d in range(level1):
        if speed_x[d] == 0:
            speed_x[d] += 5
        if speed_y[d] == 0:
            speed_y[d] -= 5
    for h in range(level):
        if speed_xs[h] == 0:
            speed_xs[h] -= 10
        if speed_ys[h] == 0:
            speed_ys[h] += 10
        if ax[h] == 0:
            ax[h] += 1
        if ay[h] == 0:
            ay[h] -= 1


def balls():
    """
    balls' moving
    :return: new position
    """
    for m in range(level1):
        x[m] += speed_x[m]
        y[m] += speed_y[m]
        circle(screen, color[m], (x[m], y[m]), r[m])


def square():
    """
    squares' moving
    :return: new position
    """
    for s in range(level):
        speed_xs[s] += ax[s]
        speed_ys[s] += ay[s]
        xs[s] += speed_xs[s]
        ys[s] += speed_ys[s]
        rect(screen, color1[s], (xs[s], ys[s], a[s], a[s]))


def counter():
    """
    checks hitting the target
    :return: updates remaining number of hits for squares (liv)
             number of hits for balls
    """
    s = pygame.mouse.get_pos()
    x1 = s[0]
    y1 = s[1]
    for k in range(level1):
        p = ((x1 - x[k]) ** 2 + (y1 - y[k]) ** 2) ** (1 / 2)
        if p <= float(r[k]):
            n[k] = 1
    for u in range(level):
        if (x1 >= xs[u]) and (x1 <= (xs[u] + a[u])) and (y1 >= ys[u]) and (y1 <= (ys[u] + a[u])):
            liv[u] -= 1
            color1[u] = COLORS[randint(0, 7)]


def controller():
    """
    controls the location of all balls and squares within the boundaries
    changes the direction of the speed
    :return: new speed
    """
    for l in range(level1):
        if x[l] + r[l] >= 800 or x[l] - r[l] <= 50:
            speed_x[l] *= -1
        if y[l] + r[l] >= 600 or y[l] - r[l] <= 50:
            speed_y[l] *= -1
    for z in range(level):
        if abs(speed_xs[z]) >= 30:
            if speed_xs[z] > 0:
                speed_xs[z] = 30
            else:
                speed_xs[z] = -30
        if abs(speed_ys[z]) >= 30:
            if speed_ys[z] > 0:
                speed_ys[z] = 30
            else:
                speed_ys[z] = -30
        if xs[z] + a[z] >= 800 or xs[z] <= 50:
            speed_xs[z] *= -1
            xs[z] += speed_xs[z]
        if ys[z] + a[z] >= 600 or ys[z] <= 50:
            speed_ys[z] *= -1
            ys[z] += speed_ys[z]


def remover():
    """
    deletes hitted balls and squares
    """
    for p in range(level1):
        if n[p] == 1:
            x[p] = 0
            y[p] = 0
            r[p] = 0
    for v in range(level):
        if liv[v] <= 0:
            xs[v] = 0
            ys[v] = 0
            a[v] = 0


def new_circle():
    """
    update for counter
    """
    for t in range(level1):
        n[t] = 0
    for b in range(level):
        if liv[b] == 0:
            liv[b] = -1


rect(screen, WHITE, (50, 50, 750, 550))
generator()
test()

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    rect(screen, WHITE, (50, 50, 750, 550))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                counter()
                for i in range(level1):
                    result += n[i]
                    for w in range(level):
                        if liv[w] == 0:
                            result += 25
            elif event.button == 3:
                records = open('records.txt', 'a')
                records.write(name + ' : ' + str(result) + '\n')
                records.close()
                finished = True

    balls()
    square()
    controller()
    remover()
    new_circle()
    pygame.display.update()
    text = "Score " + str(result)
    Text = "click right button to finish"
    text2 = text1.render(text, True, WHITE, BLACK)
    text4 = text3.render(Text, True, WHITE, BLACK)
    screen.fill(BLACK)
    screen.blit(text2, (50, 650))
    screen.blit(text4, (50, 720))

pygame.quit()
