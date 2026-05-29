# Dual-Track RED 설계표 — 대화 트랜스크립트 (Full Export)

**작성일**: 2026-05-29  
**형식**: 사용자 요청 원문 + 어시스턴트 산출물 (RED 설계표 세션)  
**TDD phase**: RED (설계만)  
**요약 보고서**: `Report/11-dual-track-red-design-report.md`  
**선행 Export**: `Prompt/07-prd-boundary-red-qa-conversation-transcript.md`

---

## 세션 개요

| 항목 | 내용 |
|---|---|
| 역할 | Dual-Track UI + Logic TDD 전문가 |
| 범위 | FR-01~FR-05 전체 Dual-Track RED 설계표 |
| 금지 | 구현·테스트·스켈레톤·파일 저장·pytest·GREEN/REFACTOR |
| 산출 | UI RED Tests 표 14건 + Logic RED Tests 표 12건 |

---

## Turn 1 — Dual-Track RED 설계표 작성

### [USER] (원문)

```
당신은 Dual-Track UI + Logic TDD 전문가입니다.

**TDD phase: RED** — 오직 RED 테스트 설계표만 작성하십시오.

## 금지 (엄격)
- 구현 코드, 테스트 코드, 스켈레톤 코드 작성 금지
- 클래스/파일 구조 확정 금지
- GREEN / REFACTOR 단계 진입 금지
- pytest 실행·코드 생성·파일 저장 금지 (설계표 텍스트 출력만)

## SSOT (반드시 참조)
- `docs/PRD_MagicSquare.md` v0.2
- `Report/02.MagicSquare_DualTrack_TDD_Design_Report.md`
- `.cursorrules` (ECB, Dual-Track, Test ID 규칙)

## 프로젝트 계약
(입력 4×4, 0=빈칸 2개, int[6] 1-index 출력, M=34, short-circuit 검증 순서,
 E003/E001/E002/E004/E005 Failure envelope, execute 0회 U-FLOW-02,
 Domain Mock 금지, G0~G3, find_blank_coords / find_not_exist_nums /
 is_magic_square / solution 별칭, I1~I11 …)

## 범위
[전체 FR-01~FR-05 Dual-Track RED 설계표]

(Track A U-IN/U-OUT/U-FLOW, Track B D-LOC/D-MIS/D-VAL/D-SOL 상세 지시 …)

## 출력 형식
**TDD phase: RED**
# UI RED Tests | # Logic RED Tests | RED 설계 자체 검수 체크리스트
```

### [ASSISTANT] 산출물 요약

| 항목 | 내용 |
|---|---|
| SSOT 상태 | `docs/PRD_MagicSquare.md` v0.2, `Report/02.MagicSquare_DualTrack_TDD_Design_Report.md` **워크스페이스 미존재** |
| 1차 SSOT | 사용자 명시 계약(E00x, U-*, D-*, I*, G0~G3) |
| 2차 SSOT | `Report/09`, `Report/07` SC-DOM-SOL-001 |
| Track A | 14건 (U-IN 10 + U-OUT 2 + U-FLOW 1) |
| Track B | 12건 (D-LOC~D-SOL) |
| G3 | placeholder 명시 |
| 검수 체크리스트 | 6항목 전부 ✅ |

**핵심 설계 결정**
- Boundary: Failure envelope `E003`~`E005`, Python 예외 아님
- U-FLOW-02: invalid 시 `execute.call_count == 0` 별도 행
- Logic: Domain Mock 금지; G1→`[2,2,7,3,3,10]`, G2 surrogate→`[3,3,6,4,4,1]`
- D-VAL-02~06: 행·열·대각·중복·0포함 **분리** 검증

**상세 표** → `Report/11-dual-track-red-design-report.md` §3~§4

---

## Turn 2 — Report · Prompt Export (본 Turn)

### [USER] (원문)

```
Report 폴더에 보고서 생성하고, Prompting 폴더에 Transcript도 Export 해줘
```

### [ASSISTANT] 산출물

| 파일 | 설명 |
|---|---|
| `Report/11-dual-track-red-design-report.md` | Dual-Track RED 설계 통합 보고서 |
| `Prompt/08-dual-track-red-design-conversation-transcript.md` | 본 문서 (Full Export) |

---

## 산출물 인덱스 (본 세션)

| 유형 | 경로 |
|---|---|
| Report 11 | `Report/11-dual-track-red-design-report.md` |
| Prompt 08 | `Prompt/08-dual-track-red-design-conversation-transcript.md` |

---

## 재현 프롬프트 (요약)

```
Dual-Track TDD 전문가로서 TDD phase RED만 수행하라.
FR-01~FR-05 전체에 대해 U-IN/U-OUT/U-FLOW(Track A)와
D-LOC/D-MIS/D-VAL/D-SOL(Track B) RED 설계표를 작성하라.
코드·테스트·파일 저장 금지. G0~G3 격자 부록 포함.
```

---

## 다음 사용자 프롬프트 (권장)

```
Report/11의 E001/E003 체계와 기존 test_plan.md INVALID_SIZE를
PRD v0.2 기준으로 통일한 뒤, U-IN-01 RED 테스트 코드만 작성하라.
pytest FAILED 확인 후 GREEN은 하지 마라.
```

---

## Report · Prompt 번호 체계 (갱신)

| # | Report | Prompt |
|---|---|---|
| 10 | PRD · Boundary RED · QA | 07 |
| **11** | **Dual-Track RED 설계** | **08** |
