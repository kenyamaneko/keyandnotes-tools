import json
import os
import subprocess
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
GENERATION_TIMEOUT_SECONDS = 60
REGIONS = ("本体", "共通", "運用", "外部連携", "シナリオ")
GO_EVENT_TIME = "2026-11-07T00:00:00+09:00"
DART_LOADING_SUITE_PATH = "test/shipping_fee_test.dart"


@dataclass(frozen=True)
class CatalogPage:
    """生成したテストケースカタログの HTML から取り出した内容。"""

    catalog: dict
    title: str
    style: str


_CAPTURED_ELEMENTS = {
    ("title", None): "title",
    ("style", None): "style",
    ("script", "data"): "catalog",
}


class _CatalogPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = {"title": "", "style": "", "catalog": "", "ignored": ""}
        self._current = "ignored"

    def handle_starttag(self, tag, attrs):
        self._current = _CAPTURED_ELEMENTS.get((tag, dict(attrs).get("id")), "ignored")

    def handle_endtag(self, tag):
        self._current = "ignored"

    def handle_data(self, data):
        self.texts[self._current] += data


def assert_message_contains(error, *phrases):
    """エラーのメッセージに、原因を示す語がすべて含まれることを確かめる。"""
    for phrase in phrases:
        assert phrase in str(error), f"{phrase!r} not in {str(error)!r}"


def assert_stopped_with_message(result, *phrases):
    """生成コマンドが 0 以外の終了コードで終わり、標準エラーに原因の語が出ることを確かめる。"""
    assert result.returncode != 0, result.stdout
    for phrase in phrases:
        assert phrase in result.stderr, f"{phrase!r} not in {result.stderr!r}"


def build_features(regions):
    """区分ごとの大機能と中機能を、5 つの区分すべてのキーを持つ機能の一覧にする。"""
    empty_region = {"大機能": [], "中機能": []}
    return {region: regions.get(region, empty_region) for region in REGIONS}


def build_features_of_region(region, majors, minors=()):
    """1 つの区分だけに大機能と中機能を持つ機能の一覧を作る。"""
    return build_features({region: {"大機能": list(majors), "中機能": list(minors)}})


def build_case(region, major, minor, feature):
    """機能だけが違うケースを作る。"""
    return {
        "region": region,
        "major": major,
        "minor": minor,
        "feature": feature,
        "kind": "単体テスト",
        "normal_or_abnormal": "正常系",
        "perspectives": [],
        "environments": [],
        "steps": [
            {
                "given": None,
                "whens": ["注文金額3000円で送料を計算する"],
                "then": "送料は無料になる",
                "environment_thens": [],
            }
        ],
    }


def build_result_entry(language, path):
    """設定ファイルの results の要素を作る。"""
    return {"language": language, "path": str(path)}


def build_config(
    directory, results, features, title="テストケースカタログ", css=".catalog{}"
):
    """CSS ファイルを作り、必須のキーを持つ設定ファイルの内容を作る。"""
    css_path = write_result_file(directory, "catalog.css", css)
    return {
        "title": title,
        "css": str(css_path),
        "results": results,
        "features": features,
    }


def spec_prints(properties):
    """項目を、Dart のテストが出力する `@spec キー=値` の行にする。"""
    return [f"@spec {key}={value}" for key, value in properties]


def write_result_file(directory, filename, content):
    """ファイルを UTF-8 で書き、そのパスを返す。"""
    path = Path(directory) / filename
    path.write_text(content, encoding="utf-8")
    return path


def _build_junit_testcase(classname, name, properties):
    testcase = ElementTree.Element(
        "testcase", {"classname": classname, "name": name, "time": "0.000"}
    )
    properties_element = ElementTree.SubElement(testcase, "properties")
    for key, value in properties:
        ElementTree.SubElement(
            properties_element, "property", {"name": key, "value": value}
        )
    return testcase


def _write_junit_xml(directory, filename, suites):
    root = ElementTree.Element("testsuites")
    for suite_name, testcases in suites:
        suite = ElementTree.SubElement(root, "testsuite", {"name": suite_name})
        suite.extend(testcases)
    path = Path(directory) / filename
    ElementTree.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
    return path


