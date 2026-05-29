# Test Plan — F-1 Boundary Input Validation (Sample: grid = None)

| 항목 | 내용 |
|---|---|
| **문서 ID** | TP-MSQ-F1-001 |
| **버전** | 1.0 |
| **작성일** | 2026-05-29 |
| **기준 PRD** | `Report/09-product-requirements-document.md` |
| **샘플 AC** | AC-FR-01-01 (PRD AC-1-1 / US-01 선행 조건) |
| **대상 FR** | F-1 Boundary Input Validator (§6.2) |
| **RED Test ID** | RED-BND-VAL-004 (구조/크기 위반 계열) |
| **Scenario** | SC-BND-VAL-004 |

---

## 1. 목적

PRD **F-1**의 입력 유효성 검사 중, **가장 선행되는 구조 검증**(격자 존재·4×4 형태)을 RED 단계에서 먼저 고정한다.

본 플랜의 **샘플 예제**는 `grid = None` 입력 시 Boundary가 **실패 결과**를 반환하고 **Control(Solver) 진입점을 호출하지 않음**을 검증하는 것이다.

---

## 2. 범위

### 2.1 In Scope (본 RED 커밋)

| ID | 범위 |
|---|---|
| TP-01 | Boundary `InputValidator` / orchestrator의 **구조·크기** 선행 검증 |
| TP-02 | `grid = None` 및 **크기 불일치** 경계값 |
| TP-03 | 실패 결과 `{ code, message }` 계약 |
| TP-04 | Solver(`resolve` / `solve`) **0회 호출** mock/spy 검증 |

### 2.2 Out of Scope (본 RED 커밋 — 포함 금지)

| ID | 제외 항목 | PRD AC |
|---|---|---|
| OUT-01 | 빈칸 개수(0의 개수 ≠ 2) | AC-1-3 |
| OUT-02 | 셀 값 범위(0 미만, 17 이상) | AC-1-4 |
| OUT-03 | 0 제외 중복 숫자 | AC-1-5 |
| OUT-04 | **4×4 정상 입력 Happy Path** | AC-1-7 |
| OUT-05 | Control BlankFinder / MSN / Validator / Solver 로직 | F-2 ~ F-5 |

> **AC-FR-01-02 ~ AC-FR-01-05** (빈칸·범위·중복)는 **후속 RED 커밋**으로 분리한다.

---

## 3. 테스트 대상 (SUT)

| 레이어 | 모듈 (PRD §6.2) | 진입점 | 비고 |
|---|---|---|---|
| Boundary | `magic_square/boundary/input_validator.py` | `validate(grid) -> None` 또는 `validate_grid(grid) -> ValidationResult` | 구조 검증 선행 |
| Boundary | `magic_square/boundary/cli.py` (orchestrator) | `solve(grid) -> list[int]` | None 분기 시 Solver 미호출 |
| Control | `magic_square/control/solver.py` | `solve(grid) -> list[int]` | **mock 대상** — 호출 0회 |

**PRD 계약 매핑 (D-07):**

- 구조 위반 → `InputValidationError` (ValueError 하위)
- 본 테스트 플랜의 `{ code: "INVALID_SIZE", message: "..." }`는 Boundary **실패 결과 DTO**로 정의하며, 최종 구현에서 예외로 변환하거나 그대로 반환할 수 있다. **RED 테스트는 DTO 계약을 고정**한다.

---

## 4. 샘플 예제 (Anchor Case)

| 항목 | 값 |
|---|---|
| **AC ID** | AC-FR-01-01 |
| **PRD 매핑** | F-1 §6.2, US-01 AC-1-1, §6.1.1 Input Contract, §8.1 SC2 |
| **입력** | `grid = None` |
| **기대 출력** | `{ "code": "INVALID_SIZE", "message": "Grid must be 4x4." }` |
| **기대 부수 효과** | `solver.solve` 호출 횟수 = **0** |

---

## 5. pytest 단위 테스트 — 범위 및 우선순위

