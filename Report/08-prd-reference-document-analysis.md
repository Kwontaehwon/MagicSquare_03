# PRD Reference Document Analysis

> Magic Square 4×4 — PRD 작성 전 참고 문서 분석 및 매핑  
> 작성일: 2026-05-29  
> 목적: PRD 본문 작성 전, `Report/` 및 `.cursorrules` 참고 문서의 역할·매핑·우선순위 정리

---

## 1. Overall Judgment

- **PRD 작성 가능 여부:** **조건부 가능** — Epic·Journey·User Story·계약·성공 기준이 `07-user-journey.md`에 상당히 정리되어 있으나, **문제 정의(완성형 마방진)와 User Journey(2칸 빈칸 퍼즐 Solver)의 범위 불일치**, **에러 반환 형식 미정**, **Magic Square 코어 Test List 부재** 등 PRD 작성 전에 결정·보완이 필요한 항목이 있다.
- **가장 중요한 1차 참고 문서:** `Report/07-user-journey.md` — 기능 범위, 입출력 계약, User Story, Acceptance Criteria, Dual-Track TDD, 성공 기준(SC1~SC7), Gherkin 시나리오, Traceability가 가장 PRD에 가깝게 정리됨.
- **보조 참고 문서:**
  - `Report/01-problem-definition-report.md` — 배경·Why·불변식 철학·훈련 목표
  - `.cursorrules` + `.cursor/rules/*.mdc` — ECB 아키텍처, TDD 규칙, NFR, 금지 패턴
  - `Report/03-user-domain-extension.md` + `Report/04-user-test-list.md` — User(귀속) 부기능
  - `Report/02-tdd-design-prompt-report.md` — FR/Test 추적 구조 템플릿
  - `.cursor/agents/product-manager.md` — PRD 13섹션 표준 목차
- **누락된 정보:**
  - **제품 범위 확정:** 완성형 `generate/validate/display` vs 2칸 빈칸 `Solver` 중 PRD v1의 핵심 기능
  - **`Report/tdd-design-document.md`** — `02`에서 예정했으나 미생성 (Magic Square 코어 Test List·Function Contract)
  - **Boundary 진입점 명세** — CLI/API/함수 시그니처, 오류 시 반환 타입·메시지 정책
  - **P0/P1/P2 우선순위** — User Story는 있으나 MoSCoW/RICE 미적용
  - **마일스톤·일정**
  - **User 엔티티의 PRD 포함 여부** — `07`에 없음, 코드만 부분 구현
  - **시나리오 보완 항목** — `07` §5~8 자체 검증에서 SC-BND-VAL-004, SC-DOM-BLK/MSN/VAL/SOL-002~003 등 추가 필요로 명시

---

## 2. Document Summary

