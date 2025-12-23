from src.models.field import Field

class Board:
    def __init__(self, n):
        self.n = n if (9 > n > 2
                   and n % 2 is 1) else n % 9 + 1 # stranica hex
        self.min_win_moves = 7 # deluje da je const 7
        self.board = []


    def generate_board(self):
        addition = 0
        for i in range(0, 2 * self.n - 1):
            if i < self.n-1:
                for j in range(0, self.n + addition):
                    self.board.append(Field(i, j))
            else:
                addition -= 1
                for j in range(i-(self.n-1), 2 * self.n - 1):
                    self.board.append(Field(i, j))
