"""Golden Master output contract assertions — GM-2."""

from __future__ import annotations

from magic_square.boundary.models import ValidationFailure
from magic_square.control.blank_finder import find_blank_coords
from magic_square.control.missing_number_finder import find_not_exist_nums

from tests.golden_master.scenarios import GoldenScenario

Grid = list[list[int]]
SolveResult = list[int] | ValidationFailure


def assert_solver_contract(result: SolveResult, scenario: GoldenScenario) -> None:
    """Verify int[6] / Error Contract rules before Golden Master file comparison."""
    if scenario.expect_success:
        _assert_success_contract(result, scenario.grid, scenario.combo_rule)
    else:
        _assert_failure_contract(result, scenario)


def _assert_row_major_blank_scan(grid: Grid) -> list[tuple[int, int]]:
    """Blank discovery must scan the grid in row-major order."""
    blanks = find_blank_coords(grid)
    expected: list[tuple[int, int]] = []
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell == 0:
                expected.append((row_index, col_index))
    assert blanks == expected, "blank coordinates must be collected row-major"
    return blanks


def _assert_success_contract(
    result: SolveResult,
    grid: Grid,
    combo_rule: str,
) -> None:
    assert isinstance(result, list), "success path must return int[6]"
    assert len(result) == 6, "success output must have length 6"

    r1, c1, n1, r2, c2, n2 = result
    assert all(isinstance(value, int) for value in result)

    for coord in (r1, c1, r2, c2):
        assert 1 <= coord <= 4, "coordinates must be 1-index in [1, 4]"

    _assert_row_major_blank_scan(grid)

    missing = find_not_exist_nums(grid)
    assert len(missing) == 2
    assert {n1, n2} == set(missing)

    if combo_rule == "small_first":
        assert [n1, n2] == sorted(missing), "small-first combination rule"
    elif combo_rule == "reverse_fallback":
        assert [n1, n2] == sorted(missing, reverse=True), "reverse fallback rule"
        blanks = find_blank_coords(grid)
        assert [r1, c1, n1, r2, c2, n2] == [
            blanks[0][0] + 1,
            blanks[0][1] + 1,
            n1,
            blanks[1][0] + 1,
            blanks[1][1] + 1,
            n2,
        ], "reverse fallback output follows row-major blank coordinates"


def _assert_failure_contract(result: SolveResult, scenario: GoldenScenario) -> None:
    assert isinstance(result, ValidationFailure), "failure path must return ValidationFailure"
    assert result.code == scenario.expected_code, "error code must match Error Contract"
    assert result.message == scenario.expected_message, "error message must match Error Contract"
