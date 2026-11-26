import argparse
import sys
from collections.abc import Callable, Sequence
from pathlib import Path

from change_detection.domain.change_detection_result import ChangeDetectionResult
from change_detection.domain.errors import (
    BaseNotSpecifiedError,
    PullRequestBaseNotFoundError,
    PushedBeforeNotFoundError,
)

SCOPE_SEPARATOR = "="
NEW_BRANCH_PUSHED_BEFORE = "0" * 40
EXIT_CODE_SUCCESS = 0
EXIT_CODE_FAILURE = 1


def _parse_scope(argument: str) -> tuple[str, str]:
    name, separator, pattern = argument.partition(SCOPE_SEPARATOR)
    if not separator or not name or not pattern:
        raise argparse.ArgumentTypeError(f"<範囲名>=<パスのパターン> の形で指定してください: {argument}")
    return name, pattern


def _parse_arguments(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="change_detection")
    parser.add_argument("--pull-request-base")
    parser.add_argument("--pushed-before")
    parser.add_argument("--head", required=True)
    parser.add_argument("--output-file", type=Path)
    parser.add_argument("--excluded-path", action="append", default=[])
    parser.add_argument("--scope", action="append", default=[], type=_parse_scope)
    return parser.parse_args(argv)


def run_change_detection(
    argv: Sequence[str],
    detect_change: Callable[..., ChangeDetectionResult],
    write_output_file: Callable[[Path, ChangeDetectionResult], None],
) -> int:
    """変更判定をコマンドラインから実行し、終了コードを返す。"""
    arguments = _parse_arguments(argv)
    if arguments.output_file is None:
        print("出力ファイルが指定されていません。--output-file に出力先を指定してください。", file=sys.stderr)
        return EXIT_CODE_FAILURE
    try:
        result = detect_change(
            pull_request_base=arguments.pull_request_base,
            pushed_before=arguments.pushed_before,
            is_new_branch_push=arguments.pull_request_base is None
            and arguments.pushed_before == NEW_BRANCH_PUSHED_BEFORE,
            head=arguments.head,
            added_excluded_paths=arguments.excluded_path,
            scopes=dict(arguments.scope),
        )
    except BaseNotSpecifiedError:
        print(
            "比較元が指定されていません。--pull-request-base か --pushed-before にコミットを指定してください。",
            file=sys.stderr,
        )
        return EXIT_CODE_FAILURE
    except PullRequestBaseNotFoundError as error:
        print(f"取り込み先のコミット {error.args[0]} がリポジトリに存在しません。コミットを確認してください。", file=sys.stderr)
        return EXIT_CODE_FAILURE
    except PushedBeforeNotFoundError as error:
        print(f"プッシュ前のコミット {error.args[0]} がリポジトリに存在しません。コミットを確認してください。", file=sys.stderr)
        return EXIT_CODE_FAILURE
    write_output_file(arguments.output_file, result)
    return EXIT_CODE_SUCCESS
