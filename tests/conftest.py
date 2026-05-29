"""Shared grid fixtures — RED skeleton placeholders (G0~G3).

GREEN phase: uncomment and wire into pytest fixtures.
"""

from __future__ import annotations

# G0 — complete magic square (Report/11 §2)
# GRID_G0: list[list[int]] = [
#     [16, 3, 2, 13],
#     [5, 10, 11, 8],
#     [9, 6, 7, 12],
#     [4, 15, 14, 1],
# ]

# G1 — Step A success; blanks at (2,2), (3,3); missing {7, 10}
# GRID_G1: list[list[int]] = [
#     [16, 2, 3, 13],
#     [5, 11, 0, 8],
#     [9, 1, 6, 12],
#     [4, 14, 15, 0],
# ]

# G2 — Step A fail → Step B success (SC-DOM-SOL-001 surrogate)
# GRID_G2: list[list[int]] = [
#     [16, 2, 3, 13],
#     [5, 11, 10, 8],
#     [9, 7, 0, 12],
#     [4, 14, 15, 0],
# ]

# G3 — both combinations fail (placeholder — verify at GREEN)
# GRID_G3: list[list[int]] = [
#     [8, 1, 0, 6],
#     [0, 5, 7, 2],
#     [3, 0, 4, 5],
#     [9, 11, 12, 13],
# ]
