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
    lasers = []  # List of all the lasers
    bombs = []
    game_quit = False  # Does the user want to quit?
    game_running = True  # Is the game running?
    game_state = ''
    frame_count = 0
    spray_toggle = False
    spray_angle = 0.0
    timers = {
        'time_start': time.time(),
        'last_spray_toggle': time.time(),
        'last_debug_toggle': time.time(),
        'last_time_change': time.time()
    }
    time_change = 0
    powerups = []

    pygame.event.clear()  # Good for the environment

    player_obj = Player.Player(300, 300, [])
    player_obj.debug = debug_state
    player_obj.refresh_debug()

    while game_running:
        frame_count += 1

        CLOCK.tick(FRAMERATE)
        SCREEN.fill(COLOR_SCREEN)

        spray_angle, spray_toggle = \
            update_player(player_obj, spray_angle, spray_toggle, debug_state, bombs)

        draw_gui(timers, difficulty)

        make_lasers(lasers, difficulty)

        check_time(debug_state, timers)

        update_mouse(player_obj)

        game_running, game_state, game_quit = \
            update_events(game_running, game_state, game_quit, lasers)

        debug_state, last_spray_toggle, spray_toggle, time_change = \
            update_keyboard(debug_state, timers, spray_toggle, player_obj, time_change)

        spawn_powerups(POWERUP_CHANCE, powerups)  # Chance that a powerup will spawn on any given second

        update_lasers(lasers, time_change)

        update_bombs(player_obj, bombs)

        update_shots(player_obj.shots)

        check_collisions(lasers, player_obj)

        time_change, spray_angle =\
            update_powerups(powerups, player_obj, frame_count, time_change, spray_angle)

        pygame.display.flip()  # This is required by pygame to render the screen.

    return game_state, game_quit
