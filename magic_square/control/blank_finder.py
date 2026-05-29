"""Control blank finder — locate zero cells in row-major 0-index order."""

from __future__ import annotations

Board = list[list[int]]


def find_blank_coords(matrix: Board) -> list[tuple[int, int]]:
    coords: list[tuple[int, int]] = []
    for row_index, row in enumerate(matrix):
        for col_index, cell in enumerate(row):
            if cell == 0:
                coords.append((row_index, col_index))
    return coords
