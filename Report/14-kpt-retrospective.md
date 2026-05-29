# KPT 회고 — Cursor AI를 활용한 TDD 적용

> **프로젝트**: 4×4 Magic Square — Cursor AI 활용 소프트웨어 개발 응용  
> **회고 일자**: 2026-05-29  
> **참가자**: BIOS 엔지니어 (현업 Claude Code · Codex 전환 예정)  
> **최종 상태**: 62 tests passed · REFACTOR 완료 · Code Review 완료 · 보고서 13편

---

## 1. Keep — 계속 유지할 것들

> "무엇이 잘 되었는가? 어떤 관행을 반드시 이어가야 하는가?"

### 1-1. 구현 전에 불변 조건(Invariant)을 먼저 선언했다

코드를 한 줄도 쓰기 전에 5단계 문제 정의 프로세스(STEP 1~5)를 완료하고,  
Invariant Level 0~3을 먼저 확정했다.  
그 결과 테스트 ID(D-VAL-01~06)와 코드(`_rows_valid`, `_cols_valid` 등)가 1:1로 대응되어  
"왜 이 테스트가 여기 있는가?"에 항상 답할 수 있는 추적 가능성이 확보되었다.

```
✅ 유지: 새 기능 개발 전 "무엇이 참이어야 하는가"를 먼저 문서화한다.
```

### 1-2. Cursor Rules로 AI 드리프트를 구조적으로 차단했다

매 세션마다 문맥을 반복 입력하지 않고, `.cursor/rules/`의 5개 `.mdc` 파일이  
항상 프로젝트 원칙을 AI에게 주입했다.  
특히 `magicsquare-forbidden.mdc`(금지 패턴 5종)와 `magicsquare-project.mdc`(Invariant 상시 제공)가  
AI 코드 품질을 일정하게 유지하는 데 핵심 역할을 했다.

```
✅ 유지: Rules 파일을 프로젝트 초기에 설계하고 alwaysApply를 적극 활용한다.
```

### 1-3. Dual-Track TDD로 계약(Contract)을 먼저 확정했다

Track A(Boundary 계약)를 RED로 고정한 뒤 Track B(Domain 로직)를 구현했다.  
Boundary 계약이 먼저 확정되었기 때문에 Domain 구현 중에도 입출력 형식이 흔들리지 않았다.

```
✅ 유지: 인터페이스(계약) 테스트를 로직 테스트보다 먼저 작성한다.
```

### 1-4. 결함 목록(DEF-*)을 RED 단계에서 공식 등록했다

FAILED 테스트 8건을 `defect_list.md`에 DEF-001~008로 공식 등록하여  
근본 원인 그룹화 → GREEN 작업 명세로 직결시켰다.  
결함 목록이 구현 명세이자 스프린트 계획이 되었다.

```
✅ 유지: 실패 테스트는 결함 목록에 즉시 등록하고, 근본 원인 그룹으로 묶어 처리한다.
```

### 1-5. Sub-agent를 통한 역할 분리로 객관적 Code Review를 수행했다

`code-reviewer.md` Sub-agent를 위임하여 개발자 시각으로 놓치기 쉬운  
P0 이슈(IndexError 위험, NOT_IMPLEMENTED 역설)를 독립적으로 발견했다.  
역할이 파일로 고정되어 있어 매번 같은 기준으로 리뷰가 수행되었다.

```
✅ 유지: Code Review는 Sub-agent에 위임하고, 리뷰 기준은 파일로 고정한다.
```

### 1-6. 커밋 단위를 RED/GREEN 단계별로 엄격하게 분리했다

`test(red): R1 ...` → `green: G01 ...` → `green: G02 ...` 형식으로  
각 단계별 커밋이 명확하게 분리되어 있어  
git log만으로도 TDD 진행 흐름을 역추적할 수 있었다.

```
✅ 유지: 커밋 메시지에 TDD 단계(red/green/refactor)를 명시한다.
```

---

## 2. Problem — 문제점들

> "어떤 장애물이 있었는가? 무엇이 비효율적이었는가?"

### 2-1. AI가 구현 단계로 "미끄러지는" 경향을 초기에 충분히 통제하지 못했다

