from GameMaster import GameMaster

while True:
    gm = GameMaster()
    value = gm.run_game()
    if value < 0:
        break
