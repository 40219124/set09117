from Node import Node
from GameLogic import GameLogic


class ArtI(object):

    def __init__(self):
        self.heck = True

    @staticmethod
    def get_turn(board, forced, ac_fac):
        tree = Node()
        tree.root = True
        for loc in forced:
            # Find options for the forced pieces
            opt = GameLogic.take_options(board, loc)
            if len(opt) == 0:
                opt.extend(GameLogic.move_options(board, loc))
            # Create the tree from options
            for finish in opt:
                tree.branches.append(ArtI.make_tree(board, loc, finish, ac_fac, 1, 7))
        # Get the best root to base from the tree
        value, turns, moves = ArtI.best_future(tree, ac_fac)
        moves.reverse()
        # Return only the immediate turn's moves
        # If there was more than 1 turn - it's more complicated
        if turns > 1:
            # Value to check against
            last_end = moves[0].end
            # List of output moves
            out_moves = [moves[0]]
            # For each move in moves (after the first)
            for move in moves[1:]:
                # If the end of a move matches with the start of the next
                if last_end == move.start:
                    # Add move to output and change the value to check against
                    out_moves.append(move)
                    last_end = move.end
                # Else the turn is over
                else:
                    # Break out of the for loop
                    break
            # Return the moves from the turn
            return out_moves
        # If there was only one turn
        else:
            # Return the move list
            return moves

    @staticmethod
    def make_tree(board, start, end, ac_fac, swaps, max_swaps):
        node = Node()
        node.active_faction = ac_fac
        board.select_piece(start)
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
                    options = {}
                    # Find possible takes for friendly pieces
                    for loc in friendly_pieces:
                        opt = GameLogic.take_options(board, loc)
                        if len(opt) > 0:
                            options[loc] = opt
                            forced.append(loc)
                    # If no takes possible
                    if len(forced) == 0:
                        # Find possible regular moves for friendly pieces
                        for loc in friendly_pieces:
                            opt = GameLogic.move_options(board, loc)
                            # If new
                            if len(opt) > 0:
                                options[loc] = opt
                                forced.append(loc)
                    # If at stalemate, enemy wins
                    if len(forced) == 0:
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
        # If not the root node
        if not node.root:
            # Declare whether this will add or detract from the score
            ally = 1
            if ac_fac != node.active_faction:
                ally *= -1
            # Sum values of the turn
            if node.move.crowned:
                value += (5 * ally)
            if node.move.did_take:
                if node.move.took_piece.crown:
                    value += (9 * ally)
                else:
                    value += (5 * ally)
            if node.lost:
                value += ((-50000) * ally)
        # If this node has branches
        if len(node.branches) > 0:
            # Initialise return variables
            best_sum = -1000000
            best_turns = 1
            best_moves = []
            # Check each branch
            for leaf in node.branches:
                # Get values from this recursive function
                temp_sum, temp_turns, temp_moves = ArtI.best_future(leaf, ac_fac)
                # If the average value of the returned branch is better than the best average
                if best_turns < temp_turns and temp_sum < 10000:
                    # Store new bests for later
                    best_turns = temp_turns
                    best_sum = temp_sum
                    best_moves.clear()
                    best_moves.extend(temp_moves)
                else:
                    t_avg = temp_sum / temp_turns
                    b_avg = best_sum / best_turns
                    if t_avg > b_avg:
                        # Store new bests for later
                        best_turns = temp_turns
                        best_sum = temp_sum
                        best_moves.clear()
                        best_moves.extend(temp_moves)
            # If this node is the last one in a turn, add one to the turn count
            if node.active_faction != node.branches[0].active_faction:
                best_turns += 1
            # If not the root node
            if not node.root:
                best_moves.append(node.move)
                # Return the values of branches + this node's values
                return best_sum + value, best_turns, best_moves
            # If the root node
            else:
                # Return the values of branches
                return best_sum, best_turns, best_moves
        # If there are no branches
        else:
            # Return the value of this node
            return value, 1, [node.move]
