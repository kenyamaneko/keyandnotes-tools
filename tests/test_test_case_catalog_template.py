import pytest
from catalog_browser_support import (
    DEFAULT_VIEWPORT_HEIGHT,
    DEFAULT_VIEWPORT_WIDTH,
    assert_no_major_is_highlighted,
    assert_only_major_is_highlighted,
    assert_toc_link_is_visible_in_toc,
    build_catalog_html,
    locate_catalog_header,
    locate_toc_link,
    scroll_until_major_header_is_below_catalog_header,
    wait_until_scroll_stops,
    write_catalog_html,
)
from playwright.sync_api import sync_playwright

MAJORS_ORDER_MEMBER_STOCK = ["注文", "会員", "在庫"]
MAJORS_OF_TWELVE = [
    "注文",
    "会員",
    "在庫",
    "決済",
    "配送",
    "返品",
    "クーポン",
    "ポイント",
    "レビュー",
    "通知",
    "検索",
    "お気に入り",
]
FEATURE_COUNT_PER_MAJOR = 10
TALL_VIEWPORT_HEIGHT = 800
SHORT_VIEWPORT_HEIGHT = 300
GIVEN_THREE_MAJORS = (
    "テストケースカタログに区分「本体」の大機能「注文」「会員」「在庫」があるとき"
)
GIVEN_THREE_MAJORS_WITH_FEATURES = "ブラウザのウィンドウが幅 1280 px・高さ 800 px で、テストケースカタログに区分「本体」の大機能「注文」「会員」「在庫」があり、各大機能に小機能が 10 個ずつあるとき"
GIVEN_ABNORMAL_MAJORS = "テストケースカタログに区分「本体」の大機能「注文」「会員」「在庫」があり、「注文」は正常系のケースだけを持ち、「会員」と「在庫」は異常系のケースを持つとき"
GIVEN_NORMAL_ONLY_MAJORS = "テストケースカタログに区分「本体」の大機能「注文」「会員」「在庫」があり、すべての大機能が正常系のケースだけを持つとき"
GIVEN_TWELVE_MAJORS = "ブラウザのウィンドウが幅 1280 px・高さ 300 px で、テストケースカタログに区分「本体」の大機能「注文」「会員」「在庫」「決済」「配送」「返品」「クーポン」「ポイント」「レビュー」「通知」「検索」「お気に入り」があり、各大機能に小機能が 10 個ずつあるとき"
WHEN_PREFIX = "テストケースカタログの画面の目次の現在位置のハイライトで、"


@pytest.fixture(scope="module")
def chromium():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        yield browser
        browser.close()


@pytest.fixture
def open_catalog_page(chromium, tmp_path):
    pages = []

    def open_page(html, width=DEFAULT_VIEWPORT_WIDTH, height=DEFAULT_VIEWPORT_HEIGHT):
        path = write_catalog_html(tmp_path, html)
        page = chromium.new_page(viewport={"width": width, "height": height})
        pages.append(page)
        page.goto(path.as_uri())
        return page

    yield open_page
    for page in pages:
        page.close()


class Test本体__テストケースカタログ__画面表示__開いた直後のハイライト:
    def test_テストケースカタログに区分本体の大機能注文会員在庫があるとき_テストケースカタログの画面の目次の現在位置のハイライトで_画面を開くと_目次でハイライトされている大機能は注文の_1_つだけになる(
        self, record_case, tmp_path, open_catalog_page
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", GIVEN_THREE_MAJORS),
                ("When", WHEN_PREFIX + "画面を開く"),
                ("Then", "目次でハイライトされている大機能は『注文』の 1 つだけになる"),
            ],
        )
        html = build_catalog_html(tmp_path, MAJORS_ORDER_MEMBER_STOCK)
        page = open_catalog_page(html)
        assert_only_major_is_highlighted(page, "注文")


