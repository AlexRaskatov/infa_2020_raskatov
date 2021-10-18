import pygame
from pygame.draw import *
from random import randint
import datetime

now = datetime.datetime.now()
pygame.init()
pygame.display.set_caption('epileptic hell')

FPS = 50
screen_width = 1200
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (randint(0,70), randint(0, 70), randint(0, 70))
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

balls = [[0, 0, 0, 0, 0] for i in range(6)]
'''[x, y, v_x, v_y, r] - coordinates and speeds'''

rects = [[0, 0, 0, 0, 0, 0] for i in range(6)]
'''[x of center, y of center, v_x, v_y, size, speed of size]'''


def new_rect(delay):
    '''
    draw new rects
    '''
    global FPS, point, Time, rects, record
    Time = 0
    point = 0
    color = 0
    if delay % FPS == 0:
        for elem in rects:
            elem[0] = randint(105, 1095)
            elem[1] = randint(105, 795)
            elem[2] = ((-1) ** (elem[0] % 2)) * randint(5, 10)
            elem[3] = ((-1) ** (elem[1] % 2)) * randint(5, 10)
            elem[4] = randint(50, 100)
            elem[5] = randint(5, 10)
            rect(screen,
                 COLORS[color],
                 (elem[0] - elem[4]//2, elem[1] - elem[4]//2, elem[4], elem[4]))
            color += 1
    else:
        for elem in rects:
            rect(screen,
                COLORS[color],
                (elem[0] - elem[4]//2, elem[1] - elem[4]//2, elem[4], elem[4]))
            color += 1

def rect_motion():
    '''
    move rects
    '''
    global Time, rects
    Time += 1
    color = 0
    for elem in rects:
        if elem[0] + elem[4]//2 > screen_width or elem[0] - elem[4]//2 < 1:
            elem[2] = -elem[2]
        if elem[1] - elem[4]//2 < 1 or elem[1] + elem[4]//2 > screen_height:
            elem[3] = -elem[3]
        if elem[4] > 180 or elem[4] < 20:
            elem[5] = -elem[5]
        elem[0] += elem[2]
        elem[1] += elem[3]
        elem[4] += elem[5]
        rect(screen,
             COLORS[color],
             (elem[0] - elem[4] // 2, elem[1] - elem[4] // 2, elem[4], elem[4]))
        color += 1

def click_rects(event, points):
    '''
    checking the ball hit
    event - mousebottondown
    points - points for hitting
    '''
    for elem in rects:
        if elem[0]-elem[4]//2 < event.pos[0] < elem[0]+elem[4]//2 and elem[1]-elem[4]//2 < event.pos[1] < elem[1]+elem[4]//2:
            k = 1
            return  2
        else:
            k = -1
    if k == -1:
        return -1

def new_ball(delay):
    '''
    draw new ball
    '''
    global FPS, point, Time, balls
    Time = 0
    point = 0
    color = 0
    if delay % FPS == 0:
        for elem in balls:
            elem[0] = randint(105, 1095)
            elem[1] = randint(105, 795)
            elem[2] = ((-1)**(elem[0] % 2))*randint(5,10)
            elem[3] = ((-1)**(elem[1] % 2))*randint(5, 10)
            elem[4] = randint(50, 100)
            circle(screen, COLORS[color], (elem[0], elem[1]), elem[4])
            color += 1
    else:
        for elem in balls:
            circle(screen, COLORS[color], (elem[0], elem[1]), elem[4])
            color += 1

def ball_motion():
    '''
    moves a ball
    '''
    global Time, balls
    Time += 1
    color = 0
    for elem in balls:
        if elem[0] > screen_width - elem[4] or elem[0] < elem[4]:
            elem[2] = -elem[2]
        if elem[1] < elem[4] or elem[1] > screen_height - elem[4]:
            elem[3] = -elem[3]
        elem[0] += elem[2]
        elem[1] += elem[3]
        circle(screen, COLORS[color], (elem[0], elem[1]), elem[4])
        color += 1

def click_ball(event, points):
    '''
    checking the ball hit
    event - mousebottondown
    points - points for hitting
    '''
    for elem in balls:
        if (event.pos[0]-elem[0])**2 + (event.pos[1]-elem[1])**2 < elem[4]**2:
            k = 1
            return 1
        else:
            k = -1
    if k == -1:
        return -1

def counter(points):
    '''counter'''
    front = pygame.font.Font(None, 50)
    text = front.render('points: ' + str(points), True, (255, 255, 255))
    screen.blit(text, (1000, 30))

def time():
    '''time counter'''
    front = pygame.font.Font(None, 50)
    text = front.render('time: ' + str(Time/FPS), True, (255, 255, 255))
    screen.blit(text, (1000, 100))

def records(point):
    global now
    file_read = open('record.txt', 'r')
    file_append = open('record.txt', 'a')
    strings = file_read.readlines()
    if int(strings[-1]) > point:
        file_append.write(now.strftime("%d-%m-%Y %H:%M"))
        file_append.write('\n')
        file_append.write(record)





pygame.display.update()
clock = pygame.time.Clock()
finished = False

point = 0
record = 0
delta_point_ball, delta_point_rect = 0, 0
Time = 0
delay = 0

screen.fill(BLACK)

while not finished:

    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            delta_point_ball = click_ball(event, point)
            delta_point_rect = click_rects(event, point)
    point += max(delta_point_ball, delta_point_rect)

    if max(delta_point_ball, delta_point_rect) == -1 or point == 0:
        record = point
        delay += 1
        new_ball(delay)
        new_rect(delay)
    else:
        ball_motion()
        rect_motion()

    delta_point_ball, delta_point_rect = 0, 0
    counter(point)
    time()
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()