import re
from typing import Protocol

VersionNumbers = tuple[int, int, int]


class VersionBump(Protocol):
    """バージョンアップの種類ごとの、X.Y.Z の上げ方。"""

    def bump_version(self, version_numbers: VersionNumbers) -> VersionNumbers:
        """X.Y.Z を上げた X.Y.Z を返す。"""
        ...


class PatchBump:
    """patch を上げる。"""

    def bump_version(self, version_numbers: VersionNumbers) -> VersionNumbers:
        major, minor, patch = version_numbers
        return major, minor, patch + 1


class MinorBump:
    """minor を上げ、patch を 0 に戻す。"""

    def bump_version(self, version_numbers: VersionNumbers) -> VersionNumbers:
        major, minor, _ = version_numbers
        return major, minor + 1, 0


class MajorBump:
    """major を上げ、minor と patch を 0 に戻す。"""

    def bump_version(self, version_numbers: VersionNumbers) -> VersionNumbers:
        major, _, _ = version_numbers
        return major + 1, 0, 0


VERSION_BUMPS: dict[str, VersionBump] = {
    "patch": PatchBump(),
    "minor": MinorBump(),
    "major": MajorBump(),
}

VERSION_TAG_PATTERN = re.compile(r"v(\d+)\.(\d+)\.(\d+)")


class NoVersionTagError(Exception):
    """リモートにバージョンタグが 1 つも無い。"""

    def __init__(self):
        super().__init__("バージョンタグが無い。最初のバージョンタグは手で打つ必要がある")


class UnknownBumpKindError(Exception):
    """バージョンアップの種類が patch・minor・major のいずれでもない。"""

    def __init__(self, bump_kind):
        super().__init__(
            f"バージョンアップの種類は {'・'.join(VERSION_BUMPS)} のいずれかを指定する必要がある: {bump_kind}"
        )


def calculate_next_version_tag(tag_names: list[str], bump_kind: str) -> str:
    """タグ名の一覧とバージョンアップの種類から、打つバージョンタグを求める。

    Args:
        bump_kind: バージョンアップの種類。patch・minor・major のいずれか。
    """
    if bump_kind not in VERSION_BUMPS:
        raise UnknownBumpKindError(bump_kind)
    versions = [
        tuple(int(digits) for digits in match.groups())
        for match in map(VERSION_TAG_PATTERN.fullmatch, tag_names)
        if match
    ]
    if not versions:
        raise NoVersionTagError()
    major, minor, patch = VERSION_BUMPS[bump_kind].bump_version(max(versions))
    return f"v{major}.{minor}.{patch}"
