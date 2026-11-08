import pytest

from version_tag.domain import (
    NoVersionTagError,
    UnknownBumpKindError,
    calculate_next_version_tag,
)


class Test本体__バージョンタグ__業務ルール__打つバージョンタグを求める:
    @pytest.mark.parametrize(
        ("given", "tag_names", "perspectives"),
        [
            pytest.param(
                "バージョンタグが `v1.4.2` だけあるとき",
                ["v1.4.2"],
                (),
                id="バージョンタグが_v1ドット4ドット2_だけあるとき_バージョンアップの種類_patch_で_打つバージョンタグを求めると_打つバージョンタグは_v1ドット4ドット3_になる",
            ),
            pytest.param(
                "タグが `v1.4.2`・`v1.5.0-rc1`・`latest` のとき",
                ["v1.4.2", "v1.5.0-rc1", "latest"],
                ("エッジケース",),
                id="タグが_v1ドット4ドット2とv1ドット5ドット0ハイフンrc1とlatest_のとき_バージョンアップの種類_patch_で_打つバージョンタグを求めると_打つバージョンタグは_v1ドット4ドット3_になる",
            ),
        ],
    )
    def test_calculates_patch_version_tag_from_version_tag_only(
        self, record_case, given, tag_names, perspectives
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=perspectives,
            items=[
                ("Given", given),
                ("When", "バージョンアップの種類 patch で、打つバージョンタグを求める"),
                ("Then", "打つバージョンタグは `v1.4.3` になる"),
            ],
        )
        assert calculate_next_version_tag(tag_names, "patch") == "v1.4.3"

    def test_バージョンタグが_v1ドット4ドット2_だけあるとき_バージョンアップの種類_minor_で_打つバージョンタグを求めると_打つバージョンタグは_v1ドット5ドット0_になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", "バージョンタグが `v1.4.2` だけあるとき"),
                ("When", "バージョンアップの種類 minor で、打つバージョンタグを求める"),
                ("Then", "打つバージョンタグは `v1.5.0` になる"),
            ],
        )
        assert calculate_next_version_tag(["v1.4.2"], "minor") == "v1.5.0"

    def test_バージョンタグが_v1ドット4ドット2_だけあるとき_バージョンアップの種類_major_で_打つバージョンタグを求めると_打つバージョンタグは_v2ドット0ドット0_になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", "バージョンタグが `v1.4.2` だけあるとき"),
                ("When", "バージョンアップの種類 major で、打つバージョンタグを求める"),
                ("Then", "打つバージョンタグは `v2.0.0` になる"),
            ],
        )
        assert calculate_next_version_tag(["v1.4.2"], "major") == "v2.0.0"

    def test_バージョンタグが_v1ドット2ドット0とv1ドット10ドット0とv1ドット9ドット0_の_3_件あるとき_バージョンアップの種類_patch_で_打つバージョンタグを求めると_打つバージョンタグは_v1ドット10ドット1_になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "Given",
                    "バージョンタグが `v1.2.0`・`v1.10.0`・`v1.9.0` の 3 件あるとき",
                ),
                ("When", "バージョンアップの種類 patch で、打つバージョンタグを求める"),
                ("Then", "打つバージョンタグは `v1.10.1` になる"),
            ],
        )
        assert (
            calculate_next_version_tag(["v1.2.0", "v1.10.0", "v1.9.0"], "patch")
            == "v1.10.1"
        )

    @pytest.mark.parametrize(
        ("given", "tag_names"),
        [
            pytest.param(
                "タグが `latest` だけのとき",
                ["latest"],
                id="タグが_latest_だけのとき_バージョンアップの種類_patch_で_打つバージョンタグを求めると_バージョンタグが無く_最初のバージョンタグは手で打つ必要があることを示すエラーになる",
            ),
            pytest.param(
                "タグが 1 つも無いとき",
                [],
                id="タグが_1_つも無いとき_バージョンアップの種類_patch_で_打つバージョンタグを求めると_バージョンタグが無く_最初のバージョンタグは手で打つ必要があることを示すエラーになる",
            ),
        ],
    )
    def test_fails_to_calculate_version_tag_without_version_tag(
        self, record_case, given, tag_names
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            perspectives=["件数・有無"],
            items=[
                ("Given", given),
                ("When", "バージョンアップの種類 patch で、打つバージョンタグを求める"),
                (
                    "Then",
                    "バージョンタグが無く、最初のバージョンタグは手で打つ必要があることを示すエラーになる",
                ),
            ],
        )
        with pytest.raises(NoVersionTagError) as raised:
            calculate_next_version_tag(tag_names, "patch")
        assert (
            str(raised.value)
            == "バージョンタグが無い。最初のバージョンタグは手で打つ必要がある"
        )

    def test_バージョンタグが_v1ドット4ドット2_だけあるとき_バージョンアップの種類_hotfix_で_打つバージョンタグを求めると_指定できるバージョンアップの種類は_patchとminorとmajor_であることを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                ("Given", "バージョンタグが `v1.4.2` だけあるとき"),
                (
                    "When",
                    "バージョンアップの種類 `hotfix` で、打つバージョンタグを求める",
                ),
                (
                    "Then",
                    "指定できるバージョンアップの種類は patch・minor・major であることを示すエラーになる",
                ),
            ],
        )
        with pytest.raises(UnknownBumpKindError) as raised:
            calculate_next_version_tag(["v1.4.2"], "hotfix")
        assert (
            str(raised.value)
            == "バージョンアップの種類は patch・minor・major のいずれかを指定する必要がある: hotfix"
        )
