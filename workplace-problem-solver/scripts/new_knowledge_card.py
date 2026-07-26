#!/usr/bin/env python3
"""Create a traceable workplace knowledge-card scaffold."""

from __future__ import annotations

import argparse
from pathlib import Path


SOURCE_TYPES = ("book", "paper", "video", "interview", "policy", "article", "other")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True)
    parser.add_argument("--creator", required=True)
    parser.add_argument("--source-type", required=True, choices=SOURCE_TYPES)
    parser.add_argument("--source", required=True, help="URL or local path")
    parser.add_argument("--published", default="unknown")
    parser.add_argument("--library-id", default="unassigned")
    parser.add_argument("--edition", default="unknown")
    parser.add_argument("--jurisdiction", default="general")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite an existing output file.",
    )
    return parser.parse_args()


def render(args: argparse.Namespace) -> str:
    return f"""# {args.title}

## 来源

- 作者或讲者：{args.creator}
- 书库 ID：{args.library_id}
- 类型：{args.source_type}
- 发布日期：{args.published}
- 版本：{args.edition}
- 适用国家或地区：{args.jurisdiction}
- 链接或路径：{args.source}
- 证据等级：待评估
- 启用等级：L0
- 作者角色与潜在偏差：待评估
- 使用限制：待核验

## 核心主张

- 待蒸馏。每条只写一个可判断的观点。

## 适用场景

- 待填写对应的职场问题标签。

## 诊断问题

1. 待填写用于判断是否适用的问题。

## 判断规则

- 如果___，那么___，除非___。

## 行动步骤

1. 待填写用户今天可以完成的动作。

## 可直接使用的话术

- 对象：待填写。
- 渠道与时机：待填写。

> 待填写可复制表达。

## 失败信号与边界

- 待填写不适用条件、风险和停止信号。

## 反例、失败案例或争议

- 待查找独立来源或反例。

## 规则冲突

- 待记录与其他书籍、论文、制度或案例相冲突的地方。

## 案例验证

- 通过案例 ID：无。
- 失败案例 ID：无。

## 关联标签

- 待填写。
"""


def main() -> int:
    args = parse_args()
    output = args.output.expanduser().resolve()
    if output.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite existing file: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(args), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
