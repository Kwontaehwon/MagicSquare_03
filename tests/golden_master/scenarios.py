"""Golden Master input scenarios — GM-1 / GM-2."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from tests.conftest import (
    DUPLICATE_NONZERO_GRID,
    GRID_G1,
    GRID_G2,
    THREE_BLANK_GRID,
)

Grid = list[list[int]]
ComboRule = Literal["small_first", "reverse_fallback", "none"]

# Two blanks, valid input, but neither placement order completes a magic square.
UNSOLVABLE_GRID: Grid = [
    [0, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 12, 4],
    [14, 15, 6, 0],
]

SECTION_SEPARATOR = "________________________________________"

E002_MESSAGE = "Exactly two blank cells (0) are required."
E005_MESSAGE = "Non-zero cell values must not duplicate."
UNSOLVABLE_MESSAGE = "no placement order yields a magic square"


@dataclass(frozen=True)
class GoldenScenario:
    """Named scenario for Golden Master capture, contract checks, and comparison."""

    test_id: str
    name: str
    grid: Grid
    expect_success: bool
    combo_rule: ComboRule = "none"
    expected_code: str = ""
    expected_message: str = ""


GOLDEN_SCENARIOS: tuple[GoldenScenario, ...] = (
    GoldenScenario(
        test_id="GM-TC-01",
        name="normal_success",
        grid=GRID_G1,
        expect_success=True,
        combo_rule="small_first",
    ),
    GoldenScenario(
        test_id="GM-TC-02",
        name="reverse_success",
        grid=GRID_G2,
        expect_success=True,
        combo_rule="reverse_fallback",
    ),
    GoldenScenario(
        test_id="GM-TC-03",
        name="invalid_blank_count",
        grid=THREE_BLANK_GRID,
        expect_success=False,
        expected_code="E002",
        expected_message=E002_MESSAGE,
    ),
    GoldenScenario(
        test_id="GM-TC-04",
        name="duplicate_number",
        grid=DUPLICATE_NONZERO_GRID,
        expect_success=False,
        expected_code="E005",
        expected_message=E005_MESSAGE,
    ),
    GoldenScenario(
        test_id="GM-TC-05",
        name="no_valid_solution",
        grid=UNSOLVABLE_GRID,
        expect_success=False,
        expected_code="UNSOLVABLE",
        expected_message=UNSOLVABLE_MESSAGE,
    ),
)
