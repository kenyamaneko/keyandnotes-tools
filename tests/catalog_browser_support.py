import math
import re
from pathlib import Path

from catalog_support import (
    REPOSITORY_ROOT,
    build_config,
    build_features_of_region,
    run_catalog_generation,
    write_typescript_result,
)
from playwright.sync_api import expect

CSS_PATH = REPOSITORY_ROOT / "test_case_catalog" / "test_case_catalog.css"
DEFAULT_VIEWPORT_WIDTH = 1280
DEFAULT_VIEWPORT_HEIGHT = 720
STABLE_FRAME_COUNT = 20
MAX_WHEEL_DELTA = 3000
MAX_WHEEL_COUNT = 100
WHEEL_POSITION_RATIO = 0.75
NORMAL_OR_ABNORMAL_OF_ABNORMAL = {True: "異常系", False: "正常系"}
NEXT_ANIMATION_FRAME_JS = "() => new Promise(resolve => requestAnimationFrame(resolve))"


def build_catalog_html(directory, majors, abnormal_majors=(), feature_count=1):
    """区分「本体」に、指定した大機能を持つテストケースカタログの HTML を生成する。

    Args:
        majors: 大機能の名前の並び。カタログはこの順に並ぶ。
        abnormal_majors: 異常系のケースを持たせる大機能。それ以外は正常系のケースを持つ。
        feature_count: 大機能ごとの小機能の数。小機能ごとにケースを 1 つ持つ。
    """
    testcases = [
        (
            f"[本体:{major}]{major}の機能{number} > 操作すると、結果になる",
            (
                ("種別", "単体テスト"),
                ("正常異常", NORMAL_OR_ABNORMAL_OF_ABNORMAL[major in abnormal_majors]),
                ("When", "操作する"),
                ("Then", "結果になる"),
            ),
        )
        for major in majors
        for number in range(1, feature_count + 1)
    ]
    entry = write_typescript_result(directory, testcases)
    config = build_config(
        directory,
        [entry],
        build_features_of_region("本体", list(majors)),
        css=CSS_PATH.read_text(encoding="utf-8"),
    )
    result = run_catalog_generation(directory, config)
    assert result.returncode == 0, result.stderr
    return result.stdout


def write_catalog_html(directory, html):
    """カタログの HTML をファイルに書き、そのパスを返す。"""
    path = Path(directory) / "catalog.html"
    path.write_text(html, encoding="utf-8")
    return path


def locate_toc(page):
    """目次のナビゲーションを返す。"""
    return page.get_by_role("navigation", name="大機能の目次")


def locate_toc_link(page, major):
    """目次にある、大機能の表ヘッダーへ移動するリンクを返す。"""
    return locate_toc(page).get_by_role("link", name=re.compile(f"^{re.escape(major)}"))


def locate_catalog_header(page):
    """画面の上端に固定された、フィルターのボタンなどが並ぶエリアを返す。"""
    return page.get_by_role("region", name="フィルター")


def locate_highlighted_toc_links(page):
    """目次でハイライトされている大機能のリンクを返す。"""
    return locate_toc(page).locator("a[aria-current='location']")


def assert_only_major_is_highlighted(page, major):
    """目次でハイライトされている大機能が、指定した大機能の 1 つだけであることを確かめる。"""
    expect(locate_highlighted_toc_links(page)).to_have_text(
        [re.compile(rf"^{re.escape(major)}\d+$")]
    )


def assert_no_major_is_highlighted(page):
    """目次でハイライトされている大機能が 0 個であることを確かめる。"""
    expect(locate_highlighted_toc_links(page)).to_have_count(0)


def assert_toc_link_is_visible_in_toc(page, major):
    """目次の大機能のリンクが、目次の表示範囲と画面の範囲の両方に収まっていることを確かめる。"""
    link = locate_toc_link(page, major).bounding_box()
    toc_area = page.get_by_role("complementary").bounding_box()
    visible_top = max(toc_area["y"], 0)
    visible_bottom = min(
        toc_area["y"] + toc_area["height"], page.viewport_size["height"]
    )
    assert link["y"] >= visible_top, (link, toc_area)
    assert link["y"] + link["height"] <= visible_bottom, (link, toc_area)


def wait_until_scroll_stops(page):
    """画面と目次のスクロール位置が、連続する描画フレームで変わらなくなるまで待つ。"""
    toc_area = page.get_by_role("complementary")
    stable_frames = 0
    last_positions = None
    while stable_frames < STABLE_FRAME_COUNT:
        page.evaluate(NEXT_ANIMATION_FRAME_JS)
        positions = (
            page.evaluate("window.scrollY"),
            toc_area.evaluate("e => e.scrollTop"),
        )
        stable_frames = (stable_frames + 1) * int(positions == last_positions)
        last_positions = positions


def measure_distance_to_catalog_header(page, major):
    """大機能の表ヘッダーの上端から、カタログヘッダーの下端までの距離を返す。

    表ヘッダーがカタログヘッダーより下にあるとき正の値、同じ位置か上にあるとき 0 以下になる。
    """
    major_header = page.get_by_role("heading", level=2, name=major, exact=True)
    catalog_header = locate_catalog_header(page).bounding_box()
    major_header_top = major_header.bounding_box()["y"]
    return major_header_top - (catalog_header["y"] + catalog_header["height"])


def scroll_until_major_header_is_below_catalog_header(page, major):
    """マウスホイールで、大機能の表ヘッダーがカタログヘッダーの直下に来るまでスクロールする。"""
    viewport = page.viewport_size
    page.mouse.move(viewport["width"] * WHEEL_POSITION_RATIO, viewport["height"] / 2)
    wheel_count = 0
    distance = measure_distance_to_catalog_header(page, major)
    while distance > 0 and wheel_count < MAX_WHEEL_COUNT:
        page.mouse.wheel(0, min(math.ceil(distance), MAX_WHEEL_DELTA))
        wait_until_scroll_stops(page)
        wheel_count += 1
        distance = measure_distance_to_catalog_header(page, major)
    assert distance <= 0, f"{major} の表ヘッダーがカタログヘッダーの直下まで来なかった"
