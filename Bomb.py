import pygame
import time
import math
from Shot import Shot


class Bomb:
    def __init__(self, px, py, fuse=1.5):
        self.color = (0, 0, 0)
        self.fuse = fuse
        self.time_start = time.time()
        self.cord_x = px
        self.cord_y = py
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, 10, 10)

    def tick(self, player_obj):
        if time.time() >= self.time_start + self.fuse:
            angle = 0
            for i in range(0, 8, 1):
                angle += 360/8
                new_shot = Shot(angle=math.radians(angle), px=self.cord_x, py=self.cord_y,
                                speed=3.25, size=player_obj.shot_size, distance=75, shot_list=player_obj.shots)
                player_obj.shots.append(new_shot)
            player_obj.bombs.remove(self)
