"""Scoring Engine — orchestrates rules and computes 3-Layer scores.

Usage:
    engine = ScoringEngine("config/scoring_framework.json")
    report = engine.score_dataset("data/nyc_tlc/sample.parquet", "parquet", "nyc_tlc")
    print(report.final_score)
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from rules.base import BaseRule, RuleContext, RuleRegistry, RuleResult

# Force rule modules to load so decorators run
import rules.general      # noqa: F401
import rules.csv_rules    # noqa: F401
import rules.json_rules   # noqa: F401
import rules.xml_rules    # noqa: F401
import rules.parquet_rules  # noqa: F401
import rules.other_rules  # noqa: F401


@dataclass
class CriteriaScore:
    criteria_id: str
    criteria_name: str
    weight: float
    rule_results: List[RuleResult] = field(default_factory=list)

    @property
    def avg_pass_rate(self) -> float:
        if not self.rule_results:
            return 1.0
        return sum(r.pass_rate for r in self.rule_results) / len(self.rule_results)

    @property
    def weighted_score(self) -> float:
        return self.avg_pass_rate * self.weight * 100

    @property
    def score_100(self) -> float:
        return round(self.avg_pass_rate * 100, 2)


@dataclass
class DatasetReport:
    dataset_id: str
    data_type: str
    standard_name: str
    criteria_scores: Dict[str, CriteriaScore] = field(default_factory=dict)
    rule_results: List[RuleResult] = field(default_factory=list)

    @property
    def final_score(self) -> float:
        return round(sum(cs.weighted_score for cs in self.criteria_scores.values()), 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dataset_id": self.dataset_id,
            "data_type": self.data_type,
            "standard": self.standard_name,
            "final_score": self.final_score,
            "criteria": {
                cid: {
                    "name": cs.criteria_name,
                    "weight": cs.weight,
                    "score": cs.score_100,
                    "weighted_score": round(cs.weighted_score, 2),
                    "rules_count": len(cs.rule_results),
                }
                for cid, cs in self.criteria_scores.items()
            },
            "rules_detail": [r.to_dict() for r in self.rule_results],
        }


CRITERIA_NAMES = {
    "SYN": "Syntax Validity",
    "STR": "Structural Conformance",
    "CMP": "Completeness",
    "CST": "Consistency",
    "ACC": "Accuracy / Range",
    "SEC": "Security / Integrity",
}


class ScoringEngine:
    def __init__(self, config_path: str | Path):
        with open(config_path, "r") as f:
            self.config = json.load(f)

    def _resolve_data_type_key(self, data_type: str) -> str:
        """Map file-level type to config key."""
        mapping = {
            "csv": "csv", "tsv": "csv",
            "json": "json", "jsonl": "json",
            "xml": "xml",
            "parquet": "parquet",
            "avro": "avro",
            "orc": "orc",
            "xlsx": "xlsx", "xls": "xlsx",
            "fixed_width": "fixed_width", "dly": "fixed_width",
            "txt_log": "txt_log", "log": "txt_log", "txt": "txt_log",
            "geojson": "geojson",
            "osm": "osm",
            "archives": "archives", "zip": "archives", "gz": "archives",
        }
        return mapping.get(data_type, data_type)

    def _load_data(self, file_path: Path, data_type: str) -> tuple:
        """Load file content into appropriate format for rules."""
        raw_bytes = None
        raw_text = None
        parsed_obj = None

        key = self._resolve_data_type_key(data_type)

        try:
            if key in ("csv", "fixed_width", "txt_log"):
                raw_bytes = file_path.read_bytes()
                raw_text = raw_bytes.decode("utf-8", errors="replace")
                if key == "csv":
                    parsed_obj = pd.read_csv(file_path, nrows=5000)
                elif key == "fixed_width":
                    parsed_obj = pd.DataFrame({"raw_line": raw_text.splitlines()})
            elif key in ("json", "geojson", "osm"):
                raw_bytes = file_path.read_bytes()
                raw_text = raw_bytes.decode("utf-8", errors="replace")
            elif key == "parquet":
                parsed_obj = pd.read_parquet(file_path)
            elif key == "xlsx":
                parsed_obj = pd.read_excel(file_path, nrows=5000)
                raw_bytes = file_path.read_bytes()
            elif key == "avro":
                raw_bytes = file_path.read_bytes()
            elif key == "orc":
                raw_bytes = file_path.read_bytes()
            elif key == "xml":
                raw_bytes = file_path.read_bytes()
                raw_text = raw_bytes.decode("utf-8", errors="replace")
        except Exception:
            pass  # Rules will handle missing data gracefully

        return raw_bytes, raw_text, parsed_obj

    def score_dataset(self, file_path: str | Path,
                      data_type: str,
                      dataset_id: str = "") -> DatasetReport:
        file_path = Path(file_path)
        config_key = self._resolve_data_type_key(data_type)
        std_config = self.config.get("standards", {}).get(config_key)

        if not std_config:
            return DatasetReport(dataset_id=dataset_id, data_type=data_type,
                                 standard_name="UNKNOWN")

        # Load data
        raw_bytes, raw_text, parsed_obj = self._load_data(file_path, data_type)

        ctx = RuleContext(
            file_path=file_path,
            data_type=config_key,
            dataset_id=dataset_id,
            raw_bytes=raw_bytes,
            raw_text=raw_text,
            parsed_obj=parsed_obj,
        )

        # Run rules per criteria
        weights = std_config["weights"]
        rule_map = std_config["rules"]
        all_rules = RuleRegistry.get_all()

        criteria_scores: Dict[str, CriteriaScore] = {}
        all_results: List[RuleResult] = []

        for crit_id, rule_ids in rule_map.items():
            cs = CriteriaScore(
                criteria_id=crit_id,
                criteria_name=CRITERIA_NAMES.get(crit_id, crit_id),
                weight=weights.get(crit_id, 0),
            )
            for rid in rule_ids:
                rule_cls = all_rules.get(rid)
                if not rule_cls:
                    continue
                try:
                    result = rule_cls().evaluate(ctx)
                    cs.rule_results.append(result)
                    all_results.append(result)
                except Exception as e:
                    err_result = RuleResult(
                        rule_id=rid, rule_tag="error", criteria=crit_id,
                        error=str(e)[:200],
                    )
                    cs.rule_results.append(err_result)
                    all_results.append(err_result)

            criteria_scores[crit_id] = cs

        return DatasetReport(
            dataset_id=dataset_id or file_path.stem,
            data_type=data_type,
            standard_name=std_config["standard_name"],
            criteria_scores=criteria_scores,
            rule_results=all_results,
        )
