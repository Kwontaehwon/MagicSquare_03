"""Boundary display — board and result representation only."""

from __future__ import annotations

from magic_square.entity.constants import GRID_SIZE, MAGIC_CONSTANT

Board = list[list[int]]


def format_board(board: Board) -> str:
    """Return a human-readable multi-line board string."""
    lines = [" ".join(_cell_text(cell) for cell in row) for row in board]
    return "\n".join(lines)


def format_solution(result: list[int]) -> str:
    """Format int[6] solver output as readable text."""
    r1, c1, n1, r2, c2, n2 = result
    return (
        f"({r1}, {c1}) → {n1}\n"
        f"({r2}, {c2}) → {n2}"
    )


def format_row_sums(board: Board) -> list[int]:
    """Return each row sum (presentation helper, not validation)."""
    return [sum(row) for row in board]


def format_col_sums(board: Board) -> list[int]:
    """Return each column sum (presentation helper, not validation)."""
    return [
        sum(board[row][col] for row in range(GRID_SIZE))
        for col in range(GRID_SIZE)
    ]


def magic_constant_label() -> str:
    """Return magic constant for UI labels."""
    return str(MAGIC_CONSTANT)


def _cell_text(cell: int) -> str:
    return "·" if cell == 0 else f"{cell:2d}"
