import game

real_running = True
i = 1
win = False
while real_running:
    if not game.main_menu(win):
        break
    results = game.game(i)
    if results == "win":
        win = True
        i += 1
    elif results == "loose":
        win = False
        i = 1
    elif results == False:
        break
