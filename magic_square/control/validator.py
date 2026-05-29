"""Control validator — magic square predicate (generation-agnostic)."""

from __future__ import annotations

from magic_square.entity.constants import GRID_SIZE, MAGIC_CONSTANT

Board = list[list[int]]


def _shape_valid(board: Board) -> bool:
    if len(board) != GRID_SIZE:
        return False
    return all(len(row) == GRID_SIZE for row in board)


def _composition_valid(board: Board) -> bool:
    cells = [cell for row in board for cell in row]
    if len(cells) != GRID_SIZE * GRID_SIZE:
        return False
    if any(cell == 0 for cell in cells):
        return False
    if set(cells) != set(range(1, GRID_SIZE * GRID_SIZE + 1)):
        return False
    return True


def _rows_valid(board: Board) -> bool:
    return all(sum(row) == MAGIC_CONSTANT for row in board)


def _cols_valid(board: Board) -> bool:
    return all(
        sum(board[row][col] for row in range(GRID_SIZE)) == MAGIC_CONSTANT
        for col in range(GRID_SIZE)
    )


def _main_diagonal_valid(board: Board) -> bool:
    return sum(board[i][i] for i in range(GRID_SIZE)) == MAGIC_CONSTANT


def _anti_diagonal_valid(board: Board) -> bool:
    return (
        sum(board[i][GRID_SIZE - 1 - i] for i in range(GRID_SIZE)) == MAGIC_CONSTANT
    )


def is_magic_square(matrix: Board) -> bool:
    if not _shape_valid(matrix):
        return False
    return (
        _composition_valid(matrix)
        and _rows_valid(matrix)
        and _cols_valid(matrix)
        and _main_diagonal_valid(matrix)
        and _anti_diagonal_valid(matrix)
    )
