# 4×4 Magic Square — Cursor Rules 설계 보고서

**작성일**: 2026-05-28
**단계**: STEP 5 이후 — 프로젝트 AI 가이드라인 선언
**선행 산출물**: `Report/01-problem-definition-report.md` (STEP 1~5), `Report/03-user-domain-extension.md`, `Report/04-user-test-list.md`
**목적**: 본 프로젝트의 AI 코딩 어시스턴트가 일관되게 따라야 할 규칙 파일(`.cursor/rules/*.mdc`)의 설계 근거와 구조를 기록한다.

---

## 0. 본 보고서의 범위

| 구분 | 위치 |
|---|---|
| Cursor Rules 파일 (산출물) | `.cursor/rules/*.mdc` (5개) |
| Rules 설계 보고서 (본 문서) | `Report/05-cursorrules-design-report.md` |
| 설계 대화 재현 | `Prompt/04-cursorrules-design-transcript.md` |

---

## 1. 설계 배경

STEP 1~5의 문제 정의, ECB 아키텍처, TDD 설계, User 도메인 확장을 거쳐
프로젝트의 핵심 원칙이 다음과 같이 확정되었다.

```
문제 정의 → Invariant Level 0~3 확정
ECB 분리  → generate / validate / display 독립
TDD       → 불변 조건 먼저 선언, 테스트 목록 = 완성 기준
금지 사항 → 하드코딩, 책임 혼재, 조건 생략, 성공 기준 없는 루프
```

이 원칙들을 매 세션마다 프롬프트로 반복 입력하지 않도록,
`.cursor/rules/` 에 영구 가이드라인으로 선언한다.

---

## 2. 생성된 Rules 파일 목록

| 번호 | 파일명 | 적용 범위 | 핵심 역할 |
|---|---|---|---|
| 1 | `magicsquare-project.mdc` | `alwaysApply: true` | 문제 정의 핵심·Invariant 레벨·훈련 목표 상시 제공 |
| 2 | `magicsquare-ecb-architecture.mdc` | `**/*.py` | ECB 3계층 책임 분리 원칙 및 도메인 엔티티 목록 |
| 3 | `magicsquare-forbidden.mdc` | `alwaysApply: true` | 안티패턴 5종 금지 (하드코딩·책임혼재·조건생략 등) |
| 4 | `magicsquare-python-code-style.mdc` | `**/*.py` | 타입 힌트·Magic Constant 유도·모듈 구조·네이밍 |
| 5 | `magicsquare-tdd-testing.mdc` | `**/test_*.py` | Invariant 계층별 테스트 순서·픽스처 분리 규칙 |

---

## 3. 각 Rules 파일의 설계 근거

### 3-1. `magicsquare-project.mdc` (alwaysApply)

**문제 의식**
AI 어시스턴트가 매 세션 초기화 시 프로젝트 문맥을 잃으면,
"마방진을 만드는" 표면 정의로 회귀하여 구현 직행 패턴이 반복된다.

**설계 결정**
STEP 5에서 확정한 개선된 문제 정의, Invariant 4개 레벨, 훈련 목표 5가지,
핵심 수치(880개 해, Magic Constant 공식)를 항상 적용 컨텍스트로 주입한다.

**포함 내용**
- 개선된 문제 정의 ("만든다"가 아니라 "존재하는가를 판단하고 다룰 수 있는가")
- Invariant Level 0~3 테이블
- 훈련 목표 5가지
- 핵심 수치 (16!, 880, 34, 조건 10개)

---

### 3-2. `magicsquare-ecb-architecture.mdc` (*.py)

**문제 의식**
Python 파일 작성 시 `generate()`, `validate()`, `display()`가 하나의 함수나
하나의 파일에 뒤섞이는 경향이 STEP 4에서 구조적 문제로 확인되었다.

**설계 결정**
Python 파일에 한해 ECB 3계층 책임 경계를 코드 예시와 함께 명시한다.
Level 3 설계 불변 조건(검증은 생성 방식을 모른다)을 금지 규칙 형태로 서술한다.

**포함 내용**
- generate / validate / display 역할 테이블
- 도메인 엔티티 목록 (Board, Cell, Row, Column, Diagonal, MagicConstant)
- 올바른/잘못된 분리 코드 예시
- Level 3 설계 불변 조건 4가지

