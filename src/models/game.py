from src.models.board import Board

class Game:
    def __init__(self, n: Board, p1 = 'X', p2 = 'O', p1cpu = False, p2cpu = False, p1first = True):
        self.board = Board(n)
        self.p1label = p1
        self.p2label = p2
        self.p1cpu = p1cpu
        self.p2cpu = p2cpu
        self.p1first = p1first