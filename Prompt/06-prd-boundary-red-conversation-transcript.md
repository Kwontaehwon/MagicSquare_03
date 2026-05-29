# PRD · Boundary RED · venv 배치 — 대화형 프롬프트 트랜스크립트

**작성일**: 2026-05-29  
**형식**: PRD 작성 → 테스트 플랜 → RED 테스트 → 실행 환경 구축 (재현용)  
**용도**: 동일한 PRD·TDD RED 진입 프로세스를 다른 AI 또는 다른 세션에서 재현할 때 사용  
**선행 산출물**: `Report/07-user-journey.md`, `Report/01-problem-definition-report.md`, `.cursorrules`

---

## 사용 방법

1. 이 파일의 `[USER]` 블록을 **순서대로** 입력한다.
2. 각 단계는 이전 단계의 산출물(Report, test_plan, 테스트 파일)을 전제로 한다.
3. `[ASSISTANT] 기대 산출물`을 기준으로 응답이 충분한지 자가 점검한다.
4. **구현(GREEN)은 본 conv 범위 밖** — RED 실패 확인까지만 수행한다.

---

## 세션 설정 프롬프트

```
당신은 PRD 작성 전문가이자 Dual-Track UI + Logic TDD 기반 제품 기획·QA 리드입니다.
프로젝트: Magic Square 4×4, ECB, pytest, RED-GREEN-REFACTOR.
참고: Report/, .cursorrules, .cursor/rules/*.mdc
구현 코드는 내가 명시적으로 요청하기 전까지 작성하지 마십시오.
```

---

---

## [USER] STEP A — PRD 구현 문서 존재 여부 확인

```
현재 PRD가 구현되어 있는 문서가 있는가
```

### [ASSISTANT] 기대 응답 핵심 포인트

- 공식 `PRD` 파일 **없음**
- `Report/07-user-journey.md`가 사실상 요구사항 문서
- **구현 추적 문서 없음** — User 엔티티만 코드·테스트 존재
- `README.md` 진행 상태는 갱신 lag 가능성 언급

---

---

## [USER] STEP B — PRD 작성 전 참고 문서 분석 (본문 작성 금지)

```
당신은 PRD 작성 전문가이자 Dual-Track UI + Logic TDD 기반 제품 기획자입니다.

목표: Magic Square 프로젝트 구현 전에 PRD를 작성하려고 합니다.
단, 지금은 PRD 본문을 바로 작성하지 마십시오.
먼저 PRD 작성에 참고해야 할 문서들을 분석하고,
각 문서의 어떤 내용을 PRD의 어떤 섹션에 반영해야 하는지 정리해 주세요.

참고 문서: Report/, .cursorrules + .cursor/rules/*.mdc

작업 지시:
1. 각 문서를 읽고 핵심 내용을 요약
2. PRD 섹션 매핑
3. 중복 시 우선 출처
4. 본문 vs 부록 구분
5. 구현·테스트 코드 작성 금지
6. PRD 본문 전체 작성 금지

출력 형식: # PRD Reference Document Analysis (§1~§8 권장 목차)
```

### [ASSISTANT] 기대 산출물

| 산출물 | 경로 |
|---|---|
| PRD 참고 문서 분석 | `Report/08-prd-reference-document-analysis.md` |

**핵심 판단**
- PRD 작성 **조건부 가능** — `07-user-journey.md` 1차, `01` 보조
- **충돌**: 완성형 generate/validate vs 2칸 Solver — §3.5에서 확정 필요
- **누락**: 코어 Test List, P0/P1, 오류 반환 형식

---

---

## [USER] STEP C — PRD 본문 상세 작성

```
해당 문서 참고하여 실제 PRD 까지 상세히 작성
(Report/08-prd-reference-document-analysis.md 참조)
```

### [ASSISTANT] 기대 산출물

| 산출물 | 경로 |
|---|---|
| Product Requirements Document v1.0 | `Report/09-product-requirements-document.md` |

**§3.5 확정 결정 (D-01~D-10)**
- v1 Primary: **Partial Puzzle Solver** (2 blanks, `int[6]`)
- Validator = **Control**, ECB 디렉터리 구조
- 커버리지: Control ≥95%, 전체 ≥80%
- 좌표: 내부 0-index / 출력 1-index
- User 엔티티 P1, Solver 경로와 분리

---

---

## [USER] STEP D-1 — 샘플 예제 선택 (코드 금지)

```
prd 문서를 참고하여 테스트 플랜 작성을 위한 샘플 예제 1개를 선택해줘.

선택 기준:
1. PRD FR-01의 Acceptance Criteria 중 가장 선행 조건인 입력 유효성 검사
2. 비즈니스 로직(grid is None → INVALID_SIZE 반환)을 직접 검증
3. Boundary 계층과 Domain 진입점 호출 격리를 동시에 검증 가능

선택 결과: AC ID, PRD 번호, 입력/출력 예시, 선택 이유 2줄
코드 작성 금지.
```

### [ASSISTANT] 기대 응답

| 항목 | 값 |
|---|---|
| AC ID | AC-FR-01-01 (PRD AC-1-1, F-1) |
| 입력 | `grid = None` |
| 출력 | `{ code: "INVALID_SIZE", message: "Grid must be 4x4." }` |
| 격리 | `resolve()` / `solve()` 0회 |

---

---

## [USER] STEP D-2 — 테스트 플랜 작성

```
[P] 시니어 QA 리드 [C] Python 3.11+, pytest, pydantic, unittest.mock
[T] AC-FR-01-01 (grid=None → INVALID_SIZE) 기반 테스트 계획서

포함: 단위 테스트 범위/우선순위, 경계값(None/[]/[[]]*4/3×4),
격리 mock/spy, 커버리지 목표, pytest-cov 명령
[F] Markdown → test_plan.md
```

