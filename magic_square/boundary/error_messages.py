"""Boundary error codes and messages — SSOT for Failure envelope strings."""

from __future__ import annotations

from magic_square.entity.constants import MAX_CELL_VALUE

INVALID_SIZE_CODE = "INVALID_SIZE"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."

E002_CODE = "E002"
E002_MESSAGE = "Exactly two blank cells (0) are required."

E004_CODE = "E004"
E004_MESSAGE = f"Each cell must be 0 or an integer from 1 to {MAX_CELL_VALUE}."

E005_CODE = "E005"
E005_MESSAGE = "Non-zero cell values must not duplicate."
