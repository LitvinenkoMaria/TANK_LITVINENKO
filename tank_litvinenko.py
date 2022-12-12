import math
import random

from random import randint as rnd
from math import pi

import pygame
from pygame import draw
from pygame.draw import *


FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (170, 170, 180)
RED = (255, 0, 0)
BLUE = (34, 70, 185)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PINK = (237,76, 153)


WIDTH = 800
HEIGHT = 600

left_key_down = False
right_key_down = False
score = 0


class Ball:
    def __init__(self, screen):
        """
        класс Ball: задаем координаты, радиус, скорость, цвет, время жизни шарика.
        """
        self.screen = screen
        self.x = gun.x1
        self.y = gun.y1
        self.r = 15
        self.vx = 0
        self.vy = 0
        self.color = random.choice([RED, BLUE, YELLOW, GREEN, PINK])
        self.max_age = 100
        self.current_age = 0

    def move(self):
        """ функция перемещает ball; учитываем, чтобы он не вылетел за границы мира """
        if self.x + self.r >= 800:
            self.vx = -self.vx + 10
            self.x = 800 - self.r
        if self.x - self.r <= 0:
            self.vx = -self.vx - 10
            self.x = self.r
        if self.y + self.r >= 600:
            self.vy = -self.vy - 5
            self.y = 600 - self.r
        if self.y - self.r <= 0:
            self.vy = -self.vy + 5
            self.y = self.r
        self.vy -= 2
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        """ функция рисует ball """
        draw.circle(self.screen, self.color, (self.x, self.y), self.r)


    def hittest(self, obj):
        """ Проверка на столкновение ball с обЪектом: если столкнулись, и ball, и обЪект удаляем """
        global bullets, targets
        if self in bullets and (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            bullets.remove(self)
            targets.remove(obj)
            return True
        else:
            return False

    def aging(self):
        """ Ball через некоторое время должен удалиться из массива """
        global bullets
        self.current_age += 1
        if self.current_age > self.max_age:
            bullets = bullets[1:]


class Gun:
    def __init__(self, screen):
        """ класс Gun """
        self.screen = screen
        self.f2_power = 10
        self.f2_on = False #флаг; меняется при прицеливании
        self.an = pi #угол поворота дула
        self.color = BLACK
        self.x1 = 40
        self.y1 = 570
        self.r = 30
        self.x2 = 70
        self.y2 = 550

    def move(self):
        """ С помощью клавиш "стрелочка вправо" и "стрелочка влево" можно двигать дуло """
        global left_key_down, right_key_down
        if left_key_down and self.x1 >= 30:
            self.x1 -= 10
        if right_key_down and self.x1 <= 770:
            self.x1 += 10

    def start(self):
        """ Запускает power_up """
        self.f2_on = True

    def end(self, event):
        """ При отпускании ПКМ из дула вылетает ball """
        global bullet_count, bullets
        
        bullet_count += 1
        new_ball = Ball(self.screen)
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = -self.f2_power * math.sin(self.an)
        bullets.append(new_ball)
        self.f2_on = False
        self.f2_power = 10

    def targetting(self, event):
        """ Двигаем мышь -> можем прицеливаться """
        if event.pos[0] == self.x1:
            if event.pos[1] < self.y1:
                self.an = 3 * pi / 2
            else:
                self.an = pi / 2
        elif event.pos[0] > self.x1:
            self.an = math.atan((event.pos[1] - self.y1) / (event.pos[0] - self.x1))
        else:
            self.an = pi + math.atan((event.pos[1]-self.y1) / (event.pos[0]-self.x1))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        """ Рисует дуло в зависимоти от координат одного конца, радиуса и угла наклона """
        draw.line(screen, self.color, (self.x1, self.y1), (self.x1 + self.r * math.cos(self.an), self.y1 + self.r * math.sin(self.an)), 10)

    def power_up(self):
        """ При нажатии на ПКМ меняются цвет и размер дула + увеличивается скорость вылета ball """
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 5
                self.r += 4
            self.color = RED
        else:
            self.color = BLACK
            self.r = 30


class Target:
    def __init__(self):
        """ класс Target """
        self.alive = True
        self.screen = pygame.Surface
        self.x = rnd(0, WIDTH - 20)
        self.y = rnd(0, 300)
        self.r = rnd(20, 40)
        
        """С самого начала летит в рандомную сторону:"""
        self.vx = rnd(3, 5) * random.choice([-1, 1]) 
        self.vy = rnd(3, 5) * random.choice([-1, 1])


    def move(self):
        """двигаются немного хаотично"""
        if self.x + self.r >= 800:
            self.vx = -self.vx
            self.x = 800 - self.r
        if self.x - self.r <= 0:
            self.vx = -self.vx
            self.x = self.r
        if self.y + self.r >= 300:
            self.vy = -self.vy
            self.y = 300 - self.r
        if self.y - self.r <= 0:
            self.vy = -self.vy
            self.y = self.r
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        """ Рисует круглые цели"""
        draw.circle(screen, random.choice([RED, YELLOW, GREEN, PINK]), (self.x, self.y), self.r, 0)

    def hit(self):
        """Если попали в цель, то +очко"""
        global score
        
        score += 1

    def spawn_bomb(self):
        """ Цель может сбросить бомбу на танк"""
        global bombs
        if not rnd(0,99):
            new_bomb = Bomb()
            new_bomb.x = self.x
            new_bomb.y = self.y
            bombs.append(new_bomb)


class New_Target(Target):
    def __init__(self):
        """ класс New_Target """
        self.alive = True
        self.screen = pygame.Surface
        self.x = rnd(0, WIDTH - 70)
        self.y = rnd(0, 300)
        self.r = rnd(20, 40)
        self.vx = rnd(3, 5) * random.choice([-1, 1])


    def move(self):
        """
        движение new_target
        """
        if self.x + self.r >= 800:
            self.vx = -self.vx
            self.x = 800 - self.r
        if self.x - self.r <= 0:
            self.vx = -self.vx
            self.x = self.r
        
        self.x += self.vx

    def draw(self):
        """
        Рисует new_target (звёздочка).
        """
        polygon(screen, RED, [(self.x - 40, self.y), (self.x - 14, self.y - 14), (self.x, self.y - 40),
                          (self.x + 14, self.y - 14), (self.x + 40, self.y),
                          (self.x + 14, self.y + 14), (self.x, self.y + 40), (self.x - 14, self.y + 14)])
        polygon(screen, YELLOW, [(self.x - 28, self.y + 28), (self.x - 10, self.y), (self.x - 28, self.y - 28),
                             (self.x, self.y - 10), (self.x + 28, self.y - 28),
                             (self.x + 10, self.y), (self.x + 28, self.y + 28), (self.x, self.y + 10)])




class Tank:
    def __init__(self):
        """ класс Tank """
        self.alive = True
        self.screen = pygame.Surface
        self.r = 10
        self.x = gun.x1
        self.y = gun.y1

    def draw(self):
        """ Рисует танк """
        draw.circle(screen, PINK, (self.x, self.y), self.r)
        draw.circle(screen, BLACK, (self.x, self.y), self.r, 1)
        draw.rect(screen, PINK, (self.x - 30, self.y, 60, 20))
        draw.rect(screen, BLACK, (self.x - 30, self.y, 60, 20), 1)
        draw.rect(screen, BLACK, (self.x - 30, self.y + 20, 60, 7))

    def pos_update(self):
        """ Дуло и танк должны иметь одинаковые координаты """
        self.x = gun.x1
        self.y = gun.y1


class Bomb:
    def __init__(self):
        """ класс Bomb """
        self.r = 10
        self.vy = 4

    def move(self):
        """Движется вниз, если вышла за границы экрана, то ее удаляем """
        global bombs
        self.y += self.vy
        if len(bullets) > 0 and self.y >= HEIGHT:
            bombs.remove(self)

    def draw(self):
        """ Рисует саму бомбу """
        draw.circle(screen, random.choice([RED, YELLOW, GREEN, PINK]), (self.x, self.y), self.r, 0)
        draw.circle(screen, WHITE, (self.x, self.y), self.r - 2, 0)

    def hit_tank(self, obj):
        """ Если бомба попала в танк, то танк умирает"""
        if abs(self.x - obj.x) < 25 and abs(self.y - obj.y) < 25:
            obj.alive = False


def round_target():
    """создание новой круглой цели и добавление ее в список целей"""
    global targets
    
    round_target = Target()
    targets.append(round_target)


def star_target():
    """ создание новой цели в виде звезды и добавление ее в список"""
    global targets
    
    star_target = New_Target()
    targets.append(star_target)


def display_score():
    """ показывает число очков"""
    font = pygame.font.SysFont('Verdana', 26)
    text = font.render('SCORE: ' + str(score) + '', True, BLACK)
    textpos = text.get_rect(centerx = 70, y = 20)
    screen.blit(text, textpos)


def display_results():
    """это если танк умер"""
    rect(screen, WHITE, (tank.x - 35, tank.y - 35, 90, 90))
    rect(screen, GREY, (tank.x - 10, tank.y - 30, 10, 70))
    rect(screen, GREY, (tank.x - 20, tank.y - 20, 30, 10))
    rect(screen, BLACK, (tank.x - 10, tank.y - 30, 10, 70), 1)
    rect(screen, BLACK, (tank.x - 20, tank.y - 20, 30, 10), 1)
    rect(screen, GREEN, (tank.x - 20, tank.y + 26, 30, 10))
    rect(screen, RED, (WIDTH / 2 - 350, HEIGHT / 2 - 40, 700, 100))
    rect(screen, BLACK, (WIDTH / 2 - 350, HEIGHT / 2 - 40, 700, 100), 2)
    font = pygame.font.SysFont('Verdana', 30)
    text = font.render('GAME OVER. YOU HAVE EARNED ' + str(score) + ' POINTS', True, BLACK)
    textpos = text.get_rect(centerx=WIDTH/2, y=HEIGHT/2 - 6)
    screen.blit(text, textpos)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet_count = 0
targets = []
bullets = []
bombs = []

clock = pygame.time.Clock()
gun = Gun(screen)
tank = Tank()

for i in range(6):
    if rnd(0,1):
        round_target()
    else:
        star_target()

finished = False

while not finished:

    if not tank.alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
        display_results()
        pygame.display.update()
    
    else:
        screen.fill(WHITE)
        gun.move()
        gun.draw()
        tank.pos_update()
        tank.draw()
        display_score()
        for target in targets:
            target.spawn_bomb()
            target.move()
            target.draw()
        for bomb in bombs:
            bomb.hit_tank(tank)
            bomb.move()
            bomb.draw()
        for bullet in bullets:
            bullet.aging()
            bullet.draw()
        pygame.display.update()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left_key_down = False
                if event.key == pygame.K_RIGHT:
                    right_key_down = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left_key_down = True
                if event.key == pygame.K_RIGHT:
                    right_key_down = True

            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gun.start()
            elif event.type == pygame.MOUSEBUTTONUP:
                gun.end(event)
            elif event.type == pygame.MOUSEMOTION:
                gun.targetting(event)

        for b in bullets:
            b.move()
            for t in targets:
                if b.hittest(t) and t.alive:
                    t.alive = False
                    t.hit()
                    if rnd(0,1):
                        round_target()
                    else:
                        star_target()
        gun.power_up()

pygame.quit()