---

### 3-3. `magicsquare-forbidden.mdc` (alwaysApply)

**문제 의식**
STEP 2~4 분석에서 반복적으로 등장한 구조적 결함(완성 목적화, 하드코딩, 검증 은폐)이
구현 단계에서 코드로 재현될 위험이 있다.

**설계 결정**
문제 정의 단계에서 도출된 안티패턴 5종을 코드 수준의 ❌/✅ 예시로 명시한다.
alwaysApply로 설정하여 파일 종류와 무관하게 항상 경고한다.

**안티패턴 5종**
1. 목적·수단 혼동 (`make_magic_square()`)
2. Magic Constant 34 하드코딩
3. 검증 조건 부분 생략 (행만 검사)
4. display에서 검증·생성 로직 포함
5. 성공 기준 없는 무한 루프

---

### 3-4. `magicsquare-python-code-style.mdc` (*.py)

**문제 의식**
타입 힌트 부재, Magic Constant 하드코딩, 검증 함수의 단일 함수 묶음이
Python 파일에서 반복될 위험이 있다.

**설계 결정**
Python 파일에 한해 타입 힌트 필수화, Magic Constant 유도 방식, 모듈 구조,
검증 함수 독립 분리, 네이밍 규칙을 코드 예시와 함께 제시한다.

**포함 내용**
- `Board = list[list[int]]` 타입 별칭
- `magic_constant(n)` 유도 함수 패턴
- `magic_square/` 모듈 디렉토리 구조
- 검증 함수 5개 독립 분리 패턴
- 네이밍 규칙 테이블

---

### 3-5. `magicsquare-tdd-testing.mdc` (test_*.py)

**문제 의식**
테스트 파일 작성 시 Invariant 계층 순서를 무시하고 고수준 테스트만 작성하거나,
하나의 테스트에 여러 조건을 묶어 실패 원인이 불명확해지는 문제가 있다.

**설계 결정**
Level 0 → 1 → 2 → 3 순서의 테스트 작성 강제,
각 조건을 독립 테스트로 분리,
픽스처 명명 규칙으로 어떤 조건이 위반된 보드인지 이름에 명시한다.

**포함 내용**
- Level 0~3별 테스트 함수 목록
- 단일 Invariant 검증 원칙 (Good/Bad 예시)
- 유효·무효 픽스처 분리 규칙
- TDD 필연성 요약 1문장

---

## 4. Rules 적용 범위 설계 원칙

| 원칙 | 내용 |
|---|---|
| **항상 적용** | 프로젝트 문맥과 금지 패턴은 파일 종류와 무관하게 필요하다 |
| **파일 한정** | 코드 스타일·아키텍처·테스트 규칙은 해당 파일 작업 시에만 로드한다 |
| **중복 최소화** | alwaysApply 파일은 간결하게, 구체적 예시는 파일 한정 규칙에 배치한다 |
| **50줄 이내** | 각 규칙 파일은 핵심만 담아 AI 컨텍스트 낭비를 방지한다 |

---

## 5. 산출물 파일 구조

```
.cursor/
└── rules/
    ├── magicsquare-project.mdc          (alwaysApply: true)  ← 문제 정의 & Invariant
    ├── magicsquare-forbidden.mdc        (alwaysApply: true)  ← 안티패턴 금지
    ├── magicsquare-ecb-architecture.mdc (globs: **/*.py)     ← 책임 분리
    ├── magicsquare-python-code-style.mdc (globs: **/*.py)    ← 코드 스타일
    └── magicsquare-tdd-testing.mdc      (globs: **/test_*.py) ← 테스트 규칙
```

---

## 6. 다음 단계

본 Rules 선언 이후 진행 순서:

1. **RED 단계**: `tests/entity/test_user.py` 실행 (Identity-1~7 모두 FAILED)
2. **GREEN 단계**: `magic_square/entity/user.py` 구현 → pytest 통과
3. **REFACTOR**: 구조 개선 (필요 시)
4. **확장**: `generate()`, `validate()`, `display()` 각 모듈 TDD 진행

각 단계에서 `.cursor/rules/` 의 금지 패턴 위반 여부를 자가 점검한다.
