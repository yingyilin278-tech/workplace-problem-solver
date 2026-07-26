#!/usr/bin/env python3
"""Validate L2 core-book knowledge cards and their Skill routing."""

from __future__ import annotations

import json
import re
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
REFERENCE_DIR = SKILL_DIR / "references"
KNOWLEDGE_DIR = REFERENCE_DIR / "knowledge"
TEST_DIR = SKILL_DIR / "tests"

REQUIRED_HEADINGS = {
    "## Source status",
    "## Required user information",
    "## Applicable roles, power, and culture",
    "## Core claims",
    "## Decision rules",
    "## Action steps",
    "## Ready-to-use wording",
    "## Counterexamples",
    "## Contraindications",
    "## Conflicts and limitations",
    "## Case validation",
}


def main() -> int:
    errors: list[str] = []
    library = (REFERENCE_DIR / "book-library.md").read_text(encoding="utf-8")
    expected_ids = {
        match.group(1)
        for line in library.splitlines()
        if (
            match := re.match(
                r"\| (B\d{2,3}) \| .* \| L2(?:；[^|]*)? \|",
                line,
            )
        )
    }
    cards: dict[str, str] = {}
    for path in sorted(KNOWLEDGE_DIR.glob("book-b*.md")):
        match = re.fullmatch(r"book-(b\d{2,3})\.md", path.name)
        if not match:
            continue
        book_id = match.group(1).upper()
        cards[book_id] = path.read_text(encoding="utf-8")

    missing_cards = expected_ids - set(cards)
    extra_cards = set(cards) - expected_ids
    if missing_cards:
        errors.append(
            f"card IDs mismatch: missing={sorted(missing_cards)}"
        )

    for book_id in sorted(expected_ids):
        content = cards.get(book_id, "")
        if not content:
            continue
        missing = sorted(
            heading for heading in REQUIRED_HEADINGS if heading not in content
        )
        if missing:
            errors.append(f"{book_id} missing headings: {missing}")
        if "Enablement level: L2" not in content:
            errors.append(f"{book_id} is not marked L2")
        if "http" not in content:
            errors.append(f"{book_id} has no traceable source URL")
        if "## Decision rules\n\n-" not in content:
            errors.append(f"{book_id} has no decision rule")
        if "## Counterexamples\n\n-" not in content:
            errors.append(f"{book_id} has no counterexample")

    source_map = (REFERENCE_DIR / "source-selection-map.md").read_text(
        encoding="utf-8"
    )
    conflict_matrix = (REFERENCE_DIR / "core-book-conflicts.md").read_text(
        encoding="utf-8"
    )

    for book_id in expected_ids:
        library_line = next(
            (
                line
                for line in library.splitlines()
                if line.startswith(f"| {book_id} |")
            ),
            "",
        )
        if "L2" not in library_line:
            errors.append(f"{book_id} catalog level is not L2")
        if book_id not in source_map:
            errors.append(f"{book_id} missing from source selection map")

    if "直接对话 vs 先留证据和走正式渠道" not in conflict_matrix:
        errors.append("conflict matrix missing high-risk dialogue gate")
    if "个人调节 vs 工作设计改变" not in conflict_matrix:
        errors.append("conflict matrix missing burnout gate")
    if "普遍管理框架 vs 中国大陆劳动制度" not in conflict_matrix:
        errors.append("conflict matrix missing jurisdiction gate")

    summary = {
        "status": "PASS" if not errors else "FAIL",
        "l2_book_count": len(expected_ids),
        "card_count": len(expected_ids & set(cards)),
        "ignored_non_l2_cards": sorted(extra_cards),
        "required_heading_count": len(REQUIRED_HEADINGS),
        "catalog_l2_count": sum(
            1
            for book_id in expected_ids
            if "L2"
            in next(
                (
                    line
                    for line in library.splitlines()
                    if line.startswith(f"| {book_id} |")
                ),
                "",
            )
        ),
        "checks": [
            "traceable source",
            "source access scope",
            "decision rules",
            "action steps",
            "ready-to-use wording",
            "counterexamples",
            "contraindications",
            "rule conflict matrix",
            "category routing",
        ],
        "not_tested": [
            "full-text fidelity where full text was unavailable",
            "real-world adoption effect",
            "local legal conclusion",
        ],
        "errors": errors,
    }

    TEST_DIR.mkdir(parents=True, exist_ok=True)
    (TEST_DIR / "core-book-distillation-results.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    report = [
        "# L2书籍蒸馏校验",
        "",
        f"- 结果：**{summary['status']}**",
        f"- L2书籍：{summary['l2_book_count']}本",
        f"- 知识卡：{summary['card_count']}张",
        f"- L2目录状态：{summary['catalog_l2_count']}本",
        "- 已检查：来源、访问层级、判断规则、行动、话术、反例、禁用条件、冲突矩阵和类别路由",
        "- 尚未证明：未获全文书籍的全文一致性、真实采用效果、属地法律结论",
        "",
    ]
    if errors:
        report.extend(["## 错误", "", *[f"- {error}" for error in errors]])
    (TEST_DIR / "core-book-distillation-report.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
