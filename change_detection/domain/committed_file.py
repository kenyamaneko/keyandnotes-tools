from dataclasses import dataclass


@dataclass(frozen=True)
class CommittedFile:
    """コミット時点のファイル。

    Attributes:
        file_mode: ファイルの権限と種類を表す値。
    """

    file_mode: str
    content: str
