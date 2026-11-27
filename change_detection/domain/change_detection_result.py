from collections.abc import Mapping
from dataclasses import dataclass

from change_detection.domain.base_resolution import BaseResolution


@dataclass(frozen=True)
class ChangeDetectionResult:
    """変更判定の結果。"""

    has_code_change: bool
    scopes: Mapping[str, bool]
    base_resolution: BaseResolution
