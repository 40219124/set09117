from Stack import Stack
from Turn import Turn


class Timeline(object):

    def __init__(self):
        self.past = Stack()
        self.future = Stack()

    def add_turn(self, move):
        self.past.push(move)
        self.future.clear()

    def add_past(self, move):
        self.past.push(move)

    def add_future(self, move):
        self.future.push(move)

    def count_past(self):
        return self.past.size()

    def count_future(self):
        return self.future.size()

    def undo(self):
        if self.count_past() > 0:
            past_turn = self.past.pop()
            return past_turn
        else:
            print("Nothing to undo.")
            return Turn()

    def redo(self):
        if self.count_future() > 0:
            future_move = self.future.pop()
            return future_move
        else:
            print("Nothing to redo.")
            return Turn()

