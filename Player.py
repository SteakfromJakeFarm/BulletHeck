import pygame
import math
import time
import Bomb
from config import *


class Player:
    def __init__(self, x, y, shots):
        self.cord_x = x
        self.cord_y = y
        self.size_x, self.size_y = (10, 10)
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, self.size_x, self.size_y)
        self.shots = shots
        self.adjusted_color = COLOR_PLAYER
        self.debug = False
        self.collide = True
        self.burst_shot_cooldown = 2
        self.shot_size = (5, 5)
        self.last_burst_shot_time = time.time() - self.burst_shot_cooldown
        self.bomb_cooldown = 1.25
        self.last_bomb_time = time.time() - self.bomb_cooldown
        if self.debug == False:
            self.shot_cooldown = PLAYER_SHOOT_COOLDOWN
            self.shot_speed = PLAYER_SHOT_SPEED
            self.speed = PLAYER_SPEED
            self.collide = True
        else:
            self.shot_cooldown = DEBUG_PLAYER_SHOOT_COOLDOWN
            self.shot_speed = DEBUG_PLAYER_SHOT_SPEED
            self.speed = DEBUG_PLAYER_SPEED
            self.collide = False
        self.last_shot_time = 0
        self.powerup = 0
        self.powerup_time = 0
        self.powerup_duration = 0

    def movement(self):
        pressed = pygame.key.get_pressed()
        if (pressed[pygame.K_UP] or pressed[pygame.K_w]) and (pressed[pygame.K_DOWN] or pressed[pygame.K_s]):
            self.cord_y += 1 * self.speed
        elif (pressed[pygame.K_LEFT] or pressed[pygame.K_a]) and (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]):
            self.cord_x += 1 * self.speed
        elif (pressed[pygame.K_UP] or pressed[pygame.K_w]) and (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]):
            if self.cord_x < 590 and self.cord_y > 0:
                self.cord_x += math.cos(math.pi/4) * self.speed
                self.cord_y -= math.sin(math.pi/4) * self.speed
        elif (pressed[pygame.K_UP] or pressed[pygame.K_w]) and (pressed[pygame.K_LEFT] or pressed[pygame.K_a]):
            if self.cord_x > 0 and self.cord_y > 0:
                self.cord_x -= math.cos(math.pi/4) * self.speed
                self.cord_y -= math.sin(math.pi/4) * self.speed
        elif (pressed[pygame.K_DOWN] or pressed[pygame.K_s]) and (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]):
            if self.cord_x < 590 and self.cord_y < 590:
                self.cord_x += math.cos(math.pi/4) * self.speed
                self.cord_y += math.sin(math.pi/4) * self.speed
        elif (pressed[pygame.K_DOWN] or pressed[pygame.K_s]) and (pressed[pygame.K_LEFT] or pressed[pygame.K_a]):
            if self.cord_x > 0 and self.cord_y < 590:
                self.cord_x -= math.cos(math.pi/4) * self.speed
                self.cord_y += math.sin(math.pi/4) * self.speed
        elif pressed[pygame.K_UP] or pressed[pygame.K_w]:
            if self.cord_y > 0:
                self.cord_y -= 1 * self.speed
        elif pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            if self.cord_y < 590:
                self.cord_y += 1 * self.speed
        elif pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            if self.cord_x < 590:
                self.cord_x += 1 * self.speed
        elif pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            if self.cord_x > 0:
                self.cord_x -= 1 * self.speed
        else:
            pass

    def shoot(self, mouse_x, mouse_y, shot):
        if time.time() >= self.last_shot_time + self.shot_cooldown:
            player_bullet = shot(mx=mouse_x, my=mouse_y, px=self.cord_x, py=self.cord_y, speed=self.shot_speed, size=self.shot_size)
            self.shots.append(player_bullet)
            self.last_shot_time = time.time()

    # This fires bullets in equal angles from each other
    def shoot_spray(self, parts, shot, frame):
        if self.powerup == 1:
            j = 0.0
            for i in range(0, parts, 1):
                j += math.pi / math.radians(parts)
                player_bullet = shot(angle=j, speed=self.shot_speed, px=self.cord_x, py=self.cord_y, size=self.shot_size)
                self.shots.append(player_bullet)
            self.powerup = 0

    def shoot_angle(self, angle, shot):
        player_bullet = shot(angle=angle, px=self.cord_x, py=self.cord_y, speed=self.shot_speed, size=self.shot_size)
        self.shots.append(player_bullet)

    def shoot_burst(self, mx, my, shot):
        if time.time() >= self.last_burst_shot_time + self.burst_shot_cooldown:
            angle = math.atan2((my - self.cord_y), (mx - self.cord_x))
            player_bullet = shot(angle=angle, px=self.cord_x, py=self.cord_y, speed=self.shot_speed, size=self.shot_size)
            self.shots.append(player_bullet)
            for i in range(1, 3, 1):
                angle = math.atan2((my - self.cord_y), (mx - self.cord_x)) + math.radians(i*5)
                player_bullet = shot(angle=angle, px=self.cord_x, py=self.cord_y, speed=self.shot_speed, size=self.shot_size)
                self.shots.append(player_bullet)
            for i in range(1, 3, 1):
                angle = math.atan2((my - self.cord_y), (mx - self.cord_x)) - math.radians(i*5)
                player_bullet = shot(angle=angle, px=self.cord_x, py=self.cord_y, speed=self.shot_speed, size=self.shot_size)
                self.shots.append(player_bullet)
            self.last_burst_shot_time = time.time()

    def update(self, bombs):
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, self.size_x, self.size_y)
        if self.powerup > 0 and (time.time() >= self.powerup_time + self.powerup_duration):
            self.powerup = 0
        if self.powerup == 6:
            self.drop_bomb(bombs)

    def refresh_debug(self):
        if not self.debug:
            self.shot_cooldown = PLAYER_SHOOT_COOLDOWN
            self.shot_speed = PLAYER_SHOT_SPEED
            self.speed = PLAYER_SPEED
            if self.powerup == 4:
                self.collide = False
            else:
                self.collide = True
        else:
            self.shot_cooldown = DEBUG_PLAYER_SHOOT_COOLDOWN
            self.shot_speed = DEBUG_PLAYER_SHOT_SPEED
            self.speed = DEBUG_PLAYER_SPEED
            self.collide = False

    def give_powerup(self, powerup_id, duration=1):
        self.powerup = powerup_id
        self.powerup_duration = duration
        self.powerup_time = time.time()

    def drop_bomb(self, bombs):
        if time.time() >= self.last_bomb_time + self.bomb_cooldown:
            new_bomb = Bomb.Bomb(self.cord_x, self.cord_y, 5)
            bombs.append(new_bomb)
            self.last_bomb_time = time.time()