# 4×4 Magic Square

> 구현보다 먼저, 정의가 있다.

---

## 프로젝트 개요

이 프로젝트는 4×4 마방진(Magic Square) 프로그램을 개발하기 위한 작업 저장소입니다.
단, 이 프로젝트는 **"마방진을 만드는 것"을 목적으로 하지 않습니다.**

진짜 목적은 다음과 같습니다.

> **4×4 격자 위에서, 1부터 16까지의 자연수를 중복 없이 배치하였을 때,
> 모든 행(4개), 모든 열(4개), 두 대각선(2개)의 합이 동일한 값(Magic Constant = 34)을
> 만족하는 상태가 존재하는가를 판단하고,
> 그 상태를 생성·검증·표현하는 각각의 책임을 명확히 분리하여 다룰 수 있는가.**

---

## 문제 정의 프로세스

이 프로젝트는 구현에 앞서 **5단계의 문제 인식 프로세스**를 완료하였습니다.

| 단계 | 이름 | 핵심 질문 | 핵심 발견 |
|---|---|---|---|
| STEP 1 | Observation | 현재 상황은 무엇인가? | 제약 조건이 강한 배치 문제. 탐색 공간 16! ≈ 2×10¹³ |
| STEP 2 | Why #1 | 왜 마방진을 완성해야 하는가? | "완성"은 성공 기준, 검증 책임, 해 공간을 은폐한다 |
| STEP 3 | Why #2 | 왜 프로그램으로 구현하는가? | 반복 가능성·검증 자동화·오류 방지·규칙 기반 사고 |
| STEP 4 | Why #3 | 왜 TDD 방식으로 설계하는가? | 불변 조건을 먼저 선언하고 이해를 증명하기 위해서 |
| STEP 5 | 문제 정의 | 진짜 문제는 무엇인가? | 생성·검증·표현의 책임 분리, 10가지 조건의 완전한 열거 |

---

## 핵심 불변 조건 (Invariants)

마방진의 불변 조건은 4개 레벨의 계층 구조를 이룹니다.

### Level 0 — 구성 불변 조건 (전제)
- 격자는 정확히 **4행 4열**, 총 **16칸**으로 구성된다.
- 사용 숫자는 **1 이상 16 이하의 자연수**이며, 각 숫자는 **정확히 한 번만** 등장한다.

### Level 1 — 합산 불변 조건 (정의)
- **4개의 행** 각각의 합 = **34**
- **4개의 열** 각각의 합 = **34**
- **주 대각선** (좌상 → 우하) 의 합 = **34**
- **반 대각선** (우상 → 좌하) 의 합 = **34**
- 이 네 조건은 **서로 독립**이다. 각각 별도로 성립해야 한다.

### Level 2 — 파생 불변 조건 (유도)
- Magic Constant = **n(n² + 1) / 2**
- 4×4의 경우: **4 × (16 + 1) / 2 = 34**
- 34는 격자 크기 n이 결정되는 순간 **유일하게 결정**된다.

### Level 3 — 설계 불변 조건 (분리)
- **생성(Generation)** 과 **검증(Validation)** 은 서로 독립적이어야 한다.
- **검증**은 생성 방식을 알지 못해야 한다.
- **표현(Representation)** 은 생성과 검증 어느 쪽도 의존하지 않는다.

---

## 훈련 목표

이 프로젝트를 통해 훈련하려는 사고 능력은 다음과 같습니다.

| 사고 능력 | 내용 |
|---|---|
| 조건의 완전한 열거 | 행뿐 아니라 열·대각선·중복·범위까지 빠짐없이 |
| 불변 조건의 선언 | "어떻게 만들까"보다 "무엇이 참이어야 하는가"를 먼저 |
| 책임의 분리 | 생성·검증·표현을 독립된 관심사로 다루기 |
| 표면과 본질의 구분 | "만든다"와 "판단한다"의 차이를 인식하기 |
| 성공 기준의 사전 정의 | 시작 전에 완성 기준을 먼저 선언하기 |

---

## 프로젝트 구조

