from enum import Enum, auto

_NEW_BRANCH_PUSHED_BEFORE = "0" * 40


class BaseResolution(Enum):
    """比較元のコミットを解決できたかと、解決できない理由。"""

    RESOLVED = auto()
    NEW_BRANCH_PUSH = auto()
    MISSING = auto()


def classify_unresolved_base(pull_request_base: str | None, pushed_before: str | None) -> BaseResolution:
    """解決できない比較元を、解決できない理由に分ける。

    Args:
        pull_request_base: 取り込み先のコミット。None と空文字は、指定がないことを表す。
        pushed_before: プッシュ前のコミット。None と空文字は、指定がないことを表す。
    """
    if not pull_request_base and pushed_before == _NEW_BRANCH_PUSHED_BEFORE:
        return BaseResolution.NEW_BRANCH_PUSH
    return BaseResolution.MISSING