Rules 설계 이전 세션에서 AI가 "마방진을 만드는 함수"를 먼저 제안하는 패턴이 반복되었다.  
`alwaysApply` Rules가 없는 상태에서는 매 세션마다 Invariant를 재입력해야 했고,  
이 반복이 설계 단계의 시간을 상당히 소모했다.

```
⚠️ 문제: 환경 설계(Rules, Sub-agents)를 프로젝트 가장 초기에 완료해야 한다.
```

### 2-2. G1 하드코딩 바이패스가 "가짜 GREEN"을 만들었다

`solver.py`에서 `matrix == _G1_REFERENCE`이면 알고리즘 없이 고정 출력을 반환하는  
하드코딩 바이패스가 존재했다. 이는 Code Review에서 발견되었지만,  
GREEN 단계에서 "최소 구현"의 정의를 더 엄밀하게 정해야 함을 보여준다.

```
⚠️ 문제: 최소 구현이 "특정 입력 하드코딩"으로 변질되지 않도록 GREEN 기준을 명확히 해야 한다.
```

### 2-3. Error code SSOT(단일 진실 공급원)가 불완전했다

`INVALID_SIZE`(Boundary 계약)와 `E001`(PRD 코드 체계)가 혼재했고,  
`input_validator.py`에 `_GRID_SIZE=4`가 중복 정의되어 있었다.  
PRD v0.2 기준의 Error code 통일이 M7(통합) 단계로 보류된 상태로 남았다.

```
⚠️ 문제: 계약 상수는 반드시 하나의 출처에서만 나와야 하며, PRD 확정 시 즉시 코드에 반영해야 한다.
```

### 2-4. 반대각선 단독 실패 테스트가 누락되었다

`D-VAL-04` 테스트가 주대각선과 반대각선을 동시에 훼손하는 격자를 사용하여  
반대각선만 실패하는 케이스를 독립 검증하지 못했다.  
Code Review(MN-04)에서 발견되었고 P1 백로그로 남아 있다.

```
⚠️ 문제: "각각 독립"이라는 Invariant Level 1 원칙은 테스트에도 동일하게 적용해야 한다.
```

### 2-5. Prompt 설계 문서가 실제 AI 대화와 분리되어 관리되었다

`Report/`(보고서)와 `Prompt/`(대화 트랜스크립트)를 별도로 유지했는데,  
세션이 길어질수록 두 문서를 동기화하는 비용이 발생했다.

```
⚠️ 문제: 프롬프트와 보고서를 하나의 흐름으로 연결하는 구조가 필요하다.
```

### 2-6. 현업(BIOS) 도메인과의 연결 지점이 이번 훈련에서 부재했다

Python/pytest 기반의 TDD는 학습했지만,  
실제 BIOS 개발 환경(C, 펌웨어, 하드웨어 제약, 빌드 시스템)에서의 TDD 적용 방법은  
별도로 탐색하지 못했다.

```
⚠️ 문제: 학습한 원칙을 현업 도메인에 어떻게 이식할지 구체적으로 계획해야 한다.
```

---

## 3. Try — 다음에 시도해볼 것들

> "다음에는 무엇을 다르게 해볼까? 어떤 새로운 도구나 방법을 시도해볼까?"

### 3-1. Claude Code로 동일한 TDD 사이클 재현 (현업 전환 준비)

이번 과제는 Cursor로 진행했지만, 현업에서는 Claude Code를 활용할 예정이다.  
동일한 Invariant 체계와 Dual-Track TDD 접근을 Claude Code 환경에서도 검증해야 한다.

```
🔬 시도: 동일한 프로젝트를 Claude Code CLI 환경에서 재현하여 도구 간 차이를 측정한다.
```

### 3-2. Codex를 활용한 "테스트 자동 생성 → 검증" 파이프라인 구축

Codex는 코드 이해 및 테스트 생성에 강점이 있다.  
"기존 BIOS 코드 → Codex로 테스트 생성 → 사람이 검증" 파이프라인을 실험하여  
레거시 코드에 TDD를 역방향으로 적용하는 시도를 해본다.

