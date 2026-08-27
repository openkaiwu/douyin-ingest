"""Backward-compatible wrapper for the public ``douyin-export`` command."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from project.export import export_result


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="将 output/result.json 导出为 Word 文档。")
    parser.add_argument("--result", type=Path, default=ROOT / "output" / "result.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = export_result(args.result, output_path=args.output, output_format="docx")
    print(
        json.dumps(
            {
                "output": str(report.output_path),
                "run_dir": str(report.run_dir),
                "videos": report.videos,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
