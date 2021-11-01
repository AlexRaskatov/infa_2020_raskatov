import math
from random import choice, randint

import pygame

FPS = 60

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600

G = 2.5


# ускорение свободного падения

class Counter:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def count(self, points):
        front = pygame.font.Font(None, 100)
        text = front.render('points: ' + str(points), True, (0, 0, 0))
        self.screen.blit(text, (400, 300))
        print(points)


class Rocket:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.live = 120
        self.an = 0
        self.rocket_surf = pygame.image.load('rocket_3.png')
        self.rocket_surf_clean = rocket_surf.copy()
        self.rocket_rect = rocket_surf.get_rect()

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение ракеты за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на ракету,
        и стен по краям окна.
        """
        self.x += self.vx
        self.y -= self.vy - G / 2
        self.vy -= G
        self.live -= 1
        if self.x + self.r >= WIDTH or self.x - self.r <= 0:
            self.vx = 0
        if self.y - self.r <= 0 or self.y + self.r >= HEIGHT:
            self.vy = 0


    def draw(self):
        self.an = 28.66*math.atan2(self.vy, self.vx) - 90
        self.rocket_rect = self.rocket_surf.get_rect(center=(self.x, self.y))
        self.rocket_surf = pygame.transform.rotozoom(self.rocket_surf_clean, self.an, 1)
        self.screen.blit(self.rocket_surf, self.rocket_rect)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj."""

        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 < (self.r + obj.r) ** 2:
            return True
        else:
            return False


