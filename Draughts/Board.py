from Square import Square
from Piece import Piece


def str_to_tup(string):
    return int(string[0: 1]), int(string[1])


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
        self.left_row(0, 1)
        self.right_row(1, 1)
        self.left_row(2, 1)
        self.right_row(5, 0)
        self.left_row(6, 0)
        self.right_row(7, 0)

    def left_row(self, row, faction):
        for i in range(0, 8, 2):
            piece = Piece(faction, 0)
            self.squares[(row, i)].set_content(piece)

    def right_row(self, row, faction):
        for i in range(1, 8, 2):
            piece = Piece(faction, 0)
            self.squares[(row, i)].set_content(piece)

    def print(self):

        print("   |   A   |   B   |   C   |   D   |   E   |   F   |   G   |   H   |")
        print("---+-------+-------+-------+-------+-------+-------+-------+-------|")
        rh = 4
        for line_no in range(rh * 8 - 1):
            if line_no % rh == rh-1:
                print("---+-------+-------+-------+-------+-------+-------+-------+-------|")
            else:
                output = self.number_column[line_no // rh][line_no % rh] + "|"
                for column in range(8):
                    output += self.square_text(line_no, column)
                print(output)
        print("---'-------'-------'-------'-------'-------'-------'-------'-------'")

    def square_text(self, line_no, column):
        return Square.print(self.squares[(line_no // 4, column)], line_no % 4) + "|"

    def move(self, start, finish):
        self.squares[str_to_tup(finish)].set_content(self.squares[str_to_tup(start)].content)
        self.squares[str_to_tup(start)].deselect_piece()
        self.squares[str_to_tup(start)].delete_content()

    def select_piece(self, piece):
        self.squares[str_to_tup(piece)].select_piece()

    def deselect_piece(self, piece):
        self.squares[str_to_tup(piece)].deselect_piece()
