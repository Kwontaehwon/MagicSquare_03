"""Track B — D-LOC-01: BlankFinder coordinates."""

from __future__ import annotations

from magic_square.control.blank_finder import find_blank_coords
from tests.conftest import GRID_G1


class TestDLoc01FindBlankCoords:
    """D-LOC-01 — G1 → row-major 0-index blank coordinates."""

    def test_d_loc_01_find_blank_coords_g1_row_major_0_index(self) -> None:
        """D-LOC-01 / I6 / AC-2-3 — G1 blank coords row-major 0-index."""
        # Given
        matrix = GRID_G1

        # When
        coords = find_blank_coords(matrix)

        # Then
        assert coords == [(1, 2), (3, 3)]
