# Cursor를 이용한 TDD 적용 — 최종 보고서

> **과제명**: 4×4 Magic Square — Cursor AI 활용 소프트웨어 개발 응용  
> **작성일**: 2026-05-29  
> **상태**: 전체 62 tests passed · REFACTOR 완료 · Code Review 완료

---

## 목차

1. [프로젝트 한눈에 보기](#1-프로젝트-한눈에-보기)
2. [전체 흐름 타임라인](#2-전체-흐름-타임라인)
3. [Phase 0 — 문제 정의 (STEP 1~5)](#3-phase-0--문제-정의-step-15)
4. [Phase 1 — Cursor 환경 설계](#4-phase-1--cursor-환경-설계)
5. [Phase 2 — PRD와 Dual-Track TDD 설계](#5-phase-2--prd와-dual-track-tdd-설계)
6. [Phase 3 — RED: 테스트 먼저 작성](#6-phase-3--red-테스트-먼저-작성)
7. [Phase 4 — GREEN: 최소 구현](#7-phase-4--green-최소-구현)
8. [Phase 5 — REFACTOR & Code Review](#8-phase-5--refactor--code-review)
9. [핵심 인사이트](#9-핵심-인사이트)
10. [복습 체크리스트](#10-복습-체크리스트)
11. [산출물 전체 목록](#11-산출물-전체-목록)

---

## 1. 프로젝트 한눈에 보기

### 1.1 무엇을 만들었는가

**4×4 마방진(Magic Square) 부분 해결 라이브러리**  
빈칸 2개가 있는 4×4 부분 격자를 입력받아 마방진을 완성하고 `[r1,c1,n1,r2,c2,n2]`를 반환하는 Python 패키지.

```
입력  : 4×4 int[][] (0 = 빈칸, 정확히 2개)
출력  : int[6] = [r1, c1, n1, r2, c2, n2]  (좌표 1-index)
```

### 1.2 진짜 목적은 "마방진을 만드는 것"이 아니다

> **4×4 격자에서 제약 조건을 만족하는 상태가 존재하는지 판단하고,  
> 그 상태를 생성·검증·표현하는 책임을 분리하여 다룰 수 있는가.**

이 프로젝트는 마방진을 핑계 삼아 **"Cursor AI를 활용한 TDD 사고 훈련"** 을 수행하는 것이 목적이다.

### 1.3 최종 지표

| 지표 | 결과 |
|---|---|
| 전체 테스트 | **62 passed, 0 failed** (0.21s) |
| Track A (Boundary) | 33건 GREEN |
| Track B (Entity/Control) | 29건 GREEN |
| 금지 패턴 위반 | **0건** |
| Code Review P0 이슈 | **해소 완료** |
| Cursor Rules 파일 | 5개 |
| Cursor Sub-agents | 8개 |
| 보고서 | 12편 |
| Git 커밋 수 | 약 35개 |

---

## 2. 전체 흐름 타임라인

```
[2026-05-28]
  STEP 1~5  │ 문제 정의 프로세스 → Invariant Level 0~3 확정
            │ Report/01-problem-definition-report.md
            │
  STEP 6    │ TDD 설계 프롬프트 설계 → TDD 설계 문서 구조 확정
            │ Report/02-tdd-design-prompt-report.md
            │
  STEP 7    │ User 도메인 확장 정의
            │ Report/03-user-domain-extension.md
            │
  STEP 8    │ Test List 작성
            │ Report/04-user-test-list.md
            │
  STEP 9    │ Cursor Rules 5개 설계·생성
            │ Report/05-cursorrules-design-report.md
            │
  STEP 10   │ Role-based Sub-agents 8개 설계·생성
            │ Report/06-role-subagents-design-report.md

[2026-05-29]
  STEP 11   │ User Journey 작성
            │ Report/07-user-journey.md
            │
  STEP 12   │ PRD 참고 분석 + PRD v1.0 작성 (13섹션)
            │ Report/08 + 09-product-requirements-document.md
            │
  STEP 13   │ RED 테스트 작성 (R1) + 결함 목록 + QA 환경 구축
            │ Report/10-prd-boundary-red-qa-report.md
            │ defect_list.md (DEF-001~008)
            │
  STEP 14   │ Dual-Track RED 설계 (R1~R8 전체, 33건)
            │ Report/11-dual-track-red-design-report.md
            │
  STEP 15   │ GREEN G01~G33 (33건) 순차 구현
            │ commit: green: AC-FR-01-01 G01 … → G33
            │
  STEP 16   │ REFACTOR M6 (Not_Implemented 제거, shape_valid 추가 등)
            │ commit: refactor(m6): clean boundary validation
            │
  STEP 17   │ Code Review (Code Reviewer 서브에이전트 위임)
            │ Report/12-code-review-report.md
```

---

## 3. Phase 0 — 문제 정의 (STEP 1~5)

### 3.1 5단계 문제 인식 프로세스

| 단계 | 이름 | 핵심 질문 | 핵심 발견 |
|---|---|---|---|
| STEP 1 | Observation | 현재 상황은 무엇인가? | 제약 조건이 강한 배치 문제. 탐색 공간 16! ≈ 2×10¹³ |
| STEP 2 | Why #1 | 왜 마방진을 완성해야 하는가? | "완성"은 성공 기준·검증 책임·해 공간을 은폐한다 |
| STEP 3 | Why #2 | 왜 프로그램으로 구현하는가? | 반복 가능성·검증 자동화·오류 방지·규칙 기반 사고 |
| STEP 4 | Why #3 | 왜 TDD 방식으로 설계하는가? | 불변 조건을 먼저 선언하고 이해를 증명하기 위해서 |
| STEP 5 | 문제 정의 | 진짜 문제는 무엇인가? | 생성·검증·표현의 책임 분리, 10가지 조건의 완전한 열거 |

### 3.2 표면 문제 vs. 개선된 문제

| 구분 | 정의 | 결함 |
|---|---|---|
| **표면 (거부)** | "1~16을 배치해 행·열·대각선 합이 같아지는 마방진을 **만드는** 프로그램" | 목적 부재, 성공 기준 없음, 검증 은폐, 해 공간 무시 |
| **개선 (정본)** | "4×4 격자에서 제약 조건을 만족하는 상태가 **존재하는가를 판단**하고, 그 상태를 생성·검증·표현하는 책임을 **명확히 분리**하여 다룰 수 있는가" | — |

> **핵심 통찰**: "만든다"라는 동사가 목적을 설명하지 않는다.  
> "판단한다"와 "다룰 수 있는가"로 전환할 때 테스트 가능성이 생긴다.

### 3.3 Invariant 계층

```
Level 0 — 구성 불변 조건 (전제)
  └── 16칸, 1~16, 중복 없음

Level 1 — 합산 불변 조건 (정의)
  └── 행 4 + 열 4 + 주대각선 1 + 반대각선 1 = 34
      (각각 독립, 모두 성립해야 함)

Level 2 — 파생 불변 조건 (유도)
  └── Magic Constant = n(n²+1)/2 → 4×(17)/2 = 34
      (격자 크기 n이 결정되면 유일하게 결정, 하드코딩 금지)

Level 3 — 설계 불변 조건 (분리)
  └── generate() / validate() / display() 는 서로 독립
```

---

## 4. Phase 1 — Cursor 환경 설계

### 4.1 Cursor Rules 5개 (`.cursor/rules/`)

Cursor Rules는 "매 세션마다 반복 입력하지 않아도 되는 영구 가이드라인"이다.

| 파일 | 적용 범위 | 핵심 역할 |
|---|---|---|
| `magicsquare-project.mdc` | `alwaysApply: true` | 문제 정의 핵심 + Invariant Level 0~3 상시 주입 |
| `magicsquare-forbidden.mdc` | `alwaysApply: true` | 안티패턴 5종 금지 (하드코딩·책임혼재·조건생략 등) |
| `magicsquare-ecb-architecture.mdc` | `**/*.py` | ECB 3계층 책임 분리 원칙 |
| `magicsquare-python-code-style.mdc` | `**/*.py` | 타입 힌트 필수, Magic Constant 유도, 네이밍 |
| `magicsquare-tdd-testing.mdc` | `**/test_*.py` | Invariant 계층별 테스트 순서·픽스처 분리 규칙 |

**Rules 설계 원칙**:
- `alwaysApply`: 프로젝트 문맥·금지 패턴은 파일 종류와 무관하게 필요
- 파일 한정: 코드 스타일·아키텍처·테스트 규칙은 해당 파일 작업 시에만 로드
- 50줄 이내: AI 컨텍스트 낭비 방지

### 4.2 Role-based Sub-agents 8개 (`.cursor/agents/`)

"특정 작업을 위임할 전문 역할"을 영구 선언.

| 파일 | 역할 | readonly |
|---|---|---|
| `code-reviewer.md` | Code Reviewer | `true` (검토 전용) |
| `performance-optimizer.md` | 측정→가설→수정→재측정 사이클 | `false` |
| `ux-design-advisor.md` | WCAG 2.1 AA 기준 UX 점검 | `false` |
| `product-manager.md` | PRD 13개 섹션 표준 | `false` |
| `backend-developer.md` | 계약 우선·계층 분리 | `false` |
| `frontend-developer.md` | a11y·성능·디자인 토큰 | `false` |
| `qa-engineer.md` | 마방진 10개 조건 검사 명시 | `false` |
| `ai-integration-specialist.md` | OpenRouter + DeepSeek 패턴 | `false` |

**Sub-agent 설계 원칙**:
- `description` 끝에 위임 신호 포함 ("~ 필요할 때 적극 활용하세요")
- 모든 에이전트가 `.cursor/rules/` 참조 한 줄 명시
- 역할 단일성: 한 에이전트는 한 역할만

---

## 5. Phase 2 — PRD와 Dual-Track TDD 설계

### 5.1 PRD v1.0 (13섹션)

PRD는 "구현 직전 계약서"다. 구현 전에 **수락 기준(Acceptance Criteria)**을 명문화한다.

| 결정 ID | 내용 |
|---|---|
| D-01 | v1 Primary = **2칸 빈칸 Solver** (`int[6]` 출력) |
| D-03 | `MagicSquareValidator` = Control 계층 |
| D-05 | Control ≥95%, 전체 ≥80% 커버리지 목표 |
| D-06 | 내부 0-index / Boundary 출력 1-index |
| D-07 | 실패 DTO: `INVALID_SIZE`, `"Grid must be 4x4."` |

**핵심 Error Envelope**:

| code | message |
|---|---|
| `E003` | `Input matrix must not be null.` |
| `E001` | `Grid must be 4x4.` |
| `E002` | `Exactly two blank cells (0) are required.` |
| `E004` | `Each cell must be 0 or an integer from 1 to 16.` |
| `E005` | `Non-zero cell values must not duplicate.` |

### 5.2 Dual-Track TDD 구조

두 개의 독립적인 테스트 트랙이 병렬로 진행된다.

```
Track A — Boundary (UI Contract)
  ├── U-IN:   입력 검증 계약
  ├── U-FLOW: 도메인 격리 (invalid → resolve 미호출)
  ├── U-OUT:  출력 계약
  └── AC-FR:  Acceptance Criteria 검증

Track B — Entity/Control (Domain Logic)
  ├── D-LOC:  BlankFinder
  ├── D-MIS:  MissingNumberFinder
  ├── D-VAL:  MagicSquareValidator (6건 독립)
  └── D-SOL:  Solver (4건)
```

### 5.3 격자 픽스처 G0~G3

테스트의 재현 가능성을 위해 픽스처를 사전 정의.

| ID | 용도 | 특성 |
|---|---|---|
| G0 | 완전 마방진 | 행·열·대각선 합 = 34 |
| G1 | Step A 성공 | 빈칸 (2,2)(3,3), 누락 {7,10}, 기대 `[2,2,7,3,3,10]` |
| G2 | Step A실패→B성공 | fallback 경로 검증 |
| G3 | 양 조합 실패 | `UnsolvableDomainError` |

---

## 6. Phase 3 — RED: 테스트 먼저 작성

### 6.1 RED 커밋 8묶음 (R1~R8, 총 33건)

| RED 커밋 | 테스트 파일 | 건수 | 범위 |
|---|---|---|---|
| R1 | `test_ac_fr_01_01_input_size_validation.py` | 9 | 크기 검증·격리 |
| R2 | `test_u_in_04_08_input_validation.py` | 5 | blank·범위·중복 |
| R3 | `test_u_flow_02_domain_isolation.py` | 4 | 도메인 격리 확장 |
| R4 | `test_u_out_01_03_output_contract.py` | 3 | 출력 계약 |
| R5 | `test_d_loc_01_blank_finder.py` | 1 | BlankFinder |
| R6 | `test_d_mis_01_missing_numbers.py` | 1 | MissingNumberFinder |
| R7 | `test_d_val_01_06_validator.py` | 6 | Validator 6조건 |
| R8 | `test_d_sol_01_04_solver.py` | 4 | Solver |

**RED 커밋 권장 순서**: R1 → R2 → R3 → (R5, R6, R7, R8) → R4  
(출력 계약 R4는 RED를 먼저, GREEN은 Solver(G27) 이후)

### 6.2 결함 목록 (DEF-001~008)

RED 단계에서 8건의 결함을 공식 등록.

| ID | Severity | 근본 원인 |
|---|---|---|
| DEF-001~006, 008 | Critical/High | `validate_grid`가 RED stub으로 고정 반환 |
| DEF-007 | Critical | `cli.solve`가 검증 전 `resolve()` 선호출 |

> **TDD의 의미**: 결함 목록이 곧 "다음에 구현해야 할 것의 명세"가 된다.  
> FAILED 테스트 = 구현되지 않은 요구사항의 실행 가능한 문서.

---

## 7. Phase 4 — GREEN: 최소 구현

### 7.1 GREEN G01~G33 순서 및 원칙

**의존성 원칙**: 입력 검증 → 격리 → Entity 기초 → Validator → Solver → 출력

| Phase | G# | 범위 | 핵심 구현 |
|---|---|---|---|
| Phase 1 | G01~G09 | FR-01 크기·격리 | `validate_grid`, `cli.solve` |
| Phase 2 | G10~G14 | FR-01 추가 검증 | blank·범위·중복 에러 |
| Phase 3 | G15~G18 | 격리 확장 | E002·E004·E005 resolve 격리 |
| Phase 4 | G19~G30 | Domain Entity/Control | BlankFinder·Validator·Solver |
| Phase 5 | G31~G33 | Boundary 출력 | 출력 계약 완성 |

**GREEN 단계 규칙**:
- 한 GREEN 커밋 = 한 테스트(또는 동일 분기 묶음)만 통과시키는 최소 구현
- REFACTOR·설계 개선·다른 AC 선행 구현 금지

### 7.2 ECB 아키텍처 구현 결과

```
magic_square/
├── entity/
│   ├── constants.py   ← GRID_SIZE, MAGIC_CONSTANT = magic_constant(4)
│   └── user.py        ← User frozen dataclass + identity invariant
├── control/
│   ├── validator.py   ← is_magic_square() + 5개 독립 검증 함수
│   ├── solver.py      ← solution() — Step A/B fallback
│   ├── blank_finder.py
│   └── missing_number_finder.py
└── boundary/
    ├── input_validator.py  ← validate_grid() -> ValidationFailure | None
    ├── cli.py              ← solve() 진입점
    ├── display.py          ← format_board(), format_solution()
    ├── models.py           ← ValidationFailure (Pydantic)
    └── gui.py              ← PyQt6 GUI (coverage omit)
```

### 7.3 핵심 코드: Magic Constant 유도 (Level 2 준수)

```python
# entity/constants.py — 하드코딩 금지, 크기로 유도
GRID_SIZE: int = 4
MAGIC_CONSTANT: int = GRID_SIZE * (GRID_SIZE ** 2 + 1) // 2  # 34
```

### 7.4 핵심 코드: 검증 함수 완전 분리 (Level 1 준수)

```python
# control/validator.py — 10개 조건 각각 독립 함수
def is_magic_square(matrix: Board) -> bool:
    if not _shape_valid(matrix):      # Level 0
        return False
    return (
        _composition_valid(matrix)    # Level 0: 1~16 중복 없음
        and _rows_valid(matrix)       # Level 1: 행 4개
        and _cols_valid(matrix)       # Level 1: 열 4개
        and _main_diagonal_valid(matrix)   # Level 1: 주대각선
        and _anti_diagonal_valid(matrix)   # Level 1: 반대각선
    )
```

---

## 8. Phase 5 — REFACTOR & Code Review

### 8.1 REFACTOR M6 (GREEN 전체 완료 후)

| 작업 | 내용 | 상태 |
|---|---|---|
| `NOT_IMPLEMENTED` 제거 | `validate_grid() -> ValidationFailure \| None` 시그니처 정리 | ✅ |
| `_shape_valid()` 추가 | 비정형 격자에서 IndexError 방지 | ✅ |
| Entity constants SSOT | `_GRID_SIZE=4` 중복 제거, entity 상수 단일 출처 | ✅ |
| Error messages SSOT | `boundary/error_messages.py` | ✅ |
| RED stub 제거 | `NOT_IMPLEMENTED` 잔여물 정리 | ✅ |
| Golden Master | baseline 불변 유지 | ✅ |
| Coverage ≥80% | `gui.py`·`__main__.py` omit 후 기준 통과 | ✅ |

### 8.2 Code Review 결과 (Code Reviewer 서브에이전트 위임)

**전체 평가**: 핵심 불변 조건을 대체로 잘 지킨 성숙한 코드베이스  
**금지 패턴 5종 위반**: **0건**

| 패턴 | 결과 |
|---|---|
| 목적/수단 혼동 (`make_magic_square` 등) | 통과 |
| Magic Constant `34` 하드코딩 | 통과 (`.py`에 `34` 리터럴 없음) |
| 부분 검증 (행만 검사) | 통과 |
| display에 검증/생성 로직 | 통과 |
| 무기준 루프 | 통과 |

**잘 된 점**:
- `magic_constant(n)` 유도식으로 SSOT 달성
- validator 5개 독립 함수 + `is_magic_square` 조합
- `test_u_flow_02` — invalid 시 `resolve` 미호출 spy 검증
- Golden Master 시나리오 기반 end-to-end 회귀 테스트

**개선 항목 (P0 완료, P1~P2 백로그)**:

| 우선순위 | 이슈 | 상태 |
|---|---|---|
| P0 | `validate_grid` NOT_IMPLEMENTED 제거 | ✅ REFACTOR에서 해소 |
| P0 | `_shape_valid()` 추가 — IndexError 방지 | ✅ REFACTOR에서 해소 |
| P1 | Solver G1 하드코딩 제거 | 백로그 |
| P1 | 주/반대각선 독립 negative 테스트 추가 | 백로그 |
| P2 | `GRID_SIZE**2` SSOT 통일 | 백로그 |

---

## 9. 핵심 인사이트

### 9.1 "불변 조건을 먼저 선언한다"는 원칙이 모든 것을 바꿨다

```
❌ 일반적 접근:
  "어떻게 마방진을 만들까?" → 코드 직행 → 테스트 후작성

✅ 이 프로젝트의 접근:
  "무엇이 참이어야 하는가?" → Invariant 선언 → Test List → 구현
```

Invariant를 먼저 선언했기 때문에:
- 테스트 ID(D-VAL-01~06)와 코드(`_rows_valid` 등)가 1:1 대응
- "왜 이 테스트가 여기 있는가?"에 항상 답할 수 있는 추적 가능성 확보
- 리팩터 후에도 테스트가 의미를 잃지 않음

### 9.2 Cursor Rules가 "AI 드리프트"를 차단한다

AI 어시스턴트는 매 세션 초기화 시 프로젝트 문맥을 잃고 구현 직행 패턴으로 회귀한다.  
Rules의 `alwaysApply`는 이를 구조적으로 차단한다.

| Rules 없이 | Rules 있으면 |
|---|---|
| "마방진을 만드는 함수 짜줘" → 코드 직행 | Invariant 계층 확인 → 계약 먼저 |
| `if sum == 34` 하드코딩 | `MAGIC_CONSTANT = magic_constant(4)` |
| `validate()`가 `generate()`를 호출 | ECB 경계 위반으로 경고 |

### 9.3 Dual-Track TDD의 실용적 가치

Track A(Boundary)와 Track B(Domain)를 분리하면:

```
Track A RED 먼저 → 입출력 계약이 확정됨
                → Track B가 계약을 믿고 순수 로직에 집중 가능
```

- Track A는 `spy`/`mock`으로 Domain을 격리
- Track B는 Mock 없이 순수 로직만 검증
- 두 트랙의 GREEN이 만나는 지점 = 통합 완성

### 9.4 결함 목록(Defect List)이 "실행 가능한 스프린트 계획"이 된다

```
RED 8건 FAILED → defect_list.md 등록 (DEF-001~008)
             → 근본 원인 그룹화 (G-1: input_validator / G-2: cli.py)
             → GREEN 작업 명세로 직결
```

전통적 개발에서 결함 목록은 구현 이후에 등장한다.  
TDD에서 결함 목록은 구현 이전에 작성되어 구현 명세가 된다.

### 9.5 Sub-agents를 통한 역할 분리가 품질을 높인다

Code Reviewer 서브에이전트를 통한 리뷰:
- 개발자가 놓친 P0 이슈(IndexError, NOT_IMPLEMENTED 역설)를 독립적으로 발견
- "측정→가설→수정→재측정" 사이클을 체계화
- 리뷰 기준이 프롬프트가 아닌 파일(`.cursor/agents/code-reviewer.md`)로 고정됨

### 9.6 Prompt Engineering이 TDD 설계 문서의 품질을 결정한다

TDD 설계 문서를 생성하는 프롬프트 자체에도 TDD 원칙을 적용했다:

```
프롬프트 설계 원칙:
1. 전제(Given)의 명시적 고정 — Invariant를 변경 불가 블록으로 삽입
2. 출력 형식 강제 (Schema 주도) — SECTION 1~7 채우기 방식
3. 금지 사항 명시 — "하지 말 것"이 "할 것"보다 통제력이 강함
4. 추적 가능성 강제 — 모든 테스트에 출처 Invariant 부기
5. Done의 사전 정의 — "언제 완성인가"를 프롬프트에서 먼저 선언
```

### 9.7 "표면과 본질의 구분"이 설계의 시작이다

```
표면: 마방진을 만드는 것
본질: 제약 조건의 완전한 집합을 먼저 선언하고,
      그것을 독립적으로 생성·검증·표현할 수 있는 시스템을 설계할 수 있는가
```

이 구분이 없으면:
- `display()`에서 `validate()`를 호출하게 됨 (책임 혼재)
- `34`를 하드코딩하게 됨 (본질인 공식 은폐)
- 행 합만 검사하게 됨 (조건 생략)

---

## 10. 복습 체크리스트

### 10.1 문제 정의

- [ ] "무엇을 만드는가"와 "무엇이 참이어야 하는가"의 차이를 설명할 수 있는가?
- [ ] Invariant Level 0~3이 각각 무엇을 의미하는지 기술할 수 있는가?
- [ ] 표면 문제 정의의 결함 6가지를 나열할 수 있는가?
- [ ] Magic Constant 34가 어떻게 유도되는지 공식으로 설명할 수 있는가?

### 10.2 Cursor 환경 설계

- [ ] Cursor Rules의 `alwaysApply`와 glob 한정의 차이와 선택 기준은?
- [ ] Sub-agent의 `readonly: true`는 언제 사용하는가?
- [ ] Rules와 Sub-agents의 역할 차이("항상적 원칙" vs "위임 가능한 역할")는?
- [ ] Sub-agent `description`에 위임 신호를 넣는 이유는?

### 10.3 TDD RED-GREEN-REFACTOR

- [ ] RED 단계에서 커밋하는 이유는?
- [ ] GREEN 단계에서 "최소 구현"의 의미는?
- [ ] Dual-Track TDD에서 Track A와 Track B를 분리하는 이유는?
- [ ] 결함 목록(DEF-*)이 구현 명세가 되는 원리는?
- [ ] `conftest.py`에서 픽스처(G0~G3)를 미리 정의하는 이유는?

### 10.4 ECB 아키텍처

- [ ] Entity / Control / Boundary 각 계층의 책임은?
- [ ] `validate()`가 `generate()`를 import하면 안 되는 이유는?
- [ ] `display()`에서 검증 로직을 포함하면 어떤 문제가 생기는가?
- [ ] Partial Solver가 Level 3 예외를 허용받는 근거는?

### 10.5 Code Review

- [ ] 금지 패턴 5종을 코드 예시와 함께 설명할 수 있는가?
- [ ] P0/P1/P2 우선순위 분류 기준은?
- [ ] `NOT_IMPLEMENTED`를 성공 센티널로 사용하면 안 되는 이유는?
- [ ] Golden Master 테스트의 역할은?

---

## 11. 산출물 전체 목록

### 11.1 보고서 (Report/)

| 번호 | 파일 | 내용 |
|---|---|---|
| 01 | `problem-definition-report.md` | STEP 1~5 문제 정의 완료 |
| 02 | `tdd-design-prompt-report.md` | TDD 설계 프롬프트 설계 보고서 |
| 03 | `user-domain-extension.md` | User 도메인 확장 정의 |
| 04 | `user-test-list.md` | User 테스트 목록 |
| 05 | `cursorrules-design-report.md` | Cursor Rules 5개 설계 근거 |
| 06 | `role-subagents-design-report.md` | Sub-agents 8개 설계 근거 |
| 07 | `user-journey.md` | 사용자 여정 |
| 08 | `prd-reference-document-analysis.md` | PRD 참고 분석 |
| 09 | `product-requirements-document.md` | PRD v1.0 (13섹션) |
| 10 | `prd-boundary-red-qa-report.md` | PRD·RED·QA 통합 보고서 |
| 11 | `dual-track-red-design-report.md` | Dual-Track RED 설계표 |
| 12 | `code-review-report.md` | GREEN 이후 전체 코드 리뷰 |
| **13** | **`final-tdd-with-cursor-report.md`** | **본 최종 보고서** |

### 11.2 Cursor 환경 파일

| 경로 | 파일 수 | 역할 |
|---|---|---|
| `.cursor/rules/` | 5개 `.mdc` | 프로젝트 AI 가이드라인 (항상 적용) |
| `.cursor/agents/` | 8개 `.md` | 역할 기반 서브에이전트 |

### 11.3 소스 코드

| 경로 | 파일 | 역할 |
|---|---|---|
| `magic_square/entity/` | `constants.py`, `user.py` | 도메인 상수·객체 |
| `magic_square/control/` | `validator.py`, `solver.py`, `blank_finder.py`, `missing_number_finder.py` | 유즈케이스 로직 |
| `magic_square/boundary/` | `input_validator.py`, `cli.py`, `display.py`, `models.py`, `gui.py` | 입출력 계층 |

### 11.4 테스트 파일

| 경로 | 파일 | 건수 | 트랙 |
|---|---|---|---|
| `tests/boundary/` | `test_ac_fr_01_01_*` | 9 | A |
| `tests/boundary/` | `test_u_in_04_08_*` | 5 | A |
| `tests/boundary/` | `test_u_flow_02_*` | 4 | A |
| `tests/boundary/` | `test_u_out_01_03_*` | 3 | A |
| `tests/boundary/` | `test_display.py` | 4 | A |
| `tests/boundary/` | `test_golden_master_*` | 6 | GM |
| `tests/boundary/` | `test_validate_grid_success.py` | 1 | A |
| `tests/entity/` | `test_d_loc_01_*` | 1 | B |
| `tests/entity/` | `test_d_mis_01_*` | 1 | B |
| `tests/entity/` | `test_d_val_01_06_*` | 9 | B |
| `tests/entity/` | `test_d_sol_01_04_*` | 4 | B |
| `tests/entity/` | `test_user.py` | 13 | B |
| `tests/entity/` | `test_constants.py` | 2 | B |
| **합계** | | **62** | |

---

## 종합 — 한 줄로 남기는 본질

> **"만든다"는 말 뒤에 숨어 있는 "무엇이 참이어야 하는가"를  
> 먼저 선언하고, 그것을 실행 가능한 테스트로 증명한 다음,  
> 그 테스트를 통과시키는 최소 코드를 작성한다.**  
> **Cursor는 이 사고 과정을 방해받지 않고 유지하기 위한 환경 설계 도구다.**

---

*Report/13-final-tdd-with-cursor-report.md — 2026-05-29*
