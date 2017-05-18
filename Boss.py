import random
import time
import pygame

import Shot
from config import *


class Boss:
    def __init__(self, health, firerate):
        self.size_x = 60
        self.size_y = 60
        self.cord_x = (WINDOW_X / 2) - (self.size_x/2)
        self.cord_y = 50
        self.speed = 3
        self.color = COLOR_BOSS
        self.health = health
        self.firerate = firerate
        self.shots = []
        self.timers = {
            "movement": time.time(),
        }
        self.cooldowns = {
            "movement": 0.4,
        }
        self.current_direction = 1
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, self.size_x, self.size_y)

    def movement(self, time_state):
        if time_state == 1:
            temp_speed = self.speed * SPEED_SLOW
        elif time_state == 2:
            temp_speed = self.speed * SPEED_FAST
        else:
            temp_speed = self.speed
        if self.timers["movement"] + self.cooldowns["movement"] <= time.time():
            self.current_direction = random.randint(1, 2)
            self.timers["movement"] = time.time()
        if self.current_direction == 1:
            self.cord_x += temp_speed
        elif self.current_direction == 2:
            self.cord_x -= temp_speed
        if self.cord_x <= 0:
            self.cord_x = 0
        if self.cord_x >= WINDOW_X - self.size_x:
            self.cord_x = WINDOW_X - self.size_x

    def hurt(self, dmg=1):
        self.health -= dmg

    def shoot(self, player_obj):
        shot = Shot.Shot(self.shots, mx=player_obj.cord_x, my=player_obj.cord_y,
                         px=self.cord_x, py=self.cord_y, size=(15, 15), color=(0, 0, 255), owner='Steven')
        self.shots.append(shot)

    def update(self, player_obj, time_state):
        if random.random() <= self.firerate:
            self.shoot(player_obj)
        self.movement(time_state)
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, self.size_x, self.size_y)
        pygame.draw.rect(SCREEN, self.color, self.hitbox)
        title = pygame.font.SysFont(FONT, FONT_SIZE).render("Steven", 1, (200, 0, 200))
        SCREEN.blit(title, ((self.cord_x - (len("Steven")/2)), self.cord_y - 30))

