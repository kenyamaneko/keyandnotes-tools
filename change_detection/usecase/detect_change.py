from collections.abc import Mapping, Sequence

from change_detection.domain.change_detection_result import ChangeDetectionResult
from change_detection.domain.comment_only_diff import is_code_change
from change_detection.domain.errors import (
    BaseNotSpecifiedError,
    PullRequestBaseNotFoundError,
    PushedBeforeNotFoundError,
)
from change_detection.domain.path_pattern import is_excluded_path, is_in_scope
from change_detection.port.git_repository import GitRepository


def detect_change(
    repository: GitRepository,
    *,
    pull_request_base: str | None,
    pushed_before: str | None,
    is_new_branch_push: bool,
    head: str,
    added_excluded_paths: Sequence[str],
    scopes: Mapping[str, str],
) -> ChangeDetectionResult:
    """変更後のコミットに、コードの変更があるかを範囲ごとに判定する。

    Args:
        pull_request_base: 取り込み先のコミット。プルリクエストでないときは None。
        pushed_before: プッシュ前のコミット。取り込み先のコミットがあるときは使わない。
        is_new_branch_push: 新しいブランチのプッシュか。プッシュ前のコミットがないため、すべてをコードの変更とする。
        added_excluded_paths: 標準の除外パスに足す、パスのパターン。
        scopes: 範囲の名前から、範囲に属するパスのパターンへの対応。
    """
    if is_new_branch_push:
        return ChangeDetectionResult(has_code_change=True, scopes={name: True for name in scopes})
    if pull_request_base is None and pushed_before is None:
        raise BaseNotSpecifiedError
    if pull_request_base is not None:
        base = pull_request_base
        not_found_error = PullRequestBaseNotFoundError
    else:
        base = pushed_before
        not_found_error = PushedBeforeNotFoundError
    if not repository.has_commit(base):
        raise not_found_error(base)

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
    )
