from Square import Square
from Piece import Piece


class Board(object):

    surround = ["-->", "<--"]

    def __init__(self):
        self.squares = {}
        for x in range(8):
            for y in range(8):
                self.squares[(x, y)] = Square(x, y)
        self.default_board()
        self.whites, self.blacks = [], []
        self.find_pieces()
        self.number_column = []
        for i in range(8):
            self.number_column.append([])
            self.number_column[i] = ["   ", " " + str(i+1) + " ", "   "]

    def default_board(self):
        self.make_row(0, 1)
        self.make_row(1, 1)
        self.make_row(2, 1)
        self.make_row(5, 0)
        self.make_row(6, 0)
        self.make_row(7, 0)

    def test_board(self):
        self.left_row(4, 1)
        self.left_row(6, 0)
        self.make_row(0, 1)
        self.make_row(1, 0)

    def left_row(self, row, faction):
        for i in range(0, 8, 2):
            piece = Piece(faction, 1)
            self.squares[(i, row)].set_content(piece)

    def right_row(self, row, faction):
        for i in range(1, 8, 2):
            piece = Piece(faction, 1)
            self.squares[(i, row)].set_content(piece)

    def make_row(self, row, faction):
        for i in range(0, 8):
            if (row + i) % 2 == 0:
                self.squares[(i, row)].set_content(Piece(faction, 0))

    def find_pieces(self):
        piece_list_white = []
        piece_list_black = []
        for x in range(8):
            for y in range(8):
                if self.get_piece((x, y)).faction == 0:
                    piece_list_white.append((x, y))
                elif self.get_piece((x, y)).faction == 1:
                    piece_list_black.append((x, y))
        self.whites, self.blacks = piece_list_white, piece_list_black

    def print(self, faction):
        self.find_pieces()
        print()
        print()
        w_surround = ["   ", "   "]
        b_surround = w_surround
        if faction == 0:
            w_surround = self.surround
        elif faction == 1:
            b_surround = self.surround
        print("  ╔╦═════════════════════════╦╦┬─────────────────────────┬┐")  # 59 chars long
        print("  ║║  " + w_surround[0] + " WHITE:      " + str(len(self.whites)).zfill(2) + " " + w_surround[1] +
              " ║║│ " + b_surround[0] + " BLACK:      " + str(len(self.blacks)).zfill(2) + " " + b_surround[1] + "  ││")
        print("  ╚╩═════════════════════════╩┴┴─────────────────────────┴┘")
        print("      A      B      C      D      E      F      G      H   ")
        '''
        ╠ ╣ ╩ ╦ ╬ ║ ╔ ╗ ╚ ╝ ═
        ├ ┤ ┴ ┬ ┼ │ ┌ ┐ └ ┘ ─
        , "║   ║"
         "│░░░│",
        '''
        rh = 3
        for line_no in range(rh * 8):
            output = self.number_column[line_no // rh][line_no % rh]
            for column in range(8):
                output += self.squares[column, line_no // rh].print(line_no % rh)
            print(output)

    def square_text(self, line_no, column):
        return Square.print(self.squares[(column, line_no // 4)], line_no % 4)

    def move(self, start, finish):
        self.squares[finish].set_content(self.squares[start].content)
        self.squares[start].deselect_piece()
        self.squares[start].delete_content()
        # If taking a piece
        if not (-1 <= finish[0] - start[0] <= 1):
            taking = ((start[0] + finish[0]) / 2, (start[1] + finish[1]) / 2)
            self.squares[taking].delete_content()

    def highlight_square(self, loc):
        self.squares[loc].highlight()

    def low_light_square(self, loc):
        self.squares[loc].low_light()

    def select_piece(self, piece):
        self.squares[piece].select_piece()

    def deselect_piece(self, piece):
        self.squares[piece].deselect_piece()

    def piece_faction(self, piece):
        return self.squares[piece].content.faction

    def piece_rank(self, piece):
        return self.squares[piece].content.crown

    def square_highlighted(self, loc):
        return self.squares[loc].highlighted

    def get_piece(self, loc):
        return self.squares[loc].get_content()

    def set_piece(self, loc, piece):
        self.squares[loc].set_content(piece)

    def delete_piece(self, loc):
        self.squares[loc].delete_content()

    def get_faction_pieces(self, faction):
        if faction == 0:
            return self.whites
        elif faction == 1:
            return self.blacks

    def abdicate(self, loc):
        self.squares[loc].abdicate()
