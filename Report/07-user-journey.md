# Magic Square 4×4 TDD Practice — User Journey

> Epic: 불변식 기반 사고 훈련 시스템 구축  
> 작성일: 2026-05-28

---

# Level 1: Epic — Business Goal

---

## 1. Epic Title

**불변식 기반 사고 훈련 시스템 구축**  
*(Invariant-First Thinking Training System via 4×4 Magic Square TDD Practice)*

---

## 2. Business Goal

4×4 Magic Square 문제를 매개로, 소프트웨어 설계자가 "어떻게 만드는가"보다 "무엇이 참이어야 하는가"를 먼저 사고하는 훈련 환경을 구축한다.

이 시스템은 단순한 알고리즘 구현이 아니라, **불변식 선언 → 계약 명세 → 테스트 작성 → 구현 → 리팩토링**이라는 설계 흐름을 실습할 수 있는 구조적 학습 경로를 제공한다.

---

## 3. Learning Goal

| # | 훈련 목표 | 설명 |
|---|---|---|
| L1 | 불변식 중심 설계 사고 | "조건이 무엇인가"를 코드 이전에 선언할 수 있다 |
| L2 | Dual-Track TDD 적용 | Domain Logic과 UI/표현 계층을 분리하여 각각 TDD로 개발할 수 있다 |
| L3 | 입력/출력 계약 명확화 | 함수의 사전 조건(pre-condition)과 사후 조건(post-condition)을 명시할 수 있다 |
| L4 | 설계 흐름 체화 | Concept → Invariant → Contract → Test → Implement → Refactor 흐름을 반복 적용할 수 있다 |
| L5 | 추적 가능성 확보 | 어떤 불변식이 어떤 테스트와 연결되는지 역추적할 수 있다 |

---

## 4. Problem Statement

전통적인 알고리즘 훈련은 "어떻게 풀 것인가"에 집중하여, 설계자가 **"무엇이 참이어야 하는가"를 먼저 정의하는 능력**을 훈련하지 못한다.

4×4 Magic Square는 다음 구조적 특성으로 이 훈련에 적합하다:

- **검증 조건이 10개로 명확하다** (행 4 + 열 4 + 대각선 2)
- **Magic Constant(34)는 격자 크기에서 유도되며 하드코딩을 금지할 수 있다**
- **생성 / 검증 / 표현의 책임 분리가 자연스럽게 요구된다**
- **탐색 공간(16! ≈ 2×10¹³)은 무작위 접근의 비효율을 실감하게 한다**

결과적으로 이 프로젝트는 Magic Square를 "만드는" 것이 목적이 아니라, Magic Square를 통해 **불변식 중심 사고 방식을 체화하는 것**이 목적이다.

---

## 5. Target Learners / Users

| 대상 | 설명 |
|---|---|
| **Primary** | TDD 개념을 배웠으나 설계 사고로 연결하지 못한 주니어~미드레벨 개발자 |
| **Secondary** | 불변식 기반 설계(DDD, Invariant-First Design)를 실습 없이 이론으로만 접한 개발자 |
| **Tertiary** | 코드 리뷰 기준을 정립하려는 팀 리드 또는 교육 담당자 |

---

## 6. Scope

이 Epic이 다루는 범위:

- **Domain Logic 설계** — 생성(generate), 검증(validate), 표현(display) 책임 분리 구조
- **불변식 계층 정의** — Level 0~3 Invariant의 명세와 테스트 추적
- **Dual-Track TDD 구조** — Domain Logic Track과 UI/Presentation Track의 분리
- **입력/출력 계약 명세** — 각 함수의 pre-condition, post-condition, boundary 정의
- **Magic Constant 유도 규칙** — n(n²+1)/2 공식으로부터의 도출, 하드코딩 금지 강제
- **리팩토링 내성 검증** — 외부 계약 불변 조건 하에서 내부 구현 교체 가능성 확인
- **학습 피드백 구조** — 테스트 실패 메시지가 어떤 불변식이 위반되었는지를 명시

---

## 7. Non-Scope

이 Epic이 다루지 않는 범위:

- 웹 UI, GUI, API 엔드포인트 구현
- 성능 최적화 (탐색 속도, 메모리 효율)
- 모든 880개 해를 열거하거나 비교하는 알고리즘 연구
- 다른 크기(3×3, 5×5)의 Magic Square 확장
- 데이터베이스 저장, 상태 관리, 영속성 계층
- 배포 파이프라인 및 운영 환경 구성

---

## 8. Success Criteria

| # | 기준 | 측정 방법 |
|---|---|---|
| SC1 | Domain Logic 테스트 커버리지 95% 이상 | 커버리지 도구 측정 |
| SC2 | Boundary 입력 검증 계약 테스트 100% 통과 | 전체 테스트 스위트 실행 결과 |
| SC3 | 설명 없는 매직 넘버 0개 | 코드 리뷰 및 lint 규칙 |
| SC4 | `GRID_SIZE`, `MAX_VALUE`, `MAGIC_CONSTANT` 등 명명된 상수 사용 | 코드 구조 검토 |
| SC5 | 정답 하드코딩 금지 — 생성 로직이 유효 해를 동적으로 도출 | 테스트로 검증 |
| SC6 | 주요 Invariant마다 최소 1개 이상의 테스트가 존재하고 추적 가능 | Traceability Matrix |
| SC7 | 리팩토링 후 외부 입력/출력 계약 불변 | 동일 테스트 스위트로 재검증 |

---

## 9. Key Invariants

프로젝트 전반을 관통하는 불변식 계층:

| 레벨 | 불변식 | 의미 |
|---|---|---|
| **Level 0** | 16칸, 1~16, 중복 없음 | Magic Square 개념의 구성 전제 — 이것이 깨지면 마방진 정의 자체 붕괴 |
| **Level 1** | 행 4개, 열 4개, 주대각선, 반대각선 각각의 합 = 34 | 마방진의 핵심 정의 — 10개 조건 각각은 서로 독립적 |
| **Level 2** | Magic Constant = n(n²+1)/2 (n=4 → 34) | 격자 크기로 유일하게 결정 — 하드코딩 금지 |
| **Level 3** | 생성·검증·표현은 서로 독립적이어야 한다 | 설계 불변 — 책임 혼재 금지 |

---

## 10. Traceability Rule

> **모든 Invariant는 최소 하나의 테스트 케이스와 양방향으로 추적 가능해야 한다.**

- 테스트 케이스 이름은 어떤 Invariant를 검증하는지 명시한다
- Invariant 정의 문서는 어떤 테스트 케이스가 이를 보증하는지 참조한다
- 리팩토링 시 Invariant가 바뀌지 않았다면, 해당 테스트는 통과 상태를 유지해야 한다
- 새로운 Invariant가 발견되면 테스트가 먼저 작성되고, 구현이 뒤따른다

---

## 11. Candidate User Stories for Level 2

다음 User Story 후보는 Level 2에서 세분화한다. 현재는 분류와 범위만 식별한다.

| # | 후보 User Story 제목 | 연관 Invariant |
|---|---|---|
| US-01 | 나는 4×4 격자의 구성 전제 조건을 검증할 수 있다 | Level 0 |
| US-02 | 나는 행·열·대각선 각각의 합이 34임을 독립적으로 검증할 수 있다 | Level 1 |
| US-03 | 나는 Magic Constant를 격자 크기로부터 유도할 수 있다 | Level 2 |
| US-04 | 나는 유효한 4×4 Magic Square를 하드코딩 없이 생성할 수 있다 | Level 0, 1, 2 |
| US-05 | 나는 임의 보드 입력에 대해 Magic Square 여부를 판단할 수 있다 | Level 1 |
| US-06 | 나는 보드를 사람이 읽을 수 있는 형식으로 표현할 수 있다 | Level 3 |
| US-07 | 나는 잘못된 입력(경계값, 중복, 범위 초과)을 명확한 오류로 거부할 수 있다 | Level 0 |
| US-08 | 나는 리팩토링 후에도 외부 계약이 변경되지 않음을 확인할 수 있다 | Level 3 |

---

---

# Level 2: User Journey — Magic Square 4×4

---

## 1. Persona

| 속성 | 설명 |
|---|---|
| **역할** | TDD를 학습 중인 소프트웨어 개발 학습자 |
| **배경** | 알고리즘 문제 풀이 경험은 있으나, 설계 계약과 불변식 선언을 먼저 하는 훈련은 부족 |
| **목표** | "정답 코드"가 아닌 "설계 → 계약 → 테스트 → 구현 → 리팩토링" 흐름을 체화하는 것 |
| **불안** | 테스트를 먼저 작성하면 방향을 잃을 것 같다는 막연한 두려움 |
| **기대** | 마방진을 통해 Clean Architecture의 계층 분리와 Dual-Track TDD를 경험하고 싶다 |

---

## 2. Journey Goal

- 4×4 Magic Square 문제를 통해 불변식 중심 사고를 훈련한다
- 입력/출력 계약을 구현보다 먼저 정의한다
- Domain Logic과 UI/Boundary 책임을 명확히 분리한다
- Dual-Track (UI Track + Logic Track) TDD 흐름을 직접 경험한다
- 설계 → 테스트 → 구현 → 리팩토링 → 회귀 보호의 순환 흐름을 학습한다

---

## 3. Journey Overview

| Stage | User Action | Thinking | Pain Point | Opportunity | Learning Outcome |
|---|---|---|---|---|---|
| **1. Problem Recognition** | 문제를 읽고 불변식 조건을 열거한다 | "이건 구현 문제가 아니라 조건 정의 문제다" | 행만 보고 열·대각선 조건을 누락한다 | 10개 조건을 독립적으로 선언하는 시작점 | 불변식 계층을 먼저 정의하는 사고 방식 체득 |
| **2. Contract Definition** | 입력·출력·오류 계약을 명세한다 | "무엇이 들어오고 무엇이 나가야 하는가" | 오류 정책을 나중에 생각하거나 누락한다 | 계약이 테스트의 사전 조건이 됨을 인식 | 입력/출력/오류 계약이 테스트 설계의 기반임을 체화 |
| **3. Domain Separation** | 책임 단위를 분리하여 도메인 모델을 정의한다 | "이 책임은 누가 져야 하는가" | 하나의 함수에 모든 책임을 넣으려는 충동 | 각 도메인이 독립 테스트 가능한 단위가 됨 | 책임 분리가 테스트 용이성과 리팩토링 내성을 높임을 경험 |
| **4. Dual-Track TDD Progress** | UI RED와 Logic RED를 분리하여 TDD 사이클을 진행한다 | "UI와 로직을 왜 동시에 테스트하면 안 되는가" | RED가 여러 계층에 섞여 원인 파악이 어려움 | 계층별 RED → GREEN → REFACTOR 명확화 | Dual-Track TDD에서 계층 분리가 피드백 속도를 높임을 경험 |
| **5. Regression Protection** | 엣지 케이스와 조합 실패 케이스를 추가한다 | "정상 케이스만으로는 계약 보호가 불충분하다" | 리팩토링 후 경계 케이스가 무너지는 경험 | 회귀 보호 테스트가 설계 안전망임을 인식 | 계약 불변 조건은 리팩토링 이후에도 테스트로 보증됨을 체화 |

