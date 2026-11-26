from typing import Protocol


class GitRepository(Protocol):
    """変更判定が使う、Git のリポジトリの読み取り。"""

    def has_commit(self, commit: str) -> bool:
        """コミットがリポジトリにあるかを返す。"""
        ...

    def list_changed_paths(self, base: str, head: str) -> list[str]:
        """2 つのコミットの間で変更されたファイルのパスを返す。名前の変更は、元のパスの削除と新しいパスの追加として返す。"""
        ...

    def read_file(self, commit: str, path: str) -> str | None:
        """コミット時点のファイルの内容を返す。ファイルがないときは None を返す。"""
        ...
