"""Boundary orchestrator — validate input and delegate to Control."""

from __future__ import annotations

from typing import Any

from magic_square.boundary.input_validator import validate_grid
from magic_square.boundary.models import ValidationFailure
from magic_square.control.solver import UnsolvableDomainError, resolve


def solve(grid: Any) -> ValidationFailure | list[int]:
    """Validate input and delegate to Control resolve on success."""
    failure = validate_grid(grid)
    if failure is not None:
        return failure
    try:
        return resolve(grid)
    except UnsolvableDomainError as exc:
        return ValidationFailure(code="UNSOLVABLE", message=str(exc))
