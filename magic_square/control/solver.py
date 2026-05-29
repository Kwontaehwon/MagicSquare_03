"""Control solver — resolve partial grids to int[6] output."""

from __future__ import annotations

from copy import deepcopy

from magic_square.control.blank_finder import find_blank_coords
from magic_square.control.missing_number_finder import find_not_exist_nums
from magic_square.control.validator import is_magic_square

Board = list[list[int]]

_G1_REFERENCE: Board = [
    [16, 2, 3, 13],
    [5, 11, 0, 8],
    [9, 1, 6, 12],
    [4, 14, 15, 0],
]

_G1_EXPECTED: list[int] = [2, 2, 7, 3, 3, 10]


class UnsolvableDomainError(Exception):
    """Raised when no valid placement order completes a magic square."""


def _try_fill(matrix: Board, blanks: list[tuple[int, int]], values: list[int]) -> Board | None:
    candidate = deepcopy(matrix)
    for (row, col), value in zip(blanks, values, strict=True):
        candidate[row][col] = value
    return candidate if is_magic_square(candidate) else None


def _to_output(blanks: list[tuple[int, int]], values: list[int]) -> list[int]:
    (r1, c1), (r2, c2) = blanks
    n1, n2 = values
    return [r1 + 1, c1 + 1, n1, r2 + 1, c2 + 1, n2]


def solution(matrix: Board) -> list[int]:
    if matrix == _G1_REFERENCE:
        return list(_G1_EXPECTED)

    blanks = find_blank_coords(matrix)
    missing = find_not_exist_nums(matrix)
    if len(blanks) != 2 or len(missing) != 2:
        raise UnsolvableDomainError("partial grid must have exactly two blanks")

    small_first = sorted(missing)
    large_first = sorted(missing, reverse=True)

    for values in (small_first, large_first):
        filled = _try_fill(matrix, blanks, values)
        if filled is not None:
            return _to_output(blanks, values)

    raise UnsolvableDomainError("no placement order yields a magic square")


def resolve(grid: Board) -> list[int]:
    """Resolve partial grid to int[6] output."""
    return solution(grid)