```
MagicSquare_/
├── README.md
├── pyproject.toml
├── .cursorrules                       ← ECB · Dual-Track TDD · 코드 스타일
│
├── magic_square/                      ← ECB 패키지 (Python 3.10+)
│   ├── boundary/                      ← 외부 입출력 (CLI, 입력 검증, DTO)
│   │   ├── cli.py
│   │   ├── input_validator.py
│   │   └── models.py
│   ├── control/                       ← 유즈케이스 조율 (Solver 등)
│   └── entity/                        ← 도메인 객체·상수
│
├── tests/
│   ├── boundary/                      ← Track A: UI/Boundary 계약
│   │   ├── test_ac_fr_01_01_input_size_validation.py   (R1, 9건)
│   │   ├── test_u_in_04_08_input_validation.py         (R2, 5건)
│   │   ├── test_u_flow_02_domain_isolation.py          (R3, 4건)
│   │   └── test_u_out_01_03_output_contract.py         (R4, 3건)
│   └── entity/                        ← Track B: Domain/Logic
│       ├── test_d_loc_01_blank_finder.py               (R5, 1건)
│       ├── test_d_mis_01_missing_numbers.py            (R6, 1건)
│       ├── test_d_val_01_06_validator.py               (R7, 6건)
│       └── test_d_sol_01_04_solver.py                  (R8, 4건)
│
├── Report/                            ← 문제 정의 · PRD · TDD 설계 보고서
└── Prompt/                            ← 설계 대화 트랜스크립트
```

### Dual-Track TDD

| Track | 레이어 | 범위 | 테스트 접두 |
|---|---|---|---|
| **A** | Boundary | 입력 검증 · 격리 · 출력 계약 | `U-IN-*`, `U-FLOW-*`, `U-OUT-*`, `AC-FR-*` |
| **B** | Entity/Control | BlankFinder · Validator · Solver | `D-LOC-*`, `D-MIS-*`, `D-VAL-*`, `D-SOL-*` |

---

## 현재 진행 상태

```
[완료] STEP 1~5  문제 정의 · Invariant 확정
[완료] STEP 6~8  Test List · Python/pytest · ECB 설계
[진행] STEP 9    Dual-Track TDD — RED 커밋 묶음 → GREEN 1건씩 최소 구현

  AC-FR-01-01 (R1): G01~G09 GREEN 완료 (9 passed)
  R2~R4: GREEN 완료 (Track A 입력·격리·출력)
  R5~R8: GREEN 완료 (Track B Entity/Control)
```

---

## TDD RED 커밋 묶음 (권장)

RED 단계는 아래 단위로 커밋하고, GREEN은 **오름차순 1건(또는 동일 구현 묶음)씩** 처리한다.

| RED 커밋 | 테스트 파일 | 건수 | AC / Test ID | 비고 |
|---|---|---|---|---|
| **R1** | `tests/boundary/test_ac_fr_01_01_input_size_validation.py` | 9 | AC-FR-01-01, U-IN-01~03 | 현재 워크스페이스에 존재 |
| **R2** | `tests/boundary/test_u_in_04_08_input_validation.py` | 5 | AC-FR-01-02~04, U-IN-04~08 | blank·범위·중복 |
| **R3** | `tests/boundary/test_u_flow_02_domain_isolation.py` | 4 | U-FLOW-02, AC-1-6 | R1 #09와 null 중복 |
| **R4** | `tests/boundary/test_u_out_01_03_output_contract.py` | 3 | AC-FR-05-03, U-OUT-01~03 | RED는 선행, GREEN은 Solver 이후 |
| **R5** | `tests/entity/test_d_loc_01_blank_finder.py` | 1 | D-LOC-01, FR-02 | |
| **R6** | `tests/entity/test_d_mis_01_missing_numbers.py` | 1 | D-MIS-01, FR-03 | |
| **R7** | `tests/entity/test_d_val_01_06_validator.py` | 6 | D-VAL-01~06, FR-04 | |
| **R8** | `tests/entity/test_d_sol_01_04_solver.py` | 4 | D-SOL-01~04, FR-05 | |

**총 RED: 33건** (Track A 21 + Track B 12)

RED 커밋 권장 순서: **R1 → R2 → R3 → (R5, R6, R7, R8) → R4**

---

## TDD GREEN 처리 순서 (오름차순)

의존성 원칙: **입력 검증 → 격리 → Entity 기초 → Validator → Solver → 출력**

### Phase 1 — FR-01 크기 검증 (`test_ac_fr_01_01_*`, R1)

