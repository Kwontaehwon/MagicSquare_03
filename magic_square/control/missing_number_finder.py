"""Control missing number finder — sorted absent values from 1..n²."""

from __future__ import annotations

from magic_square.entity.constants import GRID_SIZE

Board = list[list[int]]


def find_not_exist_nums(matrix: Board) -> list[int]:
    present = {cell for row in matrix for cell in row if cell != 0}
    universe = set(range(1, GRID_SIZE * GRID_SIZE + 1))
    return sorted(universe - present)
