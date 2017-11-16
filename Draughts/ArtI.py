from Node import Node
from Move import Move
from GameLogic import GameLogic


class ArtI(object):

    def __init__(self):
        self.heck = True

    @staticmethod
    def rotate_faction(faction):
        return (faction + 1) % 2

    def get_turn(self, board):
        tree = Node()
        tree = self.make_tree(board, (-1, -1), (-1, -1), 0, 0)

    def make_tree(self, board, start, end, ac_fac, swaps):
        node = Node()
        node.active_faction = ac_fac
        node.move.equals(board.move(start, end))
        options = []
        # If the piece took something on this move check for more takes
        if node.move.did_take:
            options = GameLogic.take_options(board, end)
        # If the piece can take more things
        if len(options) > 0:
            # Take all the things
            for opt in options:
                # And save the memories
                node.branches.append(self.make_tree(board, end, opt, ac_fac, swaps))
        # If piece can't continue taking
        else:
            swaps += 1
            ac_fac = self.rotate_faction(ac_fac)
            friendly_pieces = board.get_faction_pieces(ac_fac)
            # If out of pieces, enemy wins
            if len(friendly_pieces) == 0:
                node.win = self.rotate_faction(ac_fac)
            else:
                forced = []
                options = []
                size = 0
                # Find possible takes for friendly pieces
                for loc in friendly_pieces:
                    options[loc] = GameLogic.take_options(board, loc)
                    if len(options) > size:
                        size = len(options)
                        forced.append(loc)
                # If no takes possible
                if size == 0:
                    # Find possible regular moves for friendly pieces
                    for loc in friendly_pieces:
                        options[loc] = GameLogic.move_options(board, loc)
                        # If new
                        if len(options) > size:
                            size = len(options)
                            forced.append(loc)
                # If at stalemate, enemy wins
                if size == 0:
                    node.win = self.rotate_faction(ac_fac)
                else:
                    # For each movable piece...
                    for begin in forced:
                        # ...check each possible move...
                        for finish in options[begin]:
                            # ...and save the nodes.
                            node.branches.append(self.make_tree(board, begin, finish, ac_fac, swaps))
        # Return the finished node
        return node