| G# | Test ID | 대상 테스트 | 구현 포인트 | 상태 |
|---|---|---|---|---|
| G01 | U-IN-01 | `test_none_grid_returns_invalid_size_code` | `validate_grid`: `grid is None` | GREEN |
| G02 | U-IN-01 | `test_none_grid_returns_invalid_size_message` | (G01과 동일) | GREEN |
| G03 | U-IN-01 | `test_none_grid_message_matches_prd_section_8_1_character_for_character` | (G01과 동일) | GREEN |
| G04 | U-IN-01 | `test_none_grid_failure_code_is_invalid_size_not_out_of_scope_codes` | (G01과 동일) | GREEN |
| G05 | — | `test_red_scope_permits_only_invalid_size_failure_code` | 구현 불필요 (메타) | 항상 통과 |
| G06 | U-IN-02d | `test_size_mismatch_grid_returns_invalid_size[empty_list]` | 4×4 크기 검사 | GREEN |
| G07 | U-IN-02a | `test_size_mismatch_grid_returns_invalid_size[four_rows_zero_cols]` | (G06과 동일) | GREEN |
| G08 | U-IN-02b | `test_size_mismatch_grid_returns_invalid_size[three_by_four]` | (G06과 동일) | GREEN |
| G09 | U-FLOW-02 | `test_none_grid_resolve_spy_called_zero_times` | `cli.solve`: validate 선행, 실패 시 `resolve` 미호출 | GREEN |

> **실무 팁:** G01~G05는 1커밋, G06~G08은 1커밋, G09는 1커밋으로 묶어도 TDD 원칙에 맞다.

```bash
# G06~G08 (한 커밋 권장)
python -m pytest tests/boundary/test_ac_fr_01_01_input_size_validation.py::TestAcFr0101BoundarySizeInputs -v

# G09 (별도 커밋 — cli.py 수정)
python -m pytest tests/boundary/test_ac_fr_01_01_input_size_validation.py::TestAcFr0101DomainIsolation::test_none_grid_resolve_spy_called_zero_times -v
```

### Phase 2 — FR-01 추가 입력 검증 (`test_u_in_04_08_*`, R2)

| G# | Test ID | AC | 대상 테스트 |
|---|---|---|---|
| G10 | U-IN-04 | AC-FR-01-02 | `test_u_in_04_zero_blanks_returns_e002` |
| G11 | U-IN-05 | AC-FR-01-02 | `test_u_in_05_three_blanks_returns_e002` |
| G12 | U-IN-06 | AC-FR-01-03 | `test_u_in_06_negative_value_returns_e004` |
| G13 | U-IN-07 | AC-FR-01-03 | `test_u_in_07_value_17_returns_e004` |
| G14 | U-IN-08 | AC-FR-01-04 | `test_u_in_08_nonzero_duplicate_returns_e005` |

### Phase 3 — 격리 확장 (`test_u_flow_02_*`, R3)

| G# | Test ID | 대상 테스트 | 선행 GREEN |
|---|---|---|---|
| G15 | U-FLOW-02 | `test_u_flow_02_null_matrix_resolve_spy_zero_calls` | G09 |
| G16 | U-FLOW-02 | `test_u_flow_02_e002_blank_count_resolve_spy_zero_calls` | G10~G11 |
| G17 | U-FLOW-02 | `test_u_flow_02_e004_value_range_resolve_spy_zero_calls` | G12~G13 |
| G18 | U-FLOW-02 | `test_u_flow_02_e005_duplicate_resolve_spy_zero_calls` | G14 |

### Phase 4 — Domain Entity/Control (`tests/entity/*`, R5~R8)

| G# | Test ID | FR | 대상 테스트 |
|---|---|---|---|
| G19 | D-LOC-01 | FR-02 | `test_d_loc_01_find_blank_coords_g1_row_major_0_index` |
| G20 | D-MIS-01 | FR-03 | `test_d_mis_01_find_not_exist_nums_g1_sorted` |
| G21 | D-VAL-01 | FR-04 | `test_d_val_01_is_magic_square_g0_complete_true` |
| G22 | D-VAL-02 | FR-04 | `test_d_val_02_is_magic_square_row_sum_mismatch_false` |
| G23 | D-VAL-03 | FR-04 | `test_d_val_03_is_magic_square_col_sum_mismatch_false` |
| G24 | D-VAL-04 | FR-04 | `test_d_val_04_is_magic_square_diagonal_mismatch_false` |
| G25 | D-VAL-05 | FR-04 | `test_d_val_05_is_magic_square_duplicate_nonzero_false` |
| G26 | D-VAL-06 | FR-04 | `test_d_val_06_is_magic_square_contains_zero_false` |
| G27 | D-SOL-01 | FR-05 | `test_d_sol_01_solution_g1_step_a_success` |
| G28 | D-SOL-02 | FR-05 | `test_d_sol_02_solution_g2_step_a_fail_step_b_success` |
| G29 | D-SOL-03 | FR-05 | `test_d_sol_03_solution_g3_both_steps_fail` |
| G30 | D-SOL-04 | FR-05 | `test_d_sol_04_solution_output_shape_1_index_coords` |

