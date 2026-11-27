import sys
from functools import partial

from version_tag.adapter import GitRemoteTagRepository
from version_tag.presentation import run_version_tag_command
from version_tag.usecase import create_version_tag


def main() -> int:
    """git のリモートを相手に、コマンドラインの引数でバージョンタグを打つコマンドを実行する。"""
    remote = GitRemoteTagRepository()
    return run_version_tag_command(
        sys.argv[1:], partial(create_version_tag, remote), sys.stdout, sys.stderr
    )


if __name__ == "__main__":
    sys.exit(main())
