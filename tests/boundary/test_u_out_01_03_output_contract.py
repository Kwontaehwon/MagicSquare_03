"""Track A — U-OUT-01~03: success output contract (RED skeleton).

U-OUT: Control mock/spy allowed (resolve / execute stub) — comments only in RED.
"""

from __future__ import annotations

import pytest

from magic_square.boundary.cli import solve

# Expected G1 success vector (Report/11 §2): [2, 2, 7, 3, 3, 10] (1-index)


class TestUOut01ResultLength:
    """U-OUT-01 — successful solve returns int[6]."""

    def test_u_out_01_success_result_length_is_six(self) -> None:
        """U-OUT-01 / AC-FR-05-03 — len(result) == 6 for valid G1 input."""
        # Given
        # matrix = GRID_G1
        # mocker.patch("magic_square.control.solver.resolve", return_value=[2, 2, 7, 3, 3, 10])

        # When
        # result = solve(matrix)

        pytest.fail("RED: U-OUT-01 — G1 success path → solve returns length-6 int list")


class TestUOut02CoordinatesOneIndexed:
    """U-OUT-02 — r,c are 1-index in [1,4]; fill values match missing numbers."""

    def test_u_out_02_success_coordinates_are_1_index_in_range(self) -> None:
        """U-OUT-02 / I11 — 1-index coords in [1,4] for G1 stub [2,2,7,3,3,10]."""
        # Given
        # matrix = GRID_G1
        # mocker.patch("magic_square.control.solver.resolve", return_value=[2, 2, 7, 3, 3, 10])

        # When
        # result = solve(matrix)

        pytest.fail(
            "RED: U-OUT-02 — G1 output r,c ∈ [1,4] (1-index); n1=7, n2=10"
        )


class TestUOut03FillValuesMatchMissing:
    """U-OUT-03 — n1,n2 equal sorted missing numbers from partial grid."""

    def test_u_out_03_success_fill_values_match_missing_numbers(self) -> None:
        """U-OUT-03 / I7+I11 — n1,n2 are missing values {7,10} for G1."""
        # Given
        # matrix = GRID_G1
        # mocker.patch("magic_square.control.solver.resolve", return_value=[2, 2, 7, 3, 3, 10])

        # When
        # result = solve(matrix)

        pytest.fail(
            "RED: U-OUT-03 — G1 success → result[2]==7 and result[5]==10 (missing nums)"
        )
