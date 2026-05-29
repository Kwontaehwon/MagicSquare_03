"""Boundary input validation — RED stub (not implemented)."""

from __future__ import annotations

from typing import Any

from magic_square.boundary.models import ValidationFailure

_GRID_SIZE = 4
_E002_CODE = "E002"
_E002_MESSAGE = "Exactly two blank cells (0) are required."
_E004_CODE = "E004"
_E004_MESSAGE = "Each cell must be 0 or an integer from 1 to 16."


def _blank_count(grid: list[list[int]]) -> int:
    return sum(1 for row in grid for cell in row if cell == 0)


def _value_in_range(cell: int) -> bool:
    return cell == 0 or 1 <= cell <= 16


def validate_grid(grid: Any) -> ValidationFailure:
    """Validate grid structure per Input Contract §6.1.1.

    RED stub: always returns placeholder failure until GREEN implementation.
    """
    if grid is None:
        return ValidationFailure(
            code="INVALID_SIZE",
            message="Grid must be 4x4.",
        )
    if len(grid) != _GRID_SIZE or any(len(row) != _GRID_SIZE for row in grid):
        return ValidationFailure(
            code="INVALID_SIZE",
            message="Grid must be 4x4.",
        )
    if _blank_count(grid) != 2:
        return ValidationFailure(
            code=_E002_CODE,
            message=_E002_MESSAGE,
        )
    if any(not _value_in_range(cell) for row in grid for cell in row):
        return ValidationFailure(
            code=_E004_CODE,
            message=_E004_MESSAGE,
        )
    return ValidationFailure(
        code="NOT_IMPLEMENTED",
        message="validate_grid is not implemented",
    )
