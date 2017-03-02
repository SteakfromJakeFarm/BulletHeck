import pygame
import lib
import time
import math
import random

VERSION = '0.3a'

FRAMERATE = 60  # Times per second that the loop runs
WINDOW_X = 600  # Width of the game window in pixels
WINDOW_Y = 600  # Length of the game window in pixels
LASER_THRESHOLD = 25  # Base number of lasers that should be on screen at a time
TIME_LIMIT = 10  # How long do you need to survive before you can pass to the next level?
PLAYER_COLLIDE = True
PLAYER_SHOOT_COOLDOWN = 0.3  # Time between the player's shots
PLAYER_SHOT_SPEED = 2  # Multiplier of the player's shots' speed
PLAYER_SPEED = 1.5  # Multiplier of the player's speed
FONT = "Comic Sans MS"  # Font to be used in every menu
COLOR_START = (10, 10, 200)  # Color of the "Start" option in the main menu
COLOR_QUIT = (200, 10, 10)  # Color of the "Quit" option in the main menu
COLOR_SCREEN = (255, 255, 255)  # Color of the game background
COLOR_MENU_SCREEN = (255, 255, 255)  # Color of the main menu background
COLOR_TIMER = (100, 0, 255)  # Color of the timer in the game
COLOR_PLAYER = (0, 100, 0)  # Color of the player's hitbox
COLOR_LASER = (100, 0, 100)  # Color of the lasers' hitboxes
COLOR_DED = (0, 0, 255)  # Color of the message on the lose screen
COLOR_WIN = (0, 200, 0)  # Color of the message on the win screen
COLOR_SHOT = (255, 0, 0)  # Color of the player's bullets
COLOR_DIFFICULTY = (100, 50, 170)  # Color of the difficulty counter
FONT_SIZE = 20  # Size of the font of every piece of text
LASER_MIN_SPEED = 1  # The lowest speed that a laser should ever go
LASER_MULTIPLIER = 3  # Turns the random decimal of 0-1 to a larger, more usable number
LASER_RESPAWN = True  # Should the lasers respawn once they move off screen?
TOGGLE_DEBUFFER = 0.2  # Time between toggling cheat mode

DEBUG_TIME_LIMIT = 99  # Longer for easier debugging
DEBUG_PLAYER_COLLIDE = False  # Invincibility for easier debugging
DEBUG_PLAYER_SHOOT_COOLDOWN = 0.0  # No cooldown for easier debugging
DEBUG_PLAYER_SHOT_SPEED = 3  # Faster shot speed for easier debugging
DEBUG_PLAYER_SPEED = 3  # Faster move speed for easier debugging
DEBUG_COLOR_PLAYER = (0, 0, 0)  # Different color to differentiate from normal mode
DEBUG_COLOR_SCREEN = (100, 100, 100)  # Change the screen's color to signify the mode
DEBUG_SPRAY_DEBUFFER = 0.3  # This is just for fun. Time between toggling the spray mode.

pygame.init()  # Its a pygame thing. Idk. It tells me to call this first.

SCREEN = pygame.display.set_mode((WINDOW_X, WINDOW_Y))  # Create screen on the display
CLOCK = pygame.time.Clock()  # Create the clock object. Useful for implementing the framerate


