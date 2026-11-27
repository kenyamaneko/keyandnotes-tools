from version_tag.domain import calculate_next_version_tag
from version_tag.port import RemoteTagRepository


def create_version_tag(remote: RemoteTagRepository, bump_kind: str) -> str:
    """バージョンタグを打ち、打ったバージョンタグを返す。"""
    version_tag = calculate_next_version_tag(remote.list_tag_names(), bump_kind)
    remote.push_tag(version_tag)
    return version_tag
