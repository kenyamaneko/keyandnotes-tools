import argparse
from collections.abc import Callable
from typing import TextIO

from version_tag.domain import NoVersionTagError, UnknownBumpKindError

EXIT_CODE_SUCCESS = 0
EXIT_CODE_FAILURE = 1


def run_version_tag_command(
    arguments: list[str],
    create_version_tag: Callable[[str], str],
    output: TextIO,
    error_output: TextIO,
) -> int:
    """バージョンタグを打つコマンドを実行する。

    Args:
        arguments: コマンドの引数。`--bump-kind <patch・minor・major>` を取る。
        create_version_tag: バージョンアップの種類を受け取り、打ったバージョンタグを返す。

    Returns:
        終了コード。成功したときは 0、失敗したときは 0 以外。
    """
    parser = argparse.ArgumentParser(prog="version_tag")
    parser.add_argument("--bump-kind", required=True)
    parsed = parser.parse_args(arguments)
    try:
        version_tag = create_version_tag(parsed.bump_kind)
    except (NoVersionTagError, UnknownBumpKindError) as error:
        print(error, file=error_output)
        return EXIT_CODE_FAILURE
    print(version_tag, file=output)
    return EXIT_CODE_SUCCESS
