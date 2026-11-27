import argparse
import json
import sys
from collections.abc import Callable, Sequence
from pathlib import Path

from change_detection.domain.base_resolution import BaseResolution
from change_detection.domain.change_detection_result import ChangeDetectionResult
from change_detection.domain.errors import HeadCommitNotFoundError

SCOPE_SEPARATOR = "="
EXIT_CODE_SUCCESS = 0
EXIT_CODE_FAILURE = 1
# GitHub Actions は、新しいブランチのプッシュでは、プッシュ前のコミットに 40 桁の 0 を渡すため、この値で見分ける。
NEW_BRANCH_PUSHED_BEFORE = "0" * 40


def _parse_scope(argument: str) -> tuple[str, str]:
    name, separator, pattern = argument.partition(SCOPE_SEPARATOR)
    if not separator or not name or not pattern:
        raise argparse.ArgumentTypeError(f"<範囲名>=<パスのパターン> の形で指定してください: {argument}")
    return name, pattern


def _group_scope_patterns(scopes: Sequence[tuple[str, str]]) -> dict[str, list[str]]:
    patterns_by_name: dict[str, list[str]] = {}
    for name, pattern in scopes:
        patterns_by_name.setdefault(name, []).append(pattern)
    return patterns_by_name


def _parse_arguments(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="change_detection")
    parser.add_argument("--pull-request-base")
    parser.add_argument("--pushed-before")
    parser.add_argument("--head", required=True)
    parser.add_argument("--output-file")
    parser.add_argument("--excluded-path", action="append", default=[])
    parser.add_argument("--scope", action="append", default=[], type=_parse_scope)
    return parser.parse_args(argv)


def _log_unresolved_base(
    base_resolution: BaseResolution, pull_request_base: str | None, pushed_before: str | None
) -> None:
    record = {
        "level": "Info" if base_resolution is BaseResolution.NEW_BRANCH_PUSH else "Warn",
        "message": "比較元のコミットを解決できないため、すべてをコードの変更とします。",
        "pull_request_base": pull_request_base,
        "pushed_before": pushed_before,
    }
    print(json.dumps(record, ensure_ascii=False), file=sys.stderr)


def _log_unparsable_file(path: str) -> None:
    record = {"level": "Warn", "message": "ファイルを解析できないため、コードの変更とします。", "path": path}
    print(json.dumps(record, ensure_ascii=False), file=sys.stderr)


def run_change_detection(
    argv: Sequence[str],
    detect_change: Callable[..., ChangeDetectionResult],
    write_output_file: Callable[[Path, ChangeDetectionResult], None],
) -> int:
    """変更判定をコマンドラインから実行し、終了コードを返す。"""
    arguments = _parse_arguments(argv)
    if not arguments.output_file:
        print("出力ファイルが指定されていません。--output-file に出力先を指定してください。", file=sys.stderr)
        return EXIT_CODE_FAILURE
    is_new_branch_push = arguments.pushed_before == NEW_BRANCH_PUSHED_BEFORE
    try:
        result = detect_change(
            pull_request_base=arguments.pull_request_base or None,
            pushed_before=None if is_new_branch_push else arguments.pushed_before or None,
            is_new_branch_push=is_new_branch_push,
            head=arguments.head,
            added_excluded_paths=arguments.excluded_path,
            scopes=_group_scope_patterns(arguments.scope),
        )
    except HeadCommitNotFoundError as error:
        print(
            f"変更後のコミット {error.head} がリポジトリにありません。--head にリポジトリにあるコミットを指定してください。",
            file=sys.stderr,
        )
        return EXIT_CODE_FAILURE
    if result.base_resolution is not BaseResolution.RESOLVED:
        _log_unresolved_base(result.base_resolution, arguments.pull_request_base, arguments.pushed_before)
    for path in result.unparsable_paths:
        _log_unparsable_file(path)
    write_output_file(Path(arguments.output_file), result)
    return EXIT_CODE_SUCCESS