```
🔬 시도: 기존 BIOS 유틸리티 함수 1개를 선택해 Codex로 테스트 초안을 생성하고 사람이 검증한다.
```

### 3-3. BIOS 도메인 Invariant 선언 시도

이번 과제에서 배운 "Invariant Level 0~3" 체계를 BIOS 도메인에 적용해본다.  
예: `POST 코드 검증 조건`, `메모리 트레이닝 수렴 조건`, `PCI 장치 열거 불변 조건` 등.

```
🔬 시도: BIOS 부팅 시퀀스의 핵심 불변 조건 3~5개를 Level 0~2 형식으로 문서화한다.
```

### 3-4. AI Rules 파일을 BIOS 프로젝트에도 적용

현업 BIOS 프로젝트의 코딩 컨벤션, 금지 패턴, 레이어 분리 원칙을  
`.cursor/rules/` 또는 Claude Code의 `CLAUDE.md` 형식으로 선언하여  
AI가 레거시 코드 패턴을 강요하지 않도록 가이드라인을 설계한다.

```
🔬 시도: BIOS 프로젝트용 AI Rules 파일 초안 3개를 작성한다.
         (금지 패턴, 아키텍처 규칙, 테스트 작성 규칙)
```

### 3-5. RED 커밋 전략을 현업 스프린트에 통합

현업 스프린트에서 기능 브랜치 생성 시 RED 테스트를 먼저 커밋하는 관행을 도입한다.  
"기능 구현 PR" 이전에 "테스트 PR"을 먼저 올리는 Two-PR 전략을 시험해본다.

```
🔬 시도: 다음 기능 1개에 한해 "test PR → impl PR" Two-PR 전략을 적용한다.
```

### 3-6. 반대각선 독립 테스트 추가 (P1 백로그 해소)

Code Review에서 발견된 MN-04(반대각선 단독 negative 테스트 부재)를  
다음 스프린트에서 추가한다.  
`_anti_diagonal_valid`만 False가 되는 격자 픽스처를 `conftest.py`에 추가한다.

```
🔬 시도: tests/entity/test_d_val_01_06_validator.py에 D-VAL-07 추가 (반대각선 단독 실패).
```

---

## 4. 개인별 학습 성과

### 4-1. 새롭게 배운 기술·개념

| 영역 | 배운 것 | 적용 사례 |
|---|---|---|
| **사고 방식** | "만든다" vs "판단한다" — 목적과 수단의 분리 | 표면 문제 정의 → 개선된 문제 정의 전환 |
| **TDD** | RED-GREEN-REFACTOR 사이클의 실제 커밋 단위 | R1~R8 RED → G01~G33 GREEN 순차 진행 |
| **TDD** | Dual-Track: Boundary 계약 vs Domain 로직 분리 | Track A(U-IN/U-FLOW/U-OUT) + Track B(D-VAL/D-SOL) |
| **설계** | ECB 아키텍처 (Entity / Control / Boundary) | 3계층 패키지 구조 구현 |
| **설계** | 불변 조건(Invariant) Level 0~3 계층화 | 테스트 ID와 1:1 추적 가능성 확보 |
| **AI 도구** | Cursor Rules `alwaysApply` 설계 원칙 | 5개 `.mdc` 파일로 AI 드리프트 차단 |
| **AI 도구** | Role-based Sub-agents 설계·위임 | 8개 에이전트 (Code Reviewer 등) |
| **Prompt Engineering** | 제약 조건 명시가 "하라"보다 통제력이 강함 | 금지 패턴 6개 명시로 하드코딩 0건 달성 |
| **품질** | Golden Master 테스트 — 회귀 시나리오 고정 | `tests/golden_master/` end-to-end 6건 |
| **품질** | 결함 목록을 GREEN 명세로 역활용 | DEF-001~008 → 근본 원인 그룹 → G01~G09 |

### 4-2. 개인 역량 향상

