"""Track B — D-VAL-01~06: MagicSquareValidator / is_magic_square."""

from __future__ import annotations

from copy import deepcopy

from magic_square.control.validator import is_magic_square
from magic_square.entity.constants import MAGIC_CONSTANT
from tests.conftest import GRID_G0


def _g0_row_sum_mismatch() -> list[list[int]]:
    board = deepcopy(GRID_G0)
    board[0][0] = 1
    return board


def _g0_col_sum_mismatch() -> list[list[int]]:
    board = deepcopy(GRID_G0)
    board[0][0] = 15
    board[3][0] = 5
    return board


def _g0_diagonal_mismatch() -> list[list[int]]:
    board = deepcopy(GRID_G0)
    board[0][0] = 15
    board[3][3] = 2
    return board


def _duplicate_nonzero_board() -> list[list[int]]:
    return [
        [1, 1, 0, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0],
    ]


def _g0_with_zero() -> list[list[int]]:
    board = deepcopy(GRID_G0)
    board[0][0] = 0
    return board


class TestDVal01CompleteGrid:
    """D-VAL-01 — G0 complete grid → True (M derived, not hardcoded)."""

    def test_d_val_01_is_magic_square_g0_complete_true(self) -> None:
        """D-VAL-01 / I1~I5 — G0 → is_magic_square returns True."""
        # Given
        matrix = GRID_G0

        # When
        result = is_magic_square(matrix)

        # Then
        assert result is True
        assert sum(matrix[0]) == MAGIC_CONSTANT


class TestDVal02RowSumMismatch:
    """D-VAL-02 — row sum ≠ M → False."""

    def test_d_val_02_is_magic_square_row_sum_mismatch_false(self) -> None:
        """D-VAL-02 / I1 — G0 variant with broken row sum → False."""
        # Given
        matrix = _g0_row_sum_mismatch()

        # When
        result = is_magic_square(matrix)

        # Then
        assert result is False


class TestDVal03ColSumMismatch:
    """D-VAL-03 — column sum ≠ M → False."""

    def test_d_val_03_is_magic_square_col_sum_mismatch_false(self) -> None:
        """D-VAL-03 / I2 — G0 variant with broken column sum → False."""
        # Given
        matrix = _g0_col_sum_mismatch()

        # When
        result = is_magic_square(matrix)

        # Then
        assert result is False


class TestDVal04DiagonalMismatch:
    """D-VAL-04 — diagonal sum ≠ M → False."""

    def test_d_val_04_is_magic_square_diagonal_mismatch_false(self) -> None:
        """D-VAL-04 / I3 — G0 variant with broken diagonal → False."""
        # Given
        matrix = _g0_diagonal_mismatch()

        # When
        result = is_magic_square(matrix)

        # Then
        assert result is False


class TestDVal05DuplicateNonzero:
    """D-VAL-05 — non-zero duplicate → False."""

    def test_d_val_05_is_magic_square_duplicate_nonzero_false(self) -> None:
        """D-VAL-05 / I4 — grid with duplicate non-zero → False."""
        # Given
        matrix = _duplicate_nonzero_board()

        # When
        result = is_magic_square(matrix)

        # Then
        assert result is False


class TestDVal07MalformedShape:
    """Malformed grid shape → False without IndexError."""

    def test_d_val_07_three_by_four_false(self) -> None:
        """3×4 grid → False."""
        matrix = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
        ]
        assert is_magic_square(matrix) is False

    def test_d_val_07_four_by_three_false(self) -> None:
        """4×3 grid → False."""
        matrix = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
            [10, 11, 12],
        ]
        assert is_magic_square(matrix) is False

    def test_d_val_07_jagged_rows_false(self) -> None:
        """Jagged row lengths → False."""
        matrix = [
            [1, 2, 3, 4],
            [5, 6, 7],
            [8, 9, 10, 11],
            [12, 13, 14, 15],
        ]
        assert is_magic_square(matrix) is False


class TestDVal06ContainsZero:
    """D-VAL-06 — complete grid must not contain 0 → False."""

    def test_d_val_06_is_magic_square_contains_zero_false(self) -> None:
        """D-VAL-06 / I4 — G0 with 0 inserted → False."""
        # Given
        matrix = _g0_with_zero()

        # When
        result = is_magic_square(matrix)

        # Then
        assert result is False
