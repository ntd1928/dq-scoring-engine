"""Report generator — produces Markdown, CSV, and JSON from scoring results."""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

from engine.scorer import DatasetReport


def generate_markdown(reports: List[DatasetReport], output_path: Path) -> None:
    lines = [
        "# DQ Scoring Report",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"**Datasets scored:** {len(reports)}",
        "",
    ]

    for rpt in reports:
        lines.append(f"## {rpt.dataset_id}")
        lines.append(f"- **Data type:** {rpt.data_type}")
        lines.append(f"- **Standard:** {rpt.standard_name}")
        lines.append(f"- **FINAL SCORE: {rpt.final_score}/100**")
        lines.append("")
        lines.append("| Criteria | Weight | Score | Weighted |")
        lines.append("|---|---|---|---|")

        for cid, cs in rpt.criteria_scores.items():
            lines.append(
                f"| {cs.criteria_name} | {cs.weight:.0%} | "
                f"{cs.score_100}/100 | {cs.weighted_score:.1f} |"
            )
        lines.append("")

        # Rule details table
        lines.append("<details><summary>Rule Details</summary>")
        lines.append("")
        lines.append("| Rule | Tag | Criteria | Pass Rate | Details |")
        lines.append("|---|---|---|---|---|")
        for r in rpt.rule_results:
            detail_str = json.dumps(r.details, ensure_ascii=False)[:80] if r.details else ""
            if r.error:
                detail_str = f"ERROR: {r.error[:60]}"
            lines.append(
                f"| {r.rule_id} | {r.rule_tag} | {r.criteria} | "
                f"{r.pass_rate:.2%} | {detail_str} |"
            )
        lines.append("")
        lines.append("</details>")
        lines.append("")
        lines.append("---")
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def generate_csv(reports: List[DatasetReport], output_path: Path) -> None:
    rows = []
    for rpt in reports:
        base = {
            "dataset_id": rpt.dataset_id,
            "data_type": rpt.data_type,
            "standard": rpt.standard_name,
            "final_score": rpt.final_score,
        }
        for cid, cs in rpt.criteria_scores.items():
            base[f"{cid}_weight"] = cs.weight
            base[f"{cid}_score"] = cs.score_100
            base[f"{cid}_weighted"] = round(cs.weighted_score, 2)
        rows.append(base)

    if not rows:
        return

    fieldnames = list(rows[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_json(reports: List[DatasetReport], output_path: Path) -> None:
    data = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "datasets": [rpt.to_dict() for rpt in reports],
    }
    output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
