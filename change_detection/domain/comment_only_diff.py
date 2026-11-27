import ast
import io
import re
import tokenize
from collections.abc import Callable, Sequence
from functools import cache
from pathlib import PurePosixPath

import tree_sitter
import tree_sitter_c_sharp
import tree_sitter_dart
import tree_sitter_go
import tree_sitter_hcl
import tree_sitter_javascript
import tree_sitter_kotlin
import tree_sitter_typescript

Span = tuple[int, int]

_HORIZONTAL_SPACES = b" \t"
_LINE_END_SPACES = b" \t\r"
_NEWLINE = b"\n"
_COMMENT_MARKERS = re.compile(r"^(?:/\*+|//+|#+|\*+/?)?\s*")
_DOCTEST_PROMPT = ">>>"

_DIRECTIVE_COMMENT_PATTERNS = {
    "typescript": (
        r"@ts-[a-z-]+",
        r"eslint-(?:disable|enable)",
        r"prettier-ignore",
        r"(?:istanbul|c8|v8) ignore",
        r"<reference ",
    ),
    "go": (r"go:", r"\+build ", r"nolint"),
    "dart": (r"ignore:", r"ignore_for_file:"),
    "csharp": (r"ReSharper (?:disable|restore)",),
    "kotlin": (r"noinspection", r"ktlint-(?:disable|enable)"),
    "hcl": (r"tflint-ignore", r"checkov:"),
    "python": (
        r"type:",
        r"noqa",
        r"pragma:",
        r"-\*- coding",
    ),
}
_DIRECTIVE_COMMENT_PATTERNS["javascript"] = _DIRECTIVE_COMMENT_PATTERNS["typescript"]
_DIRECTIVE_COMMENT_PATTERNS["tsx"] = _DIRECTIVE_COMMENT_PATTERNS["typescript"]

_LANGUAGE_BY_SUFFIX = {
    ".ts": "typescript",
    ".mts": "typescript",
    ".cts": "typescript",
    ".tsx": "tsx",
    ".js": "javascript",
    ".jsx": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".go": "go",
    ".dart": "dart",
    ".cs": "csharp",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".tf": "hcl",
    ".tfvars": "hcl",
    ".py": "python",
}

_GRAMMAR_LANGUAGES: dict[str, Callable[[], object]] = {
    "typescript": tree_sitter_typescript.language_typescript,
    "tsx": tree_sitter_typescript.language_tsx,
    "javascript": tree_sitter_javascript.language,
    "go": tree_sitter_go.language,
    "dart": tree_sitter_dart.language,
    "csharp": tree_sitter_c_sharp.language,
    "kotlin": tree_sitter_kotlin.language,
    "hcl": tree_sitter_hcl.language,
}


class _UnparsableSourceError(Exception):
    pass


@cache
def _build_parser(language: str) -> tree_sitter.Parser:
    return tree_sitter.Parser(tree_sitter.Language(_GRAMMAR_LANGUAGES[language]()))


def _is_directive_comment(language: str, comment: str) -> bool:
    body = _COMMENT_MARKERS.sub("", comment, count=1)
    if language == "python" and comment.startswith("#!"):
        return True
    return any(re.match(pattern, body) for pattern in _DIRECTIVE_COMMENT_PATTERNS[language])


def _find_tree_sitter_comment_spans(language: str, source: bytes) -> list[Span]:
    tree = _build_parser(language).parse(source)
    if tree.root_node.has_error:
        raise _UnparsableSourceError
    spans = []
    pending = [tree.root_node]
    while pending:
        node = pending.pop()
        if "comment" in node.type:
            text = source[node.start_byte : node.end_byte].decode(errors="replace")
            if not _is_directive_comment(language, text):
                spans.append((node.start_byte, node.end_byte))
            continue
        pending.extend(node.children)
    return sorted(spans)


