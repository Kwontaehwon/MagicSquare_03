"""Shared grid fixtures — G0~G3 (Report/11 §2)."""

from __future__ import annotations

GRID_G0: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

GRID_G1: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 0, 8],
    [9, 1, 6, 12],
    [4, 14, 15, 0],
]

GRID_G2: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

GRID_G3: list[list[int]] = [
    [8, 1, 0, 6],
    [0, 5, 7, 2],
    [3, 0, 4, 5],
    [9, 11, 12, 13],
]

THREE_BLANK_GRID: list[list[int]] = [
    [0, 1, 2, 3],
    [4, 0, 6, 7],
    [8, 9, 0, 11],
    [12, 13, 14, 15],
]

NEGATIVE_VALUE_GRID: list[list[int]] = [
    [1, 2, 3, 4],
    [5, -1, 7, 8],
    [9, 10, 0, 12],
    [13, 14, 15, 0],
]

VALUE_17_GRID: list[list[int]] = [
    [1, 2, 3, 4],
    [5, 17, 7, 8],
    [9, 10, 0, 12],
    [13, 14, 15, 0],
]

DUPLICATE_NONZERO_GRID: list[list[int]] = [
    [1, 1, 0, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 0],
]
