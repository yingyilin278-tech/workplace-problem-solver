#!/usr/bin/env python3
"""Compile validated core-book research JSON into Skill knowledge cards."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = SKILL_DIR.parent
DEFAULT_INPUT_DIR = WORKSPACE_DIR / "book-research" / "results"
DEFAULT_OUTPUT_DIR = SKILL_DIR / "references" / "knowledge"

REQUIRED_FIELDS = {
    "book_id",
    "original_title",
    "author",
    "edition",
    "official_sources",
    "source_access_status",
    "coverage_codes",
    "required_user_information",
    "applicable_roles",
    "power_asymmetry",
    "jurisdiction_and_culture",
    "core_claims",
    "decision_rules",
    "action_steps",
    "ready_to_use_wording",
    "counterexamples",
    "contraindications",
    "evidence_tier",
    "author_bias_and_conflicts",
    "rule_conflicts",
    "copyright_scope",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else [value]


def bullet_lines(value: Any) -> str:
    return "\n".join(f"- {item}" for item in as_list(value))


def numbered_lines(value: Any) -> str:
    return "\n".join(
        f"{index}. {item}" for index, item in enumerate(as_list(value), start=1)
    )


def wording_lines(value: Any) -> str:
    lines: list[str] = []
    for item in as_list(value):
        if isinstance(item, dict):
            audience = item.get("audience", "unspecified audience")
            channel = item.get("channel", "unspecified channel")
            timing = item.get("timing", "unspecified timing")
            wording = item.get("wording", "")
            lines.extend(
                [
                    f"- Audience: {audience}",
                    f"- Channel and timing: {channel}; {timing}",
                    "",
                    f"> {wording}",
                    "",
                ]
            )
        else:
            lines.append(f"- {item}")
    return "\n".join(lines).rstrip()


def render(book: dict[str, Any]) -> str:
    authors = "; ".join(str(x) for x in as_list(book["author"]))
    coverage = ", ".join(str(x) for x in as_list(book["coverage_codes"]))
    sources = bullet_lines(book["official_sources"])
    uncertain = bullet_lines(book.get("uncertain", [])) or "- None recorded."
    return f"""# {book["book_id"]} — {book["original_title"]}

## Source status

- Enablement level: L2, pending case validation
- Authors and roles: {authors}
- Edition: {book["edition"]}
- Access scope: {book["source_access_status"]}
- Evidence tier: {book["evidence_tier"]}
- Coverage: {coverage}

Official sources:

{sources}

## Required user information

{bullet_lines(book["required_user_information"])}

## Applicable roles, power, and culture

Applicable roles:

{bullet_lines(book["applicable_roles"])}

Power asymmetry:

{book["power_asymmetry"]}

Jurisdiction and cultural transfer:

{book["jurisdiction_and_culture"]}

## Core claims

{bullet_lines(book["core_claims"])}

## Decision rules

{bullet_lines(book["decision_rules"])}

## Action steps

{numbered_lines(book["action_steps"])}

## Ready-to-use wording

{wording_lines(book["ready_to_use_wording"])}

## Counterexamples

{bullet_lines(book["counterexamples"])}

## Contraindications

{bullet_lines(book["contraindications"])}

## Conflicts and limitations

- Author bias and conflicts: {book["author_bias_and_conflicts"]}
- Rule conflicts: {book["rule_conflicts"]}
- Copyright scope: {book["copyright_scope"]}

## Uncertain

{uncertain}

## Case validation

- Status: pending
- Passed case IDs: none
- Failed case IDs: none
"""


def main() -> int:
    args = parse_args()
    input_dir = args.input_dir.resolve()
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    books: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for path in sorted(input_dir.glob("*_batch_*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            errors.append(f"{path.name}: expected a JSON list")
            continue
        for item in data:
            if not isinstance(item, dict) or "book_id" not in item:
                continue
            missing = sorted(
                field for field in REQUIRED_FIELDS if not item.get(field)
            )
            if missing:
                errors.append(
                    f"{path.name}:{item.get('book_id', 'unknown')} missing {missing}"
                )
                continue
            books[item["book_id"]] = item

    if errors:
        raise SystemExit("\n".join(errors))

    for book_id, book in sorted(books.items()):
        output = output_dir / f"book-{book_id.lower()}.md"
        output.write_text(render(book), encoding="utf-8")

    print(
        json.dumps(
            {
                "status": "PASS",
                "book_count": len(books),
                "output_dir": str(output_dir),
                "book_ids": sorted(books),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
