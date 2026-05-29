"""Entity constants — Level 2 derived magic constant."""

from __future__ import annotations

from magic_square.entity.constants import magic_constant


class TestMagicConstantDerived:
    """magic_constant(n) is derived, not hardcoded per n."""

    def test_magic_constant_for_3x3(self) -> None:
        assert magic_constant(3) == 15

    def test_magic_constant_for_4x4(self) -> None:
        assert magic_constant(4) == 34