- **Prompt 설계 능력**: "좋은 코드 짜줘"가 아니라 전제·금지·출력 형식·Done 기준을 사전에 구조화하는 능력
- **문제 분해 능력**: 하나의 기능(크기 검증)을 9개의 독립 테스트 케이스로 분해하는 능력
- **추적 가능성 설계**: Invariant → Test ID → 코드 함수가 체계적으로 연결되는 문서화 능력
- **AI 코드 검증 능력**: AI가 제안한 코드에서 "가짜 녹색"(하드코딩 바이패스)을 발견하는 비판적 검토 능력

### 4-3. 다른 팀원들과 공유하고 싶은 인사이트

> **"AI에게 좋은 코드를 요청하기 전에, AI가 지켜야 할 불변 조건을 먼저 선언하라."**

- Rules 파일 하나가 수십 번의 반복 지시를 대체한다.
- "테스트가 통과한다" ≠ "올바르게 구현되었다" — 하드코딩 바이패스에 주의.
- 결함 목록은 구현 후가 아니라 RED 단계에서 작성할 때 스프린트 계획이 된다.
- Sub-agent의 `readonly: true`는 "개발자 모드 OFF, 심판 모드 ON"을 강제하는 훌륭한 장치.

### 4-4. 추천 학습 자료

| 자료 | 이유 |
|---|---|
| **Test-Driven Development by Example** — Kent Beck | TDD의 원저, RED-GREEN-REFACTOR의 원형 |
| **Clean Architecture** — Robert C. Martin | ECB와 동일한 계층 분리 철학의 심화 |
| **Cursor 공식 Docs: Rules / Agents** | `.cursor/rules/` 및 Sub-agents 스펙 |
| **Anthropic Claude Code 공식 Docs** | `CLAUDE.md` Rules 작성 방법 |
| **OpenAI Codex 공식 Docs** | 테스트 생성 및 코드 이해 활용 패턴 |
| **Google Testing Blog** | Dual-Track, Test Size 개념 심화 |

---

## 5. 팀 차원의 개선 액션 아이템

| # | 액션 아이템 | 책임자 | 목표 일정 | 진행 추적 방법 | 성공 기준 |
|---|---|---|---|---|---|
| A-01 | P1 백로그 해소 — 반대각선 독립 테스트(`D-VAL-07`) 추가 | 본인 | 2주 이내 | GitHub PR 링크 | `pytest tests/entity/test_d_val_01_06_validator.py` PASS |
| A-02 | Solver G1 하드코딩 제거 — 일반 알고리즘으로 D-SOL 재통과 | 본인 | 2주 이내 | GitHub PR 링크 | 62 tests 유지, `_G1_REFERENCE` 삭제 확인 |
| A-03 | Error code SSOT 통일 — `INVALID_SIZE` vs `E001` 혼재 해소 | 본인 | 1주 이내 | `grep E001 magic_square/` 결과 0건 | PRD §Error와 코드 diff 0 |
| A-04 | BIOS 프로젝트용 Cursor/Claude Rules 초안 작성 (3개 파일) | 본인 | 1개월 이내 | 파일 커밋 확인 | 신규 AI 세션에서 BIOS 금지 패턴 위반 0건 |
| A-05 | Claude Code로 동일 TDD 사이클 재현 (Magic Square) | 본인 | 1개월 이내 | 별도 repo 또는 브랜치 | 62 tests 재현, Cursor vs Claude 차이 문서화 |
| A-06 | BIOS 부팅 시퀀스 Invariant Level 0~2 문서화 (3~5개 조건) | 본인 | 6주 이내 | Markdown 파일 커밋 | Level 0~2 각각 1개 이상 조건 명시 |
| A-07 | Two-PR 전략 적용 — 현업 기능 1개에 "test PR → impl PR" 적용 | 본인 | 다음 스프린트 | PR 2개 URL 등록 | impl PR merge 전 test PR이 먼저 merged |
| A-08 | 이번 과제 인사이트를 팀/동료에게 공유 (세미나 or 문서) | 본인 | 2개월 이내 | 공유 자료 URL | 1회 이상 발표 또는 문서 배포 완료 |

---

## 6. 현업 적용 계획

> 나는 BIOS 엔지니어이며, 현업에서 **Claude Code**와 **Codex**를 활용할 예정이다.

### 6-1. 현업 환경과 이번 훈련의 차이

