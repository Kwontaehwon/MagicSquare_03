"""Boundary GUI — PyQt6 presentation layer for Magic Square solver."""

from __future__ import annotations

import sys

from magic_square.boundary.cli import solve
from magic_square.boundary.display import (
    format_col_sums,
    format_row_sums,
    format_solution,
    magic_constant_label,
)
from magic_square.boundary.models import ValidationFailure
from magic_square.entity.constants import GRID_SIZE, MAGIC_CONSTANT

Board = list[list[int]]

_BLANK = 0
_MIN_VALUE = 0
_MAX_VALUE = 16
_CELL_SIZE = 56

_EXAMPLE_G1: Board = [
    [16, 2, 3, 13],
    [5, 11, 0, 8],
    [9, 1, 6, 12],
    [4, 14, 15, 0],
]

_STYLE_SUCCESS = "color: #1b5e20; background: #e8f5e9; border-radius: 6px; padding: 10px;"
_STYLE_ERROR = "color: #b71c1c; background: #ffebee; border-radius: 6px; padding: 10px;"
_STYLE_INFO = "color: #0d47a1; background: #e3f2fd; border-radius: 6px; padding: 10px;"


def _require_pyqt6():
    try:
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QFont
        from PyQt6.QtWidgets import (
            QApplication,
            QGridLayout,
            QGroupBox,
            QHBoxLayout,
            QLabel,
            QMainWindow,
            QPushButton,
            QSpinBox,
            QVBoxLayout,
            QWidget,
        )
    except ImportError as exc:
        raise SystemExit(
            "PyQt6 is required for the GUI. Install with: pip install PyQt6"
        ) from exc
    return (
        Qt,
        QFont,
        QApplication,
        QGridLayout,
        QGroupBox,
        QHBoxLayout,
        QLabel,
        QMainWindow,
        QPushButton,
        QSpinBox,
        QVBoxLayout,
        QWidget,
    )


