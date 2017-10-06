def string_add_int(string, tup):
    return str(int(string[0:1]) + tup[0]) + str(int(string[1]) + tup[1])


def valid_square(string):
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
            if 0 <= int(loc[0: 1]) + x < 8:
                for y in range(-1, 2, 2):
                    if 0 <= int(loc[1]) + y < 8:
                        check = string_add_int(loc, (x, y))
                        if board.piece_faction(check) < 0:
                            if board.piece_rank(loc) == 1:
                                options.append(check)
                            else:
                                if board.piece_faction(loc) == 0 and y < 0:
                                    options.append(check)
                                elif board.piece_faction(loc) > 0 and y > 0:
                                    options.append(check)
        return options

    @staticmethod
    def take_options(board, loc, taken):
        options = []
        min_y = -2
        max_y = 2
        if board.piece_rank(loc) == 0:
            if board.piece_faction(loc) == 0:
                max_y = min_y
            else:
                min_y = max_y
        for x in range(-2, 3, 4):
            if 0 <= int(loc[0:1]) + x < 8:
                for y in range(min_y, max_y + 1, 4):
                    if 0 <= int(loc[1]) + y < 8:
                        check = string_add_int(loc, (x, y))
                        if board.piece_faction(check) < 0:
                            over = string_add_int(loc, (x//2, y//2))
                            if 0 <= board.piece_faction(over) != board.piece_faction(loc) and \
                                    not taken.__contains__(over):
                                taken.append(over)
                                recursive_results = GameLogic.take_options(board, check, taken)
                                print("rr:" + str(recursive_results))
                                print("ch:" + check)
                                print("ov:" + over)
                                print("op:" + str(options))
                                # options.append(recursive_results)
                                print("op:" + str(options))
                                # options.append(check)
                                print("op:" + str(options))
                                if recursive_results.__len__() > 0:
                                    options = recursive_results
                                else:
                                    options.append(check)
        print("op:" + str(options))
        return options
