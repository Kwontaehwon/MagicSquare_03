# Defect List — Magic Square 4×4

| 항목 | 내용 |
|---|---|
| **문서 ID** | DEF-MSQ-001 |
| **작성일** | 2026-05-29 |
| **작성자** | QA Lead |
| **기준 PRD** | `Report/09-product-requirements-document.md` (F-1, US-01, AC-1-1, AC-1-6) |
| **기준 테스트** | `tests/boundary/test_ac_fr_01_01_input_size_validation.py` |
| **실행 환경** | Python 3.13, pytest 9.x, `.venv`, `run_tests.bat` / `cov html` |
| **상태 요약** | Open **7** / Closed **0** / Total **7** |

---

## 실행 스냅샷 (2026-05-29)

| 구분 | 결과 |
|---|---|
| 전체 테스트 | 22 collected — **14 passed**, **8 failed** |
| Boundary (AC-FR-01-01) | **8 failed**, 1 passed |
| Entity (User) | 13 passed |
| 커버리지 | 97.44% (stub 호출로 수치는 GREEN 후 재측정 필요) |

---

## 결함 목록

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|---|---|---|---|---|---|---|---|
| DEF-001 | Critical | AC-FR-01-01 | 1. `validate_grid(None)` 호출 (`test_none_grid_returns_invalid_size_code`) | `result.code == "INVALID_SIZE"` | `result.code == "NOT_IMPLEMENTED"` | `input_validator.validate_grid`가 RED stub으로 고정 반환 | `grid is None` 또는 비-4×4 구조 시 `ValidationFailure(code="INVALID_SIZE", message="Grid must be 4x4.")` 반환 구현 |
| DEF-002 | Critical | AC-FR-01-01 | 1. `validate_grid(None)` 호출 (`test_none_grid_returns_invalid_size_message`) | `result.message == "Grid must be 4x4."` | `result.message == "validate_grid is not implemented"` | DEF-001과 동일 — 메시지 계약 미구현 | PRD §8.1 문구를 **문자 단위 동일**하게 반환 |
| DEF-003 | High | AC-FR-01-01 | 1. `validate_grid([])` 호출 (`test_size_mismatch_grid_returns_invalid_size[empty_list]`) | `code="INVALID_SIZE"`, `message="Grid must be 4x4."` | `code="NOT_IMPLEMENTED"`, stub 메시지 | 행 수 0 검사 누락 (4×4 구조 검증 미구현) | 빈 리스트 입력 시 INVALID_SIZE 반환 |
| DEF-004 | High | AC-FR-01-01 | 1. `validate_grid([[]]*4)` 호출 (`test_size_mismatch_grid_returns_invalid_size[four_rows_zero_cols]`) | `code="INVALID_SIZE"`, `message="Grid must be 4x4."` | `code="NOT_IMPLEMENTED"`, stub 메시지 | 열 수 0 검사 누락 | 각 행 길이 4 여부 검사 추가 |
| DEF-005 | High | AC-FR-01-01 | 1. `validate_grid(3×4 행렬)` 호출 (`test_size_mismatch_grid_returns_invalid_size[three_by_four]`) | `code="INVALID_SIZE"`, `message="Grid must be 4x4."` | `code="NOT_IMPLEMENTED"`, stub 메시지 | 행 수 ≠ 4 검사 누락 | `len(grid) != 4` 또는 열 불일치 시 INVALID_SIZE |
| DEF-006 | High | AC-FR-01-01 | 1. `validate_grid(None)` 2. code·message·길이·문자 단위 비교 (`test_none_grid_message_matches_prd_section_8_1_character_for_character`) | `code`/`message` PRD §8.1과 완전 일치 | `NOT_IMPLEMENTED` / stub 메시지 | DEF-001·002와 동일 근본 원인 | DEF-001·002 수정으로 해소 |
| DEF-007 | Critical | AC-FR-01-01, AC-1-6, L3-4 | 1. `solve(None)` 호출, `resolve` spy 설정 (`test_none_grid_resolve_spy_called_zero_times`) | `resolve` 호출 **0회** | `resolve(None)` **1회** 호출 (`Calls: [call(None)]`) | `cli.solve`가 검증 전 `resolve(grid)` 선호출 (RED stub) | 검증 실패 시 **즉시** `ValidationFailure` 반환, `resolve` 미호출 |
| DEF-008 | High | AC-FR-01-01 | 1. `validate_grid(None)` 2. `result.code not in {INVALID_BLANK_COUNT, ...}` (`test_none_grid_failure_code_is_invalid_size_not_out_of_scope_codes`) | `result.code == "INVALID_SIZE"` | `result.code == "NOT_IMPLEMENTED"` | DEF-001과 동일 — 오류 코드 체계 미정립 | DEF-001 수정으로 해소 |

---

## 근본 원인 그룹 (수정 우선순위)

| 그룹 | 결함 ID | 담당 모듈 | GREEN 작업 |
|---|---|---|---|
| **G-1** | DEF-001, 002, 003, 004, 005, 006, 008 | `magic_square/boundary/input_validator.py` | 4×4 구조 검증 + `INVALID_SIZE` / `Grid must be 4x4.` |
| **G-2** | DEF-007 | `magic_square/boundary/cli.py` | `validate_grid` 선행, 실패 시 early return |

---

## 영향 테스트 매핑

| pytest 테스트 | 결함 ID | 상태 |
|---|---|---|
| `test_none_grid_returns_invalid_size_code` | DEF-001 | Open |
| `test_none_grid_returns_invalid_size_message` | DEF-002 | Open |
| `test_size_mismatch_grid_returns_invalid_size[empty_list]` | DEF-003 | Open |
| `test_size_mismatch_grid_returns_invalid_size[four_rows_zero_cols]` | DEF-004 | Open |
| `test_size_mismatch_grid_returns_invalid_size[three_by_four]` | DEF-005 | Open |
| `test_none_grid_message_matches_prd_section_8_1_character_for_character` | DEF-006 | Open |
| `test_none_grid_resolve_spy_called_zero_times` | DEF-007 | Open |
| `test_none_grid_failure_code_is_invalid_size_not_out_of_scope_codes` | DEF-008 | Open |
| `test_red_scope_permits_only_invalid_size_failure_code` | — | Pass (결함 아님) |

---

## AC-FR-01-02~05 범위 외 (본 문서 미등록)

다음은 **의도적 RED 범위 외**이며 결함으로 분류하지 않음 (`test_plan.md` OUT-01~05).

| 항목 | 사유 |
|---|---|
| 빈칸 개수 ≠ 2 | AC-FR-01-02 — 후속 스프린트 |
| 값 범위 위반 | AC-FR-01-03 — 후속 스프린트 |
| 0 제외 중복 | AC-FR-01-04 — 후속 스프린트 |
| 4×4 정상 입력 Happy Path | AC-1-7 — GREEN 후 |

---

## 수정 완료 시 체크리스트

- [ ] DEF-001 ~ DEF-008 상태를 Closed로 변경
- [ ] `run_tests.bat boundary` → 9 passed (또는 8 failed → 0)
- [ ] `run_tests.bat` 전체 → 22 passed
- [ ] `run_tests.bat cov html` 재실행 후 Boundary 실제 분기 커버리지 확인
- [ ] README `결함 목록 연결` — 회귀 통과 체크

---

## 변경 이력

| 날짜 | 변경 |
|---|---|
| 2026-05-29 | 초안 — RED 단계 Boundary 8건 실패 등록 (DEF-001 ~ DEF-008) |