class Test本体__テストケースカタログ__画面表示__スクロールに合わせたハイライトの移動:
    def test_ブラウザのウィンドウが幅_1280_px高さ_800_px_で_テストケースカタログに区分本体の大機能注文会員在庫があり_各大機能に小機能が_10_個ずつあるとき_テストケースカタログの画面の目次の現在位置のハイライトで_画面を大機能会員の表ヘッダーがカタログヘッダーの直下に来るまでスクロールすると_目次でハイライトされている大機能は会員の_1_つだけになる(
        self, record_case, tmp_path, open_catalog_page
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", GIVEN_THREE_MAJORS_WITH_FEATURES),
                (
                    "When",
                    WHEN_PREFIX
                    + "画面を大機能『会員』の表ヘッダーがカタログヘッダーの直下に来るまでスクロールする",
                ),
                ("Then", "目次でハイライトされている大機能は『会員』の 1 つだけになる"),
            ],
        )
        html = build_catalog_html(
            tmp_path, MAJORS_ORDER_MEMBER_STOCK, feature_count=FEATURE_COUNT_PER_MAJOR
        )
        page = open_catalog_page(html, height=TALL_VIEWPORT_HEIGHT)
        scroll_until_major_header_is_below_catalog_header(page, "会員")
        assert_only_major_is_highlighted(page, "会員")

    def test_ブラウザのウィンドウが幅_1280_px高さ_800_px_で_テストケースカタログに区分本体の大機能注文会員在庫があり_各大機能に小機能が_10_個ずつあるとき_テストケースカタログの画面の目次の現在位置のハイライトで_画面を大機能在庫の表ヘッダーがカタログヘッダーの直下に来るまでスクロールすると_目次でハイライトされている大機能は在庫の_1_つだけになる(
        self, record_case, tmp_path, open_catalog_page
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", GIVEN_THREE_MAJORS_WITH_FEATURES),
                (
                    "When",
                    WHEN_PREFIX
                    + "画面を大機能『在庫』の表ヘッダーがカタログヘッダーの直下に来るまでスクロールする",
                ),
                ("Then", "目次でハイライトされている大機能は『在庫』の 1 つだけになる"),
            ],
        )
        html = build_catalog_html(
            tmp_path, MAJORS_ORDER_MEMBER_STOCK, feature_count=FEATURE_COUNT_PER_MAJOR
        )
        page = open_catalog_page(html, height=TALL_VIEWPORT_HEIGHT)
        scroll_until_major_header_is_below_catalog_header(page, "在庫")
        assert_only_major_is_highlighted(page, "在庫")


class Test本体__テストケースカタログ__画面表示__目次の大機能を押したときのハイライト:
    def test_ブラウザのウィンドウが幅_1280_px高さ_800_px_で_テストケースカタログに区分本体の大機能注文会員在庫があり_各大機能に小機能が_10_個ずつあるとき_テストケースカタログの画面の目次の現在位置のハイライトで_目次の在庫を押す_スクロールが止まるまで待つと_目次でハイライトされている大機能は在庫の_1_つだけになる(
        self, record_case, tmp_path, open_catalog_page
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", GIVEN_THREE_MAJORS_WITH_FEATURES),
                ("When", WHEN_PREFIX + "目次の『在庫』を押す"),
                ("When", "スクロールが止まるまで待つ"),
                ("Then", "目次でハイライトされている大機能は『在庫』の 1 つだけになる"),
            ],
        )
        html = build_catalog_html(
            tmp_path, MAJORS_ORDER_MEMBER_STOCK, feature_count=FEATURE_COUNT_PER_MAJOR
        )
        page = open_catalog_page(html, height=TALL_VIEWPORT_HEIGHT)
        locate_toc_link(page, "在庫").click()
        wait_until_scroll_stops(page)
        assert_only_major_is_highlighted(page, "在庫")


