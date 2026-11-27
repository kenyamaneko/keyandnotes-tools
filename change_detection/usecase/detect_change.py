from collections.abc import Mapping, Sequence

from change_detection.domain.base_resolution import (
    BaseResolution,
    classify_unresolved_base,
)
from change_detection.domain.change_detection_result import ChangeDetectionResult
from change_detection.domain.comment_only_diff import is_code_change
from change_detection.domain.errors import (
    HeadCommitNotFoundError,
    UnparsableSourceError,
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
    scopes: Mapping[str, Sequence[str]],
) -> ChangeDetectionResult:
    """変更後のコミットに、コードの変更があるかを範囲ごとに判定する。

    Args:
        pull_request_base: 取り込み先のコミット。指定がないときは None。
        pushed_before: プッシュ前のコミット。指定がないときと、新しいブランチのプッシュのときは None。取り込み先のコミットの指定があるときは使わない。
        added_excluded_paths: 標準の除外パスに足す、パスのパターン。
        scopes: 範囲の名前から、範囲に属するパスのパターンへの対応。

    Raises:
        HeadCommitNotFoundError: 変更後のコミットがリポジトリにない。
    """
    if not repository.has_commit(head):
        raise HeadCommitNotFoundError(head)
    base = pull_request_base or pushed_before
    # 比較元のコミットがないと差分を取れないため、すべてをコードの変更とする。
    if base is None or not repository.has_commit(base):
        return ChangeDetectionResult(
            has_code_change=True,
            scopes={name: True for name in scopes},
            base_resolution=classify_unresolved_base(base, is_new_branch_push=is_new_branch_push),
            unparsable_paths=(),
        )

    changed_paths = []
    unparsable_paths = []
    for path in repository.list_changed_paths(base, head):
        if is_excluded_path(path, added_excluded_paths):
            continue
        try:
            if not is_code_change(path, repository.find_file(base, path), repository.find_file(head, path)):
                continue
        except UnparsableSourceError:
            # 解析できないファイルは、コメントだけの変更かを確かめられないため、コードの変更とする。
            unparsable_paths.append(path)
        changed_paths.append(path)
    return ChangeDetectionResult(
        has_code_change=bool(changed_paths),
        scopes={name: any(is_in_scope(path, patterns) for path in changed_paths) for name, patterns in scopes.items()},
        base_resolution=BaseResolution.RESOLVED,
        unparsable_paths=tuple(unparsable_paths),
    )
