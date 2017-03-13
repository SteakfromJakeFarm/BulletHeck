from config import *
import pygame
import math


class Shot:
    def __init__(self, angle=False, mx=0, my=0, px=0, py=0, speed=1, size=(5, 5)):
        self.cord_x = px
        self.cord_y = py
        self.mouse_x = mx
        self.mouse_y = my
        self.size_x, self.size_y = size
        self.hurtbox = pygame.Rect(self.cord_x, self.cord_y, self.size_x, self.size_y)
        self.angle = angle
        self.speed = speed
        if not self.angle:
            self.calc_angle()

    def calc_angle(self):
        try:
            self.angle = math.atan2((self.mouse_y - self.cord_y), (self.mouse_x - self.cord_x))
        except ZeroDivisionError:
            self.angle = math.pi/2

    def movement(self):
        self.cord_y += math.sin(self.angle) * self.speed
        self.cord_x += math.cos(self.angle) * self.speed

    def update(self):
        self.hurtbox = pygame.Rect(self.cord_x, self.cord_y, self.size_x, self.size_y)
        pygame.draw.circle(SCREEN, COLOR_SHOT, (int(self.cord_x), int(self.cord_y)), int(self.size_x/2), 0)
