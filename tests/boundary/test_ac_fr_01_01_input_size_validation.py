"""AC-FR-01-01 / PRD §8.1 INVALID_SIZE — Boundary grid structure validation tests.

Scope: grid=None and size-mismatch inputs only.
Excludes AC-FR-01-02~05 and FR-02~05 (blank count, value range, duplicates, solver logic).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from pydantic import BaseModel

from magic_square.boundary.cli import solve
from magic_square.boundary.input_validator import validate_grid
from magic_square.boundary.models import ValidationFailure

if TYPE_CHECKING:
    from pytest_mock.plugin import MockerFixture

# PRD §8.1 / test_plan.md — failure contract (exact strings)
AC_FR_01_01: str = "AC-FR-01-01"
PRD_SECTION: str = "§8.1"
INVALID_SIZE_CODE: str = "INVALID_SIZE"
INVALID_SIZE_MESSAGE: str = "Grid must be 4x4."


class _ExpectedFailureShape(BaseModel):
    """Expected failure DTO shape for AC-FR-01-01 (pydantic structural check)."""

    code: str
    message: str


def _three_by_four_grid() -> list[list[int]]:
    return [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
    ]


class TestAcFr0101InvalidSizeFailureReturn:
    """AC-FR-01-01: PRD §8.1 INVALID_SIZE — normal failure return path."""

    def test_none_grid_returns_invalid_size_code(self) -> None:
        """AC-FR-01-01 / PRD §8.1 INVALID_SIZE — None grid yields INVALID_SIZE code."""
        # AC-FR-01-01
        # Given
        grid: None = None

        # When
        result: ValidationFailure = validate_grid(grid)

        # Then
        assert result.code == INVALID_SIZE_CODE, (
            "None grid must yield INVALID_SIZE per PRD §8.1"
        )

    def test_none_grid_returns_invalid_size_message(self) -> None:
        """AC-FR-01-01 / PRD §8.1 INVALID_SIZE — None grid yields exact PRD message."""
        # AC-FR-01-01
        # Given
        grid: None = None

        # When
        result: ValidationFailure = validate_grid(grid)

        # Then
        assert result.message == INVALID_SIZE_MESSAGE, (
            "None grid message must match PRD §8.1 verbatim"
        )


class TestAcFr0101BoundarySizeInputs:
    """AC-FR-01-01: PRD §8.1 INVALID_SIZE — structural boundary inputs."""

    @pytest.mark.parametrize(
        "grid,case_label",
        [
            pytest.param([], "empty_list", id="empty_list"),
            pytest.param([[]] * 4, "four_rows_zero_cols", id="four_rows_zero_cols"),
            pytest.param(_three_by_four_grid(), "three_by_four", id="three_by_four"),
        ],
    )
    def test_size_mismatch_grid_returns_invalid_size(
        self,
        grid: list[list[int]],
        case_label: str,
    ) -> None:
        """AC-FR-01-01 / PRD §8.1 INVALID_SIZE — size mismatch returns INVALID_SIZE."""
        # AC-FR-01-01
        # Given — grid is not 4×4 (case: case_label)

        # When
        result: ValidationFailure = validate_grid(grid)

        # Then
        assert result.code == INVALID_SIZE_CODE, (
            f"{case_label}: non-4x4 grid must yield INVALID_SIZE"
        )
        assert result.message == INVALID_SIZE_MESSAGE, (
            f"{case_label}: message must match PRD §8.1 exactly"
        )


class TestAcFr0101MessageExactMatch:
    """AC-FR-01-01: PRD §8.1 INVALID_SIZE — character-level message identity."""

    def test_none_grid_message_matches_prd_section_8_1_character_for_character(
        self,
    ) -> None:
        """AC-FR-01-01 / PRD §8.1 INVALID_SIZE — message byte-for-byte equals PRD text."""
        # AC-FR-01-01
        # Given
        grid: None = None
        expected: _ExpectedFailureShape = _ExpectedFailureShape(
            code=INVALID_SIZE_CODE,
            message=INVALID_SIZE_MESSAGE,
        )

        # When
        result: ValidationFailure = validate_grid(grid)

        # Then
        assert result.code == expected.code
        assert result.message == expected.message
        assert len(result.message) == len(INVALID_SIZE_MESSAGE)
        assert list(result.message) == list(INVALID_SIZE_MESSAGE)


class TestAcFr0101DomainIsolation:
    """AC-FR-01-01: PRD §8.1 INVALID_SIZE — Control resolve() must not be invoked."""

    def test_none_grid_resolve_spy_called_zero_times(
        self,
        mocker: MockerFixture,
    ) -> None:
        """AC-FR-01-01 / PRD §8.1 INVALID_SIZE — None grid must not call resolve()."""
        # AC-FR-01-01
        # Given
        grid: None = None
        resolve_spy = mocker.patch(
            "magic_square.boundary.cli.resolve",
            autospec=True,
        )

        # When
        result: ValidationFailure = solve(grid)

        # Then — isolation checked before contract (spy is primary RED signal)
        resolve_spy.assert_not_called()
        assert resolve_spy.call_count == 0, (
            "resolve() must not run when grid is None (AC-1-6 / L3-4)"
        )
        assert result.code == INVALID_SIZE_CODE
        assert result.message == INVALID_SIZE_MESSAGE


class TestAcFr0101ScopeRestriction:
    """AC-FR-01-01 scope guard — size-only failures; no FR-02~05 or AC-FR-01-02~05 codes."""

    FORBIDDEN_CODES_IN_THIS_MODULE: frozenset[str] = frozenset(
        {
            "INVALID_BLANK_COUNT",
            "INVALID_VALUE_RANGE",
            "INVALID_DUPLICATE",
            "NO_SOLUTION",
        }
    )

    def test_none_grid_failure_code_is_invalid_size_not_out_of_scope_codes(
        self,
    ) -> None:
        """AC-FR-01-01 / PRD §8.1 INVALID_SIZE — failure code stays within AC-FR-01-01."""
        # AC-FR-01-01
        # Given
        grid: None = None

        # When
        result: ValidationFailure = validate_grid(grid)

        # Then
        assert result.code == INVALID_SIZE_CODE
        assert result.code not in self.FORBIDDEN_CODES_IN_THIS_MODULE, (
            "AC-FR-01-02~05 and FR-02~05 failure codes must not appear in this RED scope"
        )

    def test_red_scope_permits_only_invalid_size_failure_code(self) -> None:
        """AC-FR-01-01 / PRD §8.1 INVALID_SIZE — RED commit allows only INVALID_SIZE."""
        # AC-FR-01-01
        # Given
        allowed_codes: frozenset[str] = frozenset({INVALID_SIZE_CODE})

        # When / Then — FR-02~05 and AC-FR-01-02~05 codes are out of scope
        assert INVALID_SIZE_CODE in allowed_codes
        assert self.FORBIDDEN_CODES_IN_THIS_MODULE.isdisjoint(allowed_codes)
