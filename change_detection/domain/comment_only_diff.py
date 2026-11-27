import ast
import io
import re
import tokenize
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from functools import cached_property
from pathlib import PurePosixPath
from typing import Protocol

import tree_sitter
import tree_sitter_c_sharp
import tree_sitter_dart
import tree_sitter_go
import tree_sitter_hcl
import tree_sitter_javascript
import tree_sitter_kotlin
import tree_sitter_typescript

from change_detection.domain.committed_file import CommittedFile
from change_detection.domain.errors import UnparsableSourceError

Span = tuple[int, int]

_HORIZONTAL_SPACES = b" \t"
_LINE_END_SPACES = b" \t\r"
_NEWLINE = b"\n"
_COMMENT_MARKERS = re.compile(r"^(?:/\*+|//+|#+|\*+/?)?\s*")
_DOCTEST_PROMPT = ">>>"


class _TargetLanguage(Protocol):
    def find_comment_spans(self, text: str) -> list[Span]:
        """指示コメントを除くコメントの、バイト位置の範囲を昇順で返す。"""
        ...


def _has_directive_comment_pattern(patterns: Sequence[str], comment: str) -> bool:
    body = _COMMENT_MARKERS.sub("", comment, count=1)
    return any(re.match(pattern, body) for pattern in patterns)


@dataclass(frozen=True)
class _TreeSitterTargetLanguage:
    load_grammar: Callable[[], object]
    directive_comment_patterns: tuple[str, ...]

    @cached_property
    def parser(self) -> tree_sitter.Parser:
        return tree_sitter.Parser(tree_sitter.Language(self.load_grammar()))

    def _is_directive_comment(self, comment: str) -> bool:
        return _has_directive_comment_pattern(self.directive_comment_patterns, comment)

    def find_comment_spans(self, text: str) -> list[Span]:
        source = text.encode(errors="surrogateescape")
        tree = self.parser.parse(source)
        if tree.root_node.has_error:
            raise UnparsableSourceError
        spans = []
        pending = [tree.root_node]
        while pending:
            node = pending.pop()
            if "comment" in node.type:
                comment = source[node.start_byte : node.end_byte].decode(errors="replace")
                if not self._is_directive_comment(comment):
                    spans.append((node.start_byte, node.end_byte))
                continue
            pending.extend(node.children)
        return sorted(spans)


def _list_line_start_offsets(source: bytes) -> list[int]:
    offsets = [0]
    for line in source.split(_NEWLINE)[:-1]:
        offsets.append(offsets[-1] + len(line) + 1)
    return offsets


@dataclass(frozen=True)
class _PythonTargetLanguage:
    directive_comment_patterns: tuple[str, ...]

    def _is_directive_comment(self, comment: str) -> bool:
        return comment.startswith("#!") or _has_directive_comment_pattern(self.directive_comment_patterns, comment)

    def find_comment_spans(self, text: str) -> list[Span]:
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
                if token.type == tokenize.COMMENT and not self._is_directive_comment(token.string):
                    spans.append(
                        (
                            calculate_byte_offset_from_character(*token.start),
                            calculate_byte_offset_from_character(*token.end),
                        )
                    )
            tree = ast.parse(text)
        except (tokenize.TokenError, SyntaxError, ValueError) as error:
            raise UnparsableSourceError from error
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


