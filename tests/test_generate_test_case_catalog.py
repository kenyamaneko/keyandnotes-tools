import pytest
from catalog_support import (
    assert_message_contains,
    assert_stopped_with_message,
    build_case,
    build_config,
    build_features,
    build_features_of_region,
    build_result_entry,
    generate_catalog_page,
    run_catalog_generation,
    spec_prints,
    write_csharp_result,
    write_dart_result,
    write_go_interleaved_result,
    write_go_result,
    write_kotlin_result,
    write_python_result,
    write_result_file,
    write_typescript_result,
)

import test_case_catalog.generate_test_case_catalog as catalog

LOGIN_TEST_NAME = "[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される"
LOGIN_PROPERTIES = (
    ("種別", "単体テスト"),
    ("正常異常", "正常系"),
    ("When", "ログイン画面で「メールでログイン」を押す"),
    ("Then", "確認を促すメッセージが表示される"),
)
SHIPPING_FEE_CASE_NAME = "注文金額3000円で送料を計算すると、送料は無料になる"
SHIPPING_FEE_PROPERTIES = (
    ("種別", "単体テスト"),
    ("正常異常", "正常系"),
    ("When", "注文金額3000円で送料を計算する"),
    ("Then", "送料は無料になる"),
)
SHIPPING_FEE_PERSPECTIVE_PROPERTIES = (
    ("種別", "単体テスト"),
    ("正常異常", "正常系"),
    ("観点", "境界値"),
    ("観点", "エッジケース"),
    ("When", "注文金額3000円で送料を計算する"),
    ("Then", "送料は無料になる"),
)
CSHARP_ORDER_FEATURE_NAME = ("区分・大機能・中機能・小機能", "[本体:注文]送料計算")
HINT_CASE_NAME = "ログインしているとき、ホーム画面で「探しに行く」を押し、出題画面で「ヒント」を押すと、出題の英文が表示される"
HINT_PROPERTIES = (
    ("種別", "単体テスト"),
    ("正常異常", "正常系"),
    ("Given", "ログインしているとき"),
    ("When", "ホーム画面で「探しに行く」を押す"),
    ("When", "出題画面で「ヒント」を押す"),
    ("Then", "出題の英文が表示される"),
)
HINT_STEPS = [
    {
        "G": "ログインしているとき",
        "W": ["ホーム画面で「探しに行く」を押す", "出題画面で「ヒント」を押す"],
        "T": "出題の英文が表示される",
    }
]
SCENARIO_TEST_NAME = "[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面 > ホーム画面で「探しに行く」を押す"
SCENARIO_CASE_NAME = "ホーム画面で「探しに行く」を押すと、英文が表示される"
SCENARIO_PROPERTIES = (
    ("種別", "シナリオテスト"),
    ("正常異常", "正常系"),
    ("環境", "ローカル"),
    ("環境", "dev環境"),
    ("When", "ホーム画面で「探しに行く」を押す"),
    ("Then:ローカル", "英文「Hello.」が表示される"),
    ("Then:dev環境", "英単語を含む英文が表示される"),
)
CSHARP_SCENARIO_FEATURE_NAME = (
    "区分・大機能・中機能・小機能",
    "[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面",
)
FEATURES_AUTH = build_features_of_region("本体", ["認証"])
FEATURES_ORDER = build_features_of_region("本体", ["注文"])
FEATURES_HINT = build_features_of_region("本体", ["出題"])
FEATURES_SCENARIO = build_features_of_region(
    "シナリオ", ["商品を購入する"], ["通常の動線"]
)


class Test本体__テストケースカタログ__入力__TypeScript_のテスト名からの機能名の読み取り:
    def test_テスト名本体認証ログイン_大なり記号_未確認のアカウントでログインすると_確認を促すメッセージが表示されるから_機能名を読み取ると_機能名は本体認証ログインになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "When",
                    "テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」から、機能名を読み取る",
                ),
                ("Then", "機能名は「[本体:認証]ログイン」になる"),
            ],
        )
        feature_name = catalog.read_typescript_feature_name(
            "[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される"
        )
        assert feature_name == "[本体:認証]ログイン"

    def test_テスト名本体認証ログイン_一重山括弧_未確認のアカウントでログインすると_確認を促すメッセージが表示されるから_機能名を読み取ると_機能名は本体認証ログインになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "When",
                    "テスト名「[本体:認証]ログイン › 未確認のアカウントでログインすると、確認を促すメッセージが表示される」から、機能名を読み取る",
                ),
                ("Then", "機能名は「[本体:認証]ログイン」になる"),
            ],
        )
        feature_name = catalog.read_typescript_feature_name(
            "[本体:認証]ログイン › 未確認のアカウントでログインすると、確認を促すメッセージが表示される"
        )
        assert feature_name == "[本体:認証]ログイン"


class Test本体__テストケースカタログ__入力__機能名の読み取り:
    def test_機能名本体認証ログインから_区分大機能中機能小機能を読み取ると_区分は本体になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["件数・有無"],
            items=[
                (
                    "When",
                    "機能名「[本体:認証]ログイン」から、区分・大機能・中機能・小機能を読み取る",
                ),
                ("Then", "区分は「本体」になる"),
            ],
        )
        parsed = catalog.parse_feature_name("[本体:認証]ログイン")
        assert parsed["region"] == "本体"

    def test_機能名本体認証ログインから_区分大機能中機能小機能を読み取ると_大機能は認証になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["件数・有無"],
            items=[
                (
                    "When",
                    "機能名「[本体:認証]ログイン」から、区分・大機能・中機能・小機能を読み取る",
                ),
                ("Then", "大機能は「認証」になる"),
            ],
        )
        parsed = catalog.parse_feature_name("[本体:認証]ログイン")
        assert parsed["major"] == "認証"

    def test_機能名本体認証ログインから_区分大機能中機能小機能を読み取ると_中機能はなしになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["件数・有無"],
            items=[
                (
                    "When",
                    "機能名「[本体:認証]ログイン」から、区分・大機能・中機能・小機能を読み取る",
                ),
                ("Then", "中機能はなしになる"),
            ],
        )
        parsed = catalog.parse_feature_name("[本体:認証]ログイン")
        assert parsed["minor"] is None

    def test_機能名本体認証ログインから_区分大機能中機能小機能を読み取ると_小機能はログインになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["件数・有無"],
            items=[
                (
                    "When",
                    "機能名「[本体:認証]ログイン」から、区分・大機能・中機能・小機能を読み取る",
                ),
                ("Then", "小機能は「ログイン」になる"),
            ],
        )
        parsed = catalog.parse_feature_name("[本体:認証]ログイン")
        assert parsed["feature"] == "ログイン"

    def test_機能名本体注文画面表示送料の表示から_区分大機能中機能小機能を読み取ると_区分は本体になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["件数・有無"],
            items=[
                (
                    "When",
                    "機能名「[本体:注文:画面表示]送料の表示」から、区分・大機能・中機能・小機能を読み取る",
                ),
                ("Then", "区分は「本体」になる"),
            ],
        )
        parsed = catalog.parse_feature_name("[本体:注文:画面表示]送料の表示")
        assert parsed["region"] == "本体"

    def test_機能名本体注文画面表示送料の表示から_区分大機能中機能小機能を読み取ると_大機能は注文になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["件数・有無"],
            items=[
                (
                    "When",
                    "機能名「[本体:注文:画面表示]送料の表示」から、区分・大機能・中機能・小機能を読み取る",
                ),
                ("Then", "大機能は「注文」になる"),
            ],
        )
        parsed = catalog.parse_feature_name("[本体:注文:画面表示]送料の表示")
        assert parsed["major"] == "注文"

    def test_機能名本体注文画面表示送料の表示から_区分大機能中機能小機能を読み取ると_中機能は画面表示になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["件数・有無"],
            items=[
                (
                    "When",
                    "機能名「[本体:注文:画面表示]送料の表示」から、区分・大機能・中機能・小機能を読み取る",
                ),
                ("Then", "中機能は「画面表示」になる"),
            ],
        )
        parsed = catalog.parse_feature_name("[本体:注文:画面表示]送料の表示")
        assert parsed["minor"] == "画面表示"

    def test_機能名本体注文画面表示送料の表示から_区分大機能中機能小機能を読み取ると_小機能は送料の表示になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["件数・有無"],
            items=[
                (
                    "When",
                    "機能名「[本体:注文:画面表示]送料の表示」から、区分・大機能・中機能・小機能を読み取る",
                ),
                ("Then", "小機能は「送料の表示」になる"),
            ],
        )
        parsed = catalog.parse_feature_name("[本体:注文:画面表示]送料の表示")
        assert parsed["feature"] == "送料の表示"

    def test_機能名本体ログインから_区分大機能中機能小機能を読み取ると_機能名が_区分大機能中機能小機能_の形ではないことを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "When",
                    "機能名「[本体]ログイン」から、区分・大機能・中機能・小機能を読み取る",
                ),
                (
                    "Then",
                    "機能名が `[区分:大機能(:中機能)]小機能` の形ではないことを示すエラーになる",
                ),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.parse_feature_name("[本体]ログイン")
        assert_message_contains(
            error.value, "[区分:大機能(:中機能)]小機能", "形ではない"
        )


class Test本体__テストケースカタログ__入力__ステップの読み取り:
    def test_Givenログインしているとき_Whenホーム画面で探しに行くを押す_When出題画面でヒントを押す_Then出題の英文が表示されるの順に並ぶ項目から_ステップを読み取ると_読み取ったステップは_Givenログインしているとき_Whenホーム画面で探しに行くを押す出題画面でヒントを押す_Then出題の英文が表示されるの_1_つになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "When",
                    "Given「ログインしているとき」、When「ホーム画面で「探しに行く」を押す」、When「出題画面で「ヒント」を押す」、Then「出題の英文が表示される」の順に並ぶ項目から、ステップを読み取る",
                ),
                (
                    "Then",
                    "読み取ったステップは、Given「ログインしているとき」、When「ホーム画面で「探しに行く」を押す」「出題画面で「ヒント」を押す」、Then「出題の英文が表示される」の 1 つになる",
                ),
            ],
        )
        steps = catalog.read_steps(
            [
                ("Given", "ログインしているとき"),
                ("When", "ホーム画面で「探しに行く」を押す"),
                ("When", "出題画面で「ヒント」を押す"),
                ("Then", "出題の英文が表示される"),
            ]
        )
        assert steps == [
            {
                "given": "ログインしているとき",
                "whens": [
                    "ホーム画面で「探しに行く」を押す",
                    "出題画面で「ヒント」を押す",
                ],
                "then": "出題の英文が表示される",
                "environment_thens": [],
            }
        ]

    def test_Whenホーム画面で探しに行くを押す_Then出題の英文が表示されるの順に並ぶ項目から_ステップを読み取ると_読み取ったステップは_Given_なし_Whenホーム画面で探しに行くを押す_Then出題の英文が表示されるの_1_つになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["件数・有無"],
            items=[
                (
                    "When",
                    "When「ホーム画面で「探しに行く」を押す」、Then「出題の英文が表示される」の順に並ぶ項目から、ステップを読み取る",
                ),
                (
                    "Then",
                    "読み取ったステップは、Given なし、When「ホーム画面で「探しに行く」を押す」、Then「出題の英文が表示される」の 1 つになる",
                ),
            ],
        )
        steps = catalog.read_steps(
            [
                ("When", "ホーム画面で「探しに行く」を押す"),
                ("Then", "出題の英文が表示される"),
            ]
        )
        assert steps == [
            {
                "given": None,
                "whens": ["ホーム画面で「探しに行く」を押す"],
                "then": "出題の英文が表示される",
                "environment_thens": [],
            }
        ]

    def test_Givenログインしているとき_Whenホーム画面で探しに行くを押す_Then出題の英文が表示される_When結果画面でもう一度を押す_Then新しい出題の英文が表示されるの順に並ぶ項目から_ステップを読み取ると_読み取ったステップは_1_つ目が_Givenログインしているとき_Whenホーム画面で探しに行くを押す_Then出題の英文が表示される_2_つ目が_Given_なし_When結果画面でもう一度を押す_Then新しい出題の英文が表示されるの_2_つになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "When",
                    "Given「ログインしているとき」、When「ホーム画面で「探しに行く」を押す」、Then「出題の英文が表示される」、When「結果画面で「もう一度」を押す」、Then「新しい出題の英文が表示される」の順に並ぶ項目から、ステップを読み取る",
                ),
                (
                    "Then",
                    "読み取ったステップは、1 つ目が Given「ログインしているとき」、When「ホーム画面で「探しに行く」を押す」、Then「出題の英文が表示される」、2 つ目が Given なし、When「結果画面で「もう一度」を押す」、Then「新しい出題の英文が表示される」の 2 つになる",
                ),
            ],
        )
        steps = catalog.read_steps(
            [
                ("Given", "ログインしているとき"),
                ("When", "ホーム画面で「探しに行く」を押す"),
                ("Then", "出題の英文が表示される"),
                ("When", "結果画面で「もう一度」を押す"),
                ("Then", "新しい出題の英文が表示される"),
            ]
        )
        assert steps == [
            {
                "given": "ログインしているとき",
                "whens": ["ホーム画面で「探しに行く」を押す"],
                "then": "出題の英文が表示される",
                "environment_thens": [],
            },
            {
                "given": None,
                "whens": ["結果画面で「もう一度」を押す"],
                "then": "新しい出題の英文が表示される",
                "environment_thens": [],
            },
        ]

    def test_Givenログインしているとき_Then出題の英文が表示されるの順に並ぶ項目から_ステップを読み取ると_When_の無い_Then_があることを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "When",
                    "Given「ログインしているとき」、Then「出題の英文が表示される」の順に並ぶ項目から、ステップを読み取る",
                ),
                ("Then", "When の無い Then があることを示すエラーになる"),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_steps(
                [("Given", "ログインしているとき"), ("Then", "出題の英文が表示される")]
            )
        assert_message_contains(error.value, "When の無い Then")

    def test_Givenログインしているとき_Whenホーム画面で探しに行くを押すの順に並ぶ項目から_ステップを読み取ると_Then_の無いステップがあることを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "When",
                    "Given「ログインしているとき」、When「ホーム画面で「探しに行く」を押す」の順に並ぶ項目から、ステップを読み取る",
                ),
                ("Then", "Then の無いステップがあることを示すエラーになる"),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_steps(
                [
                    ("Given", "ログインしているとき"),
                    ("When", "ホーム画面で「探しに行く」を押す"),
                ]
            )
        assert_message_contains(error.value, "Then の無いステップ")

    def test_Givenログインしているとき_Givenメールアドレスが未確認のときの順に並ぶ項目から_ステップを読み取ると_Then_の前に_Given_が続いていることを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "When",
                    "Given「ログインしているとき」、Given「メールアドレスが未確認のとき」の順に並ぶ項目から、ステップを読み取る",
                ),
                ("Then", "Then の前に Given が続いていることを示すエラーになる"),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_steps(
                [
                    ("Given", "ログインしているとき"),
                    ("Given", "メールアドレスが未確認のとき"),
                ]
            )
        assert_message_contains(error.value, "Then の前に Given が続いて")

    def test_GivenWhenThen_が_1_つも無い項目から_ステップを読み取ると_GivenWhenThen_が無いことを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            perspectives=["件数・有無"],
            items=[
                ("When", "Given・When・Then が 1 つも無い項目から、ステップを読み取る"),
                ("Then", "Given・When・Then が無いことを示すエラーになる"),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_steps([])
        assert_message_contains(error.value, "Given・When・Then が無い")


class Test本体__テストケースカタログ__入力__設定ファイルの機能の一覧にある機能の読み取り:
    def test_設定ファイルの機能の一覧が_区分本体に大機能注文と中機能画面表示を持つとき_テスト名本体注文画面表示送料の表示__カート画面を開くと_送料が表示されるで_種別単体テスト_正常異常正常系_Whenカート画面を開く_Then送料が表示されるを持つケースを読み取ると_読み取ったケースの中機能は画面表示になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "Given",
                    "設定ファイルの機能の一覧が、区分「本体」に大機能「注文」と中機能「画面表示」を持つとき",
                ),
                (
                    "When",
                    "テスト名「[本体:注文:画面表示]送料の表示 > カート画面を開くと、送料が表示される」で、種別「単体テスト」、正常異常「正常系」、When「カート画面を開く」、Then「送料が表示される」を持つケースを読み取る",
                ),
                ("Then", "読み取ったケースの中機能は「画面表示」になる"),
            ],
        )
        feature_list = build_features_of_region("本体", ["注文"], ["画面表示"])
        case = catalog.read_typescript_case(
            "[本体:注文:画面表示]送料の表示 > カート画面を開くと、送料が表示される",
            (
                ("種別", "単体テスト"),
                ("正常異常", "正常系"),
                ("When", "カート画面を開く"),
                ("Then", "送料が表示される"),
            ),
            feature_list,
        )
        assert case["minor"] == "画面表示"

    def test_設定ファイルの機能の一覧が_区分本体に大機能認証を持つとき_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別単体テスト_正常異常正常系_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示されるを持つケースを読み取ると_読み取ったケースの中機能はなしになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["件数・有無"],
            items=[
                (
                    "Given",
                    "設定ファイルの機能の一覧が、区分「本体」に大機能「認証」を持つとき",
                ),
                (
                    "When",
                    "テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「単体テスト」、正常異常「正常系」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」を持つケースを読み取る",
                ),
                ("Then", "読み取ったケースの中機能はなしになる"),
            ],
        )
        case = catalog.read_typescript_case(
            LOGIN_TEST_NAME, LOGIN_PROPERTIES, FEATURES_AUTH
        )
        assert case["minor"] is None

    def test_設定ファイルの機能の一覧が_区分運用に大機能ログ出力を持つとき_テスト名運用ログ出力構造化ログの出力__ログを出力すると_JSON_形式の_1_行が出力されるで_種別単体テスト_正常異常正常系_Whenログを出力する_ThenJSON_形式の_1_行が出力されるを持つケースを読み取ると_読み取ったケースの区分は運用になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["件数・有無"],
            items=[
                (
                    "Given",
                    "設定ファイルの機能の一覧が、区分「運用」に大機能「ログ出力」を持つとき",
                ),
                (
                    "When",
                    "テスト名「[運用:ログ出力]構造化ログの出力 > ログを出力すると、JSON 形式の 1 行が出力される」で、種別「単体テスト」、正常異常「正常系」、When「ログを出力する」、Then「JSON 形式の 1 行が出力される」を持つケースを読み取る",
                ),
                ("Then", "読み取ったケースの区分は「運用」になる"),
            ],
        )
        case = catalog.read_typescript_case(
            "[運用:ログ出力]構造化ログの出力 > ログを出力すると、JSON 形式の 1 行が出力される",
            (
                ("種別", "単体テスト"),
                ("正常異常", "正常系"),
                ("When", "ログを出力する"),
                ("Then", "JSON 形式の 1 行が出力される"),
            ),
            build_features_of_region("運用", ["ログ出力"]),
        )
        assert case["region"] == "運用"


