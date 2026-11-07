"""テスト結果から、テストケースカタログ (HTML) を生成する。

設定ファイル (JSON) に書いた言語ごとのテスト結果を読み、機能名と項目 (種別・正常異常・観点・環境・
Given・When・Then) を取り出して、小機能ごとの表にして標準出力へ書き出す。
項目が足りないケースと、機能の一覧にない大機能・中機能は、原因を示すメッセージでエラーにする。
"""

import argparse
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from html import escape
from pathlib import Path

REGIONS = ("本体", "共通", "運用", "外部連携", "シナリオ")
REGION_WITHOUT_MINOR = "運用"
KINDS = (
    "単体テスト",
    "部品間結合テスト",
    "インフラ結合テスト",
    "サービス間結合テスト",
    "E2Eテスト",
    "シナリオテスト",
)
SCENARIO_KIND = "シナリオテスト"
ENVIRONMENTS = ("ローカル", "dev環境")
NORMAL_OR_ABNORMALS = ("正常系", "異常系")
MIN_ENVIRONMENT_THEN_COUNT = 2
PERSPECTIVE_NAMES = (
    "境界値",
    "同値分割",
    "エッジケース",
    "件数・有無",
    "外部依存の失敗",
    "回復確認",
)
PERSPECTIVE_BOUNDARY = "境界値"
PERSPECTIVE_EQUIVALENCE = "同値分割"
LANGUAGES = ("TypeScript", "Python", "C#", "Kotlin", "Go", "Dart")

KEY_KIND = "種別"
KEY_NORMAL_OR_ABNORMAL = "正常異常"
KEY_PERSPECTIVE = "観点"
KEY_ENVIRONMENT = "環境"
KEY_GIVEN = "Given"
KEY_WHEN = "When"
KEY_THEN = "Then"
THEN_ENVIRONMENT_PREFIX = "Then:"

FEATURE_NAME_PATTERN = re.compile(r"\[([^:\]]+):([^:\]]+)(?::([^\]]+))?\](.+)")
FEATURE_NAME_FORM = "[区分:大機能(:中機能)]小機能"
MAJOR_FEATURES = "大機能"
MINOR_FEATURES = "中機能"

# Vitest は " > "、Playwright は " › " でテスト名をつなぐため、どちらでも分ける
TYPESCRIPT_SEPARATOR_PATTERN = re.compile(r" > | › ")

PYTHON_CLASS_PREFIX = "Test"
PYTHON_CLASS_PART_SEPARATOR = "__"
PYTHON_CLASS_FORM = "区分・大機能・(中機能・)小機能"

CSHARP_FEATURE_NAME_TRAIT = "区分・大機能・中機能・小機能"
CSHARP_STEP_KEY_PATTERN = re.compile(r"(Given|When|Then)(\d*)(:.+)?")
CSHARP_STEP_KEY_ORDER = {KEY_GIVEN: 0, KEY_WHEN: 1, KEY_THEN: 2}
UNNUMBERED_STEP = 0

GO_NAME_SEPARATOR = "/"
GO_NAME_LEVEL_COUNT = 3

DART_SPEC_PREFIX = "@spec"
DART_SPEC_PATTERN = re.compile(r"@spec ([^=]+)=(.*)", re.DOTALL)
DART_SPEC_FORM = "@spec キー=値"

# テストの無い仕様はカタログに現れないため、「載っていない = 仕様がない」という誤読を防ぐ
DISCLAIMER = (
    "本カタログはテストコードが担保する振る舞いの一覧であり、仕様の全量ではない。"
)

REQUIRED_CONFIG_KEYS = ("title", "css", "results", "features")
TEMPLATE_PATH = Path(__file__).with_name("test_case_catalog_template.html")
TEMPLATE_PLACEHOLDER_PATTERN = re.compile(r"__(TITLE|CSS|DATA)__")


class CatalogError(ValueError):
    """カタログにできない入力があることを表す。"""


@dataclass(frozen=True)
class RawTest:
    """テスト結果から取り出した、ケース 1 件分の機能名の元と項目の並び。

    Args:
        where: エラーに添える、テストの所在。
        source: 言語ごとに機能名が載っている場所の値。
        properties: 結果に載った順の (キー, 値)。
    """

    where: str
    source: str
    properties: list[tuple[str, str]]


