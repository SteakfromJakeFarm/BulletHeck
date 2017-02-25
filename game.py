import pygame
import lib
import time
import math

VERSION = '0.2'
DEBUG = False

FRAMERATE = 60
WINDOW_X = 600
WINDOW_Y = 600
LASER_THRESHOLD = 50
TIME_LIMIT = 5
PLAYER_COLLIDE = True
PLAYER_SHOOT_COOLDOWN = 0.5
PLAYER_SPEED = 1
FONT = "Comic Sans MS"
COLOR_START = (10, 10, 200)
COLOR_QUIT = (200, 0, 0)
COLOR_SCREEN = (255, 255, 255)
COLOR_TIMER = (100, 0, 255)
COLOR_PLAYER = (0, 100, 0)
COLOR_LASER = (100, 0, 100)
COLOR_DED = (0, 0, 255)
COLOR_WIN = (0, 200, 0)
COLOR_SHOT = (255, 0, 0)
COLOR_DIFFICULTY = (100, 50, 170)
FONT_SIZE = 20
LASER_MIN_SPEED = 1
LASER_MULTIPLIER = 3
LASER_RESPAWN = True

if DEBUG:
    TIME_LIMIT = 99
    PLAYER_COLLIDE = False
    PLAYER_SHOOT_COOLDOWN = 0.0
    PLAYER_SPEED = 3
    COLOR_PLAYER = (100, 100, 100)

pygame.init()

SCREEN = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
CLOCK = pygame.time.Clock()


def main_menu(win):
    menu_running = True
    menu_quit = False
    menu_spot = 0
    if win:
        label_start = pygame.font.SysFont(FONT, 20).render("Continue", 1, COLOR_START)
    else:
        label_start = pygame.font.SysFont(FONT, 20).render("Start", 1, COLOR_START)
    label_quit = pygame.font.SysFont(FONT, 20).render("Quit", 1, COLOR_QUIT)
    while menu_running:
        pygame.event.pump()
        CLOCK.tick(FRAMERATE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_quit = True

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] and menu_spot > 0:
            menu_spot -= 1
        elif pressed[pygame.K_DOWN] and menu_spot < 1:
            menu_spot += 1
        elif pressed[pygame.K_LEFT] and menu_spot > 0:
            menu_spot -= 1
        elif pressed[pygame.K_RIGHT] and menu_spot < 1:
            menu_spot += 1
        elif pressed[pygame.K_RETURN]:
            if menu_spot == 0:
                menu_running = False
            elif menu_spot == 1:
                return False

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

        SCREEN.fill(COLOR_SCREEN)
        SCREEN.blit(label_start, ((WINDOW_X / 2) - 50, (WINDOW_Y / 2 - 50)))
        SCREEN.blit(label_quit, ((WINDOW_X / 2) - 50, (WINDOW_Y / 2)))

        pygame.display.flip()

        if menu_quit:
            return False
    return True


def game(difficulty):
    lasers = []
    game_quit = False
    game_running = True
    player_obj = lib.Player(PLAYER_SHOOT_COOLDOWN, PLAYER_SPEED)

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

    def make_lasers(laser_list, x, frame):
        for i in range(0, x, 1):
            if len(laser_list) < LASER_THRESHOLD * difficulty and (LASER_RESPAWN or frame):
                laser_shot = lib.Laser(LASER_MIN_SPEED, LASER_MULTIPLIER + difficulty)
                laser_list.append(laser_shot)

    def update_player(player, key):
        player.movement(key)
        player.update()
        pygame.draw.rect(SCREEN, COLOR_PLAYER, player.hitbox, 0)

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

    time_start = time.time()
    first_frame = True
    frame_count = 0
    while game_running:
        frame_count += 1
        pygame.event.pump()

        if time.time() >= time_start + TIME_LIMIT:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"event": "win"}))

        make_lasers(lasers, 1, first_frame)

        CLOCK.tick(FRAMERATE)

        SCREEN.fill(COLOR_SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                game_quit = True

            elif event.type == pygame.KEYDOWN:
                key = event.key
                update_player(player_obj, key)

            elif event.type == pygame.USEREVENT:
                if event.event == 'hit':
                    label = pygame.font.SysFont(FONT, FONT_SIZE).render("ded", 1, COLOR_DED)
                    SCREEN.blit(label, (300, 300))
                    pygame.display.flip()

                    time.sleep(3)

                    for laser in lasers:  # Probably redundant. Better safe than sorry for now...
                        lasers.remove(laser)

                    game_running = False
                    game_state = 'loose'

                elif event.event == 'win':
                    label = pygame.font.SysFont(FONT, FONT_SIZE).render("Win!", 1, COLOR_WIN)
                    SCREEN.blit(label, (300, 300))
                    pygame.display.flip()

                    time.sleep(3)

                    for laser in lasers:
                        lasers.remove(laser)

                    game_running = False
                    game_state = 'win'

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            update_player(player_obj, pygame.K_UP)

        if pressed[pygame.K_DOWN]:
            update_player(player_obj, pygame.K_DOWN)

        if pressed[pygame.K_RIGHT]:
            update_player(player_obj, pygame.K_RIGHT)

        if pressed[pygame.K_LEFT]:
            update_player(player_obj, pygame.K_LEFT)

        mouse_pressed = pygame.mouse.get_pressed()

        if mouse_pressed[0]:
            x, y = pygame.mouse.get_pos()
            player_obj.shoot(x, y)

        # check for collisions with player or player's lasers
        for laser in lasers:
            if player_obj.hitbox.colliderect(laser.hitbox) and PLAYER_COLLIDE:  # If player has hit a laser, post a 'hit' event
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"event": "hit"}))
            for shot in player_obj.shots:
                if shot.hurtbox.colliderect(laser.hitbox):  # If a player bullet has hit a laser, destroy both
                    try:
                        lasers.remove(laser)
                        player_obj.shots.remove(shot)
                    except ValueError:
                        pass

        player_obj.update()
        pygame.draw.rect(SCREEN, COLOR_PLAYER, player_obj.hitbox, 0)

        update_lasers(lasers)

        update_shots(player_obj.shots)

        timer = pygame.font.SysFont(FONT, FONT_SIZE).render(str(int(time.time() - time_start)), 1, COLOR_TIMER)
        SCREEN.blit(timer, (0, 0))

        level = pygame.font.SysFont(FONT, FONT_SIZE).render(str(difficulty), 1, COLOR_DIFFICULTY)
        SCREEN.blit(level, (WINDOW_X-50, 0))

        if first_frame:
            first_frame = False

        pygame.display.flip()  # This is required to render the screen

        if game_quit:
            return False
    return game_state
