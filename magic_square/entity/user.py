"""User 엔티티 — 마방진 해의 귀속(attribution)을 식별하는 도메인 객체.

이 모듈은 ECB의 entity 레이어에 속하며 외부 의존을 갖지 않는다.
도메인 정당성과 불변 조건은 ``Report/user-domain-extension.md`` (Level 4)를 참조한다.

Identity Invariants (Level 4):
    Identity-1: user_id는 비어 있지 않은 문자열이다.
    Identity-2: user_id는 공백만으로 구성되지 않는다.
    Identity-3: name은 비어 있지 않은 문자열이다.
    Identity-4: name은 공백만으로 구성되지 않는다.
    Identity-5: 생성 후 필드는 재할당할 수 없다 (불변성).
    Identity-6: 동등성은 user_id로만 결정된다.
    Identity-7: User는 해시 가능하다.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class User:
    """마방진 해를 탐색·제출한 주체의 도메인 식별자.

    User는 인증·세션·이력 관리 등 응용 책임을 갖지 않는다.
    오직 "이 해가 누구의 것인가"를 도메인 차원에서 식별하기 위한 값 객체이다.

    Attributes:
        user_id: 사용자 고유 식별자. 비어 있지 않은 문자열이며 공백만으로 구성될 수 없다.
        name: 사용자 표시 이름. 비어 있지 않은 문자열이며 공백만으로 구성될 수 없다.

    Raises:
        TypeError: user_id 또는 name이 문자열이 아닌 경우.
        ValueError: user_id 또는 name이 빈 문자열이거나 공백만으로 구성된 경우.

    Example:
        >>> user = User(user_id="user-001", name="Ada Lovelace")
        >>> user.user_id
        'user-001'
    """

    user_id: str
    name: str = field(compare=False)

    def __post_init__(self) -> None:
        """생성 직후 Identity-1~4 불변 조건을 강제한다.

        Raises:
            TypeError: user_id 또는 name이 문자열 타입이 아닌 경우.
            ValueError: user_id 또는 name이 빈 문자열이거나 공백만으로 구성된 경우.
        """
        self._validate_string_field(value=self.user_id, field_name="user_id")
        self._validate_string_field(value=self.name, field_name="name")

    @staticmethod
    def _validate_string_field(value: object, field_name: str) -> None:
        """문자열 필드가 비어 있지 않고 공백 외 문자를 포함하는지 검증한다.

        Args:
            value: 검증 대상 값.
            field_name: 오류 메시지에 사용할 필드명.

        Raises:
            TypeError: value가 str 타입이 아닌 경우.
            ValueError: value가 빈 문자열이거나 공백만으로 구성된 경우.
        """
        if not isinstance(value, str):
            raise TypeError(
                f"{field_name}은(는) 문자열이어야 합니다. "
                f"실제 타입: {type(value).__name__}"
            )

        if not value or not value.strip():
            raise ValueError(
                f"{field_name}은(는) 비어 있거나 공백만으로 구성될 수 없습니다."
            )
