from Piece import Piece


class Square(object):

    select_left = ["/", "|", "\\"]
    select_right = ["\\", "|", "/"]

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
        if self.content.selected == 1:
            return self.select_left[line_no] + self.content.print(line_no) + self.select_right[line_no]
        return " " + self.content.print(line_no) + " "

    def select_piece(self):
        self.content.select()

    def deselect_piece(self):
        self.content.deselect()
