import pygame
import random
import math
from config import *


class Laser:
    def __init__(self, difficulty):
        self.side = random.randint(0, 3)
        min_speed = LASER_SPEED_START
        max_speed = random.random() + (difficulty * LASER_SPEED_ADD)
        self.speed = random.uniform(min_speed, max_speed)
        if self.speed < min_speed:
            self.speed = min_speed
        if self.speed < LASER_SPEED_START:
            self.speed = LASER_SPEED_START

        if self.side == 0:
            self.cord_x = random.randint(0, WINDOW_X)
            self.cord_y = random.randint(-100, -10)
        elif self.side == 1:
            self.cord_x = random.randint(0, WINDOW_X)
            self.cord_y = random.randint(WINDOW_Y, WINDOW_Y + 100)
        elif self.side == 2:
            self.cord_x = random.randint(-100, -10)
            self.cord_y = random.randint(0, WINDOW_Y)
        else:
            self.cord_x = random.randint(WINDOW_X, WINDOW_X + 100)
            self.cord_y = random.randint(0, WINDOW_Y)

        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, 10, 10)

    def update(self, time):
        if time == 1:
            temp_speed = self.speed * SPEED_SLOW
        elif time == 2:
            temp_speed = self.speed * SPEED_FAST
        else:
            temp_speed = self.speed
        if self.side == 0:
            self.cord_y += 1 * temp_speed
        elif self.side == 1:
            self.cord_y -= 1 * temp_speed
        elif self.side == 2:
            self.cord_x += 1 * temp_speed
        elif self.side == 3:
            self.cord_x -= 1 * temp_speed
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, 10, 10)