---

## 4. Detailed Journey

---

### Stage 1: Problem Recognition

- **Action:**
  문제 명세를 읽고 즉시 구현에 착수하는 대신, 먼저 "무엇이 참이어야 하는가"를 질문하며 불변식 조건 목록을 작성한다. 행·열·대각선·중복·범위·빈칸 수·좌표 기준 등 구성 전제 조건을 독립 항목으로 열거한다.

- **Thinking:**
  "행의 합만 34이면 되는 것 아닌가? 왜 열과 대각선을 별도로 확인해야 하는가?"
  → 각 조건은 서로 독립적이며, 하나를 만족해도 나머지가 자동으로 만족되지 않는다는 것을 인식한다.

- **Emotion:**
  익숙한 "풀어야 할 문제" 프레임에서 "조건을 선언해야 할 문제" 프레임으로 전환될 때의 인지적 마찰과 새로운 관점에 대한 호기심이 공존한다.

- **Pain Point:**
  행 합산 조건만 인식하고, 열 4개·대각선 2개 조건을 누락하는 부분 열거의 오류. 빈칸 개수(정확히 2개) 조건을 경계 케이스가 아닌 가정으로 처리하는 경향.

- **Opportunity:**
  10개 조건(행 4 + 열 4 + 대각선 2) 각각을 독립 불변식으로 선언하는 훈련. 구성 전제(Level 0)를 검증 조건(Level 1)보다 먼저 확인해야 한다는 계층 인식.

- **Related Invariant:**
  - Level 0: 4×4 격자, 값 범위 0 또는 1~16, 빈칸 정확히 2개, 0 제외 숫자 중복 없음
  - Level 1: 행 4개, 열 4개, 주대각선, 반대각선 각각의 합 = 34 (10개 조건 독립)
  - Level 2: Magic Constant = n(n²+1)/2, n=4 → 34, 하드코딩 금지

- **Expected Learning Outcome:**
  "어떻게 구현하는가"보다 "무엇이 참이어야 하는가"를 먼저 열거하는 사고 순서를 체득한다. 조건의 부분 열거가 버그의 근원임을 인식한다.

---

### Stage 2: Contract Definition

- **Action:**
  구현 없이 입력 스키마, 출력 스키마, 오류 정책을 문서로 먼저 작성한다. 입력값의 타입·구조·허용 범위, 출력값의 타입·순서·의미, 계약 위반 시의 오류 분류를 각각 독립적으로 명세한다.

- **Thinking:**
  "출력이 `int[6]`이라면, 6개 원소의 의미와 순서가 계약에 포함되어야 한다."
  "빈칸이 2개가 아닌 경우를 어떻게 처리할 것인가 — 오류인가, 예외인가, 거부인가?"

- **Emotion:**
  계약을 먼저 쓰면 구현이 더 쉬워진다는 것을 경험하기 전의 불편함. "왜 코드도 없는데 이걸 먼저 써야 하는가"라는 저항감.

- **Pain Point:**
  오류 정책을 나중에 결정하거나 테스트에서만 암묵적으로 정의하는 습관. 출력 형식(`[r1, c1, n1, r2, c2, n2]`)의 순서와 좌표 기준(1-index)을 명세하지 않고 "당연히 알 것"으로 처리하는 경향.

- **Opportunity:**
  계약이 확정되면 테스트 작성이 계약 검증으로 변환된다. 오류 정책이 명시되면 경계 케이스 테스트가 자동으로 도출된다.

- **Input Contract:**
  - 타입: 4×4 정수 행렬 (`int[4][4]`)
  - 값 범위: 각 원소는 0 또는 1 이상 16 이하의 정수
  - 빈칸 표현: 0은 빈칸을 의미하며, 빈칸은 정확히 2개여야 한다
  - 중복 제약: 0을 제외한 숫자는 행렬 전체에서 중복될 수 없다
  - 좌표 기준: 행·열 인덱스는 1-index 기준

- **Output Contract:**
  - 타입: 길이 6의 정수 배열 (`int[6]`)
  - 형식: `[r1, c1, n1, r2, c2, n2]`
    - `(r1, c1)`: 첫 번째 빈칸의 행·열 좌표 (1-index)
    - `n1`: 첫 번째 빈칸에 채울 숫자
    - `(r2, c2)`: 두 번째 빈칸의 행·열 좌표 (1-index)
    - `n2`: 두 번째 빈칸에 채울 숫자
  - 시도 순서: 누락 숫자 중 작은 값을 첫 번째 빈칸에, 큰 값을 두 번째 빈칸에 먼저 시도. 실패 시 반대 조합 시도

- **Error Contract:**
  - 입력 행렬이 4×4가 아닌 경우 → 계약 위반으로 거부
  - 값 범위 위반 (음수, 17 이상) → 계약 위반으로 거부
  - 빈칸이 2개가 아닌 경우 (0개, 1개, 3개 이상) → 계약 위반으로 거부
  - 0을 제외한 숫자 중복 → 계약 위반으로 거부
  - 두 조합 시도 모두 마방진 조건 미충족 → 해 없음으로 반환

- **Expected Learning Outcome:**
  계약이 테스트 케이스의 사전 조건(pre-condition)과 사후 조건(post-condition)의 원천임을 체화한다. 오류 정책이 구현보다 먼저 결정되어야 경계 케이스 누락을 방지할 수 있음을 인식한다.

---

### Stage 3: Domain Separation

- **Action:**
  Stage 2에서 정의한 계약을 바탕으로, 풀이 과정을 독립적인 책임 단위로 분리한다. 각 도메인이 "무엇을 알고, 무엇을 하며, 무엇을 반환하는가"를 명세한다. 도메인 간 의존 방향을 정의한다.

- **Thinking:**
  "빈칸 위치를 찾는 것과 누락 숫자를 찾는 것은 서로 다른 책임이다."
  "검증은 생성에 의존하지 않아야 하고, 표현은 검증에 의존하지 않아야 한다."

- **Emotion:**
  하나의 함수로 모든 것을 해결하고 싶은 충동에 저항하는 인지적 불편함. 분리된 각 도메인이 독립적으로 테스트 가능해졌을 때의 명확함.

- **Pain Point:**
  `Solver`가 빈칸 탐색·누락 숫자 탐색·검증·반환 형식화를 모두 담당하는 단일 책임 원칙 위반. 검증 로직이 생성 로직 내부에 숨어 있어 독립 테스트가 불가능한 구조.

- **Opportunity:**
  각 도메인이 독립 단위로 분리되면, 도메인별 RED → GREEN → REFACTOR가 가능해진다. 하나의 도메인 변경이 다른 도메인 테스트에 영향을 주지 않는 구조가 확보된다.

- **Responsibility Separation:**

  | 도메인 | 책임 | 입력 | 출력 |
  |---|---|---|---|
  | `BlankFinder` | 4×4 행렬에서 빈칸(0) 위치 목록을 반환한다 | 4×4 정수 행렬 | 빈칸 좌표 목록 (1-index 기준) |
  | `MissingNumberFinder` | 행렬에서 누락된 1~16 숫자 목록을 반환한다 | 4×4 정수 행렬 | 누락 숫자 목록 (오름차순) |
  | `MagicSquareValidator` | 완성된 4×4 행렬이 마방진 조건 10개를 모두 만족하는지 판단한다 | 완성된 4×4 정수 행렬 | 유효 여부 (boolean) |
  | `Solver` | 두 빈칸에 누락 숫자를 배치하여 마방진을 완성하고 결과를 반환한다 | 4×4 정수 행렬 | `int[6]` 또는 해 없음 |

- **Related Invariant:**
  - Level 3: 생성·검증·표현은 서로 독립적이어야 한다 (책임 혼재 금지)
  - `MagicSquareValidator`는 `Solver`나 `BlankFinder`에 의존하지 않는다
  - `BlankFinder`와 `MissingNumberFinder`는 서로에 의존하지 않는다
  - `Solver`는 위 세 도메인을 조합하되, 각 도메인의 내부를 알지 않는다

- **Expected Learning Outcome:**
  책임 분리가 테스트 용이성의 전제 조건임을 경험한다. 분리된 도메인은 독립적으로 교체·확장 가능하며, 이것이 리팩토링 내성의 기반임을 체화한다.

---

### Stage 4: Dual-Track TDD Progress

- **Action:**
  Stage 3에서 분리한 도메인을 기반으로, UI/Boundary 계층과 Domain Logic 계층을 별도 트랙으로 나누어 TDD 사이클을 진행한다. 두 트랙의 RED 상태가 동시에 혼재하지 않도록 트랙별로 순서를 관리한다.

- **Thinking:**
  "입력 파싱 오류(UI 계층)와 마방진 검증 실패(Logic 계층)가 같은 테스트에서 실패하면 원인을 구분할 수 없다."
  "GREEN은 계약을 통과시키는 최소한의 구현이어야 하며, 완벽한 구현이 아니다."

- **Emotion:**
  RED 상태를 유지하면서 작업하는 심리적 불안감. GREEN을 빠르게 달성했을 때의 성취감. REFACTOR 단계에서 GREEN이 유지됨을 확인할 때의 신뢰 형성.

- **Pain Point:**
  UI 계층과 Logic 계층의 RED가 뒤섞여 어느 계층을 먼저 GREEN으로 만들어야 할지 판단이 어려워지는 상황. GREEN을 과잉 구현하여 REFACTOR의 의미가 사라지는 경향.

