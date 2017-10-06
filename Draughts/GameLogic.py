def string_add_int(string, tup):
    return str(int(string[0:1]) + tup[0]) + str(int(string[1]) + tup[1])


def valid_square(string):
    print(string)
    if int(string[0: 1]) in range(8) and int(string[1]) in range(8):
        return True
    return False


class GameLogic(object):
    def __init__(self):
        self.good = "yes"

    @staticmethod
    def options(board, loc):
        options = []
        for x in range(-1, 2, 2):
            if 0 <= int(loc[1]) + x < 8:
                for y in range(-1, 2, 2):
                    if 0 <= int(loc[0: 1]) + y < 8:
                        check = string_add_int(loc, (y, x))
                        if board.piece_faction(check) < 0:
                            if board.piece_faction(loc) == 0 and y < 0:
                                options.append(check)
                            elif board.piece_faction(loc) > 0 and y > 0:
                                options.append(check)
        print(options)
        return options