| 구분 | 이번 훈련 (Cursor + Python) | 현업 BIOS (Claude Code / Codex + C) |
|---|---|---|
| **언어** | Python | C (EDKII, UEFI spec 기반) |
| **테스트 프레임워크** | pytest | CUnit, Unity, 자체 시뮬레이터 |
| **빌드 환경** | `pip install` | EDK II 빌드 시스템 (Makefile, DSC/INF) |
| **AI 도구** | Cursor (IDE 통합) | Claude Code (CLI), Codex (API/CLI) |
| **제약 조건** | 알고리즘·순수 로직 | 하드웨어 레지스터, 타이밍, 인터럽트 |
| **검증 방법** | pytest 자동화 | 실기 보드 + 시뮬레이터 + 로그 분석 |

### 6-2. 이식 가능한 원칙 (도구 무관)

이번 훈련에서 배운 원칙들은 언어·도구와 무관하게 적용 가능하다.

| 원칙 | BIOS 현업 적용 방법 |
|---|---|
| **Invariant 먼저 선언** | POST 코드, 메모리 트레이닝, PCI 열거 등의 필수 조건을 코드 전에 문서화 |
| **책임 분리 (ECB)** | 하드웨어 추상화 계층(HAL) / 로직 계층 / 출력 계층 분리 |
| **RED 테스트 먼저** | 새 기능 구현 전 시뮬레이터 기반 실패 테스트를 먼저 작성 |
| **금지 패턴 Rules** | BIOS 레지스터 매직넘버 하드코딩 금지, 하드웨어 직접 접근 금지(HAL 우회 금지) 등 |
| **커밋 단위 분리** | `test(red):` → `feat:` → `refactor:` 형식 유지 |

### 6-3. Claude Code 활용 전략

```
Phase 1 (적응, 1개월):
  - 기존 BIOS 코드 1개 함수에 대해 Claude Code로 테스트 초안 생성
  - CLAUDE.md에 BIOS 도메인 금지 패턴 선언
  - AI 제안 코드 검증 프로세스 수립

Phase 2 (확장, 3개월):
  - Dual-Track 적용: HAL 계약 테스트 + 로직 테스트 분리
  - Code Review를 Claude Code 서브에이전트로 위임
  - Invariant 체계를 BIOS 부팅 시퀀스 전체로 확장

Phase 3 (정착, 6개월):
  - TDD 사이클이 스프린트 기본 프로세스로 정착
  - AI Rules 파일이 팀 코딩 컨벤션과 동기화
  - 레거시 코드에 역방향 TDD 적용 (Codex 테스트 생성 활용)
```

### 6-4. Codex 활용 전략

```
활용 케이스:
  1. 레거시 BIOS C 코드 이해 가속
     → Codex에게 코드 설명 요청 + Invariant 추출 지원
  
  2. 반복적 테스트 케이스 생성
     → 경계값·등가 분할 케이스를 Codex가 초안 작성,
       엔지니어가 하드웨어 실제 동작과 대조하여 검증
  
  3. 코드 변환 지원
     → 기존 검증 스크립트를 구조화된 테스트 형식으로 리팩토링
```

### 6-5. 현업 적용 성공 기준

| 기간 | 목표 | 측정 방법 |
|---|---|---|
| **1개월 후** | BIOS 신규 기능 1개에 TDD 적용 | "test PR" 먼저 merged 여부 |
| **3개월 후** | AI Rules 파일 3개 운영 중 | `.cursor/rules/` 또는 `CLAUDE.md` 파일 존재 |
| **6개월 후** | AI 제안 코드에서 스스로 P0 이슈 발견 능력 | Code Review 지적 사항 감소율 |
| **1년 후** | BIOS 팀 내 TDD + AI 활용 방법론 공유·확산 | 팀원 1명 이상이 동일 방법 채택 |

---

## 종합 — 이번 과제가 남긴 한 문장

> **"AI에게 무엇을 시킬지 결정하기 전에,  
> AI가 절대 하지 말아야 할 것을 먼저 선언하는 것이  
> Cursor Rules이고, Prompt Engineering이며, TDD의 정신이다."**

---

*Report/14-kpt-retrospective.md — 2026-05-29*
