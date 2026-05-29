# 4×4 Magic Square — PRD · Boundary RED · QA 실행 보고서

**작성일**: 2026-05-29  
**단계**: PRD 확정 → Test Plan → RED 테스트 → 결함 등록 → 커버리지·실행 환경  
**선행 산출물**: `Report/07-user-journey.md`, `Report/08-prd-reference-document-analysis.md`, `Report/09-product-requirements-document.md`  
**대화 재현**: `Prompt/07-prd-boundary-red-qa-conversation-transcript.md`  
**목적**: 구현(GREEN) 진입 전, PRD·RED·QA 산출물과 테스트 실행 결과를 통합 기록한다.

---

## 0. 본 보고서의 범위

| 구분 | 위치 |
|---|---|
| PRD 참고 분석 | `Report/08-prd-reference-document-analysis.md` |
| PRD 본문 | `Report/09-product-requirements-document.md` |
| Test Plan | `test_plan.md` |
| RED 테스트 | `tests/boundary/test_ac_fr_01_01_input_size_validation.py` |
| 결함 목록 | `defect_list.md` |
| QA 실행 배치 | `setup_venv.bat`, `run_tests.bat`, `setup_and_test.bat` |
| 커버리지 HTML | `htmlcov/index.html` |
| 대화 트랜스크립트 | `Prompt/07-prd-boundary-red-qa-conversation-transcript.md` |
| 본 보고서 | `Report/10-prd-boundary-red-qa-report.md` |

**본 보고서 범위 밖:** GREEN 구현(`input_validator`, `cli.solve` 수정), AC-FR-01-02~05

---

## 1. 세션 목표 및 성과

### 1.1 목표

| # | 목표 | 달성 |
|---|---|---|
| G1 | PRD 작성 전 참고 문서 분석·매핑 | ✅ `Report/08` |
| G2 | PRD v1.0 본문 작성 (13섹션) | ✅ `Report/09` |
| G3 | AC-FR-01-01 RED 테스트·Test Plan | ✅ `test_plan.md`, boundary tests |
| G4 | 결함 문서화 | ✅ `defect_list.md` (DEF-001~008) |
| G5 | venv·pytest·coverage HTML 실행 환경 | ✅ 배치 파일, `htmlcov/` |
| G6 | 대화 트랜스크립트 Export | ✅ `Prompt/07` |

### 1.2 PRD 핵심 확정 (D-01~D-10)

| 결정 | 내용 |
|---|---|
| D-01 | v1 Primary = **2칸 빈칸 Solver** (`int[6]` 출력) |
| D-03 | `MagicSquareValidator` = **Control** |
| D-05 | Control ≥95%, 전체 ≥80% 커버리지 |
| D-06 | 내부 0-index / Boundary 출력 1-index |
| D-07 | 실패 DTO: `INVALID_SIZE`, `Grid must be 4x4.` |

---

## 2. 산출물 트리

```
MagicSquare_/
├── Report/
│   ├── 08-prd-reference-document-analysis.md
│   ├── 09-product-requirements-document.md
│   └── 10-prd-boundary-red-qa-report.md          ← 본 문서
├── Prompt/
│   ├── 06-prd-boundary-red-conversation-transcript.md  (단계별 프롬프트)
│   └── 07-prd-boundary-red-qa-conversation-transcript.md ← 전체 Export
├── test_plan.md
├── defect_list.md
├── tests/boundary/test_ac_fr_01_01_input_size_validation.py
├── magic_square/boundary/                        ← RED stub
├── setup_venv.bat | run_tests.bat | setup_and_test.bat
└── htmlcov/                                      ← coverage HTML
```

---

## 3. Test Plan 요약

| 항목 | 내용 |
|---|---|
| Anchor AC | AC-FR-01-01 (F-1, US-01, AC-1-1) |
| Anchor 입력 | `grid = None` |
| Anchor 출력 | `{ code: "INVALID_SIZE", message: "Grid must be 4x4." }` |
| Track A | Boundary 검증·실패 DTO·메시지 동일성 |
| Track B | `resolve()` 0회 spy (AC-1-6, L3-4) |
| Out of Scope | AC-FR-01-02~05, 4×4 정상 Happy Path |

---

## 4. RED 테스트 실행 결과

**실행:** `run_tests.bat` / `python -m pytest tests/ -v` (2026-05-29, `.venv`)

