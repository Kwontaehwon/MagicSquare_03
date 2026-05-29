"""Track A — U-IN-04~08: blank count, value range, duplicate (RED skeleton).

U-IN-01~03 covered by tests/boundary/test_ac_fr_01_01_* (do not duplicate).
"""

from __future__ import annotations

import pytest

from magic_square.boundary.input_validator import validate_grid
from tests.conftest import (
    DUPLICATE_NONZERO_GRID,
    GRID_G0,
    NEGATIVE_VALUE_GRID,
    THREE_BLANK_GRID,
    VALUE_17_GRID,
)

# Report/11 — Failure envelope (GREEN: PRD v0.2 diff 0)
E002_CODE = "E002"
E002_MESSAGE = "Exactly two blank cells (0) are required."
E004_CODE = "E004"
E005_CODE = "E005"


class TestUIn04BlankCountZero:
    """U-IN-04 — G0 complete grid has zero blanks → E002."""

    def test_u_in_04_zero_blanks_returns_e002(self) -> None:
        """U-IN-04 / AC-FR-01-02 — zero blank cells → code E002."""
        # Given
        matrix = GRID_G0

        # When
        result = validate_grid(matrix)

        # Then
        assert result.code == E002_CODE


class TestUIn05BlankCountThree:
    """U-IN-05 — matrix with three blank cells → E002."""

    def test_u_in_05_three_blanks_returns_e002(self) -> None:
        """U-IN-05 / AC-FR-01-02 — three cells with 0 → code E002."""
        # Given
        matrix = THREE_BLANK_GRID

        # When
        result = validate_grid(matrix)

        # Then
        assert result.code == E002_CODE


class TestUIn06ValueRangeNegative:
    """U-IN-06 — cell value -1 → E004."""

    def test_u_in_06_negative_value_returns_e004(self) -> None:
        """U-IN-06 / AC-FR-01-03 — cell -1 → code E004."""
        # Given
        matrix = NEGATIVE_VALUE_GRID

        # When
        result = validate_grid(matrix)

        # Then
        assert result.code == E004_CODE


class TestUIn07ValueRangeAboveMax:
    """U-IN-07 — cell value 17 → E004."""

    def test_u_in_07_value_17_returns_e004(self) -> None:
        """U-IN-07 / AC-FR-01-03 — cell 17 → code E004."""
        # Given
        matrix = VALUE_17_GRID

        # When
        result = validate_grid(matrix)

        # Then
        assert result.code == E004_CODE


class TestUIn08NonzeroDuplicate:
    """U-IN-08 — non-zero duplicate → E005."""

    def test_u_in_08_nonzero_duplicate_returns_e005(self) -> None:
        """U-IN-08 / AC-FR-01-04 — duplicate non-zero → code E005."""
        # Given
        matrix = DUPLICATE_NONZERO_GRID

        # When
        result = validate_grid(matrix)

        # Then
        assert result.code == E005_CODE
