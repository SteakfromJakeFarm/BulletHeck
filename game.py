import pygame
import Player
import Boss
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
    frame = 0
    while menu_running:
        frame += 1
        pygame.event.pump()  # pygame tells me that I should do this.
        CLOCK.tick(FRAMERATE)

        if not update_events_menu():  # Returns false if player selected quit or tried to close it
            menu_quit = True
            break

        menu_spot, last_toggle, debug_state, menu_running, menu_quit = \
            update_keyboard_menu(menu_spot, last_toggle, debug_state, frame)

        draw_gui_menu(menu_spot, debug_state, win, difficulty)

        pygame.display.flip()  # This is apparently required for things to be rendered

    return menu_quit, debug_state  # Return if the user wanted to quit and if the user wanted to use debug mode


# This function is the actual game loop. It changes based on the difficulty and is debug mode is on
def game(difficulty, score, debug_state=False):
    lasers = []  # List of all the lasers
    game_quit = False  # Does the user want to quit?
    game_running = True  # Is the game running?
    game_state = ''
    frame_count = 0
    spray_toggle = False
    timers = {
        'time_start': time.time(),
        'last_spray_toggle': time.time(),
        'last_bomb_toggle': time.time(),
        'last_nocollide_toggle': time.time(),
        'last_ring_toggle': time.time(),
        'last_tinyman_toggle': time.time(),
        'last_bigbullets_toggle': time.time(),
        'last_slowtime_toggle': time.time(),
        'last_fasttime_toggle': time.time(),
        'last_debug_toggle': time.time(),
        'last_time_change': time.time()
    }
    debug_powerups = {
        'ring': False,
        'bomb': False,
        'nocollide': False,
        'tinyman': False,
        'bigbullets': False,
        'slowtime': False,
        'fasttime': False,
        'spray': False,
    }

    time_change = 0
    powerups = []
    # score = score
    score_thresh = 10

    pygame.event.clear()  # Good for the environment

    player_obj = Player.Player(WINDOW_X/2, WINDOW_Y/2, [], [])
    player_obj.debug = debug_state
    player_obj.refresh_debug()

    if difficulty % 5 == 0:
        boss_obj = Boss.Boss(difficulty * 5, (difficulty/5.0)/FRAMERATE)
    else:
        boss_obj = False

    while game_running:
        frame_count += 1

        CLOCK.tick(FRAMERATE)
        SCREEN.fill(COLOR_SCREEN)

        if difficulty % 5 == 0:
            update_shots(boss_obj.shots, time_change)
            update_boss(boss_obj, player_obj, time_change)
            score = boss_obj.health
            check_collisions(lasers, player_obj, difficulty, boss_obj)  # Do things touch other things?
        else:
            update_lasers(lasers, time_change)
            make_lasers(lasers, difficulty)  # If lasers despawn, make more to replace them
            check_time(debug_state, timers, score, score_thresh)
            score += check_collisions(lasers, player_obj, difficulty, boss_obj)  # Do things touch other things?
            if score >= score_thresh:
                score = score_thresh

        update_mouse(player_obj)

        game_running, game_state, game_quit = \
            update_events(game_running, game_state, game_quit, lasers)

        debug_state, last_spray_toggle, spray_toggle, time_change, debug_powerups = \
            update_keyboard(debug_state, timers, spray_toggle, player_obj, time_change, debug_powerups)

        update_bombs(player_obj)

        update_shots(player_obj.shots, time_change)

        time_change, powerup_display = \
            update_player(player_obj, debug_state)

        spawn_powerups(POWERUP_CHANCE, powerups)  # Chance that a powerup will spawn on any given second

        update_powerups(powerups, player_obj, debug_powerups)  # Draw powerups

        draw_gui(timers, difficulty, powerup_display, score, score_thresh)  # Show the powerups being used, the level, time, etc.

        pygame.display.flip()  # This is required by pygame to render the screen.
    return game_state, game_quit
