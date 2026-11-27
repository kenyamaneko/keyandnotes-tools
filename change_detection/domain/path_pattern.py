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
        added_excluded_paths: 標準の除外パスに足す、パスのパターン。`*` は `/` を含む任意の文字列に一致する。
    """
    return any(fnmatchcase(path, pattern) for pattern in (*_STANDARD_EXCLUDED_PATHS, *added_excluded_paths))


def is_in_scope(path: str, scope_patterns: Sequence[str]) -> bool:
    """パスが範囲に属するかを返す。

    Args:
        path: リポジトリのルートからのパス。
        scope_patterns: 範囲に属する、パスのパターン。どれか 1 つに当てはまれば範囲に属する。`*` は `/` を含む任意の文字列に一致する。
    """
    return any(fnmatchcase(path, pattern) for pattern in scope_patterns)