- **Opportunity:**
  트랙 분리로 피드백 루프가 짧아지고, 실패 원인의 계층이 명확해진다. GREEN 최소 구현 원칙이 지켜지면 REFACTOR가 안전해지고, 테스트가 설계 안전망으로 기능한다.

- **UI RED Focus:**
  - 입력 형식 위반 감지: 행렬 크기, 값 범위, 빈칸 개수, 중복 여부
  - 출력 형식 검증: 반환값이 `int[6]` 구조이며 좌표가 1-index임을 확인
  - 오류 정책 검증: Error Contract에 정의된 각 위반 조건이 올바른 오류를 발생시킴을 확인

- **Logic RED Focus:**
  - `BlankFinder`: 빈칸 위치 목록이 좌표 계약을 만족하는지
  - `MissingNumberFinder`: 누락 숫자 목록이 오름차순이며 완전한지
  - `MagicSquareValidator`: 10개 조건(행 4 + 열 4 + 대각선 2) 각각이 독립적으로 검증되는지
  - `Solver`: 작은 누락 숫자 우선 배치 시도 → 실패 시 반대 조합 시도 순서가 지켜지는지

- **GREEN Minimal Implementation Principle:**
  - 해당 RED 테스트를 통과시키는 최소한의 코드만 작성한다
  - 다른 케이스를 미리 처리하거나 최적화를 포함하지 않는다
  - GREEN 달성 후에만 다음 RED로 이동한다

- **REFACTOR Principle:**
  - 외부 계약(입력/출력/오류)은 변경하지 않는다
  - 모든 테스트가 GREEN인 상태에서만 리팩토링을 시작한다
  - 리팩토링 완료 후 전체 테스트 스위트가 여전히 GREEN임을 확인한다
  - 내부 구현(변수명, 알고리즘, 구조)만 변경하며, 계약은 보존한다

- **Expected Learning Outcome:**
  Dual-Track TDD에서 계층 분리가 피드백의 명확성과 속도를 높임을 경험한다. GREEN 최소 구현 원칙이 REFACTOR 단계의 안전성과 직결됨을 체화한다.

---

### Stage 5: Regression Protection

- **Action:**
  정상 케이스 GREEN 달성 이후, 계약의 경계를 탐색하여 엣지 케이스·입력 오류 케이스·조합 실패 케이스·출력 형식 케이스를 추가 테스트로 등록한다. 리팩토링 이후에도 이 테스트들이 계속 GREEN임을 확인한다.

- **Thinking:**
  "정상 케이스만 통과하는 코드는 계약을 보호하지 않는다."
  "내가 리팩토링하면 이 경계 케이스가 무너질 수 있는가? 그것을 지금 테스트로 잡아두어야 한다."

- **Emotion:**
  경계 케이스를 추가할수록 코드가 더 견고해진다는 확신. 과거에 리팩토링 후 경계 케이스가 무너지는 경험을 했던 학습자에게 "이제 테스트가 지켜준다"는 안도감.

- **Pain Point:**
  정상 케이스 이후 추가 테스트를 "나중에 하면 된다"고 미루는 경향. 엣지 케이스가 Error Contract에 이미 명세되어 있음에도 테스트로 변환하지 않는 누락.

- **Opportunity:**
  Error Contract와 Invariant가 명세되어 있으므로, 회귀 보호 테스트는 "탐색"이 아니라 "계약의 테스트 변환"이다. 이미 선언된 계약으로부터 테스트가 기계적으로 도출된다.

- **Regression Test Target:**

  | 분류 | 회귀 보호 대상 | 검증 내용 |
  |---|---|---|
  | **Edge Case** | 빈칸이 행렬의 첫 번째 셀 `(1,1)` 또는 마지막 셀 `(4,4)`에 위치하는 경우 | 좌표 반환이 1-index 기준으로 정확한지 |
  | **Edge Case** | 누락 숫자가 1과 16 (범위 경계값)인 경우 | 경계값 숫자가 누락 숫자 목록에 포함되는지 |
  | **Input Error Case** | 빈칸이 1개 또는 3개인 경우 | Error Contract에 정의된 거부 동작이 발생하는지 |
  | **Input Error Case** | 값 범위 위반 (0 미만, 17 이상) | 계약 위반으로 거부되는지 |
  | **Input Error Case** | 0 제외 숫자 중복 존재 | 계약 위반으로 거부되는지 |
  | **Combination Failure Case** | 두 조합 모두 마방진 조건 불충족 | 해 없음 결과가 반환되는지 |
  | **Combination Failure Case** | 첫 번째 조합(작은→첫 번째 빈칸) 실패, 두 번째 조합 성공 | 시도 순서가 계약대로 지켜지는지 |
  | **Output Format Case** | 성공 케이스 반환값이 `int[6]` 구조를 만족하는지 | 원소 수, 좌표 범위, 1-index 기준 준수 |

- **Protected Contract or Invariant:**
  - Input Contract: 빈칸 수 정확히 2개, 값 범위 0 또는 1~16, 중복 없음
  - Output Contract: `[r1, c1, n1, r2, c2, n2]` 형식, 1-index 기준
  - Error Contract: 각 위반 조건에 대응하는 거부 동작
  - Level 1 Invariant: 10개 조건(행 4 + 열 4 + 대각선 2) 모두 독립 충족
  - Solver 시도 순서: 작은 누락 숫자 우선 → 실패 시 반대 조합

- **Expected Learning Outcome:**
  계약과 불변식이 명세되어 있으면 회귀 보호 테스트는 창의적 발견이 아니라 계약의 기계적 변환임을 체화한다. 리팩토링 이후에도 계약이 보존됨을 테스트가 보증함을 경험한다.

---

## 5. Journey to User Story Mapping

| Journey Stage | Candidate User Story | Acceptance Criteria Direction |
|---|---|---|
| Stage 1: Problem Recognition | US-01: 나는 4×4 마방진의 불변식 조건 10개를 독립 항목으로 열거할 수 있다 | 행 4, 열 4, 대각선 2 조건이 각각 독립적으로 명세되어 있어야 한다 |
| Stage 1: Problem Recognition | US-02: 나는 Level 0 구성 전제 조건(빈칸 수, 범위, 중복)을 Level 1 검증 조건보다 먼저 선언할 수 있다 | 구성 전제 위반이 검증 조건보다 먼저 감지되어야 한다 |
| Stage 2: Contract Definition | US-03: 나는 입력 계약(타입, 범위, 빈칸 수, 중복 제약)을 구현 전에 명세할 수 있다 | 입력 계약의 각 조건이 테스트 케이스로 변환 가능해야 한다 |
| Stage 2: Contract Definition | US-04: 나는 출력 계약(`int[6]`, 1-index, 시도 순서)을 구현 전에 명세할 수 있다 | 출력 형식·순서·좌표 기준이 테스트로 검증 가능해야 한다 |
| Stage 2: Contract Definition | US-05: 나는 오류 정책(위반 유형별 거부 동작)을 구현 전에 명세할 수 있다 | 각 오류 유형이 독립된 테스트 케이스를 가져야 한다 |
| Stage 3: Domain Separation | US-06: 나는 `BlankFinder`가 빈칸 위치를 1-index 좌표로 반환함을 검증할 수 있다 | 빈칸 좌표 목록이 계약에 명시된 형식과 일치해야 한다 |
| Stage 3: Domain Separation | US-07: 나는 `MissingNumberFinder`가 누락된 1~16 숫자를 오름차순으로 반환함을 검증할 수 있다 | 누락 숫자 목록이 완전하고 오름차순이어야 한다 |
| Stage 3: Domain Separation | US-08: 나는 `MagicSquareValidator`가 10개 조건을 각각 독립적으로 검증함을 확인할 수 있다 | 조건 중 하나라도 실패하면 전체가 실패해야 한다 |
| Stage 3: Domain Separation | US-09: 나는 `Solver`가 두 조합을 계약에 정의된 순서로 시도함을 검증할 수 있다 | 첫 번째 조합 실패 시 반대 조합이 시도되어야 한다 |
| Stage 4: Dual-Track TDD | US-10: 나는 UI 계층에서 입력 오류를 도메인 로직과 분리하여 검증할 수 있다 | UI 오류 테스트가 실패해도 Domain Logic 테스트에 영향이 없어야 한다 |
| Stage 4: Dual-Track TDD | US-11: 나는 GREEN 최소 구현 원칙에 따라 각 RED를 통과시킬 수 있다 | GREEN 달성 코드가 해당 테스트 외 추가 케이스를 사전 처리하지 않아야 한다 |
| Stage 5: Regression Protection | US-12: 나는 엣지 케이스와 조합 실패 케이스를 회귀 보호 테스트로 등록할 수 있다 | 리팩토링 후에도 등록된 회귀 테스트가 모두 GREEN이어야 한다 |
| Stage 5: Regression Protection | US-13: 나는 리팩토링 후 외부 계약이 변경되지 않음을 테스트로 확인할 수 있다 | 동일 테스트 스위트가 리팩토링 전후 모두 GREEN이어야 한다 |

---

## 6. Traceability Link

| Epic Goal | Journey Stage | Invariant / Contract | Future Test Target |
|---|---|---|---|
| 불변식 중심 설계 사고 훈련 | Stage 1: Problem Recognition | Level 0: 빈칸 정확히 2개, 범위 0·1~16, 중복 없음 | `BlankFinder`, `MissingNumberFinder` 입력 검증 테스트 |
| 불변식 중심 설계 사고 훈련 | Stage 1: Problem Recognition | Level 1: 행 4 + 열 4 + 대각선 2 = 10개 조건 독립 | `MagicSquareValidator` 조건별 독립 테스트 |
| 불변식 중심 설계 사고 훈련 | Stage 1: Problem Recognition | Level 2: Magic Constant = n(n²+1)/2, 하드코딩 금지 | `MagicSquareValidator` 상수 유도 테스트 |
| 입력/출력 계약 명확화 | Stage 2: Contract Definition | Input Contract: 4×4, 범위, 빈칸 수, 중복 제약 | UI 계층 입력 검증 테스트 (Error Contract 기반) |
| 입력/출력 계약 명확화 | Stage 2: Contract Definition | Output Contract: `int[6]`, 1-index, 시도 순서 | `Solver` 출력 형식 테스트 |
| 입력/출력 계약 명확화 | Stage 2: Contract Definition | Error Contract: 위반 유형별 거부 동작 | UI 계층 오류 정책 테스트 |
| Domain Logic / UI 책임 분리 | Stage 3: Domain Separation | Level 3: 생성·검증·표현 독립 (책임 혼재 금지) | 각 도메인 단독 테스트, 도메인 간 의존 방향 테스트 |
| Dual-Track TDD 경험 | Stage 4: Dual-Track TDD | UI Track: 입력 형식·오류 정책 계약 | UI RED → GREEN → REFACTOR 사이클 테스트 |
| Dual-Track TDD 경험 | Stage 4: Dual-Track TDD | Logic Track: 빈칸·누락·검증·풀이 계약 | Logic RED → GREEN → REFACTOR 사이클 테스트 |
| 리팩토링 내성 확보 | Stage 5: Regression Protection | Output Contract + Error Contract + Level 1 Invariant | 엣지 케이스·조합 실패·출력 형식 회귀 테스트 |
| 리팩토링 내성 확보 | Stage 5: Regression Protection | 리팩토링 전후 외부 계약 불변 | 전체 테스트 스위트 리팩토링 후 재실행 |

