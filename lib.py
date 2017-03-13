import pygame
import random
import math
import time
import Laser
import Player
import Shot
import PowerUp
from config import *


def update_events_menu():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Happens when the user selects quit or closes with X
            return False
    return True


def update_keyboard_menu(menu_spot, last_toggle, debug_state, frame):
    pressed = pygame.key.get_pressed()  # Make a list of every key that is being pressed down.

    if frame == 1:  # Fixes bug in which pressed from last game can move the cursor to quit on first frame
        pressed = []
        for i in range(0, 300):
            pressed.append(0)

    if pressed[pygame.K_c] and time.time() >= last_toggle + TOGGLE_DEBUFFER:
        # Toggles cheat mode. assuming enough time has passed
        debug_state = not debug_state
        last_toggle = time.time()

    # This chain moves the cursor
    if (pressed[pygame.K_UP] or pressed[pygame.K_w]) and (pressed[pygame.K_DOWN] or pressed[pygame.K_s]):
        pass
    elif (pressed[pygame.K_LEFT] or pressed[pygame.K_a]) and (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]):
        pass
    elif (pressed[pygame.K_UP] or pressed[pygame.K_w]) and menu_spot > 0:
        menu_spot -= 1
    elif (pressed[pygame.K_DOWN] or pressed[pygame.K_s]) and menu_spot < 1:
        menu_spot += 1
    elif (pressed[pygame.K_LEFT] or pressed[pygame.K_a]) and menu_spot > 0:
        menu_spot -= 1
    elif (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]) and menu_spot < 1:
        menu_spot += 1

    if pressed[pygame.K_RETURN]:  # What to do if the user finalized a selection
        if menu_spot == 0:
            menu_running = False
            menu_quit = False
        elif menu_spot == 1:
            menu_running = False
            menu_quit = True
        else:
            menu_running = False
            menu_quit = False
            print("If you see this, please let the developer know!")
            print("Error No: 2")
    else:
        menu_running = True
        menu_quit = False

    return menu_spot, last_toggle, debug_state, menu_running, menu_quit


def draw_gui_menu(menu_spot, debug_state, win, difficulty):
    # This chain draws the text on the menu
    if menu_spot == 0:
        if win:
            label_start = pygame.font.SysFont(FONT, FONT_SIZE).render("Continue  <--", 1, COLOR_START)
        else:
            label_start = pygame.font.SysFont(FONT, FONT_SIZE).render("New Game  <--", 1, COLOR_START)
        label_quit = pygame.font.SysFont(FONT, FONT_SIZE).render("Quit", 1, COLOR_QUIT)
    elif menu_spot == 1:
        if win:
            label_start = pygame.font.SysFont(FONT, FONT_SIZE).render("Continue", 1, COLOR_START)
        else:
            label_start = pygame.font.SysFont(FONT, FONT_SIZE).render("New Game", 1, COLOR_START)
        label_quit = pygame.font.SysFont(FONT, FONT_SIZE).render("Quit  <--", 1, COLOR_QUIT)
    else:
        label_start = pygame.font.SysFont(FONT, FONT_SIZE).render("Go", 1, COLOR_START)
        label_quit = pygame.font.SysFont(FONT, FONT_SIZE).render("Stop", 1, COLOR_QUIT)
        print("If you see this, please let the developer know!")
        print("Error No: 1")

    if debug_state:
        SCREEN.fill(DEBUG_COLOR_SCREEN)
    else:
        SCREEN.fill(COLOR_SCREEN)
    SCREEN.blit(label_start, ((WINDOW_X / 2) - 50, (WINDOW_Y / 2 - 50)))
    SCREEN.blit(label_quit, ((WINDOW_X / 2) - 50, (WINDOW_Y / 2)))

    # Display the current difficulty
    level = pygame.font.SysFont(FONT, FONT_SIZE).render(str(difficulty), 1, COLOR_DIFFICULTY)
    SCREEN.blit(level, (WINDOW_X - 50, 0))


# Draw the lasers and remove ones that go off screen
def update_lasers(lasers_list, time_change):
    for laser in lasers_list:
        laser.update(time_change)
        r, g, b = (0, 10, 255)
        b -= laser.speed*50
        r += laser.speed*50
        if b < 0:
            b = 0
        if r > 255:
            r = 255
        adjusted_color = (r, g, b)
        if laser.cord_x > 620 and laser.side == 2:
            lasers_list.remove(laser)
        elif laser.cord_x < -20 and laser.side == 3:
            lasers_list.remove(laser)
        elif laser.cord_y > 620 and laser.side == 0:
            lasers_list.remove(laser)
        elif laser.cord_y < -20 and laser.side == 1:
            lasers_list.remove(laser)
        else:
            pygame.draw.rect(SCREEN, adjusted_color, laser.hitbox, 0)


