class UnparsableSourceError(Exception):
    """対象言語のソースを解析できない。"""


class HeadCommitNotFoundError(Exception):
    """変更後のコミットがリポジトリにない。"""

    def __init__(self, head: str):
        super().__init__(head)
        self.head = head
