class BaseNotSpecifiedError(Exception):
    """取り込み先のコミットもプッシュ前のコミットも指定されていない。"""


class PullRequestBaseNotFoundError(Exception):
    """指定された取り込み先のコミットがリポジトリにない。"""


class PushedBeforeNotFoundError(Exception):
    """指定されたプッシュ前のコミットがリポジトリにない。"""