class MagicSquareWindow:
    """Main window — delegates solving to boundary cli.solve()."""

    def __init__(self) -> None:
        (
            self._Qt,
            QFont,
            _QApplication,
            QGridLayout,
            QGroupBox,
            QHBoxLayout,
            QLabel,
            QMainWindow,
            QPushButton,
            QSpinBox,
            QVBoxLayout,
            QWidget,
        ) = _require_pyqt6()

        self._window = QMainWindow()
        self._window.setWindowTitle("4×4 Magic Square")
        self._window.setMinimumSize(520, 620)

        central = QWidget()
        self._window.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setSpacing(14)

        title = QLabel("4×4 Magic Square Solver")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(self._Qt.AlignmentFlag.AlignCenter)
        root.addWidget(title)

        subtitle = QLabel(
            f"빈칸(0) 2개를 채워 모든 행·열·대각선의 합이 "
            f"{magic_constant_label()}이 되도록 합니다."
        )
        subtitle.setWordWrap(True)
        subtitle.setAlignment(self._Qt.AlignmentFlag.AlignCenter)
        root.addWidget(subtitle)

        grid_group = QGroupBox("격자 입력 (0 = 빈칸)")
        grid_layout = QGridLayout(grid_group)
        grid_layout.setSpacing(6)

        header_font = QFont()
        header_font.setBold(True)

        for col in range(GRID_SIZE):
            label = QLabel(str(col + 1))
            label.setAlignment(self._Qt.AlignmentFlag.AlignCenter)
            label.setFont(header_font)
            grid_layout.addWidget(label, 0, col + 1)

        self._cells: list[list[QSpinBox]] = []
        for row in range(GRID_SIZE):
            row_label = QLabel(str(row + 1))
            row_label.setAlignment(self._Qt.AlignmentFlag.AlignCenter)
            row_label.setFont(header_font)
            grid_layout.addWidget(row_label, row + 1, 0)

            row_cells: list[QSpinBox] = []
            for col in range(GRID_SIZE):
                spin = QSpinBox()
                spin.setRange(_MIN_VALUE, _MAX_VALUE)
                spin.setSpecialValueText("·")
                spin.setAlignment(self._Qt.AlignmentFlag.AlignCenter)
                spin.setFixedSize(_CELL_SIZE, _CELL_SIZE)
                spin.setFont(QFont("Consolas", 12))
                spin.valueChanged.connect(self._on_grid_changed)
                grid_layout.addWidget(spin, row + 1, col + 1)
                row_cells.append(spin)
            self._cells.append(row_cells)

        root.addWidget(grid_group)

        sums_layout = QHBoxLayout()
        self._row_sums_label = QLabel()
        self._col_sums_label = QLabel()
        sums_layout.addWidget(self._row_sums_label)
        sums_layout.addWidget(self._col_sums_label)
        root.addLayout(sums_layout)

        button_layout = QHBoxLayout()
        solve_btn = QPushButton("풀이")
        solve_btn.setDefault(True)
        solve_btn.clicked.connect(self._on_solve)
        button_layout.addWidget(solve_btn)

        example_btn = QPushButton("예제 (G1)")
        example_btn.clicked.connect(self._load_example)
        button_layout.addWidget(example_btn)

        clear_btn = QPushButton("초기화")
        clear_btn.clicked.connect(self._clear_grid)
        button_layout.addWidget(clear_btn)
        root.addLayout(button_layout)

        self._result_label = QLabel("격자를 입력한 뒤 「풀이」를 누르세요.")
        self._result_label.setWordWrap(True)
        self._result_label.setStyleSheet(_STYLE_INFO)
        root.addWidget(self._result_label)

        root.addStretch()
        self._update_sums()

    def show(self) -> None:
        self._window.show()

    def _read_grid(self) -> Board:
        return [[cell.value() for cell in row] for row in self._cells]

    def _write_grid(self, board: Board) -> None:
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self._cells[row][col].setValue(board[row][col])
        self._update_sums()

    def _clear_grid(self) -> None:
        for row in self._cells:
            for cell in row:
                cell.setValue(_BLANK)
        self._result_label.setText("격자가 초기화되었습니다.")
        self._result_label.setStyleSheet(_STYLE_INFO)

    def _load_example(self) -> None:
        self._write_grid(_EXAMPLE_G1)
        self._result_label.setText("예제 G1이 로드되었습니다. 「풀이」를 눌러 보세요.")
        self._result_label.setStyleSheet(_STYLE_INFO)

    def _on_grid_changed(self) -> None:
        self._update_sums()

    def _update_sums(self) -> None:
        board = self._read_grid()
        row_sums = format_row_sums(board)
        col_sums = format_col_sums(board)
        target = MAGIC_CONSTANT
        self._row_sums_label.setText(
            "행 합: "
            + "  ".join(f"{s:>2}" + ("✓" if s == target else "") for s in row_sums)
        )
        self._col_sums_label.setText(
            "열 합: "
            + "  ".join(f"{s:>2}" + ("✓" if s == target else "") for s in col_sums)
        )

    def _apply_solution(self, result: list[int]) -> None:
        r1, c1, n1, r2, c2, n2 = result
        self._cells[r1 - 1][c1 - 1].setValue(n1)
        self._cells[r2 - 1][c2 - 1].setValue(n2)
        self._update_sums()

    def _on_solve(self) -> None:
        grid = self._read_grid()
        result = solve(grid)

        if isinstance(result, ValidationFailure):
            self._result_label.setText(f"[{result.code}] {result.message}")
            self._result_label.setStyleSheet(_STYLE_ERROR)
            return

        self._apply_solution(result)
        self._result_label.setText(
            "풀이 완료!\n\n"
            + format_solution(result)
            + f"\n\n목표 합(Magic Constant): {MAGIC_CONSTANT}"
        )
        self._result_label.setStyleSheet(_STYLE_SUCCESS)


def main() -> None:
    """Launch the Magic Square GUI application."""
    _Qt, _QFont, QApplication, *_ = _require_pyqt6()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MagicSquareWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
