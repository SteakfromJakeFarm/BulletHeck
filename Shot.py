from config import *
import pygame
import math


class Shot:
    def __init__(self, shot_list, angle=False, mx=0, my=0, px=0, py=0, speed=3, size=(5, 5),
                 distance=-1, color=COLOR_SHOT, owner='player'):
        self.cord_x = px
        self.cord_y = py
        self.init_cord_x = px
        self.init_cord_y = py
        self.shot_list=shot_list
        self.mouse_x = mx
        self.mouse_y = my
        self.color = color
        self.size_x, self.size_y = size
        self.hurtbox = pygame.Rect(self.cord_x, self.cord_y, self.size_x, self.size_y)
        self.angle = angle
        self.speed = speed
        self.distance = distance
        self.owner = owner
        if not self.angle:
            self.calc_angle()

    def calc_angle(self):
        try:
            self.angle = math.atan2((self.mouse_y - self.cord_y), (self.mouse_x - self.cord_x))
        except ZeroDivisionError:
            self.angle = math.pi/2

    def movement(self, time_state):
        if time_state == 1:
            temp_speed = self.speed * SPEED_SLOW
        elif time_state == 2:
            temp_speed = self.speed * SPEED_FAST
        else:
            temp_speed = self.speed
        if self.distance == -1:
            self.cord_y += math.sin(self.angle) * temp_speed
            self.cord_x += math.cos(self.angle) * temp_speed
        elif (self.cord_x-self.init_cord_x)**2 + (self.cord_y-self.init_cord_y)**2 >= self.distance**2:
            self.shot_list.remove(self)
        else:
            self.cord_y += math.sin(self.angle) * temp_speed
            self.cord_x += math.cos(self.angle) * temp_speed

    def update(self):
        self.hurtbox = pygame.Rect(self.cord_x, self.cord_y, self.size_x, self.size_y)
        pygame.draw.circle(SCREEN, self.color, (int(self.cord_x), int(self.cord_y)), int(self.size_x/2), 0)
