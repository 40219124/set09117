from Piece import Piece


class Square(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.content = Piece(-1, 0)

    def set_content(self, piece):
        assert isinstance(piece, Piece), "Data is not of type 'Piece'"
        self.content = piece

    def delete_content(self):
        self.content = Piece(-1, 0)

    def print(self, line_no):
        assert 0 <= line_no < 3, "Line number, '%r' invalid for squares" % line_no
        return " " + Piece.print(self.content, line_no) + " "
