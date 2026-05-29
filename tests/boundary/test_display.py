"""Boundary display — representation-only helpers."""

from __future__ import annotations

from magic_square.boundary.display import (
    format_board,
    format_col_sums,
    format_row_sums,
    format_solution,
    magic_constant_label,
)
from magic_square.entity.constants import MAGIC_CONSTANT
from tests.conftest import GRID_G1


class TestFormatBoard:
    """format_board renders blanks and numbers for display."""

    def test_format_board_shows_blank_and_numbers(self) -> None:
        text = format_board(GRID_G1)
        assert "·" in text
        assert "16" in text
        lines = text.splitlines()
        assert len(lines) == 4


class TestFormatSums:
    """Row/column sum helpers are presentation-only."""

    def test_format_row_and_col_sums_length(self) -> None:
        assert len(format_row_sums(GRID_G1)) == 4
        assert len(format_col_sums(GRID_G1)) == 4

    def test_magic_constant_label_matches_constant(self) -> None:
        assert magic_constant_label() == str(MAGIC_CONSTANT)


class TestFormatSolution:
    """format_solution renders int[6] as human-readable lines."""

    def test_format_solution_includes_coordinates(self) -> None:
        result = [2, 2, 7, 3, 3, 10]
        text = format_solution(result)
        assert "(2, 2)" in text
        assert "7" in text
        assert "(3, 3)" in text
        assert "10" in text
