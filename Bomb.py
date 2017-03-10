import pygame
import time
import math
from Shot import Shot


class Bomb:
    def __init__(self, px, py, fuse=5):
        self.color = (0, 0, 0)
        self.fuse = fuse
        self.time_start = time.time()
        self.cord_x = px
        self.cord_y = py
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, 10, 10)

    def tick(self, player_obj, bombs):
        if time.time() >= self.time_start + self.fuse:
            angle = 0
            for i in range(1, 8, 1):
                angle += 360/8
                new_shot = Shot(angle=i, px=self.cord_x, py=self.cord_y)
                player_obj.shots.append(new_shot)
            bombs.remove(self)