def write_typescript_result(directory, testcases, filename="typescript.xml"):
    """TypeScript のテスト結果 (JUnit XML) を書き、設定ファイルの results の要素を返す。

    Args:
        testcases: (テスト名, 項目の並び) の並び。
    """
    built = [
        _build_junit_testcase("example.test.ts", name, properties)
        for name, properties in testcases
    ]
    path = _write_junit_xml(directory, filename, [("example.test.ts", built)])
    return build_result_entry("TypeScript", path)


def write_python_result(directory, testcases, filename="python.xml"):
    """Python のテスト結果 (pytest の JUnit XML) を書き、設定ファイルの results の要素を返す。

    Args:
        testcases: (classname 属性, 項目の並び) の並び。
    """
    built = [
        _build_junit_testcase(classname, "test_case", properties)
        for classname, properties in testcases
    ]
    path = _write_junit_xml(directory, filename, [("pytest", built)])
    return build_result_entry("Python", path)


def write_csharp_result(directory, testcases, filename="csharp.xml"):
    """C# のテスト結果 (JUnit XML) を書き、設定ファイルの results の要素を返す。

    Args:
        testcases: (ケースの DisplayName, Trait を含む項目の並び) の並び。
    """
    built = [
        _build_junit_testcase("ExampleTests", name, properties)
        for name, properties in testcases
    ]
    path = _write_junit_xml(directory, filename, [("ExampleTests", built)])
    return build_result_entry("C#", path)


def write_kotlin_result(directory, testcases, filename="kotlin.xml"):
    """Kotlin のテスト結果 (Gradle の JUnit XML) を書き、設定ファイルの results の要素を返す。

    Args:
        testcases: (テストクラスの表示名, ケース名, 項目の並び) の並び。
            テストクラスの表示名が testsuite 要素の name 属性になる。
    """
    suites = [
        (
            class_display_name,
            [_build_junit_testcase("ExampleTest", name, properties)],
        )
        for class_display_name, name, properties in testcases
    ]
    path = _write_junit_xml(directory, filename, suites)
    return build_result_entry("Kotlin", path)


def _go_event(action, **fields):
    return {"Time": GO_EVENT_TIME, "Action": action, "Package": "probe", **fields}


def _write_go_events(directory, filename, events):
    path = Path(directory) / filename
    lines = [json.dumps(event, ensure_ascii=False) for event in events]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return build_result_entry("Go", path)


def _build_go_events(tests, parent_tests, attr_events):
    names = [name for name, _ in tests]
    return (
        [_go_event("start")]
        + [_go_event("run", Test=name) for name in [*parent_tests, *names]]
        + attr_events
        + [_go_event("pass", Test=name, Elapsed=0) for name in [*names, *parent_tests]]
        + [_go_event("pass", Elapsed=0)]
    )


def write_go_result(directory, tests, parent_tests=(), filename="go.jsonl"):
    """Go のテスト結果 (`go test -json`) を書き、設定ファイルの results の要素を返す。

    Args:
        tests: (`/` でつないだテスト名, 項目の並び) の並び。項目はテストごとに続けて出る。
        parent_tests: 項目を持たずに実行される上位のテスト名の並び。
    """
    attr_events = [
        _go_event("attr", Test=name, Key=key, Value=value)
        for name, properties in tests
        for key, value in properties
    ]
    events = _build_go_events(tests, parent_tests, attr_events)
    return _write_go_events(directory, filename, events)


def write_go_interleaved_result(directory, tests, filename="go_interleaved.jsonl"):
    """項目が複数のテストで 1 項目ずつ交互に出る Go のテスト結果を書き、results の要素を返す。

    Args:
        tests: (`/` でつないだテスト名, 項目の並び) の並び。項目の数はテストの間でそろえる。
    """
    per_test_attrs = [
        [
            _go_event("attr", Test=name, Key=key, Value=value)
            for key, value in properties
        ]
        for name, properties in tests
    ]
    attr_events = [event for round_ in zip(*per_test_attrs) for event in round_]
    events = _build_go_events(tests, (), attr_events)
    return _write_go_events(directory, filename, events)


