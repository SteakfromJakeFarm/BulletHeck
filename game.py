from lib import *
import time
from config import *

pygame.init()  # Its a pygame thing. Idk. It tells me to call this first.


def main_menu(difficulty, win):  # Draws the main menu. Once the user select an option, it returns the result.
    menu_running = True  # Is the menu running?
    menu_quit = False  # Did the user want to quit?
    menu_spot = 0  # Position that the cursor is over
    debug_state = False  # Is debug(cheat) mode on?

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
    game_state = ''
    time_start = time.time()
    frame_count = 0
    spray_toggle = False
    spray_angle = 0.0
    last_spray_toggle = time.time()
    last_debug_state = debug_state
    last_debug_toggle = time.time()
    powerups = []

    pygame.event.clear()  # Good for the environment

    player_obj = Player.Player(300, 300, debug_state)

    while game_running:
        CLOCK.tick(FRAMERATE)
        SCREEN.fill(COLOR_SCREEN)

        frame_count += 1

        last_debug_state, last_debug_toggle, spray_angle, spray_toggle = \
            update_player(player_obj, last_debug_state, last_debug_toggle, spray_angle, spray_toggle, debug_state)

        try:
            player_obj, last_debug_state, last_debug_toggle = \
                update_player_debug(player_obj, last_debug_state, last_debug_toggle, debug_state)
        except TypeError:
            pass

        draw_gui(time_start, difficulty)

        make_lasers(lasers, difficulty)

        check_time(debug_state, time_start)

        update_mouse(player_obj)

        game_running, game_state, game_quit = \
            update_events(game_running, game_state, game_quit, lasers)

        debug_state, last_spray_toggle, spray_toggle = \
            update_keyboard(debug_state,last_debug_toggle, last_spray_toggle, spray_toggle, player_obj)

        spawn_powerups(0.20, powerups)  # Chance that a powerup will spawn on any given second

        update_lasers(lasers)

        update_shots(player_obj.shots)

        update_powerups(powerups, player_obj)

        check_collisions(lasers, player_obj, debug_state)

        pygame.display.flip()  # This is required by pygame to render the screen.

    return game_state, game_quit
