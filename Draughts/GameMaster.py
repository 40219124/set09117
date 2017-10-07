from Board import Board
from GameLogic import GameLogic


def str_to_tup(string):
    return int(string[0: 1]), int(string[1])


class GameMaster(object):

    lettersToNumbers = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    def __init__(self):
        self.board = Board()
        self.active_faction = 0
        self.highlighted = []
        self.selected = (-1, -1)

    def run_game(self):
        self.board.print()
        # while playing
        while True:
            # take input
            prompt = input().lower()
            # close if exit is typed
            if prompt == "exit":
                break
            # if a 2 character input, assume grid square and format appropriately
            elif len(prompt) == 2:
                if (prompt[0] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']) and \
                        (prompt[1] in ['1', '2', '3', '4', '5', '6', '7', '8']):
                    prompt = (self.lettersToNumbers[prompt[0]], int(prompt[1]) - 1)
                    print(prompt)
                else:
                    print("Invalid grid square.")
                    continue
                # If no piece is currently selected
                if self.selected == (-1, -1):
                    # If you picked one of your pieces it is now selected
                    if self.active_faction != self.board.piece_faction(prompt):
                        print("Not one of your pieces.")
                        continue
                    self.sel_and_high(prompt)
                # If you picked the already selected one, deselect it
                elif self.selected == prompt:
                    self.desel_and_low()
                # If you picked another of your faction, make it the selected piece
                elif self.board.piece_faction(prompt) == self.active_faction:
                    self.desel_and_low()
                    self.sel_and_high(prompt)
                # If an empty space is selected move there
                elif self.board.square_highlighted(prompt):
                    self.board.move(self.selected, prompt)
                    # Swap the active faction
                    if self.active_faction == 0:
                        self.active_faction = 1
                    else:
                        self.active_faction = 0
                    # Deselect the piece
                    self.selected = (-1, -1)
                    if len(self.highlighted) > 0:
                        for loc in self.highlighted:
                            self.board.low_light_square(loc)
                    self.highlighted = []
                # No valid turn was taken
                else:
                    print("Please select a valid location to move to.")
                    continue
                # Show the updated board
                self.board.print()
            # No recognised command given
            else:
                print("Please enter a valid command.")

            # else calculate moves
            # draw highlights

    def get_options(self, prompt):
        self.highlighted = GameLogic.take_options(self.board, prompt)
        if self.highlighted.__len__() == 0:
            self.highlighted = (GameLogic.move_options(self.board, prompt))

    def sel_and_high(self, prompt):
        self.selected = prompt
        self.board.select_piece(self.selected)
        self.get_options(prompt)
        if len(self.highlighted) > 0:
            for loc in self.highlighted:
                self.board.highlight_square(loc)

    def desel_and_low(self):
        self.board.deselect_piece(self.selected)
        self.selected = (-1, -1)
        if len(self.highlighted) > 0:
            for loc in self.highlighted:
                self.board.low_light_square(loc)
        self.highlighted = []
