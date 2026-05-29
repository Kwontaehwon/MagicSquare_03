# 4×4 Magic Square — 역할 기반 서브에이전트 설계 대화형 프롬프트 트랜스크립트

**작성일**: 2026-05-28
**형식**: Cursor 커스텀 서브에이전트 7개 생성 세션의 대화 재현 (단일 요청 방식)
**선행 자산**:
- `Prompt/01-conversation-transcript.md` (STEP 1~5 문제 정의)
- `Prompt/03-tdd-design-prompt-transcript.md` (TDD 설계 프롬프트)
- `Prompt/04-cursorrules-design-transcript.md` (Cursor Rules 설계)
- `Report/05-cursorrules-design-report.md` (Cursor Rules 설계 보고서)
- `.cursor/agents/code-reviewer.md` (기존 서브에이전트 1개 — 동일 포맷의 레퍼런스)
**용도**: 동일한 7개 역할 서브에이전트 구성을 다른 세션 또는 다른 프로젝트에서 재현할 때 사용

---

## 사용 방법

본 트랜스크립트의 `[USER]` 블록을 순서대로 입력하면,
동일한 Cursor 서브에이전트 7개와 보고서·트랜스크립트가 재생성된다.
각 단계는 이전 단계 완료를 전제로 설계되어 있으므로 순서를 지켜주십시오.

---

## 선행 조건

본 트랜스크립트를 실행하기 전, 다음이 완료되어 있어야 한다.

- STEP 1~5 문제 정의 완료 — `Prompt/01-conversation-transcript.md`
- ECB 아키텍처 결정 — `Report/02-tdd-design-prompt-report.md`
- Cursor Rules 5개 선언 — `Report/05-cursorrules-design-report.md`
- 기존 서브에이전트 `.cursor/agents/code-reviewer.md` 존재 (동일 포맷 참고용)

---

---

## [USER] STEP 1 — 7개 역할 서브에이전트 일괄 생성 요청

```
아래에 있는 subagent를 만드려고해.

A-1. 시스템 최적화 엔지니어 에이전트
> 최적화 전문가: 애플리케이션의 작동을 원활하게 개선하고 속도를 빠르게 만들며
  병목 지점을 찾아서 해결하는 시스템 최적화 엔지니어

A-2. 사용자 경험 전문가 에이전트
> UX 디자이너: 사용자가 쉽고 편하게 이용할 수 있도록 화면 디자인, 버튼 배치,
  에러 메시지를 개선하는 사용자 경험 전문가.

A-3. 다중 에이전트 협업 (사용 시나리오)
> code-bug-analyzer로 '냉장고를 부탁해' 애플리케이션 코드 전체를 리뷰한 뒤,
  발견한 문제를 performance-optimizer가 수정해서 성능 최적화한 다음,
  ux-design-advisor가 사용자 경험을 개선하게 해 줘.

A-4. 제품 기획 관리자
> 전체 개발 일정을 관리하는 프로덕트 매니저로서 PRD를 작성하여 제품의 목표,
  기능, 사용자 요구사항을 정의한다

A-5. 백엔드 개발자
> 서버 아키텍처 설계, API 개발, 데이터 처리, 외부 서비스 통합, 보안 및 성능
  최적화를 담당하는 서버 사이드 개발 전문가.

A-6. 프런트엔드 개발자
> 사용자 인터페이스 설계 및 구현, 반응형 디자인, 웹 접근성, 성능 최적화를
  담당하는 클라이언트 사이드 개발 전문가.

A-7. 품질 보증 엔지니어
> 전체 시스템의 기능 테스트, 에러 처리 검증, 성능 최적화, 코드 리뷰를 수행하는
  품질 관리 전문가. 버그 발견, 사용성 개선사항 제안.

A-8. AI 통합 전문가
> LLM 및 AI 서비스 통합, 프롬프트 최적화, 모델 파인튜닝, AI 파이프라인 구축을
  담당하는 인공지능 전문가. 여기서는 OpenRouter API를 통해 DeepSeek 모델과
  연동하여 텍스트 생성, 요약을 구현하는 LLM 활용 전문가
```

### [ASSISTANT] 기대 응답 핵심 포인트

**클래리피케이션 단계 (Plan 모드)**

