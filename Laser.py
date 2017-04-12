import pygame
import random
from config import *


class Laser:
    def __init__(self, difficulty):
        self.side = random.randint(0, 3)
        self.min_speed = LASER_SPEED_START
        self.speed = random.random() * (difficulty * LASER_SPEED_ADD + LASER_SPEED_START)
        if self.speed < LASER_MIN_SPEED:
            self.speed = LASER_MIN_SPEED

        if self.side == 0:
            self.cord_x = random.randint(0, 600)
            self.cord_y = random.randint(-40, -10)
        elif self.side == 1:
            self.cord_x = random.randint(0, 600)
            self.cord_y = random.randint(600, 640)
        elif self.side == 2:
            self.cord_x = random.randint(-40, -10)
            self.cord_y = random.randint(0, 600)
        else:
            self.cord_x = random.randint(600, 640)
            self.cord_y = random.randint(0, 600)

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