class Test本体__テストケースカタログ__入力__設定ファイルの機能の一覧にない機能の拒否:
    def test_設定ファイルの機能の一覧が_区分本体に大機能認証を持つとき_テスト名営業認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別単体テスト_正常異常正常系_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示されるを持つケースを読み取ると_区分営業が_本体共通運用外部連携シナリオのいずれでもないことを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "Given",
                    "設定ファイルの機能の一覧が、区分「本体」に大機能「認証」を持つとき",
                ),
                (
                    "When",
                    "テスト名「[営業:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「単体テスト」、正常異常「正常系」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」を持つケースを読み取る",
                ),
                (
                    "Then",
                    "区分「営業」が、本体・共通・運用・外部連携・シナリオのいずれでもないことを示すエラーになる",
                ),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_typescript_case(
                "[営業:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される",
                LOGIN_PROPERTIES,
                FEATURES_AUTH,
            )
        assert_message_contains(
            error.value,
            "区分「営業」",
            "本体・共通・運用・外部連携・シナリオ",
            "いずれでもない",
        )

    def test_設定ファイルの機能の一覧が_区分本体に大機能認証を持つとき_テスト名本体在庫在庫の表示__在庫画面を開くと_在庫数が表示されるで_種別単体テスト_正常異常正常系_When在庫画面を開く_Then在庫数が表示されるを持つケースを読み取ると_設定ファイルの機能の一覧の区分本体に_大機能在庫がないことを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "Given",
                    "設定ファイルの機能の一覧が、区分「本体」に大機能「認証」を持つとき",
                ),
                (
                    "When",
                    "テスト名「[本体:在庫]在庫の表示 > 在庫画面を開くと、在庫数が表示される」で、種別「単体テスト」、正常異常「正常系」、When「在庫画面を開く」、Then「在庫数が表示される」を持つケースを読み取る",
                ),
                (
                    "Then",
                    "設定ファイルの機能の一覧の区分「本体」に、大機能「在庫」がないことを示すエラーになる",
                ),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_typescript_case(
                "[本体:在庫]在庫の表示 > 在庫画面を開くと、在庫数が表示される",
                (
                    ("種別", "単体テスト"),
                    ("正常異常", "正常系"),
                    ("When", "在庫画面を開く"),
                    ("Then", "在庫数が表示される"),
                ),
                FEATURES_AUTH,
            )
        assert_message_contains(error.value, "区分「本体」", "大機能「在庫」", "がない")

    def test_設定ファイルの機能の一覧が_区分本体に大機能認証を持ち_中機能を持たないとき_テスト名本体認証検索ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別単体テスト_正常異常正常系_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示されるを持つケースを読み取ると_設定ファイルの機能の一覧の区分本体に_中機能検索がないことを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "Given",
                    "設定ファイルの機能の一覧が、区分「本体」に大機能「認証」を持ち、中機能を持たないとき",
                ),
                (
                    "When",
                    "テスト名「[本体:認証:検索]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「単体テスト」、正常異常「正常系」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」を持つケースを読み取る",
                ),
                (
                    "Then",
                    "設定ファイルの機能の一覧の区分「本体」に、中機能「検索」がないことを示すエラーになる",
                ),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_typescript_case(
                "[本体:認証:検索]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される",
                LOGIN_PROPERTIES,
                FEATURES_AUTH,
            )
        assert_message_contains(error.value, "区分「本体」", "中機能「検索」", "がない")

    def test_設定ファイルの機能の一覧が_区分運用に大機能ログ出力を持つとき_テスト名運用ログ出力画面表示構造化ログの出力__ログを出力すると_JSON_形式の_1_行が出力されるで_種別単体テスト_正常異常正常系_Whenログを出力する_ThenJSON_形式の_1_行が出力されるを持つケースを読み取ると_区分運用には中機能を付けられないことを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "Given",
                    "設定ファイルの機能の一覧が、区分「運用」に大機能「ログ出力」を持つとき",
                ),
                (
                    "When",
                    "テスト名「[運用:ログ出力:画面表示]構造化ログの出力 > ログを出力すると、JSON 形式の 1 行が出力される」で、種別「単体テスト」、正常異常「正常系」、When「ログを出力する」、Then「JSON 形式の 1 行が出力される」を持つケースを読み取る",
                ),
                ("Then", "区分「運用」には中機能を付けられないことを示すエラーになる"),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_typescript_case(
                "[運用:ログ出力:画面表示]構造化ログの出力 > ログを出力すると、JSON 形式の 1 行が出力される",
                (
                    ("種別", "単体テスト"),
                    ("正常異常", "正常系"),
                    ("When", "ログを出力する"),
                    ("Then", "JSON 形式の 1 行が出力される"),
                ),
                build_features_of_region("運用", ["ログ出力"]),
            )
        assert_message_contains(error.value, "区分「運用」", "中機能を付けられない")


class Test本体__テストケースカタログ__入力__ケースの読み取り:
    def test_機能の一覧が_区分本体に大機能認証を持つとき_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別部品間結合テスト_正常異常異常系_Givenメールアドレスが未確認のアカウントのとき_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示されるを持つケースを読み取ると_読み取ったケースの種別は部品間結合テストになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「認証」を持つとき"),
                (
                    "When",
                    "テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「部品間結合テスト」、正常異常「異常系」、Given「メールアドレスが未確認のアカウントのとき」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」を持つケースを読み取る",
                ),
                ("Then", "読み取ったケースの種別は「部品間結合テスト」になる"),
            ],
        )
        case = catalog.read_typescript_case(
            LOGIN_TEST_NAME,
            (
                ("種別", "部品間結合テスト"),
                ("正常異常", "異常系"),
                ("Given", "メールアドレスが未確認のアカウントのとき"),
                ("When", "ログイン画面で「メールでログイン」を押す"),
                ("Then", "確認を促すメッセージが表示される"),
            ),
            FEATURES_AUTH,
        )
        assert case["kind"] == "部品間結合テスト"

    def test_機能の一覧が_区分本体に大機能認証を持つとき_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別部品間結合テスト_正常異常異常系_Givenメールアドレスが未確認のアカウントのとき_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示されるを持つケースを読み取ると_読み取ったケースの正常異常は異常系になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「認証」を持つとき"),
                (
                    "When",
                    "テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「部品間結合テスト」、正常異常「異常系」、Given「メールアドレスが未確認のアカウントのとき」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」を持つケースを読み取る",
                ),
                ("Then", "読み取ったケースの正常異常は「異常系」になる"),
            ],
        )
        case = catalog.read_typescript_case(
            LOGIN_TEST_NAME,
            (
                ("種別", "部品間結合テスト"),
                ("正常異常", "異常系"),
                ("Given", "メールアドレスが未確認のアカウントのとき"),
                ("When", "ログイン画面で「メールでログイン」を押す"),
                ("Then", "確認を促すメッセージが表示される"),
            ),
            FEATURES_AUTH,
        )
        assert case["normal_or_abnormal"] == "異常系"

    def test_機能の一覧が_区分本体に大機能認証を持つとき_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別部品間結合テスト_正常異常異常系_Givenメールアドレスが未確認のアカウントのとき_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示されるを持つケースを読み取ると_読み取ったケースのステップは_Givenメールアドレスが未確認のアカウントのとき_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示されるの_1_つになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「認証」を持つとき"),
                (
                    "When",
                    "テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「部品間結合テスト」、正常異常「異常系」、Given「メールアドレスが未確認のアカウントのとき」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」を持つケースを読み取る",
                ),
                (
                    "Then",
                    "読み取ったケースのステップは、Given「メールアドレスが未確認のアカウントのとき」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」の 1 つになる",
                ),
            ],
        )
        case = catalog.read_typescript_case(
            LOGIN_TEST_NAME,
            (
                ("種別", "部品間結合テスト"),
                ("正常異常", "異常系"),
                ("Given", "メールアドレスが未確認のアカウントのとき"),
                ("When", "ログイン画面で「メールでログイン」を押す"),
                ("Then", "確認を促すメッセージが表示される"),
            ),
            FEATURES_AUTH,
        )
        assert case["steps"] == [
            {
                "given": "メールアドレスが未確認のアカウントのとき",
                "whens": ["ログイン画面で「メールでログイン」を押す"],
                "then": "確認を促すメッセージが表示される",
                "environment_thens": [],
            }
        ]

    def test_機能の一覧が_区分本体に大機能認証を持つとき_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_正常異常正常系_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示されるを持ち_種別を持たないケースを読み取ると_種別が付いていないため_種別のいずれでもないことを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            perspectives=["件数・有無"],
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「認証」を持つとき"),
                (
                    "When",
                    "テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、正常異常「正常系」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」を持ち、種別を持たないケースを読み取る",
                ),
                (
                    "Then",
                    "種別が付いていないため、種別のいずれでもないことを示すエラーになる",
                ),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_typescript_case(
                LOGIN_TEST_NAME,
                (
                    ("正常異常", "正常系"),
                    ("When", "ログイン画面で「メールでログイン」を押す"),
                    ("Then", "確認を促すメッセージが表示される"),
                ),
                FEATURES_AUTH,
            )
        assert_message_contains(
            error.value, "種別が付いていない", "種別のいずれでもない"
        )

    def test_機能の一覧が_区分本体に大機能認証を持つとき_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別単体テスト_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示されるを持ち_正常異常を持たないケースを読み取ると_正常異常が付いていないため_正常系異常系のいずれでもないことを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            perspectives=["件数・有無"],
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「認証」を持つとき"),
                (
                    "When",
                    "テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「単体テスト」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」を持ち、正常異常を持たないケースを読み取る",
                ),
                (
                    "Then",
                    "正常異常が付いていないため、正常系・異常系のいずれでもないことを示すエラーになる",
                ),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_typescript_case(
                LOGIN_TEST_NAME,
                (
                    ("種別", "単体テスト"),
                    ("When", "ログイン画面で「メールでログイン」を押す"),
                    ("Then", "確認を促すメッセージが表示される"),
                ),
                FEATURES_AUTH,
            )
        assert_message_contains(
            error.value, "正常異常が付いていない", "正常系・異常系のいずれでもない"
        )

    def test_機能の一覧が_区分本体に大機能認証を持つとき_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別負荷テスト_正常異常正常系_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示されるを持つケースを読み取ると_種別負荷テストが種別のいずれでもないことを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「認証」を持つとき"),
                (
                    "When",
                    "テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「負荷テスト」、正常異常「正常系」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」を持つケースを読み取る",
                ),
                (
                    "Then",
                    "種別「負荷テスト」が種別のいずれでもないことを示すエラーになる",
                ),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_typescript_case(
                LOGIN_TEST_NAME,
                (
                    ("種別", "負荷テスト"),
                    ("正常異常", "正常系"),
                    ("When", "ログイン画面で「メールでログイン」を押す"),
                    ("Then", "確認を促すメッセージが表示される"),
                ),
                FEATURES_AUTH,
            )
        assert_message_contains(error.value, "種別「負荷テスト」", "いずれでもない")


class Test本体__テストケースカタログ__入力__観点の読み取り:
    def test_機能の一覧が_区分本体に大機能認証を持つとき_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_観点を持たない_種別単体テスト_正常異常正常系_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示されるのケースを読み取ると_読み取ったケースの観点は_0_個になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["件数・有無"],
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「認証」を持つとき"),
                (
                    "When",
                    "テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、観点を持たない、種別「単体テスト」、正常異常「正常系」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」のケースを読み取る",
                ),
                ("Then", "読み取ったケースの観点は 0 個になる"),
            ],
        )
        case = catalog.read_typescript_case(
            LOGIN_TEST_NAME, LOGIN_PROPERTIES, FEATURES_AUTH
        )
        assert case["perspectives"] == []

    def test_機能の一覧が_区分本体に大機能認証を持つとき_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別単体テスト_正常異常正常系_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示される_観点境界値を持つケースを読み取ると_読み取ったケースの観点は境界値の_1_つになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["件数・有無"],
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「認証」を持つとき"),
                (
                    "When",
                    "テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「単体テスト」、正常異常「正常系」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」、観点「境界値」を持つケースを読み取る",
                ),
                ("Then", "読み取ったケースの観点は「境界値」の 1 つになる"),
            ],
        )
        case = catalog.read_typescript_case(
            LOGIN_TEST_NAME,
            (
                ("種別", "単体テスト"),
                ("正常異常", "正常系"),
                ("観点", "境界値"),
                ("When", "ログイン画面で「メールでログイン」を押す"),
                ("Then", "確認を促すメッセージが表示される"),
            ),
            FEATURES_AUTH,
        )
        assert case["perspectives"] == ["境界値"]

    def test_機能の一覧が_区分本体に大機能認証を持つとき_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別単体テスト_正常異常正常系_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示される_観点境界値とエッジケースを持つケースを読み取ると_読み取ったケースの観点は境界値とエッジケースの_2_つになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["件数・有無"],
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「認証」を持つとき"),
                (
                    "When",
                    "テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「単体テスト」、正常異常「正常系」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」、観点「境界値」と「エッジケース」を持つケースを読み取る",
                ),
                (
                    "Then",
                    "読み取ったケースの観点は「境界値」と「エッジケース」の 2 つになる",
                ),
            ],
        )
        case = catalog.read_typescript_case(
            LOGIN_TEST_NAME,
            (
                ("種別", "単体テスト"),
                ("正常異常", "正常系"),
                ("観点", "境界値"),
                ("観点", "エッジケース"),
                ("When", "ログイン画面で「メールでログイン」を押す"),
                ("Then", "確認を促すメッセージが表示される"),
            ),
            FEATURES_AUTH,
        )
        assert case["perspectives"] == ["境界値", "エッジケース"]

    def test_機能の一覧が_区分本体に大機能認証を持つとき_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別単体テスト_正常異常正常系_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示される_観点網羅を持つケースを読み取ると_観点網羅が観点のいずれでもないことを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「認証」を持つとき"),
                (
                    "When",
                    "テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「単体テスト」、正常異常「正常系」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」、観点「網羅」を持つケースを読み取る",
                ),
                ("Then", "観点「網羅」が観点のいずれでもないことを示すエラーになる"),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_typescript_case(
                LOGIN_TEST_NAME,
                (
                    ("種別", "単体テスト"),
                    ("正常異常", "正常系"),
                    ("観点", "網羅"),
                    ("When", "ログイン画面で「メールでログイン」を押す"),
                    ("Then", "確認を促すメッセージが表示される"),
                ),
                FEATURES_AUTH,
            )
        assert_message_contains(error.value, "観点「網羅」", "いずれでもない")

    def test_機能の一覧が_区分本体に大機能認証を持つとき_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別単体テスト_正常異常正常系_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示される_観点境界値を_2_つ持つケースを読み取ると_観点が重複していることを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「認証」を持つとき"),
                (
                    "When",
                    "テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「単体テスト」、正常異常「正常系」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」、観点「境界値」を 2 つ持つケースを読み取る",
                ),
                ("Then", "観点が重複していることを示すエラーになる"),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_typescript_case(
                LOGIN_TEST_NAME,
                (
                    ("種別", "単体テスト"),
                    ("正常異常", "正常系"),
                    ("観点", "境界値"),
                    ("観点", "境界値"),
                    ("When", "ログイン画面で「メールでログイン」を押す"),
                    ("Then", "確認を促すメッセージが表示される"),
                ),
                FEATURES_AUTH,
            )
        assert_message_contains(error.value, "観点が重複している")

    def test_機能の一覧が_区分本体に大機能認証を持つとき_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別単体テスト_正常異常正常系_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示される_観点境界値と同値分割を持つケースを読み取ると_境界値と同値分割は同時に付けられないことを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「認証」を持つとき"),
                (
                    "When",
                    "テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「単体テスト」、正常異常「正常系」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」、観点「境界値」と「同値分割」を持つケースを読み取る",
                ),
                ("Then", "境界値と同値分割は同時に付けられないことを示すエラーになる"),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_typescript_case(
                LOGIN_TEST_NAME,
                (
                    ("種別", "単体テスト"),
                    ("正常異常", "正常系"),
                    ("観点", "境界値"),
                    ("観点", "同値分割"),
                    ("When", "ログイン画面で「メールでログイン」を押す"),
                    ("Then", "確認を促すメッセージが表示される"),
                ),
                FEATURES_AUTH,
            )
        assert_message_contains(error.value, "境界値と同値分割は同時に付けられない")


