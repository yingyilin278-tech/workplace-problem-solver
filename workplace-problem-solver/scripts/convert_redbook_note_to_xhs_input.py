#!/usr/bin/env python3
"""Convert redbook note JSON into workplace xhs-content-input schema."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def load_json_payload(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    stripped = raw.lstrip()
    if stripped.startswith("{"):
        return json.loads(stripped)
    start = raw.find("{")
    if start == -1:
        raise ValueError(f"No JSON object found in {path}")
    return json.loads(raw[start:])


def detect_text_basis(payload: dict) -> str:
    note_type = (payload.get("type") or "").lower()
    if note_type == "video":
        return "详情页正文"
    return "详情页正文"


def detect_evidence_level(text: str) -> str:
    if len(text.strip()) >= 280:
        return "X1"
    if len(text.strip()) >= 80:
        return "X2"
    return "X3"


def build_item(payload: dict, captured_at: str | None) -> dict:
    text = (payload.get("desc") or "").strip()
    raw_type = (payload.get("type") or "note").lower()
    content_type = "note" if raw_type == "normal" else raw_type
    return {
        "content_id": payload.get("note_id") or payload.get("id") or "unknown-note-id",
        "title": payload.get("title") or "未命名小红书内容",
        "author": (payload.get("user") or {}).get("nickname") or "未知作者",
        "url": payload.get("webUrl") or "",
        "content_type": content_type,
        "text_basis": detect_text_basis(payload),
        "captured_at": captured_at or date.today().isoformat(),
        "evidence_level": detect_evidence_level(text),
        "text": text,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Path to redbook read --json output")
    parser.add_argument("output", help="Path to xhs-content-input json")
    parser.add_argument("--captured-at", dest="captured_at", help="Override capture date")
    args = parser.parse_args()

    src = Path(args.input)
    dst = Path(args.output)
    payload = load_json_payload(src)
    item = build_item(payload, args.captured_at)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(
        json.dumps({"items": [item]}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(dst),
                "content_id": item["content_id"],
                "title": item["title"],
                "evidence_level": item["evidence_level"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
