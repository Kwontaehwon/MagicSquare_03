# 4×4 Magic Square — Cursor Rules 설계 대화형 프롬프트 트랜스크립트

**작성일**: 2026-05-28
**형식**: Cursor Rules 설계 세션의 대화 재현 (단일 요청 방식)
**선행 자산**:
- `Prompt/01-conversation-transcript.md` (STEP 1~5 문제 정의)
- `Prompt/03-tdd-design-prompt-transcript.md` (TDD 설계 프롬프트)
- `Report/03-user-domain-extension.md` (User 도메인 확장)
- `Report/04-user-test-list.md` (User 테스트 목록)
**용도**: 동일한 Cursor Rules 구성을 다른 세션 또는 다른 프로젝트에서 재현할 때 사용

---

## 사용 방법

본 트랜스크립트의 `[USER]` 블록을 순서대로 입력하면,
동일한 Cursor Rules 파일 5개가 재생성된다.
각 단계는 이전 단계 완료를 전제로 설계되어 있으므로 순서를 지켜주십시오.

---

## 선행 조건

본 트랜스크립트를 실행하기 전, 다음이 완료되어 있어야 한다.

- STEP 1~5 문제 정의 완료 — `Prompt/01-conversation-transcript.md`
- Invariant Level 0~3 확정 — `Report/01-problem-definition-report.md`
- ECB 아키텍처 결정 — `Report/02-tdd-design-prompt-report.md`
- User 도메인 Invariant Level 4 확정 — `Report/03-user-domain-extension.md`

---

---

## [USER] STEP 1 — Cursor Rules 생성 요청

```
다음 구조로 .cursor/rules/ 안에 Cursor Rules 파일 5개를 생성해줘.

파일 목록:
1. magicsquare-project.mdc       — alwaysApply: true
2. magicsquare-ecb-architecture.mdc — globs: **/*.py
3. magicsquare-forbidden.mdc     — alwaysApply: true
4. magicsquare-python-code-style.mdc — globs: **/*.py
5. magicsquare-tdd-testing.mdc   — globs: **/test_*.py

각 파일의 내용 기준:
- magicsquare-project: STEP 5의 개선된 문제 정의, Invariant Level 0~3, 훈련 목표 5가지, 핵심 수치
- magicsquare-ecb-architecture: generate/validate/display 책임 분리, 도메인 엔티티, Level 3 설계 불변 조건
- magicsquare-forbidden: 하드코딩 금지, 목적·수단 혼동, 조건 부분 생략, display에서 검증 포함, 성공 기준 없는 루프 — 각각 코드 예시 포함
- magicsquare-python-code-style: 타입 힌트, Magic Constant 유도 함수, 모듈 구조, 검증 함수 독립 분리, 네이밍 규칙
- magicsquare-tdd-testing: Invariant 계층별 테스트 순서, 단일 조건 테스트 원칙, 픽스처 분리 규칙

각 파일은 50줄 이내로 간결하게 작성하고, 코드 예시는 ❌/✅ 형태로 포함하라.
```

### [ASSISTANT] 기대 응답 핵심 포인트

- `.cursor/rules/` 디렉토리 생성
- 5개 `.mdc` 파일 각각 YAML frontmatter (`description`, `globs` 또는 `alwaysApply`) 포함
- `magicsquare-project`: 개선된 정의 인용문, Invariant 레벨 테이블, 수치 명시
- `magicsquare-ecb-architecture`: `generate() / validate() / display()` 분리 코드 예시
- `magicsquare-forbidden`: 5종 안티패턴 ❌ → ✅ 코드 쌍
- `magicsquare-python-code-style`: `Board = list[list[int]]` 타입 별칭, 모듈 구조 트리
- `magicsquare-tdd-testing`: Level 0 → 1 → 2 → 3 테스트 함수 목록, 픽스처 명명 규칙

---

---

## [USER] STEP 2 — 보고서 및 트랜스크립트 생성 요청

```
1. Report 폴더에 보고서 생성해줘
2. 현재까지의 프롬프트 전체를 대화형 프롬프트로 Prompt 폴더에 Export transcript 해줘
각 문서는 작성된 순서대로 번호가 있어야해.
```

### [ASSISTANT] 기대 응답 핵심 포인트

**Report 폴더 번호 부여**
- 기존 파일 4개를 01~04 접두사로 리네이밍
- 새 보고서: `05-cursorrules-design-report.md`

**Prompt 폴더 번호 부여**
- 기존 파일 3개를 01~03 접두사로 리네이밍
- 새 트랜스크립트: `04-cursorrules-design-transcript.md`

**05-cursorrules-design-report.md 포함 내용**
- 설계 배경 (매 세션 컨텍스트 손실 문제)
- 5개 Rules 파일 목록 테이블 (번호·파일명·적용 범위·역할)
- 각 파일별 문제 의식·설계 결정·포함 내용 (3-1 ~ 3-5)
- 적용 범위 설계 원칙 4가지
- 산출물 파일 구조 (디렉토리 트리)
- 다음 단계 (RED → GREEN → REFACTOR → 확장)

**04-cursorrules-design-transcript.md 포함 내용**
- 선행 조건 명시
- STEP 1 실행 프롬프트 (Rules 생성 요청 전체)
- STEP 2 실행 프롬프트 (보고서·트랜스크립트 생성 요청)
- 각 단계별 기대 응답 핵심 포인트

---

---

## 최종 산출물 구조

```
c:\dev\MagicSquare_
├── .cursor/
│   └── rules/
│       ├── magicsquare-project.mdc          (alwaysApply: true)
│       ├── magicsquare-forbidden.mdc        (alwaysApply: true)
│       ├── magicsquare-ecb-architecture.mdc (globs: **/*.py)
│       ├── magicsquare-python-code-style.mdc (globs: **/*.py)
│       └── magicsquare-tdd-testing.mdc      (globs: **/test_*.py)
│
├── Report/
│   ├── 01-problem-definition-report.md
│   ├── 02-tdd-design-prompt-report.md
│   ├── 03-user-domain-extension.md
│   ├── 04-user-test-list.md
│   └── 05-cursorrules-design-report.md      ← 신규
│
└── Prompt/
    ├── 01-conversation-transcript.md
    ├── 02-cursor_4x4_magic_square_problem_definit.md
    ├── 03-tdd-design-prompt-transcript.md
    └── 04-cursorrules-design-transcript.md  ← 신규
```

---

## 메타 노트

본 트랜스크립트는 **Cursor Rules 설계 과정의 반복 재현**을 위해 작성되었습니다.
STEP 1 프롬프트를 다른 세션에 붙여 넣으면, 동일한 5개 Rules 파일이 재생성됩니다.
각 단계의 "기대 응답 핵심 포인트"는 생성된 Rules 파일의 품질 평가 기준으로도 사용할 수 있습니다.
