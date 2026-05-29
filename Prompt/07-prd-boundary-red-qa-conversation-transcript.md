# PRD · Boundary RED · QA — 대화 트랜스크립트 (Full Export)

**작성일**: 2026-05-29  
**형식**: 사용자 요청 원문 + 어시스턴트 산출물 기록 (세션 전체 Export)  
**용도**: 동일 작업 흐름을 다른 AI·다른 세션에서 재현  
**요약 보고서**: `Report/10-prd-boundary-red-qa-report.md`  
**단계별 프롬프트**: `Prompt/06-prd-boundary-red-conversation-transcript.md`

---

## 세션 개요

| 항목 | 내용 |
|---|---|
| 프로젝트 | Magic Square 4×4, ECB, Dual-Track TDD |
| 범위 | PRD 분석·작성 → Test Plan → RED → defect → coverage → venv 배치 |
| GREEN | 본 Export 범위 **외** |

---

## Turn 1 — PRD 구현 문서 존재 여부

### [USER] (원문)

```
현재 PRD가 구현되어 있는 문서가 있는가
```

### [ASSISTANT] 요약

- 공식 `PRD` 파일 없음
- `Report/07-user-journey.md`가 요구사항에 가장 근접
- 구현 추적 문서 없음 — `User` 엔티티만 구현됨
- `README` 진행 상태 미갱신 가능성

---

## Turn 2 — PRD 참고 문서 분석 (본문 작성 금지)

### [USER] (원문)

```
당신은 PRD 작성 전문가이자 Dual-Track UI + Logic TDD 기반 제품 기획자입니다.

목표:
Magic Square 프로젝트 구현 전에 PRD를 작성하려고 합니다.

단, 지금은 PRD 본문을 바로 작성하지 마십시오.
먼저 PRD 작성에 참고해야 할 문서들을 분석하고,
각 문서의 어떤 내용을 PRD의 어떤 섹션에 반영해야 하는지 정리해 주세요.

프로젝트:
- Magic Square 4x4
- 목적: 알고리즘 난이도보다 불변식 기반 사고, 계약 기반 테스트, Dual-Track UI + Logic TDD, 리팩토링 훈련
- 아키텍처: Clean Architecture + ECB
- 테스트 방식: pytest, AAA 패턴, RED-GREEN-REFACTOR
- 핵심 산출물: 구현 전 PRD

참고 문서 : 
@Report/

.cursorrules + .cursor/rules/*.mdc
- 팀이 따라야 할 상세 개발 규칙 원문
- PRD의 Engineering Principles 또는 Appendix에 요약 반영
- 상세 규칙이 필요할 경우 부록으로 연결

작업 지시:
1. 각 문서를 읽고 핵심 내용을 요약하십시오.
2. 각 문서가 PRD의 어떤 섹션에 들어가야 하는지 매핑하십시오.
3. 중복되는 내용은 어느 문서를 우선 출처로 삼을지 정하십시오.
4. PRD 본문에 직접 넣을 내용과 부록으로 보낼 내용을 구분하십시오.
5. 구현 코드나 테스트 코드는 작성하지 마십시오.
6. 아직 PRD 본문 전체를 작성하지 마십시오.
7. 이번 단계는 "PRD 작성 전 참고 문서 분석 및 매핑"만 수행하십시오.

출력 형식:

# PRD Reference Document Analysis
(§1~§8 권장 목차)
```

### [ASSISTANT] 산출물

| 파일 | 설명 |
|---|---|
| `Report/08-prd-reference-document-analysis.md` | PRD 섹션 매핑, 우선순위, 충돌·누락, 권장 목차 |

---

## Turn 3 — PRD 본문 작성

### [USER] (원문)

```
해당 문서 참고하여 실제 PRD 까지 상세히 작성
```

### [ASSISTANT] 산출물

| 파일 | 설명 |
|---|---|
| `Report/09-product-requirements-document.md` | PRD v1.0, 13섹션, D-01~D-10 확정 |

---

