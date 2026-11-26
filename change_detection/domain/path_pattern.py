from collections.abc import Sequence
from fnmatch import fnmatchcase

_STANDARD_EXCLUDED_PATHS = (
    "*.md",
    "docs/**",
    "rules/**",
    ".claude/**",
    ".vscode/**",
    ".gitignore",
    "LICENSE",
)


def is_excluded_path(path: str, added_excluded_paths: Sequence[str] = ()) -> bool:
    """パスが除外パスに当てはまるかを返す。

    Args:
        path: リポジトリのルートからのパス。
        added_excluded_paths: 標準の除外パスに足す、パスのパターン。
    """
    return any(fnmatchcase(path, pattern) for pattern in (*_STANDARD_EXCLUDED_PATHS, *added_excluded_paths))


def is_in_scope(path: str, scope_pattern: str) -> bool:
    """パスが範囲に属するかを返す。

    Args:
        path: リポジトリのルートからのパス。
    """
    return fnmatchcase(path, scope_pattern)
