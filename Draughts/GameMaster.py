from Board import Board
from GameLogic import GameLogic
from ArtI import ArtI
from Turn import Turn
from Move import Move
from Timeline import Timeline


def str_to_tup(string):
    return int(string[0: 1]), int(string[1])


def tup_to_str(tup):
    return GameMaster.numbersToLetters[tup[0]] + str(tup[1])


class GameMaster(object):

    lettersToNumbers = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    numbersToLetters = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    faction_to_string = {0: "White", 1: "Black"}

    def __init__(self):
        self.board = Board()
        self.timeline = Timeline()
        self.active_faction = 0  # white = 0, black = 1
        self.turn = Turn()
        self.highlighted = []
        self.forced = []
        self.mid_turn = False
        self.selected = (-1, -1)
        self.message = ""
        self.ai_choices = []

    def run_game(self):
        play_on = True
        # while playing
        while play_on:
            friendly_pieces = self.board.get_faction_pieces(self.active_faction)
            self.no_force()
            if len(friendly_pieces) == 0:
                play_on = False
                self.message = self.faction_to_string[self.active_faction] + " is out of usable pieces.\n" \
                    + self.faction_to_string[(self.active_faction + 1) % 2] + " is the winner."
            else:
                enemy_pieces = self.board.get_faction_pieces((self.active_faction + 1) % 2)
                for loc in friendly_pieces:
                    can_take = GameLogic.take_options(self.board, loc)
                    if len(can_take) > 0:
                        self.forced.append(loc)
                if len(self.forced) == 0:
                    for loc in friendly_pieces:
                        can_move = GameLogic.move_options(self.board, loc)
                        if len(can_move) > 0:
                            self.forced.append(loc)
                if len(self.forced) > 0:
                    for loc in self.forced:
                        self.board.force(loc)
                else:
                    play_on = False
                    self.message = self.faction_to_string[self.active_faction] + " is unable to move their pieces.\n" \
                        + self.faction_to_string[(self.active_faction + 1) % 2] + " is the winner."
            print()
            print("------------------------------------------------------------")
            print()
            self.board.print(self.active_faction)
            print()
            print(self.message)
            print()
            print()
            self.message = ""
            # Ai turn
            if self.active_faction == 1 and self.timeline.count_future() == 0:
                self.ai_choices = ArtI.get_turn(self.board, self.forced, self.active_faction)
                for move in self.ai_choices:
                    self.turn.push_past(move)
                self.timeline.add_future(self.turn)
                self.redo()
                self.turn = Turn()
                self.swap_turns()
            # Not ai turn
            else:
                # take input
                text_prompt = input().lower()
                # close if exit is typed
                if text_prompt == "exit":
                        play_on = False
                else:
                    # If an undo is prompted
                    if text_prompt == "undo" or text_prompt == "u":
                        # If half way through a turn undo current progress
                        if self.mid_turn:
                            self.undo_half()
                            self.mid_turn = False
                            self.message = "Reset to the start of your turn"
                        # If no piece is currently selected undo a turn
                        elif self.selected == (-1, -1):
                            # Undo a turn if there are turns to undo
                            if self.timeline.count_past() > 0:
                                self.undo()
                                self.swap_turns()
                                self.message = "Turn undone."
                            else:
                                self.message = "Nothing to undo."
                        # If a piece is selected, undo the selection
                        else:
                            self.message = "Piece deselected."
                        # Do cleaning for all possibilities
                        self.low_light()
                        self.deselect()
                    # If a redo is prompted
                    elif (text_prompt == "redo" or text_prompt == "r") and not self.mid_turn:
                        # If there are turns to be redone
                        if self.timeline.count_future() > 0:
                            self.redo()
                            self.low_light()
                            self.deselect()
                            self.swap_turns()
                            self.message = "Turn redone."
                        else:
                            self.message = "Nothing to redo."
                    # if a 2 character input, assume grid square and format appropriately
                    elif len(text_prompt) == 2:
                        if (text_prompt[0] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']) and \
                                (text_prompt[1] in ['1', '2', '3', '4', '5', '6', '7', '8']):
                            prompt = (self.lettersToNumbers[text_prompt[0]], int(text_prompt[1]) - 1)
                            # If no piece is currently selected
                            if self.selected == (-1, -1):
                                # If you didn't pick one of your pieces try again
                                if self.active_faction != self.board.piece_faction(prompt):
                                    self.message = "'" + text_prompt + "' is not one of your pieces."
                                # If the prompt is not a forced take
                                elif not (prompt in self.forced):
                                    self.message = "A different piece is required to move."
                                # Else select the piece
                                else:
                                    self.sel_and_high(prompt)
                                    self.message = "'" + text_prompt + "' selected."
                            # If you picked the already selected one, deselect it
                            elif self.selected == prompt and not self.mid_turn:
                                self.deselect()
                                self.low_light()
                                self.message = "'" + text_prompt + "' deselected."
                            # If you picked another of your faction, make it the selected piece
                            elif self.board.piece_faction(prompt) == self.active_faction and not self.mid_turn:
                                self.deselect()
                                self.low_light()
                                self.sel_and_high(prompt)
                                self.message = "'" + text_prompt + "' selected."
                            # If an empty space is selected move there
                            elif self.board.square_highlighted(prompt):
                                # Set up basic move
                                move = Move()
                                # If moving into an adjacent empty space
                                if -1 <= prompt[0] - self.selected[0] <= 1:
                                    # Make move
                                    move.equals(self.board.move(self.selected, prompt))
                                    # Deselect the piece
                                    self.selected = (-1, -1)
                                    self.low_light()
                                # If moving to a non adjacent space (taking a piece)
                                else:
                                    # Take the piece and deselect everything
                                    move.equals(self.board.move(self.selected, prompt))
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
                                self.turn.push_past(move)
                                self.message = "Moved piece to '" + text_prompt + "'."
                                # If not mid-turn push the Turn to the timeline and swap teams
                                if not self.mid_turn:
                                    self.timeline.add_turn(self.turn)
                                    self.turn = Turn()
                                    self.swap_turns()
                            # No valid turn was taken
                            else:
                                self.message = "'" + text_prompt + "' is not a valid location to move to."
                            self.board.find_pieces()
                        else:
                            self.message = "'" + text_prompt + "' is not an existing grid square."
                    # No recognised command given
                    else:
                        self.message = "'" + text_prompt + "' is not in the list of valid commands."

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
        if self.selected != (-1, -1):
            self.board.deselect_piece(self.selected)
            self.selected = (-1, -1)

    def low_light(self):
        if len(self.highlighted) > 0:
            for loc in self.highlighted:
                self.board.low_light_square(loc)
        self.highlighted = []

    def no_force(self):
        if len(self.forced) > 0:
            for loc in self.forced:
                self.board.no_force(loc)
        self.forced = []

    def swap_turns(self):
        # Swap the active faction
        if self.active_faction == 0:
            self.active_faction = 1
        else:
            self.active_faction = 0

    def undo(self):
        deque = self.timeline.undo()
        while deque.has_moves() > 0:
            move = deque.pop_past()
            self.board.set_piece(move.start, self.board.get_piece(move.end))
            self.board.delete_piece(move.end)
            if move.crowned:
                self.board.abdicate(move.start)
            if move.did_take:
                self.board.set_piece(move.took_from, move.took_piece)
        self.board.find_pieces()

    def undo_half(self):
        while self.turn.has_moves() > 0:
            move = self.turn.pop_past()
            self.board.set_piece(move.start, self.board.get_piece(move.end))
            self.board.delete_piece(move.end)
            if move.crowned:
                self.board.abdicate(move.start)
            if move.did_take:
                self.board.set_piece(move.took_from, move.took_piece)
        self.turn = Turn()
        self.board.find_pieces()

    def redo(self):
        deque = self.timeline.redo()
        while deque.has_moves() > 0:
            move = deque.pop_future()
            self.board.set_piece(move.end, self.board.get_piece(move.start))
            self.board.delete_piece(move.start)
            if move.did_take:
                self.board.delete_piece(move.took_from)
        self.board.find_pieces()