## Turn 4 — 샘플 예제 선택 (Step 1)

### [USER] (원문)

```
prd 문서를 참고하여 테스트 플랜 작성을 위한 샘플 예제 1개를 선택해줘.
선택 기준:
1. PRD FR-01의 Acceptance Criteria 중 가장 선행 조건인 입력 유효성 검사
2. 비즈니스 로직(grid is None → INVALID_SIZE 반환)을 직접 검증
3. Boundary 계층과 Domain 진입점 호출 격리를 동시에 검증 가능한 기능
...
코드 작성 금지. 선택 결과 문서만 출력.
```

### [ASSISTANT] 산출물

- **AC:** AC-FR-01-01 (PRD AC-1-1, F-1)
- **입력:** `grid = None`
- **출력:** `{ code: "INVALID_SIZE", message: "Grid must be 4x4." }`

---

## Turn 5 — Test Plan (Step 2)

### [USER] (원문)

```
[P] 시니어 QA 리드입니다. [C] Python 3.11+, pytest, pydantic, unittest.mock
[T] 선택한 샘플 예제(AC-FR-01-01: grid=None → INVALID_SIZE)를 기반으로 테스트 계획서를 작성해줘.
...
[F] Markdown 문서. test_plan.md로 저장.
```

### [ASSISTANT] 산출물

| 파일 | 설명 |
|---|---|
| `test_plan.md` | 경계값, mock/spy, 커버리지 목표, Track A/B |

---

## Turn 6 — README RED To-Do (Step 3)

### [USER] (원문)

```
README.md 파일에 아래 섹션을 추가해줘. 기존 내용은 유지하고, ## RED 단계 To-Do 리스트 섹션만 새로 삽입.
(Track A/B, 커버리지, defect_list 체크리스트 포함)
```

### [ASSISTANT] 산출물

- `README.md` — `## RED 단계 To-Do 리스트` 섹션 추가

---

## Turn 7 — RED 테스트 코드 (AC-FR-01-01)

### [USER] (원문)

```
[P] 테스트 설계에 강한 시니어 Python QA입니다. [C] Python 3.11+, pytest, pydantic, unittest.mock
[T] AC-FR-01-01 범위 내에서 아이템 타입별 최소 5개 테스트를 작성해줘.
대상 케이스:
- 정상 실패 반환: grid=None → code="INVALID_SIZE", message="Grid must be 4x4."
- 경계값: grid=[] / grid=[[]] * 4 / grid 크기 3×4
- 격리 검증: grid=None 시 resolve() 0회 호출 (spy/mock)
- 메시지 동일성: PRD §8.1 문구와 문자 단위 비교
- 범위 제한: AC-FR-01-02~05, FR-02~05 케이스 포함 금지
...
[F] 완성된 테스트 코드. RED 단계이므로 pytest가 실패하는 상태로 작성.
```

### [ASSISTANT] 산출물

| 파일 | 설명 |
|---|---|
| `tests/boundary/test_ac_fr_01_01_input_size_validation.py` | 9 tests, Given-When-Then, # AC-FR-01-01 |
| `magic_square/boundary/*.py` | RED stub (NOT_IMPLEMENTED) |
| `magic_square/control/solver.py` | RED stub |

**실행 결과:** 8 failed, 1 passed (RED 정상)

---

## Turn 8 — venv 테스트 실행 방법

### [USER] (원문)

```
테스트코드를 테스트 할 수 있는 방법을 알려줘. 가상환경 기준으로
```

### [ASSISTANT] 산출물

- `python -m venv .venv` → activate → `pip install -e ".[dev]"` → `python -m pytest`
- PowerShell / CMD 명령 구분

---

## Turn 9 — PASS 테스트 목록

### [USER] (원문)

```
pass 되는 테스트는 뭐야
```

### [ASSISTANT] 요약

| PASS | 개수 |
|---|---|
| User entity T01~T13 | 13 |
| `test_red_scope_permits_only_invalid_size_failure_code` | 1 |
| **합계** | **14 / 22** |

---

