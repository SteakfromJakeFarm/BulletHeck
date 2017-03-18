# import pygame
import math
import time
import Bomb
import Shot
from config import *


class Player:
    def __init__(self, x, y, shots, bombs):
        self.cord_x = x
        self.cord_y = y
        self.size_x, self.size_y = (10, 10)
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, self.size_x, self.size_y)
        self.shots = shots  # Grab the list of bullets
        self.bombs = bombs  # Grab the list of bombs
        self.adjusted_color = COLOR_PLAYER
        self.debug = False
        self.collide = True
        self.cooldowns = {  # List, in seconds, of cooldowns for different functions
            "shot": PLAYER_SHOOT_COOLDOWN,
            "burst": 2,
            "bomb": 1.25,
        }
        self.timers = {  # Records the time.time() of the last usage of the functions.
            "shot": 0,
            "burst": 0,
            "bomb": 0,
        }
        self.shot_size = (5, 5)  # Size of the bullets
        self.spray_angle = 0  # Used for powerup 3
        self.powerups_applied = []  # List of all powerups that are applied to the player, their durations, and times.
        if not self.debug:
            self.cooldowns["shot"] = PLAYER_SHOOT_COOLDOWN
            self.shot_speed = PLAYER_SHOT_SPEED
            self.speed = PLAYER_SPEED
            self.collide = True
        else:
            self.cooldowns["shot"] = DEBUG_PLAYER_SHOOT_COOLDOWN
            self.shot_speed = DEBUG_PLAYER_SHOT_SPEED
            self.speed = DEBUG_PLAYER_SPEED
            self.collide = False

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
            elif self.cord_x < 590:
                self.cord_x += math.cos(math.pi/4) * self.speed
            elif self.cord_y > 0:
                self.cord_y -= math.sin(math.pi/4) * self.speed
        elif (pressed[pygame.K_UP] or pressed[pygame.K_w]) and (pressed[pygame.K_LEFT] or pressed[pygame.K_a]):
            if self.cord_x > 0 and self.cord_y > 0:
                self.cord_x -= math.cos(math.pi/4) * self.speed
                self.cord_y -= math.sin(math.pi/4) * self.speed
            elif self.cord_x > 0:
                self.cord_x -= math.sin(math.pi/4) * self.speed
            elif self.cord_y > 0:
                self.cord_y -= math.sin(math.pi/4) * self.speed
        elif (pressed[pygame.K_DOWN] or pressed[pygame.K_s]) and (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]):
            if self.cord_x < 590 and self.cord_y < 590:
                self.cord_x += math.cos(math.pi/4) * self.speed
                self.cord_y += math.sin(math.pi/4) * self.speed
            elif self.cord_x < 590:
                self.cord_x += math.sin(math.pi/4) * self.speed
            elif self.cord_y < 590:
                self.cord_y += math.sin(math.pi/4) * self.speed
        elif (pressed[pygame.K_DOWN] or pressed[pygame.K_s]) and (pressed[pygame.K_LEFT] or pressed[pygame.K_a]):
            if self.cord_x > 0 and self.cord_y < 590:
                self.cord_x -= math.cos(math.pi/4) * self.speed
                self.cord_y += math.sin(math.pi/4) * self.speed
            elif self.cord_x > 0:
                self.cord_x -= math.sin(math.pi/4) * self.speed
            elif self.cord_y < 590:
                self.cord_y += math.sin(math.pi / 4) * self.speed
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
        if time.time() >= self.timers["shot"] + self.cooldowns["shot"]:
            player_bullet = shot(mx=mouse_x, my=mouse_y, px=self.cord_x, py=self.cord_y,
                                 speed=self.shot_speed, size=self.shot_size)
            self.shots.append(player_bullet)
            self.timers["shot"] = time.time()

    # This fires bullets in equal angles from each other
    def shoot_spray(self, parts, shot):
        j = 0.0
        for i in range(0, parts, 1):
            j += math.pi / math.radians(parts)
            player_bullet = shot(angle=j, speed=self.shot_speed, px=self.cord_x, py=self.cord_y, size=self.shot_size)
            self.shots.append(player_bullet)

    def shoot_angle(self, angle, shot):
        player_bullet = shot(angle=angle, px=self.cord_x, py=self.cord_y, speed=self.shot_speed, size=self.shot_size)
        self.shots.append(player_bullet)

    def shoot_burst(self, mx, my, shot):
        if time.time() >= self.timers["burst"] + self.cooldowns["burst"]:
            angle = math.atan2((my - self.cord_y), (mx - self.cord_x))
            player_bullet = shot(angle=angle, px=self.cord_x, py=self.cord_y,
                                 speed=self.shot_speed, size=self.shot_size)
            self.shots.append(player_bullet)
            for i in range(1, 3, 1):  # TODO
                angle = math.atan2((my - self.cord_y), (mx - self.cord_x)) + math.radians(i*5)
                player_bullet = shot(angle=angle, px=self.cord_x, py=self.cord_y,
                                     speed=self.shot_speed, size=self.shot_size)
                self.shots.append(player_bullet)
            for i in range(1, 3, 1):
                angle = math.atan2((my - self.cord_y), (mx - self.cord_x)) - math.radians(i*5)
                player_bullet = shot(angle=angle, px=self.cord_x, py=self.cord_y,
                                     speed=self.shot_speed, size=self.shot_size)
                self.shots.append(player_bullet)
            self.timers["burst"] = time.time()

    def spray(self, shot):
        self.spray_angle += 0.1
        self.shoot_angle(self.spray_angle, shot)
        self.shoot_angle(self.spray_angle + math.pi / 2, shot)
        self.shoot_angle(self.spray_angle + 3 * math.pi / 2, shot)
        self.shoot_angle(self.spray_angle + math.pi, shot)
        self.shoot_angle(-self.spray_angle, shot)
        self.shoot_angle(-(self.spray_angle + math.pi / 2), shot)
        self.shoot_angle(-(self.spray_angle + 3 * math.pi / 2), shot)
        self.shoot_angle(-(self.spray_angle + math.pi), shot)

    def update(self):
        self.hitbox = pygame.Rect(self.cord_x, self.cord_y, self.size_x, self.size_y)
        time_change = 0
        label_text = []
        if len(self.powerups_applied) > 0:
            for i in self.powerups_applied:
                if time.time() >= i[1] + i[2]:
                    self.powerups_applied.remove(i)
                else:
                    if i[0] == 0:
                        self.powerups_applied = []
                        label_text.append("Reset")
                    elif i[0] == 1:
                        label_text.append("Ring " + str(int(math.ceil(i[2] + i[1] - time.time()))))
                        self.shoot_spray(360, Shot.Shot)
                        self.powerups_applied.remove(i)
                    elif i[0] == 2:
                        time_change = 1
                        label_text.append("Slow Time " + str(int(math.ceil(i[2] + i[1] - time.time()))))
                    elif i[0] == 3:
                        self.spray(Shot.Shot)
                        label_text.append("Spin Fire " + str(int(math.ceil(i[2] + i[1] - time.time()))))
                    elif i[0] == 4:
                        self.collide = False
                        self.adjusted_color = (150, 150, 150)
                        label_text.append("No Collide " + str(int(math.ceil(i[2] + i[1] - time.time()))))
                    elif i[0] == 5:
                        self.shot_size = (20, 20)
                        label_text.append("Big Bullets " + str(int(math.ceil(i[2] + i[1] - time.time()))))
                    elif i[0] == 6:
                        self.drop_bomb()
                        label_text.append("Bombs " + str(int(math.ceil(i[2] + i[1] - time.time()))))
                    elif i[0] == 7:
                        self.size_x, self.size_y = (6, 6)
                        label_text.append("Tiny Man! " + str(int(math.ceil(i[2] + i[1] - time.time()))))
                    elif i[0] == 8:
                        pass
        else:
            self.adjusted_color = (0, 150, 0)
            self.collide = True
            self.adjusted_color = COLOR_PLAYER
            self.shot_size = (5, 5)
            self.speed = PLAYER_SPEED
            self.size_x, self.size_y = (10, 10)
        final_string = ''
        count = 0
        for i in label_text:
            count += 1
            final_string += i
            if count < len(label_text):
                final_string += ", "
        return time_change, final_string

    def refresh_debug(self):
        if not self.debug:
            self.cooldowns["shot"] = PLAYER_SHOOT_COOLDOWN
            self.shot_speed = PLAYER_SHOT_SPEED
            self.speed = PLAYER_SPEED
        else:
            self.cooldowns["shot"] = DEBUG_PLAYER_SHOOT_COOLDOWN
            self.shot_speed = DEBUG_PLAYER_SHOT_SPEED
            self.speed = DEBUG_PLAYER_SPEED
            self.collide = False

    def give_powerup(self, powerup_id, duration=1):
        powerup = powerup_id, duration, time.time()  # Needs to keep track of time applied
        check = 0

        for i in self.powerups_applied:
            if powerup[0] == i[0]:  # the ids are the same
                self.powerups_applied.remove(i)
                self.powerups_applied.append(powerup)  # Overwrite
                check = True  # We found a match

        if not check:  # No matches
            self.powerups_applied.append(powerup)

    def drop_bomb(self):
        if time.time() >= self.timers["bomb"] + self.cooldowns["bomb"]:
            new_bomb = Bomb.Bomb(self.cord_x, self.cord_y)
            self.bombs.append(new_bomb)
            self.timers["bomb"] = time.time()
