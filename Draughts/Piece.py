class Piece(object):

    no_piece = ["     ", "     ", "     "]
    white = ["     ", "╔╦═╦╗", "╚╩═╩╝"]
    black = ["┌───┐", "└───┘", "     "]
    white_crown = ["╔═══╗", "╠^-^╣", "╚═══╝"]
    black_crown = ["┌───┐", "│*_*│", "└───┘"]
    '''
    ╠ ╣ ╩ ╦ ╬ ║ ╔ ╗ ╚ ╝ ═
    ├ ┤ ┴ ┬ ┼ │ ┌ ┐ └ ┘ ─
    , "║   ║"
     "│░░░│",
    '''

    def __init__(self, faction, rank):
        self.faction = faction
        self.crown = rank
        self.selected = False

    def rank_up(self):
        self.crown = True

    def abdicate(self):
        self.crown = False

    def select(self):
        if not self.selected:
            self.selected = True
        else:
            print("Already selected this piece.")

    def deselect(self):
        if self.selected:
            self.selected = False
        else:
            print("This piece wasn't selected.")

    def equals(self, piece):
        self.faction = piece.faction
        self.crown = piece.crown

    def clear(self):
        self.faction = -1
        self.crown = False
        self.selected = 0

    def print(self, line_no):
        output = ""
        if self.faction < 0:
            output += Piece.no_piece[line_no]
        elif self.faction == 0:
            if self.crown:
                output += Piece.white_crown[line_no]
            else:
                output += Piece.white[line_no]
        else:
            if self.crown:
                output += Piece.black_crown[line_no]
            else:
                output += Piece.black[line_no]
        output += ""
        return output
