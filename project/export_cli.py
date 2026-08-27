from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import cast

from loguru import logger

from project import __version__
from project.agent_output import error_json
from project.export import (
    ExportDependencyError,
    ExportError,
    ExportFormat,
    export_result,
)


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="douyin-export",
        description="将已保存的采集结果导出为 Word、Markdown 或纯文本。",
    )
    parser.add_argument("result", type=Path, help="采集结果 JSON 文件")
    parser.add_argument(
        "--format",
        dest="output_format",
        choices=("docx", "markdown", "text"),
        default="docx",
        help="导出格式（默认 docx）",
    )
    parser.add_argument("--output", type=Path, help="导出文件路径")
    parser.add_argument("--run-dir", type=Path, help="原始/清理转写副本的保存目录")
    parser.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    parser.add_argument("--version", action="version", version=__version__)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_argument_parser().parse_args(argv)
    output_format = cast(ExportFormat, args.output_format)
    try:
        report = export_result(
            args.result,
            output_path=args.output,
            output_format=output_format,
            run_dir=args.run_dir,
        )
    except ExportDependencyError as exc:
        return _emit_error(args, exc, "pip install -e '.[word]'")
    except ExportError as exc:
        return _emit_error(args, exc)
    except OSError as exc:
        return _emit_error(args, exc)

    payload = {
        "schema_version": "1.0",
        "ok": True,
        "format": report.format,
        "output_file": str(report.output_path),
        "run_dir": str(report.run_dir),
        "videos": report.videos,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
    else:
        print(f"导出完成：{report.output_path}")
        print(f"条目数量：{report.videos}")
        print(f"转写副本：{report.run_dir}")
    return 0


def _emit_error(
    args: argparse.Namespace,
    error: BaseException,
    fix_command: str | None = None,
) -> int:
    logger.error("导出失败: {}", error)
    if args.json:
        print(error_json(error, f"导出失败: {error}", fix_command=fix_command))
    return 1


def run() -> None:
    raise SystemExit(main())


if __name__ == "__main__":
    run()
