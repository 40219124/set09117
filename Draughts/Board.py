from Square import Square
from Piece import Piece


class Board(object):

    def __init__(self):
        self.squares = {}
        for x in range(8):
            for y in range(8):
                self.squares[(x, y)] = Square(x, y)
        self.default_board()
        self.number_column = []
        for i in range(8):
            self.number_column.append([])
            self.number_column[i] = ["   ", " " + str(i+1) + " ", "   "]

    def default_board(self):
        '''self.left_row(0, 1)
        self.right_row(1, 1)
        self.left_row(2, 1)'''
        self.left_row(4, 1)
        # self.right_row(5, 0)
        self.left_row(6, 0)
        # self.right_row(7, 0)
        self.make_row(0, 1)
        self.make_row(1, 0)

    def left_row(self, row, faction):
        for i in range(0, 8, 2):
            piece = Piece(faction, 1)
            self.squares[(i, row)].set_content(piece)

    def right_row(self, row, faction):
        for i in range(1, 8, 2):
            piece = Piece(faction, 0)
            self.squares[(i, row)].set_content(piece)

    def make_row(self, row, faction):
        for i in range(0, 8):
            if (row + i) % 2 == 0:
                self.squares[(i, row)].set_content(Piece(faction, 0))

    def print(self):

        print("      A      B      C      D      E      F      G      H   ")
        # print("---+-------+-------+-------+-------+-------+-------+-------+-------|")
        rh = 4
        for line_no in range(rh * 8 - 1):
            if line_no % rh == rh-1:
                heck = 5
                # print("---+-------+-------+-------+-------+-------+-------+-------+-------|")
            else:
                output = self.number_column[line_no // rh][line_no % rh] # + "|"
                for column in range(8):
                    output += self.square_text(line_no, column)
                print(output)
        # print("---'-------'-------'-------'-------'-------'-------'-------'-------'")

    def square_text(self, line_no, column):
        return Square.print(self.squares[(column, line_no // 4)], line_no % 4) # + "|"

    def move(self, start, finish):
        self.squares[finish].set_content(self.squares[start].content)
        self.squares[start].deselect_piece()
        self.squares[start].delete_content()

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
        return self.squares[piece].content.rank

    def square_highlighted(self, loc):
        return self.squares[loc].highlighted