| 우선순위 | TC ID | 설명 | Track |
|---|---|---|---|
| **P0** | TC-A-01 | `grid=None` → 실패 결과 반환 | A |
| **P0** | TC-A-04 | `grid=None` → Solver 0회 호출 | A |
| **P0** | TC-A-02 | `code == "INVALID_SIZE"` (문자열 정확 일치) | A |
| **P0** | TC-A-03 | `message == "Grid must be 4x4."` (문자 단위 동일) | A |
| **P0** | TC-A-07 | 반환 타입이 지정 실패 결과 구조체/DTO | A |
| **P1** | TC-A-05 | `grid=[]` → INVALID_SIZE | A |
| **P1** | TC-A-06 | `grid=3×4` → INVALID_SIZE | A |
| **P1** | TC-B-01 | Control `solve(None)` 직접 호출 경로 격리 | B |
| **P1** | TC-B-02 | Boundary None 분기 후 resolve 미호출 | B |
| **P1** | TC-B-03 | mock 호출 시 테스트 **실패** (assert) | B |
| **P2** | TC-A-08 | `grid=[[]]*4` (행 4, 열 0) → INVALID_SIZE | A |
| **P2** | TC-A-09 | `grid=4×3` → INVALID_SIZE | A |
| **P2** | TC-A-10 | `grid=5×5` → INVALID_SIZE | A |

### Track A — Boundary (UI / 입출력 격리)

- **파일:** `tests/boundary/test_input_validator.py`, `tests/boundary/test_solve_orchestrator.py`
- **패턴:** AAA (Arrange-Act-Assert), 1 test = 1 behavior
- **명명:** `test_<상황>_<기대결과>`

### Track B — Domain / Logic (격리 확인)

- Control 모듈은 **아직 GREEN 대상 아님**
- `unittest.mock.patch` / `pytest-mock` `mocker.spy`로 **호출 여부만** 검증
- Track B는 “Boundary가 Control을 보호한다”(L3-4, AC-1-6)는 **설계 불변** 검증

---

## 6. 경계값 케이스 목록

| # | 입력 | 기대 code | 기대 message (요약) | 비고 |
|---|---|---|---|---|
| BV-01 | `grid = None` | `INVALID_SIZE` | `Grid must be 4x4.` | **Anchor — P0** |
| BV-02 | `grid = []` | `INVALID_SIZE` | `Grid must be 4x4.` | 행 0 |
| BV-03 | `grid = [[]] * 4` | `INVALID_SIZE` | `Grid must be 4x4.` | 행 4, 열 0 |
| BV-04 | `grid = 3×4` | `INVALID_SIZE` | `Grid must be 4x4.` | 행 부족 |
| BV-05 | `grid = 4×3` | `INVALID_SIZE` | `Grid must be 4x4.` | 열 부족 |
| BV-06 | `grid = 5×5` | `INVALID_SIZE` | `Grid must be 4x4.` | 초과 |
| — | `grid = 4×4` 정상 | *(본 커밋 제외)* | — | **OUT-04** |

**4×4 정상 격자 예시 (참고용 — 테스트 작성 금지):**

```text
[[16, 2, 3, 13],
 [5, 11, 10, 8],
 [9, 7, 0, 12],
 [4, 14, 15, 0]]
```

---

## 7. 예외 / 특이 케이스 목록

| ID | 케이스 | 기대 동작 | 우선순위 |
|---|---|---|---|
| EX-01 | `grid`가 `list`가 아닌 타입 (`str`, `dict`, `int`) | `INVALID_SIZE` 또는 PRD D-07 `TypeError` — **후속 AC에서 통일**; 본 커밋은 `None`만 P0 | P2 |
| EX-02 | `grid` 내부 행이 `list`가 아님 (`[1,2,3,4]*4` 혼합) | `INVALID_SIZE` | P2 |
| EX-03 | `grid`가 `numpy.ndarray` 등 duck-type | 본 프로젝트 v1 **비범위** — list only | Won't |
| EX-04 | Validator가 예외 대신 Result 반환 vs raise — API 스타일 | RED는 **Result DTO** 고정; GREEN에서 `InputValidationError` raise 허용 if message/code 동일 | P1 |
| EX-05 | `solve()` mock이 **의도적 호출**된 테스트 | `pytest.fail` 또는 `assert not mock.called` | P0 |

---

## 8. Domain 진입점 호출 횟수 검증 전략

