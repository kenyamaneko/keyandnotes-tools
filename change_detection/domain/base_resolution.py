from enum import Enum, auto


class BaseResolution(Enum):
    """比較元のコミットを解決できたかと、解決できない理由。"""

    RESOLVED = auto()
    NEW_BRANCH_PUSH = auto()
    MISSING = auto()


def classify_unresolved_base(base: str | None, *, is_new_branch_push: bool) -> BaseResolution:
    """解決できない比較元を、解決できない理由に分ける。

    Args:
        base: 解決できない比較元のコミット。指定がないときは None。
    """
    if base is None and is_new_branch_push:
        return BaseResolution.NEW_BRANCH_PUSH
    return BaseResolution.MISSING
