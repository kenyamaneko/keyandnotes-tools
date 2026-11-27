import subprocess
from pathlib import Path

from change_detection.domain.committed_file import CommittedFile


class GitCommandRepository:
    """git コマンドで読む、ローカルの Git のリポジトリ。"""

    def __init__(self, repository_directory: Path):
        self._repository_directory = repository_directory

    def has_commit(self, commit: str) -> bool:
        """コミットがリポジトリにあるかを返す。"""
        return self._run_git_command(["cat-file", "-e", f"{commit}^{{commit}}"], check=False).returncode == 0

    def list_changed_paths(self, base: str, head: str) -> list[str]:
        """2 つのコミットの間で変更されたファイルのパスを返す。名前の変更は、元のパスの削除と新しいパスの追加として返す。"""
        output = self._run_git_command(["diff", "--name-only", "--no-renames", "-z", base, head]).stdout
        return [path.decode(errors="surrogateescape") for path in output.split(b"\0") if path]

    def find_file(self, commit: str, path: str) -> CommittedFile | None:
        """コミット時点のファイルを返す。パスにファイルがないとき (サブモジュールやディレクトリのときを含む) は None を返す。"""
        entry = self._run_git_command(
            ["--literal-pathspecs", "ls-tree", "-z", "--full-tree", commit, "--", path]
        ).stdout
        if not entry:
            return None
        file_mode, object_type, object_id = entry.split(b"\t", 1)[0].decode().split()
        if object_type != "blob":
            return None
        content = self._run_git_command(["cat-file", "blob", object_id]).stdout
        return CommittedFile(file_mode=file_mode, content=content.decode(errors="surrogateescape"))

    def _run_git_command(self, arguments: list[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(
            ["git", "-C", str(self._repository_directory), *arguments],
            capture_output=True,
            check=check,
        )