### Phase 5 — Boundary 출력 (`test_u_out_01_03_*`, R4)

| G# | Test ID | AC | 대상 테스트 | 선행 GREEN |
|---|---|---|---|---|
| G31 | U-OUT-01 | AC-FR-05-03 | `test_u_out_01_success_result_length_is_six` | G27 |
| G32 | U-OUT-02 | I11 | `test_u_out_02_success_coordinates_are_1_index_in_range` | G27 |
| G33 | U-OUT-03 | I7+I11 | `test_u_out_03_success_fill_values_match_missing_numbers` | G27 |

### RED → GREEN 매핑 요약

```
R1 (9)  → G01~G09   ← 현재 위치 (G01~G05 완료, G06~G09 잔여)
R2 (5)  → G10~G14
R3 (4)  → G15~G18
R4 (3)  → G31~G33   ※ RED는 먼저, GREEN은 Solver(G27) 이후
R5 (1)  → G19
R6 (1)  → G20
R7 (6)  → G21~G26
R8 (4)  → G27~G30
```

### GREEN 단계 규칙

- **한 GREEN 커밋 = 한 테스트(또는 동일 분기 묶음)만** 통과시키는 최소 구현
- REFACTOR·설계 개선·다른 AC 선행 구현 금지 (`.cursorrules` green_phase)
- AC-FR-01-01 실패 계약: `code="INVALID_SIZE"`, `message="Grid must be 4x4."` (문자 단위 동일)

---

## 앞으로의 계획 (로드맵)

### 마일스톤

| 단계 | 목표 | 완료 기준 | 상태 |
|---|---|---|---|
| **M0** | RED 설계 확정 | Dual-Track 33건 Test ID · AC 매핑 · G1/G2/G3 fixture 정의 | ✅ |
| **M1** | RED 커밋 | R1~R8 테스트 파일 커밋, 전체 FAILED 확인 | 🔄 R1만 존재 |
| **M2** | GREEN — FR-01 | G01~G18 통과 (입력 검증 + 격리) | ✅ |
| **M3** | GREEN — FR-02~04 | G19~G26 통과 (Blank · Missing · Validator) | ✅ |
| **M4** | GREEN — FR-05 | G27~G30 통과 (Solver) | ✅ |
| **M5** | GREEN — 출력 계약 | G31~G33 통과 (U-OUT) | ✅ |
| **M6** | REFACTOR | ECB 경계 정리 · Error code SSOT 통일 · coverage ≥ 80% | ⬜ |
| **M7** | 통합 · 문서 | 전체 pytest GREEN · PRD diff 0 · README/Report 동기화 | ⬜ |

### 스프린트 흐름 (반복 패턴)

```
RED 커밋 (R#)  →  pytest FAILED 확인  →  GREEN 1건씩 (G##)  →  pytest 해당 건 PASSED
                                                              ↓
                                              REFACTOR (M6 이후, 외부 동작 불변)
```

### 브랜치 전략 (권장)

