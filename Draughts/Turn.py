from Move import Move
from Stack import Stack


class Turn(object):

    def __init__(self):
        self.moves = Stack()

    def push_move(self, move):
        if isinstance(move, Move):
            self.moves.push(move)
        else:
            print("Only put the moves on this stack.")

    def pop_move(self):
        return self.moves.pop()

    def peek_move(self):
        return self.moves.peek()

    def has_moves(self):
        return not self.moves.is_empty()

    def move_count(self):
        return self.moves.size()

    def clear(self):
        self.moves.clear()
