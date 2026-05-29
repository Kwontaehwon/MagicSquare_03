"""User 엔티티 단위 테스트.

`Report/user-domain-extension.md`의 Level 4 Invariants(Identity-1~7)와
`Report/user-test-list.md`의 T01~T13에 1:1 대응한다.

테스트 규약:
    - AAA(Arrange-Act-Assert) 구조, 각 구역은 빈 줄로 구분.
    - 1 test = 1 behavior.
    - 매직 넘버·매직 문자열 직접 하드코딩 금지 — 도메인 상수 또는 픽스처 사용.
"""

from dataclasses import FrozenInstanceError
from typing import Any

import pytest

from magic_square.entity.user import User


VALID_USER_ID: str = "user-001"
VALID_NAME: str = "Ada Lovelace"
OTHER_USER_ID: str = "user-002"
OTHER_NAME: str = "Grace Hopper"


# ---------------------------------------------------------------------------
# T01 — 정상 생성 (Identity-1, Identity-3)
# ---------------------------------------------------------------------------


def test_user_is_created_when_id_and_name_are_valid() -> None:
    """유효한 user_id와 name으로 User 인스턴스가 생성된다.

    Identity-1, Identity-3을 검증한다.
    """
    user_id: str = VALID_USER_ID
    name: str = VALID_NAME

    user: User = User(user_id=user_id, name=name)

    assert user.user_id == user_id, "user_id가 입력값과 동일해야 한다"
    assert user.name == name, "name이 입력값과 동일해야 한다"


# ---------------------------------------------------------------------------
# T02~T05 — 입력 거부 (Identity-1, Identity-2, Identity-3, Identity-4)
# ---------------------------------------------------------------------------


def test_user_creation_raises_when_user_id_is_empty_string() -> None:
    """빈 문자열 user_id는 ValueError를 발생시킨다.

    Identity-1을 검증한다.
    """
    empty_id: str = ""

    with pytest.raises(ValueError):
        User(user_id=empty_id, name=VALID_NAME)


def test_user_creation_raises_when_user_id_is_blank_whitespace() -> None:
    """공백만으로 구성된 user_id는 ValueError를 발생시킨다.

    Identity-2를 검증한다.
    """
    blank_id: str = "   \t\n"

    with pytest.raises(ValueError):
        User(user_id=blank_id, name=VALID_NAME)


def test_user_creation_raises_when_name_is_empty_string() -> None:
    """빈 문자열 name은 ValueError를 발생시킨다.

    Identity-3을 검증한다.
    """
    empty_name: str = ""

    with pytest.raises(ValueError):
        User(user_id=VALID_USER_ID, name=empty_name)


def test_user_creation_raises_when_name_is_blank_whitespace() -> None:
    """공백만으로 구성된 name은 ValueError를 발생시킨다.

    Identity-4를 검증한다.
    """
    blank_name: str = " \t\n "

    with pytest.raises(ValueError):
        User(user_id=VALID_USER_ID, name=blank_name)


# ---------------------------------------------------------------------------
# T06~T07 — 타입 검증 (Identity-1, Identity-3)
# ---------------------------------------------------------------------------


def test_user_creation_raises_when_user_id_is_not_string() -> None:
    """문자열이 아닌 user_id는 TypeError를 발생시킨다.

    Identity-1의 타입 부분을 검증한다.
    """
    non_string_id: Any = 12345

    with pytest.raises(TypeError):
        User(user_id=non_string_id, name=VALID_NAME)


def test_user_creation_raises_when_name_is_not_string() -> None:
    """문자열이 아닌 name은 TypeError를 발생시킨다.

    Identity-3의 타입 부분을 검증한다.
    """
    non_string_name: Any = None

    with pytest.raises(TypeError):
        User(user_id=VALID_USER_ID, name=non_string_name)


# ---------------------------------------------------------------------------
# T08~T09 — 불변성 (Identity-5)
# ---------------------------------------------------------------------------


def test_user_id_cannot_be_reassigned_after_creation() -> None:
    """생성된 User의 user_id는 재할당할 수 없다.

    Identity-5를 검증한다. ``setattr``를 사용하여 정적 분석기를 우회하지 않고
    런타임 동작을 직접 검증한다.
    """
    user: User = User(user_id=VALID_USER_ID, name=VALID_NAME)

    with pytest.raises(FrozenInstanceError):
        setattr(user, "user_id", OTHER_USER_ID)


def test_user_name_cannot_be_reassigned_after_creation() -> None:
    """생성된 User의 name은 재할당할 수 없다.

    Identity-5를 검증한다. ``setattr``를 사용하여 정적 분석기를 우회하지 않고
    런타임 동작을 직접 검증한다.
    """
    user: User = User(user_id=VALID_USER_ID, name=VALID_NAME)

    with pytest.raises(FrozenInstanceError):
        setattr(user, "name", OTHER_NAME)


# ---------------------------------------------------------------------------
# T10~T12 — 동등성 (Identity-6)
# ---------------------------------------------------------------------------


def test_two_users_are_equal_when_user_ids_match() -> None:
    """user_id가 같은 두 User는 동등하다.

    Identity-6을 검증한다.
    """
    user_a: User = User(user_id=VALID_USER_ID, name=VALID_NAME)
    user_b: User = User(user_id=VALID_USER_ID, name=VALID_NAME)

    assert user_a == user_b, "user_id가 같으면 두 User는 동등해야 한다"


def test_two_users_are_not_equal_when_user_ids_differ() -> None:
    """user_id가 다른 두 User는 동등하지 않다.

    Identity-6을 검증한다.
    """
    user_a: User = User(user_id=VALID_USER_ID, name=VALID_NAME)
    user_b: User = User(user_id=OTHER_USER_ID, name=VALID_NAME)

    assert user_a != user_b, "user_id가 다르면 두 User는 동등하지 않아야 한다"


def test_two_users_are_equal_even_when_only_names_differ() -> None:
    """user_id가 같으면 name이 달라도 두 User는 동등하다.

    Identity-6의 핵심: 동등성은 user_id로만 결정된다.
    """
    user_a: User = User(user_id=VALID_USER_ID, name=VALID_NAME)
    user_b: User = User(user_id=VALID_USER_ID, name=OTHER_NAME)

    assert user_a == user_b, "동등성 기준은 user_id이며 name은 영향을 주지 않아야 한다"


# ---------------------------------------------------------------------------
# T13 — 해시 가능성 (Identity-7)
# ---------------------------------------------------------------------------


def test_user_is_hashable_and_collapses_in_set_when_user_ids_match() -> None:
    """user_id가 같은 두 User는 set에서 하나로 축약된다.

    Identity-7을 검증한다.
    """
    user_a: User = User(user_id=VALID_USER_ID, name=VALID_NAME)
    user_b: User = User(user_id=VALID_USER_ID, name=OTHER_NAME)

    user_set: set[User] = {user_a, user_b}

    assert len(user_set) == 1, "user_id가 같은 두 User는 set에서 1개로 축약되어야 한다"
