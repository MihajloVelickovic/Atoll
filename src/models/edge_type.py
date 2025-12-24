from enum import Enum

class EdgeType(Enum):
    T = 0   # Top
    TR = 1  # Top-right
    BR = 2  # Bottom-right
    B = 3   # Bottom
    BL = 4  # Bottom-left
    TL = 5  # Top-left