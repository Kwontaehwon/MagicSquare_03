"""GM-2 — Golden Master regression tests for Magic Square Solver.

Run:
    pytest -m golden_master -v

Approve baseline refresh:
    set GM_APPROVE=1
    pytest -m golden_master -v
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from magic_square.boundary.cli import solve
from tests.golden_master.approve import (
    DEFAULT_GOLDEN_PATH,
    approve_section,
    build_golden_master_document,
    compare_text_baseline,
)
from tests.golden_master.contracts import assert_solver_contract
from tests.golden_master.scenarios import GOLDEN_SCENARIOS, GoldenScenario

pytestmark = pytest.mark.golden_master


@pytest.fixture(scope="session")
def golden_master_path() -> Path:
    return DEFAULT_GOLDEN_PATH


@pytest.fixture(scope="session")
def approve_mode() -> bool:
    return os.environ.get("GM_APPROVE", "").lower() in {"1", "true", "yes"}


class TestGoldenMasterMagicSquareDocument:
    """GM-2 — full baseline file approve/compare via open(expected).read()."""

    def test_gm_02_full_baseline_matches_solver_output(
        self,
        golden_master_path: Path,
        approve_mode: bool,
    ) -> None:
        """[GoldenMaster] entire golden_master_expected.txt vs live capture."""
        actual_document = build_golden_master_document()
        compare_text_baseline(
            expected_path=golden_master_path,
            actual=actual_document,
            approve=approve_mode,
            context="full document",
        )


@pytest.mark.parametrize(
    "scenario",
    GOLDEN_SCENARIOS,
    ids=[scenario.test_id for scenario in GOLDEN_SCENARIOS],
)
class TestGoldenMasterMagicSquareCases:
    """GM-2 — GM-TC-01~05 contract + section Golden Master tests."""

    def test_gm_tc_matches_baseline_and_contract(
        self,
        scenario: GoldenScenario,
        golden_master_path: Path,
        approve_mode: bool,
    ) -> None:
        """[GoldenMaster] API result serialization + Error Contract + baseline diff."""
        result = solve(scenario.grid)
        assert_solver_contract(result, scenario)
        approve_section(
            scenario=scenario,
            expected_path=golden_master_path,
            approve=approve_mode,
        )
