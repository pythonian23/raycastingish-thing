import pygame
from pygame.locals import *
import math


def collide(l1, l2):
    result = False
    intersection = l1[1]
    out = (result, intersection)
    x1, y1 = l1[0]
    x2, y2 = l1[1]
    x3, y3 = l2[0]
    x4, y4 = l2[1]
    try:
        uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / (((y4 - y3) * (x2 - x1)) - ((x4 - x3) * (y2 - y1)))
        uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / (((y4 - y3) * (x2 - x1)) - ((x4 - x3) * (y2 - y1)))
    except ZeroDivisionError:
        return out
    if (0 <= uA <= 1) and (0 <= uB <= 1):
        result = True
        intersection = (round(x1 + (uA * (x2 - x1)) + .5), round(y1 + (uA * (y2 - y1)) + .5))
    out = (result, intersection)
    return out


rad = math.pi / 180
pygame.init()
wn = pygame.display.set_mode((1280, 720), True, 32)
fps = pygame.time.Clock()
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
esc = False
circle = (638, 358)
pygame.mouse.set_pos((640, 360))
angle = 1
length = 255 * 2
lines = [((0, 0), (1280, 0)), ((1280, 0), (1280, 720)), ((1280, 720), (0, 720)), ((0, 720), (0, 0))]
lines.append(((0, 0), (320, 180)))
lines.append(((336, 189), (464, 261)))
lines.append(((480, 270), (1248, 702)))
lines.append(((700, 700), (1200, 100)))
movement = [0, 0]
a = 0
b = 80
forward = 0
direc = 0
ang = 40
while True:
    loc = 0
    a += direc
    b += direc
    ang += direc
    if a < 0:
        a += 360
    if a >= 360:
        a -= 360
    if b <= 0:
        b += 360
    if b > 360:
        b -= 360
    if ang < 0:
        ang += 360
    if ang >= 360:
        ang -= 360
    rays = []
    for direction in range(0, 360, angle):
        rays.append((round(length * math.cos(direction * rad) + .5) + circle[0],
                     round(length * math.sin(direction * rad) + .5) + circle[1],
                     direction))
    for point in rays:
        test = point
        for line in lines:
            check = collide((circle, (point[0], point[1])), line)
            if (test[0] - circle[0]) ** 2 + (test[1] - circle[1]) ** 2 > (check[1][0] - circle[0]) ** 2 + \
                    (check[1][1] - circle[1]) ** 2:
                test = check[1]
        draw = False
        if a < b:
            if a <= point[2] < b:
                draw = True
        elif a > b:
            if point[2] < b or point[2] >= a:
                draw = True
        if draw:
            col = abs((test[0] - circle[0]) / math.cos(point[2]*rad) / 2)
            if col > 255:
                col = 255
            if col < 0:
                col  = 0
            print(col)
            pygame.draw.rect(wn, (col, col, col), (loc, 0, 16, 30))
            loc += 16
            pygame.draw.line(wn, (0, 0, 255), circle, (test[0], test[1]), 4)
    pygame.draw.circle(wn, (0, 0, 255), (640, 360), 4)
    if not esc:
        temp = [circle[0] + round(forward * math.cos(ang * rad)), circle[1] + round(forward * math.sin(ang * rad))]
        go = True
        for line in lines:
            if collide((circle, temp), line)[0]:
                go = False
        if go:
            circle = temp
        # x = movement[0]
        # y = movement[1]
        # for bound in lines:
        #     if collide((circle, [circle[0] + x, circle[1] + y]), bound)[0]:
        #         x = y = 0
        # circle = (circle[0] + x, circle[1] + y)
        pygame.mouse.set_pos(circle)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_w:
                forward = 3
            if event.key == K_a:
                direc = -5
            if event.key == K_d:
                direc = 5
            if event.key == K_s:
                forward = -3
            # if event.key == K_w:
            #     movement[1] = -2
            # if event.key == K_a:
            #     movement[0] = -2
            # if event.key == K_s:
            #     movement[1] = 2
            # if event.key == K_d:
            #     movement[0] = 2
            if event.key == K_ESCAPE:
                esc = True
                pygame.event.set_grab(False)
                pygame.mouse.set_visible(True)
        if event.type == KEYUP:
            if event.key == K_w:
                forward = 0
            if event.key == K_a:
                direc = 0
            if event.key == K_d:
                direc = 0
            if event.key == K_s:
                forward = 0
            # if event.key == K_w:
            #     movement[1] = 0
            # if event.key == K_a:
            #     movement[0] = 0
            # if event.key == K_s:
            #     movement[1] = 0
            # if event.key == K_d:
            #     movement[0] = 0
        if event.type == MOUSEBUTTONDOWN:
            pygame.event.set_grab(True)
            pygame.mouse.set_visible(False)
            esc = False
            pygame.mouse.set_pos(640, 360)
            movement = [0, 0]
    pygame.display.update()
    fps.tick(24)
    wn.fill((0, 0, 0))
