import pytest


class FakeRemoteTagRepository:
    """リモートのタグ名の一覧を状態として持つ、リモートのタグの偽物。"""

    def __init__(self):
        self.tag_names = []

    def list_tag_names(self):
        return list(self.tag_names)

    def push_tag(self, tag_name):
        self.tag_names.append(tag_name)


@pytest.fixture
def remote_tag_repository():
    """タグが 1 つも無い状態のリモートのタグの偽物を返す。"""
    return FakeRemoteTagRepository()
