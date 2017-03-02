import random
import pygame
import math
import time


class Laser:
    def __init__(self, min_speed, multiplier):
        self.side = random.randint(0, 3)

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

        self.speed = random.random() * multiplier
        if self.speed < min_speed:
            self.speed = min_speed
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


class Player:
    def __init__(self, shot_cooldown, speed, shot_speed, x, y):
        self.cord_x = x
        self.cord_y = y
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, 10, 10)
        self.shots = []
        self.shot_cooldown = shot_cooldown
        self.shot_speed = shot_speed
        self.last_shot_time = 0
        self.speed = speed
        self.powerup = 0
        self.last_powerup_time = 0
        self.last_powerup_duration = 0

    def movement(self):
        pressed = pygame.key.get_pressed()
        if (pressed[pygame.K_UP] or pressed[pygame.K_w]) and (pressed[pygame.K_DOWN] or pressed[pygame.K_s]):
            pass
        elif (pressed[pygame.K_LEFT] or pressed[pygame.K_a]) and (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]):
            pass
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

    def shoot(self, mouse_x, mouse_y):
        if time.time() >= self.last_shot_time + self.shot_cooldown:
            player_bullet = Shot(mouse_x, mouse_y, self.cord_x, self.cord_y, self.shot_speed)
            self.shots.append(player_bullet)
            self.last_shot_time = time.time()

    # This fires bullets in equal angles from eachother
    def shoot_spray(self, parts):
        if self.powerup == 1:
            temp = self.shot_cooldown
            self.shot_cooldown = 0.0
            j = 0.0
            for i in range(0, 12, 1):
                j += math.pi / parts
                self.shoot_angle(j)
            self.shot_cooldown = temp

    def update(self):
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, 10, 10)
        if self.powerup > 0 and (time.time() >= self.last_powerup_time + self.last_powerup_duration):
            self.powerup = 0
        if self.powerup == 1:
            self.shoot_spray(6)

    def shoot_angle(self, angle):
        if time.time() >= self.last_shot_time + self.shot_cooldown:
            player_bullet = SpinShot(angle, self.cord_x, self.cord_y, self.shot_speed)
            self.shots.append(player_bullet)
            self.last_shot_time = time.time()


class Shot:
    def __init__(self, mouse_x, mouse_y, player_x, player_y, speed):
        self.cord_x = player_x
        self.cord_y = player_y
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.hurtbox = pygame.Rect(self.cord_x, self.cord_y, 5, 5)
        self.angle = 0
        self.speed = speed
        self.calc_angle()

    def calc_angle(self):
        try:
            self.angle = math.atan2((self.mouse_y - self.cord_y), (self.mouse_x - self.cord_x))
        except ZeroDivisionError:
            self.angle = math.pi/2

    def movement(self):
        self.cord_y += math.sin(self.angle) * self.speed
        self.cord_x += math.cos(self.angle) * self.speed

    def update(self):
        self.hurtbox = pygame.Rect(self.cord_x, self.cord_y, 5, 5)


class SpinShot(Shot):
    def __init__(self, angle, player_x, player_y, speed):
        self.cord_x = player_x
        self.cord_y = player_y
        self.hurtbox = pygame.Rect(self.cord_x, self.cord_y, 5, 5)
        self.angle = angle
        self.speed = speed


class PowerUp:
    def __init__(self, id):
        self.id = id
        self.cord_x = random.randint(0, 590)
        self.cord_y = random.randint(0, 590)
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, 15, 15)
