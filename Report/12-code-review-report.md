# 4×4 Magic Square — Code Review 보고서

**작성일**: 2026-05-29  
**단계**: GREEN 구현 이후 — 전체 코드베이스 품질 검토  
**선행 산출물**: `Report/10-prd-boundary-red-qa-report.md`, `Report/11-dual-track-red-design-report.md`  
**대화 재현**: `Prompt/08-code-review-conversation-transcript.md`  
**검토 방법**: Code Reviewer 서브에이전트 위임 + 소스 직접 확인  
**목적**: ECB·불변 조건·금지 패턴 준수 여부를 점검하고, P0~P2 개선 항목을 기록한다.

---

## 0. 본 보고서의 범위

| 구분 | 위치 |
|---|---|
| 검토 대상 (Control) | `magic_square/control/` — validator, solver, blank_finder, missing_number_finder |
| 검토 대상 (Boundary) | `magic_square/boundary/` — input_validator, cli, display, gui, models |
| 검토 대상 (Entity) | `magic_square/entity/` — constants, user |
| 검토 대상 (Tests) | `tests/entity/`, `tests/boundary/`, `tests/golden_master/` |
| 프로젝트 규칙 | `.cursor/rules/magicsquare-forbidden.mdc`, `magicsquare-project.mdc`, `magicsquare-ecb-architecture.mdc` |
| 대화 트랜스크립트 | `Prompt/08-code-review-conversation-transcript.md` |
| 본 보고서 | `Report/12-code-review-report.md` |

**본 보고서 범위 밖:** P0~P2 권장 사항의 실제 코드 수정 (별도 GREEN/REFACTOR 세션)

---

## 1. 세션 목표 및 성과

### 1.1 목표

| # | 목표 | 달성 |
|---|---|---|
| G1 | 전체 Python 소스 코드 리뷰 | ✅ entity / control / boundary / tests |
| G2 | 금지 패턴 5종 위반 여부 점검 | ✅ 위반 없음 확인 |
| G3 | ECB 레이어·책임 분리 평가 | ✅ 대체로 준수, Level 3 긴장 1건 |
| G4 | 테스트 실행·통과 확인 | ✅ 52 passed (0.26s) |
| G5 | 우선순위별 개선 항목 도출 | ✅ P0 2건, P1 3건, P2 3건 |
| G6 | Report · Prompt Export | ✅ 본 문서, `Prompt/08` |

### 1.2 전체 평가 (Executive Summary)

MagicSquare 프로젝트는 ECB 레이어 분리, Magic Constant 유도, 10개 검증 조건의 독립 함수 분해, Golden Master·도메인 격리 테스트 등 **핵심 불변 조건을 대체로 잘 지킨 성숙한 코드베이스**입니다. `python -m pytest tests/ -q` 기준 **52 tests passed**.

다만 Boundary의 `NOT_IMPLEMENTED` 성공 센티널, solver의 G1 하드코딩, validator의 격자 형태 미검증, Level 3 책임 분리(solver→validator) 등은 **유지보수·확장 시 실제 리스크**로 남아 있습니다. 금지 패턴(34 하드코딩, 행만 검증, display 내 검증, 무기준 루프)은 **Python 소스에서 위반 사례를 찾지 못했습니다**.

---

## 2. 테스트 실행 결과

```
52 passed in 0.26s
```

| Track | 범위 | 비고 |
|---|---|---|
| Track A (Boundary) | U-IN, U-OUT, U-FLOW, AC-FR, Golden Master | 입력 계약·격리·회귀 |
| Track B (Domain) | D-VAL, D-SOL, D-MIS, D-LOC, User | Control 순수 로직 |
| Golden Master | 시나리오 기반 end-to-end | approve workflow 포함 |

---

## 3. 금지 패턴 체크리스트

| # | 패턴 | 결과 | 근거 |
|---|---|---|---|
| 1 | 목적/수단 혼동 (`make_magic_square` 등) | **통과** | `resolve`, `is_magic_square`, `format_*` |
| 2 | Magic Constant `34` 하드코딩 | **통과** | `.py`에 `34` 리터럴 없음, `magic_constant(n)` 사용 |
| 3 | 부분 검증 (행만 검사) | **통과** | 행 4 + 열 4 + 대각선 2 + 구성(Level 0) |
| 4 | display에 검증/생성 로직 | **통과** | `display.py`는 표현만 (GUI ✓ 표시는 boundary UI) |
| 5 | 무기준 루프 | **통과** | `while True` 없음; solver는 `is_magic_square`로 종료 |

---

## 4. 잘 된 점 (Strengths)

| 영역 | 내용 |
|---|---|
| **Magic Constant** | `magic_square/entity/constants.py`에서 `n * (n**2 + 1) // 2`로 유도 |
| **완전 검증** | `validator.py` — `_composition_valid`, `_rows_valid`, `_cols_valid`, `_main_diagonal_valid`, `_anti_diagonal_valid` + `is_magic_square` |
| **표현 분리** | `display.py`는 포맷만 담당, 검증·생성 로직 없음 |
| **경계 격리** | `test_u_flow_02_domain_isolation.py` — invalid 시 `resolve` 미호출 spy 검증 |
| **테스트 구조** | D-VAL/D-SOL/U-IN/Golden Master 시나리오, fixture `GRID_G0~G3` 명확 |
| **타입·모델** | `Board` 별칭, `ValidationFailure`(Pydantic), `User` frozen dataclass + invariant |
| **User 엔티티** | Level 4 identity invariant가 테스트와 1:1 대응 |