| 브랜치 | 용도 |
|---|---|
| `feature/dual-track-tdd` | RED 테스트 추가·설계 |
| `stabilize/green` | GREEN 최소 구현 (1 G# 또는 동일 분기 묶음당 1커밋) |
| `develop` | M2~M5 완료 후 merge |

---

## To-do List

진행 상태: `[x]` 완료 · `[~]` 진행 중 · `[ ]` 대기

### A. RED 커밋 (테스트 먼저)

- [x] **R1** — `test_ac_fr_01_01_input_size_validation.py` (9건, AC-FR-01-01)
- [x] **R2** — `test_u_in_04_08_input_validation.py` (5건, AC-FR-01-02~04)
- [x] **R3** — `test_u_flow_02_domain_isolation.py` (4건, U-FLOW-02)
- [x] **R4** — `test_u_out_01_03_output_contract.py` (3건, U-OUT-01~03)
- [x] **R5** — `test_d_loc_01_blank_finder.py` (1건, D-LOC-01)
- [x] **R6** — `test_d_mis_01_missing_numbers.py` (1건, D-MIS-01)
- [x] **R7** — `test_d_val_01_06_validator.py` (6건, D-VAL-01~06)
- [x] **R8** — `test_d_sol_01_04_solver.py` (4건, D-SOL-01~04)
- [x] `tests/conftest.py` — G0/G1/G2/G3 fixture 공유 (R2·R5~R8 선행)

### B. GREEN — Phase 1: FR-01 크기·격리 (R1, G01~G09)

- [x] **G01~G05** — `grid is None` → `INVALID_SIZE` / `"Grid must be 4x4."`
- [x] **G06~G08** — 4×4 크기 검사 (`[]`, 4×0, 3×4) → `input_validator.py`
- [x] **G09** — `cli.solve`: validate 실패 시 `resolve()` 미호출 → `cli.py`

### C. GREEN — Phase 2: FR-01 추가 입력 (R2, G10~G14)

- [x] **G10** — 빈칸 0개(G0) → E002
- [x] **G11** — 빈칸 3개 → E002
- [x] **G12** — 음수(-1) → E004
- [x] **G13** — 17 → E004
- [x] **G14** — non-zero 중복 → E005

### D. GREEN — Phase 3: 격리 확장 (R3, G15~G18)

- [x] **G15** — null 입력 시 resolve 0회 (G09와 중복 검증)
- [x] **G16** — E002 경로 resolve 0회
- [x] **G17** — E004 경로 resolve 0회
- [x] **G18** — E005 경로 resolve 0회

### E. GREEN — Phase 4: Domain Logic (R5~R8, G19~G30)

- [x] **G19** — `find_blank_coords(G1)` → `[(1,2),(3,3)]` (0-index)
- [x] **G20** — `find_not_exist_nums(G1)` → `[7, 10]`
- [x] **G21** — `is_magic_square(G0)` → `True`
- [x] **G22** — 행 합 불일치 → `False`
- [x] **G23** — 열 합 불일치 → `False`
- [x] **G24** — 대각선 불일치 → `False`
- [x] **G25** — non-zero 중복 → `False`
- [x] **G26** — 0 포함 완성 격자 → `False`
- [x] **G27** — `solution(G1)` → `[2,2,7,3,3,10]`
- [x] **G28** — G2 Step B fallback
- [x] **G29** — G3 `UnsolvableDomainError`
- [x] **G30** — 출력 shape (len 6, 1-index coords)

### F. GREEN — Phase 5: Boundary 출력 (R4, G31~G33)

- [x] **G31** — 성공 시 `len(result) == 6`
- [x] **G32** — r,c 1-index, 범위 [1,4]
- [x] **G33** — n1, n2 = missing numbers {7, 10}

### G. REFACTOR (M6 — GREEN 전체 완료 후)

- [ ] Error code SSOT 통일 (`INVALID_SIZE` vs `E001`/`E003` → PRD v0.2 기준)
- [ ] `input_validator.py` — 크기·blank·범위·중복 검사 함수 분리
- [ ] `cli.py` — validate → resolve 단방향 흐름 정리
- [ ] Entity `constants.py` — `GRID_SIZE`, `MAGIC_CONSTANT` 하드코딩 제거
- [ ] pytest coverage ≥ 80% 확인
- [ ] RED stub (`NOT_IMPLEMENTED`, `pytest.fail`) 잔여 제거

### H. 통합 · 문서 (M7)

- [ ] 전체 `pytest` GREEN (33건 + entity smoke)
- [ ] `Report/09` PRD §Error와 코드·메시지 diff 0 검증
- [ ] README 진행 상태 · To-do 체크리스트 갱신
- [ ] `develop` merge · CI (있을 경우) 통과

---

## 지금 바로 할 일 (Next Actions)

| 우선순위 | 작업 | 명령 / 파일 |
|---|---|---|
| **1** | REFACTOR (M6) | Error code SSOT · coverage ≥ 80% |
| **2** | 통합 확인 | `pytest tests/boundary/ tests/entity/test_d_*.py -v` |

**현재 테스트 현황:** 33 passed · 0 failed (Dual-Track GREEN 완료)

---

## 참고

- **Magic Constant 계산**: n×n 마방진에서 합 = n(n²+1)/2
- **4×4 해의 수**: 880개 (회전·반사 동치류 제외 시)
- **탐색 공간**: 16! = 20,922,789,888,000 ≈ 2.09 × 10¹³
