from pathlib import Path

from change_detection.domain.change_detection_result import ChangeDetectionResult


def write_output_file(path: Path, result: ChangeDetectionResult) -> None:
    """変更判定の結果を、`changed=true|false` と `<範囲名>=true|false` の行で出力ファイルに書く。"""
    lines = [f"changed={_format_boolean(result.has_code_change)}"]
    lines += [f"{name}={_format_boolean(has_code_change)}" for name, has_code_change in result.scopes.items()]
    with path.open("a", encoding="utf-8") as output_file:
        output_file.write("\n".join(lines) + "\n")


def _format_boolean(value: bool) -> str:
    return "true" if value else "false"