다음 두 가지를 사용자에게 묻는다.

1. **A-3 처리 방식**:
   - (a) `code-bug-analyzer` 를 신규 서브에이전트로 만든다
   - (b) 기존 `code-reviewer.md` 로 대체한다
   - (c) A-3 는 사용 시나리오일 뿐 별도 에이전트를 만들지 않는다
2. **에이전트 범위(scope)**:
   - (a) 범용(generic) 역할 정의만
   - (b) 본 워크스페이스 맞춤(MagicSquare 규칙 인용)
   - (c) 하이브리드 — 범용 역할 정의 + `.cursor/rules/` 준수 한 줄 명시

권장 응답: A-3 = (c) skip, scope = (c) hybrid.

**계획 단계 (Plan 모드)**

- `.cursor/agents/` 아래에 7개 신규 파일을 영문 kebab-case 로 생성
- frontmatter 는 공식 5필드만 사용 (`name`, `description`, `model: inherit`, `readonly: false`, 필요 시 `is_background`)
- 본문은 6개 표준 섹션으로 통일
  - `## 핵심 책임`
  - `## 작업 원칙`
  - `## 체크리스트`
  - `## 출력 형식`
  - `## 금지 사항`
  - `## 프로젝트 규칙 준수`

**구현 단계 (Agent 모드)**

7개 파일을 다음 순서로 생성한다.

| 순서 | 파일 | name |
|---|---|---|
| 1 | `performance-optimizer.md` | Performance Optimizer |
| 2 | `ux-design-advisor.md` | UX Design Advisor |
| 3 | `product-manager.md` | Product Manager |
| 4 | `backend-developer.md` | Backend Developer |
| 5 | `frontend-developer.md` | Frontend Developer |
| 6 | `qa-engineer.md` | QA Engineer |
| 7 | `ai-integration-specialist.md` | AI Integration Specialist |

**역할별 핵심 포함 사항**

- **performance-optimizer**: "측정 → 가설 → 수정 → 재측정" 사이클, 알고리즘·I/O·메모리·관측성 4영역 체크리스트, p50/p95/p99·throughput 표준 지표.
- **ux-design-advisor**: WCAG 2.1 AA, 정보 위계·인터랙션·에러 메시지·접근성 4영역 체크리스트, Before/After 근거 강제.
- **product-manager**: PRD 13개 섹션 표준, MoSCoW/RICE/Impact-Effort 우선순위 도구, 가정·미해결 질문 분리.
- **backend-developer**: 계약 우선·계층 분리·불변식·실패 설계, API/도메인/보안/신뢰성/관측성 5영역.
- **frontend-developer**: 컴포넌트=책임 단위, 표현/로직 분리, 접근성 옵션 아님, Core Web Vitals.
- **qa-engineer**: 등가분할·경계값·결정테이블 등 6대 기법, 결함 리포트 형식, **마방진 10개 조건 검사 명시**.
- **ai-integration-specialist**: 프롬프트는 코드, 출력 JSON 강제, LLM 비결정성 인정, 평가 우선, **OpenRouter+DeepSeek 표준 호출 패턴 의사코드 포함**.

**검증**

- `.cursor/agents/` 디렉토리에 8개 파일(기존 1 + 신규 7)이 모두 존재
- frontmatter 4필드(`name`, `description`, `model`, `readonly`)가 모든 파일 라인 2~5에 일치
- 본문 6개 섹션 모두 포함
- 모든 파일에 `.cursor/rules/` 참조 한 줄 존재
- 린트 오류 없음

---

---

## [USER] STEP 2 — 보고서 및 트랜스크립트 생성 요청

```
1. Report 폴더에 보고서 생성해줘
2. 현재까지의 프롬프트 전체를 대화형 프롬프트로 Prompt 폴더에 Export transcript 해줘
```

### [ASSISTANT] 기대 응답 핵심 포인트

**Report 폴더 신규 파일**
- `06-role-subagents-design-report.md`

**Prompt 폴더 신규 파일**
- `05-role-subagents-design-transcript.md`

