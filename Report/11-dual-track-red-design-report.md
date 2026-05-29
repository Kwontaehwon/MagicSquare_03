# 4×4 Magic Square — Dual-Track RED 설계 보고서

**작성일**: 2026-05-29  
**단계**: TDD RED — FR-01~FR-05 전체 Dual-Track 설계표 (코드·테스트 미작성)  
**TDD phase**: **RED** (설계만, GREEN/REFACTOR 미진입)  
**선행 산출물**: `Report/09-product-requirements-document.md`, `Report/07-user-journey.md`, `.cursorrules`  
**대화 재현**: `Prompt/08-dual-track-red-design-conversation-transcript.md`  
**목적**: Boundary(UI) Track과 Domain(Logic) Track의 RED 테스트 설계표를 SSOT 계약에 맞춰 통합 기록한다.

---

## 0. 본 보고서의 범위

| 구분 | 위치 |
|---|---|
| RED 설계표 (본문) | §3~§4 |
| 격자 부록 G0~G3 | §2 |
| Error envelope (E00x) | §1.3 |
| 대화 트랜스크립트 | `Prompt/08-dual-track-red-design-conversation-transcript.md` |
| 본 보고서 | `Report/11-dual-track-red-design-report.md` |

**범위 밖:** pytest 코드, 구현·스켈레톤, 파일 구조 확정, GREEN/REFACTOR

### SSOT 참고 상태

| 문서 | 상태 |
|---|---|
| `docs/PRD_MagicSquare.md` v0.2 | 워크스페이스 **미존재** — 요청 계약(E00x·U-*·D-*·I*)을 1차 SSOT로 사용 |
| `Report/02.MagicSquare_DualTrack_TDD_Design_Report.md` | **미존재** — `Report/02-tdd-design-prompt-report.md`만 존재 |
| `.cursorrules` | ECB, Dual-Track, AAA, coverage 규칙 적용 |
| `Report/09`, `Report/07` | G2 surrogate(SC-DOM-SOL-001), AC-FR 매핑 2차 참조 |

---

## 1. 프로젝트 계약 요약

### 1.1 입출력

| 항목 | 명세 |
|---|---|
| 입력 | 4×4 `int[][]`, `0`=빈칸(정확히 2개), 값 ∈ `{0}∪{1..16}`, non-zero 중복 금지 |
| 출력 | `int[6]` = `[r1,c1,n1,r2,c2,n2]`, 좌표 **1-index** |
| Magic Constant | M = 34 = `n(n²+1)/2`, n=4 — `MagicConstant` SSOT, 리터럴 `34` 금지 |

### 1.2 검증 순서 (short-circuit)

`null` → `size` → `empty count` → `value range` → `duplicate`

### 1.3 Boundary Failure Envelope (Python 예외 아님)

| code | message (설계 고정안 — GREEN 시 PRD v0.2와 diff 0 맞출 것) |
|---|---|
| E003 | `Input matrix must not be null.` |
| E001 | `Grid must be 4x4.` |
| E002 | `Exactly two blank cells (0) are required.` |
| E004 | `Each cell must be 0 or an integer from 1 to 16.` |
| E005 | `Non-zero cell values must not duplicate.` |

**흐름 격리:** invalid 입력 시 `SolvePartialMagicSquare.execute` **call_count == 0** (U-FLOW-02, L3-4)

### 1.4 Logic Track 규칙

- Entity/Control 단위 검증
- **Domain Mock 금지** (Boundary U-OUT만 `execute` stub/spy 허용)

---

## 2. 격자 부록 G0~G3

| ID | 용도 | 4×4 `int[][]` (0-index) | 비고 |
|---|---|---|---|
| **G0** | 완전 마방진 | `[[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]]` | 행·열·대각선 합 = M |
| **G1** | Step A 성공 | `[[16,2,3,13],[5,11,0,8],[9,1,6,12],[4,14,15,0]]` | 0@(2,2),(3,3); 누락 `{7,10}`; 기대 `[2,2,7,3,3,10]` |
| **G2** | Step A실패→B성공 | `[[16,2,3,13],[5,11,10,8],[9,7,0,12],[4,14,15,0]]` | `07` SC-DOM-SOL-001 surrogate; 기대 `[3,3,6,4,4,1]` |
| **G3** | 양 조합 실패 | `[[8,1,0,6],[0,5,7,2],[3,0,4,5],[9,11,12,13]]` | **placeholder** — GREEN 시 양 배치 모두 M≠34 검증 필요 |