# If the laser count is lower than we want, make more
def make_lasers(laser_list, difficulty):
    if len(laser_list) < (LASER_THRESHOLD * (difficulty/LASER_DIVIDE)) + LASER_ADD and LASER_RESPAWN:
        laser_shot = Laser.Laser(difficulty)
        laser_list.append(laser_shot)


# Change the player's cords based on what keys are pressed and draw the player
def update_player(player_obj, spray_angle, spray_toggle, debug_state, bombs):
    player_obj.movement()
    player_obj.update(bombs)
    player_obj.debug = debug_state
    player_obj.refresh_debug()
    if debug_state:
        pygame.draw.rect(SCREEN, DEBUG_COLOR_PLAYER, player_obj.hitbox, 0)
    else:
        pygame.draw.rect(SCREEN, player_obj.adjusted_color, player_obj.hitbox, 0)

    # Makes a spinning illusion.
    if spray_toggle and debug_state:
        spray_angle = spray(Shot.Shot, spray_angle, player_obj)

    return spray_angle, spray_toggle


def spawn_powerups(chance, powerups):
    if random.random() <= chance/FRAMERATE:  # This makes it so that the chance is per second
        x = PowerUp.PowerUp(random.randint(1, 8))
        powerups.append(x)


def update_powerups(powerups, player_obj, frame, time_change, spray_angle):
    for i in powerups:
        if i.id == 1:
            pygame.draw.rect(SCREEN, (120, 120, 255), i.hitbox)
            if i.hitbox.colliderect(player_obj.hitbox):
                player_obj.give_powerup(1)
                powerups.remove(i)
        elif i.id == 2:
            pygame.draw.rect(SCREEN, (200, 200, 10), i.hitbox)
            if i.hitbox.colliderect(player_obj.hitbox):
                player_obj.give_powerup(2, 3)
                powerups.remove(i)
        elif i.id == 3:
            pygame.draw.rect(SCREEN, (10, 200, 100), i.hitbox)
            if i.hitbox.colliderect(player_obj.hitbox):
                player_obj.give_powerup(3)
                powerups.remove(i)
        elif i.id == 4:
            pygame.draw.rect(SCREEN, (255, 50, 150), i.hitbox)
            if i.hitbox.colliderect(player_obj.hitbox):
                player_obj.give_powerup(4, 5)
                powerups.remove(i)
        elif i.id == 5:
            pygame.draw.rect(SCREEN, (0, 50, 100), i.hitbox)
            if i.hitbox.colliderect(player_obj.hitbox):
                player_obj.give_powerup(5, 3)
                powerups.remove(i)
        elif i.id == 6:
            pygame.draw.rect(SCREEN, (140, 90, 70), i.hitbox)
            if i.hitbox.colliderect(player_obj.hitbox):
                player_obj.give_powerup(6, 4)
                powerups.remove(i)
        elif i.id == 7:
            pygame.draw.rect(SCREEN, (0, 0, 0), i.hitbox)
            pygame.draw.rect(SCREEN, (255, 50, 50), pygame.Rect(i.cord_x+4, i.cord_y+4, 7, 7))
            if i.hitbox.colliderect(player_obj.hitbox):
                player_obj.give_powerup(7, 3)
                powerups.remove(i)
        elif i.id == 8:
            pygame.draw.rect(SCREEN, (0, 255, 0), i.hitbox)
            pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(i.cord_x + 4, i.cord_y, 7, 2))
            pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(i.cord_x + 2, i.cord_y + 2, 2, 2))
            pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(i.cord_x + 11, i.cord_y + 2, 2, 6))
            pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(i.cord_x + 5, i.cord_y + 8, 6, 2))
            pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(i.cord_x + 5, i.cord_y + 10, 2, 2))
            pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(i.cord_x + 5, i.cord_y + 13, 2, 2))
            if i.hitbox.colliderect(player_obj.hitbox):
                player_obj.give_powerup(random.randint(1, 7))
                powerups.remove(i)

    if player_obj.powerup == 1:
        player_obj.shoot_spray(360, Shot.Shot, frame)
    elif player_obj.powerup == 2:
        time_change = 1
    elif player_obj.powerup == 3:
        spray_angle = spray(Shot.Shot, spray_angle, player_obj)
    elif player_obj.powerup == 4:
        player_obj.collide = False
        player_obj.adjusted_color = (150, 150, 150)
    elif player_obj.powerup == 5:
        player_obj.shot_size = (20, 20)
    elif player_obj.powerup == 6:
        player_obj.bombs = True
    elif player_obj.powerup == 7:
        player_obj.size_x, player_obj.size_y = (6, 6)
    elif player_obj.powerup == 0:
        time_change = 0
        player_obj.collide = True
        player_obj.adjusted_color = (0, 150, 0)
        player_obj.shot_size = (5, 6)
        player_obj.bombs = False
        player_obj.size_x, player_obj.size_y = (10, 10)
    else:
        print("Error No. 7")
        print("If you see this, please let the developer know!")
    return time_change, spray_angle


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
            pygame.draw.circle(SCREEN, COLOR_SHOT, (int(shot.cord_x), int(shot.cord_y)), 4, 0)


