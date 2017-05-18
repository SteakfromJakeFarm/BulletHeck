import pygame

VERSION = '0.7'
FRAMERATE = 60  # Times per second that the loop runs
WINDOW_X = 700  # Width of the game window in pixels
WINDOW_Y = 700  # Length of the game window in pixels


# len(laser_list) < (LASER_THRESHOLD * (difficulty/LASER_DIVIDE)) + LASER_ADD
# Tricky math. Handles spawning of lasers each round. After LASER_DIVIDE number of rounds, there will
# be LASER_THRESHOLD + LASER_ADD amount of lasers. LASER_ADD is to offset the low amount of lasers in early rounds.
LASER_START = 20
LASER_ADD = 2

LASER_SPEED_START = 1.5  # Starting speed of lasers
LASER_SPEED_ADD = 0.5  # Amount to add to the max laser speed each round

LASER_RESPAWN = True  # Should the lasers respawn once they move off screen?

TIME_LIMIT = 20  # How long do you need to survive before you can pass to the next level?
PLAYER_COLLIDE = True  # Should the player be hit by lasers?
PLAYER_SHOOT_COOLDOWN = 0.50  # Time between the player's shots
PLAYER_SHOT_SPEED = 4  # Multiplier of the player's shots' speed
PLAYER_SPEED = 2  # Multiplier of the player's speed
FONT = "Comic Sans MS"  # Font to be used in every menu
COLOR_START = (10, 10, 200)  # Color of the "Start" option in the main menu
COLOR_QUIT = (200, 10, 10)  # Color of the "Quit" option in the main menu
COLOR_SCREEN = (255, 255, 255)  # Color of the game background
COLOR_MENU_SCREEN = (255, 255, 255)  # Color of the main menu background
COLOR_TIMER = (100, 0, 255)  # Color of the timer in the game
COLOR_PLAYER = (0, 150, 0)  # Color of the player's hit box
COLOR_LASER = (100, 0, 100)  # Color of the lasers' hit boxes
COLOR_DED = (0, 0, 255)  # Color of the message on the lose screen
COLOR_WIN = (0, 200, 0)  # Color of the message on the win screen
COLOR_SHOT = (255, 0, 0)  # Color of the player's bullets
COLOR_DIFFICULTY = (100, 50, 170)  # Color of the difficulty counter
COLOR_OTHERS = (0, 0, 0)  # Accent color
COLOR_BOSS = (255, 180, 20)  # Color of the boss
FONT_SIZE = 20  # Size of the font of every piece of text
TOGGLE_DEBUFFER = 0.2  # Time between toggling cheat mode
SPEED_SLOW = 0.25  # Speed multiplier of the slowdown powerup
SPEED_FAST = 2.0  # Speed multiplier of the speedup powerup
POWERUP_CHANCE = 0.15  # Chance that a powerup will spawn any given second. 0-1
SHOT_RADIUS = 4  # Radius to draw the player's shots.
POWERUPS = 8  # Number of unique powerup types
SCORE_THRESHOLD = 10
SCORE_MULTIPLIER = 0.25  #

DEBUG_TIME_LIMIT = 99  # Longer for easier debugging
DEBUG_PLAYER_COLLIDE = False  # Invincibility for easier debugging
DEBUG_PLAYER_SHOOT_COOLDOWN = 0.0  # No cooldown for easier debugging
DEBUG_PLAYER_SHOT_SPEED = 3  # Faster shot speed for easier debugging
DEBUG_PLAYER_SPEED = 3  # Faster move speed for easier debugging
DEBUG_COLOR_PLAYER = (0, 0, 0)  # Different color to differentiate from normal mode
DEBUG_COLOR_SCREEN = (100, 100, 100)  # Change the screen's color to signify the mode
DEBUG_SPRAY_DEBUFFER = 0.3  # This is just for fun. Time between toggling the spray mode.
DEBUG_BOMB_DEBUFFER = 0.3
DEBUG_BIGBULLETS_DEBUFFER = 0.3
DEBUG_NOCOLLIDE_DEBUFFER = 0.3
DEBUG_SLOWTIME_DEBUFFER = 0.3
DEBUG_FASTTIME_DEBUFFER = 0.3
DEBUG_TINYMAN_DEBUFFER = 0.3
DEBUG_RING_DEBUFFER = 0.3

SCREEN = pygame.display.set_mode((WINDOW_X, WINDOW_Y))  # Create screen on the display
CLOCK = pygame.time.Clock()  # Create the clock object. Useful for implementing the framerate