| Document | Main Content | PRD Usage | Priority |
|---|---|---|---|
| `Report/07-user-journey.md` | Epic·Learning Goal·Scope/Non-Scope·SC1~SC7·Invariant·5단계 Journey·Input/Output/Error Contract·도메인 분리(BlankFinder 등)·Dual-Track TDD·US-01~05·AC·Gherkin 4건·Traceability·자체 갭 분석 | **FR·User Story·계약·성공 지표·Dual-Track·시나리오**의 1차 출처 | **P0** |
| `Report/01-problem-definition-report.md` | STEP 1~5: Observation·Why×3·표면/개선 문제 정의·Level 0~3 Invariant·훈련 사고 5가지·핵심 수치 | **배경·목표/비목표·불변식 철학·Why** | **P0** |
| `.cursorrules` | Python 3.10+·ECB 3계층·의존 방향·RED/GREEN/REFACTOR·pytest AAA·커버리지 80%·금지 패턴·디렉터리 구조·AI 행동 규칙 | **NFR·Engineering Principles·아키텍처·TDD 프로세스** | **P0** |
| `.cursor/rules/magicsquare-project.mdc` | 개선된 문제 정의·Level 0~3·훈련 목표 5·핵심 수치 | `01`과 중복 — TL;DR·Invariant 요약 | **P1** (중복) |
| `.cursor/rules/magicsquare-forbidden.mdc` | 5종 안티패턴 (목적혼동·34 하드코딩·검증 생략·display 혼재·무한루프) | **Non-Goals·Engineering Constraints·Acceptance 보조** | **P1** |
| `.cursor/rules/magicsquare-ecb-architecture.mdc` | generate/validate/display 분리·엔티티 목록·Level 3 규칙 | **아키텍처·FR 레이어 매핑** (단, validate 레이어 표기 주의) | **P1** |
| `.cursor/rules/magicsquare-tdd-testing.mdc` | Level 0~3 테스트 우선순위·1 test = 1 invariant·픽스처 규칙 | **테스트 전략·Dual-Track Logic Track** | **P1** |
| `.cursor/rules/magicsquare-python-code-style.mdc` | 타입 힌트·magic_constant 유도·모듈 구조·검증 함수 분리·네이밍 | **NFR(코드 품질)·부록** | **P2** |
| `Report/02-tdd-design-prompt-report.md` | TDD 설계 문서 SECTION 1~7 스키마·추적 의무·Done 정의·금지 사항 | **FR/Test 추적 구조·부록 Traceability 템플릿** | **P1** |
| `Report/03-user-domain-extension.md` | User 귀속(attribution) 정당성·Level 4 Identity-1~7·ECB 판정·배제 책임 | **선택적 FR(귀속)·Assumptions·Out of Scope 경계** | **P2** |
| `Report/04-user-test-list.md` | User T01~T13·AAA·RED→GREEN 순서·의도적 누락 | **User FR의 Acceptance Criteria·Test Traceability** | **P2** |
| `Report/05-cursorrules-design-report.md` | Rules 5종 설계 근거·적용 범위 원칙 | **Engineering Principles 근거·부록** | **P3** |
| `Report/06-role-subagents-design-report.md` | PM/QA/BE 등 서브에이전트 역할·PRD 13섹션 언급 | **PRD 목차 참고·리뷰 프로세스** (본문 직접 반영 최소) | **P3** |
| `.cursor/agents/product-manager.md` | PRD 13섹션 표준·MoSCoW/RICE·체크리스트 | **권장 PRD Outline의 골격** | **P0** (구조) |

---

## 3. PRD Section Mapping

| PRD Section | Primary Source | Secondary Source | Content to Extract |
|---|---|---|---|
| **1. TL;DR** | `07` Epic Title + Business Goal | `01` 개선된 문제 정의 | "불변식 기반 TDD 훈련 시스템", 2칸 빈칸 Solver + ECB + Dual-Track 한 줄 요약 |
| **2. 배경 / 문제 정의** | `01` STEP 1~5 | `07` §4 Problem Statement | Why×3, 표면 vs 개선 정의, "만든다≠판단한다", 4×4 선택 이유 |
| **3. 목표 / 비목표** | `07` §6 Scope + §7 Non-Scope | `01` 훈련 목표 5 | Learning Goal L1~L5 → Goals; 웹/GUI/880열거/DB/성능 최적화 → Non-Goals |
| **4. 대상 사용자 / 페르소나** | `07` §5 Target Learners + Level 2 Persona | — | Primary/Secondary/Tertiary + TDD 학습자 Persona |
| **5. 사용자 시나리오** | `07` Level 2 Journey Overview + Level 3 US-01~05 | `07` Level 4 Gherkin (SC-*) | 5 Stage Journey + 5 User Story (As a learner…) |
| **6. 기능 요구사항 (FR)** | `07` Level 3 AC + Level 2 Contracts + Responsibility Table | `01` Invariant, `.cursorrules` ECB | F-1 Boundary 입력검증, F-2 BlankFinder, F-3 MissingNumberFinder, F-4 Validator, F-5 Solver, (선택) F-6 User, (미결) generate/display |
| **7. 비기능 요구사항** | `.cursorrules` | `07` SC1~SC7, `magicsquare-tdd-testing.mdc` | pytest·AAA·RED-GREEN-REFACTOR·커버리지 80%(rules) vs 95% Domain(07 SC1)·타입힌트·ECB 의존 방향·매직넘버 금지 |
| **8. 성공 지표** | `07` §8 Success Criteria SC1~SC7 | `01` 훈련 목표, `04` User Test List | 커버리지·계약 테스트 100%·Traceability·리팩토링 후 계약 불변 |
| **9. 마일스톤 / 일정** | *(없음 — PRD에서 신규 정의)* | `07` Stage 1~5, `02` §9, `04` T01→T13 순서 | Contract → Test List → Dual-Track RED → GREEN → REFACTOR → Regression |
| **10. 리스크 및 의존성** | `07` §5 Verification (갭 분석) | `02` §1 위험(Slipping 등) | 시나리오 미완·범위 이중 정의·validate 레이어 불일치·TDD 문서 미생성 |
| **11. 가정 (Assumptions)** | `07` Input/Output Contract | `03` User 배제 책임 | 2칸 빈칸·0=blank·1-index 출력·small-first 시도 순서·Python 3.10+ |
| **12. 미해결 질문** | `07` §5~8 Issue/Fix 표 | `03` vs `07` 범위 | v1에 generate/display 포함? User 포함? 오류 반환 형식? BlankFinder 내부 0-index? |
| **13. 부록** | `.cursorrules`, `.cursor/rules/*`, `02` Traceability 스키마 | `05`, `06`, `04` 전체 Test List | 상세 규칙 원문 링크·Invariant↔Test Matrix·금지 패턴 |

