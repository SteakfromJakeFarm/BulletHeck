import random
import math
import time
import Laser
import Player
import Shot
import PowerUp
from config import *


# Draw the lasers and remove ones that go off screen
def update_lasers(lasers_list):
    for laser in lasers_list:
        laser.update()
        if laser.cord_x > 620 and laser.side == 2:
            lasers_list.remove(laser)
        elif laser.cord_x < -20 and laser.side == 3:
            lasers_list.remove(laser)
        elif laser.cord_y > 620 and laser.side == 0:
            lasers_list.remove(laser)
        elif laser.cord_y < -20 and laser.side == 1:
            lasers_list.remove(laser)
        else:
            pygame.draw.rect(SCREEN, COLOR_LASER, laser.hitbox, 0)


# If the laser count is lower than we want, make more
def make_lasers(laser_list, difficulty):
    if len(laser_list) < LASER_THRESHOLD * (difficulty/2.0) and LASER_RESPAWN:
        laser_shot = Laser.Laser(difficulty)
        laser_list.append(laser_shot)


# Change the player's cords based on what keys are pressed and draw the player
def update_player(player_obj, last_debug_state, last_debug_toggle, spray_angle, spray_toggle, debug_state):
    player_obj.movement()
    player_obj.update()
    if debug_state:
        pygame.draw.rect(SCREEN, DEBUG_COLOR_PLAYER, player_obj.hitbox, 0)
    else:
        pygame.draw.rect(SCREEN, COLOR_PLAYER, player_obj.hitbox, 0)

    # Makes a spinning illusion.
    if spray_toggle and debug_state:
        spray_angle = spray(Shot.Shot, spray_angle, player_obj)

    return last_debug_state, last_debug_toggle, spray_angle, spray_toggle


def update_player_debug(player_obj, last_debug_state, last_debug_toggle, debug_state):
    # If debug mode has changed, change the player
    if (last_debug_state != debug_state) and (time.time() >= last_debug_toggle + 0.3):
        last_debug_state = debug_state
        last_debug_toggle = time.time()
        player_obj = Player.Player(player_obj.cord_x, player_obj.cord_y, debug_state)
        return player_obj, last_debug_state, last_debug_toggle
    return False


def spawn_powerups(chance, powerups):
    if random.random() <= chance/60.0:
        x = PowerUp.PowerUp(random.randint(1, 1))
        powerups.append(x)


def update_powerups(powerups, player_obj):
    for i in powerups:
        pygame.draw.rect(SCREEN, (10, 10, 255), i.hitbox)
        if i.hitbox.colliderect(player_obj.hitbox):
            player_obj.last_powerup_time = time.time()
            player_obj.powerup = 1
            player_obj.last_powerup_duration = 1
            powerups.remove(i)
    if player_obj.powerup == 1:
        player_obj.shoot_spray(6, Shot.Shot)


# Draw the player's bullets and update their movement. Bullets that go off screen are removed
def update_shots(shots_list):
    for shot in shots_list:
        shot.movement()
        shot.update()
        if shot.cord_x > 620:
            shots_list.remove(shot)
        elif shot.cord_x < 1:
            shots_list.remove(shot)
        elif shot.cord_y > 620:
            shots_list.remove(shot)
        elif shot.cord_y < 1:
            shots_list.remove(shot)
        else:
            pygame.draw.rect(SCREEN, COLOR_SHOT, shot.hurtbox, 0)


def check_collisions(lasers, player_obj, debug_state):
    # check for collisions with player or player's lasers
    for laser in lasers:
        if player_obj.hitbox.colliderect(
                laser.hitbox) and not debug_state:  # If player has hit a laser, post a 'hit' event
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"event": "hit"}))
        for shot in player_obj.shots:
            if shot.hurtbox.colliderect(laser.hitbox):  # If a player bullet has hit a laser, destroy both
                try:
                    lasers.remove(laser)
                    player_obj.shots.remove(shot)
                except ValueError:  # This happens when we try to delete something that doesnt exist
                    pass