def check_collisions(lasers, player_obj):
    # check for collisions with player or player's lasers
    for laser in lasers:
        if player_obj.hitbox.colliderect(laser.hitbox) and player_obj.collide:
            # If player has hit a laser, post a 'hit' event
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"event": "hit"}))
        for shot in player_obj.shots:
            if shot.hurtbox.colliderect(laser.hitbox):  # If a player bullet has hit a laser, destroy both
                try:
                    lasers.remove(laser)
                    player_obj.shots.remove(shot)
                except ValueError:  # This happens when we try to delete something that doesnt exist
                    pass


def draw_gui(timers, difficulty):
    timer = pygame.font.SysFont(FONT, FONT_SIZE).render(str(int(time.time() - timers['time_start'])), 1, COLOR_TIMER)
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

                time.sleep(1)  # Allow time for player to understand what he did wrong.

                for laser in lasers:  # Probably redundant. Better safe than sorry for now...
                    lasers.remove(laser)

                game_running = False
                game_state = 'lose'

            elif event.event == 'win':
                SCREEN.fill(COLOR_SCREEN)
                label = pygame.font.SysFont(FONT, FONT_SIZE).render("Win!", 1, COLOR_WIN)
                SCREEN.blit(label, (300, 300))
                pygame.display.flip()

                time.sleep(0.5)  # Allow only enough time for player to know that they aren't dead yet

                for laser in lasers:  # Probably redundant. Better safe than sorry for now...
                    lasers.remove(laser)

                game_running = False
                game_state = 'win'
    return game_running, game_state, game_quit


def update_keyboard(debug_state, timers, spray_toggle, player_obj, time_change):
    pressed = pygame.key.get_pressed()  # Make a list of every key that is being pressed down.

    if pressed[pygame.K_c] and time.time() >= timers['last_debug_toggle'] + 0.3:
        debug_state = not debug_state
        player_obj.debug = debug_state
        player_obj.refresh_debug()
        timers['last_debug_toggle'] = time.time()

    if pressed[pygame.K_v] and time.time() >= timers['last_time_change'] + 0.3:
        if time_change == 0:
            time_change = 1
        elif time_change == 1:
            time_change = 2
        elif time_change == 2:
            time_change = 0
        else:
            print("If you see this, let the developer know!")
            print("Error No. 5")
        timers['last_time_change'] = time.time()

    # Another fun easter egg.
    if pressed[pygame.K_r] and debug_state and (time.time() >= timers['last_spray_toggle'] + DEBUG_SPRAY_DEBUFFER):
        player_obj.give_powerup(3)
        timers['last_spray_toggle'] = time.time()
    return debug_state, timers, spray_toggle, time_change


def update_mouse(player_obj):
    mouse_pressed = pygame.mouse.get_pressed()  # List of all mouse buttons pressed

    if mouse_pressed[0]:
        x, y = pygame.mouse.get_pos()
        player_obj.shoot(x, y, Shot.Shot)
    if mouse_pressed[2]:
        x, y = pygame.mouse.get_pos()
        player_obj.shoot_burst(x, y, Shot.Shot)


def check_time(debug_state, timers):
    # This determines the time passed.
    if debug_state:
        time_reached = time.time() >= timers['time_start'] + DEBUG_TIME_LIMIT
    else:
        time_reached = time.time() >= timers['time_start'] + TIME_LIMIT
        # Once the player has survived the required time, he wins the level
    if time_reached:
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"event": "win"}))
    return time_reached


def update_bombs(player_obj, bombs):
    for bomb in bombs:
        bomb.tick(player_obj, bombs)
        pygame.draw.rect(SCREEN, bomb.color, bomb.hitbox)
