from __future__ import annotations

import json
import zipfile
from datetime import UTC, datetime
from pathlib import Path

from project.export import clean_transcript, export_result
from project.models import CrawlResult, Transcription, TranscriptionSegment, UserProfile, Video


def _write_result(tmp_path: Path) -> Path:
    transcript = tmp_path / "transcripts" / "1.txt"
    transcript.parent.mkdir()
    transcript.write_text(
        "[00:00.000] 嗯，今天我们聊聊大脑。\n(音乐)\n\n结论很简单。\n",
        encoding="utf-8",
    )
    video = Video(
        aweme_id="1",
        title="测试标题 😀",
        publish_time=datetime(2026, 8, 27, 8, 0, tzinfo=UTC),
        video_url="https://www.douyin.com/video/1",
        transcription=Transcription(
            text="今天我们聊聊大脑。",
            language="zh",
            duration=3,
            model="base",
            segments=[TranscriptionSegment(id=0, start=0, end=3, text="今天我们聊聊大脑。")],
            transcript_file=str(transcript),
            segments_file=str(tmp_path / "transcripts" / "1.segments.json"),
        ),
    )
    result = CrawlResult(
        source_url="https://www.douyin.com/user/test",
        user=UserProfile(nickname="测试账号", sec_user_id="test"),
        total_works=1,
        top1=video,
        top10=[video],
        videos=[video],
        crawled_at=datetime.now(UTC),
    )
    path = tmp_path / "result.json"
    path.write_text(
        json.dumps(result.model_dump(mode="json"), ensure_ascii=False),
        encoding="utf-8",
    )
    return path


def test_clean_transcript_removes_timestamps_noise_and_emoji() -> None:
    cleaned = clean_transcript("[00:01.200] 嗯，今天开始。\n(音乐)\n结论很简单。😀")
    assert cleaned == "今天开始。\n结论很简单。"


def test_export_markdown_preserves_sidecars_and_metadata(tmp_path: Path) -> None:
    result_path = _write_result(tmp_path)
    report = export_result(
        result_path,
        output_path=tmp_path / "out" / "口播.md",
        output_format="markdown",
    )

    assert report.videos == 1
    assert report.output_path.read_text(encoding="utf-8").startswith("# 测试账号_全部口播文案")
    assert "发布时间：2026-08-27 16:00" in report.output_path.read_text(encoding="utf-8")
    markdown = report.output_path.read_text(encoding="utf-8")
    assert "视频链接：https://www.douyin.com/video/1" in markdown
    item_dir = report.run_dir / "videos" / "1"
    assert (item_dir / "transcript_raw.txt").read_text(encoding="utf-8").startswith("[00:00.000]")
    assert (item_dir / "transcript_clean.txt").read_text(encoding="utf-8") == (
        "今天我们聊聊大脑。\n结论很简单。"
    )


def test_export_docx_contains_a_clickable_video_link(tmp_path: Path) -> None:
    result_path = _write_result(tmp_path)
    report = export_result(
        result_path,
        output_path=tmp_path / "out" / "口播.docx",
        output_format="docx",
    )

    with zipfile.ZipFile(report.output_path) as archive:
        document_xml = archive.read("word/document.xml").decode("utf-8")
        relationships = archive.read("word/_rels/document.xml.rels").decode("utf-8")
    assert "测试账号_全部口播文案" in document_xml
    assert "视频链接：" in document_xml
    assert "https://www.douyin.com/video/1" in relationships
