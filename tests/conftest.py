import pytest


@pytest.fixture
def record_case(record_property):
    """ケースの種別・正常異常・観点・項目を、テスト結果の項目として載せる関数を返す。

    Args:
        kind: 種別。
        normal_or_abnormal: 正常異常。
        perspectives: 観点。観点ごとに 1 項目として載せる。
        items: (キー, 値) の並び。Given・When・Then の順に、ステップの数だけ並べる。
    """

    def record(*, kind, normal_or_abnormal, items, perspectives=()):
        record_property("種別", kind)
        record_property("正常異常", normal_or_abnormal)
        for perspective in perspectives:
            record_property("観点", perspective)
        for key, value in items:
            record_property(key, value)

    return record