class Test本体__テストケースカタログ__業務ルール__並び順:
    def test_機能の一覧が_区分本体の大機能を認証注文の順に持つとき_区分本体の大機能注文のケースと_区分本体の大機能認証のケースを_この順に並べ替えると_ケースの並びは_大機能認証のケース_大機能注文のケースの順になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」の大機能を「認証」「注文」の順に持つとき",
                ),
                (
                    "When",
                    "区分「本体」の大機能「注文」のケースと、区分「本体」の大機能「認証」のケースを、この順に並べ替える",
                ),
                (
                    "Then",
                    "ケースの並びは、大機能「認証」のケース、大機能「注文」のケースの順になる",
                ),
            ],
        )
        feature_list = build_features_of_region("本体", ["認証", "注文"])
        cases = [
            build_case("本体", "注文", None, "送料計算"),
            build_case("本体", "認証", None, "ログイン"),
        ]
        sorted_cases = catalog.sort_cases(cases, feature_list)
        assert [case["major"] for case in sorted_cases] == ["認証", "注文"]

    def test_機能の一覧が_区分運用に大機能ログ出力を_区分本体に大機能認証を_この順に持つとき_区分運用の大機能ログ出力のケースと_区分本体の大機能認証のケースを_この順に並べ替えると_ケースの並びは_区分の順_本体_共通_運用_外部連携_シナリオ_に従い_区分本体のケース_区分運用のケースの順になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「運用」に大機能「ログ出力」を、区分「本体」に大機能「認証」を、この順に持つとき",
                ),
                (
                    "When",
                    "区分「運用」の大機能「ログ出力」のケースと、区分「本体」の大機能「認証」のケースを、この順に並べ替える",
                ),
                (
                    "Then",
                    "ケースの並びは、区分の順 (本体、共通、運用、外部連携、シナリオ) に従い、区分「本体」のケース、区分「運用」のケースの順になる",
                ),
            ],
        )
        feature_list = build_features(
            {
                "運用": {"大機能": ["ログ出力"], "中機能": []},
                "本体": {"大機能": ["認証"], "中機能": []},
            }
        )
        cases = [
            build_case("運用", "ログ出力", None, "構造化ログの出力"),
            build_case("本体", "認証", None, "ログイン"),
        ]
        sorted_cases = catalog.sort_cases(cases, feature_list)
        assert [case["region"] for case in sorted_cases] == ["本体", "運用"]

    def test_機能の一覧が_区分本体に大機能認証と中機能画面表示を持つとき_区分本体の大機能認証で中機能を持たないケースと_中機能画面表示を持つケースを_この順に並べ替えると_中機能画面表示を持つケースが先_中機能を持たないケースが後になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["件数・有無"],
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「認証」と中機能「画面表示」を持つとき",
                ),
                (
                    "When",
                    "区分「本体」の大機能「認証」で中機能を持たないケースと、中機能「画面表示」を持つケースを、この順に並べ替える",
                ),
                (
                    "Then",
                    "中機能「画面表示」を持つケースが先、中機能を持たないケースが後になる",
                ),
            ],
        )
        feature_list = build_features_of_region("本体", ["認証"], ["画面表示"])
        cases = [
            build_case("本体", "認証", None, "ログイン"),
            build_case("本体", "認証", "画面表示", "ログイン画面の表示"),
        ]
        sorted_cases = catalog.sort_cases(cases, feature_list)
        assert [case["minor"] for case in sorted_cases] == ["画面表示", None]

    def test_機能の一覧が_区分本体に大機能認証を持つとき_区分本体の大機能認証の小機能ログインのケースと_同じく大機能認証の小機能パスワード再設定のケースを_この順に並べ替えると_ケースの並びは_小機能ログインのケース_小機能パスワード再設定のケースの順のままになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「認証」を持つとき"),
                (
                    "When",
                    "区分「本体」の大機能「認証」の小機能「ログイン」のケースと、同じく大機能「認証」の小機能「パスワード再設定」のケースを、この順に並べ替える",
                ),
                (
                    "Then",
                    "ケースの並びは、小機能「ログイン」のケース、小機能「パスワード再設定」のケースの順のままになる",
                ),
            ],
        )
        cases = [
            build_case("本体", "認証", None, "ログイン"),
            build_case("本体", "認証", None, "パスワード再設定"),
        ]
        sorted_cases = catalog.sort_cases(cases, FEATURES_AUTH)
        assert [case["feature"] for case in sorted_cases] == [
            "ログイン",
            "パスワード再設定",
        ]


class Test本体__テストケースカタログ__画面表示__HTML_形式の出力:
    def test_機能の一覧が_区分本体に大機能認証を持ち_設定ファイルの言語TypeScriptのテスト結果に_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別単体テスト_正常異常正常系_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースのステップは_Given_なし_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示されるの_1_つになる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「認証」を持ち、設定ファイルの言語「TypeScript」のテスト結果に、テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「単体テスト」、正常異常「正常系」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」を持つケースがあるとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "カタログに載るそのケースのステップは、Given なし、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」の 1 つになる",
                ),
            ],
        )
        entry = write_typescript_result(tmp_path, [(LOGIN_TEST_NAME, LOGIN_PROPERTIES)])
        config = build_config(tmp_path, [entry], FEATURES_AUTH)
        page = generate_catalog_page(tmp_path, config)
        assert page.catalog["cases"][0]["steps"] == [
            {
                "G": "",
                "W": ["ログイン画面で「メールでログイン」を押す"],
                "T": "確認を促すメッセージが表示される",
            }
        ]

    def test_機能の一覧が_区分本体に大機能認証を持ち_設定ファイルの言語TypeScriptのテスト結果に_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別単体テスト_正常異常正常系_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示されるを持つケースが_1_つあり_設定ファイルのコミットがabc123のとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るコミットはabc123になる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「認証」を持ち、設定ファイルの言語「TypeScript」のテスト結果に、テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「単体テスト」、正常異常「正常系」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」を持つケースが 1 つあり、設定ファイルのコミットが「abc123」のとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                ("Then", "カタログに載るコミットは「abc123」になる"),
            ],
        )
        entry = write_typescript_result(tmp_path, [(LOGIN_TEST_NAME, LOGIN_PROPERTIES)])
        config = build_config(tmp_path, [entry], FEATURES_AUTH)
        config["commit"] = "abc123"
        page = generate_catalog_page(tmp_path, config)
        assert page.catalog["commit"] == "abc123"

    def test_機能の一覧が_区分本体に大機能認証を持ち_設定ファイルの言語TypeScriptのテスト結果に_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別単体テスト_正常異常正常系_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示されるを持つケースが_1_つあり_設定ファイルにコミットが無いとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るコミットは空になる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            perspectives=["件数・有無"],
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「認証」を持ち、設定ファイルの言語「TypeScript」のテスト結果に、テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「単体テスト」、正常異常「正常系」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」を持つケースが 1 つあり、設定ファイルにコミットが無いとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                ("Then", "カタログに載るコミットは空になる"),
            ],
        )
        entry = write_typescript_result(tmp_path, [(LOGIN_TEST_NAME, LOGIN_PROPERTIES)])
        config = build_config(tmp_path, [entry], FEATURES_AUTH)
        page = generate_catalog_page(tmp_path, config)
        assert page.catalog["commit"] == ""

    def test_機能の一覧が_区分本体に大機能認証を持ち_設定ファイルの言語TypeScriptのテスト結果に_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別単体テスト_正常異常正常系_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示されるを持つケースが_1_つあり_設定ファイルのタイトルがpokelingual_テストケースカタログのとき_設定ファイルを渡して生成コマンドを実行すると_HTML_を解析して取り出した_title_要素の内容はpokelingual_テストケースカタログになる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「認証」を持ち、設定ファイルの言語「TypeScript」のテスト結果に、テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「単体テスト」、正常異常「正常系」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」を持つケースが 1 つあり、設定ファイルのタイトルが「pokelingual テストケースカタログ」のとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "HTML を解析して取り出した title 要素の内容は「pokelingual テストケースカタログ」になる",
                ),
            ],
        )
        entry = write_typescript_result(tmp_path, [(LOGIN_TEST_NAME, LOGIN_PROPERTIES)])
        config = build_config(
            tmp_path, [entry], FEATURES_AUTH, title="pokelingual テストケースカタログ"
        )
        page = generate_catalog_page(tmp_path, config)
        assert page.title == "pokelingual テストケースカタログ"

    def test_機能の一覧が_区分本体に大機能認証を持ち_設定ファイルの言語TypeScriptのテスト結果に_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別単体テスト_正常異常正常系_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示されるを持つケースが_1_つあり_設定ファイルの_css_が指す_CSS_ファイルの内容がcssfromtailwindcolorredのとき_設定ファイルを渡して生成コマンドを実行すると_HTML_を解析して取り出した_style_要素の内容はcssfromtailwindcolorredになる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「認証」を持ち、設定ファイルの言語「TypeScript」のテスト結果に、テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「単体テスト」、正常異常「正常系」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」を持つケースが 1 つあり、設定ファイルの css が指す CSS ファイルの内容が「.css-from-tailwind{color:red}」のとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "HTML を解析して取り出した style 要素の内容は「.css-from-tailwind{color:red}」になる",
                ),
            ],
        )
        entry = write_typescript_result(tmp_path, [(LOGIN_TEST_NAME, LOGIN_PROPERTIES)])
        config = build_config(
            tmp_path, [entry], FEATURES_AUTH, css=".css-from-tailwind{color:red}"
        )
        page = generate_catalog_page(tmp_path, config)
        assert page.style == ".css-from-tailwind{color:red}"

    def test_機能の一覧が_区分本体に大機能認証を持ち_設定ファイルの言語TypeScriptのテスト結果に_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別単体テスト_正常異常正常系_Whenscriptを押す_Then確認を促すメッセージが表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの_When_はscriptを押すになる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            perspectives=["エッジケース"],
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「認証」を持ち、設定ファイルの言語「TypeScript」のテスト結果に、テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「単体テスト」、正常異常「正常系」、When「</script>を押す」、Then「確認を促すメッセージが表示される」を持つケースがあるとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                ("Then", "カタログに載るそのケースの When は「</script>を押す」になる"),
            ],
        )
        entry = write_typescript_result(
            tmp_path,
            [
                (
                    LOGIN_TEST_NAME,
                    (
                        ("種別", "単体テスト"),
                        ("正常異常", "正常系"),
                        ("When", "</script>を押す"),
                        ("Then", "確認を促すメッセージが表示される"),
                    ),
                )
            ],
        )
        config = build_config(tmp_path, [entry], FEATURES_AUTH)
        page = generate_catalog_page(tmp_path, config)
        assert page.catalog["cases"][0]["steps"][0]["W"] == ["</script>を押す"]

    def test_機能の一覧が_区分本体に大機能認証を持ち_設定ファイルの言語TypeScriptのテスト結果に_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別単体テスト_正常異常正常系_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示される_観点境界値を持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの観点は境界値だけになる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「認証」を持ち、設定ファイルの言語「TypeScript」のテスト結果に、テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「単体テスト」、正常異常「正常系」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」、観点「境界値」を持つケースがあるとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                ("Then", "カタログに載るそのケースの観点は「境界値」だけになる"),
            ],
        )
        entry = write_typescript_result(
            tmp_path,
            [
                (
                    LOGIN_TEST_NAME,
                    (
                        ("種別", "単体テスト"),
                        ("正常異常", "正常系"),
                        ("観点", "境界値"),
                        ("When", "ログイン画面で「メールでログイン」を押す"),
                        ("Then", "確認を促すメッセージが表示される"),
                    ),
                )
            ],
        )
        config = build_config(tmp_path, [entry], FEATURES_AUTH)
        page = generate_catalog_page(tmp_path, config)
        assert page.catalog["cases"][0]["g"] == ["境界値"]


class Test本体__テストケースカタログ__入力__必須のキーがない設定ファイルの拒否:
    def test_設定ファイルにtitleが無いとき_設定ファイルを渡して生成コマンドを実行すると_設定ファイルに必須のキーtitleがないことを示すエラーで止まる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="異常系",
            items=[
                ("Given", "設定ファイルに「title」が無いとき"),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "設定ファイルに必須のキー「title」がないことを示すエラーで止まる",
                ),
            ],
        )
        entry = write_typescript_result(tmp_path, [(LOGIN_TEST_NAME, LOGIN_PROPERTIES)])
        config = build_config(tmp_path, [entry], FEATURES_AUTH)
        del config["title"]
        result = run_catalog_generation(tmp_path, config)
        assert_stopped_with_message(result, "必須のキー「title」がない")

    def test_設定ファイルにcssが無いとき_設定ファイルを渡して生成コマンドを実行すると_設定ファイルに必須のキーcssがないことを示すエラーで止まる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="異常系",
            items=[
                ("Given", "設定ファイルに「css」が無いとき"),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "設定ファイルに必須のキー「css」がないことを示すエラーで止まる",
                ),
            ],
        )
        entry = write_typescript_result(tmp_path, [(LOGIN_TEST_NAME, LOGIN_PROPERTIES)])
        config = build_config(tmp_path, [entry], FEATURES_AUTH)
        del config["css"]
        result = run_catalog_generation(tmp_path, config)
        assert_stopped_with_message(result, "必須のキー「css」がない")

    def test_設定ファイルにresultsが無いとき_設定ファイルを渡して生成コマンドを実行すると_設定ファイルに必須のキーresultsがないことを示すエラーで止まる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="異常系",
            items=[
                ("Given", "設定ファイルに「results」が無いとき"),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "設定ファイルに必須のキー「results」がないことを示すエラーで止まる",
                ),
            ],
        )
        entry = write_typescript_result(tmp_path, [(LOGIN_TEST_NAME, LOGIN_PROPERTIES)])
        config = build_config(tmp_path, [entry], FEATURES_AUTH)
        del config["results"]
        result = run_catalog_generation(tmp_path, config)
        assert_stopped_with_message(result, "必須のキー「results」がない")

    def test_設定ファイルにfeaturesが無いとき_設定ファイルを渡して生成コマンドを実行すると_設定ファイルに必須のキーfeaturesがないことを示すエラーで止まる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="異常系",
            items=[
                ("Given", "設定ファイルに「features」が無いとき"),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "設定ファイルに必須のキー「features」がないことを示すエラーで止まる",
                ),
            ],
        )
        entry = write_typescript_result(tmp_path, [(LOGIN_TEST_NAME, LOGIN_PROPERTIES)])
        config = build_config(tmp_path, [entry], FEATURES_AUTH)
        del config["features"]
        result = run_catalog_generation(tmp_path, config)
        assert_stopped_with_message(result, "必須のキー「features」がない")


class Test本体__テストケースカタログ__入力__テスト結果の指定が不正な設定ファイルの拒否:
    def test_設定ファイルのresultsに_パスと言語Rubyを持つ要素があるとき_設定ファイルを渡して生成コマンドを実行すると_言語Rubyが_TypeScriptPythonCKotlinGoDart_のいずれでもないことを示すエラーで止まる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "Given",
                    "設定ファイルの「results」に、パスと言語「Ruby」を持つ要素があるとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "言語「Ruby」が TypeScript・Python・C#・Kotlin・Go・Dart のいずれでもないことを示すエラーで止まる",
                ),
            ],
        )
        entry = {
            **write_typescript_result(tmp_path, [(LOGIN_TEST_NAME, LOGIN_PROPERTIES)]),
            "language": "Ruby",
        }
        config = build_config(tmp_path, [entry], FEATURES_AUTH)
        result = run_catalog_generation(tmp_path, config)
        assert_stopped_with_message(
            result,
            "言語「Ruby」",
            "TypeScript・Python・C#・Kotlin・Go・Dart のいずれでもない",
        )

    def test_設定ファイルのresultsに_パスだけを持ち言語を持たない要素があるとき_設定ファイルを渡して生成コマンドを実行すると_resultsの要素にlanguageがないことを示すエラーで止まる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "Given",
                    "設定ファイルの「results」に、パスだけを持ち言語を持たない要素があるとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "「results」の要素に「language」がないことを示すエラーで止まる",
                ),
            ],
        )
        entry = write_typescript_result(tmp_path, [(LOGIN_TEST_NAME, LOGIN_PROPERTIES)])
        del entry["language"]
        config = build_config(tmp_path, [entry], FEATURES_AUTH)
        result = run_catalog_generation(tmp_path, config)
        assert_stopped_with_message(result, "「results」の要素に「language」がない")

    def test_設定ファイルのresultsに_言語だけを持ちパスを持たない要素があるとき_設定ファイルを渡して生成コマンドを実行すると_resultsの要素にpathがないことを示すエラーで止まる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "Given",
                    "設定ファイルの「results」に、言語だけを持ちパスを持たない要素があるとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                ("Then", "「results」の要素に「path」がないことを示すエラーで止まる"),
            ],
        )
        entry = write_typescript_result(tmp_path, [(LOGIN_TEST_NAME, LOGIN_PROPERTIES)])
        del entry["path"]
        config = build_config(tmp_path, [entry], FEATURES_AUTH)
        result = run_catalog_generation(tmp_path, config)
        assert_stopped_with_message(result, "「results」の要素に「path」がない")


class Test本体__テストケースカタログ__入力__テスト結果の読み込み:
    def test_設定ファイルに言語TypeScriptのテスト結果のパスが_2_つあり_1_つ目にテスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別単体テスト_正常異常正常系_Whenログイン画面でメールでログインを押す_Then確認を促すメッセージが表示されるを持つケースが_2_つ目にテスト名本体注文送料計算__注文金額3000円で送料を計算すると_送料は無料になるで_種別単体テスト_正常異常正常系_When注文金額3000円で送料を計算する_Then送料は無料になるを持つケースがあり_機能の一覧が区分本体に大機能認証注文を持つとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るケースは_小機能ログインのケースと小機能送料計算のケースの_2_つになる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "Given",
                    "設定ファイルに言語「TypeScript」のテスト結果のパスが 2 つあり、1 つ目にテスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「単体テスト」、正常異常「正常系」、When「ログイン画面で「メールでログイン」を押す」、Then「確認を促すメッセージが表示される」を持つケースが、2 つ目にテスト名「[本体:注文]送料計算 > 注文金額3000円で送料を計算すると、送料は無料になる」で、種別「単体テスト」、正常異常「正常系」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持つケースがあり、機能の一覧が区分「本体」に大機能「認証」「注文」を持つとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "カタログに載るケースは、小機能「ログイン」のケースと小機能「送料計算」のケースの 2 つになる",
                ),
            ],
        )
        login_entry = write_typescript_result(
            tmp_path, [(LOGIN_TEST_NAME, LOGIN_PROPERTIES)], "login.xml"
        )
        shipping_fee_entry = write_typescript_result(
            tmp_path,
            [
                (
                    "[本体:注文]送料計算 > 注文金額3000円で送料を計算すると、送料は無料になる",
                    SHIPPING_FEE_PROPERTIES,
                )
            ],
            "shipping_fee.xml",
        )
        config = build_config(
            tmp_path,
            [login_entry, shipping_fee_entry],
            build_features_of_region("本体", ["認証", "注文"]),
        )
        page = generate_catalog_page(tmp_path, config)
        assert [case["s"] for case in page.catalog["cases"]] == ["ログイン", "送料計算"]


