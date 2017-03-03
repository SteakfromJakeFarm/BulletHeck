import random
from config import *


class Laser:
    def __init__(self, difficulty):
        self.side = random.randint(0, 3)
        self.min_speed = LASER_MIN_SPEED
        self.multiplier = LASER_MULTIPLIER + (difficulty/5.0)

        if self.side == 0:
            self.cord_x = random.randint(0, 600)
            self.cord_y = -20
        elif self.side == 1:
            self.cord_x = random.randint(0, 600)
            self.cord_y = 620
        elif self.side == 2:
            self.cord_x = -20
            self.cord_y = random.randint(0, 600)
        else:
            self.cord_x = 620
            self.cord_y = random.randint(0, 600)

        self.speed = random.random() * self.multiplier
        if self.speed < self.min_speed:
            self.speed = self.min_speed
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, 10, 10)

    def update(self):
        if self.side == 0:
            self.cord_y += 1 * self.speed
        elif self.side == 1:
            self.cord_y -= 1 * self.speed
        elif self.side == 2:
            self.cord_x += 1 * self.speed
        elif self.side == 3:
            self.cord_x -= 1 * self.speed
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, 10, 10)
