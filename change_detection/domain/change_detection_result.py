from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from change_detection.domain.base_resolution import BaseResolution


@dataclass(frozen=True)
class ChangeDetectionResult:
    """変更判定の結果。

    Attributes:
        unparsable_paths: 解析できないため、コードの変更に数えたファイルのパス。
    """

    has_code_change: bool
    scopes: Mapping[str, bool]
    base_resolution: BaseResolution
    unparsable_paths: Sequence[str]
