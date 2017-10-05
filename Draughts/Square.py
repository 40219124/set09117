from Piece import Piece


class Square(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.content = Piece(-1, 0)
        # self.delete_content()

    def set_content(self, piece):
        assert isinstance(piece, Piece), "Data is not of type 'Piece'"
        self.content = piece

    def delete_content(self):
        self.content = Piece(-1, 0)

    def print(self, line_no):
        assert 0 <= line_no < 3, "Line number, '%r' invalid for squares" % line_no
        # if 1 <= line_no <= 3:
        return " " + Piece.print(self.content, line_no) + " "
        # else:
        # return "     "