@dataclass(frozen=True)
class LanguageReader:
    """言語ごとのテスト結果の読み取り方。

    Args:
        list_tests: テスト結果のファイルから、ケース 1 件ごとの RawTest を取り出す。
        read_case: RawTest の source と項目の並びを、機能の一覧に照らしてケースにする。
    """

    list_tests: Callable[[Path], list[RawTest]]
    read_case: Callable[[str, Sequence[tuple[str, str]], dict], dict]


@dataclass(frozen=True)
class TestResult:
    """設定ファイルの results の要素。"""

    language: str
    path: Path


@dataclass(frozen=True)
class CatalogConfig:
    """カタログ生成の設定。

    Args:
        title: カタログのページタイトル。
        css: ページに埋め込む、Tailwind が生成した CSS のパス。
        results: テスト結果。
        features: 区分ごとの、大機能の並びと中機能の並び。カタログはこの順に並ぶ。
        commit: 生成元 commit の SHA。None ならカタログに表示しない。
    """

    title: str
    css: Path
    results: tuple[TestResult, ...]
    features: dict[str, dict[str, list[str]]]
    commit: str | None = None


@contextmanager
def add_location_to_errors(where: str) -> Iterator[None]:
    """ブロックの中で起きた CatalogError に、テストの所在を添えて送出し直す。"""
    try:
        yield
    except CatalogError as error:
        raise CatalogError(f"{where}: {error}") from error


def check_listed(
    name: str, value: str | None, allowed: Sequence[str], *, by_name: bool = False
) -> None:
    """値が選べる値の一覧にあることを確かめる。

    Args:
        name: 項目の名前。
        value: 確かめる値。None は項目が付いていないことを表す。
        allowed: 選べる値。
        by_name: True なら、メッセージで選べる値の一覧ではなく項目の名前を使う。

    Raises:
        CatalogError: 値が選べる値にないとき。
    """
    if value in allowed:
        return
    choices = "・".join(allowed)
    scope = name if by_name else choices
    particle = " " if scope[-1].isascii() else ""
    hint = f" (選べる値: {choices})" if by_name else ""
    subject = f"{name}が付いていないため、" if value is None else f"{name}「{value}」が"
    raise CatalogError(f"{subject}{scope}{particle}のいずれでもない{hint}")


def read_single_value(properties: Sequence[tuple[str, str]], key: str) -> str | None:
    """項目の並びから、1 つだけ付くキーの値を取り出す。付いていなければ None。"""
    values = [value for item_key, value in properties if item_key == key]
    if len(values) > 1:
        raise CatalogError(f"{key}が重複している")
    return values[0] if values else None


def parse_feature_name(feature_name: str) -> dict:
    """`[区分:大機能(:中機能)]小機能` を分解する。

    Returns:
        region・major・minor・feature を持つ辞書。中機能が無ければ minor は None。

    Raises:
        CatalogError: 形に合わないとき。
    """
    match = FEATURE_NAME_PATTERN.fullmatch(feature_name)
    if match is None:
        raise CatalogError(f"機能名が {FEATURE_NAME_FORM} の形ではない")
    region, major, minor, feature = match.groups()
    return {"region": region, "major": major, "minor": minor, "feature": feature}


def validate_feature(feature: dict, feature_list: dict) -> None:
    """区分・大機能・中機能が設定ファイルの機能の一覧にあることを確かめる。

    Args:
        feature: parse_feature_name の戻り値。
        feature_list: 設定ファイルの機能の一覧。

    Raises:
        CatalogError: 一覧にない組のとき、または運用に中機能が付いているとき。
    """
    region, major, minor = feature["region"], feature["major"], feature["minor"]
    check_listed("区分", region, REGIONS)
    if region not in feature_list:
        raise CatalogError(f"設定ファイルの機能の一覧に区分「{region}」がない")
    if major not in feature_list[region][MAJOR_FEATURES]:
        raise CatalogError(
            f"設定ファイルの機能の一覧の区分「{region}」に、大機能「{major}」がない"
        )
    if minor is None:
        return
    if region == REGION_WITHOUT_MINOR:
        raise CatalogError(f"区分「{region}」には中機能を付けられない")
    if minor not in feature_list[region][MINOR_FEATURES]:
        raise CatalogError(
            f"設定ファイルの機能の一覧の区分「{region}」に、中機能「{minor}」がない"
        )


