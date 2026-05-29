"""Golden Master approve pattern — capture, compare, and optional refresh."""

from __future__ import annotations

import difflib
from pathlib import Path

from magic_square.boundary.cli import solve
from magic_square.boundary.models import ValidationFailure

from tests.golden_master.scenarios import GOLDEN_SCENARIOS, SECTION_SEPARATOR, GoldenScenario

DEFAULT_GOLDEN_PATH = Path(__file__).resolve().parent.parent / "golden_master_expected.txt"
Grid = list[list[int]]


def format_grid(grid: Grid) -> str:
    """Render a 4x4 grid as space-separated rows."""
    return "\n".join(" ".join(str(cell) for cell in row) for row in grid)


def serialize_success(result: list[int]) -> str:
    """Serialize int[6] solver output in compact list form."""
    return "[" + ",".join(str(value) for value in result) + "]"


def serialize_failure(failure: ValidationFailure) -> str:
    """Serialize ValidationFailure as Error block."""
    return f"Error:\n{failure.code}\n{failure.message}"


def capture_output(grid: Grid) -> str:
    """Capture Boundary solve() result as Golden Master output text."""
    result = solve(grid)
    if isinstance(result, ValidationFailure):
        return serialize_failure(result)
    if isinstance(result, list):
        return serialize_success(result)
    raise TypeError(f"Unexpected solve() return type: {type(result)!r}")


def serialize_section(scenario: GoldenScenario, output: str | None = None) -> str:
    """Serialize one Golden Master section."""
    captured = output if output is not None else capture_output(scenario.grid)
    if captured.startswith("Error:"):
        body_label = "Error:"
        body = captured.removeprefix("Error:\n")
    else:
        body_label = "Output:"
        body = captured
    return (
        f"[{scenario.name}]\n"
        f"Input:\n"
        f"{format_grid(scenario.grid)}\n"
        f"{body_label}\n"
        f"{body}"
    )


def build_golden_master_document(
    scenarios: tuple[GoldenScenario, ...] = GOLDEN_SCENARIOS,
) -> str:
    """Build the full Golden Master baseline file content."""
    sections = [serialize_section(scenario) for scenario in scenarios]
    return f"\n{SECTION_SEPARATOR}\n".join(sections) + "\n"


def parse_golden_master(text: str) -> dict[str, str]:
    """Parse Golden Master file into section name -> full section text."""
    sections: dict[str, str] = {}
    blocks = text.split(SECTION_SEPARATOR)
    for block in blocks:
        stripped = block.strip()
        if not stripped:
            continue
        if not stripped.startswith("["):
            raise ValueError("Golden Master section must start with [section_name]")
        header_end = stripped.index("]")
        name = stripped[1:header_end]
        sections[name] = stripped
    return sections


def write_golden_master(path: Path, content: str) -> None:
    """Write Golden Master baseline file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def read_expected_baseline(path: Path) -> str:
    """Read Golden Master baseline via open(path).read()."""
    with path.open(encoding="utf-8") as handle:
        return handle.read()


def format_unified_diff(expected: str, actual: str, *, fromfile: str, tofile: str) -> str:
    """Format expected vs actual as unified diff for test failure output."""
    return "\n".join(
        difflib.unified_diff(
            expected.splitlines(),
            actual.splitlines(),
            fromfile=fromfile,
            tofile=tofile,
            lineterm="",
        )
    )


def compare_text_baseline(
    *,
    expected_path: Path,
    actual: str,
    approve: bool = False,
    context: str,
) -> None:
    """Approve pattern: create baseline if missing, otherwise compare file content."""
    if not expected_path.exists():
        write_golden_master(expected_path, actual)
        if approve:
            return
        raise AssertionError(
            f"Golden Master baseline created at {expected_path} ({context}). "
            "Review the file and re-run tests."
        )

    expected = read_expected_baseline(expected_path)
    if expected == actual:
        return

    if approve:
        write_golden_master(expected_path, actual)
        return

    diff = format_unified_diff(
        expected,
        actual,
        fromfile="expected",
        tofile="actual",
    )
    raise AssertionError(
        f"Golden Master mismatch ({context}) in {expected_path}:\n{diff}"
    )


def approve_section(
    *,
    scenario: GoldenScenario,
    expected_path: Path = DEFAULT_GOLDEN_PATH,
    approve: bool = False,
) -> str | None:
    """Compare or create one Golden Master section.

    Returns refreshed section text when approve=True and content was written.
    Raises AssertionError with unified diff when actual != expected.
    """
    actual_section = serialize_section(scenario)
    if not expected_path.exists():
        return _bootstrap_missing_file(expected_path, actual_section, scenario.name, approve)

    expected_sections = parse_golden_master(read_expected_baseline(expected_path))
    expected_section = expected_sections.get(scenario.name)
    if expected_section is None:
        raise AssertionError(
            f"Golden Master section [{scenario.name}] is missing in {expected_path}"
        )

    if actual_section == expected_section:
        return None

    if approve:
        refreshed = _replace_section(expected_path, scenario.name, actual_section)
        return refreshed

    diff = format_unified_diff(
        expected_section,
        actual_section,
        fromfile=f"expected [{scenario.name}]",
        tofile=f"actual [{scenario.name}]",
    )
    raise AssertionError(
        f"Golden Master mismatch for [{scenario.name}] in {expected_path}:\n{diff}"
    )


def approve_all(
    *,
    expected_path: Path = DEFAULT_GOLDEN_PATH,
    approve: bool = False,
    scenarios: tuple[GoldenScenario, ...] = GOLDEN_SCENARIOS,
) -> bool:
    """Run approve pattern for all scenarios. Returns True if file was (re)written."""
    actual_document = build_golden_master_document(scenarios)
    if not expected_path.exists():
        write_golden_master(expected_path, actual_document)
        if approve:
            return True
        raise AssertionError(
            f"Golden Master baseline created at {expected_path}. "
            "Review the file and re-run tests."
        )

    expected_document = read_expected_baseline(expected_path)
    compare_text_baseline(
        expected_path=expected_path,
        actual=actual_document,
        approve=approve,
        context="full document",
    )
    return approve


def _bootstrap_missing_file(
    expected_path: Path,
    actual_section: str,
    section_name: str,
    approve: bool,
) -> str | None:
    content = build_golden_master_document()
    write_golden_master(expected_path, content)
    if approve:
        return actual_section
    raise AssertionError(
        f"Golden Master baseline created at {expected_path}. "
        f"Re-run tests after reviewing section [{section_name}]."
    )


def _replace_section(path: Path, section_name: str, new_section: str) -> str:
    sections = parse_golden_master(read_expected_baseline(path))
    sections[section_name] = new_section
    ordered = []
    for scenario in GOLDEN_SCENARIOS:
        if scenario.name in sections:
            ordered.append(sections[scenario.name])
    content = f"\n{SECTION_SEPARATOR}\n".join(ordered) + "\n"
    write_golden_master(path, content)
    return new_section