---

## 3. Track A — Boundary / UI Contract RED

| Test ID | Layer | 테스트 이름 | Given | When | Then | Expected RED Failure | Boundary 계약 |
|---|---|---|---|---|---|---|---|
| U-IN-01 | Boundary | `test_null_matrix_returns_E003` | `matrix=null` | `InputValidator.validate(matrix)` | `code=E003`, message exact | ModuleNotFound / AttributeError / assertion | AC-FR-01-01, short-circuit ① |
| U-IN-02a | Boundary | `test_non_4x4_row_count_returns_E001` | 3×4 행렬 | `InputValidator.validate(matrix)` | `code=E001` | 동일 | AC-1-1 |
| U-IN-02b | Boundary | `test_non_4x4_col_count_returns_E001` | 4×3 행렬 | `InputValidator.validate(matrix)` | `code=E001` | 동일 | AC-1-2 |
| U-IN-02c | Boundary | `test_oversize_matrix_returns_E001` | 5×5 | `InputValidator.validate(matrix)` | `code=E001` | 동일 | AC-FR-01-01 |
| U-IN-02d | Boundary | `test_empty_matrix_returns_E001` | `[]` | `InputValidator.validate(matrix)` | `code=E001` | 동일 | AC-FR-01-01 |
| U-IN-03a | Boundary | `test_zero_blanks_returns_E002` | G0 (빈칸 0개) | `InputValidator.validate(matrix)` | `code=E002` | assertion / 미구현 | AC-FR-01-02 |
| U-IN-03b | Boundary | `test_three_blanks_returns_E002` | 0이 3칸 | `InputValidator.validate(matrix)` | `code=E002` | 동일 | AC-FR-01-02 |
| U-IN-04a | Boundary | `test_negative_value_returns_E004` | 셀 `-1` | `InputValidator.validate(matrix)` | `code=E004` | 동일 | AC-FR-01-03 |
| U-IN-04b | Boundary | `test_value_17_returns_E004` | 셀 `17` | `InputValidator.validate(matrix)` | `code=E004` | 동일 | AC-FR-01-03 |
| U-IN-05 | Boundary | `test_nonzero_duplicate_returns_E005` | non-zero 중복 | `InputValidator.validate(matrix)` | `code=E005` | 동일 | AC-FR-01-04 |
| U-OUT-01 | Boundary | `test_success_result_length_is_six` | G1 + execute stub | `UIBoundary.solve(G1)` | `len(result)==6` | AssertionError / 미구현 | U-OUT-01, AC-FR-05-03 |
| U-OUT-02 | Boundary | `test_success_coordinates_are_1_index_in_range` | G1 + stub `[2,2,7,3,3,10]` | `UIBoundary.solve(G1)` | r,c ∈ [1,4]; n1=7,n2=10 | assertion fail | U-OUT-02, I11 |
| U-FLOW-02 | Boundary | `test_invalid_input_never_calls_execute` | `matrix=null`, execute spy | `UIBoundary.solve(matrix)` | `execute.call_count==0` | AssertionError (1회 호출) | U-FLOW-02, AC-1-6, L3-4 |

**Track A 건수:** 14건 (U-IN 10 + U-OUT 2 + U-FLOW 1)

---

## 4. Track B — Domain / Logic RED