def is_then_key(key: str) -> bool:
    """キーが Then か、環境ごとの Then かを返す。"""
    return key == KEY_THEN or key.startswith(THEN_ENVIRONMENT_PREFIX)


def is_step_key(key: str) -> bool:
    """キーがステップを組み立てる項目 (Given・When・Then・環境ごとの Then) かを返す。"""
    return key in (KEY_GIVEN, KEY_WHEN) or is_then_key(key)


def build_step(group: Sequence[tuple[str, str]]) -> dict:
    """Given (任意)・When (1 つ以上)・Then の並びを、ステップにする。

    Returns:
        given・whens・then・environment_thens を持つ辞書。given は無ければ None。
        環境ごとの Then を持つステップでは、then が None で、environment_thens に
        (環境, 結果) を載せた順に並べる。

    Raises:
        CatalogError: Then が無いとき、When が無いとき、または Then の付き方が不正なとき。
    """
    givens = [value for key, value in group if key == KEY_GIVEN]
    whens = [value for key, value in group if key == KEY_WHEN]
    thens = [value for key, value in group if key == KEY_THEN]
    environment_thens = [
        (key.removeprefix(THEN_ENVIRONMENT_PREFIX), value)
        for key, value in group
        if key.startswith(THEN_ENVIRONMENT_PREFIX)
    ]
    if not thens and not environment_thens:
        raise CatalogError("Then の無いステップがある")
    for environment, _ in environment_thens:
        check_listed("環境", environment, ENVIRONMENTS)
    if not whens:
        raise CatalogError("When の無い Then がある")
    if thens and environment_thens:
        raise CatalogError("同じステップに Then と環境ごとの Then が混ざっている")
    if len(thens) > 1:
        raise CatalogError("同じステップに Then が 2 つある")
    environments = [environment for environment, _ in environment_thens]
    for environment in environments:
        if environments.count(environment) > 1:
            raise CatalogError(
                f"同じステップに環境「{environment}」の Then が 2 つある"
            )
    return {
        "given": givens[0] if givens else None,
        "whens": whens,
        "then": thens[0] if thens else None,
        "environment_thens": environment_thens,
    }


def read_steps(properties: Sequence[tuple[str, str]]) -> list[dict]:
    """載った順の Given・When・Then の並びを、ステップに組み立てる。

    Given か、Then の後に続く When から、新しいステップが始まる。

    Args:
        properties: 載った順の (キー, 値)。Given・When・Then・`Then:環境` のキーだけを渡す。

    Returns:
        ステップの並び。build_step の戻り値を参照。

    Raises:
        CatalogError: ステップが 1 つも無いとき、または並びが不正なとき。
    """
    groups: list[list[tuple[str, str]]] = []
    for key, value in properties:
        has_then = bool(groups) and any(is_then_key(k) for k, _ in groups[-1])
        if key == KEY_GIVEN and groups and not has_then:
            raise CatalogError("Then の前に Given が続いている")
        if not groups or key == KEY_GIVEN or (key == KEY_WHEN and has_then):
            groups.append([])
        groups[-1].append((key, value))
    if not groups:
        raise CatalogError("Given・When・Then が無い")
    return [build_step(group) for group in groups]


def validate_perspectives(perspectives: Sequence[str]) -> None:
    """観点が一覧にあり、重複せず、同時に付けられない組でないことを確かめる。"""
    for perspective in perspectives:
        check_listed("観点", perspective, PERSPECTIVE_NAMES, by_name=True)
    if len(set(perspectives)) != len(perspectives):
        raise CatalogError("観点が重複している")
    if PERSPECTIVE_BOUNDARY in perspectives and PERSPECTIVE_EQUIVALENCE in perspectives:
        raise CatalogError(
            f"{PERSPECTIVE_BOUNDARY}と{PERSPECTIVE_EQUIVALENCE}は同時に付けられない"
        )


