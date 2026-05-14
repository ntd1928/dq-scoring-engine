"""Base classes for the DQ Scoring Engine rule system.

Every rule inherits from ``BaseRule`` and registers itself via ``RuleRegistry``.
A rule receives a data sample (file path or in-memory object) and returns a
``RuleResult`` with pass/fail counts so the scoring engine can aggregate.
"""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Type


@dataclass
class RuleResult:
    """Outcome produced by a single rule execution."""

    rule_id: str
    rule_tag: str  # "general" | "specific"
    criteria: str  # SYN | STR | CMP | CST | ACC | SEC
    total_records: int = 0
    passed_records: int = 0
    details: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    @property
    def pass_rate(self) -> float:
        if self.total_records == 0:
            return 1.0
        return self.passed_records / self.total_records

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "rule_tag": self.rule_tag,
            "criteria": self.criteria,
            "total_records": self.total_records,
            "passed_records": self.passed_records,
            "pass_rate": round(self.pass_rate, 6),
            "details": self.details,
            "error": self.error,
        }


class BaseRule:
    """Abstract base for every DQ rule.

    Subclasses MUST set ``rule_id``, ``rule_tag``, ``criteria`` and implement
    ``evaluate()``.
    """

    rule_id: str = ""
    rule_tag: str = ""  # "general" | "specific"
    criteria: str = ""  # SYN | STR | CMP | CST | ACC | SEC
    applicable_types: List[str] = []  # e.g. ["csv", "json"]

    def evaluate(self, context: "RuleContext") -> RuleResult:
        raise NotImplementedError

    def _result(self, total: int = 0, passed: int = 0,
                details: Dict[str, Any] | None = None,
                error: str | None = None) -> RuleResult:
        return RuleResult(
            rule_id=self.rule_id,
            rule_tag=self.rule_tag,
            criteria=self.criteria,
            total_records=total,
            passed_records=passed,
            details=details or {},
            error=error,
        )


@dataclass
class RuleContext:
    """All information a rule needs to evaluate a dataset sample."""

    file_path: Path
    data_type: str  # csv, json, xml, parquet, ...
    dataset_id: str = ""
    # Pre-loaded content caches (set by engine before rule runs)
    raw_bytes: Optional[bytes] = None
    raw_text: Optional[str] = None
    parsed_obj: Any = None  # e.g. dict for JSON, DataFrame for CSV
    metadata: Dict[str, Any] = field(default_factory=dict)


class RuleRegistry:
    """Global registry mapping rule_id → rule class."""

    _rules: Dict[str, Type[BaseRule]] = {}

    @classmethod
    def register(cls, rule_cls: Type[BaseRule]) -> Type[BaseRule]:
        """Decorator to register a rule class."""
        if rule_cls.rule_id:
            cls._rules[rule_cls.rule_id] = rule_cls
        return rule_cls

    @classmethod
    def get(cls, rule_id: str) -> Type[BaseRule]:
        return cls._rules[rule_id]

    @classmethod
    def get_all(cls) -> Dict[str, Type[BaseRule]]:
        return dict(cls._rules)

    @classmethod
    def get_for_type(cls, data_type: str) -> List[Type[BaseRule]]:
        return [
            r for r in cls._rules.values()
            if not r.applicable_types or data_type in r.applicable_types
        ]
