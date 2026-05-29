"""Track A — U-FLOW-02 (extended): invalid input never reaches Control.

Base U-FLOW-02 null case overlaps test_ac_fr_01_01 spy — extended E002/E004/E005 paths.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from magic_square.boundary.cli import solve

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture


class TestUFlow02InvalidNeverCallsResolve:
    """U-FLOW-02 — short-circuit: resolve/execute call_count == 0 on invalid input."""

    def test_u_flow_02_null_matrix_resolve_spy_zero_calls(
        self,
        mocker: "MockerFixture",
    ) -> None:
        """U-FLOW-02 / AC-1-6 — null matrix → resolve() not called."""
        # Given
        # grid = None
        # resolve_spy = mocker.patch("magic_square.control.solver.resolve", autospec=True)

        # When
        # result = solve(grid)

        pytest.fail("RED: U-FLOW-02 — null input → resolve call_count == 0")

    def test_u_flow_02_e002_blank_count_resolve_spy_zero_calls(
        self,
        mocker: "MockerFixture",
    ) -> None:
        """U-FLOW-02 ext — E002 (blank ≠ 2) → resolve() not called."""
        # Given
        # grid = GRID_G0  # 0 blanks
        # resolve_spy = mocker.patch("magic_square.control.solver.resolve", autospec=True)

        # When
        # result = solve(grid)

        pytest.fail("RED: U-FLOW-02 ext — E002 path → resolve call_count == 0")

    def test_u_flow_02_e004_value_range_resolve_spy_zero_calls(
        self,
        mocker: "MockerFixture",
    ) -> None:
        """U-FLOW-02 ext — E004 (value out of range) → resolve() not called."""
        # Given
        # grid = 4×4 with cell 17
        # resolve_spy = mocker.patch("magic_square.control.solver.resolve", autospec=True)

        # When
        # result = solve(grid)

        pytest.fail("RED: U-FLOW-02 ext — E004 path → resolve call_count == 0")

    def test_u_flow_02_e005_duplicate_resolve_spy_zero_calls(
        self,
        mocker: "MockerFixture",
    ) -> None:
        """U-FLOW-02 ext — E005 (non-zero duplicate) → resolve() not called."""
        # Given
        # grid = 4×4 with duplicate non-zero
        # resolve_spy = mocker.patch("magic_square.control.solver.resolve", autospec=True)

        # When
        # result = solve(grid)

        pytest.fail("RED: U-FLOW-02 ext — E005 path → resolve call_count == 0")
