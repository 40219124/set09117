class Deque(object):

    def __init__(self):
        self.deque = []

    def add_rear(self, move):
        self.deque.insert(0, move)

    def remove_rear(self):
        return self.deque.pop(0)

    def add_front(self, move):
        self.deque.append(move)

    def remove_front(self):
        return self.deque.pop()

    def is_empty(self):
        return self.size() == 0

    def size(self):
        return len(self.deque)

    def clear(self):
        self.deque = []
