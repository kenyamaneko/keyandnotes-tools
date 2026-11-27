import io
from collections import namedtuple
from functools import partial

from version_tag.presentation import run_version_tag_command
from version_tag.usecase import create_version_tag

CommandResult = namedtuple("CommandResult", ["exit_code", "output", "error_output"])


def execute_version_tag_command(remote, bump_kind):
    """バージョンタグを打つコマンドを、バージョンアップの種類を指定して実行し、終了コードと出力を返す。"""
    output = io.StringIO()
    error_output = io.StringIO()
    exit_code = run_version_tag_command(
        ["--bump-kind", bump_kind],
        partial(create_version_tag, remote),
        output,
        error_output,
    )
    return CommandResult(exit_code, output.getvalue(), error_output.getvalue())


class Test本体__バージョンタグ__業務ルール__バージョンタグを打つ:
    def test_リモートにバージョンタグが_v1ドット4ドット2_だけあるとき_バージョンタグを打つコマンドを_バージョンアップの種類_patch_を指定して実行すると_バージョンタグを打つコマンドが出力するバージョンタグは_v1ドット4ドット3_になる(
        self, record_case, remote_tag_repository
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", "リモートにバージョンタグが `v1.4.2` だけあるとき"),
                (
                    "When",
                    "バージョンタグを打つコマンドを、バージョンアップの種類 patch を指定して実行する",
                ),
                (
                    "Then",
                    "バージョンタグを打つコマンドが出力するバージョンタグは `v1.4.3` になる",
                ),
            ],
        )
        remote_tag_repository.tag_names = ["v1.4.2"]

        result = execute_version_tag_command(remote_tag_repository, "patch")

        assert result.output == "v1.4.3\n"

    def test_リモートにバージョンタグが_v1ドット4ドット2_だけあるとき_バージョンタグを打つコマンドを_バージョンアップの種類_patch_を指定して実行すると_リモートのバージョンタグは_v1ドット4ドット2_と_v1ドット4ドット3_の_2_件になる(
        self, record_case, remote_tag_repository
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", "リモートにバージョンタグが `v1.4.2` だけあるとき"),
                (
                    "When",
                    "バージョンタグを打つコマンドを、バージョンアップの種類 patch を指定して実行する",
                ),
                ("Then", "リモートのバージョンタグは `v1.4.2` と `v1.4.3` の 2 件になる"),
            ],
        )
        remote_tag_repository.tag_names = ["v1.4.2"]

        execute_version_tag_command(remote_tag_repository, "patch")

        assert remote_tag_repository.list_tag_names() == ["v1.4.2", "v1.4.3"]

    def test_リモートにタグが_latest_だけのとき_バージョンタグを打つコマンドを_バージョンアップの種類_patch_を指定して実行すると_バージョンタグを打つコマンドの実行は_バージョンタグが無く_最初のバージョンタグは手で打つ必要があることを示すエラーで失敗する_リモートに最初のバージョンタグ_v1ドット0ドット0_が打たれているとき_バージョンタグを打つコマンドを_バージョンアップの種類_patch_を指定して実行すると_バージョンタグを打つコマンドが出力するバージョンタグは_v1ドット0ドット1_になる(
        self, record_case, remote_tag_repository
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="異常系",
            perspectives=["回復確認"],
            items=[
                ("Given", "リモートにタグが `latest` だけのとき"),
                (
                    "When",
                    "バージョンタグを打つコマンドを、バージョンアップの種類 patch を指定して実行する",
                ),
                (
                    "Then",
                    "バージョンタグを打つコマンドの実行は、バージョンタグが無く、最初のバージョンタグは手で打つ必要があることを示すエラーで失敗する",
                ),
                (
                    "Given",
                    "リモートに最初のバージョンタグ `v1.0.0` が打たれているとき",
                ),
                (
                    "When",
                    "バージョンタグを打つコマンドを、バージョンアップの種類 patch を指定して実行する",
                ),
                (
                    "Then",
                    "バージョンタグを打つコマンドが出力するバージョンタグは `v1.0.1` になる",
                ),
            ],
        )
        remote_tag_repository.tag_names = ["latest"]

        failed = execute_version_tag_command(remote_tag_repository, "patch")

        assert failed.exit_code != 0
        assert (
            failed.error_output
            == "バージョンタグが無い。最初のバージョンタグは手で打つ必要がある\n"
        )

        remote_tag_repository.tag_names = ["latest", "v1.0.0"]

        recovered = execute_version_tag_command(remote_tag_repository, "patch")

        assert recovered.output == "v1.0.1\n"

    def test_リモートにバージョンタグが_v1ドット4ドット2_だけあるとき_バージョンタグを打つコマンドを_バージョンアップの種類_hotfix_を指定して実行すると_バージョンタグを打つコマンドの実行は_指定できるバージョンアップの種類は_patchとminorとmajor_であることを示すエラーで失敗する_バージョンタグを打つコマンドを_バージョンアップの種類_patch_を指定して実行すると_バージョンタグを打つコマンドが出力するバージョンタグは_v1ドット4ドット3_になる(
        self, record_case, remote_tag_repository
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="異常系",
            perspectives=["回復確認"],
            items=[
                ("Given", "リモートにバージョンタグが `v1.4.2` だけあるとき"),
                (
                    "When",
                    "バージョンタグを打つコマンドを、バージョンアップの種類 `hotfix` を指定して実行する",
                ),
                (
                    "Then",
                    "バージョンタグを打つコマンドの実行は、指定できるバージョンアップの種類は patch・minor・major であることを示すエラーで失敗する",
                ),
                (
                    "When",
                    "バージョンタグを打つコマンドを、バージョンアップの種類 patch を指定して実行する",
                ),
                (
                    "Then",
                    "バージョンタグを打つコマンドが出力するバージョンタグは `v1.4.3` になる",
                ),
            ],
        )
        remote_tag_repository.tag_names = ["v1.4.2"]

        failed = execute_version_tag_command(remote_tag_repository, "hotfix")

        assert failed.exit_code != 0
        assert (
            failed.error_output
            == "バージョンアップの種類は patch・minor・major のいずれかを指定する必要がある: hotfix\n"
        )

        recovered = execute_version_tag_command(remote_tag_repository, "patch")

        assert recovered.output == "v1.4.3\n"
