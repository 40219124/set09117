class Piece(object):

    no_piece = ["   ", "   ", "   "]
    white = [" O ", "OOO", " O "]
    black = [" X ", "XXX", " X "]

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

    def print(self, line_no):
        output = " "
        if self.faction < 0:
            output += Piece.no_piece[line_no]
        elif self.faction == 0:
            output += Piece.white[line_no]
        else:
            output += Piece.black[line_no]
        output += " "
        return output
