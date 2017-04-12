import game
import math

running = True
i = 1
win = False
score = 0
checkpoint_score = 0
while running:
    #if i%5 == 0:
    #    checkpoint_score = score

    menu_quit, debug = game.main_menu(i, win)

    if menu_quit:
        break

    game_result, game_quit = game.game(i, debug)

    if game_quit:
        break

    if game_result == "win":
        win = True
        i += 1
    elif game_result == "time" or game_result == "hit":
        win = False
        i = int(math.floor(i-(i % 5)))  # This creates a checkpoint every 5 levels
        if i <= 0:  # safety first
            i = 1
    elif not game_result:
        break
