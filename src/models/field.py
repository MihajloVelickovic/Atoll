from src.models.piece_color import PieceColor

class Field:
    def __init__(self, q, r, is_border=False, edge=None):
        self.q = q  # axial coordinate q
        self.r = r  # axial coordinate r
        self.is_border = is_border
        self.edge = edge  # which edge this border position belongs to
        self.piece = PieceColor.EMPTY

    def __repr__(self):
        return f"Field(q={self.q}, r={self.r}, border={self.is_border}, piece={self.piece.name})"

    def __hash__(self):
        return hash((self.q, self.r))

    def __eq__(self, other):
        return self.q == other.q and self.r == other.r