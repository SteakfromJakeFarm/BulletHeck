import random
import pygame
import math


class Laser:
    def __init__(self):
        self.side = random.randint(0, 3)

        if self.side == 0:
            self.cord_x = random.randint(0, 600)
            self.cord_y = 0
        elif self.side == 1:
            self.cord_x = random.randint(0, 600)
            self.cord_y = 600
        elif self.side == 2:
            self.cord_x = 0
            self.cord_y = random.randint(0, 600)
        else:
            self.cord_x = 600
            self.cord_y = random.randint(0, 600)

        self.speed = random.random() * 3
        if self.speed < 0.1:
            self.speed = 0.1
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
        else:
            print 'It\'s all broken now...'
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, 10, 10)


class Player:
    def __init__(self):
        self.cord_x = 300
        self.cord_y = 300
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, 10, 10)

    def move_up(self):
        if self.cord_y > 0:
            self.cord_y -= 1

    def move_down(self):
        if self.cord_y < 600:
            self.cord_y += 1

    def move_right(self):
        if self.cord_x < 600:
            self.cord_x += 1

    def move_left(self):
        if self.cord_x > 0:
            self.cord_x -= 1

    def movement(self, key=''):
        if key == pygame.K_UP:
            self.move_up()
        elif key == pygame.K_DOWN:
            self.move_down()
        elif key == pygame.K_RIGHT:
            self.move_right()
        elif key == pygame.K_LEFT:
            self.move_left()
        else:
            pass

    def update(self):
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, 10, 10)