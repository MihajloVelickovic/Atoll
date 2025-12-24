from collections import deque

from src.models.board import Board
from src.models.edge_type import EdgeType
from src.models.piece_color import PieceColor


class Game:
    def __init__(self, board_size=7):
        self.board = Board(board_size)
        self.current_player = PieceColor.WHITE

    @staticmethod
    def are_edges_adjacent(edge1, edge2):
        """Check if two edges are adjacent"""
        if edge1 is None or edge2 is None:
            return False

        e1_val = edge1.value
        e2_val = edge2.value

        diff = abs(e1_val - e2_val)
        return diff == 1 or diff == 5

    def get_edge_fields(self, edge, color):
        """Get all fields on a specific edge with the given color"""
        return [field for field in self.board.fields.values()
                if field.is_border and field.edge == edge and field.piece == color]

    def check_connection_bfs(self, color, start_edge, target_edge):
        """BFS to check if start_edge connects to target_edge"""
        # Start from all fields on start_edge with the given color
        queue = deque()
        visited = set()

        for field in self.get_edge_fields(start_edge, color):
            queue.append(field)
            visited.add((field.q, field.r))

        while queue:
            current = queue.popleft()

            # Check if we reached target edge
            if current.is_border and current.edge == target_edge:
                return True

            # Check all neighbors
            for neighbor in self.board.get_neighbors(current.q, current.r):
                if (neighbor.q, neighbor.r) not in visited and neighbor.piece == color:
                    visited.add((neighbor.q, neighbor.r))
                    queue.append(neighbor)

        return False

    def check_win(self, color):
        """Check if player has won by connecting non-adjacent edges"""
        edges = list(EdgeType)

        for i, edge1 in enumerate(edges):
            for edge2 in edges[i + 1:]:
                if not self.are_edges_adjacent(edge1, edge2):
                    if self.check_connection_bfs(color, edge1, edge2):
                        return True, edge1, edge2

        return False, None, None

    def make_move(self, q, r):
        """Make a move at the given coordinate"""
        if self.board.place_piece(q, r, self.current_player):
            won, edge1, edge2 = self.check_win(self.current_player)
            if won:
                return True, edge1, edge2

            # Switch player
            self.current_player = (PieceColor.WHITE if self.current_player == PieceColor.BLACK
                                   else PieceColor.BLACK)
            return False, None, None

        return None, None, None

    def display_board_info(self):
        """Display board information for debugging"""
        print(f"Total fields: {len(self.board.fields)}")

        main_fields = [f for f in self.board.fields.values() if not f.is_border]
        border_fields = [f for f in self.board.fields.values() if f.is_border]

        print(f"Main fields: {len(main_fields)}")
        print(f"Border fields: {len(border_fields)}")

        print("\nBorder fields by edge:")
        for edge in EdgeType:
            edge_fields = [f for f in border_fields if f.edge == edge]
            print(f"  {edge.name}: {len(edge_fields)} fields")

        print("\nSample neighbor counts:")
        for i, ((q, r), field) in enumerate(self.board.fields.items()):
            if i >= 5:
                break
            neighbors = self.board.get_neighbors(q, r)
            readable = self.board.to_readable_coord(q, r)
            print(f"  {readable} (q={q}, r={r}): {len(neighbors)} neighbors")