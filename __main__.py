import game

real_running = True
i = 1
win = False
while real_running:
    menu_quit, debug = game.main_menu(win, i)

    if menu_quit:
        break

    game_result, game_quit = game.game(i, debug)

    if game_quit:
        break

    if game_result == "win":
        win = True
        i += 1
    elif game_result == "lose":
        win = False
        i = 1
    elif not game_result:
        break
