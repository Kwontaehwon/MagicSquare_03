"""Track B — D-LOC-01: BlankFinder coordinates (RED skeleton).

Domain Mock 금지 — real Control entry point only.
"""

from __future__ import annotations

import pytest

from magic_square.control.blank_finder import find_blank_coords

# G1 blanks (0-index row-major): (2, 2), (3, 3)


class TestDLoc01FindBlankCoords:
    """D-LOC-01 — G1 → [(2,2), (3,3)] in 0-index row-major order."""

    def test_d_loc_01_find_blank_coords_g1_row_major_0_index(self) -> None:
        """D-LOC-01 / I6 / AC-2-3 — G1 blank coords row-major 0-index."""
        # Given
        # matrix = GRID_G1

        # When
        # coords = find_blank_coords(matrix)

        pytest.fail(
            "RED: D-LOC-01 — G1 → find_blank_coords returns [(2,2), (3,3)] 0-index"
        )
