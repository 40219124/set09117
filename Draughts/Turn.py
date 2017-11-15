from Move import Move
from Deque import Deque


class Turn(object):

    def __init__(self):
        self.moves = Deque()

    def push_past(self, move):
        if isinstance(move, Move):
            self.moves.add_front(move)
        else:
            print("Only put the moves in this deque.")

    def pop_past(self):
        return self.moves.remove_front()

    def push_future(self, move):
        if isinstance(move, Move):
            self.moves.add_rear(move)
        else:
            print("Only put the moves in this deque.")

    def pop_future(self):
        return self.moves.remove_rear()

    '''def peek_move(self):
        return self.moves.peek()'''

    def has_moves(self):
        return not self.moves.is_empty()

    def move_count(self):
        return self.moves.size()

    def equals(self, turn):
        self.moves.equals(turn.moves)

    def clear(self):
        self.moves.clear()
