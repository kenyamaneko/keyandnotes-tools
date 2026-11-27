from collections.abc import Mapping, Sequence

from change_detection.domain.base_resolution import (
    BaseResolution,
    classify_unresolved_base,
)
from change_detection.domain.change_detection_result import ChangeDetectionResult
from change_detection.domain.comment_only_diff import is_code_change
from change_detection.domain.path_pattern import is_excluded_path, is_in_scope
from change_detection.port.git_repository import GitRepository


def detect_change(
    repository: GitRepository,
    *,
    pull_request_base: str | None,
    pushed_before: str | None,
    head: str,
    added_excluded_paths: Sequence[str],
    scopes: Mapping[str, str],
) -> ChangeDetectionResult:
    """変更後のコミットに、コードの変更があるかを範囲ごとに判定する。

    Args:
        pull_request_base: 取り込み先のコミット。None と空文字は、指定がないことを表す。
        pushed_before: プッシュ前のコミット。None と空文字は、指定がないことを表す。取り込み先のコミットの指定があるときは使わない。
        added_excluded_paths: 標準の除外パスに足す、パスのパターン。
        scopes: 範囲の名前から、範囲に属するパスのパターンへの対応。
    """
    base = pull_request_base or pushed_before
    # 比較元のコミットがないと差分を取れないため、すべてをコードの変更とする。
    if not base or not repository.has_commit(base):
        return ChangeDetectionResult(
            has_code_change=True,
            scopes={name: True for name in scopes},
            base_resolution=classify_unresolved_base(pull_request_base, pushed_before),
        )

    changed_paths = [
        path
        for path in repository.list_changed_paths(base, head)
        if not is_excluded_path(path, added_excluded_paths)
        and is_code_change(path, repository.read_file(base, path), repository.read_file(head, path))
    ]
    return ChangeDetectionResult(
        has_code_change=bool(changed_paths),
        scopes={
            name: any(is_in_scope(path, pattern) for path in changed_paths)
            for name, pattern in scopes.items()
        },
        base_resolution=BaseResolution.RESOLVED,
    )
