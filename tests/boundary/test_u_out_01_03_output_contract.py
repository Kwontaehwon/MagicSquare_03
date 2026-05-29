"""Track A — U-OUT-01~03: success output contract."""

from __future__ import annotations

from magic_square.boundary.cli import solve
from tests.conftest import GRID_G1


class TestUOut01ResultLength:
    """U-OUT-01 — successful solve returns int[6]."""

    def test_u_out_01_success_result_length_is_six(self) -> None:
        """U-OUT-01 / AC-FR-05-03 — len(result) == 6 for valid G1 input."""
        # Given
        matrix = GRID_G1

        # When
        result = solve(matrix)

        # Then
        assert len(result) == 6


class TestUOut02CoordinatesOneIndexed:
    """U-OUT-02 — r,c are 1-index in [1,4]."""

    def test_u_out_02_success_coordinates_are_1_index_in_range(self) -> None:
        """U-OUT-02 / I11 — 1-index coords in [1,4] for G1."""
        # Given
        matrix = GRID_G1

        # When
        result = solve(matrix)

        # Then
        assert all(1 <= result[i] <= 4 for i in (0, 1, 3, 4))


class TestUOut03FillValuesMatchMissing:
    """U-OUT-03 — n1,n2 equal sorted missing numbers from partial grid."""

    def test_u_out_03_success_fill_values_match_missing_numbers(self) -> None:
        """U-OUT-03 / I7+I11 — n1,n2 are missing values {7,10} for G1."""
        # Given
        matrix = GRID_G1

        # When
        result = solve(matrix)

        # Then
        assert result[2] == 7
        assert result[5] == 10