_TYPESCRIPT_DIRECTIVE_COMMENT_PATTERNS = (
    r"@ts-[a-z-]+",
    r"eslint-(?:disable|enable)",
    r"prettier-ignore",
    r"(?:istanbul|c8|v8) ignore",
    r"<reference ",
)
_TYPESCRIPT = _TreeSitterTargetLanguage(
    tree_sitter_typescript.language_typescript, _TYPESCRIPT_DIRECTIVE_COMMENT_PATTERNS
)
_TSX = _TreeSitterTargetLanguage(tree_sitter_typescript.language_tsx, _TYPESCRIPT_DIRECTIVE_COMMENT_PATTERNS)
_JAVASCRIPT = _TreeSitterTargetLanguage(tree_sitter_javascript.language, _TYPESCRIPT_DIRECTIVE_COMMENT_PATTERNS)
_GO = _TreeSitterTargetLanguage(tree_sitter_go.language, (r"go:", r"\+build ", r"nolint"))
_DART = _TreeSitterTargetLanguage(tree_sitter_dart.language, (r"ignore:", r"ignore_for_file:"))
_CSHARP = _TreeSitterTargetLanguage(tree_sitter_c_sharp.language, (r"ReSharper (?:disable|restore)",))
_KOTLIN = _TreeSitterTargetLanguage(tree_sitter_kotlin.language, (r"noinspection", r"ktlint-(?:disable|enable)"))
_TERRAFORM = _TreeSitterTargetLanguage(tree_sitter_hcl.language, (r"tflint-ignore", r"checkov:"))
_PYTHON = _PythonTargetLanguage((r"type:", r"noqa", r"pragma:", r"-\*- coding"))

_TARGET_LANGUAGE_BY_SUFFIX: dict[str, _TargetLanguage] = {
    ".ts": _TYPESCRIPT,
    ".mts": _TYPESCRIPT,
    ".cts": _TYPESCRIPT,
    ".tsx": _TSX,
    ".js": _JAVASCRIPT,
    ".jsx": _JAVASCRIPT,
    ".mjs": _JAVASCRIPT,
    ".cjs": _JAVASCRIPT,
    ".go": _GO,
    ".dart": _DART,
    ".cs": _CSHARP,
    ".kt": _KOTLIN,
    ".kts": _KOTLIN,
    ".tf": _TERRAFORM,
    ".tfvars": _TERRAFORM,
    ".py": _PYTHON,
}


def _calculate_removal_span(source: bytes, start: int, end: int) -> Span:
    line_start = source.rfind(_NEWLINE, 0, start) + 1
    line_end = source.find(_NEWLINE, end)
    if line_end == -1:
        line_end = len(source)
    has_code_before = bool(source[line_start:start].strip(_HORIZONTAL_SPACES))
    has_code_after = bool(source[end:line_end].strip(_LINE_END_SPACES))
    if not has_code_before and not has_code_after:
        return line_start, min(line_end + 1, len(source))
    if has_code_before:
        while start > line_start and source[start - 1] in _HORIZONTAL_SPACES:
            start -= 1
        return start, end
    while end < line_end and source[end] in _HORIZONTAL_SPACES:
        end += 1
    return start, end


def _remove_comment_spans(source: bytes, spans: Sequence[Span]) -> bytes:
    result = bytearray()
    position = 0
    for start, end in spans:
        removal_start, removal_end = _calculate_removal_span(source, start, end)
        result += source[position : max(position, removal_start)]
        position = max(position, removal_end)
    result += source[position:]
    return bytes(result)


def _remove_comments_from_text(target_language: _TargetLanguage, text: str) -> bytes:
    source = text.encode(errors="surrogateescape")
    return _remove_comment_spans(source, target_language.find_comment_spans(text))


def is_code_change(path: str, before: CommittedFile | None, after: CommittedFile | None) -> bool:
    """ファイルの変更前後から、コードの変更に数えるかを返す。

    Args:
        path: ファイルのパス。拡張子で対象言語を決める。
        before: 変更前のファイル。ファイルが無い (追加された) ときは None。
        after: 変更後のファイル。ファイルが無い (削除された) ときは None。

    Raises:
        UnparsableSourceError: 内容の比較に必要な、対象言語のソースを解析できない。
    """
    if before is None or after is None or before.file_mode != after.file_mode:
        return True
    target_language = _TARGET_LANGUAGE_BY_SUFFIX.get(PurePosixPath(path).suffix)
    if target_language is None:
        return before.content != after.content
    return _remove_comments_from_text(target_language, before.content) != _remove_comments_from_text(
        target_language, after.content
    )
