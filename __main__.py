import game

real_running = True
while real_running:
    if not game.main_menu():
        break
    if not game.game():
        break
