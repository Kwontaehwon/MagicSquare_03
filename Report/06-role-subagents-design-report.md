# 4×4 Magic Square — 역할 기반 서브에이전트 설계 보고서

**작성일**: 2026-05-28
**단계**: Cursor Rules 선언 이후 — 역할 기반 협업 에이전트 도입
**선행 산출물**: `Report/05-cursorrules-design-report.md` (Cursor Rules 5종), `.cursor/agents/code-reviewer.md` (기존 1개)
**목적**: 본 프로젝트에서 다양한 역할(성능·UX·PM·BE·FE·QA·AI 통합)을 수행할 Cursor 커스텀 서브에이전트 7개의 설계 근거와 구조를 기록한다.

---

## 0. 본 보고서의 범위

| 구분 | 위치 |
|---|---|
| 서브에이전트 파일 (산출물) | `.cursor/agents/*.md` (신규 7개 + 기존 1개) |
| 서브에이전트 설계 보고서 (본 문서) | `Report/06-role-subagents-design-report.md` |
| 설계 대화 재현 | `Prompt/05-role-subagents-design-transcript.md` |

---

## 1. 설계 배경

`.cursor/rules/` 가 "프로젝트의 항상적인 원칙"을 선언한다면,
`.cursor/agents/` 는 "특정 작업을 위임할 전문 역할"을 선언한다.

학습 과제 A-1 ~ A-8 에서 8개의 역할이 제시되었으며, 그 중 7개는 역할 정의 형태로,
1개(A-3)는 다중 에이전트 협업 사용 시나리오 형태로 주어졌다.

```
역할 정의 (서브에이전트 신규 생성 대상): A-1, A-2, A-4, A-5, A-6, A-7, A-8 — 7개
사용 시나리오 (별도 산출물 없음):       A-3
```

