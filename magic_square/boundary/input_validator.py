"""Boundary input validation — Input Contract §6.1.1."""

from __future__ import annotations

from typing import Any

from magic_square.boundary.error_messages import (
    E002_CODE,
    E002_MESSAGE,
    E004_CODE,
    E004_MESSAGE,
    E005_CODE,
    E005_MESSAGE,
    INVALID_SIZE_CODE,
    INVALID_SIZE_MESSAGE,
)
from magic_square.boundary.models import ValidationFailure
from magic_square.entity.constants import GRID_SIZE, MAX_CELL_VALUE


def _blank_count(grid: list[list[int]]) -> int:
    """Count blank cells (0); same semantics as control.find_blank_coords."""
    return sum(1 for row in grid for cell in row if cell == 0)


def _value_in_range(cell: int) -> bool:
    return cell == 0 or 1 <= cell <= MAX_CELL_VALUE


def _has_nonzero_duplicate(grid: list[list[int]]) -> bool:
    seen: set[int] = set()
    for row in grid:
        for cell in row:
            if cell == 0:
                continue
            if cell in seen:
                return True
            seen.add(cell)
    return False


def _validate_size(grid: Any) -> ValidationFailure | None:
    if grid is None:
        return ValidationFailure(
            code=INVALID_SIZE_CODE,
            message=INVALID_SIZE_MESSAGE,
        )
    if len(grid) != GRID_SIZE or any(len(row) != GRID_SIZE for row in grid):
        return ValidationFailure(
            code=INVALID_SIZE_CODE,
            message=INVALID_SIZE_MESSAGE,
        )
    return None


def _validate_blank_count(grid: list[list[int]]) -> ValidationFailure | None:
    if _blank_count(grid) != 2:
        return ValidationFailure(
            code=E002_CODE,
            message=E002_MESSAGE,
        )
    return None


def _validate_cell_range(grid: list[list[int]]) -> ValidationFailure | None:
    if any(not _value_in_range(cell) for row in grid for cell in row):
        return ValidationFailure(
            code=E004_CODE,
            message=E004_MESSAGE,
        )
    return None


def _validate_nonzero_duplicates(grid: list[list[int]]) -> ValidationFailure | None:
    if _has_nonzero_duplicate(grid):
        return ValidationFailure(
            code=E005_CODE,
            message=E005_MESSAGE,
        )
    return None


def validate_grid(grid: Any) -> ValidationFailure | None:
    """Validate grid structure per Input Contract §6.1.1.

    Returns None when all checks pass; otherwise a ValidationFailure.
    """
    failure = _validate_size(grid)
    if failure is not None:
        return failure

    failure = _validate_blank_count(grid)
    if failure is not None:
        return failure

    failure = _validate_cell_range(grid)
    if failure is not None:
        return failure

    failure = _validate_nonzero_duplicates(grid)
    if failure is not None:
        return failure

    return None