---

---

# Level 3: User Stories — Magic Square 4×4

---

## Story Overview

| Story ID | Story Name | Layer | Protected Contract / Invariant |
|---|---|---|---|
| US-01 | 입력 검증 | Boundary | Input Contract: 4×4, 값 범위, 빈칸 수 2개, 중복 없음 |
| US-02 | 빈칸 좌표 탐색 | Control (BlankFinder) | Level 0: 빈칸은 0으로 표현되며 정확히 2개 존재 |
| US-03 | 누락 숫자 탐색 | Control (MissingNumberFinder) | Level 0: 1~16 중 0 제외 숫자는 중복 없이 존재 |
| US-04 | 마방진 검증 | Control (MagicSquareValidator) | Level 1: 행 4 + 열 4 + 대각선 2 = 10개 조건 독립, Level 2: Magic Constant = n(n²+1)/2 |
| US-05 | 두 가지 조합 시도 | Control (Solver) + Boundary | Output Contract: `int[6]`, 1-index, 시도 순서 보장 |

---

## Story 1 — 입력 검증

- **Layer:** Boundary

- **User Story:**
  As a learner,
  I want the Boundary layer to validate the input matrix before calling Domain logic,
  So that invalid data is never transmitted to the Domain layer.

- **Acceptance Criteria:**
  - AC-1-1: 입력 행렬의 행 수가 4가 아니면 정의된 검증 실패를 반환하거나 발생시킨다.
  - AC-1-2: 입력 행렬의 열 수가 4가 아니면 정의된 검증 실패를 반환하거나 발생시킨다.
  - AC-1-3: 빈칸(값이 0인 셀)의 개수가 정확히 2개가 아니면 정의된 검증 실패를 반환하거나 발생시킨다.
  - AC-1-4: 임의의 셀 값이 0 미만이거나 17 이상이면 정의된 검증 실패를 반환하거나 발생시킨다.
  - AC-1-5: 0을 제외한 숫자가 행렬 전체에서 2회 이상 등장하면 정의된 검증 실패를 반환하거나 발생시킨다.
  - AC-1-6: 위 검증 조건 중 하나라도 실패하면 Domain resolver는 호출되지 않는다.
  - AC-1-7: 모든 검증 조건을 통과한 입력은 Domain resolver에 전달된다.

- **Protected Contract:**
  Input Contract — 4×4 구조, 값 범위 (0 또는 1~16), 빈칸 수 정확히 2개, 0 제외 중복 없음.
  Level 3 Invariant — Boundary는 Domain Logic에 유효하지 않은 입력을 전달하지 않는다.

- **Future RED Test Direction:**
  - 비(非) 4×4 행렬 입력 시 검증 실패 발생 여부
  - 빈칸 0개·1개·3개 이상 입력 시 검증 실패 발생 여부
  - 값 -1, 0, 17 입력 시 각각의 처리 결과 (0은 통과, -1·17은 실패)
  - 동일 숫자 중복 입력 시 검증 실패 발생 여부
  - 검증 실패 시 Domain resolver 호출 횟수 = 0 확인

---

## Story 2 — 빈칸 좌표 탐색

- **Layer:** Control (BlankFinder)

- **User Story:**
  As a learner,
  I want to find the exact coordinates of the two blank cells,
  So that candidate number combinations can be applied correctly.

- **Acceptance Criteria:**
  - AC-2-1: 값이 0인 셀을 빈칸으로 탐지한다.
  - AC-2-2: 반환 목록의 원소 수는 정확히 2이다.
  - AC-2-3: 좌표는 행 우선(row-major) 순서로 반환된다 — 행 번호가 작은 좌표가 먼저, 같은 행이면 열 번호가 작은 좌표가 먼저 반환된다.
  - AC-2-4: 내부에서 사용하는 좌표 기준(0-index 또는 1-index)을 인터페이스 명세에 명시하며, 실제 반환값이 해당 기준을 따른다.
  - AC-2-5: 반환된 각 좌표는 행렬의 유효 범위 내에 있다.

- **Protected Invariant:**
  Level 0 — 빈칸은 0으로 표현되며 행렬 내에 정확히 2개 존재한다.
  Level 3 — `BlankFinder`는 `MissingNumberFinder`, `MagicSquareValidator`에 의존하지 않는다.

- **Future RED Test Direction:**
  - 빈칸이 `(1행, 1열)`과 `(4행, 4열)`처럼 경계 위치에 있는 경우 좌표 정확성 확인
  - 두 빈칸이 같은 행, 다른 행에 있을 때 각각 row-major 순서 준수 확인
  - 반환 좌표 기준(0-index 또는 1-index)이 명세와 일치하는지 확인
  - 반환 목록의 길이가 항상 2인지 확인

---

## Story 3 — 누락 숫자 탐색

- **Layer:** Control (MissingNumberFinder)

- **User Story:**
  As a learner,
  I want to find the two numbers missing from 1 through 16,
  So that they can be used as candidates for the blank cells.

- **Acceptance Criteria:**
  - AC-3-1: 행렬의 모든 셀 값 중 0은 누락 숫자 계산에서 제외한다.
  - AC-3-2: 1 이상 16 이하 범위에서 행렬에 존재하지 않는 숫자를 누락 숫자로 판단한다.
  - AC-3-3: 반환 목록의 원소 수는 정확히 2이다.
  - AC-3-4: 누락 숫자는 오름차순으로 반환된다 — 첫 번째 원소가 두 번째 원소보다 작다.

- **Protected Invariant:**
  Level 0 — 0을 제외한 숫자는 1~16 범위에서 중복 없이 존재하며, 빈칸이 2개이므로 누락 숫자도 정확히 2개이다.
  Level 3 — `MissingNumberFinder`는 `BlankFinder`, `MagicSquareValidator`에 의존하지 않는다.

- **Future RED Test Direction:**
  - 누락 숫자가 1과 16(경계값)인 경우 반환 목록에 포함되는지 확인
  - 누락 숫자가 연속된 숫자(예: 7, 8)인 경우와 비연속(예: 3, 15)인 경우 각각 오름차순 정렬 확인
  - 반환 목록의 길이가 항상 2인지 확인
  - 0이 누락 숫자 목록에 포함되지 않는지 확인

---

## Story 4 — 마방진 검증

- **Layer:** Control (MagicSquareValidator)

- **User Story:**
  As a learner,
  I want to verify whether a completed 4×4 grid satisfies the magic square invariant,
  So that only valid magic square results are accepted.

- **Acceptance Criteria:**
  - AC-4-1: 4개 행 각각의 합이 모두 34이면 행 조건을 통과한다.
  - AC-4-2: 4개 열 각각의 합이 모두 34이면 열 조건을 통과한다.
  - AC-4-3: 주대각선(좌상→우하)의 합이 34이면 주대각선 조건을 통과한다.
  - AC-4-4: 반대각선(우상→좌하)의 합이 34이면 반대각선 조건을 통과한다.
  - AC-4-5: 위 10개 조건(행 4 + 열 4 + 대각선 2)을 모두 만족할 때만 `true`를 반환한다.
  - AC-4-6: 10개 조건 중 하나라도 실패하면 `false`를 반환한다.
  - AC-4-7: Magic Constant 34는 코드 내에 직접 하드코딩되지 않으며, `n(n²+1)/2` 공식 또는 명명된 상수로부터 유도된다.

- **Protected Invariant:**
  Level 1 — 행 4 + 열 4 + 대각선 2 = 10개 조건 각각 독립.
  Level 2 — Magic Constant = n(n²+1)/2, n=4 → 34, 하드코딩 금지.
  Level 3 — `MagicSquareValidator`는 `Solver`, `BlankFinder`, `MissingNumberFinder`에 의존하지 않는다.

- **Future RED Test Direction:**
  - 행 조건만 만족하고 열 조건이 실패하는 격자 → `false` 반환 확인
  - 열 조건만 만족하고 대각선 조건이 실패하는 격자 → `false` 반환 확인
  - 10개 조건을 모두 만족하는 유효한 마방진 격자 → `true` 반환 확인
  - Magic Constant가 34로 직접 하드코딩되지 않고 공식 또는 상수로 유도되는지 확인
  - 각 조건(행, 열, 주대각선, 반대각선)이 독립적으로 검증되는지 확인

---

## Story 5 — 두 가지 조합 시도

- **Layer:** Control (Solver) + Boundary (출력 형식 변환)

- **User Story:**
  As a learner,
  I want the solver to try both possible missing-number combinations,
  So that it can find the valid magic square result without hardcoding the answer.

- **Acceptance Criteria:**
  - AC-5-1: 첫 번째 시도에서 작은 누락 숫자를 첫 번째 빈칸에, 큰 누락 숫자를 두 번째 빈칸에 배치한다.
  - AC-5-2: 첫 번째 조합이 마방진 조건을 만족하지 못하면 반대 조합(큰 → 첫 번째 빈칸, 작은 → 두 번째 빈칸)을 시도한다.
  - AC-5-3: 성공한 조합의 결과를 `int[6]` 형식으로 반환한다.
  - AC-5-4: 반환 배열의 길이는 정확히 6이다.
  - AC-5-5: 최종 출력 좌표는 1-index 기준을 따른다.
  - AC-5-6: 최종 출력 형식은 `[r1, c1, n1, r2, c2, n2]`이며, 원소 순서가 이 명세를 따른다.
  - AC-5-7: 두 조합 모두 마방진 조건을 만족하지 못하면 정의된 실패를 반환하거나 발생시킨다.
  - AC-5-8: 출력 좌표는 입력 행렬의 실제 빈칸 위치를 1-index로 변환한 값이다.

