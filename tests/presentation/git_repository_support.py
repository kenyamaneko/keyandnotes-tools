import os
import subprocess
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path

REPOSITORY_ROOT_PARENT_INDEX = 2
REPOSITORY_ROOT = Path(__file__).resolve().parents[REPOSITORY_ROOT_PARENT_INDEX]
COMMAND_TIMEOUT_SECONDS = 60
ISOLATED_GIT_ENVIRONMENT = {
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "Test Author",
    "GIT_AUTHOR_EMAIL": "author@example.com",
    "GIT_COMMITTER_NAME": "Test Committer",
    "GIT_COMMITTER_EMAIL": "committer@example.com",
}


def run_git(repository, *arguments):
    """リポジトリで git を実行し、標準出力を返す。git が失敗したら例外にする。"""
    completed = subprocess.run(
        ["git", *arguments],
        check=True,
        cwd=repository,
        env={**os.environ, **ISOLATED_GIT_ENVIRONMENT},
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=COMMAND_TIMEOUT_SECONDS,
    )
    return completed.stdout.strip()


def create_repository(directory: Path):
    """空の Git のリポジトリを作る。"""
    directory.mkdir(parents=True)
    run_git(directory, "init", "--quiet", "--initial-branch", "main")
    return directory


def commit_files(repository, files: Mapping[str, str], message):
    """ファイルを書いてコミットし、そのコミットを返す。ファイルが無くても空のコミットを作る。"""
    for path, content in files.items():
        file_path = Path(repository) / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
    run_git(repository, "add", "--all")
    run_git(
        repository,
        "commit",
        "--quiet",
        "--allow-empty",
        "--no-gpg-sign",
        "--message",
        message,
    )
    return run_git(repository, "rev-parse", "HEAD")


def create_commits(repository, snapshots: Sequence[Mapping[str, str]]):
    """ファイルの書き換えの並びを、1 つずつコミットにして、コミットの並びを返す。"""
    return [
        commit_files(repository, files, f"コミット {number}")
        for number, files in enumerate(snapshots, start=1)
    ]


def resolve_commit_references(options, commit_ids):
    """オプションの中の `{番号}` を、その位置のコミットに置き換える。"""
    return [option.format(*commit_ids) for option in options]


def run_change_detection(repository, options):
    """リポジトリをカレントディレクトリにして、変更判定のコマンドを実行し、その結果を返す。"""
    return subprocess.run(
        [sys.executable, "-m", "change_detection", *options],
        check=False,
        cwd=repository,
        env={
            **os.environ,
            **ISOLATED_GIT_ENVIRONMENT,
            "PYTHONPATH": str(REPOSITORY_ROOT),
            "PYTHONIOENCODING": "utf-8",
        },
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=COMMAND_TIMEOUT_SECONDS,
    )


def read_output_lines(output_file: Path):
    """出力ファイルを読み直し、行の並びを返す。"""
    return output_file.read_text(encoding="utf-8").splitlines()


def assert_succeeded(result):
    """変更判定のコマンドが終了コード 0 で終わったことを確かめる。"""
    assert result.returncode == 0, result.stderr


def assert_stopped_with_message(result, *phrases):
    """変更判定のコマンドが 0 以外の終了コードで終わり、標準エラーに原因の語が出ることを確かめる。"""
    assert result.returncode != 0, result.stdout
    for phrase in phrases:
        assert phrase in result.stderr, f"{phrase!r} not in {result.stderr!r}"


def assert_output_line_written(tmp_path, snapshots, options, expected_line):
    """スナップショットの並びをコミットしたリポジトリで変更判定を実行し、出力ファイルに期待する行が書かれたことを確かめる。"""
    repository = create_repository(tmp_path / "repository")
    output_file = tmp_path / "output.txt"
    commit_ids = create_commits(repository, snapshots)
    result = run_change_detection(
        repository,
        [
            *resolve_commit_references(options, commit_ids),
            "--head",
            commit_ids[-1],
            "--output-file",
            str(output_file),
        ],
    )
    assert_succeeded(result)
    assert expected_line in read_output_lines(output_file)
