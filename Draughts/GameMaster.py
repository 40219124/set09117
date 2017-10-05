from Board import Board


lettersToNumbers = {'A': 0, 'B': 1, 'C': 2, 'D': 3,
                    'E': 4, 'F': 5, 'G': 6, 'H': 7}

board = Board()


selected = ""
# while playing
while True:
    board.print()
    # take input
    prompt = input()
    # select square
    if prompt.lower() == "exit":
        break
    if len(prompt) == 2:
        prompt = str(int(prompt[1]) - 1) + str(lettersToNumbers[prompt[0: 1].capitalize()])
    if selected == "":
        selected = prompt
        board.select_piece(prompt)
        continue
    elif selected == prompt:
        board.deselect_piece(selected)
    else:
        board.move(selected, prompt)
    selected = ""
    # if not your piece repeat
    # else calculate moves
    # draw highlights
    # take input
    # if highlight selected move piece there
    # if friendly piece selected draw for that instead
    # else repeat
    # swap active colour
