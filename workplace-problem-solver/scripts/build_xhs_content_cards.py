#!/usr/bin/env python3
"""Build xiaohongshu content-level knowledge cards from extracted note text."""

from __future__ import annotations

import json
import re
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
PACKAGE_DIR = SKILL_DIR.parent
LOCAL_DATA_DIR = SKILL_DIR / "data"
EXTERNAL_DATA_DIR = PACKAGE_DIR / "data"
INPUT_DIR = (
    LOCAL_DATA_DIR / "xhs-content-input"
    if (LOCAL_DATA_DIR / "xhs-content-input").exists()
    else EXTERNAL_DATA_DIR / "xhs-content-input"
)
OUTPUT_DIR = SKILL_DIR / "references" / "xhs-content-knowledge"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


RULES = [
    ("C1", ["加活", "优先级", "任务", "截止", "汇报", "沟通"]),
    ("C2", ["领导", "打压", "pua", "羞辱", "否定"]),
    ("C3", ["同事", "抢功", "甩锅", "背锅", "归属"]),
    ("C5", ["加班", "边界", "工作量", "超载", "拒绝"]),
    ("C6", ["汇报", "表达", "PPT", "存在感", "发言"]),
    ("C7", ["绩效", "工资", "薪资", "评分", "考核"]),
    ("C8", ["晋升", "成长", "转岗", "职业规划"]),
    ("C9", ["PIP", "降薪", "调岗", "裁员", "解除", "仲裁"]),
    ("C10", ["内耗", "情绪", "焦虑", "人际", "排挤"]),
    ("C11", ["离职", "裸辞", "转行", "去留"]),
    ("C12", ["带团队", "管理者", "下属", "辅导", "问责"]),
]


def detect_categories(text: str) -> list[str]:
    lowered = text.lower()
    hit: list[str] = []
    for code, keywords in RULES:
        if any(k.lower() in lowered for k in keywords):
            hit.append(code)
    return hit or ["C6"]


def slug(value: str) -> str:
    value = value.strip()
    result = []
    for ch in value:
        if ch.isalnum() or "\u4e00" <= ch <= "\u9fff":
            result.append(ch)
        else:
            result.append("-")
    return re.sub(r"-+", "-", "".join(result)).strip("-")[:80] or "xhs-content"


def shorten(text: str, limit: int = 220) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit]


def infer_type(source: dict) -> str:
    raw = (source.get("content_type") or source.get("type") or "").lower()
    if "video" in raw or source.get("subtitle"):
        return "视频"
    if raw in {"normal", "note", "image"} or "image" in raw or "note" in raw:
        return "图文"
    return "混合"


def render_card(item: dict) -> str:
    text = item.get("text", "").strip()
    title = item.get("title", "未命名内容")
    author = item.get("author", "未知作者")
    categories = detect_categories(f"{title}\n{text}")
    content_type = infer_type(item)
    source_basis = item.get("text_basis", "正文")
    level = item.get("evidence_level", "X2")
    rule_line = shorten(text, 120)

    return f"""# {title}

## Source status

- Content ID: {item.get("content_id", "未记录")}
- Author: {author}
- URL: {item.get("url", "未记录")}
- Content type: {content_type}
- Text basis: {source_basis}
- Captured at: {item.get("captured_at", "未记录")}
- Evidence level: {level}
- Categories: {", ".join(categories)}

## Core claims

- 该内容围绕 `{title}` 展开，核心可用信息来自已提取正文或字幕，而不是账号定位推断。
- 当前可确认的主张片段：{rule_line}

## Decision rules

- 若用户问题与 `{title}` 对应场景高度一致，可把这条内容作为中文表达和现实案例补充，而不是直接当最终结论。
- 若该内容涉及绩效、裁员、PIP、劳动争议或心理危机，必须回到 `risk-boundaries.md` 和正式规则层复核。

## Action steps

1. 先确认用户问题与本内容是否属于同一类别：{", ".join(categories)}。
2. 提取其中能落地的一条动作，不直接照搬整条内容的情绪或标题。
3. 与 `decision-rules.md` 的主规则比对，保留一致部分，剔除夸张和绝对化表达。

## Ready-to-use wording

- Audience: user-side adaptation; channel: rewritten chat / message; timing: after rule alignment. Wording: "我先按事实把问题讲清，再说明这件事已经影响到什么，最后给你一个明确的下一步。"

## Counterexamples

- 标题强、情绪重，不代表整条内容适合作为正式建议。
- 单条内容常带平台传播目的，不能替代完整证据和正式规则。

## Contraindications

- 只拿到标题、摘要或断裂文本时，不得作为正式候选来源。
- 涉及法律、医疗或严重心理风险时，不得单独依赖本内容卡。

## Evidence excerpt

- {shorten(text, 500)}
"""


def main() -> int:
    files = sorted(INPUT_DIR.glob("*.json"))
    built = []
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        items = data if isinstance(data, list) else data.get("items", [])
        for item in items:
            if not isinstance(item, dict):
                continue
            text = (item.get("text") or "").strip()
            if len(text) < 80:
                continue
            name = slug(f"{item.get('author', '')}-{item.get('title', '')}")
            out = OUTPUT_DIR / f"{name}.md"
            out.write_text(render_card(item), encoding="utf-8")
            built.append(out.name)
    print(json.dumps({"built_count": len(built), "files": built[:20]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