---

## 4. Source Priority Rules

| Topic | Primary Source | Reason |
|---|---|---|
| **제품 기능·입출력 계약** | `07-user-journey.md` | US·AC·Contract·Gherkin·Traceability가 가장 구체적이며 Dual-Track까지 포함 |
| **프로젝트 Why·불변식 철학** | `01-problem-definition-report.md` | STEP 1~5가 "존재 판단·책임 분리"의 근거; `07`은 이를 기능으로 전개 |
| **Invariant Level 0~3 정의** | `01` + `magicsquare-project.mdc` | 동일 내용 — **`01`을 정본**, mdc는 요약용 |
| **Level 4 User Invariant** | `03-user-domain-extension.md` | User만 정의; `07`·`01`에 없음 |
| **ECB 레이어·디렉터리·import 규칙** | `.cursorrules` | 가장 완전한 ECB 명세(entity/control/boundary 파일·예시) |
| **generate/validate/display 책임 분리** | `magicsquare-ecb-architecture.mdc` + `magicsquare-forbidden.mdc` | Level 3 설계 불변의 코드 수준 표현 |
| **TDD 사이클·RED/GREEN/REFACTOR 규칙** | `.cursorrules` tdd_rules | phase별 must/must_not이 가장 상세 |
| **테스트 작성 순서·픽스처** | `magicsquare-tdd-testing.mdc` | Invariant 계층별 테스트 목록 |
| **Python 스타일·네이밍** | `magicsquare-python-code-style.mdc` | `.cursorrules` code_style과 중복 — **mdc를 부록**, rules를 NFR 요약 |
| **User Test List·RED 순서** | `04-user-test-list.md` | T01~T13만 존재; Magic Square 코어 Test List는 없음 |
| **FR↔Test 추적 구조** | `02-tdd-design-prompt-report.md` | SECTION 1~7 + 부록 A/B 스키마 |
| **PRD 문서 구조** | `.cursor/agents/product-manager.md` | 13섹션 표준 |
| **성공 기준(커버리지 등)** | `07` SC1~SC7 | `.cursorrules`(80%)와 **충돌** — PRD에서 단일 기준으로 통합 필요 |

---

## 5. Directly Transfer to PRD Body

