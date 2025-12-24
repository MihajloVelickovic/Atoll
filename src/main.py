from src.models.edge_type import EdgeType
from src.models.game import Game
from src.models.piece_color import PieceColor

if __name__ == "__main__":
    game = Game(board_size=7)


    # Place some test pieces
    print("\n--- PLACING TEST PIECES ---")
    game.board.place_piece(0, 0, PieceColor.WHITE)  # Center
    game.board.place_piece(1, 0, PieceColor.BLACK)
    game.board.place_piece(-1, 0, PieceColor.WHITE)
    game.board.place_piece(0, 1, PieceColor.BLACK)
    game.board.place_piece(0, -1, PieceColor.WHITE)

    # Place some border pieces
    game.board.place_piece(-6, -6, PieceColor.BLACK)  # Top edge
    game.board.place_piece(0, -6, PieceColor.WHITE)  # Top edge
    game.board.place_piece(6, 0, PieceColor.BLACK)  # Right edge
    game.board.place_piece(-6, 0, PieceColor.WHITE)  # Left edge
    game.board.place_piece(0, 6, PieceColor.BLACK)  # Bottom edge


    # Display board info
    print("\n--- BOARD INFORMATION ---")
    game.display_board_info()

    # Test placing pieces and checking neighbors
    print("\n--- NEIGHBOR ANALYSIS ---")
    center_neighbors = game.board.get_neighbors(0, 0)
    print(f"Center field (0, 0) has {len(center_neighbors)} neighbors")
    for neighbor in center_neighbors:
        print(f"  - ({neighbor.q}, {neighbor.r}): {neighbor.piece.name}")

    # Test edge adjacency
    print("\n--- EDGE ADJACENCY TESTS ---")
    print(f"T and TR adjacent? {Game.are_edges_adjacent(EdgeType.T, EdgeType.TR)}")  # True
    print(f"T and BR adjacent? {Game.are_edges_adjacent(EdgeType.T, EdgeType.BR)}")  # False
    print(f"TL and T adjacent? {Game.are_edges_adjacent(EdgeType.TL, EdgeType.T)}")  # True
    print(f"T and B adjacent? {Game.are_edges_adjacent(EdgeType.T, EdgeType.B)}")  # False