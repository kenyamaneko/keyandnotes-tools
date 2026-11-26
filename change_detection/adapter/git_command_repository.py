import subprocess
from pathlib import Path


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

    def read_file(self, commit: str, path: str) -> str | None:
        """コミット時点のファイルの内容を返す。ファイルがないときは None を返す。"""
        if self._run_git_command(["cat-file", "-e", f"{commit}:{path}"], check=False).returncode != 0:
            return None
        return self._run_git_command(["show", f"{commit}:{path}"]).stdout.decode(errors="surrogateescape")

    def _run_git_command(self, arguments: list[str], *, check: bool = True) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(
            ["git", "-C", str(self._repository_directory), *arguments],
            capture_output=True,
            check=check,
        )