| 구분 | collected | passed | failed |
|---|---|---|---|
| **전체** | 22 | 14 | 8 |
| Boundary (AC-FR-01-01) | 9 | 1 | 8 |
| Entity (User T01~T13) | 13 | 13 | 0 |

### 4.1 Boundary 실패 테스트 (RED 정상)

| 테스트 | 결함 ID |
|---|---|
| `test_none_grid_returns_invalid_size_code` | DEF-001 |
| `test_none_grid_returns_invalid_size_message` | DEF-002 |
| `test_size_mismatch_grid_returns_invalid_size[empty_list]` | DEF-003 |
| `test_size_mismatch_grid_returns_invalid_size[four_rows_zero_cols]` | DEF-004 |
| `test_size_mismatch_grid_returns_invalid_size[three_by_four]` | DEF-005 |
| `test_none_grid_message_matches_prd_section_8_1_character_for_character` | DEF-006 |
| `test_none_grid_resolve_spy_called_zero_times` | DEF-007 |
| `test_none_grid_failure_code_is_invalid_size_not_out_of_scope_codes` | DEF-008 |

### 4.2 PASS (참고)

- `test_red_scope_permits_only_invalid_size_failure_code` — 범위 메타 테스트
- `tests/entity/test_user.py` — 13건 전부 PASS

---

## 5. 결함 요약 (`defect_list.md`)

| 그룹 | 결함 | 근본 원인 | 수정 모듈 |
|---|---|---|---|
| **G-1** | DEF-001 ~ 006, 008 | `validate_grid` RED stub (`NOT_IMPLEMENTED`) | `boundary/input_validator.py` |
| **G-2** | DEF-007 | `solve()`가 검증 전 `resolve()` 호출 | `boundary/cli.py` |

**Open:** 7건 (표면 8 failed 테스트, 근본 2그룹)

---

## 6. 커버리지 결과

**실행:** `python -m pytest tests/ --cov=magic_square --cov-report=term-missing --cov-report=html:htmlcov`

| 항목 | 값 |
|---|---|
| **Total** | **97.44%** (전체 목표 80% 충족) |
| `entity/user.py` | 100% |
| `boundary/*` (stub) | 100% (실제 분기 미반영 — GREEN 후 재측정 필요) |
| `control/solver.py` | 75% (`NotImplementedError` 라인) |
| HTML | `htmlcov/index.html` |

> RED stub이 호출만 되어 커버리지 수치는 **참고용**이며, GREEN 후 Boundary 실제 분기 기준으로 재측정한다.

---

## 7. 실행 환경 (배치 파일)

| 파일 | 역할 |
|---|---|
| `setup_venv.bat` | `.venv` 생성 + `pip install -e ".[dev]"` |
| `run_tests.bat` | pytest (`boundary` / `entity` / `cov` / `cov html`) |
| `setup_and_test.bat` | setup + 전체 테스트 원스텝 |

**`pyproject.toml` 변경:** `[tool.setuptools.packages.find] include = ["magic_square*"]` (editable 설치 수정)

---

## 8. README·체크리스트 반영

| 항목 | 상태 |
|---|---|
| `## RED 단계 To-Do 리스트` | 추가됨 |
| `defect_list.md` 생성 | ✅ 체크 |
| 회귀 테스트 전체 통과 | ⬜ GREEN 후 |

---

## 9. 다음 단계 (GREEN)

| 순서 | 작업 | 완료 기준 |
|---|---|---|
| 1 | `input_validator.validate_grid` — 4×4 구조 검증 | DEF-001~006, 008 해소 |
| 2 | `cli.solve` — 검증 실패 시 `resolve` 미호출 | DEF-007 해소 |
| 3 | `run_tests.bat boundary` | 9 passed |
| 4 | `run_tests.bat` | 22 passed |
| 5 | `cov html` 재실행 | Boundary 실제 분기 ≥85% |
| 6 | `defect_list.md` 전건 Closed | README 회귀 체크 |

---

## 10. Report · Prompt 인덱스 (본 세션)

| # | Report | Prompt |
|---|---|---|
| 08 | PRD 참고 문서 분석 | 06 (단계별 프롬프트) |
| 09 | PRD v1.0 | 07 (전체 대화 Export) |
| 10 | 본 QA 실행 보고서 | — |

---

## 종합 — 한 줄

> **PRD v1.0과 AC-FR-01-01 RED 테스트·결함 8건·실행 환경이 준비되었으며, GREEN은 `input_validator` + `cli.solve` 두 모듈 수정으로 22 passed를 목표로 한다.**