def draw_gui(time_start, difficulty):
    timer = pygame.font.SysFont(FONT, FONT_SIZE).render(str(int(time.time() - time_start)), 1, COLOR_TIMER)
    SCREEN.blit(timer, (0, 0))

    level = pygame.font.SysFont(FONT, FONT_SIZE).render(str(difficulty), 1, COLOR_DIFFICULTY)
    SCREEN.blit(level, (WINDOW_X - 50, 0))


def spray(shot, spray_angle, player_obj):
    spray_angle += 0.1
    player_obj.shoot_angle(spray_angle, shot)
    player_obj.shoot_angle(spray_angle + math.pi / 2, shot)
    player_obj.shoot_angle(spray_angle + 3 * math.pi / 2, shot)
    player_obj.shoot_angle(spray_angle + math.pi, shot)
    player_obj.shoot_angle(-spray_angle, shot)
    player_obj.shoot_angle(-(spray_angle + math.pi / 2), shot)
    player_obj.shoot_angle(-(spray_angle + 3 * math.pi / 2), shot)
    player_obj.shoot_angle(-(spray_angle + math.pi), shot)
    return spray_angle


def update_events(game_running, game_quit, game_state, lasers):
    pygame.event.pump()  # pygame wants me to do this. Please make them stop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
            game_quit = True

        elif event.type == pygame.USEREVENT:
            if event.event == 'hit':  # If the player gets hit, he dies
                SCREEN.fill(COLOR_SCREEN)
                label = pygame.font.SysFont(FONT, FONT_SIZE).render("ded", 1, COLOR_DED)
                SCREEN.blit(label, (300, 300))
                pygame.display.flip()

                time.sleep(3)  # Allow time for player to understand what he did wrong.

                for laser in lasers:  # Probably redundant. Better safe than sorry for now...
                    lasers.remove(laser)

                game_running = False
                game_state = 'lose'

            elif event.event == 'win':
                SCREEN.fill(COLOR_SCREEN)
                label = pygame.font.SysFont(FONT, FONT_SIZE).render("Win!", 1, COLOR_WIN)
                SCREEN.blit(label, (300, 300))
                pygame.display.flip()

                time.sleep(1)  # Allow only enough time for player to know that they aren't dead yet

                for laser in lasers:  # Probably redundant. Better safe than sorry for now...
                    lasers.remove(laser)

                game_running = False
                game_state = 'win'
    return game_running, game_state, game_quit


def update_keyboard(debug_state, last_debug_toggle, last_spray_toggle, spray_toggle, player_obj):
    pressed = pygame.key.get_pressed()  # Make a list of every key that is being pressed down.

    if pressed[pygame.K_SPACE] and debug_state:  # Fun easter egg. Might make into a power-up later
        player_obj.powerup = 1
        player_obj.last_powerup_duration = 1
        player_obj.shoot_spray(6, Shot.Shot)

    if pressed[pygame.K_c] and time.time() >= last_debug_toggle + 0.3:
        debug_state = not debug_state

    # Another fun easter egg.
    if pressed[pygame.K_r] and debug_state and (time.time() >= last_spray_toggle + DEBUG_SPRAY_DEBUFFER):
        spray_toggle = not spray_toggle
        last_spray_toggle = time.time()
    return debug_state, last_spray_toggle, spray_toggle


def update_mouse(player_obj):
    mouse_pressed = pygame.mouse.get_pressed()  # List of all mouse buttons pressed

    if mouse_pressed[0]:
        x, y = pygame.mouse.get_pos()
        player_obj.shoot(x, y, Shot.Shot)


def check_time(debug_state, time_start):
    # This determines the time passed.
    if debug_state:
        time_reached = time.time() >= time_start + DEBUG_TIME_LIMIT
    else:
        time_reached = time.time() >= time_start + TIME_LIMIT
        # Once the player has survived the required time, he wins the level
    if time_reached:
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"event": "win"}))
    return time_reached