- **Protected Contract / Invariant:**
  Output Contract — `int[6]`, 형식 `[r1, c1, n1, r2, c2, n2]`, 1-index 기준.
  Level 0 — 정답은 하드코딩되지 않으며, 누락 숫자 두 조합의 동적 탐색으로 결정된다.
  Level 1 — 결과로 반환된 격자는 10개 마방진 조건을 모두 만족한다.
  Solver 시도 순서 계약 — 작은 누락 숫자 우선 시도 → 실패 시 반대 조합.

- **Future RED Test Direction:**
  - 첫 번째 조합(작은→첫 번째 빈칸)이 성공하는 케이스 → 올바른 `int[6]` 반환 확인
  - 첫 번째 조합 실패, 두 번째 조합 성공 케이스 → 시도 순서 계약 준수 및 올바른 `int[6]` 반환 확인
  - 두 조합 모두 실패하는 케이스 → 정의된 실패 반환 또는 발생 확인
  - 반환 배열의 길이가 6인지 확인
  - 반환된 좌표 `(r1, c1)`, `(r2, c2)`가 1-index 기준이며 입력 행렬의 실제 빈칸 위치와 일치하는지 확인
  - 반환된 `n1`, `n2`가 누락 숫자 목록의 원소인지 확인

---

## Traceability Matrix

| Epic Goal | Journey Stage | User Story | Acceptance Criteria | Future Test Target |
|---|---|---|---|---|
| 불변식 중심 설계 사고 훈련 | Stage 1: Problem Recognition | US-01 입력 검증 | AC-1-1~5: 각 입력 위반 조건별 독립 거부 동작 | Boundary 입력 검증 테스트 (조건별 독립 케이스) |
| 입력/출력 계약 명확화 | Stage 2: Contract Definition | US-01 입력 검증 | AC-1-6: 검증 실패 시 Domain 미호출 | Domain resolver 호출 횟수 = 0 테스트 |
| Domain Logic / UI 책임 분리 | Stage 3: Domain Separation | US-02 빈칸 좌표 탐색 | AC-2-1~5: BlankFinder 독립 동작 | `BlankFinder` 단독 단위 테스트 |
| 불변식 중심 설계 사고 훈련 | Stage 1: Problem Recognition | US-02 빈칸 좌표 탐색 | AC-2-3: row-major 순서, AC-2-4: 좌표 기준 명시 | 경계 위치 빈칸 좌표 정확성 테스트 |
| Domain Logic / UI 책임 분리 | Stage 3: Domain Separation | US-03 누락 숫자 탐색 | AC-3-1~4: MissingNumberFinder 독립 동작 | `MissingNumberFinder` 단독 단위 테스트 |
| 불변식 중심 설계 사고 훈련 | Stage 1: Problem Recognition | US-03 누락 숫자 탐색 | AC-3-3: 반환 수 정확히 2, AC-3-4: 오름차순 | 경계값(1, 16) 누락 케이스 테스트 |
| 불변식 중심 설계 사고 훈련 | Stage 1: Problem Recognition | US-04 마방진 검증 | AC-4-1~6: 10개 조건 각각 독립 검증 | `MagicSquareValidator` 조건별 독립 테스트 |
| 불변식 중심 설계 사고 훈련 | Stage 1: Problem Recognition | US-04 마방진 검증 | AC-4-7: Magic Constant 하드코딩 금지 | 상수 유도 테스트 (공식 또는 명명된 상수 참조 확인) |
| Dual-Track TDD 경험 | Stage 4: Dual-Track TDD | US-04 마방진 검증 | AC-4-5~6: 조건 일부 실패 시 false | 행만 만족·열만 만족·대각선만 실패 케이스 테스트 |
| 입력/출력 계약 명확화 | Stage 2: Contract Definition | US-05 두 가지 조합 시도 | AC-5-3~6: 출력 형식 및 1-index 좌표 계약 | `Solver` 출력 형식 테스트 |
| 불변식 중심 설계 사고 훈련 | Stage 4: Dual-Track TDD | US-05 두 가지 조합 시도 | AC-5-1~2: 시도 순서 계약 | 첫 번째 조합 실패·두 번째 조합 성공 케이스 테스트 |
| 리팩토링 내성 확보 | Stage 5: Regression Protection | US-05 두 가지 조합 시도 | AC-5-7: 두 조합 모두 실패 시 정의된 실패 | 조합 실패 케이스 회귀 테스트 |
| 리팩토링 내성 확보 | Stage 5: Regression Protection | US-01~05 전체 | 리팩토링 후 동일 AC 통과 | 전체 테스트 스위트 리팩토링 후 재실행 |

---

---

# Level 4: Implementation Scenario — Technical

> Feature: 4×4 마방진 완성

불변식에 기반하여 로직을 검증하기 위해
TDD를 연습하는 개발자로서
일부가 비어 있는 4×4 마방진을 완성하고 싶다.

---

## Background

| 조건 | 내용 |
|---|---|
| 입력 | 4×4 정수 행렬 |
| 빈칸 표현 | 0은 빈칸을 의미한다 |
| 빈칸 수 | 정확히 2개의 셀이 0을 포함한다 |
| 값 범위 | 숫자는 0 또는 1 이상 16 이하여야 한다 |
| 중복 제약 | 0을 제외한 중복 숫자는 허용되지 않는다 |
| 마방진 상수 | 4×4 마방진 상수는 34이다 |
| 출력 형식 | `[r1, c1, n1, r2, c2, n2]` |
| 좌표 기준 | 반환 좌표는 1-index 기준이어야 한다 |

---

## Scenario Overview

| Scenario ID | Scenario Name | Layer | Related User Story | RED Test ID | Task ID |
|---|---|---|---|---|---|
| SC-DOM-SOL-001 | 작은 수 우선 배치 실패 후 반대 조합으로 마방진 완성 | Domain / Solver | US-05 두 가지 조합 시도 | RED-DOM-SOL-001 | TASK-DOM-SOL-001 |
| SC-BND-VAL-001 | 빈칸 개수가 잘못된 경우 | Boundary | US-01 입력 검증 | RED-BND-VAL-001 | TASK-BND-VAL-001 |
| SC-BND-VAL-002 | 중복 숫자가 존재하는 경우 | Boundary | US-01 입력 검증 | RED-BND-VAL-002 | TASK-BND-VAL-002 |
| SC-BND-VAL-003 | 값이 범위를 벗어난 경우 | Boundary | US-01 입력 검증 | RED-BND-VAL-003 | TASK-BND-VAL-003 |

---

## SC-DOM-SOL-001

**Scenario:** 작은 수 우선 배치가 실패하고 반대 조합으로 마방진이 완성된다
**Related User Story:** Story 5 — 두 가지 조합 시도
**Layer:** Domain / Solver

---

### Given

다음 4×4 행렬이 주어진다:

| 16 | 2 | 3 | 13 |
|---|---|---|---|
| 5 | 11 | 10 | 8 |
| 9 | 7 | **0** | 12 |
| 4 | 14 | 15 | **0** |

누락 숫자는 **1**과 **6**이다.

row-major 순서의 빈칸 좌표는 다음과 같다 (1-index 기준):

| 순서 | row | column |
|---|---|---|
| 첫 번째 빈칸 | 3 | 3 |
| 두 번째 빈칸 | 4 | 4 |

---

### When / Then — 첫 번째 시도 (small-first)

**When** 시스템이 작은 누락 숫자 **1**을 첫 번째 빈칸 `(3, 3)`에 배치한다
**And** 시스템이 큰 누락 숫자 **6**을 두 번째 빈칸 `(4, 4)`에 배치한다

**Then** 첫 번째 시도는 실패해야 한다
**And** 해당 행렬은 마방진 상수 34를 만족하지 않아야 한다

> 검증 근거 (첫 번째 시도 배치 결과):
> - 3행: 9 + 7 + **1** + 12 = 29 ≠ 34 → 행 조건 실패
> - 3열: 3 + 10 + **1** + 15 = 29 ≠ 34 → 열 조건 실패

---

### When / Then — 두 번째 시도 (reverse)

**When** 시스템이 반대 조합을 시도한다
**And** 시스템이 큰 누락 숫자 **6**을 첫 번째 빈칸 `(3, 3)`에 배치한다
**And** 시스템이 작은 누락 숫자 **1**을 두 번째 빈칸 `(4, 4)`에 배치한다

**Then** 완성된 행렬은 마방진 상수 34를 만족해야 한다
**And** 모든 행의 합은 34여야 한다
**And** 모든 열의 합은 34여야 한다
**And** 두 대각선의 합은 각각 34여야 한다
**And** 결과는 길이 6의 배열로 반환되어야 한다
**And** 반환 좌표는 1-index 기준이어야 한다
**And** 기대 반환값은 `[3, 3, 6, 4, 4, 1]`이어야 한다

> 검증 근거 (두 번째 시도 완성 행렬):
>
> | 16 | 2 | 3 | 13 |
> |---|---|---|---|
> | 5 | 11 | 10 | 8 |
> | 9 | 7 | **6** | 12 |
> | 4 | 14 | 15 | **1** |
>
> - 행: 34, 34, 34, 34 ✓
> - 열: 34, 34, 34, 34 ✓
> - 주대각선 (16+11+6+1): 34 ✓
> - 반대각선 (13+10+7+4): 34 ✓

---

### Protected Invariant

- Level 1: 유효한 4×4 마방진은 모든 행, 열, 대각선의 합이 34여야 한다 (10개 조건 독립)
- Level 2: Magic Constant 34는 n(n²+1)/2 공식 또는 명명된 상수로 유도되며 하드코딩되지 않는다
- Solver 시도 순서 계약: small-first 시도가 실패하면 Solver는 반드시 reverse 조합을 시도해야 한다

### RED Test ID Candidate

`RED-DOM-SOL-001`

### Implementation Task Candidate

`TASK-DOM-SOL-001`: small-first 실패 후 reverse 조합을 시도하는 Solver 로직 작성

---

## SC-BND-VAL-001

