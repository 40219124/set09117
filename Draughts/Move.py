from Piece import Piece


class Move(object):

    def __init__(self):
        self.start = (-1, -1)
        self.end = (-1, -1)
        self.crowned = False
        self.did_take = False
        self.took_from = (-1, -1)
        self.took_piece = Piece(-1, 0)

    def equals(self, move):
        self.start = move.start
        self.end = move.end
        self.did_take = move.did_take
        self.took_from = move.took_from
        self.took_piece.equals(move.took_piece)
