# User 엔티티 Test List (STEP 6 산출물)

> 코드보다 먼저 작성된 검증 목록.
> 각 항목은 `Report/user-domain-extension.md`의 Level 4 Invariants(Identity-1~7)와 1:1 대응한다.

---

## 명명 규약 (`.cursorrules` 준수)

- 파일명: `test_user.py`
- 함수명: `test_<상황>_<기대결과>`
- 구조: AAA (Arrange-Act-Assert) — 각 구역은 빈 줄로 구분
- 1 test = 1 behavior

---

## Test List

| # | Invariant | 테스트 함수 | 검증 대상 행동 | 의존성 |
|---|---|---|---|---|
| T01 | Identity-1, 3 | `test_user_is_created_when_id_and_name_are_valid` | 정상 입력 → 인스턴스 생성 성공 | — |
| T02 | Identity-1 | `test_user_creation_raises_when_user_id_is_empty_string` | `user_id=""` → `ValueError` | T01 |
| T03 | Identity-2 | `test_user_creation_raises_when_user_id_is_blank_whitespace` | `user_id="   "` → `ValueError` | T01 |
| T04 | Identity-3 | `test_user_creation_raises_when_name_is_empty_string` | `name=""` → `ValueError` | T01 |
| T05 | Identity-4 | `test_user_creation_raises_when_name_is_blank_whitespace` | `name="\t\n "` → `ValueError` | T01 |
| T06 | Identity-1 | `test_user_creation_raises_when_user_id_is_not_string` | `user_id=123` → `TypeError` | T01 |
| T07 | Identity-3 | `test_user_creation_raises_when_name_is_not_string` | `name=None` → `TypeError` | T01 |
| T08 | Identity-5 | `test_user_id_cannot_be_reassigned_after_creation` | `user.user_id = "x"` → `FrozenInstanceError` | T01 |
| T09 | Identity-5 | `test_user_name_cannot_be_reassigned_after_creation` | `user.name = "x"` → `FrozenInstanceError` | T01 |
| T10 | Identity-6 | `test_two_users_are_equal_when_user_ids_match` | 동일 `user_id` → `==` True | T01 |
| T11 | Identity-6 | `test_two_users_are_not_equal_when_user_ids_differ` | 다른 `user_id` → `==` False | T01 |
| T12 | Identity-6 | `test_two_users_are_equal_even_when_only_names_differ` | 같은 `user_id`, 다른 `name` → `==` True (귀속 식별자만으로 동등성 판정) | T01, T10 |
| T13 | Identity-7 | `test_user_is_hashable_and_usable_in_set` | `{user_a, user_a_copy}` 길이 1 | T01, T10 |

---

## 우선순위와 진행 순서

```
T01 (창조)  →  T02~T07 (입력 불변식)  →  T08~T09 (불변성)  →  T10~T12 (동등성)  →  T13 (해시)
```

- T01은 모든 후속 테스트의 전제이므로 가장 먼저 RED → GREEN을 통과시킨다.
- T02~T07은 생성 단계 거부 행동 — 묶어서 작성하되, 각 테스트는 한 입력 케이스만 검증한다.
- T08~T09는 dataclass `frozen=True` 또는 `__setattr__` 차단을 검증한다.
- T10~T12는 값 동등성 — `user_id`만 동등성 기준임을 명시.
- T13은 해시 가능성 — Python의 `frozen=True`는 자동으로 `__hash__` 제공.

---

## 의도적으로 누락된 테스트 (도메인 외 책임)

| 누락 항목 | 사유 |
|---|---|
| 비밀번호 검증 | 도메인 외 (인증은 boundary/별도 컨텍스트) |
| 직렬화/역직렬화 | 도메인 외 (file_io는 boundary) |
| 사용자 권한 | 도메인 외 |
| `Grid`/`Solution` 보유 | 향후 별도 엔티티(`Submission`)로 분리 예정 |

---

## 다음 단계

본 Test List가 확정되면:

1. `tests/entity/test_user.py`에 T01~T13을 **AAA 구조**로 작성 (RED)
2. `pytest tests/entity/test_user.py -v` 실행하여 모든 테스트가 **FAILED** 임을 확인 (구현 없음으로 인한 실패)
3. `magic_square/entity/user.py`에 최소한의 구현 작성 (GREEN)
4. 다시 `pytest`로 모든 테스트 통과 확인