---

## 5. 이슈 목록

### 5.1 Critical (조건부)

현재 프로덕션 경로(`solve` → `validate_grid` → `resolve`)에서는 치명적 버그를 확인하지 못했습니다. Control을 직접 호출하거나 계약이 바뀔 때 Critical로 승격될 수 있습니다.

#### CR-01 — validator: 비정형 격자 시 `IndexError`

| 항목 | 내용 |
|---|---|
| **파일** | `magic_square/control/validator.py` (특히 `_cols_valid`, `_composition_valid`) |
| **심각도** | Major → 조건부 Critical |
| **문제** | `_composition_valid`는 flatten 셀 수(16)만 보며 4×4 정방형을 보장하지 않음. `len(board) != 4` 또는 행 길이 불일치 시 `_cols_valid`에서 `IndexError` 가능 |
| **수정 제안** | `_shape_valid(board) -> bool` 추가 (`len(board)==GRID_SIZE` 및 모든 `len(row)==GRID_SIZE`). 실패 시 `False` 반환 |

```python
# validator.py — 현재 _composition_valid는 셀 수만 확인
def _composition_valid(board: Board) -> bool:
    cells = [cell for row in board for cell in row]
    if len(cells) != GRID_SIZE * GRID_SIZE:
        return False
    ...
```

---

### 5.2 Major (중요 개선)

#### MJ-01 — `NOT_IMPLEMENTED`를 성공 신호로 사용

| 항목 | 내용 |
|---|---|
| **파일** | `magic_square/boundary/input_validator.py:68-71`, `magic_square/boundary/cli.py:14-18` |
| **심각도** | Major |
| **문제** | 모든 입력 검증 통과 후에도 `ValidationFailure(code="NOT_IMPLEMENTED")` 반환. `solve()`는 `code != "NOT_IMPLEMENTED"`일 때만 실패로 처리 → **통과=NOT_IMPLEMENTED** 역설. docstring은 "RED stub"인데 구현은 GREEN |
| **수정 제안** | `validate_grid() -> ValidationFailure | None` 또는 `Result[Board, ValidationFailure]`. 성공 시 `None`/성공 타입, 실패만 `ValidationFailure` |

#### MJ-02 — Solver G1 하드코딩 바이패스

| 항목 | 내용 |
|---|---|
| **파일** | `magic_square/control/solver.py:13-18`, `40-42` |
| **심각도** | Major |
| **문제** | `matrix == _G1_REFERENCE`이면 알고리즘 없이 고정 출력 반환. 회귀·리팩터 시 **가짜 녹색** 위험, `_G1_REFERENCE`가 테스트 fixture와 이중 유지 |
| **수정 제안** | 바이패스 제거 후 일반 `_try_fill` 경로만 사용 |

#### MJ-03 — Level 3: Control(solver) → Control(validator) 결합

| 항목 | 내용 |
|---|---|
| **파일** | `magic_square/control/solver.py:9`, `27-31` |
| **심각도** | Major (아키텍처) |
| **문제** | `magicsquare-ecb-architecture.mdc`는 `generate()`가 `validate()`를 import하지 말 것을 요구. solver는 `is_magic_square`로 후보 종료 → 생성(채움)과 검증이 한 모듈 체인에 묶임 |
| **수정 제안** | (a) ADR/규칙에 "부분 격자 해결은 후보 완성 후 마방진 판별 필요" 예외 명시, 또는 (b) 최종 판별을 boundary로 이동 |

#### MJ-04 — 프로젝트 규칙 네이밍과의 불일치

| 항목 | 내용 |
|---|---|
| **파일** | 전역 |
| **심각도** | Major (규칙 준수·가독성) |
| **문제** | `generate` / `validate` / `display` 공개 API 없음. 실제는 `resolve`/`solution`, `is_magic_square`, `format_board`/`format_solution` |
| **수정 제안** | 공개 별칭 추가 (`validate = is_magic_square`, `display = format_board`) 또는 규칙·README를 실제 API에 맞게 정렬 |

#### MJ-05 — 입력 검증의 `16` 하드코딩

| 항목 | 내용 |
|---|---|
| **파일** | `magic_square/boundary/input_validator.py:13`, `22-23` |
| **심각도** | Major (Level 2 정신 위반) |
| **문제** | `_GRID_SIZE=4`는 있으나 상한 `16`은 `GRID_SIZE**2`가 아님. 크기 변경 시 불일치 |
| **수정 제안** | `from magic_square.entity.constants import GRID_SIZE` 후 `1 <= cell <= GRID_SIZE * GRID_SIZE` |

---

### 5.3 Minor (권장 개선)