class Ball:
    def __init__(self, screen: pygame.Surface, x, y):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 120

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        if self.x + self.r > WIDTH or self.x - self.r < 0:
            self.vx = -self.vx
        if self.y - self.r < 0 or self.y + self.r > HEIGHT:
            self.vy = -self.vy
        self.x += self.vx
        self.y -= self.vy - G / 2
        self.vy -= G
        self.live -= 1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (int(self.x), int(self.y)),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 < (self.r + obj.r) ** 2:
            return True
        else:
            return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 20
        self.y = 450

    def move(self, event):
        if event.key == pygame.K_LEFT:
            self.x -= 5
        if event.key == pygame.K_RIGHT:
            self.x += 5

    def fire2_start_ball(self, event):
        self.f2_on = 1

    def fire2_start_rocket(self, event):
        self.f2_on = 1

    def fire2_end_ball(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x, self.y)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an) / 2
        new_ball.vy = - self.f2_power * math.sin(self.an) / 2
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def fire2_end_rocket(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global rocket, bullet
        bullet += 1
        new_rocket = Rocket(self.screen)
        new_rocket.r += 5
        self.an = math.atan2((event.pos[1] - new_rocket.y), (event.pos[0] - new_rocket.x))
        new_rocket.vx = self.f2_power * math.cos(self.an) / 2
        new_rocket.vy = - self.f2_power * math.sin(self.an) / 2
        rocket.append(new_rocket)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2(event.pos[1] - 450, event.pos[0] - 20)
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    """def draw(self):
        # FIXIT don't know how to do it
        d = 10
        y1 = - d * (math.cos(self.an) + math.sin(self.an))
        x1 = d * (- math.cos(self.an) + math.sin(self.an))
        y2 = d * (math.cos(self.an) - math.sin(self.an))
        x2 = -  d * (math.cos(self.an) + math.sin(self.an))
        y3 = d * (math.cos(self.an) + math.sin(self.an)) + self.f2_power * math.sin(self.an)
        x3 = d * (math.cos(self.an) - math.sin(self.an)) + self.f2_power * math.cos(self.an)
        y4 = d * (- math.cos(self.an) + math.sin(self.an)) + self.f2_power * math.sin(self.an)
        x4 = d * (math.cos(self.an) + math.sin(self.an)) + self.f2_power * math.cos(self.an)
        pygame.draw.polygon(
            self.screen,
            self.color,
            [
                [self.x + x1, self.y + y1],
                [self.x + x2, self.y + y2],
                [self.x + x3, self.y + y3],
                [self.x + x4, self.y + y4]
            ]
        )
    """
    def draw(self):
        

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def __init__(self, screen):
        self.screen = screen
        self.live = 1
        self.points = 0
        self.color = RED
        self.x = randint(600, 780)
        self.vx = randint(-10, 10)
        self.y = randint(300, 550)
        self.vy = randint(-10, 10)
        self.r = randint(10, 50)

    def new_target(self):
        """ Инициализация новой цели. """
        self.live = 1
        self.x = randint(600, 780)
        self.vx = randint(-10, 10)
        self.y = randint(300, 550)
        self.vy = randint(-10, 10)
        self.r = randint(10, 50)
        self.color = RED

    def move(self):
        """Переместить цель по прошествии единицы времени."""
        # FIXME
        if self.x + self.r > WIDTH or self.x - self.r < 0:
            self.vx = -self.vx
        if self.y - self.r < 0 or self.y + self.r > HEIGHT:
            self.vy = -self.vy
        self.x += self.vx
        self.y -= self.vy

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points
        return self.points

    def draw(self):
        """рисование цели"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (int(self.x), int(self.y)),
            int(self.r)
        )

    def position(self):
        return [self.x, self.y]

class Target_2:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def __init__(self, screen):
        self.screen = screen
        self.live = 1
        self.points = 0
        self.color = GREEN
        self.x = WIDTH//2
        self.vx = randint(-10, 10)
        self.y = HEIGHT//2
        self.vy = randint(-10, 10)
        self.r = randint(10, 50)

    def new_target(self):
        """ Инициализация новой цели. """
        self.live = 1
        self.x = WIDTH//2
        self.vx = randint(-10, 10)
        self.y = HEIGHT//2
        self.vy = randint(-10, 10)
        self.r = randint(2, 50)
        self.color = GREEN

    def move(self):
        """Переместить цель по прошествии единицы времени."""
        # FIXME
        if self.x + self.r > WIDTH-100 or self.x - self.r < 100:
            self.vx = -self.vx
        if self.y - self.r < 100 or self.y + self.r > HEIGHT-100:
            self.vy = -self.vy
        self.x += self.vx
        self.y -= self.vy
        self.vx += randint(-2, 2)
        self.vy += randint(-2, 2)
        if abs(self.vx) > 10 or abs(self.vy) > 10:
            self.vx = 0
            self.vy = 0

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points
        return self.points

    def draw(self):
        """рисование цели"""
        pygame.draw.circle(
            self.screen,
            self.color,
            (int(self.x), int(self.y)),
            int(self.r)
        )

    def position(self):
        return [self.x, self.y]


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
rocket = []

clock = pygame.time.Clock()
gun = Gun(screen)
target_1 = Target(screen)
target_2 = Target(screen)
target2_1 = Target_2(screen)
counter = Counter(screen)
finished = False

rocket_surf = pygame.image.load('rocket_3.png')
rocket_rect = rocket_surf.get_rect()

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target_1.draw()
    target_2.draw()
    target2_1.draw()
    for b in balls:
        b.draw()
    for r in rocket:
        r.draw()

    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                gun.fire2_start_ball(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                gun.fire2_start_rocket(event)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                gun.fire2_end_ball(event)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                gun.fire2_end_rocket(event)
        if event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        if event.type == pygame.KEYDOWN:
            gun.move(event)

    target_1.move()
    target_2.move()
    target2_1.move()

    clock.tick(FPS * 3)

    for b in balls:
        b.move()
        if b.hittest(target_1) and target_1.live:
            target_1.live = 0
            points = target_1.hit()
            counter.count(points)
            target_1.new_target()
        if b.hittest(target_2) and target_2.live:
            target_2.live = 0
            points = target_2.hit()
            counter.count(points)
            target_2.new_target()
        if b.live == 0:
            balls.remove(b)

    for r in rocket:
        r.move()
        if r.hittest(target_1) and target_1.live:
            target_1.live = 0
            points = target_1.hit()
            counter.count(points)
            target_1.new_target()
        if r.hittest(target_2) and target_2.live:
            target_2.live = 0
            points = target_2.hit()
            counter.count(points)
            target_2.new_target()
        if r.hittest(target2_1) and target2_1.live:
            target2_1.live = 0
            points = target2_1.hit()
            counter.count(points)
            target2_1.new_target()
        if r.live == 0:
            rocket.remove(r)
        if r.vx == 0 and r.vy == 0:
            rocket.remove(r)

    gun.power_up()

pygame.quit()