class Test本体__テストケースカタログ__入力__name_属性のない_testcase_を含むテスト結果の拒否:
    def test_設定ファイルの言語TypeScriptのテスト結果に_name_属性の無い_testcase_があるとき_設定ファイルを渡して生成コマンドを実行すると_testcase_に_name_属性がないことを示すエラーで止まる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "Given",
                    "設定ファイルの言語「TypeScript」のテスト結果に、name 属性の無い testcase があるとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                ("Then", "testcase に name 属性がないことを示すエラーで止まる"),
            ],
        )
        path = write_result_file(
            tmp_path,
            "typescript.xml",
            '<testsuites><testsuite name="suite"><testcase classname="suite"/></testsuite></testsuites>',
        )
        config = build_config(
            tmp_path, [build_result_entry("TypeScript", path)], FEATURES_AUTH
        )
        result = run_catalog_generation(tmp_path, config)
        assert_stopped_with_message(result, "testcase に name 属性がない")


class Test本体__テストケースカタログ__操作__生成コマンドの再実行:
    def test_機能の一覧が_区分本体に大機能認証だけを持ち_設定ファイルの言語TypeScriptのテスト結果に_大機能在庫のテスト名本体在庫ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるのケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_大機能在庫が区分本体の一覧にないことを示すメッセージで終了する_設定ファイルの言語TypeScriptのテスト結果のテスト名が本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるに直されているとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの小機能はログインになる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="異常系",
            perspectives=["回復確認"],
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「認証」だけを持ち、設定ファイルの言語「TypeScript」のテスト結果に、大機能「在庫」のテスト名「[本体:在庫]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」のケースがあるとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "大機能「在庫」が区分「本体」の一覧にないことを示すメッセージで終了する",
                ),
                (
                    "Given",
                    "設定ファイルの言語「TypeScript」のテスト結果のテスト名が「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」に直されているとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                ("Then", "カタログに載るそのケースの小機能は「ログイン」になる"),
            ],
        )
        entry = write_typescript_result(
            tmp_path,
            [
                (
                    "[本体:在庫]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される",
                    LOGIN_PROPERTIES,
                )
            ],
        )
        config = build_config(tmp_path, [entry], FEATURES_AUTH)
        result = run_catalog_generation(tmp_path, config)
        assert_stopped_with_message(result, "大機能「在庫」", "区分「本体」")
        write_typescript_result(tmp_path, [(LOGIN_TEST_NAME, LOGIN_PROPERTIES)])
        page = generate_catalog_page(tmp_path, config)
        assert page.catalog["cases"][0]["s"] == "ログイン"


class Test本体__テストケースカタログ__入力__Python_のクラス名の読み取り:
    def test_機能の一覧が_区分本体に大機能注文を持つとき_クラス名teststest_ordersTest本体__注文__送料計算のケースを読み取ると_読み取ったケースの区分は本体になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["境界値", "件数・有無"],
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「注文」を持つとき"),
                (
                    "When",
                    "クラス名「tests.test_orders.Test本体__注文__送料計算」のケースを読み取る",
                ),
                ("Then", "読み取ったケースの区分は「本体」になる"),
            ],
        )
        case = catalog.read_python_case(
            "tests.test_orders.Test本体__注文__送料計算",
            SHIPPING_FEE_PROPERTIES,
            FEATURES_ORDER,
        )
        assert case["region"] == "本体"

    def test_機能の一覧が_区分本体に大機能注文を持つとき_クラス名teststest_ordersTest本体__注文__送料計算のケースを読み取ると_読み取ったケースの大機能は注文になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["境界値", "件数・有無"],
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「注文」を持つとき"),
                (
                    "When",
                    "クラス名「tests.test_orders.Test本体__注文__送料計算」のケースを読み取る",
                ),
                ("Then", "読み取ったケースの大機能は「注文」になる"),
            ],
        )
        case = catalog.read_python_case(
            "tests.test_orders.Test本体__注文__送料計算",
            SHIPPING_FEE_PROPERTIES,
            FEATURES_ORDER,
        )
        assert case["major"] == "注文"

    def test_機能の一覧が_区分本体に大機能注文を持つとき_クラス名teststest_ordersTest本体__注文__送料計算のケースを読み取ると_読み取ったケースの中機能はなしになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["境界値", "件数・有無"],
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「注文」を持つとき"),
                (
                    "When",
                    "クラス名「tests.test_orders.Test本体__注文__送料計算」のケースを読み取る",
                ),
                ("Then", "読み取ったケースの中機能はなしになる"),
            ],
        )
        case = catalog.read_python_case(
            "tests.test_orders.Test本体__注文__送料計算",
            SHIPPING_FEE_PROPERTIES,
            FEATURES_ORDER,
        )
        assert case["minor"] is None

    def test_機能の一覧が_区分本体に大機能注文を持つとき_クラス名teststest_ordersTest本体__注文__送料計算のケースを読み取ると_読み取ったケースの小機能は送料計算になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["境界値", "件数・有無"],
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「注文」を持つとき"),
                (
                    "When",
                    "クラス名「tests.test_orders.Test本体__注文__送料計算」のケースを読み取る",
                ),
                ("Then", "読み取ったケースの小機能は「送料計算」になる"),
            ],
        )
        case = catalog.read_python_case(
            "tests.test_orders.Test本体__注文__送料計算",
            SHIPPING_FEE_PROPERTIES,
            FEATURES_ORDER,
        )
        assert case["feature"] == "送料計算"

    def test_機能の一覧が_区分本体に大機能注文と中機能画面表示を持つとき_クラス名teststest_ordersTest本体__注文__画面表示__送料の表示のケースを読み取ると_読み取ったケースの区分は本体になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["境界値", "件数・有無"],
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「注文」と中機能「画面表示」を持つとき",
                ),
                (
                    "When",
                    "クラス名「tests.test_orders.Test本体__注文__画面表示__送料の表示」のケースを読み取る",
                ),
                ("Then", "読み取ったケースの区分は「本体」になる"),
            ],
        )
        case = catalog.read_python_case(
            "tests.test_orders.Test本体__注文__画面表示__送料の表示",
            SHIPPING_FEE_PROPERTIES,
            build_features_of_region("本体", ["注文"], ["画面表示"]),
        )
        assert case["region"] == "本体"

    def test_機能の一覧が_区分本体に大機能注文と中機能画面表示を持つとき_クラス名teststest_ordersTest本体__注文__画面表示__送料の表示のケースを読み取ると_読み取ったケースの大機能は注文になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["境界値", "件数・有無"],
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「注文」と中機能「画面表示」を持つとき",
                ),
                (
                    "When",
                    "クラス名「tests.test_orders.Test本体__注文__画面表示__送料の表示」のケースを読み取る",
                ),
                ("Then", "読み取ったケースの大機能は「注文」になる"),
            ],
        )
        case = catalog.read_python_case(
            "tests.test_orders.Test本体__注文__画面表示__送料の表示",
            SHIPPING_FEE_PROPERTIES,
            build_features_of_region("本体", ["注文"], ["画面表示"]),
        )
        assert case["major"] == "注文"

    def test_機能の一覧が_区分本体に大機能注文と中機能画面表示を持つとき_クラス名teststest_ordersTest本体__注文__画面表示__送料の表示のケースを読み取ると_読み取ったケースの中機能は画面表示になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["境界値", "件数・有無"],
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「注文」と中機能「画面表示」を持つとき",
                ),
                (
                    "When",
                    "クラス名「tests.test_orders.Test本体__注文__画面表示__送料の表示」のケースを読み取る",
                ),
                ("Then", "読み取ったケースの中機能は「画面表示」になる"),
            ],
        )
        case = catalog.read_python_case(
            "tests.test_orders.Test本体__注文__画面表示__送料の表示",
            SHIPPING_FEE_PROPERTIES,
            build_features_of_region("本体", ["注文"], ["画面表示"]),
        )
        assert case["minor"] == "画面表示"

    def test_機能の一覧が_区分本体に大機能注文と中機能画面表示を持つとき_クラス名teststest_ordersTest本体__注文__画面表示__送料の表示のケースを読み取ると_読み取ったケースの小機能は送料の表示になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["境界値", "件数・有無"],
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「注文」と中機能「画面表示」を持つとき",
                ),
                (
                    "When",
                    "クラス名「tests.test_orders.Test本体__注文__画面表示__送料の表示」のケースを読み取る",
                ),
                ("Then", "読み取ったケースの小機能は「送料の表示」になる"),
            ],
        )
        case = catalog.read_python_case(
            "tests.test_orders.Test本体__注文__画面表示__送料の表示",
            SHIPPING_FEE_PROPERTIES,
            build_features_of_region("本体", ["注文"], ["画面表示"]),
        )
        assert case["feature"] == "送料の表示"

    def test_機能の一覧が_区分本体に大機能決済を持つとき_クラス名teststest_ordersTest本体__決済__与信_判定のケースを読み取ると_読み取ったケースの小機能は与信_判定になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「決済」を持つとき"),
                (
                    "When",
                    "クラス名「tests.test_orders.Test本体__決済__与信_判定」のケースを読み取る",
                ),
                ("Then", "読み取ったケースの小機能は「与信 判定」になる"),
            ],
        )
        case = catalog.read_python_case(
            "tests.test_orders.Test本体__決済__与信_判定",
            SHIPPING_FEE_PROPERTIES,
            build_features_of_region("本体", ["決済"]),
        )
        assert case["feature"] == "与信 判定"

    def test_機能の一覧が_区分本体に大機能注文_履歴を持つとき_クラス名teststest_ordersTest本体__注文_履歴__送料計算のケースを読み取ると_読み取ったケースの大機能は注文_履歴になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「注文 履歴」を持つとき"),
                (
                    "When",
                    "クラス名「tests.test_orders.Test本体__注文_履歴__送料計算」のケースを読み取る",
                ),
                ("Then", "読み取ったケースの大機能は「注文 履歴」になる"),
            ],
        )
        case = catalog.read_python_case(
            "tests.test_orders.Test本体__注文_履歴__送料計算",
            SHIPPING_FEE_PROPERTIES,
            build_features_of_region("本体", ["注文 履歴"]),
        )
        assert case["major"] == "注文 履歴"

    def test_機能の一覧が_区分本体に大機能注文と中機能履歴_表示を持つとき_クラス名teststest_ordersTest本体__注文__履歴_表示__送料の表示のケースを読み取ると_読み取ったケースの中機能は履歴_表示になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「注文」と中機能「履歴 表示」を持つとき",
                ),
                (
                    "When",
                    "クラス名「tests.test_orders.Test本体__注文__履歴_表示__送料の表示」のケースを読み取る",
                ),
                ("Then", "読み取ったケースの中機能は「履歴 表示」になる"),
            ],
        )
        case = catalog.read_python_case(
            "tests.test_orders.Test本体__注文__履歴_表示__送料の表示",
            SHIPPING_FEE_PROPERTIES,
            build_features_of_region("本体", ["注文"], ["履歴 表示"]),
        )
        assert case["minor"] == "履歴 表示"

    def test_クラス名teststest_ordersTest本体__注文のケースを読み取ると_クラス名が区分大機能中機能小機能の形ではないことを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            perspectives=["境界値"],
            items=[
                (
                    "When",
                    "クラス名「tests.test_orders.Test本体__注文」のケースを読み取る",
                ),
                (
                    "Then",
                    "クラス名が区分・大機能・(中機能・)小機能の形ではないことを示すエラーになる",
                ),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_python_case(
                "tests.test_orders.Test本体__注文",
                SHIPPING_FEE_PROPERTIES,
                build_features_of_region("本体", ["注文"], ["画面表示"]),
            )
        assert_message_contains(
            error.value, "区分・大機能・(中機能・)小機能", "形ではない"
        )

    def test_クラス名teststest_ordersTest本体__注文__画面表示__送料の表示__金額のケースを読み取ると_クラス名が区分大機能中機能小機能の形ではないことを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            perspectives=["境界値"],
            items=[
                (
                    "When",
                    "クラス名「tests.test_orders.Test本体__注文__画面表示__送料の表示__金額」のケースを読み取る",
                ),
                (
                    "Then",
                    "クラス名が区分・大機能・(中機能・)小機能の形ではないことを示すエラーになる",
                ),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_python_case(
                "tests.test_orders.Test本体__注文__画面表示__送料の表示__金額",
                SHIPPING_FEE_PROPERTIES,
                build_features_of_region("本体", ["注文"], ["画面表示"]),
            )
        assert_message_contains(
            error.value, "区分・大機能・(中機能・)小機能", "形ではない"
        )

    def test_機能の一覧が_区分本体に大機能注文を持つとき_クラス名teststest_ordersTest本体__注文__送料計算Test金額3000円のケースを読み取ると_読み取ったケースの小機能は送料計算になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「注文」を持つとき"),
                (
                    "When",
                    "クラス名「tests.test_orders.Test本体__注文__送料計算.Test金額3000円」のケースを読み取る",
                ),
                ("Then", "読み取ったケースの小機能は「送料計算」になる"),
            ],
        )
        case = catalog.read_python_case(
            "tests.test_orders.Test本体__注文__送料計算.Test金額3000円",
            SHIPPING_FEE_PROPERTIES,
            FEATURES_ORDER,
        )
        assert case["feature"] == "送料計算"

    def test_クラス名teststest_ordersのケースを読み取ると_クラス名が_Test_で始まっていないことを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                ("When", "クラス名「tests.test_orders」のケースを読み取る"),
                ("Then", "クラス名が `Test` で始まっていないことを示すエラーになる"),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_python_case(
                "tests.test_orders",
                SHIPPING_FEE_PROPERTIES,
                build_features_of_region("本体", ["注文"], ["画面表示"]),
            )
        assert_message_contains(error.value, "Test で始まっていない")