| Source Document | Content Type | Target PRD Section |
|---|---|---|
| `07` §2 Business Goal, §3 Learning Goal | 제품·학습 목표 | §3 Goals |
| `07` §6 Scope, §7 Non-Scope | 범위 선언 | §3 Non-Goals |
| `07` §5 Target Learners, Level 2 Persona | 사용자 정의 | §4 Persona |
| `01` STEP 5 개선된 문제 정의 | 핵심 문제 서술 | §2 Background (1~2문단) |
| `07` Stage 2 Input/Output/Error Contract | 입출력·오류 계약 | §6 FR (계약 블록) + §11 Assumptions |
| `07` Level 3 US-01~05 + AC | User Story + Acceptance Criteria | §5 Scenarios + §6 FR (P0 후보) |
| `07` Responsibility Separation Table | 도메인 컴포넌트 | §6 FR (F-2~F-5 레이어 매핑) |
| `07` §8 SC1~SC7 | 측정 가능 성공 기준 | §8 Success Metrics |
| `07` §9 Key Invariants + §10 Traceability Rule | 불변식·추적 원칙 | §6 FR 서두 + §8 보조 지표 |
| `07` Level 2 Journey Stage 1~5 (Overview) | 학습 흐름 | §5 User Journey (요약) |
| `07` Level 4 SC-DOM-SOL-001, SC-BND-VAL-001~003 | 대표 Gherkin | §5 또는 §6 FR 검증 예시 (요약) |
| `01` 훈련 사고 5가지 | 제품 가치 | §2 또는 §3 |
| `.cursorrules` architecture.layers + dependency_direction | ECB 구조 | §7 NFR (Architecture) |
| `.cursorrules` tdd_rules (요약) | 개발 방법론 | §7 NFR (Process) |
| `07` §5 Verification — 갭·Conflict 목록 | 리스크·Open Questions | §10 Risks + §12 Open Questions |

---

## 6. Move to Appendix or Engineering Principles

| Source Document | Content Type | Target Appendix / Section |
|---|---|---|
| `.cursorrules` 전체 | 상세 개발 규칙 원문 | **Appendix A: Engineering Rules Reference** (링크 + 1페이지 요약) |
| `magicsquare-forbidden.mdc` | 5종 안티패턴 코드 예시 | **Appendix B: Forbidden Patterns** |
| `magicsquare-ecb-architecture.mdc` | GOOD/BAD 코드·엔티티表 | **Appendix C: ECB Layer Guide** |
| `magicsquare-tdd-testing.mdc` | Level 0~3 테스트 함수 목록 | **Appendix D: Test Priority by Invariant** |
| `magicsquare-python-code-style.mdc` | 타입·네이밍·모듈 예시 | **Appendix E: Python Code Style** |
| `02` SECTION 1~7 스키마 | TDD 설계 문서 템플릿 | **Appendix F: Traceability Matrix Template** |
| `04-user-test-list.md` T01~T13 전체 | User 테스트 상세 | **Appendix G: User Entity Test List** (User를 v1에 포함할 경우) |
| `03-user-domain-extension.md` Identity-1~7 전체 | User 불변식 상세 | **Appendix H: User Domain Extension** |
| `05-cursorrules-design-report.md` | Rules 설계 근거 | **Appendix I: Rules Design Rationale** (선택) |
| `06-role-subagents-design-report.md` | 에이전트 역할 | **Appendix J: Review & Agent Roles** (선택) |
| `01` STEP 1~4 상세 Why 분석 | 장문 철학 | **Appendix K: Problem Definition Deep Dive** |
| `07` Level 2 Detailed Journey (Emotion/Pain Point) | UX·교육 설계 | **§5 본문 1~2문장 요약**, 상세는 **Appendix L: Learning Journey Detail** |

---

## 7. Conflicts / Ambiguities