def validate_environments(
    kind: str, environments: Sequence[str], steps: Sequence[dict]
) -> list[dict]:
    """実行する環境と環境ごとの Then を確かめ、環境ごとの Then を一覧の順にそろえる。

    Returns:
        環境ごとの Then を ENVIRONMENTS の順にそろえたステップ。

    Raises:
        CatalogError: 環境がシナリオテスト以外にあるとき、シナリオテストに無いとき、
            重複しているとき、または環境ごとの Then と食い違うとき。
    """
    for environment in environments:
        check_listed("環境", environment, ENVIRONMENTS)
    if len(set(environments)) != len(environments):
        raise CatalogError("環境が重複している")
    has_environment_thens = any(step["environment_thens"] for step in steps)
    if kind != SCENARIO_KIND:
        if environments:
            raise CatalogError(f"環境は{SCENARIO_KIND}だけが持つ")
        if has_environment_thens:
            raise CatalogError(f"環境ごとの Then は{SCENARIO_KIND}だけに書ける")
        return list(steps)
    if not environments:
        raise CatalogError(f"{SCENARIO_KIND}には環境が必要")
    return [sort_environment_thens(step, environments) for step in steps]


def sort_environment_thens(step: dict, environments: Sequence[str]) -> dict:
    """環境ごとの Then を確かめ、環境の一覧の順に並べたステップを返す。"""
    environment_thens = step["environment_thens"]
    if not environment_thens:
        return step
    if {environment for environment, _ in environment_thens} != set(environments):
        raise CatalogError("環境ごとの Then の環境が、ケースの環境と一致しない")
    if len(environment_thens) < MIN_ENVIRONMENT_THEN_COUNT:
        raise CatalogError("環境ごとの Then は 2 つ以上の環境で書く")
    if len({text for _, text in environment_thens}) < len(environment_thens):
        raise CatalogError("環境ごとの Then が同じ内容のため、Then を 1 つにする")
    ordered = sorted(environment_thens, key=lambda pair: ENVIRONMENTS.index(pair[0]))
    return {**step, "environment_thens": ordered}


def read_case(
    feature_name: str, properties: Sequence[tuple[str, str]], feature_list: dict
) -> dict:
    """機能名と項目の並びを、機能の一覧に照らしてケースにする。

    Args:
        feature_name: `[区分:大機能(:中機能)]小機能`。
        properties: 載った順の (キー, 値)。Given・When・Then 以外のキーも含められる。
        feature_list: 設定ファイルの機能の一覧。

    Returns:
        region・major・minor・feature・kind・normal_or_abnormal・perspectives・
        environments・steps を持つ辞書。中機能が無ければ minor は None。

    Raises:
        CatalogError: 機能の一覧にない機能のとき、または項目が足りない・不正なとき。
    """
    feature = parse_feature_name(feature_name)
    validate_feature(feature, feature_list)
    kind = read_single_value(properties, KEY_KIND)
    check_listed(KEY_KIND, kind, KINDS, by_name=True)
    normal_or_abnormal = read_single_value(properties, KEY_NORMAL_OR_ABNORMAL)
    check_listed(KEY_NORMAL_OR_ABNORMAL, normal_or_abnormal, NORMAL_OR_ABNORMALS)
    perspectives = [value for key, value in properties if key == KEY_PERSPECTIVE]
    validate_perspectives(perspectives)
    tagged_environments = [value for key, value in properties if key == KEY_ENVIRONMENT]
    steps = read_steps([item for item in properties if is_step_key(item[0])])
    steps = validate_environments(kind, tagged_environments, steps)
    return {
        **feature,
        "kind": kind,
        "normal_or_abnormal": normal_or_abnormal,
        "perspectives": perspectives,
        "environments": [e for e in ENVIRONMENTS if e in tagged_environments],
        "steps": steps,
    }


def parse_xml(path: Path) -> ET.Element:
    """JUnit XML を読み、ルート要素を返す。"""
    try:
        return ET.parse(path).getroot()
    except ET.ParseError as error:
        raise CatalogError(f"{path}: XML を読めない: {error}") from error