class Test本体__テストケースカタログ__入力__言語ごとの機能名の取り出し:
    @pytest.mark.parametrize(
        ("given", "write_result"),
        [
            pytest.param(
                "機能の一覧が、区分「本体」に大機能「注文」を持ち、設定ファイルの言語「Python」のテスト結果に、クラス名「tests.test_orders.Test本体__注文__送料計算」で、種別「単体テスト」、正常異常「正常系」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持つケースがあるとき",
                lambda directory: write_python_result(
                    directory,
                    [
                        (
                            "tests.test_orders.Test本体__注文__送料計算",
                            SHIPPING_FEE_PROPERTIES,
                        )
                    ],
                ),
                id="機能の一覧が_区分本体に大機能注文を持ち_設定ファイルの言語Pythonのテスト結果に_クラス名teststest_ordersTest本体__注文__送料計算で_種別単体テスト_正常異常正常系_When注文金額3000円で送料を計算する_Then送料は無料になるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの機能名は本体注文送料計算になる",
            ),
            pytest.param(
                "機能の一覧が、区分「本体」に大機能「注文」を持ち、設定ファイルの言語「C#」のテスト結果に、Trait「区分・大機能・中機能・小機能」が「[本体:注文]送料計算」で、種別「単体テスト」、正常異常「正常系」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持つケースがあるとき",
                lambda directory: write_csharp_result(
                    directory,
                    [
                        (
                            SHIPPING_FEE_CASE_NAME,
                            (CSHARP_ORDER_FEATURE_NAME, *SHIPPING_FEE_PROPERTIES),
                        )
                    ],
                ),
                id="機能の一覧が_区分本体に大機能注文を持ち_設定ファイルの言語Cのテスト結果に_Trait区分大機能中機能小機能が本体注文送料計算で_種別単体テスト_正常異常正常系_When注文金額3000円で送料を計算する_Then送料は無料になるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの機能名は本体注文送料計算になる",
            ),
            pytest.param(
                "機能の一覧が、区分「本体」に大機能「注文」を持ち、設定ファイルの言語「Kotlin」のテスト結果に、テストクラスの表示名が「[本体:注文]送料計算」で、種別「単体テスト」、正常異常「正常系」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持つケースがあるとき",
                lambda directory: write_kotlin_result(
                    directory,
                    [
                        (
                            "[本体:注文]送料計算",
                            SHIPPING_FEE_CASE_NAME,
                            SHIPPING_FEE_PROPERTIES,
                        )
                    ],
                ),
                id="機能の一覧が_区分本体に大機能注文を持ち_設定ファイルの言語Kotlinのテスト結果に_テストクラスの表示名が本体注文送料計算で_種別単体テスト_正常異常正常系_When注文金額3000円で送料を計算する_Then送料は無料になるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの機能名は本体注文送料計算になる",
            ),
            pytest.param(
                "機能の一覧が、区分「本体」に大機能「注文」を持ち、設定ファイルの言語「Go」のテスト結果に、テスト「TestShippingFee/[本体:注文]送料計算/注文金額3000円で送料を計算すると、送料は無料になる」で、種別「単体テスト」、正常異常「正常系」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持つケースがあるとき",
                lambda directory: write_go_result(
                    directory,
                    [
                        (
                            f"TestShippingFee/[本体:注文]送料計算/{SHIPPING_FEE_CASE_NAME}",
                            SHIPPING_FEE_PROPERTIES,
                        )
                    ],
                ),
                id="機能の一覧が_区分本体に大機能注文を持ち_設定ファイルの言語Goのテスト結果に_テストTestShippingFee本体注文送料計算注文金額3000円で送料を計算すると_送料は無料になるで_種別単体テスト_正常異常正常系_When注文金額3000円で送料を計算する_Then送料は無料になるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの機能名は本体注文送料計算になる",
            ),
            pytest.param(
                "機能の一覧が、区分「本体」に大機能「注文」を持ち、設定ファイルの言語「Dart」のテスト結果に、グループ「[本体:注文]送料計算」のテスト「注文金額3000円で送料を計算すると、送料は無料になる」で、種別「単体テスト」、正常異常「正常系」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持つケースがあるとき",
                lambda directory: write_dart_result(
                    directory,
                    [(SHIPPING_FEE_CASE_NAME, spec_prints(SHIPPING_FEE_PROPERTIES))],
                    group_names=["[本体:注文]送料計算"],
                ),
                id="機能の一覧が_区分本体に大機能注文を持ち_設定ファイルの言語Dartのテスト結果に_グループ本体注文送料計算のテスト注文金額3000円で送料を計算すると_送料は無料になるで_種別単体テスト_正常異常正常系_When注文金額3000円で送料を計算する_Then送料は無料になるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの機能名は本体注文送料計算になる",
            ),
        ],
    )
    def test_extracts_feature_name_per_language(
        self, record_case, tmp_path, given, write_result
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", given),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "カタログに載るそのケースの機能名は「[本体:注文]送料計算」になる",
                ),
            ],
        )
        entry = write_result(tmp_path)
        config = build_config(tmp_path, [entry], FEATURES_ORDER)
        page = generate_catalog_page(tmp_path, config)
        assert [
            (case["k"], case["d"], case["m"], case["s"])
            for case in page.catalog["cases"]
        ] == [("本体", "注文", "", "送料計算")]

    def test_設定ファイルの言語Cのテスト結果に_Trait区分大機能中機能小機能を持たず_種別単体テスト_正常異常正常系_When注文金額3000円で送料を計算する_Then送料は無料になるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_Trait区分大機能中機能小機能がないことを示すエラーで止まる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "Given",
                    "設定ファイルの言語「C#」のテスト結果に、Trait「区分・大機能・中機能・小機能」を持たず、種別「単体テスト」、正常異常「正常系」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持つケースがあるとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "Trait「区分・大機能・中機能・小機能」がないことを示すエラーで止まる",
                ),
            ],
        )
        entry = write_csharp_result(
            tmp_path, [(SHIPPING_FEE_CASE_NAME, SHIPPING_FEE_PROPERTIES)]
        )
        config = build_config(tmp_path, [entry], FEATURES_ORDER)
        result = run_catalog_generation(tmp_path, config)
        assert_stopped_with_message(
            result, "Trait「区分・大機能・中機能・小機能」がない"
        )

    def test_設定ファイルの言語Kotlinのテスト結果に_テストクラスの表示名が送料計算で_種別単体テスト_正常異常正常系_When注文金額3000円で送料を計算する_Then送料は無料になるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_テストクラスの表示名送料計算が_区分大機能中機能小機能_の形ではないことを示すエラーで止まる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "Given",
                    "設定ファイルの言語「Kotlin」のテスト結果に、テストクラスの表示名が「送料計算」で、種別「単体テスト」、正常異常「正常系」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持つケースがあるとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "テストクラスの表示名「送料計算」が `[区分:大機能(:中機能)]小機能` の形ではないことを示すエラーで止まる",
                ),
            ],
        )
        entry = write_kotlin_result(
            tmp_path, [("送料計算", SHIPPING_FEE_CASE_NAME, SHIPPING_FEE_PROPERTIES)]
        )
        config = build_config(tmp_path, [entry], FEATURES_ORDER)
        result = run_catalog_generation(tmp_path, config)
        assert_stopped_with_message(
            result,
            "テストクラスの表示名「送料計算」",
            "[区分:大機能(:中機能)]小機能",
            "形ではない",
        )

    def test_設定ファイルの言語Goのテスト結果に_テストTestShippingFee本体注文送料計算で_種別単体テスト_正常異常正常系_When注文金額3000円で送料を計算する_Then送料は無料になるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_テストTestShippingFee本体注文送料計算がテスト関数機能名ケースの_3_階層ではないことを示すエラーで止まる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="異常系",
            perspectives=["境界値"],
            items=[
                (
                    "Given",
                    "設定ファイルの言語「Go」のテスト結果に、テスト「TestShippingFee/[本体:注文]送料計算」で、種別「単体テスト」、正常異常「正常系」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持つケースがあるとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "テスト「TestShippingFee/[本体:注文]送料計算」がテスト関数・機能名・ケースの 3 階層ではないことを示すエラーで止まる",
                ),
            ],
        )
        entry = write_go_result(
            tmp_path, [("TestShippingFee/[本体:注文]送料計算", SHIPPING_FEE_PROPERTIES)]
        )
        config = build_config(tmp_path, [entry], FEATURES_ORDER)
        result = run_catalog_generation(tmp_path, config)
        assert_stopped_with_message(
            result,
            "テスト「TestShippingFee/[本体:注文]送料計算」",
            "テスト関数・機能名・ケースの 3 階層ではない",
        )

    def test_設定ファイルの言語Goのテスト結果に_テストTestShippingFee本体注文送料計算注文金額3000円で送料を計算すると_送料は無料になる金額3000円で_種別単体テスト_正常異常正常系_When注文金額3000円で送料を計算する_Then送料は無料になるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_テストTestShippingFee本体注文送料計算注文金額3000円で送料を計算すると_送料は無料になる金額3000円がテスト関数機能名ケースの_3_階層ではないことを示すエラーで止まる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="異常系",
            perspectives=["境界値"],
            items=[
                (
                    "Given",
                    "設定ファイルの言語「Go」のテスト結果に、テスト「TestShippingFee/[本体:注文]送料計算/注文金額3000円で送料を計算すると、送料は無料になる/金額3000円」で、種別「単体テスト」、正常異常「正常系」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持つケースがあるとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "テスト「TestShippingFee/[本体:注文]送料計算/注文金額3000円で送料を計算すると、送料は無料になる/金額3000円」がテスト関数・機能名・ケースの 3 階層ではないことを示すエラーで止まる",
                ),
            ],
        )
        entry = write_go_result(
            tmp_path,
            [
                (
                    f"TestShippingFee/[本体:注文]送料計算/{SHIPPING_FEE_CASE_NAME}/金額3000円",
                    SHIPPING_FEE_PROPERTIES,
                )
            ],
        )
        config = build_config(tmp_path, [entry], FEATURES_ORDER)
        result = run_catalog_generation(tmp_path, config)
        assert_stopped_with_message(
            result,
            "テスト「TestShippingFee/[本体:注文]送料計算/注文金額3000円で送料を計算すると、送料は無料になる/金額3000円」",
            "テスト関数・機能名・ケースの 3 階層ではない",
        )

    def test_設定ファイルの言語Dartのテスト結果に_グループに入っていないテスト注文金額3000円で送料を計算すると_送料は無料になるで_種別単体テスト_正常異常正常系_When注文金額3000円で送料を計算する_Then送料は無料になるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_テスト注文金額3000円で送料を計算すると_送料は無料になるが機能名のグループに入っていないことを示すエラーで止まる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "Given",
                    "設定ファイルの言語「Dart」のテスト結果に、グループに入っていないテスト「注文金額3000円で送料を計算すると、送料は無料になる」で、種別「単体テスト」、正常異常「正常系」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持つケースがあるとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "テスト「注文金額3000円で送料を計算すると、送料は無料になる」が機能名のグループに入っていないことを示すエラーで止まる",
                ),
            ],
        )
        entry = write_dart_result(
            tmp_path,
            [(SHIPPING_FEE_CASE_NAME, spec_prints(SHIPPING_FEE_PROPERTIES))],
        )
        config = build_config(tmp_path, [entry], FEATURES_ORDER)
        result = run_catalog_generation(tmp_path, config)
        assert_stopped_with_message(
            result,
            "テスト「注文金額3000円で送料を計算すると、送料は無料になる」",
            "機能名のグループに入っていない",
        )


class Test本体__テストケースカタログ__入力__言語ごとの項目の取り出し:
    @pytest.mark.parametrize(
        ("given", "write_result"),
        [
            pytest.param(
                "機能の一覧が、区分「本体」に大機能「出題」を持ち、設定ファイルの言語「Python」のテスト結果に、クラス名「tests.test_hint.Test本体__出題__ヒントの表示」で、種別「単体テスト」、正常異常「正常系」、Given「ログインしているとき」、When「ホーム画面で「探しに行く」を押す」と「出題画面で「ヒント」を押す」、Then「出題の英文が表示される」を持つケースがあるとき",
                lambda directory: write_python_result(
                    directory,
                    [("tests.test_hint.Test本体__出題__ヒントの表示", HINT_PROPERTIES)],
                ),
                id="機能の一覧が_区分本体に大機能出題を持ち_設定ファイルの言語Pythonのテスト結果に_クラス名teststest_hintTest本体__出題__ヒントの表示で_種別単体テスト_正常異常正常系_Givenログインしているとき_Whenホーム画面で探しに行くを押すと出題画面でヒントを押す_Then出題の英文が表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースのステップは_Givenログインしているとき_Whenホーム画面で探しに行くを押す出題画面でヒントを押す_Then出題の英文が表示されるの_1_つになる",
            ),
            pytest.param(
                "機能の一覧が、区分「本体」に大機能「出題」を持ち、設定ファイルの言語「Kotlin」のテスト結果に、テストクラスの表示名が「[本体:出題]ヒントの表示」で、種別「単体テスト」、正常異常「正常系」、Given「ログインしているとき」、When「ホーム画面で「探しに行く」を押す」と「出題画面で「ヒント」を押す」、Then「出題の英文が表示される」を持つケースがあるとき",
                lambda directory: write_kotlin_result(
                    directory,
                    [("[本体:出題]ヒントの表示", HINT_CASE_NAME, HINT_PROPERTIES)],
                ),
                id="機能の一覧が_区分本体に大機能出題を持ち_設定ファイルの言語Kotlinのテスト結果に_テストクラスの表示名が本体出題ヒントの表示で_種別単体テスト_正常異常正常系_Givenログインしているとき_Whenホーム画面で探しに行くを押すと出題画面でヒントを押す_Then出題の英文が表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースのステップは_Givenログインしているとき_Whenホーム画面で探しに行くを押す出題画面でヒントを押す_Then出題の英文が表示されるの_1_つになる",
            ),
            pytest.param(
                "機能の一覧が、区分「本体」に大機能「出題」を持ち、設定ファイルの言語「Go」のテスト結果に、テスト「TestHint/[本体:出題]ヒントの表示/ログインしているとき、ホーム画面で「探しに行く」を押し、出題画面で「ヒント」を押すと、出題の英文が表示される」で、種別「単体テスト」、正常異常「正常系」、Given「ログインしているとき」、When「ホーム画面で「探しに行く」を押す」と「出題画面で「ヒント」を押す」、Then「出題の英文が表示される」を持つケースがあるとき",
                lambda directory: write_go_result(
                    directory,
                    [
                        (
                            f"TestHint/[本体:出題]ヒントの表示/{HINT_CASE_NAME}",
                            HINT_PROPERTIES,
                        )
                    ],
                ),
                id="機能の一覧が_区分本体に大機能出題を持ち_設定ファイルの言語Goのテスト結果に_テストTestHint本体出題ヒントの表示ログインしているとき_ホーム画面で探しに行くを押し_出題画面でヒントを押すと_出題の英文が表示されるで_種別単体テスト_正常異常正常系_Givenログインしているとき_Whenホーム画面で探しに行くを押すと出題画面でヒントを押す_Then出題の英文が表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースのステップは_Givenログインしているとき_Whenホーム画面で探しに行くを押す出題画面でヒントを押す_Then出題の英文が表示されるの_1_つになる",
            ),
            pytest.param(
                "機能の一覧が、区分「本体」に大機能「出題」を持ち、設定ファイルの言語「Dart」のテスト結果に、グループ「[本体:出題]ヒントの表示」のテスト「ログインしているとき、ホーム画面で「探しに行く」を押し、出題画面で「ヒント」を押すと、出題の英文が表示される」で、種別「単体テスト」、正常異常「正常系」、Given「ログインしているとき」、When「ホーム画面で「探しに行く」を押す」と「出題画面で「ヒント」を押す」、Then「出題の英文が表示される」を持つケースがあるとき",
                lambda directory: write_dart_result(
                    directory,
                    [(HINT_CASE_NAME, spec_prints(HINT_PROPERTIES))],
                    group_names=["[本体:出題]ヒントの表示"],
                ),
                id="機能の一覧が_区分本体に大機能出題を持ち_設定ファイルの言語Dartのテスト結果に_グループ本体出題ヒントの表示のテストログインしているとき_ホーム画面で探しに行くを押し_出題画面でヒントを押すと_出題の英文が表示されるで_種別単体テスト_正常異常正常系_Givenログインしているとき_Whenホーム画面で探しに行くを押すと出題画面でヒントを押す_Then出題の英文が表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースのステップは_Givenログインしているとき_Whenホーム画面で探しに行くを押す出題画面でヒントを押す_Then出題の英文が表示されるの_1_つになる",
            ),
        ],
    )
    def test_extracts_steps_per_language(
        self, record_case, tmp_path, given, write_result
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", given),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "カタログに載るそのケースのステップは、Given「ログインしているとき」、When「ホーム画面で「探しに行く」を押す」「出題画面で「ヒント」を押す」、Then「出題の英文が表示される」の 1 つになる",
                ),
            ],
        )
        entry = write_result(tmp_path)
        config = build_config(tmp_path, [entry], FEATURES_HINT)
        page = generate_catalog_page(tmp_path, config)
        assert page.catalog["cases"][0]["steps"] == HINT_STEPS

    def test_機能の一覧が_区分本体に大機能注文を持ち_設定ファイルの言語Goのテスト結果に_テストTestShippingFee本体注文送料計算注文金額3000円で送料を計算すると_送料は無料になるが種別単体テスト_正常異常正常系_When注文金額3000円で送料を計算する_Then送料は無料になるを_テストTestShippingFee本体注文送料計算注文金額2999円で送料を計算すると_送料は500円になるが種別単体テスト_正常異常正常系_When注文金額2999円で送料を計算する_Then送料は500円になるを持ち_2_つのテストの項目が_種別_正常異常_When_Then_の順に_3000円のテスト_2999円のテストの順で_1_項目ずつ交互に出ているとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載る注文金額2999円のケースのステップは_When注文金額2999円で送料を計算する_Then送料は500円になるの_1_つになる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「注文」を持ち、設定ファイルの言語「Go」のテスト結果に、テスト「TestShippingFee/[本体:注文]送料計算/注文金額3000円で送料を計算すると、送料は無料になる」が種別「単体テスト」、正常異常「正常系」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を、テスト「TestShippingFee/[本体:注文]送料計算/注文金額2999円で送料を計算すると、送料は500円になる」が種別「単体テスト」、正常異常「正常系」、When「注文金額2999円で送料を計算する」、Then「送料は500円になる」を持ち、2 つのテストの項目が、種別、正常異常、When、Then の順に、3000円のテスト、2999円のテストの順で 1 項目ずつ交互に出ているとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "カタログに載る注文金額2999円のケースのステップは、When「注文金額2999円で送料を計算する」、Then「送料は500円になる」の 1 つになる",
                ),
            ],
        )
        entry = write_go_interleaved_result(
            tmp_path,
            [
                (
                    "TestShippingFee/[本体:注文]送料計算/注文金額3000円で送料を計算すると、送料は無料になる",
                    SHIPPING_FEE_PROPERTIES,
                ),
                (
                    "TestShippingFee/[本体:注文]送料計算/注文金額2999円で送料を計算すると、送料は500円になる",
                    (
                        ("種別", "単体テスト"),
                        ("正常異常", "正常系"),
                        ("When", "注文金額2999円で送料を計算する"),
                        ("Then", "送料は500円になる"),
                    ),
                ),
            ],
        )
        config = build_config(tmp_path, [entry], FEATURES_ORDER)
        page = generate_catalog_page(tmp_path, config)
        cases_by_then = {case["steps"][0]["T"]: case for case in page.catalog["cases"]}
        assert cases_by_then["送料は500円になる"]["steps"] == [
            {"G": "", "W": ["注文金額2999円で送料を計算する"], "T": "送料は500円になる"}
        ]

    def test_機能の一覧が_区分本体に大機能注文を持ち_設定ファイルの言語Dartのテスト結果に_グループ本体注文送料計算のテスト注文金額3000円で送料を計算すると_送料は無料になるが_種別単体テスト_正常異常正常系_When注文金額3000円で送料を計算する_Then送料は無料になるを持つほかに_spec_で始まらない出力デバッグ用を出すとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースのステップは_Given_なし_When注文金額3000円で送料を計算する_Then送料は無料になるの_1_つになる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「注文」を持ち、設定ファイルの言語「Dart」のテスト結果に、グループ「[本体:注文]送料計算」のテスト「注文金額3000円で送料を計算すると、送料は無料になる」が、種別「単体テスト」、正常異常「正常系」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持つほかに、`@spec` で始まらない出力「デバッグ用」を出すとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "カタログに載るそのケースのステップは、Given なし、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」の 1 つになる",
                ),
            ],
        )
        entry = write_dart_result(
            tmp_path,
            [
                (
                    SHIPPING_FEE_CASE_NAME,
                    [*spec_prints(SHIPPING_FEE_PROPERTIES), "デバッグ用"],
                )
            ],
            group_names=["[本体:注文]送料計算"],
        )
        config = build_config(tmp_path, [entry], FEATURES_ORDER)
        page = generate_catalog_page(tmp_path, config)
        assert page.catalog["cases"][0]["steps"] == [
            {"G": "", "W": ["注文金額3000円で送料を計算する"], "T": "送料は無料になる"}
        ]

    def test_機能の一覧が_区分本体に大機能注文を持ち_設定ファイルの言語Dartのテスト結果に_グループ本体注文送料計算のテスト注文金額3000円で送料を計算すると_送料は無料になるが_種別単体テスト_正常異常正常系_When注文金額3000円で送料を計算する_Then送料は無料になるを持つほかに_spec_で始まり__を含まない出力spec_種別を出すとき_設定ファイルを渡して生成コマンドを実行すると_出力spec_種別が_spec_キー値_の形ではないことを示すエラーで止まる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「注文」を持ち、設定ファイルの言語「Dart」のテスト結果に、グループ「[本体:注文]送料計算」のテスト「注文金額3000円で送料を計算すると、送料は無料になる」が、種別「単体テスト」、正常異常「正常系」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持つほかに、`@spec` で始まり `=` を含まない出力「@spec 種別」を出すとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "出力「@spec 種別」が `@spec キー=値` の形ではないことを示すエラーで止まる",
                ),
            ],
        )
        entry = write_dart_result(
            tmp_path,
            [
                (
                    SHIPPING_FEE_CASE_NAME,
                    [*spec_prints(SHIPPING_FEE_PROPERTIES), "@spec 種別"],
                )
            ],
            group_names=["[本体:注文]送料計算"],
        )
        config = build_config(tmp_path, [entry], FEATURES_ORDER)
        result = run_catalog_generation(tmp_path, config)
        assert_stopped_with_message(
            result, "出力「@spec 種別」", "@spec キー=値", "形ではない"
        )

    def test_機能の一覧が_区分本体に大機能出題を持ち_設定ファイルの言語Cのテスト結果に_Trait区分大機能中機能小機能が本体出題ヒントの表示で_種別単体テスト_正常異常正常系_Given1ログインしているとき_When1ホーム画面で探しに行くを押す_Then1出題の英文が表示される_When2結果画面でもう一度を押す_Then2新しい出題の英文が表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースのステップは_1_つ目が_Givenログインしているとき_Whenホーム画面で探しに行くを押す_Then出題の英文が表示される_2_つ目が_Given_なし_When結果画面でもう一度を押す_Then新しい出題の英文が表示されるの_2_つになる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「出題」を持ち、設定ファイルの言語「C#」のテスト結果に、Trait「区分・大機能・中機能・小機能」が「[本体:出題]ヒントの表示」で、種別「単体テスト」、正常異常「正常系」、Given1「ログインしているとき」、When1「ホーム画面で「探しに行く」を押す」、Then1「出題の英文が表示される」、When2「結果画面で「もう一度」を押す」、Then2「新しい出題の英文が表示される」を持つケースがあるとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "カタログに載るそのケースのステップは、1 つ目が Given「ログインしているとき」、When「ホーム画面で「探しに行く」を押す」、Then「出題の英文が表示される」、2 つ目が Given なし、When「結果画面で「もう一度」を押す」、Then「新しい出題の英文が表示される」の 2 つになる",
                ),
            ],
        )
        entry = write_csharp_result(
            tmp_path,
            [
                (
                    HINT_CASE_NAME,
                    (
                        ("区分・大機能・中機能・小機能", "[本体:出題]ヒントの表示"),
                        ("種別", "単体テスト"),
                        ("正常異常", "正常系"),
                        ("Given1", "ログインしているとき"),
                        ("When1", "ホーム画面で「探しに行く」を押す"),
                        ("Then1", "出題の英文が表示される"),
                        ("When2", "結果画面で「もう一度」を押す"),
                        ("Then2", "新しい出題の英文が表示される"),
                    ),
                )
            ],
        )
        config = build_config(tmp_path, [entry], FEATURES_HINT)
        page = generate_catalog_page(tmp_path, config)
        assert page.catalog["cases"][0]["steps"] == [
            {
                "G": "ログインしているとき",
                "W": ["ホーム画面で「探しに行く」を押す"],
                "T": "出題の英文が表示される",
            },
            {
                "G": "",
                "W": ["結果画面で「もう一度」を押す"],
                "T": "新しい出題の英文が表示される",
            },
        ]

    def test_機能の一覧が_区分本体に大機能出題を持ち_設定ファイルの言語Cのテスト結果に_Trait区分大機能中機能小機能が本体出題ヒントの表示で_種別単体テスト_正常異常正常系_When1ホーム画面で探しに行くを押す_When1出題画面でヒントを押す_Then1出題の英文が表示される_When2結果画面でもう一度を押す_Then2新しい出題の英文が表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの_1_つ目のステップの_When_は_ホーム画面で探しに行くを押す出題画面でヒントを押すになる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「出題」を持ち、設定ファイルの言語「C#」のテスト結果に、Trait「区分・大機能・中機能・小機能」が「[本体:出題]ヒントの表示」で、種別「単体テスト」、正常異常「正常系」、When1「ホーム画面で「探しに行く」を押す」、When1「出題画面で「ヒント」を押す」、Then1「出題の英文が表示される」、When2「結果画面で「もう一度」を押す」、Then2「新しい出題の英文が表示される」を持つケースがあるとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "カタログに載るそのケースの 1 つ目のステップの When は、「ホーム画面で「探しに行く」を押す」「出題画面で「ヒント」を押す」になる",
                ),
            ],
        )
        entry = write_csharp_result(
            tmp_path,
            [
                (
                    HINT_CASE_NAME,
                    (
                        ("区分・大機能・中機能・小機能", "[本体:出題]ヒントの表示"),
                        ("種別", "単体テスト"),
                        ("正常異常", "正常系"),
                        ("When1", "ホーム画面で「探しに行く」を押す"),
                        ("When1", "出題画面で「ヒント」を押す"),
                        ("Then1", "出題の英文が表示される"),
                        ("When2", "結果画面で「もう一度」を押す"),
                        ("Then2", "新しい出題の英文が表示される"),
                    ),
                )
            ],
        )
        config = build_config(tmp_path, [entry], FEATURES_HINT)
        page = generate_catalog_page(tmp_path, config)
        assert page.catalog["cases"][0]["steps"][0]["W"] == [
            "ホーム画面で「探しに行く」を押す",
            "出題画面で「ヒント」を押す",
        ]

    def test_機能の一覧が_区分本体に大機能出題を持ち_設定ファイルの言語Cのテスト結果に_Trait区分大機能中機能小機能が本体出題ヒントの表示で_種別単体テスト_正常異常正常系_When1ホーム画面で探しに行くを押す_Then出題の英文が表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_番号の付いたキーと付かないキーが混ざっていることを示すエラーで止まる(
        self, record_case, tmp_path
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「本体」に大機能「出題」を持ち、設定ファイルの言語「C#」のテスト結果に、Trait「区分・大機能・中機能・小機能」が「[本体:出題]ヒントの表示」で、種別「単体テスト」、正常異常「正常系」、When1「ホーム画面で「探しに行く」を押す」、Then「出題の英文が表示される」を持つケースがあるとき",
                ),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "番号の付いたキーと付かないキーが混ざっていることを示すエラーで止まる",
                ),
            ],
        )
        entry = write_csharp_result(
            tmp_path,
            [
                (
                    HINT_CASE_NAME,
                    (
                        ("区分・大機能・中機能・小機能", "[本体:出題]ヒントの表示"),
                        ("種別", "単体テスト"),
                        ("正常異常", "正常系"),
                        ("When1", "ホーム画面で「探しに行く」を押す"),
                        ("Then", "出題の英文が表示される"),
                    ),
                )
            ],
        )
        config = build_config(tmp_path, [entry], FEATURES_HINT)
        result = run_catalog_generation(tmp_path, config)
        assert_stopped_with_message(
            result, "番号の付いたキーと付かないキーが混ざっている"
        )


