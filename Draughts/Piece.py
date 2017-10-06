class Piece(object):

    no_piece = ["   ", "   ", "   "]
    white = [" O ", "OOO", " O "]
    black = [" X ", "XXX", " X "]
    white_crown = ["O O", " O ", "O O"]
    black_crown = ["X X", " X ", "X X"]

    def __init__(self, faction, rank):
        self.faction = faction
        self.rank = rank
        self.selected = 0

    def rank_up(self):
        self.rank += 1

    def select(self):
        assert self.selected != 1, "Piece already selected"
        self.selected = 1

    def deselect(self):
        assert self.selected != 0, "Piece not selected"
        self.selected = 0

    def equals(self, piece):
        self.faction = piece.faction
        self.rank = piece.rank

    def clear(self):
        self.faction = -1
        self.rank = 0
        self.selected = 0

    def print(self, line_no):
        output = " "
        if self.faction < 0:
            output += Piece.no_piece[line_no]
        elif self.faction == 0:
            if self.rank == 1:
                output += Piece.white_crown[line_no]
            else:
                output += Piece.white[line_no]
        else:
            if self.rank == 1:
                output += Piece.black_crown[line_no]
            else:
                output += Piece.black[line_no]
        output += " "
        return output
