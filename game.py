import pygame
import lib
import time
import math

VERSION = '0.1'
FRAMERATE = 60
WINDOW_X = 600
WINDOW_Y = 600
LASERS_WANTED = 50

pygame.init()

SCREEN = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
clock = pygame.time.Clock()


def main_menu():
    menu_running = True
    menu_quit = False
    menu_spot = 0
    label1 = pygame.font.SysFont("Comic Sans MS", 20).render("[ Start ]", 1, (0, 0, 255))
    label2 = pygame.font.SysFont("Comic Sans MS", 20).render("Quit", 1, (100, 0, 255))
    while menu_running:
        pygame.event.pump()
        clock.tick(FRAMERATE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_quit = True

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] and menu_spot > 0:
            menu_spot -= 1
        elif pressed[pygame.K_DOWN] and menu_spot < 1:
            menu_spot += 1
        elif pressed[pygame.K_RIGHT] and menu_spot > 0:
            menu_spot += 1
        elif pressed[pygame.K_LEFT] and menu_spot < 1:
            menu_spot -= 1
        elif pressed[pygame.K_RETURN]:
            if menu_spot == 0:
                menu_running = False
            elif menu_spot == 1:
                return False

        if menu_spot == 0:
            label1 = pygame.font.SysFont("Comic Sans MS", 20).render("[ Start ]", 1, (0, 0, 255))
            label2 = pygame.font.SysFont("Comic Sans MS", 20).render("Quit", 1, (100, 0, 255))
        elif menu_spot == 1:
            label1 = pygame.font.SysFont("Comic Sans MS", 20).render("Start", 1, (0, 0, 255))
            label2 = pygame.font.SysFont("Comic Sans MS", 20).render("[ Quit ]", 1, (255, 0, 0))

        SCREEN.fill((255, 255, 255))
        SCREEN.blit(label1, ((WINDOW_X / 2) - 50, (WINDOW_Y / 2 - 50)))
        SCREEN.blit(label2, ((WINDOW_X / 2) - 50, (WINDOW_Y / 2 + 50)))

        pygame.display.flip()

        if menu_quit:
            return False
    return True


def update_lasers(lasers):
    for laser in lasers:
        laser.update()
        if laser.cord_x > 620 and laser.side == 2:
            lasers.remove(laser)
        elif laser.cord_x < 1 and laser.side == 3:
            lasers.remove(laser)
        elif laser.cord_y > 620 and laser.side == 0:
            lasers.remove(laser)
        elif laser.cord_y < 1 and laser.side == 1:
            lasers.remove(laser)
        else:
            pygame.draw.rect(SCREEN, (100, 0, 100), laser.hitbox, 0)


def make_lasers(lasers, x):
    for i in range(1, x, 1):
        laser_shot = lib.Laser()
        lasers.append(laser_shot)


def update_player(player, key):
    player.movement(key)
    player.update()
    pygame.draw.rect(SCREEN, (0, 100, 0), player.hitbox, 0)


def game():
    lasers = []
    game_quit = False
    game_running = True
    player_obj = lib.Player()
    time_start = time.time()
    while game_running:
        pygame.event.pump()
        if time.time() >= time_start + 5:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"event": "win"}))
        if len(lasers) < LASERS_WANTED:
            make_lasers(lasers, 5)
        clock.tick(FRAMERATE)
        SCREEN.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
                game_quit = True
            if event.type == pygame.KEYDOWN:
                key = event.key
                update_player(player_obj, key)
            if event.type == pygame.USEREVENT:
                if event.event == 'ded':
                    label = pygame.font.SysFont("Comic Sans MS", 20).render("ded", 1, (0, 0, 255))
                    SCREEN.blit(label, (300, 300))
                    pygame.display.flip()
                    time.sleep(3)
                    for laser in lasers:
                        lasers.remove(laser)
                    game_running = False
                if event.event == 'win':
                    label = pygame.font.SysFont("Comic Sans MS", 20).render("Win!", 1, (0, 255, 0))
                    SCREEN.blit(label, (300, 300))
                    pygame.display.flip()
                    time.sleep(3)
                    for laser in lasers:
                        lasers.remove(laser)
                    game_running = False

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            update_player(player_obj, pygame.K_UP)
        if pressed[pygame.K_DOWN]:
            update_player(player_obj, pygame.K_DOWN)
        if pressed[pygame.K_RIGHT]:
            update_player(player_obj, pygame.K_RIGHT)
        if pressed[pygame.K_LEFT]:
            update_player(player_obj, pygame.K_LEFT)

        for laser in lasers:
            if player_obj.hitbox.colliderect(laser.hitbox):
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"event": "ded"}))

        player_obj.update()
        pygame.draw.rect(SCREEN, (0, 100, 0), player_obj.hitbox, 0)
        update_lasers(lasers)
        timer = pygame.font.SysFont("Comic Sans MS", 20).render(str(int(time.time() - time_start)), 1, (0, 0, 255))
        SCREEN.blit(timer,(0,0))

        pygame.display.flip()  # This should probably be the last thing called in a loop
        if game_quit:
            return False
    return True
