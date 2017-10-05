class Piece(object):

    no_piece = ["   ", "   ", "   "]
    white = [" O ", "OOO", " O "]
    black = [" X ", "XXX", " X "]

    def __init__(self, faction, rank):
        self.faction = faction
        self.rank = rank

    def rank_up(self):
        self.rank += 1

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
