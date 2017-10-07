def add_tuples(a, b):
    return a[0] + b[0], a[1] + b[1]


def valid_square(string):
    if int(string[0: 1]) in range(8) and int(string[1]) in range(8):
        return True
    return False


class GameLogic(object):
    def __init__(self):
        self.good = "yes"

    @staticmethod
    def move_options(board, loc):
        options = []
        min_y = -1
        max_y = 1
        if board.piece_rank(loc) == 0:
            if board.piece_faction(loc) == 0:
                max_y = min_y
            else:
                min_y = max_y
        for x in range(-1, 2, 2):
            if 0 <= loc[0] + x < 8:
                for y in range(min_y, max_y + 1, 2):
                    if 0 <= int(loc[1]) + y < 8:
                        check = add_tuples(loc, (x, y))
                        if board.piece_faction(check) < 0:
                            options.append(check)
        return options

    @staticmethod
    def take_options(board, loc):
        options = []
        min_y = -2
        max_y = 2
        if board.piece_rank(loc) == 0:
            if board.piece_faction(loc) == 0:
                max_y = min_y
            else:
                min_y = max_y
        for x in range(-2, 3, 4):
            if 0 <= loc[0] + x < 8:
                for y in range(min_y, max_y + 1, 4):
                    if 0 <= int(loc[1]) + y < 8:
                        check = add_tuples(loc, (x, y))
                        if board.piece_faction(check) < 0:
                            over = add_tuples(loc, (x//2, y//2))
                            if 0 <= board.piece_faction(over) != board.piece_faction(loc):
                                options.append(check)
        return options
