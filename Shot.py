from config import *
import pygame
import math


class Shot:
    def __init__(self, angle=False, mx=0, my=0, px=0, py=0, speed=1, size=(5, 5), distance=-1, shot_list=True):
        self.cord_x = px
        self.cord_y = py
        self.init_cord_x = px
        self.init_cord_y = py
        self.shot_list=shot_list
        self.mouse_x = mx
        self.mouse_y = my
        self.size_x, self.size_y = size
        self.hurtbox = pygame.Rect(self.cord_x, self.cord_y, self.size_x, self.size_y)
        self.angle = angle
        self.speed = speed
        self.distance=distance
        if not self.angle:
            self.calc_angle()

    def calc_angle(self):
        try:
            self.angle = math.atan2((self.mouse_y - self.cord_y), (self.mouse_x - self.cord_x))
        except ZeroDivisionError:
            self.angle = math.pi/2

    def movement(self):
        if self.distance == -1:
            self.cord_y += math.sin(self.angle) * self.speed
            self.cord_x += math.cos(self.angle) * self.speed
        elif (self.cord_x-self.init_cord_x)**2 + (self.cord_y-self.init_cord_y)**2 >= self.distance**2:
            self.shot_list.remove(self)
        else:
            self.cord_y += math.sin(self.angle) * self.speed
            self.cord_x += math.cos(self.angle) * self.speed

    def update(self):
        self.hurtbox = pygame.Rect(self.cord_x, self.cord_y, self.size_x, self.size_y)
        pygame.draw.circle(SCREEN, COLOR_SHOT, (int(self.cord_x), int(self.cord_y)), int(self.size_x/2), 0)