class Test本体__テストケースカタログ__入力__ケースとして数えないテストの除外:
    @pytest.mark.parametrize(
        ("given", "write_result"),
        [
            pytest.param(
                "機能の一覧が、区分「本体」に大機能「注文」を持ち、設定ファイルの言語「Dart」のテスト結果に、グループ「[本体:注文]送料計算」のテスト「注文金額3000円で送料を計算すると、送料は無料になる」が種別「単体テスト」、正常異常「正常系」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持ち、ほかに、テスト実行ツールがファイルの読み込みごとに出す、名前が「loading test/shipping_fee_test.dart」で hidden が true のテストがあるとき",
                lambda directory: write_dart_result(
                    directory,
                    [(SHIPPING_FEE_CASE_NAME, spec_prints(SHIPPING_FEE_PROPERTIES))],
                    group_names=["[本体:注文]送料計算"],
                    hidden_test_names=["loading test/shipping_fee_test.dart"],
                ),
                id="機能の一覧が_区分本体に大機能注文を持ち_設定ファイルの言語Dartのテスト結果に_グループ本体注文送料計算のテスト注文金額3000円で送料を計算すると_送料は無料になるが種別単体テスト_正常異常正常系_When注文金額3000円で送料を計算する_Then送料は無料になるを持ち_ほかに_テスト実行ツールがファイルの読み込みごとに出す_名前がloading_testshipping_fee_testdartで_hidden_が_true_のテストがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るケースは_テスト注文金額3000円で送料を計算すると_送料は無料になるの_1_つだけになる",
            ),
            pytest.param(
                "機能の一覧が、区分「本体」に大機能「注文」を持ち、設定ファイルの言語「Go」のテスト結果に、テスト「TestShippingFee/[本体:注文]送料計算/注文金額3000円で送料を計算すると、送料は無料になる」が種別「単体テスト」、正常異常「正常系」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持ち、その上位のテスト「TestShippingFee」と「TestShippingFee/[本体:注文]送料計算」が項目を持たずに実行されているとき",
                lambda directory: write_go_result(
                    directory,
                    [
                        (
                            f"TestShippingFee/[本体:注文]送料計算/{SHIPPING_FEE_CASE_NAME}",
                            SHIPPING_FEE_PROPERTIES,
                        )
                    ],
                    parent_tests=[
                        "TestShippingFee",
                        "TestShippingFee/[本体:注文]送料計算",
                    ],
                ),
                id="機能の一覧が_区分本体に大機能注文を持ち_設定ファイルの言語Goのテスト結果に_テストTestShippingFee本体注文送料計算注文金額3000円で送料を計算すると_送料は無料になるが種別単体テスト_正常異常正常系_When注文金額3000円で送料を計算する_Then送料は無料になるを持ち_その上位のテストTestShippingFeeとTestShippingFee本体注文送料計算が項目を持たずに実行されているとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るケースは_テスト注文金額3000円で送料を計算すると_送料は無料になるの_1_つだけになる",
            ),
        ],
    )
    def test_excludes_tests_not_counted_as_cases(
        self, record_case, tmp_path, given, write_result
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            perspectives=["件数・有無"],
            items=[
                ("Given", given),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "カタログに載るケースは、テスト「注文金額3000円で送料を計算すると、送料は無料になる」の 1 つだけになる",
                ),
            ],
        )
        entry = write_result(tmp_path)
        config = build_config(tmp_path, [entry], FEATURES_ORDER)
        page = generate_catalog_page(tmp_path, config)
        assert [case["steps"][0]["T"] for case in page.catalog["cases"]] == [
            "送料は無料になる"
        ]


class Test本体__テストケースカタログ__入力__言語ごとの観点の取り出し:
    @pytest.mark.parametrize(
        ("given", "write_result"),
        [
            pytest.param(
                "機能の一覧が、区分「本体」に大機能「注文」を持ち、設定ファイルの言語「Python」のテスト結果に、クラス名「tests.test_orders.Test本体__注文__送料計算」で、種別「単体テスト」、正常異常「正常系」、観点「境界値」と「エッジケース」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持つケースがあるとき",
                lambda directory: write_python_result(
                    directory,
                    [
                        (
                            "tests.test_orders.Test本体__注文__送料計算",
                            SHIPPING_FEE_PERSPECTIVE_PROPERTIES,
                        )
                    ],
                ),
                id="機能の一覧が_区分本体に大機能注文を持ち_設定ファイルの言語Pythonのテスト結果に_クラス名teststest_ordersTest本体__注文__送料計算で_種別単体テスト_正常異常正常系_観点境界値とエッジケース_When注文金額3000円で送料を計算する_Then送料は無料になるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの観点は境界値とエッジケースの_2_つになる",
            ),
            pytest.param(
                "機能の一覧が、区分「本体」に大機能「注文」を持ち、設定ファイルの言語「Kotlin」のテスト結果に、テストクラスの表示名が「[本体:注文]送料計算」で、種別「単体テスト」、正常異常「正常系」、観点「境界値」と「エッジケース」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持つケースがあるとき",
                lambda directory: write_kotlin_result(
                    directory,
                    [
                        (
                            "[本体:注文]送料計算",
                            SHIPPING_FEE_CASE_NAME,
                            SHIPPING_FEE_PERSPECTIVE_PROPERTIES,
                        )
                    ],
                ),
                id="機能の一覧が_区分本体に大機能注文を持ち_設定ファイルの言語Kotlinのテスト結果に_テストクラスの表示名が本体注文送料計算で_種別単体テスト_正常異常正常系_観点境界値とエッジケース_When注文金額3000円で送料を計算する_Then送料は無料になるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの観点は境界値とエッジケースの_2_つになる",
            ),
            pytest.param(
                "機能の一覧が、区分「本体」に大機能「注文」を持ち、設定ファイルの言語「Go」のテスト結果に、テスト「TestShippingFee/[本体:注文]送料計算/注文金額3000円で送料を計算すると、送料は無料になる」で、種別「単体テスト」、正常異常「正常系」、観点「境界値」と「エッジケース」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持つケースがあるとき",
                lambda directory: write_go_result(
                    directory,
                    [
                        (
                            f"TestShippingFee/[本体:注文]送料計算/{SHIPPING_FEE_CASE_NAME}",
                            SHIPPING_FEE_PERSPECTIVE_PROPERTIES,
                        )
                    ],
                ),
                id="機能の一覧が_区分本体に大機能注文を持ち_設定ファイルの言語Goのテスト結果に_テストTestShippingFee本体注文送料計算注文金額3000円で送料を計算すると_送料は無料になるで_種別単体テスト_正常異常正常系_観点境界値とエッジケース_When注文金額3000円で送料を計算する_Then送料は無料になるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの観点は境界値とエッジケースの_2_つになる",
            ),
            pytest.param(
                "機能の一覧が、区分「本体」に大機能「注文」を持ち、設定ファイルの言語「Dart」のテスト結果に、グループ「[本体:注文]送料計算」のテスト「注文金額3000円で送料を計算すると、送料は無料になる」で、種別「単体テスト」、正常異常「正常系」、観点「境界値」と「エッジケース」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持つケースがあるとき",
                lambda directory: write_dart_result(
                    directory,
                    [
                        (
                            SHIPPING_FEE_CASE_NAME,
                            spec_prints(SHIPPING_FEE_PERSPECTIVE_PROPERTIES),
                        )
                    ],
                    group_names=["[本体:注文]送料計算"],
                ),
                id="機能の一覧が_区分本体に大機能注文を持ち_設定ファイルの言語Dartのテスト結果に_グループ本体注文送料計算のテスト注文金額3000円で送料を計算すると_送料は無料になるで_種別単体テスト_正常異常正常系_観点境界値とエッジケース_When注文金額3000円で送料を計算する_Then送料は無料になるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの観点は境界値とエッジケースの_2_つになる",
            ),
            pytest.param(
                "機能の一覧が、区分「本体」に大機能「注文」を持ち、設定ファイルの言語「C#」のテスト結果に、Trait「区分・大機能・中機能・小機能」が「[本体:注文]送料計算」で、種別「単体テスト」、正常異常「正常系」、観点「境界値」と「エッジケース」、When「注文金額3000円で送料を計算する」、Then「送料は無料になる」を持つケースがあるとき",
                lambda directory: write_csharp_result(
                    directory,
                    [
                        (
                            SHIPPING_FEE_CASE_NAME,
                            (
                                CSHARP_ORDER_FEATURE_NAME,
                                *SHIPPING_FEE_PERSPECTIVE_PROPERTIES,
                            ),
                        )
                    ],
                ),
                id="機能の一覧が_区分本体に大機能注文を持ち_設定ファイルの言語Cのテスト結果に_Trait区分大機能中機能小機能が本体注文送料計算で_種別単体テスト_正常異常正常系_観点境界値とエッジケース_When注文金額3000円で送料を計算する_Then送料は無料になるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの観点は境界値とエッジケースの_2_つになる",
            ),
        ],
    )
    def test_extracts_perspectives_per_language(
        self, record_case, tmp_path, given, write_result
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", given),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "カタログに載るそのケースの観点は「境界値」と「エッジケース」の 2 つになる",
                ),
            ],
        )
        entry = write_result(tmp_path)
        config = build_config(tmp_path, [entry], FEATURES_ORDER)
        page = generate_catalog_page(tmp_path, config)
        assert page.catalog["cases"][0]["g"] == ["境界値", "エッジケース"]


