#!/usr/bin/env python3
"""Build and validate a combined workplace and job-search evaluation bank."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = SKILL_DIR.parent
LOCAL_DATASET = SKILL_DIR / "data" / "justoneapi-workplace-2026-07-23" / "questions-100-with-text.json"
EXTERNAL_DATASET = (
    WORKSPACE_DIR
    / "data"
    / "justoneapi-workplace-2026-07-23"
    / "questions-100-with-text.json"
)
DEFAULT_DATASET = LOCAL_DATASET if LOCAL_DATASET.exists() else EXTERNAL_DATASET
DEFAULT_JOB_DATASET = SKILL_DIR / "tests" / "job-search-case-bank.json"
DEFAULT_SUPPLEMENTAL_DATASET = SKILL_DIR / "tests" / "supplemental-case-bank.json"
DEFAULT_TEST_DIR = SKILL_DIR / "tests"

OUTPUT_SECTIONS = ["判断", "建议", "话术", "后续", "风险"]

CATEGORY_SOURCES = {
    "C1": ["B01", "B02", "B06", "B34", "P01", "P07", "V02", "V04"],
    "C2": ["B01", "B05", "B12", "B15", "P02", "P06", "V01", "V04"],
    "C3": ["B01", "B08", "B11", "B12", "P05", "P08", "V02", "V03"],
    "C4": ["B02", "B10", "B47", "B57", "P05", "P06", "P07", "V01", "V02"],
    "C5": ["B04", "B06", "B34", "B35", "P03", "P07", "V03", "V04"],
    "C6": ["B01", "B20", "B21", "B23", "P01", "P07", "V02", "V04"],
    "C7": ["B03", "B27", "B29", "B63", "P04", "P07", "V02", "V05"],
    "C8": ["B03", "B33", "B42", "B48", "P01", "P07", "V04", "V05"],
    "C9": ["B01", "B29", "B70", "B75", "P04", "P07", "V03"],
    "C10": ["B01", "B12", "B35", "B37", "P03", "P08", "V01", "V03"],
    "C11": ["B02", "B40", "B46", "B48", "P03", "P07", "V04"],
    "C12": ["B05", "B13", "B50", "B53", "P05", "P06", "P07", "V01", "V05"],
    "J1": ["B32", "B46", "B48", "B49", "P07", "V04"],
    "J2": ["B03", "B21", "B23", "B44", "P07", "V02"],
    "J3": ["B20", "B23", "B44", "B99", "P07", "V02"],
    "J4": ["B20", "B21", "B22", "B23", "P01", "V02"],
    "J5": ["B01", "B08", "B20", "B99", "P07", "V03"],
    "J6": ["B02", "B16", "B32", "B46", "P07", "V04"],
    "J7": ["B03", "B44", "B48", "B96", "P07", "V04"],
}

INTAKE_FIELDS = {
    "C1": ["任务来源", "现有任务", "期限", "验收标准", "优先级决策人"],
    "C2": ["具体行为", "持续时间", "影响范围", "评价标准", "权益动作"],
    "C3": ["分工", "时间线", "成果载体", "汇报对象", "原始记录"],
    "C4": ["共同目标", "依赖关系", "责任人", "截止时间", "升级人"],
    "C5": ["职责范围", "工作量", "加班频率", "补偿安排", "健康影响"],
    "C6": ["汇报对象", "决策目的", "结果证据", "风险", "请求"],
    "C7": ["事前标准", "实际结果", "评价人", "书面反馈", "申诉流程"],
    "C8": ["目标方向", "能力资产", "晋升标准", "市场可迁移性", "决策期限"],
    "C9": ["地区", "合同制度", "书面文件", "签字期限", "历史绩效"],
    "C10": ["触发事件", "持续时间", "行为信号", "功能影响", "支持资源"],
    "C11": ["离职原因", "现金缓冲", "健康状态", "下一方向", "家庭约束"],
    "C12": ["管理权限", "目标标准", "行为频率", "已给反馈", "资源差距"],
    "J1": ["目标岗位", "当前筹码", "约束条件", "时间压力", "求职优先级"],
    "J2": ["项目经历", "具体动作", "结果证据", "角色边界", "可复用素材"],
    "J3": ["目标JD", "现有简历", "岗位关键词", "硬要求", "匹配证据"],
    "J4": ["目标场景", "项目背景", "难点", "结果", "个人贡献"],
    "J5": ["岗位", "轮次", "已知题目", "薄弱点", "准备时长"],
    "J6": ["offer列表", "薪资结构", "岗位职责", "团队阶段", "决策底线"],
    "J7": ["挂掉轮次", "面试问题", "回答内容", "反馈", "后续目标岗位"],
}

HIGH_RISK_PATTERN = re.compile(
    r"PIP|裁员|辞退|解除|调岗|降薪|不续约|逼签|仲裁|合同|补偿|"
    r"骚扰|歧视|威胁|暴力|发烧|失眠|安眠药|胸口|健康红线|身体",
    re.IGNORECASE,
)
MEDIUM_RISK_PATTERN = re.compile(
    r"穿小鞋|报复|公开羞辱|打压|PUA|绩效不公|排挤|超负荷|长期加班|裸辞",
    re.IGNORECASE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--job-dataset", type=Path, default=DEFAULT_JOB_DATASET)
    parser.add_argument("--supplemental-dataset", type=Path, default=DEFAULT_SUPPLEMENTAL_DATASET)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_TEST_DIR)
    return parser.parse_args()


def risk_level(category_id: str, question: str) -> str:
    if category_id == "C9" or HIGH_RISK_PATTERN.search(question):
        return "high"
    if MEDIUM_RISK_PATTERN.search(question):
        return "medium"
    return "low"


def read_reference(name: str) -> str:
    return (SKILL_DIR / "references" / name).read_text(encoding="utf-8")


def validate_reference_coverage(category_ids: list[str]) -> list[str]:
    errors: list[str] = []
    workplace_references = {
        "problem-taxonomy.md": read_reference("problem-taxonomy.md"),
        "intake-requirements.md": read_reference("intake-requirements.md"),
        "decision-rules.md": read_reference("decision-rules.md"),
    }
    job_references = {
        "problem-taxonomy.md": workplace_references["problem-taxonomy.md"],
        "intake-requirements.md": workplace_references["intake-requirements.md"],
        "decision-rules.md": workplace_references["decision-rules.md"],
        "job-search-skill-integration.md": read_reference("job-search-skill-integration.md"),
    }
    source_selection_map = read_reference("source-selection-map.md")
    for category_id in category_ids:
        references = workplace_references if category_id.startswith("C") else job_references
        for filename, content in references.items():
            if category_id not in content:
                errors.append(f"{category_id} missing from {filename}")
        if category_id.startswith("C") and category_id not in source_selection_map:
            errors.append(f"{category_id} missing from source-selection-map.md")
    return errors


def build_case(item: dict) -> dict:
    category_id = item["category_id"]
    risk = risk_level(category_id, item["question"])
    return {
        "case_id": item["id"],
        "prompt": item["question"],
        "expected": {
            "primary_category": category_id,
            "category_name": item["category"],
            "risk_level": risk,
            "required_intake_fields": INTAKE_FIELDS[category_id],
            "required_output_sections": OUTPUT_SECTIONS,
            "candidate_source_ids": CATEGORY_SOURCES[category_id],
            "must_use_risk_boundary": risk == "high",
            "must_include_ready_to_use_wording": True,
            "must_distinguish_fact_and_inference": True,
        },
        "source_trace": {
            "note_id": item["source_note_id"],
            "note_text": item["source_note_text"],
            "comment_text": item["related_comments"][0]["text"],
        },
    }


def main() -> int:
    args = parse_args()
    dataset = json.loads(args.dataset.read_text(encoding="utf-8"))
    job_dataset = json.loads(args.job_dataset.read_text(encoding="utf-8"))
    supplemental_dataset = json.loads(args.supplemental_dataset.read_text(encoding="utf-8"))
    questions = (
        dataset["questions"]
        + job_dataset["questions"]
        + supplemental_dataset["questions"]
    )
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    cases = [build_case(item) for item in questions]
    category_counts = Counter(
        case["expected"]["primary_category"] for case in cases
    )
    risk_counts = Counter(case["expected"]["risk_level"] for case in cases)
    errors: list[str] = []

    expected_case_count = len(questions)
    if len(cases) != expected_case_count:
        errors.append(f"expected {expected_case_count} cases, got {len(cases)}")
    if len({case["case_id"] for case in cases}) != len(cases):
        errors.append("duplicate case IDs")
    if len({case["prompt"] for case in cases}) != len(cases):
        errors.append("duplicate prompts")
    if set(category_counts) != set(CATEGORY_SOURCES):
        errors.append(
            f"category mismatch: got {sorted(category_counts)}, "
            f"expected {sorted(CATEGORY_SOURCES)}"
        )

    errors.extend(validate_reference_coverage(sorted(CATEGORY_SOURCES)))

    for case in cases:
        expected = case["expected"]
        if expected["required_output_sections"] != OUTPUT_SECTIONS:
            errors.append(f"{case['case_id']} output contract mismatch")
        if len(expected["required_intake_fields"]) < 5:
            errors.append(f"{case['case_id']} insufficient intake fields")
        if not any(
            source.startswith("B") for source in expected["candidate_source_ids"]
        ):
            errors.append(f"{case['case_id']} missing book source")
        if not any(
            source.startswith("P") for source in expected["candidate_source_ids"]
        ):
            errors.append(f"{case['case_id']} missing paper source")
        if not any(
            source.startswith("V") for source in expected["candidate_source_ids"]
        ):
            errors.append(f"{case['case_id']} missing video source")
        if not case["source_trace"]["note_text"]:
            errors.append(f"{case['case_id']} missing note text")
        if not case["source_trace"]["comment_text"]:
            errors.append(f"{case['case_id']} missing comment text")

    case_bank_path = output_dir / f"case-bank-{expected_case_count}.jsonl"
    case_bank_path.write_text(
        "".join(json.dumps(case, ensure_ascii=False) + "\n" for case in cases),
        encoding="utf-8",
    )

    summary = {
        "status": "PASS" if not errors else "FAIL",
        "scope": "routing, intake, source selection, risk gate, output contract",
        "not_tested": [
            "LLM逐题生成答案后的事实准确性",
            "话术自然度和实际采用效果",
            "当地法律结论",
        ],
        "case_count": len(cases),
        "legacy_workplace_case_count": len(dataset["questions"]),
        "job_search_case_count": len(job_dataset["questions"]),
        "supplemental_case_count": len(supplemental_dataset["questions"]),
        "unique_prompt_count": len({case["prompt"] for case in cases}),
        "category_count": len(category_counts),
        "category_distribution": dict(sorted(category_counts.items())),
        "risk_distribution": dict(sorted(risk_counts.items())),
        "output_sections": OUTPUT_SECTIONS,
        "reference_coverage": {
            "taxonomy": len(CATEGORY_SOURCES),
            "intake_requirements": len(CATEGORY_SOURCES),
            "decision_rules": len(CATEGORY_SOURCES),
            "source_selection": 12,
            "job_search_integration": 7,
        },
        "errors": errors,
    }
    results_path = output_dir / f"baseline-results-{expected_case_count}.json"
    results_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    report_lines = [
        f"# {expected_case_count}案例基线测试",
        "",
        f"- 结果：**{summary['status']}**",
        f"- 案例：{summary['case_count']}个，唯一问法{summary['unique_prompt_count']}个",
        f"- 类别：{summary['category_count']}类",
        f"- 在职案例：{summary['legacy_workplace_case_count']}个；求职案例：{summary['job_search_case_count']}个；补充案例：{summary['supplemental_case_count']}个",
        f"- 风险分布：{dict(sorted(risk_counts.items()))}",
        "- 测试范围：路由、必问信息、资料选择、风险分流、五段输出协议",
        "- 尚未测试：逐题答案事实准确性、话术自然度、真实采用效果和当地法律结论",
        "",
        "## 类别覆盖",
        "",
        "| 类别 | 案例数 |",
        "|---|---:|",
        *[
            f"| {category_id} | {count} |"
            for category_id, count in sorted(category_counts.items())
        ],
        "",
        "## 验收门槛",
        "",
        f"- {expected_case_count}个案例和{expected_case_count}个唯一问法",
        "- C1-C12 与 J1-J7 全部有案例",
        "- 每类均有必问信息、判断规则和书籍/论文/视频候选",
        "- 每题固定判断—建议—话术—后续—风险",
        "- 高风险题必须加载风险边界",
        "",
    ]
    if errors:
        report_lines.extend(["## 错误", "", *[f"- {error}" for error in errors]])
    report_path = output_dir / f"baseline-report-{expected_case_count}.md"
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