| Test ID | Layer | 테스트 이름 | Given | When | Then | Expected RED Failure | Invariant |
|---|---|---|---|---|---|---|---|
| D-LOC-01 | Control | `test_find_blank_coords_G1_row_major_0_index` | G1 | `find_blank_coords(matrix)` | `[(2,2),(3,3)]` 0-index | ImportError / NotImplemented | I6 |
| D-MIS-01 | Control | `test_find_not_exist_nums_G1_sorted` | G1 | `find_not_exist_nums(matrix)` | `[7,10]` | 동일 | I7 |
| D-VAL-01 | Control | `test_is_magic_square_G0_complete_true` | G0 | `is_magic_square(matrix)` | `True` (M 경유) | False / 미구현 | I1~I5 |
| D-VAL-02 | Control | `test_is_magic_square_row_sum_mismatch_false` | G0 변형(행 깨짐) | `is_magic_square(matrix)` | `False` | assertion True | I1 |
| D-VAL-03 | Control | `test_is_magic_square_col_sum_mismatch_false` | G0 변형(열 깨짐) | `is_magic_square(matrix)` | `False` | assertion True | I2 |
| D-VAL-04 | Control | `test_is_magic_square_diagonal_mismatch_false` | G0 변형(대각 깨짐) | `is_magic_square(matrix)` | `False` | assertion True | I3 |
| D-VAL-05 | Control | `test_is_magic_square_duplicate_nonzero_false` | non-zero 중복 | `is_magic_square(matrix)` | `False` | assertion True | I4 |
| D-VAL-06 | Control | `test_is_magic_square_contains_zero_false` | G0+0 삽입 | `is_magic_square(matrix)` | `False` | assertion True | I4 |
| D-SOL-01 | Control | `test_solution_G1_step_A_success` | G1 | `solution(matrix)` | `[2,2,7,3,3,10]` | NotImplemented / wrong | I8 |
| D-SOL-02 | Control | `test_solution_G2_step_A_fail_step_B_success` | G2 | `solution(matrix)` | `[3,3,6,4,4,1]` | assertion fail | I9 |
| D-SOL-03 | Control | `test_solution_G3_both_steps_fail` | G3 placeholder | `solution(matrix)` | `UnsolvableDomainError` | 성공 반환 | I10 |
| D-SOL-04 | Control | `test_solution_output_shape_1_index_coords` | G1 | `solution(matrix)` | len 6; coords 1-index | shape fail | I8, I11 |

**Track B 건수:** 12건 · **Domain Mock 금지**

---

## 5. FR ↔ Test ID 추적

| FR | Track A | Track B |
|---|---|---|
| FR-01 입력 검증 | U-IN-01~05, U-FLOW-02 | — |
| FR-02 BlankFinder | — | D-LOC-01 |
| FR-03 MissingNumberFinder | — | D-MIS-01 |
| FR-04 Validator | — | D-VAL-01~06 |
| FR-05 Solver | U-OUT-01~02 | D-SOL-01~04 |

**총 RED 설계 항목:** 26건 (Track A 14 + Track B 12)

---

## 6. RED 설계 자체 검수

- [x] Boundary = E00x Failure envelope (generic Exception 아님)
- [x] invalid → execute 0회 (U-FLOW-02 별도 행)
- [x] U-IN / U-OUT / U-FLOW 분리
- [x] Logic Track Domain Mock 없음
- [x] I1~I11 · AC-FR* · D-* · U-* 추적 가능
- [x] 코드·스켈레톤·pytest 미작성

---

## 7. 권장 RED 진행 순서

1. U-IN-01 → U-IN-02* → U-IN-03* → U-IN-04* → U-IN-05  
2. **U-FLOW-02** (격리)  
3. D-LOC-01 → D-MIS-01  
4. D-VAL-01 → D-VAL-02~06  
5. D-SOL-01 → D-SOL-02 → D-SOL-03 → D-SOL-04  
6. U-OUT-01~02 (또는 Solver GREEN 직후)

---

## 8. 기존 산출물과의 관계

| 기존 | 본 설계표 |
|---|---|
| `test_plan.md` (AC-FR-01-01만) | FR-01 전체 + FR-02~05 Logic Track 확장 |
| `tests/boundary/test_ac_fr_01_01_*` (8 RED fail) | U-IN-01·02*·U-FLOW-02와 **부분 중복** — code 체계 `INVALID_SIZE` vs `E001` **정합 필요** |
| `Report/10`, `Prompt/07` | PRD·1차 Boundary RED QA 세션 |

> **정합 이슈:** 기구현 RED는 `INVALID_SIZE` / `Grid must be 4x4.` 사용. 본 설계는 `E001`/`E003` 체계. GREEN 전 PRD v0.2 또는 `Report/09` §Error와 **단일 SSOT로 통일** 필요.

---

## 9. 다음 단계 (GREEN 진입 전)

1. `docs/PRD_MagicSquare.md` v0.2 또는 `Report/09` Error Contract에 E00x ↔ 메시지 확정  
2. G3 placeholder 격자 검증(양 조합 실패)  
3. Track A RED 테스트 코드 작성 → FAILED 확인  
4. Track B RED 테스트 코드 작성 (Domain Mock 없이)  
5. GREEN은 RED **한 건씩** 최소 구현

---

## 종합 — 한 줄

> **FR-01~FR-05에 대해 Boundary 14건·Logic 12건 RED 설계표를 확정했으며, 코드 작성·pytest 실행 없이 GREEN 진입 전 Error code SSOT 통일이 선행 조건이다.**