| ID | 위치 | 문제 | 수정 제안 |
|---|---|---|---|
| MN-01 | `input_validator.py:1`, `cli.py:1` | "RED stub" docstring과 구현 불일치 | GREEN 반영 또는 Optional 성공 타입으로 정리 |
| MN-02 | `input_validator.py:9` vs `entity/constants.py` | `_GRID_SIZE` 중복 | entity 상수 단일 출처 |
| MN-03 | `gui.py:24-29`, `solver.py:13-18` | 예제 G1 보드 중복 | `tests.conftest.GRID_G1` 또는 entity fixture 공유 |
| MN-04 | `test_d_val_01_06_validator.py` D-VAL-04 | 대각선 테스트가 주·반대각선 동시 훼손 가능 | 반대각선만 깨는 보드 추가 |
| MN-05 | `test_u_out_01_03` | 성공 시 `list` 타입 미검증 | `assert isinstance(result, list)` |
| MN-06 | `display.py` | `format_board` 등 단위 테스트 없음 | 표현 전용 스냅샷/문자열 테스트 추가 |

---

## 6. 테스트 커버리지 공백

| 미검증 시나리오 | 권장 테스트 |
|---|---|
| `magic_constant(n)` for `n≠4` | Level 2: `magic_constant(3)==15` 등 |
| **주대각선만** / **반대각선만** 실패 | 각각 `is_magic_square` False 독립 검증 |
| `validate_grid` **성공** 경로 | G1 입력 → 실패 아님(현재는 `NOT_IMPLEMENTED`만 암묵) |
| `is_magic_square` + 비4×4 격자 | `False` 또는 예외 정책 명시 |
| solver **G1 바이패스 제거 후** | D-SOL-01~04 재실행 |
| `format_board`, `format_solution` | boundary display 단위 테스트 |
| GUI / PyQt6 | optional dependency — 스킵 마커 또는 smoke |
| `resolve()` 직접 호출 + invalid shape | Boundary 우회 시 방어 |
| 빈칸 1개 / 4개 | E002 경계 확장 |
| 풀이 후 **완성 보드**가 `is_magic_square(True)` | end-to-end 도메인 보증 |

**참고:** `tests/conftest.py`의 `GRID_G3`와 `tests/golden_master/scenarios.py`의 `UNSOLVABLE_GRID`는 서로 다른 "无解" 격자 — 의도적이면 문서화, 아니면 통일 검토.

---

## 7. 권장 조치 (우선순위)

### P0 (즉시)

1. **`validate_grid` 성공 계약 정리** — `NOT_IMPLEMENTED` 제거, `solve()` 분기 단순화 (MJ-01)
2. **`is_magic_square`에 격자 형태 검증** 추가 — malformed board에서 `IndexError` 방지 (CR-01)

### P1 (다음 스프린트)

3. **solver G1 하드코딩 제거** — 일반 알고리즘만으로 D-SOL·Golden Master 유지 (MJ-02)
4. **주/반대각선 독립 negative 테스트** 추가 (MN-04)
5. **Level 3 solver–validator 관계** — ADR/규칙에 예외 또는 경계 이동 여부 결정 (MJ-03)

### P2 (개선)

6. `input_validator`의 `16` → `GRID_SIZE**2`, entity 상수 단일화 (MJ-05, MN-02)
7. 공개 API 별칭 `validate`/`display` 또는 문서·규칙 동기화 (MJ-04)
8. `format_board` 등 display 테스트, `magic_constant` 다중 n 테스트 (MN-06)

---

## 8. 산출물 트리

```
MagicSquare_/
├── Report/
│   ├── 10-prd-boundary-red-qa-report.md
│   ├── 11-dual-track-red-design-report.md
│   └── 12-code-review-report.md                    ← 본 문서
├── Prompt/
│   └── 08-code-review-conversation-transcript.md   ← Full Export
├── magic_square/
│   ├── entity/     constants.py, user.py
│   ├── control/    validator.py, solver.py, ...
│   └── boundary/   input_validator.py, cli.py, display.py, gui.py
└── tests/
    ├── entity/
    ├── boundary/
    └── golden_master/
```

---

## 9. 다음 사용자 프롬프트 (P0 적용)

```
Report/12-code-review-report.md P0 항목을 적용하세요.
1. validate_grid() 성공 시 NOT_IMPLEMENTED 대신 None(또는 성공 타입)을 반환하고 cli.solve() 분기를 단순화하세요.
2. is_magic_square()에 _shape_valid()를 추가해 비정형 격자에서 IndexError 없이 False를 반환하세요.
run_tests.bat로 52 passed를 유지하세요.
```

---

## 10. 참조

| 문서 | 용도 |
|---|---|
| `.cursor/rules/magicsquare-forbidden.mdc` | 금지 패턴 5종 |
| `.cursor/rules/magicsquare-project.mdc` | Invariant Level 0~3 |
| `.cursor/rules/magicsquare-ecb-architecture.mdc` | generate/validate/display 분리 |
| `.cursor/agents/code-reviewer.md` | Code Reviewer 서브에이전트 정의 |
| `test_plan.md` | Track A/B 테스트 매핑 |
| `defect_list.md` | RED 단계 결함 (본 리뷰와 별도) |