def read_attribute(element: ET.Element, attribute: str, path: Path) -> str:
    """testcase などの属性を取り出す。無ければ CatalogError。"""
    value = element.get(attribute)
    if value is None:
        raise CatalogError(f"{path}: {element.tag} に {attribute} 属性がない")
    return value


def read_junit_properties(testcase: ET.Element, path: Path) -> list[tuple[str, str]]:
    """testcase の property を、載った順の (キー, 値) にする。"""
    return [
        (
            read_attribute(property_element, "name", path),
            read_attribute(property_element, "value", path),
        )
        for property_element in testcase.iter("property")
    ]


def read_typescript_feature_name(test_name: str) -> str:
    """TypeScript の testcase 名から、先頭の describe 名 (機能名) を取り出す。"""
    return TYPESCRIPT_SEPARATOR_PATTERN.split(test_name, maxsplit=1)[0]


def read_typescript_case(
    test_name: str, properties: Sequence[tuple[str, str]], feature_list: dict
) -> dict:
    """TypeScript の testcase 名と項目の並びを、ケースにする。"""
    return read_case(read_typescript_feature_name(test_name), properties, feature_list)


def list_typescript_tests(path: Path) -> list[RawTest]:
    """TypeScript の JUnit XML から、testcase ごとの RawTest を取り出す。"""
    tests = []
    for testcase in parse_xml(path).iter("testcase"):
        name = read_attribute(testcase, "name", path)
        where = f"{path}: テスト「{name}」"
        with add_location_to_errors(where):
            tests.append(RawTest(where, name, read_junit_properties(testcase, path)))
    return tests


def read_python_feature_name(class_name: str) -> str:
    """pytest の classname 属性から、最も外側のテストクラスが表す機能名を取り出す。

    Raises:
        CatalogError: Test で始まるクラスが無いとき、または区分・大機能・(中機能・)小機能の形でないとき。
    """
    outer_class = next(
        (
            segment
            for segment in class_name.split(".")
            if segment.startswith(PYTHON_CLASS_PREFIX)
        ),
        None,
    )
    if outer_class is None:
        raise CatalogError(f"クラス名が {PYTHON_CLASS_PREFIX} で始まっていない")
    parts = [
        part.replace("_", " ")
        for part in outer_class.removeprefix(PYTHON_CLASS_PREFIX).split(
            PYTHON_CLASS_PART_SEPARATOR
        )
    ]
    match parts:
        case [region, major, feature]:
            return f"[{region}:{major}]{feature}"
        case [region, major, minor, feature]:
            return f"[{region}:{major}:{minor}]{feature}"
        case _:
            raise CatalogError(f"クラス名が{PYTHON_CLASS_FORM}の形ではない")


def read_python_case(
    class_name: str, properties: Sequence[tuple[str, str]], feature_list: dict
) -> dict:
    """pytest の classname 属性と項目の並びを、ケースにする。"""
    return read_case(read_python_feature_name(class_name), properties, feature_list)


def list_python_tests(path: Path) -> list[RawTest]:
    """pytest の JUnit XML から、testcase ごとの RawTest を取り出す。"""
    tests = []
    for testcase in parse_xml(path).iter("testcase"):
        class_name = read_attribute(testcase, "classname", path)
        where = f"{path}: クラス名「{class_name}」"
        with add_location_to_errors(where):
            tests.append(
                RawTest(where, class_name, read_junit_properties(testcase, path))
            )
    return tests


def normalize_csharp_properties(
    properties: Sequence[tuple[str, str]],
) -> list[tuple[str, str]]:
    """C# の項目のキーから、ステップの番号を外して番号順に並べる。

    Raises:
        CatalogError: 番号の付いたキーと付かないキーが混ざっているとき。
    """
    others = []
    steps = []
    for key, value in properties:
        match = CSHARP_STEP_KEY_PATTERN.fullmatch(key)
        if match is None:
            others.append((key, value))
            continue
        name, number, environment = match.groups()
        steps.append(
            (
                int(number) if number else UNNUMBERED_STEP,
                CSHARP_STEP_KEY_ORDER[name],
                f"{name}{environment or ''}",
                value,
                bool(number),
            )
        )
    if len({is_numbered for *_, is_numbered in steps}) > 1:
        raise CatalogError("番号の付いたキーと付かないキーが混ざっている")
    steps.sort(key=lambda step: step[:2])
    return others + [(key, value) for _, _, key, value, _ in steps]