class Test本体__テストケースカタログ__画面表示__フィルターに合わせたハイライトの更新:
    def test_テストケースカタログに区分本体の大機能注文会員在庫があり_注文は正常系のケースだけを持ち_会員と在庫は異常系のケースを持つとき_テストケースカタログの画面の目次の現在位置のハイライトで_カタログヘッダーの正常異常の異常系を押すと_目次でハイライトされている大機能は会員の_1_つだけになる(
        self, record_case, tmp_path, open_catalog_page
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", GIVEN_ABNORMAL_MAJORS),
                (
                    "When",
                    WHEN_PREFIX + "カタログヘッダーの正常異常の『異常系』を押す",
                ),
                ("Then", "目次でハイライトされている大機能は『会員』の 1 つだけになる"),
            ],
        )
        html = build_catalog_html(
            tmp_path, MAJORS_ORDER_MEMBER_STOCK, abnormal_majors=["会員", "在庫"]
        )
        page = open_catalog_page(html)
        locate_catalog_header(page).get_by_role(
            "button", name="異常系", exact=True
        ).click()
        assert_only_major_is_highlighted(page, "会員")


class Test本体__テストケースカタログ__画面表示__ハイライトされた大機能の目次内での表示:
    def test_ブラウザのウィンドウが幅_1280_px高さ_300_px_で_テストケースカタログに区分本体の大機能注文会員在庫決済配送返品クーポンポイントレビュー通知検索お気に入りがあり_各大機能に小機能が_10_個ずつあるとき_テストケースカタログの画面の目次の現在位置のハイライトで_画面を大機能お気に入りの表ヘッダーがカタログヘッダーの直下に来るまでスクロールすると_目次のお気に入りが_目次の表示範囲内に見える(
        self, record_case, tmp_path, open_catalog_page
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="正常系",
            items=[
                ("Given", GIVEN_TWELVE_MAJORS),
                (
                    "When",
                    WHEN_PREFIX
                    + "画面を大機能『お気に入り』の表ヘッダーがカタログヘッダーの直下に来るまでスクロールする",
                ),
                ("Then", "目次の『お気に入り』が、目次の表示範囲内に見える"),
            ],
        )
        html = build_catalog_html(
            tmp_path, MAJORS_OF_TWELVE, feature_count=FEATURE_COUNT_PER_MAJOR
        )
        page = open_catalog_page(html, height=SHORT_VIEWPORT_HEIGHT)
        scroll_until_major_header_is_below_catalog_header(page, "お気に入り")
        assert_toc_link_is_visible_in_toc(page, "お気に入り")


class Test本体__テストケースカタログ__画面表示__全ケースが表示されないときのハイライト:
    def test_テストケースカタログに区分本体の大機能注文会員在庫があり_すべての大機能が正常系のケースだけを持つとき_テストケースカタログの画面の目次の現在位置のハイライトで_カタログヘッダーの正常異常の異常系を押すと_目次でハイライトされている大機能は_0_個になる_テストケースカタログの画面の目次の現在位置のハイライトで_カタログヘッダーの正常異常のすべてを押すと_目次でハイライトされている大機能は注文の_1_つだけになる(
        self, record_case, tmp_path, open_catalog_page
    ):
        record_case(
            kind="部品間結合テスト",
            normal_or_abnormal="異常系",
            perspectives=["回復確認"],
            items=[
                ("Given", GIVEN_NORMAL_ONLY_MAJORS),
                (
                    "When",
                    WHEN_PREFIX + "カタログヘッダーの正常異常の『異常系』を押す",
                ),
                ("Then", "目次でハイライトされている大機能は 0 個になる"),
                (
                    "When",
                    WHEN_PREFIX + "カタログヘッダーの正常異常の『すべて』を押す",
                ),
                ("Then", "目次でハイライトされている大機能は『注文』の 1 つだけになる"),
            ],
        )
        html = build_catalog_html(tmp_path, MAJORS_ORDER_MEMBER_STOCK)
        page = open_catalog_page(html)
        catalog_header = locate_catalog_header(page)
        catalog_header.get_by_role("button", name="異常系", exact=True).click()
        assert_no_major_is_highlighted(page)
        catalog_header.get_by_role("button", name="すべて", exact=True).click()
        assert_only_major_is_highlighted(page, "注文")
