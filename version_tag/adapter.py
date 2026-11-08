import subprocess

REMOTE_NAME = "origin"
TAG_REFERENCE_PREFIX = "refs/tags/"
LS_REMOTE_REFERENCE_COLUMN_INDEX = 1


class GitRemoteTagRepository:
    """カレントディレクトリの git リポジトリのリモートを対象にする。"""

    def list_tag_names(self) -> list[str]:
        """リモートのタグ名の一覧を返す。"""
        completed = subprocess.run(
            ["git", "ls-remote", "--tags", "--refs", REMOTE_NAME],
            check=True,
            stdout=subprocess.PIPE,
            text=True,
        )
        references = [
            line.split("\t")[LS_REMOTE_REFERENCE_COLUMN_INDEX]
            for line in completed.stdout.splitlines()
        ]
        return [reference.removeprefix(TAG_REFERENCE_PREFIX) for reference in references]

    def push_tag(self, tag_name: str) -> None:
        """現在のコミットに、タグをリモートで打ち込む。"""
        subprocess.run(
            ["git", "push", REMOTE_NAME, f"HEAD:{TAG_REFERENCE_PREFIX}{tag_name}"],
            check=True,
        )