def list_csharp_tests(path: Path) -> list[RawTest]:
    """C# の JUnit XML から、testcase ごとの RawTest を取り出す。

    機能名は Trait「区分・大機能・中機能・小機能」の値で、RawTest の source になる。
    """
    tests = []
    for testcase in parse_xml(path).iter("testcase"):
        name = read_attribute(testcase, "name", path)
        where = f"{path}: テスト「{name}」"
        with add_location_to_errors(where):
            properties = read_junit_properties(testcase, path)
            feature_name = read_single_value(properties, CSHARP_FEATURE_NAME_TRAIT)
            if feature_name is None:
                raise CatalogError(f"Trait「{CSHARP_FEATURE_NAME_TRAIT}」がない")
            others = [
                item for item in properties if item[0] != CSHARP_FEATURE_NAME_TRAIT
            ]
            tests.append(
                RawTest(where, feature_name, normalize_csharp_properties(others))
            )
    return tests


def list_kotlin_tests(path: Path) -> list[RawTest]:
    """Kotlin の JUnit XML から、testcase ごとの RawTest を取り出す。

    機能名は、testcase を含む testsuite の name 属性 (テストクラスの表示名) で、RawTest の source になる。
    """
    root = parse_xml(path)
    parents = {child: parent for parent in root.iter() for child in parent}
    tests = []
    for testcase in root.iter("testcase"):
        suite = parents.get(testcase)
        if suite is None or suite.tag != "testsuite":
            raise CatalogError(f"{path}: testcase が testsuite に入っていない")
        suite_name = read_attribute(suite, "name", path)
        where = f"{path}: テストクラスの表示名「{suite_name}」"
        with add_location_to_errors(where):
            tests.append(
                RawTest(where, suite_name, read_junit_properties(testcase, path))
            )
    return tests


def read_json_lines(path: Path) -> list[dict]:
    """1 行に 1 つの JSON を書いたテスト結果を読む。"""
    events = []
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise CatalogError(f"{path}: {line_number} 行目が JSON ではない") from error
    return events


def read_go_case(
    test_name: str, properties: Sequence[tuple[str, str]], feature_list: dict
) -> dict:
    """Go のテスト名 (テスト関数/機能名/ケース) と項目の並びを、ケースにする。

    Raises:
        CatalogError: テスト名がテスト関数・機能名・ケースの 3 階層でないとき。
    """
    match test_name.split(GO_NAME_SEPARATOR):
        case [_, feature_name, _]:
            return read_case(feature_name, properties, feature_list)
        case _:
            raise CatalogError(
                f"テスト関数・機能名・ケースの {GO_NAME_LEVEL_COUNT} 階層ではない"
            )


def list_go_tests(path: Path) -> list[RawTest]:
    """`go test -json` の出力から、最も下の階層のテストごとの RawTest を取り出す。"""
    names: list[tuple[str, str]] = []
    properties_by_test: dict[tuple[str, str], list[tuple[str, str]]] = {}
    for event in read_json_lines(path):
        if "Test" not in event:
            continue
        test = (event.get("Package", ""), event["Test"])
        if event.get("Action") == "run":
            names.append(test)
            properties_by_test.setdefault(test, [])
        elif event.get("Action") == "attr":
            properties_by_test.setdefault(test, []).append(
                (event["Key"], event["Value"])
            )
    parents = {
        (package, GO_NAME_SEPARATOR.join(parts[:depth]))
        for package, name in names
        for parts in [name.split(GO_NAME_SEPARATOR)]
        for depth in range(1, len(parts))
    }
    return [
        RawTest(f"{path}: テスト「{name}」", name, properties_by_test[(package, name)])
        for package, name in names
        if (package, name) not in parents
    ]


def parse_dart_spec(message: str) -> tuple[str, str]:
    """Dart のテストが出力した `@spec キー=値` の行を、(キー, 値) にする。"""
    match = DART_SPEC_PATTERN.fullmatch(message)
    if match is None:
        raise CatalogError(f"出力「{message}」が `{DART_SPEC_FORM}` の形ではない")
    return match.group(1), match.group(2)