class Test本体__テストケースカタログ__入力__言語ごとの環境の取り出し:
    @pytest.mark.parametrize(
        ("given", "write_result"),
        [
            pytest.param(
                "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持ち、設定ファイルの言語「Python」のテスト結果に、クラス名「tests.test_purchase.Testシナリオ__商品を購入する__通常の動線__ホーム画面から結果画面」で、種別「シナリオテスト」、正常異常「正常系」、環境「ローカル」、環境「dev環境」、When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」、Then:dev環境「英単語を含む英文が表示される」を持つケースがあるとき",
                lambda directory: write_python_result(
                    directory,
                    [
                        (
                            "tests.test_purchase.Testシナリオ__商品を購入する__通常の動線__ホーム画面から結果画面",
                            SCENARIO_PROPERTIES,
                        )
                    ],
                ),
                id="機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持ち_設定ファイルの言語Pythonのテスト結果に_クラス名teststest_purchaseTestシナリオ__商品を購入する__通常の動線__ホーム画面から結果画面で_種別シナリオテスト_正常異常正常系_環境ローカル_環境dev環境_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示される_Thendev環境英単語を含む英文が表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの環境はローカルdev環境になる",
            ),
            pytest.param(
                "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持ち、設定ファイルの言語「Kotlin」のテスト結果に、テストクラスの表示名が「[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面」で、種別「シナリオテスト」、正常異常「正常系」、環境「ローカル」、環境「dev環境」、When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」、Then:dev環境「英単語を含む英文が表示される」を持つケースがあるとき",
                lambda directory: write_kotlin_result(
                    directory,
                    [
                        (
                            "[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面",
                            SCENARIO_CASE_NAME,
                            SCENARIO_PROPERTIES,
                        )
                    ],
                ),
                id="機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持ち_設定ファイルの言語Kotlinのテスト結果に_テストクラスの表示名がシナリオ商品を購入する通常の動線ホーム画面から結果画面で_種別シナリオテスト_正常異常正常系_環境ローカル_環境dev環境_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示される_Thendev環境英単語を含む英文が表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの環境はローカルdev環境になる",
            ),
            pytest.param(
                "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持ち、設定ファイルの言語「Go」のテスト結果に、テスト「TestPurchase/[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面/ホーム画面で「探しに行く」を押すと、英文が表示される」で、種別「シナリオテスト」、正常異常「正常系」、環境「ローカル」、環境「dev環境」、When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」、Then:dev環境「英単語を含む英文が表示される」を持つケースがあるとき",
                lambda directory: write_go_result(
                    directory,
                    [
                        (
                            f"TestPurchase/[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面/{SCENARIO_CASE_NAME}",
                            SCENARIO_PROPERTIES,
                        )
                    ],
                ),
                id="機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持ち_設定ファイルの言語Goのテスト結果に_テストTestPurchaseシナリオ商品を購入する通常の動線ホーム画面から結果画面ホーム画面で探しに行くを押すと_英文が表示されるで_種別シナリオテスト_正常異常正常系_環境ローカル_環境dev環境_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示される_Thendev環境英単語を含む英文が表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの環境はローカルdev環境になる",
            ),
            pytest.param(
                "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持ち、設定ファイルの言語「Dart」のテスト結果に、グループ「[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面」のテスト「ホーム画面で「探しに行く」を押すと、英文が表示される」で、種別「シナリオテスト」、正常異常「正常系」、環境「ローカル」、環境「dev環境」、When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」、Then:dev環境「英単語を含む英文が表示される」を持つケースがあるとき",
                lambda directory: write_dart_result(
                    directory,
                    [(SCENARIO_CASE_NAME, spec_prints(SCENARIO_PROPERTIES))],
                    group_names=[
                        "[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面"
                    ],
                ),
                id="機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持ち_設定ファイルの言語Dartのテスト結果に_グループシナリオ商品を購入する通常の動線ホーム画面から結果画面のテストホーム画面で探しに行くを押すと_英文が表示されるで_種別シナリオテスト_正常異常正常系_環境ローカル_環境dev環境_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示される_Thendev環境英単語を含む英文が表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの環境はローカルdev環境になる",
            ),
            pytest.param(
                "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持ち、設定ファイルの言語「C#」のテスト結果に、Trait「区分・大機能・中機能・小機能」が「[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面」で、種別「シナリオテスト」、正常異常「正常系」、環境「ローカル」、環境「dev環境」、When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」、Then:dev環境「英単語を含む英文が表示される」を持つケースがあるとき",
                lambda directory: write_csharp_result(
                    directory,
                    [
                        (
                            SCENARIO_CASE_NAME,
                            (CSHARP_SCENARIO_FEATURE_NAME, *SCENARIO_PROPERTIES),
                        )
                    ],
                ),
                id="機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持ち_設定ファイルの言語Cのテスト結果に_Trait区分大機能中機能小機能がシナリオ商品を購入する通常の動線ホーム画面から結果画面で_種別シナリオテスト_正常異常正常系_環境ローカル_環境dev環境_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示される_Thendev環境英単語を含む英文が表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの環境はローカルdev環境になる",
            ),
            pytest.param(
                "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持ち、設定ファイルの言語「TypeScript」のテスト結果に、テスト名「[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面 > ホーム画面で「探しに行く」を押す」で、種別「シナリオテスト」、正常異常「正常系」、環境「ローカル」、環境「dev環境」、When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」、Then:dev環境「英単語を含む英文が表示される」を持つケースがあるとき",
                lambda directory: write_typescript_result(
                    directory, [(SCENARIO_TEST_NAME, SCENARIO_PROPERTIES)]
                ),
                id="機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持ち_設定ファイルの言語TypeScriptのテスト結果に_テスト名シナリオ商品を購入する通常の動線ホーム画面から結果画面__ホーム画面で探しに行くを押すで_種別シナリオテスト_正常異常正常系_環境ローカル_環境dev環境_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示される_Thendev環境英単語を含む英文が表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースの環境はローカルdev環境になる",
            ),
        ],
    )
    def test_extracts_environments_per_language(
        self, record_case, tmp_path, given, write_result
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", given),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "カタログに載るそのケースの環境は「ローカル」「dev環境」になる",
                ),
            ],
        )
        entry = write_result(tmp_path)
        config = build_config(tmp_path, [entry], FEATURES_SCENARIO)
        page = generate_catalog_page(tmp_path, config)
        assert page.catalog["cases"][0]["e"] == ["ローカル", "dev環境"]


class Test本体__テストケースカタログ__入力__言語ごとの環境ごとの_Then_の取り出し:
    @pytest.mark.parametrize(
        ("given", "write_result"),
        [
            pytest.param(
                "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持ち、設定ファイルの言語「Python」のテスト結果に、クラス名「tests.test_purchase.Testシナリオ__商品を購入する__通常の動線__ホーム画面から結果画面」で、種別「シナリオテスト」、正常異常「正常系」、環境「ローカル」、環境「dev環境」、When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」、Then:dev環境「英単語を含む英文が表示される」を持つケースがあるとき",
                lambda directory: write_python_result(
                    directory,
                    [
                        (
                            "tests.test_purchase.Testシナリオ__商品を購入する__通常の動線__ホーム画面から結果画面",
                            SCENARIO_PROPERTIES,
                        )
                    ],
                ),
                id="機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持ち_設定ファイルの言語Pythonのテスト結果に_クラス名teststest_purchaseTestシナリオ__商品を購入する__通常の動線__ホーム画面から結果画面で_種別シナリオテスト_正常異常正常系_環境ローカル_環境dev環境_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示される_Thendev環境英単語を含む英文が表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースのステップの環境ごとの_Then_は_ローカルが英文Helloが表示される_dev環境が英単語を含む英文が表示されるになる",
            ),
            pytest.param(
                "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持ち、設定ファイルの言語「Kotlin」のテスト結果に、テストクラスの表示名が「[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面」で、種別「シナリオテスト」、正常異常「正常系」、環境「ローカル」、環境「dev環境」、When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」、Then:dev環境「英単語を含む英文が表示される」を持つケースがあるとき",
                lambda directory: write_kotlin_result(
                    directory,
                    [
                        (
                            "[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面",
                            SCENARIO_CASE_NAME,
                            SCENARIO_PROPERTIES,
                        )
                    ],
                ),
                id="機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持ち_設定ファイルの言語Kotlinのテスト結果に_テストクラスの表示名がシナリオ商品を購入する通常の動線ホーム画面から結果画面で_種別シナリオテスト_正常異常正常系_環境ローカル_環境dev環境_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示される_Thendev環境英単語を含む英文が表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースのステップの環境ごとの_Then_は_ローカルが英文Helloが表示される_dev環境が英単語を含む英文が表示されるになる",
            ),
            pytest.param(
                "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持ち、設定ファイルの言語「Go」のテスト結果に、テスト「TestPurchase/[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面/ホーム画面で「探しに行く」を押すと、英文が表示される」で、種別「シナリオテスト」、正常異常「正常系」、環境「ローカル」、環境「dev環境」、When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」、Then:dev環境「英単語を含む英文が表示される」を持つケースがあるとき",
                lambda directory: write_go_result(
                    directory,
                    [
                        (
                            f"TestPurchase/[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面/{SCENARIO_CASE_NAME}",
                            SCENARIO_PROPERTIES,
                        )
                    ],
                ),
                id="機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持ち_設定ファイルの言語Goのテスト結果に_テストTestPurchaseシナリオ商品を購入する通常の動線ホーム画面から結果画面ホーム画面で探しに行くを押すと_英文が表示されるで_種別シナリオテスト_正常異常正常系_環境ローカル_環境dev環境_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示される_Thendev環境英単語を含む英文が表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースのステップの環境ごとの_Then_は_ローカルが英文Helloが表示される_dev環境が英単語を含む英文が表示されるになる",
            ),
            pytest.param(
                "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持ち、設定ファイルの言語「Dart」のテスト結果に、グループ「[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面」のテスト「ホーム画面で「探しに行く」を押すと、英文が表示される」で、種別「シナリオテスト」、正常異常「正常系」、環境「ローカル」、環境「dev環境」、When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」、Then:dev環境「英単語を含む英文が表示される」を持つケースがあるとき",
                lambda directory: write_dart_result(
                    directory,
                    [(SCENARIO_CASE_NAME, spec_prints(SCENARIO_PROPERTIES))],
                    group_names=[
                        "[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面"
                    ],
                ),
                id="機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持ち_設定ファイルの言語Dartのテスト結果に_グループシナリオ商品を購入する通常の動線ホーム画面から結果画面のテストホーム画面で探しに行くを押すと_英文が表示されるで_種別シナリオテスト_正常異常正常系_環境ローカル_環境dev環境_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示される_Thendev環境英単語を含む英文が表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースのステップの環境ごとの_Then_は_ローカルが英文Helloが表示される_dev環境が英単語を含む英文が表示されるになる",
            ),
            pytest.param(
                "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持ち、設定ファイルの言語「C#」のテスト結果に、Trait「区分・大機能・中機能・小機能」が「[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面」で、種別「シナリオテスト」、正常異常「正常系」、環境「ローカル」、環境「dev環境」、When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」、Then:dev環境「英単語を含む英文が表示される」を持つケースがあるとき",
                lambda directory: write_csharp_result(
                    directory,
                    [
                        (
                            SCENARIO_CASE_NAME,
                            (CSHARP_SCENARIO_FEATURE_NAME, *SCENARIO_PROPERTIES),
                        )
                    ],
                ),
                id="機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持ち_設定ファイルの言語Cのテスト結果に_Trait区分大機能中機能小機能がシナリオ商品を購入する通常の動線ホーム画面から結果画面で_種別シナリオテスト_正常異常正常系_環境ローカル_環境dev環境_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示される_Thendev環境英単語を含む英文が表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースのステップの環境ごとの_Then_は_ローカルが英文Helloが表示される_dev環境が英単語を含む英文が表示されるになる",
            ),
            pytest.param(
                "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持ち、設定ファイルの言語「TypeScript」のテスト結果に、テスト名「[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面 > ホーム画面で「探しに行く」を押す」で、種別「シナリオテスト」、正常異常「正常系」、環境「ローカル」、環境「dev環境」、When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」、Then:dev環境「英単語を含む英文が表示される」を持つケースがあるとき",
                lambda directory: write_typescript_result(
                    directory, [(SCENARIO_TEST_NAME, SCENARIO_PROPERTIES)]
                ),
                id="機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持ち_設定ファイルの言語TypeScriptのテスト結果に_テスト名シナリオ商品を購入する通常の動線ホーム画面から結果画面__ホーム画面で探しに行くを押すで_種別シナリオテスト_正常異常正常系_環境ローカル_環境dev環境_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示される_Thendev環境英単語を含む英文が表示されるを持つケースがあるとき_設定ファイルを渡して生成コマンドを実行すると_カタログに載るそのケースのステップの環境ごとの_Then_は_ローカルが英文Helloが表示される_dev環境が英単語を含む英文が表示されるになる",
            ),
        ],
    )
    def test_extracts_environment_thens_per_language(
        self, record_case, tmp_path, given, write_result
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", given),
                ("When", "設定ファイルを渡して生成コマンドを実行する"),
                (
                    "Then",
                    "カタログに載るそのケースのステップの環境ごとの Then は、ローカルが「英文「Hello.」が表示される」、dev環境が「英単語を含む英文が表示される」になる",
                ),
            ],
        )
        entry = write_result(tmp_path)
        config = build_config(tmp_path, [entry], FEATURES_SCENARIO)
        page = generate_catalog_page(tmp_path, config)
        assert page.catalog["cases"][0]["steps"][0]["E"] == [
            ["ローカル", "英文「Hello.」が表示される"],
            ["dev環境", "英単語を含む英文が表示される"],
        ]


