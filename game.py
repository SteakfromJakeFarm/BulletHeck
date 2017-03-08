import pygame
from lib import *
import time
from config import *

pygame.init()  # Its a pygame thing. Idk. It tells me to call this first.


def main_menu(difficulty, win):  # Draws the main menu. Once the user select an option, it returns the result.
    menu_running = True  # Is the menu running?
    menu_quit = False  # Did the user want to quit?
    menu_spot = 0  # Position that the cursor is over
    debug_state = False  # Is debug(cheat) mode on?
    last_toggle = time.time()
    pygame.event.clear()  # Prevents events from last round affecting the next round.
    while menu_running:
        pygame.event.pump()  # pygame tells me that I should do this.
        CLOCK.tick(FRAMERATE)

        if not update_events_menu():
            menu_quit = True
            break

        menu_spot, last_toggle, debug_state, menu_running, menu_quit = \
            update_keyboard_menu(menu_spot, last_toggle, debug_state)

        draw_gui_menu(menu_spot, debug_state, win, difficulty)

        pygame.display.flip()  # This is apparently required for things to be rendered

    return menu_quit, debug_state  # Return if the user wanted to quit and if the user wanted to use debug mode


# This function is the actual game loop. It changes based on the difficulty and is debug mode is on
def game(difficulty, debug_state=False):
    timers = []
    lasers = []  # List of all the lasers
    game_quit = False  # Does the user want to quit?
    game_running = True  # Is the game running?
    game_state = ''
    timers.append(time.time())  # time_start
    frame_count = 0
    spray_toggle = False
    spray_angle = 0.0
    timers.append(time.time())  # last_spray_toggle
    last_debug_state = debug_state
    timers.append(time.time())  # last_debug_toggle
    timers.append(time.time())  # last_time_change
    time_change = 0
    powerups = []

    pygame.event.clear()  # Good for the environment

    player_obj = Player.Player(300, 300, debug_state)

    while game_running:
        CLOCK.tick(FRAMERATE)
        SCREEN.fill(COLOR_SCREEN)

        frame_count += 1

        last_debug_state, spray_angle, spray_toggle = \
            update_player(player_obj, last_debug_state, spray_angle, spray_toggle, debug_state)

        try:
            player_obj, last_debug_state, timers = \
                update_player_debug(player_obj, last_debug_state, timers, debug_state)
        except TypeError:
            pass

        draw_gui(timers, difficulty)

        make_lasers(lasers, difficulty)

        check_time(debug_state, timers[0])

        update_mouse(player_obj)

        game_running, game_state, game_quit = \
            update_events(game_running, game_state, game_quit, lasers)

        debug_state, last_spray_toggle, spray_toggle, time_change = \
            update_keyboard(debug_state, timers, spray_toggle, player_obj, frame_count, time_change)

        spawn_powerups(0.10, powerups)  # Chance that a powerup will spawn on any given second

        update_lasers(lasers, time_change)

        update_shots(player_obj.shots)

        time_change, spray_angle =\
            update_powerups(powerups, player_obj, frame_count, time_change, spray_angle)

        check_collisions(lasers, player_obj, debug_state)

        pygame.display.flip()  # This is required by pygame to render the screen.

    return game_state, game_quit