def list_dart_tests(path: Path) -> list[RawTest]:
    """`dart test -r json` の出力から、テストごとの RawTest を取り出す。

    機能名は、テストを含む最も外側の group の名前で、RawTest の source になる。
    テスト実行ツールがファイルの読み込みごとに出す hidden のテストは、ケースに数えない。
    """
    events = read_json_lines(path)
    group_names = {
        event["group"]["id"]: event["group"]["name"]
        for event in events
        if event.get("type") == "group"
    }
    hidden_ids = {
        event["testID"]
        for event in events
        if event.get("type") == "testDone" and event.get("hidden")
    }
    printed: dict[int, list[str]] = {}
    for event in events:
        if event.get("type") == "print":
            printed.setdefault(event["testID"], []).append(event["message"])
    tests = []
    for event in events:
        if event.get("type") != "testStart" or event["test"]["id"] in hidden_ids:
            continue
        test = event["test"]
        where = f"{path}: テスト「{test['name']}」"
        with add_location_to_errors(where):
            names = [group_names[group_id] for group_id in test["groupIDs"]]
            feature_name = next((name for name in names if name), None)
            if feature_name is None:
                raise CatalogError("機能名のグループに入っていない")
            messages = [
                message
                for message in printed.get(test["id"], [])
                if message.startswith(DART_SPEC_PREFIX)
            ]
            properties = [parse_dart_spec(message) for message in messages]
            tests.append(RawTest(where, feature_name, properties))
    return tests


LANGUAGE_READERS = {
    "TypeScript": LanguageReader(list_typescript_tests, read_typescript_case),
    "Python": LanguageReader(list_python_tests, read_python_case),
    "C#": LanguageReader(list_csharp_tests, read_case),
    "Kotlin": LanguageReader(list_kotlin_tests, read_case),
    "Go": LanguageReader(list_go_tests, read_go_case),
    "Dart": LanguageReader(list_dart_tests, read_case),
}


def read_test_result(entry: object) -> TestResult:
    """設定ファイルの results の要素を読む。

    Raises:
        CatalogError: language か path が無いとき、または言語が一覧にないとき。
    """
    if not isinstance(entry, dict):
        raise CatalogError(
            "「results」の要素は language と path を持つオブジェクトで書く"
        )
    for key in ("language", "path"):
        if key not in entry:
            raise CatalogError(f"「results」の要素に「{key}」がない")
    check_listed("言語", entry["language"], LANGUAGES)
    return TestResult(entry["language"], Path(entry["path"]))


def validate_feature_list(feature_list: object) -> None:
    """設定ファイルの features が、区分ごとに大機能と中機能の並びを持つことを確かめる。"""
    if not isinstance(feature_list, dict):
        raise CatalogError(
            "「features」は区分ごとの大機能と中機能を持つオブジェクトで書く"
        )
    for region, entry in feature_list.items():
        for key in (MAJOR_FEATURES, MINOR_FEATURES):
            if not isinstance(entry, dict) or not isinstance(entry.get(key), list):
                raise CatalogError(
                    f"「features」の区分「{region}」に、{key}の配列がない"
                )


def load_config(path: Path) -> CatalogConfig:
    """設定ファイルの JSON を読む。

    Args:
        path: 設定ファイルのパス。

    Raises:
        CatalogError: JSON として読めないとき、必須のキーが無いとき、または値が不正なとき。
    """
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise CatalogError(f"{path}: 設定ファイルが JSON ではない: {error}") from error
    missing = [key for key in REQUIRED_CONFIG_KEYS if key not in raw]
    if missing:
        keys = "・".join(f"「{key}」" for key in missing)
        raise CatalogError(f"設定ファイルに必須のキー{keys}がない ({path})")
    if not isinstance(raw["results"], list):
        raise CatalogError("「results」は配列で書く")
    validate_feature_list(raw["features"])
    return CatalogConfig(
        title=raw["title"],
        css=Path(raw["css"]),
        results=tuple(read_test_result(entry) for entry in raw["results"]),
        features=raw["features"],
        commit=raw.get("commit"),
    )


