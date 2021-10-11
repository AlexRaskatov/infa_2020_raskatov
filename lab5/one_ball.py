import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 10
screen = pygame.display.set_mode((1200, 900))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (randint(0,70), randint(0, 70), randint(0, 70))
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

v_x, v_y = 10, 10

def new_ball():
    '''
    draw new ball
    x, y - ball`s coordinates
    r - ball`s radius
    '''
    global x, y, r, FPS, point, Time
    Time = 0
    point = 0
    FPS = 0.5
    x = randint(105, 1095)
    y = randint(105, 795)
    r = randint(10, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)

def ball_motion():
    global x, y, v_x, v_y, r, FPS, Time
    FPS = 20
    Time += 5
    if x > 1200 - r or x < r:
        v_x = -v_x
    if y < r or y > 900 - r:
        v_y = -v_y
    x += v_x
    y += v_y
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)

def click_ball(event, x_ball, y_ball, r_ball, points):
    '''
    checking the ball hit
    x_ball, y_ball - ball`s parameters
    event - mousebottondown
    points - points for hitting
    '''
    if (event.pos[0]-x_ball)**2 + (event.pos[1]-y_ball)**2 < r_ball**2:
        return 1
    else:
        return -1


def counter(points):
    '''counter'''
    front = pygame.font.Font(None, 50)
    text = front.render('points: ' + str(points), True, (randint(150, 255), randint(0, 255), randint(0,255)))
    screen.blit(text, (1000, 30))

def time():
    front = pygame.font.Font(None, 50)
    text = front.render('time: ' + str(Time/100), True, (randint(150, 255), randint(0, 255), randint(0,255)))
    screen.blit(text, (1000, 100))



pygame.display.update()
clock = pygame.time.Clock()
finished = False

point = 0
delta_point = 0

Time = 0

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            delta_point = click_ball(event, x, y, r, point)
    point += delta_point
    if delta_point == -1 or point == 0:
        new_ball()
    else:
        ball_motion()
    delta_point = 0
    counter(point)
    time()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()