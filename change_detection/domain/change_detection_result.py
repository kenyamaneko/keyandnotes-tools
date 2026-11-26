from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class ChangeDetectionResult:
    """変更判定の結果。
    """

    has_code_change: bool
    scopes: Mapping[str, bool]