def write_dart_result(
    directory, tests, group_names=(), hidden_test_names=(), filename="dart.jsonl"
):
    """Dart のテスト結果 (`dart test -r json`) を書き、設定ファイルの results の要素を返す。

    Args:
        tests: (ケース名, テストが出力する行の並び) の並び。
        group_names: 外側から順に入れ子にした group の名前。空ならグループに入らない。
        hidden_test_names: テスト実行ツールがファイルの読み込みごとに出す hidden のテストの名前。
    """
    suite = {"id": 0, "platform": "vm", "path": DART_LOADING_SUITE_PATH}
    metadata = {"skip": False, "skipReason": None}
    hidden_ids = list(range(1, len(hidden_test_names) + 1))
    root_group_id = len(hidden_ids) + 1
    group_ids = [root_group_id + index for index in range(len(group_names) + 1)]
    first_test_id = group_ids[-1] + 1
    parent_ids = [None, *group_ids]
    events = [
        {
            "protocolVersion": "0.1.1",
            "runnerVersion": "1.33.0",
            "pid": 1,
            "type": "start",
            "time": 0,
        },
        {"suite": suite, "type": "suite", "time": 0},
    ]
    for test_id, name in zip(hidden_ids, hidden_test_names):
        events.append(
            {
                "test": {
                    "id": test_id,
                    "name": name,
                    "suiteID": 0,
                    "groupIDs": [],
                    "metadata": metadata,
                },
                "type": "testStart",
                "time": 0,
            }
        )
        events.append(
            {
                "testID": test_id,
                "result": "success",
                "skipped": False,
                "hidden": True,
                "type": "testDone",
                "time": 1,
            }
        )
    for group_id, parent_id, name in zip(group_ids, parent_ids, ["", *group_names]):
        events.append(
            {
                "group": {
                    "id": group_id,
                    "suiteID": 0,
                    "parentID": parent_id,
                    "name": name,
                    "metadata": metadata,
                    "testCount": len(tests),
                },
                "type": "group",
                "time": 2,
            }
        )
    for test_id, (case_name, prints) in zip(
        range(first_test_id, first_test_id + len(tests)), tests
    ):
        events.append(
            {
                "test": {
                    "id": test_id,
                    "name": " ".join([*group_names, case_name]),
                    "suiteID": 0,
                    "groupIDs": group_ids,
                    "metadata": metadata,
                },
                "type": "testStart",
                "time": 3,
            }
        )
        events.extend(
            {
                "testID": test_id,
                "messageType": "print",
                "message": message,
                "type": "print",
                "time": 4,
            }
            for message in prints
        )
        events.append(
            {
                "testID": test_id,
                "result": "success",
                "skipped": False,
                "hidden": False,
                "type": "testDone",
                "time": 5,
            }
        )
    events.append({"success": True, "type": "done", "time": 6})
    path = Path(directory) / filename
    path.write_text(
        "\n".join(json.dumps(event, ensure_ascii=False) for event in events) + "\n",
        encoding="utf-8",
    )
    return build_result_entry("Dart", path)


def run_catalog_generation(directory, config):
    """設定ファイルを書き、生成コマンドを実行して、その結果を返す。"""
    config_path = write_result_file(
        directory, "config.json", json.dumps(config, ensure_ascii=False)
    )
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "test_case_catalog.generate_test_case_catalog",
            "--config",
            str(config_path),
        ],
        check=False,
        cwd=REPOSITORY_ROOT,
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=GENERATION_TIMEOUT_SECONDS,
    )


def generate_catalog_page(directory, config):
    """生成コマンドを実行し、成功した出力の HTML を解析して返す。"""
    result = run_catalog_generation(directory, config)
    assert result.returncode == 0, result.stderr
    parser = _CatalogPageParser()
    parser.feed(result.stdout)
    parser.close()
    return CatalogPage(
        catalog=json.loads(parser.texts["catalog"]),
        title=parser.texts["title"],
        style=parser.texts["style"],
    )