매 세션마다 "당신은 ~ 전문가입니다, 다음 체크리스트를 점검하세요..." 같은 프롬프트를
반복 입력하지 않도록, Cursor 공식 [Subagents 스펙](https://cursor.com/docs/subagents.md)에
따라 `.cursor/agents/` 에 영구 역할 정의로 선언한다.

---

## 2. 생성된 서브에이전트 파일 목록

| 번호 | 파일명 | 역할 | readonly | 비고 |
|---|---|---|---|---|
| 기존 | `code-reviewer.md` | Code Reviewer | `true` | 검토 전용 — Rules 설계 단계에서 생성 |
| A-1 | `performance-optimizer.md` | Performance Optimizer | `false` | 측정→가설→수정→재측정 사이클 |
| A-2 | `ux-design-advisor.md` | UX Design Advisor | `false` | WCAG 2.1 AA 기준 점검 |
| A-4 | `product-manager.md` | Product Manager | `false` | PRD 13개 섹션 표준 |
| A-5 | `backend-developer.md` | Backend Developer | `false` | 계약 우선·계층 분리·관측성 |
| A-6 | `frontend-developer.md` | Frontend Developer | `false` | a11y·성능·디자인 토큰 |
| A-7 | `qa-engineer.md` | QA Engineer | `false` | 마방진 10개 조건 검사 명시 |
| A-8 | `ai-integration-specialist.md` | AI Integration Specialist | `false` | OpenRouter + DeepSeek 표준 패턴 |

---

## 3. 표준 설계 원칙

### 3-1. Frontmatter 필드 (5필드만 사용)

Cursor 공식 스펙에 명시된 필드 외에는 사용하지 않는다.

```yaml
---
name: <표시 이름>
description: <언제 호출해야 하는지 위임 신호 포함>
model: inherit
readonly: false
---
```

- `tools`, `color` 등 비공식 필드는 사용 금지.
- `description` 끝에는 "~ 적극 활용하세요" 같은 위임 신호를 포함한다 (Cursor 공식 모범 사례).

### 3-2. 본문 6개 표준 섹션

```
# {역할 이름}
당신은 ...

## 핵심 책임
## 작업 원칙
## 체크리스트
## 출력 형식
## 금지 사항
## 프로젝트 규칙 준수
```

역할별로 필요한 보조 섹션(예: `product-manager.md` 의 PRD 표준 구조,
`ai-integration-specialist.md` 의 OpenRouter+DeepSeek 호출 표준 패턴)을 6섹션 사이에 추가한다.

### 3-3. readonly 정책

| 정책 | 적용 대상 | 이유 |
|---|---|---|
| `readonly: true` | 검토·감사·리뷰 전용 (`code-reviewer.md`) | 코드를 직접 수정하지 않는 역할 |
| `readonly: false` | 신규 7개 모두 | A-3 협업 시나리오에서 직접 수정·구현이 전제됨 |

### 3-4. 프로젝트 규칙 연동 (하이브리드)

각 에이전트 본문 마지막에 다음 한 줄로 `.cursor/rules/` 와 연결한다.

```
- `.cursor/rules/` 의 모든 `.mdc` 규칙을 준수한다.
```

추가로 본 워크스페이스(MagicSquare) 도메인 규약(예: Magic Constant 유도, ECB 책임 분리,
10개 조건 검사)을 위반하지 않도록 역할별로 한 줄을 더 명시한다. 특히
`qa-engineer.md` 는 마방진 10개 조건 검사를 검증 항목으로 명시 포함한다.

---

## 4. 각 에이전트의 설계 근거

### 4-1. `performance-optimizer.md` (A-1)

**문제 의식**
"느려 보인다"는 직관에 기반한 수정, 측정 없는 캐시·인덱스 도입, 정확성을 깨는
미세 최적화는 시스템을 더 취약하게 만든다.

**설계 결정**
"측정 → 가설 → 수정 → 재측정" 사이클을 첫 번째 작업 원칙으로 박고,
Before/After 수치 비교를 출력 형식의 필수 항목으로 만든다.

**포함 내용**
- 알고리즘·자료구조 / I/O·네트워크·DB / 메모리·자원 / 관측성 4영역 체크리스트
- p50/p95/p99·throughput·RSS 등 표준 지표 명시
- 트레이드오프(잃은 것 / 얻은 것) 보고 강제

---

### 4-2. `ux-design-advisor.md` (A-2)

**문제 의식**
"보기 좋다" 같은 취향 기반 변경, 접근성을 후순위로 미루는 관행, 화면 단위로만
평가하고 사용자 흐름을 무시하는 평가가 빈번하다.

**설계 결정**
"보기 좋다"보다 "이해하기 쉽다 + 실수가 줄어든다"를 우선한다는 원칙을 명시.
WCAG 2.1 AA 항목을 체크리스트의 독립 영역으로 둔다.

**포함 내용**
- 정보 위계·인터랙션·에러 메시지·접근성 4영역 체크리스트
- WCAG 핵심 항목(대비비, 키보드 도달, ARIA, label 연결, prefers-reduced-motion)
- Before/After 근거(휴리스틱·기준) 보고 형식

---

### 4-3. `product-manager.md` (A-4)

**문제 의식**
사용자 부재 PRD, 측정 불가능한 성공 기준, 우선순위 없는 요구사항 나열이
"PRD"라는 이름으로 통과되는 일이 많다.

**설계 결정**
PRD 13개 섹션 표준을 박아 두고, 모든 요구사항에 P0/P1/P2 부여를 강제한다.
가정(Assumption)과 미해결 질문(Open Questions)을 명시적으로 분리한다.

**포함 내용**
- TL;DR · 배경 · 목표/비목표 · 사용자 · 시나리오 · 기능/비기능 요구사항 · 성공 지표
- MoSCoW / RICE / Impact-Effort 도구
- 본 워크스페이스의 "성공 기준 사전 정의" 원칙과 정렬

---

### 4-4. `backend-developer.md` (A-5)

**문제 의식**
도메인 로직이 컨트롤러에 직접 작성되거나, 외부 호출에 타임아웃·재시도가 없거나,
비밀이 코드/로그에 노출되는 등의 회귀가 흔하다.

**설계 결정**
"계약 우선 → 계층 분리 → 불변식 명시 → 외부 입력은 신뢰 불가 → 실패는 평범하다"
6개 작업 원칙을 박는다.

**포함 내용**
- API 설계 / 도메인·데이터 / 보안 / 신뢰성·성능 / 관측성 5영역 체크리스트
- 마이그레이션의 안전성·롤백 가능성 강조
- 본 워크스페이스의 ECB 책임 분리를 백엔드 모듈 경계에도 적용

---

### 4-5. `frontend-developer.md` (A-6)

**문제 의식**
디자인 토큰을 우회한 하드코딩, "다음 스프린트로" 미루는 접근성, 측정 없는 성능
최적화, JSX 안의 비즈니스 로직 등이 반복되는 경향이 있다.

**설계 결정**
"컴포넌트 = 책임 단위, 표현/로직 분리, 접근성은 옵션이 아니다, 성능은 지표로 말한다"
는 작업 원칙을 명시한다. Core Web Vitals 를 판단 기준으로 둔다.

**포함 내용**
- 컴포넌트 구조 / 상태 관리 / 반응형 / 접근성 / 성능 / 디자인 시스템 6영역 체크리스트
- LCP·CLS·INP·TBT 명시
- 본 워크스페이스의 표현(display) 책임 분리 규약 적용

---

### 4-6. `qa-engineer.md` (A-7)

**문제 의식**
성공 기준 없는 통과 처리, 재현 불가능한 결함 등록, 외부 상태에 의존한 플레이키
테스트, 한 테스트의 다중 검증이 품질 게이트를 약화시킨다.

**설계 결정**
"성공 기준이 먼저", "결함은 재현 가능해야 한다", "단일 어서션/단일 시나리오" 원칙을
박고, 본 워크스페이스의 10개 조건 검사를 검증 항목으로 명시한다.

**포함 내용**
- 등가 분할 · 경계값 · 결정 테이블 · 상태 전이 · 오류 추측 · 페어와이즈 6대 기법
- 결함 리포트 표준 형식 (요약 / 환경 / 재현 / 기대 vs 실제 / 증거 / 회귀)
- 마방진 도메인 검증 4항목:
  - Magic Constant 유도식 (`n * (n ** 2 + 1) // 2`)
  - 행 4 + 열 4 + 대각선 2 + 구성(Level 0) = **10개 조건**
  - generate / validate / display 책임 분리
  - 사전 정의된 성공 기준 존재

---

### 4-7. `ai-integration-specialist.md` (A-8)

**문제 의식**
LLM 출력의 비결정성을 무시한 채 후처리 없이 다운스트림에 흘려보내거나,
API 키를 하드코딩하거나, 평가 없이 "프롬프트가 좋아졌다"고 주장하는 회귀가 흔하다.

**설계 결정**
"프롬프트는 코드다", "출력은 구조화한다(JSON 강제)", "LLM 은 결정론이 아니다",
"평가 없이는 개선도 없다" 작업 원칙을 박는다. 본 환경에서는 OpenRouter 경유
DeepSeek 호출의 표준 코드 패턴을 본문에 직접 포함한다.

**포함 내용**
- 8요소 프롬프트 설계 프레임워크 (역할·맥락·작업·입력·제약·출력 형식·예시·자기 점검)
- 프롬프트 품질 / 안전·보안 / 신뢰성·운영 / 관측성 / 평가 5영역 체크리스트
- OpenRouter `/api/v1/chat/completions` 표준 호출 의사코드 (인증·재시도·JSON 강제·헤더)
- 본 워크스페이스에서 LLM 출력은 항상 `validate()` 통과 후 사용 — 책임 분리 규약 위반 금지

---

## 5. A-3 (다중 에이전트 협업) 처리 방침

A-3 는 다음과 같은 사용 시나리오를 제시한다.

```
code-bug-analyzer로 '냉장고를 부탁해' 애플리케이션 코드 전체를 리뷰한 뒤,
발견한 문제를 performance-optimizer가 수정해서 성능 최적화한 다음,
ux-design-advisor가 사용자 경험을 개선하게 해 줘.
```

이는 역할 정의가 아니라 **이미 만든 에이전트들을 어떻게 조합해서 쓰는가**의 시나리오다.
별도 서브에이전트 파일을 만들지 않으며, "code-bug-analyzer" 자리는 기존
`code-reviewer.md` (`readonly: true`) 가 대체한다.

협업 흐름은 일반 Agent 모드에서 다음 순서로 위임 가능하다.

```
1. code-reviewer (readonly)         → 결함·개선 항목 도출
2. performance-optimizer            → 성능 병목 수정
3. ux-design-advisor                → 사용자 경험 개선
```

---

## 6. 적용 범위 설계 원칙

| 원칙 | 내용 |
|---|---|
| **공식 스펙 준수** | frontmatter 5필드만 사용 (`name`, `description`, `model`, `readonly`, `is_background`) |
| **역할 단일성** | 한 에이전트는 한 역할만 — 책임 혼재 금지 |
| **위임 신호** | `description` 끝에 호출 시점 명시 ("~ 필요할 때 적극 활용하세요") |
| **프로젝트 규칙 연동** | 모든 에이전트가 `.cursor/rules/` 의 규칙을 준수하도록 명시 |
| **도메인 규약 보호** | 본 워크스페이스의 ECB·10개 조건·Magic Constant 유도 등을 위반하지 않도록 한 줄 명시 |

---

## 7. 산출물 파일 구조

```
.cursor/
└── agents/
    ├── code-reviewer.md                 (readonly: true)   ← 기존
    ├── performance-optimizer.md         (readonly: false)  ← A-1 신규
    ├── ux-design-advisor.md             (readonly: false)  ← A-2 신규
    ├── product-manager.md               (readonly: false)  ← A-4 신규
    ├── backend-developer.md             (readonly: false)  ← A-5 신규
    ├── frontend-developer.md            (readonly: false)  ← A-6 신규
    ├── qa-engineer.md                   (readonly: false)  ← A-7 신규
    └── ai-integration-specialist.md     (readonly: false)  ← A-8 신규
```

---

## 8. 검증 결과

| 검증 항목 | 결과 |
|---|---|
| 8개 파일 존재 (1 기존 + 7 신규) | 통과 |
| 7개 신규 파일이 동일 frontmatter 구조 (라인 2~5: `name` / `description` / `model` / `readonly`) | 통과 |
| 7개 신규 파일이 6개 표준 섹션 모두 포함 | 통과 |
| 7개 신규 파일이 `.cursor/rules/` 참조 한 줄 포함 | 통과 |
| 린트 오류 | 없음 |

---

## 9. 다음 단계

본 서브에이전트 선언 이후 진행 순서는 다음을 권장한다.

1. **에이전트 호출 검증**: Cursor 사이드바에서 각 에이전트가 표시되고 호출 가능한지 확인.
2. **A-3 시나리오 리허설**: code-reviewer → performance-optimizer → ux-design-advisor 순으로
   임의의 작은 코드 변경에 대해 협업 흐름이 동작하는지 점검.
3. **에이전트 별 산출물 품질 평가**: 각 역할의 출력 형식이 본 보고서 4장의 "포함 내용" 과
   일치하는지 1회 회귀 점검.
4. **마방진 도메인 규약과의 정합성**: `qa-engineer.md` 의 10개 조건 검사 항목을 실제 테스트
   실행 결과와 비교 검증.