def _list_line_start_offsets(source: bytes) -> list[int]:
    offsets = [0]
    for line in source.split(_NEWLINE)[:-1]:
        offsets.append(offsets[-1] + len(line) + 1)
    return offsets


def _find_python_comment_spans(text: str) -> list[Span]:
    source = text.encode(errors="surrogateescape")
    line_starts = _list_line_start_offsets(source)
    lines = text.split("\n")

    def calculate_byte_offset_from_character(row: int, column: int) -> int:
        return line_starts[row - 1] + len(lines[row - 1][:column].encode(errors="surrogateescape"))

    def calculate_byte_offset_from_byte(row: int, column: int) -> int:
        return line_starts[row - 1] + column

    spans = []
    try:
        for token in tokenize.generate_tokens(io.StringIO(text).readline):
            if token.type == tokenize.COMMENT and not _is_directive_comment("python", token.string):
                spans.append(
                    (
                        calculate_byte_offset_from_character(*token.start),
                        calculate_byte_offset_from_character(*token.end),
                    )
                )
        tree = ast.parse(text)
    except (tokenize.TokenError, SyntaxError, ValueError) as error:
        raise _UnparsableSourceError from error
    for node in ast.walk(tree):
        if not isinstance(node, ast.Module | ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            continue
        first = node.body[0] if node.body else None
        if not (
            isinstance(first, ast.Expr)
            and isinstance(first.value, ast.Constant)
            and isinstance(first.value.value, str)
        ):
            continue
        # 実行例を含む docstring は doctest がテストとして実行するため、取り除かずに比べる。
        if _DOCTEST_PROMPT in first.value.value:
            continue
        spans.append(
            (
                calculate_byte_offset_from_byte(first.lineno, first.col_offset),
                calculate_byte_offset_from_byte(first.end_lineno, first.end_col_offset),
            )
        )
    return sorted(spans)


def _remove_span(source: bytes, start: int, end: int) -> tuple[int, int]:
    line_start = source.rfind(_NEWLINE, 0, start) + 1
    line_end = source.find(_NEWLINE, end)
    if line_end == -1:
        line_end = len(source)
    has_code_before = bool(source[line_start:start].strip(_HORIZONTAL_SPACES))
    has_code_after = bool(source[end:line_end].strip(_LINE_END_SPACES))
    if not has_code_before and not has_code_after:
        return line_start, min(line_end + 1, len(source))
    if has_code_before:
        while start > line_start and source[start - 1 : start] in (b" ", b"\t"):
            start -= 1
        return start, end
    while end < line_end and source[end : end + 1] in (b" ", b"\t"):
        end += 1
    return start, end


def _remove_comments(source: bytes, spans: Sequence[Span]) -> bytes:
    result = bytearray()
    position = 0
    for start, end in spans:
        remove_start, remove_end = _remove_span(source, start, end)
        result += source[position : max(position, remove_start)]
        position = max(position, remove_end)
    result += source[position:]
    return bytes(result)


def _strip_comments(language: str, text: str) -> bytes:
    source = text.encode(errors="surrogateescape")
    if language == "python":
        spans = _find_python_comment_spans(text)
    else:
        spans = _find_tree_sitter_comment_spans(language, source)
    return _remove_comments(source, spans)


def is_code_change(path: str, before: str | None, after: str | None) -> bool:
    """ファイルの変更前後の内容から、コードの変更に数えるかを返す。

    Args:
        path: ファイルのパス。拡張子で対象言語を決める。
        before: 変更前の内容。ファイルが無い (追加された) ときは None。空のファイルは空文字。
        after: 変更後の内容。ファイルが無い (削除された) ときは None。空のファイルは空文字。
    """
    if before is None or after is None:
        return True
    target_language = _LANGUAGE_BY_SUFFIX.get(PurePosixPath(path).suffix)
    if target_language is None:
        return before != after
    try:
        return _strip_comments(target_language, before) != _strip_comments(target_language, after)
    except _UnparsableSourceError:
        return before != after
