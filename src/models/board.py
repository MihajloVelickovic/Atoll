from src.models.edge_type import EdgeType
from src.models.field import Field
from src.models.piece_color import PieceColor


class Board:
    def __init__(self, n=7):
        self.n = n
        self.fields = {}  # (q, r) -> Field
        self.generate_board()

    def generate_board(self):
        """Generate hexagonal board with border using axial coordinates"""
        # Main board fields
        for q in range(-self.n + 1, self.n):
            r1 = max(-self.n + 1, -q - self.n + 1)
            r2 = min(self.n - 1, -q + self.n - 1)
            for r in range(r1, r2 + 1):
                self.fields[(q, r)] = Field(q, r, is_border=False)

        # Border fields - each edge has exactly (2n-1) - 2 = 2n-3 pieces
        # Wait, that's wrong too. Let me recalculate.

        # For n=7:
        # The border forms a hexagon where max(|q|, |r|, |s|) = n
        # Each straight edge of the hexagon has (n-1) = 6 pieces
        # 6 edges * 6 pieces = 36 total

        # Top edge (T): r = -n, q ranges but NOT the corners
        # q goes from -(n-1) to +(n-1), which is 2n-1 positions, but we exclude 2 corners
        # Actually: q from -(n-1) to +(n-1) gives us 2n-1 = 13 positions
        # But we want only 6 per edge...

        # AH! I see the issue. For a hexagon, each SIDE has (n-1) pieces
        # Top edge: r=-n, q from -(n-1) to (n-1), but that's too many

        # Let me think differently: looking at the image, each side has exactly 6 pieces
        # The hexagon has 6 corners (vertices) that are NOT included in border

        # Top edge (T): r = -n, q from -(n-1) to -1  [that's n-1 = 6 pieces]
        for i in range(self.n - 1):
            q = -(self.n - 1) + i
            r = -self.n
            self.fields[(q, r)] = Field(q, r, is_border=True, edge=EdgeType.T)

        # Top-right edge (TR): moves from top corner to right corner
        # q increases from 0 to (n-1), r increases from -(n-1) to -1
        for i in range(self.n - 1):
            q = i
            r = -(self.n - 1) + i
            self.fields[(q, r)] = Field(q, r, is_border=True, edge=EdgeType.TR)

        # Right edge going down: q = n, r from 0 to (n-2)
        for i in range(self.n - 1):
            q = self.n
            r = i
            self.fields[(q, r)] = Field(q, r, is_border=True, edge=EdgeType.BR)

        # Bottom edge (B): r = n, q from 1 to (n-1)
        for i in range(self.n - 1):
            q = 1 + i
            r = self.n
            self.fields[(q, r)] = Field(q, r, is_border=True, edge=EdgeType.B)

        # Bottom-left edge (BL): q decreases from 0 to -(n-2), r decreases from n to 2
        for i in range(self.n - 1):
            q = -i
            r = self.n - i
            self.fields[(q, r)] = Field(q, r, is_border=True, edge=EdgeType.BL)

        # Left edge going up: q = -n, r from 1 to (n-1)
        for i in range(self.n - 1):
            q = -self.n
            r = 1 + i
            self.fields[(q, r)] = Field(q, r, is_border=True, edge=EdgeType.TL)

    def _determine_edge(self, q, r):
        """Determine which edge a border position belongs to"""
        s = -q - r

        # Each edge is defined by which coordinate is at the maximum
        # Top edge: r = -n (and s varies)
        # Top-right edge: q = n (and r varies)
        # Bottom-right edge: s = n (which means -q - r = n, so q + r = -n)
        # Bottom edge: r = n
        # Bottom-left edge: q = -n
        # Top-left edge: s = -n (which means -q - r = -n, so q + r = n)

        if r == -self.n and q >= -self.n and q < self.n:
            return EdgeType.T
        elif q == self.n and r > -self.n and r <= self.n:
            return EdgeType.TR
        elif s == self.n and q > -self.n and q <= self.n:
            return EdgeType.BR
        elif r == self.n and q > -self.n and q <= self.n:
            return EdgeType.B
        elif q == -self.n and r >= -self.n and r < self.n:
            return EdgeType.BL
        elif s == -self.n and q >= -self.n and q < self.n:
            return EdgeType.TL

        return None

    def get_neighbors(self, q, r):
        """Get all 6 neighbors of a hexagonal cell (or fewer if at edge)"""
        # Hexagonal neighbors in axial coordinates
        directions = [
            (1, 0),  # right
            (1, -1),  # top-right
            (0, -1),  # top-left
            (-1, 0),  # left
            (-1, 1),  # bottom-left
            (0, 1)  # bottom-right
        ]

        neighbors = []
        for dq, dr in directions:
            nq, nr = q + dq, r + dr
            if (nq, nr) in self.fields:
                neighbors.append(self.fields[(nq, nr)])

        return neighbors

    def place_piece(self, q, r, color):
        """Place a piece at the given coordinate"""
        if (q, r) in self.fields:
            self.fields[(q, r)].piece = color
            return True
        return False

    def get_field(self, q, r):
        """Get field by coordinate"""
        return self.fields.get((q, r))

    def to_readable_coord(self, q, r):
        """Convert axial coordinates to readable format (A1, B2, etc.)"""
        # For main board
        if not self.fields[(q, r)].is_border:
            # Calculate row and column
            row = q + self.n - 1
            col = r + min(0, q) + 1
            return f"{chr(65 + row)}{col}"
        else:
            # For border, use edge notation
            edge = self.fields[(q, r)].edge
            # Find position along edge
            if edge == EdgeType.T:
                return f"T{q + self.n + 1}"
            elif edge == EdgeType.TR:
                return f"TR{r + self.n + 1}"
            elif edge == EdgeType.BR:
                return f"BR{-q + self.n + 1}"
            elif edge == EdgeType.B:
                return f"B{-q + self.n + 1}"
            elif edge == EdgeType.BL:
                return f"BL{-r + self.n + 1}"
            elif edge == EdgeType.TL:
                return f"TL{q + self.n + 1}"

        return f"({q},{r})"