### [ASSISTANT] 기대 산출물

| 산출물 | 경로 |
|---|---|
| Test Plan | `test_plan.md` |

---

---

## [USER] STEP D-3 — README RED To-Do

```
README.md에 ## RED 단계 To-Do 리스트 섹션 추가
(test_plan.md 기반 Track A/B, 커버리지, defect_list 체크리스트)
```

### [ASSISTANT] 기대 산출물

- `README.md` — `## RED 단계 To-Do 리스트` (기존 내용 유지, 섹션 삽입)

---

---

## [USER] STEP E — AC-FR-01-01 RED 테스트 코드 작성

```
[P] 시니어 Python QA [C] pytest, pydantic, unittest.mock
[T] AC-FR-01-01 범위, 아이템 타입별 최소 5개 테스트

케이스: None→INVALID_SIZE, 경계값([]/[[]]*4/3×4),
격리 resolve 0회 spy, 메시지 문자 단위, AC-FR-01-02~05 제외

형식: Given-When-Then, test_[조건]_[동작]_[포인트], # AC-FR-01-01
[F] RED — pytest 실패 상태
```

### [ASSISTANT] 기대 산출물

| 산출물 | 경로 |
|---|---|
| RED 테스트 (9개) | `tests/boundary/test_ac_fr_01_01_input_size_validation.py` |
| RED stub | `magic_square/boundary/*.py`, `magic_square/control/solver.py` |

**RED 실행 결과 (기준)**
- Boundary: **8 failed, 1 passed** (범위 메타 테스트 1개만 PASS)
- Entity: **13 passed**

---

---

## [USER] STEP F — venv 테스트 실행 방법

```
테스트코드를 테스트 할 수 있는 방법을 알려줘. 가상환경 기준으로
```

### [ASSISTANT] 기대 응답

- `python -m venv .venv` → activate → `pip install -e ".[dev]"` → `python -m pytest`
- PowerShell / CMD 활성화 명령 구분

---

---

## [USER] STEP G — PASS 테스트 확인

```
pass 되는 테스트는 뭐야
```

### [ASSISTANT] 기대 응답

| PASS | 개수 |
|---|---|
| User entity (T01~T13) | 13 |
| Boundary scope meta | 1 |
| **합계** | **14 / 22** |

---

---

## [USER] STEP H — venv·테스트 배치 파일

```
venv 구축 및 테스트 코드 실행에 대한 것을 배치파일로 만들어줘
```

### [ASSISTANT] 기대 산출물

| 파일 | 역할 |
|---|---|
| `setup_venv.bat` | `.venv` 생성 + `pip install -e ".[dev]"` |
| `run_tests.bat` | pytest (all / boundary / entity / cov) |
| `setup_and_test.bat` | 구축 + 전체 테스트 원스텝 |

**부수 수정**
- `pyproject.toml` — `[tool.setuptools.packages.find] include = ["magic_square*"]`

---

---

## [USER] STEP I — conv 트랜스크립트 (본 문서)

```
conv 까지
```

### [ASSISTANT] 기대 산출물

| 산출물 | 경로 |
|---|---|
| 본 대화 트랜스크립트 | `Prompt/06-prd-boundary-red-conversation-transcript.md` |

---

---

## 산출물 인덱스 (본 세션)

| # | 유형 | 파일 |
|---|---|---|
| 08 | Report | `Report/08-prd-reference-document-analysis.md` |
| 09 | Report | `Report/09-product-requirements-document.md` |
| — | Test Plan | `test_plan.md` |
| — | Tests | `tests/boundary/test_ac_fr_01_01_input_size_validation.py` |
| — | Batch | `setup_venv.bat`, `run_tests.bat`, `setup_and_test.bat` |
| 06 | Prompt | `Prompt/06-prd-boundary-red-conversation-transcript.md` |
| 10 | Report | `Report/10-prd-boundary-red-qa-report.md` |
| 07 | Prompt | `Prompt/07-prd-boundary-red-qa-conversation-transcript.md` |

---

## 다음 단계 (conv 이후)

```
GREEN: magic_square/boundary/input_validator.py — 4×4 구조 검증 구현
       magic_square/boundary/cli.py — 검증 실패 시 resolve() 미호출

확인: run_tests.bat boundary → 8 failed → 점진적 passed 증가
체크: README.md RED 단계 To-Do 리스트 항목 체크
```

---

## 재현 체크리스트

- [ ] `Report/08`, `09` 존재
- [ ] `test_plan.md` 존재
- [ ] `tests/boundary/test_ac_fr_01_01_input_size_validation.py` — RED 8 fail
- [ ] `setup_venv.bat` 실행 성공
- [ ] `run_tests.bat` — 22 collected, 14 passed
- [ ] `Prompt/06` (본 문서) 존재

---

## Prompt 폴더 번호 체계

| 파일 | 주제 |
|---|---|
| 01 | STEP 1~5 문제 정의 |
| 02 | Cursor 4×4 문제 정의 원본 |
| 03 | TDD 설계 프롬프트 |
| 04 | Cursor Rules 설계 |
| 05 | Role Subagents 설계 |
| **06** | **PRD · Boundary RED · venv (단계별 프롬프트)** |
| **07** | **PRD · Boundary RED · QA (Full Export)** |

**후속:** coverage·defect·Report/10·Prompt/07 → `Prompt/07-prd-boundary-red-qa-conversation-transcript.md`, `Report/10-prd-boundary-red-qa-report.md`
