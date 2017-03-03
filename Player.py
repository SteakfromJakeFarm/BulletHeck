import math
import time
from config import *


class Player:
    def __init__(self, x, y, debug):
        self.cord_x = x
        self.cord_y = y
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, 10, 10)
        self.shots = []
        if not debug:
            self.shot_cooldown = PLAYER_SHOOT_COOLDOWN
            self.shot_speed = PLAYER_SHOT_SPEED
            self.speed = PLAYER_SPEED
        else:
            self.shot_cooldown = DEBUG_PLAYER_SHOOT_COOLDOWN
            self.shot_speed = DEBUG_PLAYER_SHOT_SPEED
            self.speed = DEBUG_PLAYER_SPEED
        self.last_shot_time = 0
        self.powerup = 0
        self.last_powerup_time = 0
        self.last_powerup_duration = 0

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
            player_bullet = shot(mx=mouse_x, my=mouse_y, px=self.cord_x, py=self.cord_y, speed=self.shot_speed)
            self.shots.append(player_bullet)
            self.last_shot_time = time.time()

    # This fires bullets in equal angles from each other
    def shoot_spray(self, parts, shot):
        if self.powerup == 1:
            j = 0.0
            for i in range(0, 12, 1):
                j += math.pi / parts
                player_bullet = shot(angle=j, speed=self.shot_speed, px=self.cord_x, py=self.cord_y)
                self.shots.append(player_bullet)

    def shoot_angle(self, angle, shot):
        player_bullet = shot(angle=angle, px=self.cord_x, py=self.cord_y, speed=self.shot_speed)
        self.shots.append(player_bullet)

    def update(self):
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, 10, 10)
        if self.powerup > 0 and (time.time() >= self.last_powerup_time + self.last_powerup_duration):
            self.powerup = 0
