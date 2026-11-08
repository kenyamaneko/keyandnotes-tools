from typing import Protocol


class RemoteTagRepository(Protocol):
    """リモートのタグの一覧の取得と、タグの打ち込みを行う。"""

    def list_tag_names(self) -> list[str]:
        """リモートのタグ名の一覧を返す。"""
        ...

    def push_tag(self, tag_name: str) -> None:
        """現在のコミットに、タグをリモートで打ち込む。"""
        ...
