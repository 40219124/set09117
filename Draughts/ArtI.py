from Node import Node
from Move import Move
from GameLogic import GameLogic


class ArtI(object):

    def __init__(self):
        self.heck = True

    def get_turn(self, board):
        tree = Node()
        tree = self.make_tree(board, (-1, -1), (-1, -1), -1, -1, -1)

    @staticmethod
    def make_tree(board, start, end, ac_fac, swaps, max_swaps):
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
                node.branches.append(ArtI.make_tree(board, end, opt, ac_fac, swaps, max_swaps))
        # If piece can't continue taking
        else:
            swaps += 1
            # If not too many turns deep
            if swaps < max_swaps:
                node.turn_start = True
                ac_fac = ArtI.rotate_faction(ac_fac)
                friendly_pieces = board.get_faction_pieces(ac_fac)
                # If out of pieces, enemy wins
                if len(friendly_pieces) == 0:
                    node.lost = True
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
                        node.lost = True
                    else:
                        # For each movable piece...
                        for begin in forced:
                            # ...check each possible move...
                            for finish in options[begin]:
                                # ...and save the nodes.
                                node.branches.append(ArtI.make_tree(board, begin, finish, ac_fac, swaps, max_swaps))
        # Undo the move made by this node
        ArtI.undo_node_move(board, node.move)
        # Return the finished node
        return node

    @staticmethod
    def rotate_faction(faction):
        return (faction + 1) % 2

    @staticmethod
    def undo_node_move(board, move):
        board.set_piece(move.start, board.get_piece(move.end))
        board.delete_piece(move.end)
        if move.crowned:
            board.abdicate(move.start)
        if move.did_take:
            board.set_piece(move.took_from, move.took_piece)

    @staticmethod
    def best_future(node, ac_fac):
        value = 0
        if not node.root:
            ally = 1
            if ac_fac != node.active_faction:
                ally *= -1
            if node.move.crowned:
                value += (5 * ally)
            if node.move.did_take:
                if node.move.took_piece.crown:
                    value += (10 * ally)
                else:
                    value += (2 * ally)
            if node.lost:
                value += (5000 * ally)
        if len(node.branches) > 0:
            is_turn_end = False
            best_sum = -1000000
            best_turns = 1
            best_moves = []
            for leaf in node.branches:
                turn_end, temp_sum, temp_turns, temp_moves = ArtI.best_future(leaf, ac_fac)
                if (temp_sum / temp_turns) > (best_sum / best_turns):
                    best_turns = temp_turns
                    best_sum = temp_sum
                    best_moves.clear()
                    best_moves.extend(temp_moves)
                    is_turn_end = True
            if is_turn_end:
                best_turns += 1
            return node.turn_start, best_sum + value, best_turns, best_moves
        else:
            return node.turn_start, value, 1, [node.move]