**Scenario:** 빈칸 개수가 잘못된 경우
**Related User Story:** Story 1 — 입력 검증
**Layer:** Boundary

---

### Given

빈칸(값이 0인 셀)이 **1개뿐인** 행렬이 주어진다.

### When

입력 검증을 수행한다.

### Then

- 검증은 실패해야 한다
- 빈칸 개수 오류가 발생해야 한다
- Domain 해 결정 로직은 실행되지 않아야 한다

> 확장 케이스 (동일 Scenario 범위):
> - 빈칸이 0개인 행렬 → 동일하게 검증 실패
> - 빈칸이 3개 이상인 행렬 → 동일하게 검증 실패

---

### Protected Contract

- Input Contract: Boundary는 빈칸이 정확히 2개가 아닌 입력을 거부해야 한다
- Level 3 Invariant: 잘못된 입력은 Domain Solver로 전달되어선 안 된다

### RED Test ID Candidate

`RED-BND-VAL-001`

### Implementation Task Candidate

`TASK-BND-VAL-001`: 빈칸 개수 검증 로직 작성 (0의 개수 ≠ 2 → 거부)

---

## SC-BND-VAL-002

**Scenario:** 중복 숫자가 존재하는 경우
**Related User Story:** Story 1 — 입력 검증
**Layer:** Boundary

---

### Given

0을 제외한 중복 숫자가 포함된 행렬이 주어진다.

### When

입력 검증을 수행한다.

### Then

- 검증은 실패해야 한다
- 중복 숫자 오류가 발생해야 한다
- Domain 해 결정 로직은 실행되지 않아야 한다

> 확장 케이스 (동일 Scenario 범위):
> - 동일 숫자가 2회 등장하는 경우
> - 동일 숫자가 3회 이상 등장하는 경우

---

### Protected Contract

- Input Contract: 0을 제외한 중복 값은 허용되지 않는다
- Level 3 Invariant: 잘못된 입력은 Domain Solver로 전달되어선 안 된다

### RED Test ID Candidate

`RED-BND-VAL-002`

### Implementation Task Candidate

`TASK-BND-VAL-002`: 0을 제외한 중복 숫자 검증 로직 작성

---

## SC-BND-VAL-003

**Scenario:** 값이 범위를 벗어난 경우
**Related User Story:** Story 1 — 입력 검증
**Layer:** Boundary

---

### Given

16을 초과하는 숫자가 포함된 행렬이 주어진다.

### When

입력 검증을 수행한다.

### Then

- 검증은 실패해야 한다
- 범위 위반 오류가 발생해야 한다
- Domain 해 결정 로직은 실행되지 않아야 한다

> 확장 케이스 (동일 Scenario 범위):
> - 음수 값이 포함된 경우 (0 미만) → 동일하게 검증 실패
> - 값이 정확히 17인 경우 → 동일하게 검증 실패
> - 값이 정확히 0인 경우 → 빈칸으로 허용 (검증 통과)
> - 값이 정확히 1 또는 16인 경우 → 경계값으로 허용 (검증 통과)

---

### Protected Contract

- Input Contract: 모든 셀 값은 0 또는 1 이상 16 이하여야 한다
- Level 3 Invariant: 잘못된 입력은 Domain Solver로 전달되어선 안 된다

### RED Test ID Candidate

`RED-BND-VAL-003`

### Implementation Task Candidate

`TASK-BND-VAL-003`: 값 범위 검증 로직 작성 (값 < 0 또는 값 > 16 → 거부)

---

## Decomposition Preview

| Scenario ID | Related AC | Layer | Protected Contract / Invariant | RED Test ID | Implementation Task |
|---|---|---|---|---|---|
| SC-DOM-SOL-001 | AC-5-1~2: small-first 실패 후 reverse 조합 성공, AC-5-3~6: 출력 형식 | Domain / Solver | Level 1 (10개 조건), Solver 시도 순서 계약 | RED-DOM-SOL-001 | TASK-DOM-SOL-001 |
| SC-BND-VAL-001 | AC-1-3: 빈칸은 정확히 2개여야 함, AC-1-6: Domain 미호출 | Boundary | Input Contract (빈칸 수), Level 3 | RED-BND-VAL-001 | TASK-BND-VAL-001 |
| SC-BND-VAL-002 | AC-1-5: 0 제외 중복 숫자 금지, AC-1-6: Domain 미호출 | Boundary | Input Contract (중복 제약), Level 3 | RED-BND-VAL-002 | TASK-BND-VAL-002 |
| SC-BND-VAL-003 | AC-1-4: 값은 0 또는 1~16이어야 함, AC-1-6: Domain 미호출 | Boundary | Input Contract (값 범위), Level 3 | RED-BND-VAL-003 | TASK-BND-VAL-003 |

---

---

# Level 5: Scenario Verification and Summary

---

## 1. Overall Judgment

- **적합성 점수:** 7.5 / 10
- **현재 상태:** 일부 수정 필요
- **요약 판단:**
  Epic → Journey → User Story → Technical Scenario의 핵심 흐름은 일관되게 연결되어 있으며, 계약과 불변식 기반 추적 구조도 전 레벨에 걸쳐 유지된다. 다만 **Domain 독립 컴포넌트(BlankFinder, MissingNumberFinder, MagicSquareValidator)에 대한 전용 Gherkin 시나리오가 부재**하고, **small-first 성공 케이스 및 두 조합 모두 실패 케이스**의 시나리오가 없어 RED Test 분해가 불완전하다. 구조의 일관성은 높으나, 시나리오 커버리지 보완 후 RED 단계 진입이 권장된다.

---

## 2. Epic → Journey Consistency Check

| Check Item | Status | Evidence | Issue / Fix |
|---|---|---|---|
| Epic의 성공 기준이 Journey에 반영되었는가? | ✅ | Epic SC1(커버리지 95%) → Journey Stage 4 GREEN 원칙 / SC2(경계 검증 100%) → Stage 5 Regression / SC3(매직 넘버 금지) → Stage 1 Invariant | — |
| Journey의 각 단계가 Epic 목표 달성에 기여하는가? | ✅ | Stage 1~5가 각각 불변식 선언 → 계약 정의 → 책임 분리 → TDD 적용 → 회귀 보호로 Epic 훈련 흐름을 구성 | — |
| Pain Point가 명확히 정의되었는가? | ✅ | 각 Stage에 독립적인 Pain Point 명시 (예: Stage 1 — 행만 보고 열·대각선 누락) | — |
| 불변식 기반 사고 훈련이 Journey에 드러나는가? | ✅ | Stage 1 Related Invariant에 Level 0~2 계층 명시 / Stage 3 Responsibility Separation에 Level 3 명시 | — |
| Dual-Track TDD 흐름이 Journey에 반영되었는가? | ✅ | Stage 4에 UI RED Focus / Logic RED Focus / GREEN Minimal / REFACTOR Principle 각각 명시 | — |

---

## 3. Journey → User Story Consistency Check

| Check Item | Status | Evidence | Issue / Fix |
|---|---|---|---|
| Journey 각 Stage마다 최소 1개 이상의 User Story가 있는가? | ⚠️ | Stage 1~5 → Journey to User Story Mapping에 US-01~13 매핑 존재. 그러나 Level 3 User Story는 US-01~05로 재번호화되어 Level 2 US 번호 체계와 불일치 | Level 2 US 번호(US-01~13)와 Level 3 US 번호(US-01~05)의 대응 매핑 표를 별도 추가 권장 |
| User Story가 실제 기능 단위로 변환 가능한가? | ✅ | US-01 입력 검증 → Boundary Validator / US-02~04 → BlankFinder·MissingNumberFinder·Validator / US-05 → Solver | — |
| Acceptance Criteria가 측정 가능한 문장인가? | ✅ | 모든 AC가 "~이면 ~해야 한다" 또는 "~은 N이어야 한다" 형식으로 작성됨 | — |
| Boundary Story와 Domain Story가 분리되어 있는가? | ✅ | US-01은 Layer: Boundary / US-02~05는 Layer: Control로 명시 | — |
| 각 Story가 보호하는 Contract 또는 Invariant가 명시되어 있는가? | ✅ | US-01~05 각각에 Protected Contract / Protected Invariant 섹션 존재 | — |

**Level 2 ↔ Level 3 User Story 번호 대응표:**

| Level 2 US | Level 3 US | 내용 |
|---|---|---|
| US-03, US-05 | US-01 | 입력 계약 명세 + 오류 정책 명세 → 입력 검증 (Boundary) |
| US-06 | US-02 | BlankFinder 검증 |
| US-07 | US-03 | MissingNumberFinder 검증 |
| US-08 | US-04 | MagicSquareValidator 검증 |
| US-09 | US-05 | Solver 두 가지 조합 시도 |
| US-01, US-02 | (Level 3 미분리) | 불변식 열거·구성 전제 선언 — Level 3에서 US-04 AC-4-7로 흡수 |
| US-10, US-11 | (Level 3 미분리) | Dual-Track TDD 실행 — Level 3 US-01~05 전체에 분산 |
| US-12, US-13 | (Level 3 미분리) | 회귀 보호·리팩토링 내성 — Traceability Matrix 마지막 행으로 흡수 |

---

## 4. Story → Technical Scenario Consistency Check

| Check Item | Status | Evidence | Issue / Fix |
|---|---|---|---|
| 모든 Acceptance Criteria가 Gherkin Scenario로 변환되었는가? | ⚠️ | US-01 AC-1-1(4×4 구조 위반) → 전용 시나리오 없음 / US-02~04 → 전용 시나리오 없음 / US-05 AC-5-1(small-first 성공) → 시나리오 없음 | SC-BND-VAL-004, SC-DOM-BLK-001, SC-DOM-MSN-001, SC-DOM-VAL-001, SC-DOM-SOL-002, SC-DOM-SOL-003 추가 필요 |
| Given-When-Then이 명확한가? | ✅ | SC-DOM-SOL-001: 실제 행렬·좌표·수치 포함 / SC-BND-VAL-001~003: 위반 조건·기대 동작 명시 | — |
| 각 Scenario가 자동화 테스트로 변환 가능한가? | ✅ | 각 Scenario의 Given 값이 구체적이며, Then 조건이 assert 문으로 직접 변환 가능 | — |
| 각 Scenario마다 대상 Layer가 명시되어 있는가? | ✅ | SC-DOM-SOL-001: Domain / Solver / SC-BND-VAL-001~003: Boundary | — |
| 각 Scenario가 Future RED Test ID로 분해 가능한가? | ✅ | RED-DOM-SOL-001, RED-BND-VAL-001~003 각각 명시 | — |
| 각 Scenario가 Implementation Task로 분해 가능한가? | ✅ | TASK-DOM-SOL-001, TASK-BND-VAL-001~003 각각 명시 | — |

