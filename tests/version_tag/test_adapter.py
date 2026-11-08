import subprocess

import pytest

from version_tag.adapter import GitRemoteTagRepository

GIT_IDENTITY_OPTIONS = [
    "-c",
    "user.name=テスト用の利用者",
    "-c",
    "user.email=test@example.com",
    "-c",
    "commit.gpgsign=false",
    "-c",
    "tag.gpgsign=false",
]


def run_git(directory, *arguments):
    """指定したディレクトリで git を実行し、標準出力の末尾の改行を除いた文字列を返す。"""
    completed = subprocess.run(
        ["git", *GIT_IDENTITY_OPTIONS, "-C", str(directory), *arguments],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def list_remote_tag_names(remote_git_repository):
    return sorted(run_git(remote_git_repository, "tag", "--list").splitlines())


@pytest.fixture
def remote_git_repository(tmp_path):
    """タグが 1 つも無い、ローカルに作った実物の bare リポジトリのパスを返す。"""
    path = tmp_path / "remote.git"
    run_git(tmp_path, "init", "--bare", "--initial-branch=main", str(path))
    return path


@pytest.fixture
def working_clone(tmp_path, remote_git_repository, monkeypatch):
    """テスト用のリモートの複製を返す。"""
    path = tmp_path / "working"
    run_git(tmp_path, "clone", str(remote_git_repository), str(path))
    run_git(path, "commit", "--allow-empty", "-m", "最初のコミット")
    run_git(path, "commit", "--allow-empty", "-m", "次のコミット")
    monkeypatch.chdir(path)
    return path


class Test本体__バージョンタグ__保存と取得__リモートのタグの取得と打ち込み:
    def test_リモートに軽量タグ_v1ドット4ドット2_と注釈付きタグ_v1ドット5ドット0ハイフンrc1_があるとき_リモートのタグ名の一覧を取得すると_タグ名の一覧は_v1ドット4ドット2_と_v1ドット5ドット0ハイフンrc1_の_2_件になる(
        self, record_case, working_clone
    ):
        record_case(
            kind="インフラ結合テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "Given",
                    "リモートに軽量タグ `v1.4.2` と注釈付きタグ `v1.5.0-rc1` があるとき",
                ),
                ("When", "リモートのタグ名の一覧を取得する"),
                ("Then", "タグ名の一覧は `v1.4.2` と `v1.5.0-rc1` の 2 件になる"),
            ],
        )
        run_git(working_clone, "tag", "v1.4.2")
        run_git(working_clone, "tag", "-a", "v1.5.0-rc1", "-m", "リリース候補")
        run_git(working_clone, "push", "origin", "v1.4.2", "v1.5.0-rc1")

        tag_names = GitRemoteTagRepository().list_tag_names()

        assert sorted(tag_names) == ["v1.4.2", "v1.5.0-rc1"]

    def test_リモートにタグが_1_つも無いとき_リモートのタグ名の一覧を取得すると_タグ名の一覧は空になる(
        self, record_case, working_clone
    ):
        record_case(
            kind="インフラ結合テスト",
            normal_or_abnormal="正常系",
            perspectives=["件数・有無"],
            items=[
                ("Given", "リモートにタグが 1 つも無いとき"),
                ("When", "リモートのタグ名の一覧を取得する"),
                ("Then", "タグ名の一覧は空になる"),
            ],
        )

        tag_names = GitRemoteTagRepository().list_tag_names()

        assert tag_names == []

    def test_リモートにタグが_1_つも無いとき_バージョンタグ_v1ドット4ドット3_をリモートへ打ち込むと_リモートのタグ名の一覧は_v1ドット4ドット3_だけになる(
        self, record_case, remote_git_repository, working_clone
    ):
        record_case(
            kind="インフラ結合テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", "リモートにタグが 1 つも無いとき"),
                ("When", "バージョンタグ `v1.4.3` をリモートへ打ち込む"),
                ("Then", "リモートのタグ名の一覧は `v1.4.3` だけになる"),
            ],
        )

        GitRemoteTagRepository().push_tag("v1.4.3")

        assert list_remote_tag_names(remote_git_repository) == ["v1.4.3"]

    def test_コミットをチェックアウトしているとき_バージョンタグ_v1ドット4ドット3_をリモートへ打ち込むと_リモートの_v1ドット4ドット3_が指すコミットは_チェックアウトしているコミットになる(
        self, record_case, remote_git_repository, working_clone
    ):
        record_case(
            kind="インフラ結合テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", "コミットをチェックアウトしているとき"),
                ("When", "バージョンタグ `v1.4.3` をリモートへ打ち込む"),
                (
                    "Then",
                    "リモートの `v1.4.3` が指すコミットは、チェックアウトしているコミットになる",
                ),
            ],
        )
        checked_out_commit = run_git(working_clone, "rev-parse", "HEAD")

        GitRemoteTagRepository().push_tag("v1.4.3")

        assert (
            run_git(remote_git_repository, "rev-parse", "v1.4.3^{commit}")
            == checked_out_commit
        )

    def test_リモートに接続できないとき_リモートのタグ名の一覧を取得すると_リモートのタグ名の一覧の取得は_リモートに接続できないことを示すエラーで失敗する_リモートに接続でき_リモートにタグが_v1ドット4ドット2_だけあるとき_リモートのタグ名の一覧を取得すると_タグ名の一覧は_v1ドット4ドット2_だけになる(
        self,
        record_case,
        capfd,
        monkeypatch,
        tmp_path,
        remote_git_repository,
        working_clone,
    ):
        record_case(
            kind="インフラ結合テスト",
            normal_or_abnormal="異常系",
            perspectives=["外部依存の失敗", "回復確認"],
            items=[
                ("Given", "リモートに接続できないとき"),
                ("When", "リモートのタグ名の一覧を取得する"),
                (
                    "Then",
                    "リモートのタグ名の一覧の取得は、リモートに接続できないことを示すエラーで失敗する",
                ),
                (
                    "Given",
                    "リモートに接続でき、リモートにタグが `v1.4.2` だけあるとき",
                ),
                ("When", "リモートのタグ名の一覧を取得する"),
                ("Then", "タグ名の一覧は `v1.4.2` だけになる"),
            ],
        )
        run_git(working_clone, "tag", "v1.4.2")
        run_git(working_clone, "push", "origin", "v1.4.2")
        run_git(
            working_clone, "remote", "set-url", "origin", str(tmp_path / "missing.git")
        )
        monkeypatch.setenv("LC_ALL", "C")
        repository = GitRemoteTagRepository()

        with pytest.raises(subprocess.CalledProcessError):
            repository.list_tag_names()

        assert "does not appear to be a git repository" in capfd.readouterr().err

        run_git(
            working_clone, "remote", "set-url", "origin", str(remote_git_repository)
        )

        assert repository.list_tag_names() == ["v1.4.2"]
