"""Boundary orchestrator — RED stub (not implemented)."""

from __future__ import annotations

from typing import Any

from magic_square.boundary.input_validator import validate_grid
from magic_square.boundary.models import ValidationFailure
from magic_square.control.solver import resolve


def solve(grid: Any) -> ValidationFailure:
    """Validate input and delegate to Control resolve on success.

    RED stub: incorrectly calls resolve before validation (isolation test must fail).
    """
    resolve(grid)
    return validate_grid(grid)