---

## 5. MagicSquare Edge Case Coverage

### Normal Case

| Check Item | Status | Evidence | Issue / Fix |
|---|---|---|---|
| small-first 성공 시나리오가 존재하는가? | ❌ | Level 4에 해당 시나리오 없음. SC-DOM-SOL-001은 small-first 실패 케이스만 다룸 | SC-DOM-SOL-002 추가 필요 — small-first 배치 후 마방진 조건 충족 시 즉시 `[r1,c1,small,r2,c2,large]` 반환 |
| small-first 실패 후 reverse 성공 시나리오가 존재하는가? | ✅ | SC-DOM-SOL-001 전체가 이 케이스를 수치 기반으로 검증 | — |
| 최종 결과가 int[6] 형식으로 검증되는가? | ✅ | SC-DOM-SOL-001 Then: "결과는 길이 6의 배열로 반환되어야 한다" / US-05 AC-5-3~4 | — |
| 최종 좌표가 1-index로 검증되는가? | ✅ | SC-DOM-SOL-001 기대 반환값 `[3,3,6,4,4,1]` (1-index) / US-05 AC-5-5 | — |

### Exception Case

| Check Item | Status | Evidence | Issue / Fix |
|---|---|---|---|
| 4×4가 아닌 입력 검증 시나리오가 있는가? | ❌ | US-01 AC-1-1~2에 Acceptance Criteria는 존재하나 전용 Gherkin 시나리오 없음 | SC-BND-VAL-004 추가 필요 — 3×4, 4×5 행렬 입력 시 검증 실패 확인 |
| 빈칸 개수가 2개가 아닌 경우가 검증되는가? | ✅ | SC-BND-VAL-001: 빈칸 1개 케이스 명시, 확장 케이스(0개, 3개 이상)도 포함 | — |
| 0을 제외한 중복 숫자가 검증되는가? | ✅ | SC-BND-VAL-002: 중복 숫자 케이스, 확장(2회·3회 이상) 포함 | — |
| 값이 0 또는 1~16 범위를 벗어나는 경우가 검증되는가? | ✅ | SC-BND-VAL-003: 17 이상, 확장 케이스(음수, 경계값 0·1·16) 포함 | — |
| 입력 검증 실패 시 Domain resolver가 호출되지 않는가? | ✅ | SC-BND-VAL-001~003 Then에 "Domain 해 결정 로직은 실행되지 않아야 한다" 명시 / US-01 AC-1-6 | — |
| 두 조합 모두 마방진을 만들지 못하는 경우가 검증되는가? | ❌ | US-05 AC-5-7에 Acceptance Criteria는 존재하나 전용 시나리오 없음 | SC-DOM-SOL-003 추가 필요 — 두 조합 모두 실패 시 정의된 실패 반환 확인 |

### Boundary Case

| Check Item | Status | Evidence | Issue / Fix |
|---|---|---|---|
| 최소값 1이 유효값으로 처리되는가? | ⚠️ | US-03 Future RED Test Direction에 "경계값(1, 16) 누락 케이스" 언급. 전용 시나리오 없음 | SC-DOM-MSN-001에 경계값 케이스 포함 권장 |
| 최대값 16이 유효값으로 처리되는가? | ⚠️ | SC-BND-VAL-003 확장 케이스에 "값이 정확히 16인 경우 허용" 언급. 전용 Then 검증 없음 | SC-DOM-MSN-001에 포함 권장 |
| 0은 빈칸으로만 처리되는가? | ✅ | US-01 AC-1-4(0은 허용), US-03 AC-3-1(0은 누락 계산 제외), SC-BND-VAL-003 확장 케이스 | — |
| 누락 숫자가 정확히 2개인지 검증되는가? | ✅ | US-03 AC-3-3: "반환 목록의 원소 수는 정확히 2이다" | 전용 시나리오는 없음 — SC-DOM-MSN-001 추가 시 포함 권장 |
| 누락 숫자가 오름차순으로 반환되는가? | ✅ | US-03 AC-3-4: "누락 숫자는 오름차순으로 반환된다" | 전용 시나리오는 없음 — SC-DOM-MSN-001 추가 시 포함 권장 |

---

## 6. Invariant Coverage Check

| Invariant | Covered by Story | Covered by Scenario | Future RED Test ID | Status |
|---|---|---|---|---|
| 입력은 4×4여야 한다 | US-01 AC-1-1, AC-1-2 | ❌ 전용 시나리오 없음 | RED-BND-VAL-004 (추가 필요) | ⚠️ |
| 빈칸은 정확히 2개여야 한다 | US-01 AC-1-3 | SC-BND-VAL-001 ✅ | RED-BND-VAL-001 | ✅ |
| 값은 0 또는 1~16이어야 한다 | US-01 AC-1-4 | SC-BND-VAL-003 ✅ | RED-BND-VAL-003 | ✅ |
| 0을 제외한 중복 숫자는 금지된다 | US-01 AC-1-5 | SC-BND-VAL-002 ✅ | RED-BND-VAL-002 | ✅ |
| 누락 숫자는 정확히 2개여야 한다 | US-03 AC-3-3 | ❌ 전용 시나리오 없음 | RED-DOM-MSN-001 (추가 필요) | ⚠️ |
| 누락 숫자는 오름차순이어야 한다 | US-03 AC-3-4 | ❌ 전용 시나리오 없음 | RED-DOM-MSN-001 (추가 필요) | ⚠️ |
| 모든 행의 합은 34여야 한다 | US-04 AC-4-1 | SC-DOM-SOL-001 (간접 검증) ✅ | RED-DOM-VAL-001 (추가 권장) | ⚠️ |
| 모든 열의 합은 34여야 한다 | US-04 AC-4-2 | SC-DOM-SOL-001 (간접 검증) ✅ | RED-DOM-VAL-001 (추가 권장) | ⚠️ |
| 두 대각선의 합은 각각 34여야 한다 | US-04 AC-4-3, AC-4-4 | SC-DOM-SOL-001 (간접 검증) ✅ | RED-DOM-VAL-001 (추가 권장) | ⚠️ |
| 결과는 int[6]이어야 한다 | US-05 AC-5-3, AC-5-4 | SC-DOM-SOL-001 ✅ | RED-DOM-SOL-001 | ✅ |
| 결과 좌표는 1-index여야 한다 | US-05 AC-5-5 | SC-DOM-SOL-001 ✅ | RED-DOM-SOL-001 | ✅ |

> **간접 검증 주석:** SC-DOM-SOL-001은 완성된 행렬이 34를 만족함을 수치로 증명하지만, 이는 Solver 시나리오 안에서 Validator가 호출되는 형태다. `MagicSquareValidator`의 10개 조건 독립 실패 케이스(행만 실패, 열만 실패 등)는 전용 시나리오(SC-DOM-VAL-001)가 없다.

---

## 7. Dual-Track TDD Readiness Check

| Check Item | Status | Evidence | Issue / Fix |
|---|---|---|---|
| UI/Boundary RED 테스트로 분리 가능한가? | ✅ | SC-BND-VAL-001~003이 각각 독립 Boundary RED 테스트로 변환 가능. US-01 AC-1-6(Domain 미호출)이 격리 검증 조건 제공 | — |
| Logic/Domain RED 테스트로 분리 가능한가? | ⚠️ | SC-DOM-SOL-001은 Domain RED 테스트 변환 가능. 그러나 BlankFinder·MissingNumberFinder·MagicSquareValidator 전용 RED가 없음 | SC-DOM-BLK-001, SC-DOM-MSN-001, SC-DOM-VAL-001 추가 필요 |
| GREEN 단계에서 최소 구현으로 처리 가능한가? | ✅ | Level 2 Stage 4 GREEN Minimal Implementation Principle 명시 / Level 3 전체 AC가 단일 기능 단위로 작성됨 | — |
| REFACTOR 단계에서 계약 변경 없이 구조 개선 가능한가? | ✅ | Level 2 Stage 4 REFACTOR Principle: "외부 계약 변경 없이 내부 구현만 변경" / US-05 AC-5-3~6이 출력 계약을 고정 | — |
| 테스트 약화 없이 통과 가능한 구조인가? | ✅ | 각 AC가 구체적 조건(`int[6]`, 길이 6, 1-index, 오름차순 등)으로 작성되어 assert 약화 없이 GREEN 달성 가능 | — |

---

## 8. Implementation Possibility Check

| Check Item | Status | Evidence | Issue / Fix |
|---|---|---|---|
| BlankFinder로 분리 가능한가? | ✅ | US-02 AC-2-1~5: 입력·출력·좌표 기준·순서 모두 명세됨. 다른 도메인에 비의존적 | — |
| MissingNumberFinder로 분리 가능한가? | ✅ | US-03 AC-3-1~4: 입력·출력·정렬 기준 모두 명세됨. BlankFinder와 독립 | — |
| MagicSquareValidator로 분리 가능한가? | ✅ | US-04 AC-4-1~7: 10개 조건 각각 독립 명세. Solver·BlankFinder에 비의존 | — |
| Solver로 분리 가능한가? | ✅ | US-05 AC-5-1~8: 시도 순서·출력 형식·실패 처리 명세. BlankFinder·MissingNumberFinder·Validator 조합으로 구현 가능 | — |
| Boundary Validator로 분리 가능한가? | ✅ | US-01 AC-1-1~7: 4×4, 범위, 빈칸 수, 중복 각각 독립 검증 로직으로 분리 가능 | — |
| 하드코딩 없이 구현 가능한가? | ✅ | US-04 AC-4-7: Magic Constant는 `n(n²+1)/2` 또는 명명된 상수로 유도 명시 / Level 1 Invariant Level 2에서 하드코딩 금지 선언 | — |
| 매직 넘버가 명명된 상수로 대체 가능한가? | ✅ | Epic SC4: `GRID_SIZE`, `MAX_VALUE`, `MAGIC_CONSTANT` 명명 기준 명시 / cursorrules의 `constants.py` 구조와 일치 | — |

---