def main_menu(win,difficulty):  # Draws the main menu. Once the user select an option, it returns the result.
    menu_running = True  # Is the menu running?
    menu_quit = False  # Did the user want to quit?
    menu_spot = 0  # Position that the cursor is over
    debug_state = False  # Is debug(cheat) mode on?

    if win:  # Did the user win the last round?
        label_start = pygame.font.SysFont(FONT, 20).render("Continue", 1, COLOR_START)
    else:
        label_start = pygame.font.SysFont(FONT, 20).render("Start", 1, COLOR_START)

    label_quit = pygame.font.SysFont(FONT, 20).render("Quit", 1, COLOR_QUIT)
    last_toggle = time.time()
    pygame.event.clear()  # Prevents events from last round affecting the next round.
    while menu_running:
        pygame.event.pump()  # pygame tells me that I should do this.
        CLOCK.tick(FRAMERATE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Happens when the user selects quit or closes with X
                menu_running = False
                menu_quit = True

        pressed = pygame.key.get_pressed()  # Make a list of every key that is being pressed down.

        if pressed[pygame.K_c] and time.time() >= last_toggle + TOGGLE_DEBUFFER:  # Toggles cheat mode. assuming enough time has passed
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
        elif pressed[pygame.K_RETURN]:  # What to do if the user finalized a selection
            if menu_spot == 0:
                menu_running = False
                menu_quit = False
            elif menu_spot == 1:
                menu_running = False
                menu_quit = True

        # This chain draws the text on the menu
        if menu_spot == 0:
            if win:
                label_start = pygame.font.SysFont(FONT, FONT_SIZE).render("Next Level  <--", 1, COLOR_START)
            else:
                label_start = pygame.font.SysFont(FONT, FONT_SIZE).render("New Game  <--", 1, COLOR_START)
            label_quit = pygame.font.SysFont(FONT, FONT_SIZE).render("Quit", 1, COLOR_QUIT)
        elif menu_spot == 1:
            if win:
                label_start = pygame.font.SysFont(FONT, FONT_SIZE).render("Next Level", 1, COLOR_START)
            else:
                label_start = pygame.font.SysFont(FONT, FONT_SIZE).render("New Game", 1, COLOR_START)
            label_quit = pygame.font.SysFont(FONT, FONT_SIZE).render("Quit  <--", 1, COLOR_QUIT)

        if debug_state:
            SCREEN.fill(DEBUG_COLOR_SCREEN)
        else:
            SCREEN.fill(COLOR_SCREEN)
        SCREEN.blit(label_start, ((WINDOW_X / 2) - 50, (WINDOW_Y / 2 - 50)))
        SCREEN.blit(label_quit, ((WINDOW_X / 2) - 50, (WINDOW_Y / 2)))

        # Display the current difficulty
        level = pygame.font.SysFont(FONT, FONT_SIZE).render(str(difficulty), 1, COLOR_DIFFICULTY)
        SCREEN.blit(level, (WINDOW_X - 50, 0))

        pygame.display.flip()  # This is apparently required for things to be rendered

    return menu_quit, debug_state  # Return if the user wanted to quit and if the user wanted to use debug mode


# This function is the actual game loop. It changes based on the difficulty and is debug mode is on
def game(difficulty, debug_state=False):
    lasers = []  # List of all the lasers
    game_quit = False  # Does the user want to quit?
    game_running = True  # Is the game running?
    time_start = time.time()
    first_frame = True
    frame_count = 0
    spray_toggle = False
    spray_angle = 0.0
    last_spray_toggle = time.time()
    last_debug_state = debug_state
    last_debug_toggle = time.time()
    powerups = []

    if debug_state:  # If debug mode is on, change the way the player is created
        player_obj = lib.Player(DEBUG_PLAYER_SHOOT_COOLDOWN, DEBUG_PLAYER_SPEED, DEBUG_PLAYER_SHOT_SPEED, 300, 300)
    else:
        player_obj = lib.Player(PLAYER_SHOOT_COOLDOWN, PLAYER_SPEED, PLAYER_SHOT_SPEED, 300, 300)

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
    def make_lasers(laser_list, x, frame):
        for i in range(0, x, 1):
            if len(laser_list) < LASER_THRESHOLD * (difficulty/2.0) and (LASER_RESPAWN or frame):
                laser_shot = lib.Laser(LASER_MIN_SPEED, LASER_MULTIPLIER + (difficulty/5.0))
                laser_list.append(laser_shot)

    # Change the player's cords based on what keys are pressed and draw the player
    def update_player(player):
        player.movement()
        player.update()
        if debug_state:
            pygame.draw.rect(SCREEN, DEBUG_COLOR_PLAYER, player.hitbox, 0)
        else:
            pygame.draw.rect(SCREEN, COLOR_PLAYER, player.hitbox, 0)

    def spawn_powerups(chance):
        if random.random() <= chance/60.0:
            x = lib.PowerUp(random.randint(1, 1))
            powerups.append(x)

    def update_powerups(powerups):
        for i in powerups:
            pygame.draw.rect(SCREEN, (10, 10, 255), i.hitbox)
            if i.hitbox.colliderect(player_obj.hitbox):
                player_obj.last_powerup_time = time.time()
                player_obj.powerup = 1
                player_obj.last_powerup_duration = 1
                powerups.remove(i)

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

    pygame.event.clear()  # Good for the environment

    while game_running:
        CLOCK.tick(FRAMERATE)
        SCREEN.fill(COLOR_SCREEN)

        frame_count += 1
        pygame.event.pump()  # pygame wants me to do this. Please make them stop

        # This determines the time passed.
        if debug_state:
            time_reached = time.time() >= time_start + DEBUG_TIME_LIMIT
        else:
            time_reached = time.time() >= time_start + TIME_LIMIT

        # Once the player has survived the required time, he wins the level
        if time_reached:
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"event": "win"}))

        # Makes lasers when necessary
        make_lasers(lasers, 1, first_frame)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                game_quit = True

            elif event.type == pygame.USEREVENT:
                if event.event == 'hit':  # If the player gets hit, he dies
                    label = pygame.font.SysFont(FONT, FONT_SIZE).render("ded", 1, COLOR_DED)
                    SCREEN.blit(label, (300, 300))
                    pygame.display.flip()

                    time.sleep(3)  # Allow time for player to understand what he did wrong.

                    for laser in lasers:  # Probably redundant. Better safe than sorry for now...
                        lasers.remove(laser)

                    game_running = False
                    game_state = 'lose'

                elif event.event == 'win':
                    label = pygame.font.SysFont(FONT, FONT_SIZE).render("Win!", 1, COLOR_WIN)
                    SCREEN.blit(label, (300, 300))
                    pygame.display.flip()

                    time.sleep(1)  # Allow only enough time for player to know that they aren't dead yet

                    for laser in lasers:  # Probably redundant. Better safe than sorry for now...
                        lasers.remove(laser)

                    game_running = False
                    game_state = 'win'

        pressed = pygame.key.get_pressed()  # Make a list of every key that is being pressed down.

        if (pressed[pygame.K_SPACE] and debug_state):  # Fun easter egg. Might make into a power-up later
            player_obj.powerup = 1
            player_obj.last_powerup_duration = 1
            player_obj.shoot_spray(6)

        if pressed[pygame.K_c]:
            debug_state = not debug_state

        # Another fun easter egg.
        if pressed[pygame.K_r] and debug_state and (time.time() >= last_spray_toggle + DEBUG_SPRAY_DEBUFFER):
            spray_toggle = not spray_toggle
            last_spray_toggle = time.time()

        # Makes a spinning illusion.
        if (spray_toggle and debug_state):
            spray_angle += 0.1
            player_obj.shoot_angle(spray_angle)
            player_obj.shoot_angle(spray_angle + math.pi / 2)
            player_obj.shoot_angle(spray_angle + 3 * math.pi / 2)
            player_obj.shoot_angle(spray_angle + math.pi)
            player_obj.shoot_angle(-spray_angle)
            player_obj.shoot_angle(-(spray_angle + math.pi / 2))
            player_obj.shoot_angle(-(spray_angle + 3 * math.pi / 2))
            player_obj.shoot_angle(-(spray_angle + math.pi))

        mouse_pressed = pygame.mouse.get_pressed()  # List of all mouse buttons pressed

        if mouse_pressed[0]:
            x, y = pygame.mouse.get_pos()
            player_obj.shoot(x, y)

        # check for collisions with player or player's lasers
        for laser in lasers:
            if player_obj.hitbox.colliderect(laser.hitbox) and not debug_state:  # If player has hit a laser, post a 'hit' event
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"event": "hit"}))
            for shot in player_obj.shots:
                if shot.hurtbox.colliderect(laser.hitbox):  # If a player bullet has hit a laser, destroy both
                    try:
                        lasers.remove(laser)
                        player_obj.shots.remove(shot)
                    except ValueError:  # This happens when we try to delete something that doesnt exist
                        pass

        if (last_debug_state != debug_state) and (time.time() >= last_debug_toggle + 0.3):  # If debug mode has changed, change the player
            if debug_state:
                player_obj = lib.Player(DEBUG_PLAYER_SHOOT_COOLDOWN, DEBUG_PLAYER_SPEED, DEBUG_PLAYER_SHOT_SPEED,
                                        player_obj.cord_x, player_obj.cord_y)

            else:
                player_obj = lib.Player(PLAYER_SHOOT_COOLDOWN, PLAYER_SPEED, PLAYER_SHOT_SPEED,
                                        player_obj.cord_x, player_obj.cord_y)
            last_debug_state = debug_state
            last_debug_toggle = time.time()

        spawn_powerups(.10)  # Chance that a powerup will spawn on any given second

        update_player(player_obj)

        update_lasers(lasers)

        update_shots(player_obj.shots)

        update_powerups(powerups)

        timer = pygame.font.SysFont(FONT, FONT_SIZE).render(str(int(time.time() - time_start)), 1, COLOR_TIMER)
        SCREEN.blit(timer, (0, 0))

        level = pygame.font.SysFont(FONT, FONT_SIZE).render(str(difficulty), 1, COLOR_DIFFICULTY)
        SCREEN.blit(level, (WINDOW_X-50, 0))

        if first_frame:  # Test variable
            first_frame = False

        pygame.display.flip()  # This is required by pygame to render the screen.

    return game_state, game_quit
