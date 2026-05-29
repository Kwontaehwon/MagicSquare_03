"""Entity constants — derived from grid size."""

from __future__ import annotations

GRID_SIZE = 4


def magic_constant(n: int) -> int:
  return n * (n**2 + 1) // 2


MAGIC_CONSTANT = magic_constant(GRID_SIZE)