| Issue | Related Document | Decision Needed |
|---|---|---|
| **문제 도메인 이중 정의** — `01`/mdc: 완성형 1~16 배치·generate/validate/display vs `07`: 2칸 빈칸(0)·Solver·`int[6]` 출력 | `01`, `07`, `ecb-architecture.mdc` | PRD v1의 **Primary Feature** 확정: Solver-only / Classic-only / Phase 1+2 |
| **Level 0 구성 조건 불일치** — `01`: 1~16 각 1회(완성 격자) vs `07`: 0=빈칸·빈칸 2개(부분 격자) | `01`, `07` Stage 1 | 부분/완성 격자에 **별도 Invariant 서브섹션** 분리 여부 |
| **validate() 레이어** — `ecb-architecture.mdc`: Boundary vs `.cursorrules`/`07`: Control(MagicSquareValidator) | mdc, `.cursorrules`, `07` | PRD에서 **Validator = Control**로 통일 권장 (`.cursorrules`·`07` 우선) |
| **모듈 구조** — `.cursorrules`: entity/control/boundary vs `python-code-style.mdc`: flat generator/validator/display | `.cursorrules`, mdc | PRD NFR: **ECB 디렉터리 구조** 채택 |
| **커버리지 목표** — `.cursorrules`: 80% vs `07` SC1: Domain 95% | `.cursorrules`, `07` | PRD §8에서 **단일 수치** (예: Domain 95% / 전체 80%) |
| **User Story 번호체계** — Level 2 US-01~13 vs Level 3 US-01~05 | `07` §3.3 대응표 | PRD §5·§6에서 **Level 3 US-01~05를 정본**으로 사용 |
| **BlankFinder 좌표 기준** — AC-2-4 "0-index 또는 1-index 명시" vs Output Contract "1-index" | `07` US-02 vs Stage 2 | **내부 0-index / Boundary 출력 1-index** 등 변환 규칙 명시 |
| **오류 반환 정책** — AC "검증 실패 반환 또는 발생" vs 구체 타입 없음 | `07` US-01 | Exception vs Result vs error code **표준화** |
| **User 엔티티 범위** — `03`/`04`에만 존재, `07` Solver 흐름과 미연결 | `03`, `04`, `07` | v1 포함 여부·`Submission` 연기 여부 |
| **시나리오·Test 갭** — small-first 성공, 4×4 구조 위반, Validator 독립, 두 조합 모두 실패 등 | `07` §5~8 | PRD §12 Open Questions + v1 Must-have 시나리오 목록 확정 |
| **display()/CLI** — `.cursorrules` boundary/cli·formatter vs `07` Non-Scope "웹/GUI/API" | `.cursorrules`, `07` | CLI/formatter를 v1 **In Scope**로 둘지 (Dual-Track UI Track 정의) |
| **TDD 설계 문서 부재** — `02`가 `Report/tdd-design-document.md` 생성 예정 | `02` | PRD 전 **코어 Test List·Contract 문서** 작성을 선행 마일스톤으로 명시 |

---

## 8. Recommended PRD Outline

> `.cursor/agents/product-manager.md` 13섹션을 Magic Square 훈련 제품에 맞게 조정한 **목차만** (본문 미작성).