class Test本体__テストケースカタログ__入力__環境ごとの_Then_の読み取り:
    def test_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示される_Thendev環境英単語を含む英文が表示されるの順に並ぶ項目から_ステップを読み取ると_読み取ったステップは_Whenホーム画面で探しに行くを押す_Then_なし_環境ごとの_Then_はローカルが英文Helloが表示される_dev環境が英単語を含む英文が表示されるの_1_つになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "When",
                    "When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」、Then:dev環境「英単語を含む英文が表示される」の順に並ぶ項目から、ステップを読み取る",
                ),
                (
                    "Then",
                    "読み取ったステップは、When「ホーム画面で「探しに行く」を押す」、Then なし、環境ごとの Then はローカルが「英文「Hello.」が表示される」、dev環境が「英単語を含む英文が表示される」の 1 つになる",
                ),
            ],
        )
        steps = catalog.read_steps(
            [
                ("When", "ホーム画面で「探しに行く」を押す"),
                ("Then:ローカル", "英文「Hello.」が表示される"),
                ("Then:dev環境", "英単語を含む英文が表示される"),
            ]
        )
        assert steps == [
            {
                "given": None,
                "whens": ["ホーム画面で「探しに行く」を押す"],
                "then": None,
                "environment_thens": [
                    ("ローカル", "英文「Hello.」が表示される"),
                    ("dev環境", "英単語を含む英文が表示される"),
                ],
            }
        ]

    def test_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示される_Thendev環境英単語を含む英文が表示される_When結果画面でもう一度を押す_Then新しい出題の英文が表示されるの順に並ぶ項目から_ステップを読み取ると_読み取ったステップは_1_つ目が_Whenホーム画面で探しに行くを押す_環境ごとの_Then_はローカルが英文Helloが表示される_dev環境が英単語を含む英文が表示される_2_つ目が_When結果画面でもう一度を押す_Then新しい出題の英文が表示されるの_2_つになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "When",
                    "When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」、Then:dev環境「英単語を含む英文が表示される」、When「結果画面で「もう一度」を押す」、Then「新しい出題の英文が表示される」の順に並ぶ項目から、ステップを読み取る",
                ),
                (
                    "Then",
                    "読み取ったステップは、1 つ目が When「ホーム画面で「探しに行く」を押す」、環境ごとの Then はローカルが「英文「Hello.」が表示される」、dev環境が「英単語を含む英文が表示される」、2 つ目が When「結果画面で「もう一度」を押す」、Then「新しい出題の英文が表示される」の 2 つになる",
                ),
            ],
        )
        steps = catalog.read_steps(
            [
                ("When", "ホーム画面で「探しに行く」を押す"),
                ("Then:ローカル", "英文「Hello.」が表示される"),
                ("Then:dev環境", "英単語を含む英文が表示される"),
                ("When", "結果画面で「もう一度」を押す"),
                ("Then", "新しい出題の英文が表示される"),
            ]
        )
        assert steps == [
            {
                "given": None,
                "whens": ["ホーム画面で「探しに行く」を押す"],
                "then": None,
                "environment_thens": [
                    ("ローカル", "英文「Hello.」が表示される"),
                    ("dev環境", "英単語を含む英文が表示される"),
                ],
            },
            {
                "given": None,
                "whens": ["結果画面で「もう一度」を押す"],
                "then": "新しい出題の英文が表示される",
                "environment_thens": [],
            },
        ]

    def test_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示される_Then出題の英文が表示されるの順に並ぶ項目から_ステップを読み取ると_同じステップに_Then_と環境ごとの_Then_が混ざっていることを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "When",
                    "When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」、Then「出題の英文が表示される」の順に並ぶ項目から、ステップを読み取る",
                ),
                (
                    "Then",
                    "同じステップに Then と環境ごとの Then が混ざっていることを示すエラーになる",
                ),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_steps(
                [
                    ("When", "ホーム画面で「探しに行く」を押す"),
                    ("Then:ローカル", "英文「Hello.」が表示される"),
                    ("Then", "出題の英文が表示される"),
                ]
            )
        assert_message_contains(
            error.value, "同じステップに Then と環境ごとの Then が混ざっている"
        )

    def test_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示される_Thenローカル別の英文が表示されるの順に並ぶ項目から_ステップを読み取ると_同じステップに環境ローカルの_Then_が_2_つあることを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "When",
                    "When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」、Then:ローカル「別の英文が表示される」の順に並ぶ項目から、ステップを読み取る",
                ),
                (
                    "Then",
                    "同じステップに環境「ローカル」の Then が 2 つあることを示すエラーになる",
                ),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_steps(
                [
                    ("When", "ホーム画面で「探しに行く」を押す"),
                    ("Then:ローカル", "英文「Hello.」が表示される"),
                    ("Then:ローカル", "別の英文が表示される"),
                ]
            )
        assert_message_contains(
            error.value, "同じステップに環境「ローカル」の Then が 2 つある"
        )

    def test_Whenホーム画面で探しに行くを押す_Then本番出題の英文が表示されるの順に並ぶ項目から_ステップを読み取ると_環境本番がローカルdev環境のいずれでもないことを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "When",
                    "When「ホーム画面で「探しに行く」を押す」、Then:本番「出題の英文が表示される」の順に並ぶ項目から、ステップを読み取る",
                ),
                (
                    "Then",
                    "環境「本番」がローカル・dev環境のいずれでもないことを示すエラーになる",
                ),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_steps(
                [
                    ("When", "ホーム画面で「探しに行く」を押す"),
                    ("Then:本番", "出題の英文が表示される"),
                ]
            )
        assert_message_contains(
            error.value, "環境「本番」", "ローカル・dev環境のいずれでもない"
        )

    def test_Thenローカル英文Helloが表示されるだけが並ぶ項目から_ステップを読み取ると_When_の無い_Then_があることを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "When",
                    "Then:ローカル「英文「Hello.」が表示される」だけが並ぶ項目から、ステップを読み取る",
                ),
                ("Then", "When の無い Then があることを示すエラーになる"),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_steps([("Then:ローカル", "英文「Hello.」が表示される")])
        assert_message_contains(error.value, "When の無い Then")

    def test_機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持つとき_テスト名シナリオ商品を購入する通常の動線ホーム画面から結果画面__ホーム画面で探しに行くを押すで_種別シナリオテスト_正常異常正常系_環境dev環境_環境ローカル_Givenログインしているとき_Whenホーム画面で探しに行くを押す_Thendev環境英単語を含む英文が表示される_Thenローカル英文Helloが表示されるを持つケースを読み取ると_読み取ったケースのステップの環境ごとの_Then_は_ローカルが英文Helloが表示される_dev環境が英単語を含む英文が表示されるの順になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持つとき",
                ),
                (
                    "When",
                    "テスト名「[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面 > ホーム画面で「探しに行く」を押す」で、種別「シナリオテスト」、正常異常「正常系」、環境「dev環境」、環境「ローカル」、Given「ログインしているとき」、When「ホーム画面で「探しに行く」を押す」、Then:dev環境「英単語を含む英文が表示される」、Then:ローカル「英文「Hello.」が表示される」を持つケースを読み取る",
                ),
                (
                    "Then",
                    "読み取ったケースのステップの環境ごとの Then は、ローカルが「英文「Hello.」が表示される」、dev環境が「英単語を含む英文が表示される」の順になる",
                ),
            ],
        )
        case = catalog.read_typescript_case(
            SCENARIO_TEST_NAME,
            (
                ("種別", "シナリオテスト"),
                ("正常異常", "正常系"),
                ("環境", "dev環境"),
                ("環境", "ローカル"),
                ("Given", "ログインしているとき"),
                ("When", "ホーム画面で「探しに行く」を押す"),
                ("Then:dev環境", "英単語を含む英文が表示される"),
                ("Then:ローカル", "英文「Hello.」が表示される"),
            ),
            FEATURES_SCENARIO,
        )
        assert case["steps"][0]["environment_thens"] == [
            ("ローカル", "英文「Hello.」が表示される"),
            ("dev環境", "英単語を含む英文が表示される"),
        ]

    def test_機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持つとき_テスト名シナリオ商品を購入する通常の動線ホーム画面から結果画面__ホーム画面で探しに行くを押すで_種別シナリオテスト_正常異常正常系_環境ローカル_環境dev環境_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示される_Thendev環境英文Helloが表示されるを持つケースを読み取ると_環境ごとの_Then_が同じ内容なので_Then_を_1_つにするよう示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持つとき",
                ),
                (
                    "When",
                    "テスト名「[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面 > ホーム画面で「探しに行く」を押す」で、種別「シナリオテスト」、正常異常「正常系」、環境「ローカル」、環境「dev環境」、When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」、Then:dev環境「英文「Hello.」が表示される」を持つケースを読み取る",
                ),
                (
                    "Then",
                    "環境ごとの Then が同じ内容なので Then を 1 つにするよう示すエラーになる",
                ),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_typescript_case(
                SCENARIO_TEST_NAME,
                (
                    ("種別", "シナリオテスト"),
                    ("正常異常", "正常系"),
                    ("環境", "ローカル"),
                    ("環境", "dev環境"),
                    ("When", "ホーム画面で「探しに行く」を押す"),
                    ("Then:ローカル", "英文「Hello.」が表示される"),
                    ("Then:dev環境", "英文「Hello.」が表示される"),
                ),
                FEATURES_SCENARIO,
            )
        assert_message_contains(
            error.value, "環境ごとの Then が同じ内容", "Then を 1 つにする"
        )

    def test_機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持つとき_テスト名シナリオ商品を購入する通常の動線ホーム画面から結果画面__ホーム画面で探しに行くを押すで_種別シナリオテスト_正常異常正常系_環境ローカル_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示される_Thendev環境英単語を含む英文が表示されるを持つケースを読み取ると_環境ごとの_Then_の環境が_ケースの環境と一致しないことを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持つとき",
                ),
                (
                    "When",
                    "テスト名「[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面 > ホーム画面で「探しに行く」を押す」で、種別「シナリオテスト」、正常異常「正常系」、環境「ローカル」、When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」、Then:dev環境「英単語を含む英文が表示される」を持つケースを読み取る",
                ),
                (
                    "Then",
                    "環境ごとの Then の環境が、ケースの環境と一致しないことを示すエラーになる",
                ),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_typescript_case(
                SCENARIO_TEST_NAME,
                (
                    ("種別", "シナリオテスト"),
                    ("正常異常", "正常系"),
                    ("環境", "ローカル"),
                    ("When", "ホーム画面で「探しに行く」を押す"),
                    ("Then:ローカル", "英文「Hello.」が表示される"),
                    ("Then:dev環境", "英単語を含む英文が表示される"),
                ),
                FEATURES_SCENARIO,
            )
        assert_message_contains(
            error.value, "環境ごとの Then の環境が、ケースの環境と一致しない"
        )

    def test_機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持つとき_テスト名シナリオ商品を購入する通常の動線ホーム画面から結果画面__ホーム画面で探しに行くを押すで_種別シナリオテスト_正常異常正常系_環境ローカル_環境dev環境_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示されるを持つケースを読み取ると_環境ごとの_Then_の環境が_ケースの環境と一致しないことを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持つとき",
                ),
                (
                    "When",
                    "テスト名「[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面 > ホーム画面で「探しに行く」を押す」で、種別「シナリオテスト」、正常異常「正常系」、環境「ローカル」、環境「dev環境」、When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」を持つケースを読み取る",
                ),
                (
                    "Then",
                    "環境ごとの Then の環境が、ケースの環境と一致しないことを示すエラーになる",
                ),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_typescript_case(
                SCENARIO_TEST_NAME,
                (
                    ("種別", "シナリオテスト"),
                    ("正常異常", "正常系"),
                    ("環境", "ローカル"),
                    ("環境", "dev環境"),
                    ("When", "ホーム画面で「探しに行く」を押す"),
                    ("Then:ローカル", "英文「Hello.」が表示される"),
                ),
                FEATURES_SCENARIO,
            )
        assert_message_contains(
            error.value, "環境ごとの Then の環境が、ケースの環境と一致しない"
        )

    def test_機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持つとき_テスト名シナリオ商品を購入する通常の動線ホーム画面から結果画面__ホーム画面で探しに行くを押すで_種別シナリオテスト_正常異常正常系_環境ローカル_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示されるを持つケースを読み取ると_環境ごとの_Then_は_2_つ以上の環境で書くよう示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            perspectives=["境界値"],
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持つとき",
                ),
                (
                    "When",
                    "テスト名「[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面 > ホーム画面で「探しに行く」を押す」で、種別「シナリオテスト」、正常異常「正常系」、環境「ローカル」、When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」を持つケースを読み取る",
                ),
                ("Then", "環境ごとの Then は 2 つ以上の環境で書くよう示すエラーになる"),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_typescript_case(
                SCENARIO_TEST_NAME,
                (
                    ("種別", "シナリオテスト"),
                    ("正常異常", "正常系"),
                    ("環境", "ローカル"),
                    ("When", "ホーム画面で「探しに行く」を押す"),
                    ("Then:ローカル", "英文「Hello.」が表示される"),
                ),
                FEATURES_SCENARIO,
            )
        assert_message_contains(error.value, "環境ごとの Then は 2 つ以上の環境で書く")

    def test_機能の一覧が_区分本体に大機能認証を持つとき_テスト名本体認証ログイン__未確認のアカウントでログインすると_確認を促すメッセージが表示されるで_種別単体テスト_正常異常正常系_Whenホーム画面で探しに行くを押す_Thenローカル英文Helloが表示される_Thendev環境英単語を含む英文が表示されるを持つケースを読み取ると_環境ごとの_Then_はシナリオテストだけに書けることを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                ("Given", "機能の一覧が、区分「本体」に大機能「認証」を持つとき"),
                (
                    "When",
                    "テスト名「[本体:認証]ログイン > 未確認のアカウントでログインすると、確認を促すメッセージが表示される」で、種別「単体テスト」、正常異常「正常系」、When「ホーム画面で「探しに行く」を押す」、Then:ローカル「英文「Hello.」が表示される」、Then:dev環境「英単語を含む英文が表示される」を持つケースを読み取る",
                ),
                (
                    "Then",
                    "環境ごとの Then はシナリオテストだけに書けることを示すエラーになる",
                ),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_typescript_case(
                LOGIN_TEST_NAME,
                (
                    ("種別", "単体テスト"),
                    ("正常異常", "正常系"),
                    ("When", "ホーム画面で「探しに行く」を押す"),
                    ("Then:ローカル", "英文「Hello.」が表示される"),
                    ("Then:dev環境", "英単語を含む英文が表示される"),
                ),
                FEATURES_AUTH,
            )
        assert_message_contains(
            error.value, "環境ごとの Then はシナリオテストだけに書ける"
        )


class Test本体__テストケースカタログ__入力__環境の読み取り:
    def test_機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持つとき_テスト名シナリオ商品を購入する通常の動線ホーム画面から結果画面__ホーム画面で探しに行くを押すで_種別シナリオテスト_正常異常正常系_環境dev環境_環境ローカル_Givenログインしているとき_Whenホーム画面で探しに行くを押す_Thendev環境英単語を含む英文が表示される_Thenローカル英文Helloが表示されるを持つケースを読み取ると_読み取ったケースの環境はローカルdev環境の順になる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持つとき",
                ),
                (
                    "When",
                    "テスト名「[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面 > ホーム画面で「探しに行く」を押す」で、種別「シナリオテスト」、正常異常「正常系」、環境「dev環境」、環境「ローカル」、Given「ログインしているとき」、When「ホーム画面で「探しに行く」を押す」、Then:dev環境「英単語を含む英文が表示される」、Then:ローカル「英文「Hello.」が表示される」を持つケースを読み取る",
                ),
                ("Then", "読み取ったケースの環境は「ローカル」「dev環境」の順になる"),
            ],
        )
        case = catalog.read_typescript_case(
            SCENARIO_TEST_NAME,
            (
                ("種別", "シナリオテスト"),
                ("正常異常", "正常系"),
                ("環境", "dev環境"),
                ("環境", "ローカル"),
                ("Given", "ログインしているとき"),
                ("When", "ホーム画面で「探しに行く」を押す"),
                ("Then:dev環境", "英単語を含む英文が表示される"),
                ("Then:ローカル", "英文「Hello.」が表示される"),
            ),
            FEATURES_SCENARIO,
        )
        assert case["environments"] == ["ローカル", "dev環境"]

    def test_機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持つとき_テスト名シナリオ商品を購入する通常の動線ホーム画面から結果画面__ホーム画面で探しに行くを押すで_種別シナリオテスト_正常異常正常系_環境ローカル_Whenホーム画面で探しに行くを押す_Then出題の英文が表示されるを持つケースを読み取ると_読み取ったケースの環境はローカルの_1_つになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="正常系",
            perspectives=["件数・有無"],
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持つとき",
                ),
                (
                    "When",
                    "テスト名「[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面 > ホーム画面で「探しに行く」を押す」で、種別「シナリオテスト」、正常異常「正常系」、環境「ローカル」、When「ホーム画面で「探しに行く」を押す」、Then「出題の英文が表示される」を持つケースを読み取る",
                ),
                ("Then", "読み取ったケースの環境は「ローカル」の 1 つになる"),
            ],
        )
        case = catalog.read_typescript_case(
            SCENARIO_TEST_NAME,
            (
                ("種別", "シナリオテスト"),
                ("正常異常", "正常系"),
                ("環境", "ローカル"),
                ("When", "ホーム画面で「探しに行く」を押す"),
                ("Then", "出題の英文が表示される"),
            ),
            FEATURES_SCENARIO,
        )
        assert case["environments"] == ["ローカル"]

    def test_機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持つとき_テスト名シナリオ商品を購入する通常の動線ホーム画面から結果画面__ホーム画面で探しに行くを押すで_種別単体テスト_正常異常正常系_環境ローカル_Whenホーム画面で探しに行くを押す_Then出題の英文が表示されるを持つケースを読み取ると_環境はシナリオテストだけが持つことを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持つとき",
                ),
                (
                    "When",
                    "テスト名「[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面 > ホーム画面で「探しに行く」を押す」で、種別「単体テスト」、正常異常「正常系」、環境「ローカル」、When「ホーム画面で「探しに行く」を押す」、Then「出題の英文が表示される」を持つケースを読み取る",
                ),
                ("Then", "環境はシナリオテストだけが持つことを示すエラーになる"),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_typescript_case(
                SCENARIO_TEST_NAME,
                (
                    ("種別", "単体テスト"),
                    ("正常異常", "正常系"),
                    ("環境", "ローカル"),
                    ("When", "ホーム画面で「探しに行く」を押す"),
                    ("Then", "出題の英文が表示される"),
                ),
                FEATURES_SCENARIO,
            )
        assert_message_contains(error.value, "環境はシナリオテストだけが持つ")

    def test_機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持つとき_テスト名シナリオ商品を購入する通常の動線ホーム画面から結果画面__ホーム画面で探しに行くを押すで_種別シナリオテスト_正常異常正常系_Whenホーム画面で探しに行くを押す_Then出題の英文が表示されるを持ち_環境を持たないケースを読み取ると_シナリオテストには環境が必要であることを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            perspectives=["件数・有無"],
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持つとき",
                ),
                (
                    "When",
                    "テスト名「[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面 > ホーム画面で「探しに行く」を押す」で、種別「シナリオテスト」、正常異常「正常系」、When「ホーム画面で「探しに行く」を押す」、Then「出題の英文が表示される」を持ち、環境を持たないケースを読み取る",
                ),
                ("Then", "シナリオテストには環境が必要であることを示すエラーになる"),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_typescript_case(
                SCENARIO_TEST_NAME,
                (
                    ("種別", "シナリオテスト"),
                    ("正常異常", "正常系"),
                    ("When", "ホーム画面で「探しに行く」を押す"),
                    ("Then", "出題の英文が表示される"),
                ),
                FEATURES_SCENARIO,
            )
        assert_message_contains(error.value, "シナリオテストには環境が必要")

    def test_機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持つとき_テスト名シナリオ商品を購入する通常の動線ホーム画面から結果画面__ホーム画面で探しに行くを押すで_種別シナリオテスト_正常異常正常系_環境ローカル_環境ローカル_Whenホーム画面で探しに行くを押す_Then出題の英文が表示されるを持つケースを読み取ると_環境が重複していることを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持つとき",
                ),
                (
                    "When",
                    "テスト名「[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面 > ホーム画面で「探しに行く」を押す」で、種別「シナリオテスト」、正常異常「正常系」、環境「ローカル」、環境「ローカル」、When「ホーム画面で「探しに行く」を押す」、Then「出題の英文が表示される」を持つケースを読み取る",
                ),
                ("Then", "環境が重複していることを示すエラーになる"),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_typescript_case(
                SCENARIO_TEST_NAME,
                (
                    ("種別", "シナリオテスト"),
                    ("正常異常", "正常系"),
                    ("環境", "ローカル"),
                    ("環境", "ローカル"),
                    ("When", "ホーム画面で「探しに行く」を押す"),
                    ("Then", "出題の英文が表示される"),
                ),
                FEATURES_SCENARIO,
            )
        assert_message_contains(error.value, "環境が重複している")

    def test_機能の一覧が_区分シナリオに大機能商品を購入すると中機能通常の動線を持つとき_テスト名シナリオ商品を購入する通常の動線ホーム画面から結果画面__ホーム画面で探しに行くを押すで_種別シナリオテスト_正常異常正常系_環境本番_Whenホーム画面で探しに行くを押す_Then出題の英文が表示されるを持つケースを読み取ると_環境本番がローカルdev環境のいずれでもないことを示すエラーになる(
        self, record_case
    ):
        record_case(
            kind="単体テスト",
            normal_or_abnormal="異常系",
            items=[
                (
                    "Given",
                    "機能の一覧が、区分「シナリオ」に大機能「商品を購入する」と中機能「通常の動線」を持つとき",
                ),
                (
                    "When",
                    "テスト名「[シナリオ:商品を購入する:通常の動線]ホーム画面から結果画面 > ホーム画面で「探しに行く」を押す」で、種別「シナリオテスト」、正常異常「正常系」、環境「本番」、When「ホーム画面で「探しに行く」を押す」、Then「出題の英文が表示される」を持つケースを読み取る",
                ),
                (
                    "Then",
                    "環境「本番」がローカル・dev環境のいずれでもないことを示すエラーになる",
                ),
            ],
        )
        with pytest.raises(catalog.CatalogError) as error:
            catalog.read_typescript_case(
                SCENARIO_TEST_NAME,
                (
                    ("種別", "シナリオテスト"),
                    ("正常異常", "正常系"),
                    ("環境", "本番"),
                    ("When", "ホーム画面で「探しに行く」を押す"),
                    ("Then", "出題の英文が表示される"),
                ),
                FEATURES_SCENARIO,
            )
        assert_message_contains(
            error.value, "環境「本番」", "ローカル・dev環境のいずれでもない"
        )