**06-role-subagents-design-report.md 포함 내용**
- 본 보고서의 범위 (산출물 / 보고서 / 트랜스크립트 위치)
- 설계 배경 (rules vs agents 의 역할 구분, A-1~A-8 의 분류)
- 7개 신규 파일 + 1개 기존 파일 목록 테이블 (번호·파일명·역할·readonly·비고)
- 표준 설계 원칙 4개 (frontmatter 5필드, 본문 6섹션, readonly 정책, 프로젝트 규칙 연동)
- 각 에이전트별 문제 의식·설계 결정·포함 내용 (4-1 ~ 4-7)
- A-3 처리 방침 (별도 에이전트 미생성, 협업 흐름 정의)
- 적용 범위 설계 원칙 5가지
- 산출물 파일 구조 (디렉토리 트리)
- 검증 결과 표
- 다음 단계 (호출 검증 / A-3 리허설 / 산출물 품질 평가 / 도메인 정합성)

**05-role-subagents-design-transcript.md 포함 내용**
- 선행 조건 명시 (Rules 선언, code-reviewer.md 존재)
- STEP 1 실행 프롬프트 (8개 역할 일괄 정의)
- STEP 1 의 클래리피케이션 단계 (A-3 처리, scope 결정) 와 권장 응답
- STEP 1 의 7개 파일 생성 순서·name 매핑·역할별 핵심 포함 사항
- STEP 2 실행 프롬프트 (보고서·트랜스크립트 생성 요청)
- 각 단계별 기대 응답 핵심 포인트
- 최종 산출물 구조

---

---

## 최종 산출물 구조

```
c:\dev\MagicSquare_
├── .cursor/
│   ├── rules/
│   │   ├── magicsquare-project.mdc          (alwaysApply: true)
│   │   ├── magicsquare-forbidden.mdc        (alwaysApply: true)
│   │   ├── magicsquare-ecb-architecture.mdc (globs: **/*.py)
│   │   ├── magicsquare-python-code-style.mdc (globs: **/*.py)
│   │   └── magicsquare-tdd-testing.mdc      (globs: **/test_*.py)
│   │
│   └── agents/
│       ├── code-reviewer.md                 (readonly: true)   ← 기존
│       ├── performance-optimizer.md         (readonly: false)  ← A-1 신규
│       ├── ux-design-advisor.md             (readonly: false)  ← A-2 신규
│       ├── product-manager.md               (readonly: false)  ← A-4 신규
│       ├── backend-developer.md             (readonly: false)  ← A-5 신규
│       ├── frontend-developer.md            (readonly: false)  ← A-6 신규
│       ├── qa-engineer.md                   (readonly: false)  ← A-7 신규
│       └── ai-integration-specialist.md     (readonly: false)  ← A-8 신규
│
├── Report/
│   ├── 01-problem-definition-report.md
│   ├── 02-tdd-design-prompt-report.md
│   ├── 03-user-domain-extension.md
│   ├── 04-user-test-list.md
│   ├── 05-cursorrules-design-report.md
│   └── 06-role-subagents-design-report.md   ← 신규
│
└── Prompt/
    ├── 01-conversation-transcript.md
    ├── 02-cursor_4x4_magic_square_problem_definit.md
    ├── 03-tdd-design-prompt-transcript.md
    ├── 04-cursorrules-design-transcript.md
    └── 05-role-subagents-design-transcript.md  ← 신규
```

---

## 메타 노트

본 트랜스크립트는 **역할 기반 서브에이전트 설계 과정의 반복 재현**을 위해 작성되었습니다.

- STEP 1 프롬프트(8개 역할 정의)를 다른 세션에 붙여 넣고, 클래리피케이션 단계에서
  A-3 = skip, scope = hybrid 를 선택하면, 동일한 7개 서브에이전트 파일이 재생성됩니다.
- A-3 의 다중 에이전트 협업 시나리오는 별도 에이전트를 만들지 않고, 기존
  `code-reviewer.md` (`readonly: true`) → `performance-optimizer` → `ux-design-advisor`
  순서의 위임 흐름으로 실행하면 됩니다.
- 각 단계의 "기대 응답 핵심 포인트"는 생성된 서브에이전트 파일의 품질 평가 기준으로도
  사용할 수 있습니다 — 특히 `qa-engineer.md` 의 마방진 10개 조건 검사 명시,
  `ai-integration-specialist.md` 의 OpenRouter+DeepSeek 호출 패턴 의사코드 포함 여부.
