"""Track B — D-MIS-01: MissingNumberFinder (RED skeleton).

Domain Mock 금지.
"""

from __future__ import annotations

import pytest

from magic_square.control.missing_number_finder import find_not_exist_nums

# G1 missing non-zero values (sorted): [7, 10]


class TestDMis01FindNotExistNums:
    """D-MIS-01 — G1 → sorted missing values [7, 10]."""

    def test_d_mis_01_find_not_exist_nums_g1_sorted(self) -> None:
        """D-MIS-01 / I7 / AC-3-2 — G1 missing numbers sorted ascending."""
        # Given
        # matrix = GRID_G1

        # When
        # missing = find_not_exist_nums(matrix)

        pytest.fail("RED: D-MIS-01 — G1 → find_not_exist_nums returns [7, 10]")
