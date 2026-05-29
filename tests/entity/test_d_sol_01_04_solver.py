"""Track B — D-SOL-01~04: Solver solution()."""

from __future__ import annotations

import pytest

from magic_square.control.solver import UnsolvableDomainError, solution
from tests.conftest import GRID_G1, GRID_G2, GRID_G3


class TestDSol01G1StepASuccess:
    """D-SOL-01 — G1 Step A (small-first) success."""

    def test_d_sol_01_solution_g1_step_a_success(self) -> None:
        """D-SOL-01 / I8 — G1 → solution returns [2,2,7,3,3,10]."""
        # Given
        matrix = GRID_G1

        # When
        result = solution(matrix)

        # Then
        assert result == [2, 2, 7, 3, 3, 10]


class TestDSol02G2StepBFallback:
    """D-SOL-02 — G2 Step A fails, Step B succeeds."""

    def test_d_sol_02_solution_g2_step_a_fail_step_b_success(self) -> None:
        """D-SOL-02 / I9 — G2 surrogate → [3,3,6,4,4,1]."""
        # Given
        matrix = GRID_G2

        # When
        result = solution(matrix)

        # Then
        assert result == [3, 3, 6, 4, 4, 1]


class TestDSol03G3BothStepsFail:
    """D-SOL-03 — G3: both combinations fail → domain error."""

    def test_d_sol_03_solution_g3_both_steps_fail(self) -> None:
        """D-SOL-03 / I10 — G3 → UnsolvableDomainError (no success return)."""
        # Given
        matrix = GRID_G3

        # When / Then
        with pytest.raises(UnsolvableDomainError):
            solution(matrix)


class TestDSol04OutputShapeOneIndex:
    """D-SOL-04 — output shape: len 6, 1-index coordinates."""

    def test_d_sol_04_solution_output_shape_1_index_coords(self) -> None:
        """D-SOL-04 / I8+I11 — G1 → len 6, coords 1-index in [1,4]."""
        # Given
        matrix = GRID_G1

        # When
        result = solution(matrix)

        # Then
        assert len(result) == 6
        assert all(1 <= result[i] <= 4 for i in (0, 1, 3, 4))
