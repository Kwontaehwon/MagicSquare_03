#!/usr/bin/env python3
"""Generate Golden Master baseline from current Magic Square Solver output."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests.golden_master.approve import DEFAULT_GOLDEN_PATH, build_golden_master_document, write_golden_master


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate tests/golden_master_expected.txt from live solver output.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_GOLDEN_PATH,
        help="Golden Master baseline path (default: tests/golden_master_expected.txt)",
    )
    args = parser.parse_args()

    content = build_golden_master_document()
    write_golden_master(args.output, content)
    print(f"Golden Master baseline written to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
