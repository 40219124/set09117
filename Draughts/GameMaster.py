from Board import Board
from GameLogic import GameLogic
from Turn import Turn
from Move import Move
from Timeline import Timeline


def str_to_tup(string):
    return int(string[0: 1]), int(string[1])


class GameMaster(object):

    lettersToNumbers = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

    def __init__(self):
        self.board = Board()
        self.timeline = Timeline()
        self.active_faction = 0  # white = 0, black = 1
        self.turn = Turn()
        self.highlighted = []
        self.mid_turn = False
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
            elif prompt == "undo" or prompt == "u":
                if self.mid_turn:
                    self.undo_half()
                    self.mid_turn = False
                elif self.timeline.count_past() > 0 and self.selected == (-1, -1):
                    self.undo()
                    self.swap_turns()
                self.low_light()
                self.selected = (-1, -1)
                self.board.print()
            elif (prompt == "redo" or prompt == "r") and not self.mid_turn:
                if self.timeline.count_future() > 0:
                    self.redo()
                    self.board.print()
                    self.swap_turns()
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
                    # If you didn't pick one of your pieces try again
                    if self.active_faction != self.board.piece_faction(prompt):
                        print("Not one of your pieces.")
                        continue
                    # Else select the piece
                    self.sel_and_high(prompt)
                # If you picked the already selected one, deselect it
                elif self.selected == prompt and not self.mid_turn:
                    self.deselect()
                    self.low_light()
                # If you picked another of your faction, make it the selected piece
                elif self.board.piece_faction(prompt) == self.active_faction and not self.mid_turn:
                    self.deselect()
                    self.low_light()
                    self.sel_and_high(prompt)
                # If an empty space is selected move there
                elif self.board.square_highlighted(prompt):
                    # Set up basic move
                    move = Move()
                    move.start = self.selected
                    move.end = prompt
                    # If becoming a king this turn
                    if (8 - self.active_faction) % 8 == prompt[1] and self.board.get_piece(self.selected):
                        move.crowned = True
                    # If moving into an adjacent empty space
                    if -1 <= prompt[0] - self.selected[0] <= 1:
                        self.board.move(self.selected, prompt)
                        # Deselect the piece
                        self.selected = (-1, -1)
                        self.low_light()
                    # If moving to a non adjacent space (taking a piece)
                    else:
                        took_from = ((self.selected[0] + prompt[0]) / 2, (self.selected[1] + prompt[1]) / 2)
                        # Add additional data to the move
                        move.did_take = True
                        move.took_from = took_from
                        move.took_piece.equals(self.board.get_piece(took_from))
                        # Take the piece and deselect everything
                        self.board.move(self.selected, prompt)
                        self.low_light()
                        # Find the options for taking pieces from the new position
                        self.highlighted = GameLogic.take_options(self.board, prompt)
                        # If there are options lock on to the piece, and highlight a new set of moves
                        if len(self.highlighted) > 0:
                            self.mid_turn = True
                            self.sel_and_high(prompt)
                        # Else end the turn and deselect as normal
                        else:
                            self.mid_turn = False
                            self.selected = (-1, -1)
                    # Add move to current turn
                    self.turn.push_move(move)
                    # If not mid-turn push the Turn to the timeline and swap teams
                    if not self.mid_turn:
                        self.timeline.add_turn(self.turn)
                        self.turn = Turn()
                        self.swap_turns()
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
        if len(self.highlighted) == 0:
            self.highlighted = (GameLogic.move_options(self.board, prompt))

    def sel_and_high(self, prompt):
        self.selected = prompt
        self.board.select_piece(self.selected)
        self.get_options(prompt)
        if len(self.highlighted) > 0:
            for loc in self.highlighted:
                self.board.highlight_square(loc)

    def deselect(self):
        print(self.selected)
        if self.selected != (-1, -1):
            self.board.deselect_piece(self.selected)
            self.selected = (-1, -1)
        print(self.selected)

    def low_light(self):
        if len(self.highlighted) > 0:
            for loc in self.highlighted:
                self.board.low_light_square(loc)
        self.highlighted = []

    def swap_turns(self):
        # Swap the active faction
        if self.active_faction == 0:
            self.active_faction = 1
        else:
            self.active_faction = 0

    def undo(self):
        stack = self.timeline.undo()
        future = Turn()
        while stack.has_moves() > 0:
            move = stack.pop_move()
            future.push_move(move)
            self.board.set_piece(move.start, self.board.get_piece(move.end))
            self.board.delete_piece(move.end)
            if move.crowned:
                self.board.abdicate(move.start)
            if move.did_take:
                self.board.set_piece(move.took_from, move.took_piece)
        self.timeline.add_future(future)

    def undo_half(self):
        while self.turn.has_moves() > 0:
            move = self.turn.pop_move()
            self.board.set_piece(move.start, self.board.get_piece(move.end))
            self.board.delete_piece(move.end)
            if move.crowned:
                self.board.abdicate(move.start)
            if move.did_take:
                self.board.set_piece(move.took_from, move.took_piece)
        self.turn = Turn()

    def redo(self):
        stack = self.timeline.redo()
        past = Turn()
        while stack.has_moves() > 0:
            move = stack.pop_move()
            past.push_move(move)
            self.board.set_piece(move.end, self.board.get_piece(move.start))
            self.board.delete_piece(move.start)
            if move.did_take:
                self.board.delete_piece(move.took_from)
        self.timeline.add_past(past)