```
# Magic Square 4×4 — Product Requirements Document (Draft Outline)

## 1. TL;DR
## 2. 배경 / 문제 정의
   2.1 전통적 알고리즘 훈련의 한계
   2.2 STEP 1~5에서 도출한 "진짜 문제" (개선된 정의)
   2.3 4×4를 선택한 이유

## 3. 목표 (Goals) / 비목표 (Non-Goals)
   3.1 Business Goal
   3.2 Learning Goals (L1~L5)
   3.3 In Scope
   3.4 Out of Scope
   3.5 Product Scope Decision  ← 【신규】 v1 Primary Feature 확정 블록

## 4. 대상 사용자 / 페르소나
   4.1 Primary / Secondary / Tertiary
   4.2 Learner Persona

## 5. 사용자 시나리오 (User Stories & Journey)
   5.1 5-Stage Learning Journey (요약)
   5.2 Dual-Track TDD Flow (UI/Boundary Track vs Logic/Control Track)
   5.3 User Stories (US-01~US-05) + Acceptance Criteria
   5.4 Representative Gherkin Scenarios (참조 ID만; 상세는 부록)

## 6. 기능 요구사항 (Functional Requirements)
   6.0 Invariant Hierarchy (Level 0~3; 선택 Level 4 User)
   6.1 Input / Output / Error Contracts
   6.2 F-1 [P0] Boundary Input Validator
   6.3 F-2 [P0] BlankFinder (Control)
   6.4 F-3 [P0] MissingNumberFinder (Control)
   6.5 F-4 [P0] MagicSquareValidator (Control)
   6.6 F-5 [P0] Solver (Control) + Output Formatting (Boundary)
   6.7 F-6 [P1/P2] User Attribution Entity  ← 범위 결정 후
   6.8 F-7 [P2/Phase 2] generate / display (Classic Magic Square)  ← 범위 결정 후
   6.9 Traceability Rule (Invariant ↔ FR ↔ Future Test ID)

## 7. 비기능 요구사항 (Non-Functional)
   7.1 Architecture: Clean Architecture + ECB
   7.2 Methodology: Dual-Track TDD, RED-GREEN-REFACTOR
   7.3 Testing: pytest, AAA, 1 test = 1 behavior
   7.4 Code Quality: Python 3.10+, type hints, Google docstring, no magic numbers
   7.5 Engineering Constraints (Forbidden Patterns 요약)

## 8. 성공 지표 (Success Metrics)
   8.1 SC1~SC7 (from User Journey Epic)
   8.2 Coverage Policy (Domain vs Overall — 통합 수치)
   8.3 Traceability Completeness

## 9. 마일스톤 / 일정
   9.1 M0: PRD 확정 + Open Questions 해소
   9.2 M1: Contract & Core Test List (TDD Design Doc)
   9.3 M2: Boundary Track RED→GREEN
   9.4 M3: Control Track RED→GREEN (BlankFinder → MSN → Validator → Solver)
   9.5 M4: Regression Suite + REFACTOR
   9.6 M5 (Optional): User Entity / CLI / display

## 10. 리스크 및 의존성
   10.1 Scope ambiguity (Solver vs Classic)
   10.2 Incomplete scenario coverage (from 07 self-audit)
   10.3 TDD slipping / test weakening
   10.4 Dependency: pytest, coverage tool, cursor rules compliance

## 11. 가정 (Assumptions)
   11.1 Input model (4×4, 0=blank, exactly 2 blanks)
   11.2 Solver attempt order (small-first → reverse)
   11.3 Output 1-index, int[6]
   11.4 Python toolchain

## 12. 미해결 질문 (Open Questions)
   12.1 v1 feature boundary
   12.2 Error contract concrete types
   12.3 BlankFinder internal vs external coordinate convention
   12.4 User/Submission in v1?
   12.5 CLI/formatter in v1?
   12.6 Coverage target unification

## 13. 부록 (Appendix)
   A. Engineering Rules Reference (.cursorrules)
   B. Forbidden Patterns (magicsquare-forbidden.mdc)
   C. ECB Layer Guide (magicsquare-ecb-architecture.mdc)
   D. Test Priority by Invariant (magicsquare-tdd-testing.mdc)
   E. Python Code Style (magicsquare-python-code-style.mdc)
   F. Traceability Matrix Template (from 02-tdd-design-prompt-report)
   G. User Entity Test List (04) — if in scope
   H. User Domain Extension (03) — if in scope
   I. Problem Definition Deep Dive (01)
   J. User Journey Full Document Map (07 level index)
   K. Scenario Gap Backlog (from 07 §5~8)
```

---

## 다음 단계

PRD 본문 작성 전에 **§3.5 Product Scope Decision**과 **§12 Open Questions** 6항을 먼저 확정하면, 나머지 섹션은 `07-user-journey.md` + `.cursorrules`에서 갈등 없이 채울 수 있다.

---

## 참고 문서 인덱스

| # | 파일 |
|---|---|
| 01 | `Report/01-problem-definition-report.md` |
| 02 | `Report/02-tdd-design-prompt-report.md` |
| 03 | `Report/03-user-domain-extension.md` |
| 04 | `Report/04-user-test-list.md` |
| 05 | `Report/05-cursorrules-design-report.md` |
| 06 | `Report/06-role-subagents-design-report.md` |
| 07 | `Report/07-user-journey.md` |
| 08 | `Report/08-prd-reference-document-analysis.md` (본 문서) |