### 8.1 Mock / Spy 대상

| Symbol | 패치 경로 (예시) | 검증 |
|---|---|---|
| `solve` | `magic_square.boundary.cli.solve` 내부에서 참조하는 `magic_square.control.solver.solve` | `call_count == 0` |
| `resolve` | orchestrator 별칭 사용 시 동일 | `call_count == 0` |

### 8.2 패턴 (의사 코드 — RED 작성 시 참고)

```text
Arrange:
  grid = None
  spy = mocker.patch("magic_square.control.solver.solve")

Act:
  result = orchestrator.solve(grid)   # 또는 validate_and_solve

Assert:
  result.code == "INVALID_SIZE"
  result.message == "Grid must be 4x4."
  spy.call_count == 0
```

### 8.3 실패 정의

- Boundary 검증 **전** Solver가 1회라도 호출되면 **테스트 실패** (AC-1-6, L3-4 위반).
- Track B-03: spy가 호출된 상태를 **의도적으로 허용하는 테스트**는 작성하지 않는다.

---

## 9. 커버리지 목표

| 범위 | 목표 | PRD 근거 |
|---|---|---|
| **Control (Domain Logic)** | **≥ 95%** | PRD §8.2 SC1, D-05 |
| **Boundary** | **≥ 85%** | 본 테스트 플랜 (Boundary 선행 RED) |
| **프로젝트 전체** | **≥ 90%** | README RED 체크리스트 |

> v1 PRD 전체 최소 80%와 병행; **본 RED 스프린트**는 Boundary 집중으로 Boundary 85%+를 먼저 달성한다.

---

## 10. pytest-cov 측정 전략

### 10.1 설치

```bash
pip install pytest pytest-cov pytest-mock
```

### 10.2 실행 (프로젝트 패키지 경로)

```bash
pytest tests/boundary/ -v --cov=magic_square/boundary --cov=magic_square/control --cov-report=term-missing
```

### 10.3 전체 측정

```bash
pytest --cov=magic_square --cov-report=term-missing --cov-report=html
```

### 10.4 RED 단계 게이트

| 게이트 | 조건 |
|---|---|
| G-RED-1 | 샘플 TC-A-01 ~ TC-A-04 **FAILED** (구현 없음 또는 NotImplemented) |
| G-RED-2 | 실패 원인이 **Assertion/NotImplemented**이며 ImportError가 아님 |
| G-GREEN-1 | 동일 TC **PASSED** + spy 0회 유지 |
| G-COV-1 | Boundary 모듈 line coverage ≥ 85% |

---

## 11. Traceability

| PRD | Test Plan | RED TC |
|---|---|---|
| F-1 §6.2 | §4 Anchor | TC-A-01 |
| US-01 AC-1-1 | §6 BV-01~06 | TC-A-05, TC-A-06, TC-A-08~10 |
| US-01 AC-1-6 | §8 | TC-A-04, TC-B-02, TC-B-03 |
| L3-4 | §8 | TC-A-04 |
| SC-BND-VAL-004 | §4 | TC-A-01 |
| §8.1 SC2 | §9 | Boundary 85%+ |

---

## 12. 결함 관리

- 발견 결함은 **`defect_list.md`**에 기록 (ID, TC, 재현, 기대/실제, 상태).
- 결함 수정 후 **동일 TC + 회귀 스위트** 재실행.
- AC-FR-01-02~05 범위 결함은 **본 스프린트 결함으로 분류하지 않음** (범위 외).

---

## 13. 승인 기준 (본 Test Plan Done)

- [ ] Anchor TC-A-01 ~ TC-A-04 RED 작성 완료
- [ ] BV-01 ~ BV-06 중 P0/P1 케이스 RED 작성
- [ ] Solver spy 0회 검증 통과 (GREEN 후)
- [ ] Boundary coverage ≥ 85%
- [ ] `defect_list.md` 운영 시작
- [ ] README RED 체크리스트와 TC ID 일치

---

## 참고

- PRD: `Report/09-product-requirements-document.md`
- User Journey Scenario: `Report/07-user-journey.md` SC-BND-VAL-004
- Engineering Rules: `.cursorrules`, `.cursor/rules/magicsquare-tdd-testing.mdc`
