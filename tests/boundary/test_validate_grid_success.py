"""Boundary — validate_grid success path after REFACTOR."""

from __future__ import annotations

from magic_square.boundary.input_validator import validate_grid
from tests.conftest import GRID_G1


class TestValidateGridSuccess:
    """validate_grid returns None for a valid partial grid."""

    def test_validate_grid_g1_returns_none(self) -> None:
        """Valid G1 partial grid passes validation without failure DTO."""
        assert validate_grid(GRID_G1) is None
