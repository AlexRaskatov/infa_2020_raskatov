import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))

yellow = (255, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

#background
rect(screen, white, (0,0, 400, 400))

#body
circle(screen, yellow, (200, 200), 150)
circle(screen, black, (200, 200), 150, 5)

#eye_left
circle(screen, red, (140, 170), 30)
circle(screen, black, (140, 170), 30, 2)
circle(screen, black, (140, 170), 5)
line(screen, black, [100, 130], [190, 150], 7)

#eye_right
circle(screen, red, (260, 170), 20)
circle(screen, black, (260, 170), 20, 2)
circle(screen, black, (260, 170), 5)
line(screen, black, [210,160],[300,140],7)

#lip
line(screen, black, [170,250],[230,250],10)

#



pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()