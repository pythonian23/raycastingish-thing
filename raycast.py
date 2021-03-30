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


pygame.init()
wn = pygame.display.set_mode((1280, 720), True, 32)
fps = pygame.time.Clock()
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)
esc = False
circle = (638, 358)
pygame.mouse.set_pos((640, 360))
angle = 1
length = 2000
lines = [((0, 0), (1280, 0)), ((1280, 0), (1280, 720)), ((1280, 720), (0, 720)), ((0, 720), (0, 0))]
lines.append(((0, 0), (320, 180)))
lines.append(((336, 189), (464, 261)))
lines.append(((480, 270), (1280, 720)))
lines.append(((700, 700), (1200, 100)))
movement = [0, 0]
while True:
    rays = []
    for direction in range(0, 360, angle):
        rays.append((round(length * math.cos(direction) + .5) + circle[0],
                     round(length * math.sin(direction) + .5) + circle[1],))
    for point in rays:
        test = point
        for line in lines:
            check = collide((circle, point), line)
            if (test[0] - circle[0]) ** 2 + (test[1] - circle[1]) ** 2 > (check[1][0] - circle[0]) ** 2 + \
                    (check[1][1] - circle[1]) ** 2:
                test = check[1]
        pygame.draw.line(wn, (0, 255, 0), circle, test, 1)
    for line in lines:
        pygame.draw.line(wn, (255, 0, 0), line[0], line[1], 4)
    pygame.draw.circle(wn, (0, 0, 255), circle, 4)
    if not esc:
        circle = (circle[0] + (movement[0]), circle[1] + (movement[1]))
        pygame.mouse.set_pos(640, 360)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_w:
                movement[1] = -2
            if event.key == K_a:
                movement[0] = -2
            if event.key == K_s:
                movement[1] = 2
            if event.key == K_d:
                movement[0] = 2
            if event.key == K_ESCAPE:
                esc = True
                pygame.event.set_grab(False)
                pygame.mouse.set_visible(True)
        if event.type == KEYUP:
            if event.key == K_w:
                movement[1] = 0
            if event.key == K_a:
                movement[0] = 0
            if event.key == K_s:
                movement[1] = 0
            if event.key == K_d:
                movement[0] = 0
        if event.type == MOUSEBUTTONDOWN:
            pygame.event.set_grab(True)
            pygame.mouse.set_visible(False)
            esc = False
            pygame.mouse.set_pos(640, 360)
    pygame.display.update()
    fps.tick(24)
    wn.fill((0, 0, 0))
