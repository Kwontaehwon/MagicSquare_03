"""Track B — D-VAL-01~06: MagicSquareValidator / is_magic_square (RED skeleton).

Domain Mock 금지. Magic constant M via entity/constants — no literal 34 in asserts.
"""

from __future__ import annotations

import pytest

from magic_square.control.validator import is_magic_square

# G0 — complete magic square (Report/11 §2)
# Invalid variants: row/col/diag break, duplicate non-zero, zero inserted into G0


class TestDVal01CompleteGrid:
    """D-VAL-01 — G0 complete grid → True (M derived, not hardcoded)."""

    def test_d_val_01_is_magic_square_g0_complete_true(self) -> None:
        """D-VAL-01 / I1~I5 — G0 → is_magic_square returns True."""
        # Given
        # matrix = GRID_G0

        # When
        # result = is_magic_square(matrix)

        pytest.fail("RED: D-VAL-01 — G0 complete grid → is_magic_square True")


class TestDVal02RowSumMismatch:
    """D-VAL-02 — row sum ≠ M → False."""

    def test_d_val_02_is_magic_square_row_sum_mismatch_false(self) -> None:
        """D-VAL-02 / I1 — G0 variant with broken row sum → False."""
        # Given
        # matrix = G0 variant (one row sum ≠ M)

        # When
        # result = is_magic_square(matrix)

        pytest.fail("RED: D-VAL-02 — row sum mismatch → is_magic_square False")


class TestDVal03ColSumMismatch:
    """D-VAL-03 — column sum ≠ M → False."""

    def test_d_val_03_is_magic_square_col_sum_mismatch_false(self) -> None:
        """D-VAL-03 / I2 — G0 variant with broken column sum → False."""
        # Given
        # matrix = G0 variant (one column sum ≠ M)

        # When
        # result = is_magic_square(matrix)

        pytest.fail("RED: D-VAL-03 — column sum mismatch → is_magic_square False")


class TestDVal04DiagonalMismatch:
    """D-VAL-04 — diagonal sum ≠ M → False."""

    def test_d_val_04_is_magic_square_diagonal_mismatch_false(self) -> None:
        """D-VAL-04 / I3 — G0 variant with broken diagonal → False."""
        # Given
        # matrix = G0 variant (main or anti diagonal ≠ M)

        # When
        # result = is_magic_square(matrix)

        pytest.fail("RED: D-VAL-04 — diagonal mismatch → is_magic_square False")


class TestDVal05DuplicateNonzero:
    """D-VAL-05 — non-zero duplicate → False."""

    def test_d_val_05_is_magic_square_duplicate_nonzero_false(self) -> None:
        """D-VAL-05 / I4 — grid with duplicate non-zero → False."""
        # Given
        # matrix = 4×4 with duplicate non-zero values

        # When
        # result = is_magic_square(matrix)

        pytest.fail("RED: D-VAL-05 — non-zero duplicate → is_magic_square False")


class TestDVal06ContainsZero:
    """D-VAL-06 — complete grid must not contain 0 → False."""

    def test_d_val_06_is_magic_square_contains_zero_false(self) -> None:
        """D-VAL-06 / I4 — G0 with 0 inserted → False."""
        # Given
        # matrix = G0 with one cell replaced by 0

        # When
        # result = is_magic_square(matrix)

        pytest.fail("RED: D-VAL-06 — grid contains 0 → is_magic_square False")
