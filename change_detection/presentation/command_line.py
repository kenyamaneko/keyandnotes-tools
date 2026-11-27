import argparse
import json
import sys
from collections.abc import Callable, Sequence
from pathlib import Path

from change_detection.domain.base_resolution import BaseResolution
from change_detection.domain.change_detection_result import ChangeDetectionResult

SCOPE_SEPARATOR = "="
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
    result = detect_change(
        pull_request_base=arguments.pull_request_base,
        pushed_before=arguments.pushed_before,
        head=arguments.head,
        added_excluded_paths=arguments.excluded_path,
        scopes=dict(arguments.scope),
    )
    if result.base_resolution is not BaseResolution.RESOLVED:
        _log_unresolved_base(result.base_resolution, arguments.pull_request_base, arguments.pushed_before)
    write_output_file(Path(arguments.output_file), result)
    return EXIT_CODE_SUCCESS