## 9. Traceability Matrix

| Epic Goal | Journey Stage | User Story | Acceptance Criteria | Technical Scenario | Future RED Test ID | Future Implementation Task |
|---|---|---|---|---|---|---|
| 불변식 중심 설계 사고 훈련 | Stage 1: Problem Recognition | US-01 입력 검증 | AC-1-1~2: 4×4 구조 위반 거부 | SC-BND-VAL-004 (추가 필요) | RED-BND-VAL-004 | TASK-BND-VAL-004 |
| 입력/출력 계약 명확화 | Stage 2: Contract Definition | US-01 입력 검증 | AC-1-3: 빈칸 수 ≠ 2 거부 | SC-BND-VAL-001 | RED-BND-VAL-001 | TASK-BND-VAL-001 |
| 입력/출력 계약 명확화 | Stage 2: Contract Definition | US-01 입력 검증 | AC-1-5: 0 제외 중복 거부 | SC-BND-VAL-002 | RED-BND-VAL-002 | TASK-BND-VAL-002 |
| 입력/출력 계약 명확화 | Stage 2: Contract Definition | US-01 입력 검증 | AC-1-4: 범위 위반 거부 | SC-BND-VAL-003 | RED-BND-VAL-003 | TASK-BND-VAL-003 |
| Domain Logic / UI 책임 분리 | Stage 3: Domain Separation | US-01 입력 검증 | AC-1-6: 검증 실패 시 Domain 미호출 | SC-BND-VAL-001~003 (공통 Then) | RED-BND-VAL-001~003 | TASK-BND-VAL-001~003 |
| Domain Logic / UI 책임 분리 | Stage 3: Domain Separation | US-02 빈칸 좌표 탐색 | AC-2-1~5: BlankFinder 독립 동작 | SC-DOM-BLK-001 (추가 필요) | RED-DOM-BLK-001 | TASK-DOM-BLK-001 |
| Domain Logic / UI 책임 분리 | Stage 3: Domain Separation | US-03 누락 숫자 탐색 | AC-3-1~4: MissingNumberFinder 독립 동작 | SC-DOM-MSN-001 (추가 필요) | RED-DOM-MSN-001 | TASK-DOM-MSN-001 |
| 불변식 중심 설계 사고 훈련 | Stage 1: Problem Recognition | US-04 마방진 검증 | AC-4-1~6: 10개 조건 각각 독립 검증 | SC-DOM-VAL-001 (추가 필요) | RED-DOM-VAL-001 | TASK-DOM-VAL-001 |
| 불변식 중심 설계 사고 훈련 | Stage 1: Problem Recognition | US-04 마방진 검증 | AC-4-7: Magic Constant 하드코딩 금지 | SC-DOM-VAL-001 (추가 필요) | RED-DOM-VAL-001 | TASK-DOM-VAL-001 |
| Dual-Track TDD 경험 | Stage 4: Dual-Track TDD | US-05 두 가지 조합 시도 | AC-5-1: small-first 성공 | SC-DOM-SOL-002 (추가 필요) | RED-DOM-SOL-002 | TASK-DOM-SOL-002 |
| Dual-Track TDD 경험 | Stage 4: Dual-Track TDD | US-05 두 가지 조합 시도 | AC-5-1~2: small-first 실패 후 reverse 성공 | SC-DOM-SOL-001 ✅ | RED-DOM-SOL-001 | TASK-DOM-SOL-001 |
| 입력/출력 계약 명확화 | Stage 2: Contract Definition | US-05 두 가지 조합 시도 | AC-5-3~6: int[6], 길이 6, 1-index, 형식 | SC-DOM-SOL-001 ✅ | RED-DOM-SOL-001 | TASK-DOM-SOL-001 |
| 리팩토링 내성 확보 | Stage 5: Regression Protection | US-05 두 가지 조합 시도 | AC-5-7: 두 조합 모두 실패 시 정의된 실패 | SC-DOM-SOL-003 (추가 필요) | RED-DOM-SOL-003 | TASK-DOM-SOL-003 |
| 리팩토링 내성 확보 | Stage 5: Regression Protection | US-01~05 전체 | 리팩토링 후 전체 AC 동일 통과 | 전체 시나리오 재실행 | 모든 RED 재실행 | — |

---

## 10. Missing Items / Correction Needed

| Missing or Weak Item | Why It Matters | Suggested Fix |
|---|---|---|
| SC-DOM-SOL-002 부재 (small-first 성공 케이스) | 시도 순서 계약의 정방향 성공 케이스가 없으면 small-first 로직의 GREEN 검증이 불완전 | 누락 숫자를 작은 값 우선으로 배치했을 때 마방진이 완성되는 구체적 행렬과 기대 반환값을 포함한 시나리오 추가 |
| SC-DOM-SOL-003 부재 (두 조합 모두 실패 케이스) | AC-5-7이 Acceptance Criteria로 정의되어 있으나 Gherkin 변환이 없어 RED Test 분해 불가 | 두 조합 모두 34를 만족하지 않는 행렬을 Given으로 제공하고, 정의된 실패 반환을 Then으로 명시하는 시나리오 추가 |
| SC-BND-VAL-004 부재 (4×4 구조 위반 케이스) | US-01 AC-1-1~2가 Acceptance Criteria로 존재하나 전용 시나리오 없음 | 3×4, 5×4, 4×3 등 비(非) 4×4 행렬을 Given으로 사용하는 시나리오 추가 |
| SC-DOM-BLK-001 부재 (BlankFinder 독립 시나리오) | Level 3 Domain 책임 분리(Level 3 Invariant)를 검증하는 시나리오가 없으면 BlankFinder의 RED Test 분해 불가 | 빈칸 위치가 경계 셀(1,1)과 (4,4)인 행렬을 Given으로 사용, row-major 순서와 좌표 기준을 Then으로 검증하는 시나리오 추가 |
| SC-DOM-MSN-001 부재 (MissingNumberFinder 독립 시나리오) | 누락 숫자 탐색 로직의 경계값(1, 16)과 오름차순 정렬을 독립 검증하는 시나리오가 없음 | 누락 숫자가 1과 16인 케이스, 비연속 누락 케이스를 Given으로 포함하는 시나리오 추가 |
| SC-DOM-VAL-001 부재 (MagicSquareValidator 독립 시나리오) | 10개 조건의 독립 실패 검증(행만 실패, 열만 실패 등)이 시나리오로 없어 AC-4-5~6의 RED Test 분해 불가 | 행 조건만 위반하는 행렬, 열 조건만 위반하는 행렬, 대각선 조건만 위반하는 행렬을 각각 Given으로 사용하는 시나리오 추가 |
| Level 2와 Level 3 User Story 번호 불일치 | US-01~13 (Level 2)과 US-01~05 (Level 3)의 번호 체계가 달라 추적 시 혼란 발생 | Section 3의 대응 매핑 표를 공식 참조로 사용하거나, Level 3 번호를 US-L3-01~05 형식으로 재표기 |
| MagicSquareValidator의 10개 조건 독립 실패가 SC-DOM-SOL-001로 간접 검증됨 | Solver 시나리오 안에서 Validator가 호출되므로, Validator 단독 실패 케이스는 검증되지 않음 | SC-DOM-VAL-001 추가 시 각 조건별 위반 행렬을 독립 Given으로 사용 |

---

## 11. Final Summary

- **검증 결과:**
  Epic → Journey → User Story → Technical Scenario의 주요 흐름은 일관되게 연결되어 있다. 계약과 불변식 기반 추적 구조가 전 레벨에 걸쳐 유지되며, Boundary / Domain 책임 분리가 Layer 명시와 Invariant 참조로 구체화되어 있다. 그러나 Domain 독립 컴포넌트 3개(BlankFinder, MissingNumberFinder, MagicSquareValidator)의 전용 시나리오가 부재하고, Solver의 성공 케이스 및 전체 실패 케이스 시나리오가 누락되어 RED Test 분해가 불완전하다.

- **가장 강한 부분:**
  SC-DOM-SOL-001의 수치 기반 Given-When-Then 구조. 실제 행렬 데이터와 검증 근거(29 ≠ 34)가 포함되어 테스트 케이스로의 직접 변환이 가능하다. 또한 Level 1~4 전반에 걸쳐 `Magic Constant 하드코딩 금지` (Level 2 Invariant)가 Epic → Journey → US-04 AC-4-7 → 구현 요건까지 일관되게 추적된다.

- **가장 약한 부분:**
  Domain 독립 컴포넌트 시나리오의 전면 부재. BlankFinder, MissingNumberFinder, MagicSquareValidator 각각에 대한 Gherkin 시나리오가 없어 Level 3 Domain Separation (Level 3 Invariant)의 구현 분리가 RED Test 수준에서 검증되지 않는다. 이는 실제 TDD 실습 시 컴포넌트 경계가 모호해지는 원인이 될 수 있다.

- **반드시 수정해야 할 항목:**
  1. SC-DOM-SOL-002 추가 — small-first 성공 케이스 (시도 순서 계약의 정방향 검증)
  2. SC-DOM-SOL-003 추가 — 두 조합 모두 실패 케이스 (AC-5-7 RED Test 분해 전제 조건)
  3. SC-DOM-VAL-001 추가 — MagicSquareValidator 10개 조건 독립 실패 시나리오
  4. SC-DOM-BLK-001 추가 — BlankFinder 독립 시나리오 (row-major, 좌표 기준 검증)
  5. SC-DOM-MSN-001 추가 — MissingNumberFinder 독립 시나리오 (경계값, 오름차순 검증)
  6. SC-BND-VAL-004 추가 — 4×4 구조 위반 케이스 (AC-1-1~2 RED Test 분해 전제 조건)

- **다음 단계로 진행 가능 여부:**
  **조건부 가능.** 현재 존재하는 4개 시나리오(SC-DOM-SOL-001, SC-BND-VAL-001~003)를 기반으로 RED-DOM-SOL-001과 RED-BND-VAL-001~003의 RED Test 작성은 즉시 시작 가능하다. 단, Domain 독립 컴포넌트의 RED Test를 병렬로 진행하려면 SC-DOM-BLK-001, SC-DOM-MSN-001, SC-DOM-VAL-001, SC-DOM-SOL-002~003의 시나리오를 먼저 보완한 후 전체 RED → GREEN → REFACTOR 사이클을 일관되게 진행하는 것이 권장된다.
