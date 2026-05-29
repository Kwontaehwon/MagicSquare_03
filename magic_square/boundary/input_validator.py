"""Boundary input validation — RED stub (not implemented)."""

from __future__ import annotations

from typing import Any

from magic_square.boundary.models import ValidationFailure


def validate_grid(grid: Any) -> ValidationFailure:
    """Validate grid structure per Input Contract §6.1.1.

    RED stub: always returns placeholder failure until GREEN implementation.
    """
    if grid is None:
        return ValidationFailure(
            code="INVALID_SIZE",
            message="Grid must be 4x4.",
        )
    return ValidationFailure(
        code="NOT_IMPLEMENTED",
        message="validate_grid is not implemented",
    )
