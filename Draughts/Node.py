from Move import Move


class Node(object):

    def __init__(self):
        self.move = Move()
        self.branches = []
        self.active_faction = -1
        self.lost = False
        self.root = False

    def get_move(self):
        return self.move

    def get_branches(self):
        return self.branches

    def get_active_faction(self):
        return self.active_faction
