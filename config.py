import pygame

VERSION = '0.3b'
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
COLOR_PLAYER = (0, 100, 0)  # Color of the player's hit box
COLOR_LASER = (100, 0, 100)  # Color of the lasers' hit boxes
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

SCREEN = pygame.display.set_mode((WINDOW_X, WINDOW_Y))  # Create screen on the display
CLOCK = pygame.time.Clock()  # Create the clock object. Useful for implementing the framerate
