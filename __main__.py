import game
import math

running = True
i = 1
win = False
score = 0
checkpoint_score = 0
while running:
    menu_quit, debug = game.main_menu(i, win)

    if menu_quit:
        break

    game_result, game_quit = game.game(i, score, debug)
    if game_quit:
        break

    if game_result == "win":
        win = True
        i += 1
    elif game_result == "time" or game_result == "hit":
        win = False

        # This checkpoints every five levels.
        # If you lose on 7, you go to 6. If you lose on 3, you go to 1, etc.
        if i % 5 == 0:
            i -= 4
        else:
            i = int(math.floor(i-(i % 5)))+1
        if i <= 0:  # safety first
            i = 1
    elif not game_result:
        break
