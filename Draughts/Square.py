from Piece import Piece


class Square(object):

    select_left = ["/", "|", "\\"]
    select_right = ["\\", "|", "/"]
    highlight_char = "~"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.content = Piece(-1, 0)
        self.highlighted = False

    def set_content(self, piece):
        assert isinstance(piece, Piece), "Data is not of type 'Piece'"
        self.content.equals(piece)
        for i in range(2):
            if self.y == i * 7 and self.content.faction == i and self.content.rank == 0:
                self.content.rank_up()

    def get_content(self):
        return self.content

    def delete_content(self):
        self.content.clear()

    def abdicate(self):
        self.content.abdicate()

    def print(self, line_no):
        assert 0 <= line_no < 3, "Line number, '%r' invalid for squares" % line_no
        if self.content.selected == 1:
            return self.select_left[line_no] + self.content.print(line_no) + self.select_right[line_no]
        elif self.highlighted:
            return self.highlight_char + self.content.print(line_no) + self.highlight_char
        if (self.x + self.y) % 2 == 0:
            return " " + self.content.print(line_no) + " "
        else:
            return "███████"

    def highlight(self):
        if not self.highlighted:
            self.highlighted = True
        else:
            print("Already highlighted.")

    def low_light(self):
        if self.highlighted:
            self.highlighted = False
        else:
            print("Not highlighted to start with.")

    def select_piece(self):
        self.content.select()

    def deselect_piece(self):
        self.content.deselect()