## Turn 10 — 배치 파일

### [USER] (원문)

```
venv 구축 및 테스트 코드 실행에 대한 것을 배치파일로 만들어줘
```

### [ASSISTANT] 산출물

| 파일 | 설명 |
|---|---|
| `setup_venv.bat` | venv + dev deps |
| `run_tests.bat` | pytest (boundary/entity/cov/cov html) |
| `setup_and_test.bat` | 원스텝 |
| `pyproject.toml` | setuptools packages.find 수정 |

---

## Turn 11 — conv 트랜스크립트

### [USER] (원문)

```
conv 까지
```

### [ASSISTANT] 산출물

| 파일 | 설명 |
|---|---|
| `Prompt/06-prd-boundary-red-conversation-transcript.md` | 단계별 재현 프롬프트 |

---

## Turn 12 — Coverage HTML

### [USER] (원문)

```
coverage test 진행 및 html
```

### [ASSISTANT] 산출물

- 실행: `--cov=magic_square --cov-report=html:htmlcov`
- **Total 97.44%**, HTML: `htmlcov/index.html`
- `run_tests.bat cov html` 옵션 추가

---

## Turn 13 — defect_list.md

### [USER] (원문)

```
[P] QA 리드입니다. [C] 현재까지 발견된 테스트 실패/결함들을 문서화합니다.
[T] 발견된 결함을 defect_list.md에 정리해줘.
항목 형식:
| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
...
[F] Markdown. defect_list.md로 저장. README의 "RED 단계 To-Do 리스트 > 결함 목록 연결" 체크박스도 업데이트.
```

### [ASSISTANT] 산출물

| 파일 | 설명 |
|---|---|
| `defect_list.md` | DEF-001 ~ DEF-008, G-1/G-2 근본 원인 |
| `README.md` | defect_list 생성 체크 ✅ |

---

## Turn 14 — Report · Prompt Export (본 Turn)

### [USER] (원문)

```
Report 폴더에 보고서 생성하고, Prompting 폴더에 Transcript도 Export 해줘
```

### [ASSISTANT] 산출물

| 파일 | 설명 |
|---|---|
| `Report/10-prd-boundary-red-qa-report.md` | 본 세션 통합 QA 보고서 |
| `Prompt/07-prd-boundary-red-qa-conversation-transcript.md` | 본 문서 (Full Export) |

---

## 산출물 전체 인덱스

| 유형 | 경로 |
|---|---|
| Report 08 | `Report/08-prd-reference-document-analysis.md` |
| Report 09 | `Report/09-product-requirements-document.md` |
| Report 10 | `Report/10-prd-boundary-red-qa-report.md` |
| Prompt 06 | `Prompt/06-prd-boundary-red-conversation-transcript.md` |
| Prompt 07 | `Prompt/07-prd-boundary-red-qa-conversation-transcript.md` |
| Test Plan | `test_plan.md` |
| Defects | `defect_list.md` |
| Tests | `tests/boundary/test_ac_fr_01_01_input_size_validation.py` |
| Batch | `setup_venv.bat`, `run_tests.bat`, `setup_and_test.bat` |
| Coverage | `htmlcov/index.html` |

---

## 재현 순서 (권장)

1. Turn 2 → `Report/08`
2. Turn 3 → `Report/09`
3. Turn 4~6 → `test_plan.md`, README RED To-Do
4. Turn 7 → boundary RED tests
5. Turn 10 → 배치 파일
6. Turn 12 → `run_tests.bat cov html`
7. Turn 13 → `defect_list.md`
8. Turn 14 → `Report/10`, `Prompt/07`

---

## 다음 사용자 프롬프트 (GREEN)

```
Report/09-product-requirements-document.md F-1과 defect_list.md DEF-001~008을 해소하세요.
magic_square/boundary/input_validator.py에 4×4 구조 검증을 구현하고,
cli.solve는 검증 실패 시 resolve()를 호출하지 마세요.
run_tests.bat boundary로 9 passed를 확인하세요.
```
