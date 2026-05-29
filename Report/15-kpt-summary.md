# KPT 요약 — Cursor AI TDD 적용 + 현업 적용 계획

> **대상**: BIOS 엔지니어 (현업 Claude Code · Codex 전환 예정)  
> **작성일**: 2026-05-29

---

## Keep

- 구현 전 Invariant(불변 조건) 먼저 선언 → 테스트 ID와 코드가 1:1 추적 가능
- Cursor Rules(`alwaysApply`)로 AI가 구현 직행하는 드리프트를 구조적으로 차단
- Dual-Track TDD — Boundary 계약을 먼저 RED로 고정 후 Domain 로직 구현
- RED 단계에서 결함 목록 등록 → 결함 목록 = GREEN 구현 명세로 직결
- Sub-agent(`code-reviewer`) 위임으로 개발자가 놓친 P0 이슈 독립 발견

## Problem

- AI Rules 설계를 프로젝트 초기에 하지 않아 드리프트 반복 → 설계 시간 낭비
- "최소 구현"이 G1 하드코딩 바이패스로 변질 → "가짜 GREEN" 위험
- Error code SSOT 불완전 — `INVALID_SIZE` vs `E001` 혼재, 상수 중복 정의
- 반대각선 단독 실패 테스트 누락 → Level 1 "각각 독립" 원칙이 테스트에 미반영

## Try

- GREEN 단계 "최소 구현" 기준을 사전에 명시 — 특정 입력 하드코딩은 구현으로 인정하지 않는다
- 반대각선 단독 실패처럼 Level 1 "각각 독립" 원칙을 테스트 케이스에도 동일하게 적용한다
- Error code 등 계약 상수는 PRD 확정 즉시 단일 출처(SSOT)로 코드에 반영하고 혼재를 허용하지 않는다

## 현업 적용 계획 (BIOS 엔지니어 → Claude Code / Codex 전환)

- **1개월**: `CLAUDE.md`에 BIOS 금지 패턴 선언 + 신규 기능 1개에 TDD 적용
- **3개월**: HAL 계약 테스트 + 로직 테스트 Dual-Track, Code Review Sub-agent 운영
- **6개월**: TDD 사이클 스프린트 기본 프로세스 정착 + 레거시 역방향 TDD 시작
