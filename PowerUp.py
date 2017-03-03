import pygame
import random


class PowerUp:
    def __init__(self, id):
        self.id = id
        self.cord_x = random.randint(0, 590)
        self.cord_y = random.randint(0, 590)
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, 15, 15)