def read_cases(config: CatalogConfig) -> list[dict]:
    """設定ファイルの results に書かれたテスト結果から、ケースを読む。"""
    cases = []
    for result in config.results:
        reader = LANGUAGE_READERS[result.language]
        for test in reader.list_tests(result.path):
            with add_location_to_errors(test.where):
                cases.append(
                    reader.read_case(test.source, test.properties, config.features)
                )
    return cases


def sort_cases(cases: Sequence[dict], feature_list: dict) -> list[dict]:
    """区分・大機能・中機能を一覧の順に並べる。同じ組の中は読み込んだ順のまま。

    中機能を持たないケースは、同じ大機能の中機能を持つケースより後に並ぶ。
    """

    def rank(case: dict) -> tuple[int, int, int]:
        listed = feature_list[case["region"]]
        minors = listed[MINOR_FEATURES]
        minor_rank = (
            len(minors) if case["minor"] is None else minors.index(case["minor"])
        )
        return (
            REGIONS.index(case["region"]),
            listed[MAJOR_FEATURES].index(case["major"]),
            minor_rank,
        )

    return sorted(cases, key=rank)


def build_step_payload(step: dict) -> dict:
    """ステップを画面の描画に渡すデータにする。環境ごとの Then があるときだけ E を持つ。"""
    payload = {"G": step["given"] or "", "W": step["whens"], "T": step["then"] or ""}
    if step["environment_thens"]:
        payload["E"] = [list(pair) for pair in step["environment_thens"]]
    return payload


def build_payload(cases: Sequence[dict], commit: str | None, title: str) -> dict:
    """画面の描画に渡すデータを組み立てる。commit が None なら空文字にする。"""
    return {
        "title": title,
        "disclaimer": DISCLAIMER,
        "commit": commit or "",
        "regions": list(REGIONS),
        "perspectives": list(PERSPECTIVE_NAMES),
        "cases": [
            {
                "k": case["region"],
                "d": case["major"],
                "m": case["minor"] or "",
                "s": case["feature"],
                "t": case["kind"],
                "n": case["normal_or_abnormal"],
                "e": case["environments"],
                "g": case["perspectives"],
                "steps": [build_step_payload(step) for step in case["steps"]],
            }
            for case in cases
        ],
    }


def render_html(cases: Sequence[dict], commit: str | None, css: str, title: str) -> str:
    """テストケースカタログを単一ファイルの HTML ページとして描画する。

    Args:
        cases: 並べ替え済みのケース。
        commit: 生成元 commit の SHA。None ならカタログに表示しない。
        css: ページに埋め込む、Tailwind が生成した CSS。
        title: ページのタイトル。
    """
    payload = json.dumps(
        build_payload(cases, commit, title), ensure_ascii=False, separators=(",", ":")
    )
    # script 要素の中でタグと解釈されるのを避けるため、山括弧と & を文字参照ではなく JSON のエスケープにする
    payload = (
        payload.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    )
    values = {"TITLE": escape(title, quote=False), "CSS": css, "DATA": payload}
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    # 値の中に別のプレースホルダと同じ文字列があっても置き換わらないため、1 回の走査で置き換える
    return TEMPLATE_PLACEHOLDER_PATTERN.sub(lambda m: values[m.group(1)], template)


def main(argv: list[str] | None = None) -> None:
    """コマンドライン引数を解釈し、カタログを標準出力へ書き出す。原因があれば、メッセージを出して終了する。"""
    parser = argparse.ArgumentParser(
        description="テスト結果からテストケースカタログを生成する"
    )
    parser.add_argument(
        "--config",
        required=True,
        type=Path,
        help="タイトル・CSS・テスト結果・大機能と中機能の一覧をまとめた JSON のパス",
    )
    args = parser.parse_args(argv)

    try:
        config = load_config(args.config)
        cases = sort_cases(read_cases(config), config.features)
        css = config.css.read_text(encoding="utf-8")
        sys.stdout.write(render_html(cases, config.commit, css, config.title))
    except (CatalogError, OSError) as error:
        sys.exit(str(error))


if __name__ == "__main__":
    main()
