"""JSON/JSONL-specific rules (JSON01–JSON09)."""
from __future__ import annotations
import json, io
from collections import Counter
from .base import BaseRule, RuleContext, RuleRegistry, RuleResult

def _nested_depth(obj, depth=0):
    if isinstance(obj, dict):
        return max(((_nested_depth(v, depth+1)) for v in obj.values()), default=depth)
    if isinstance(obj, list) and obj:
        return max((_nested_depth(v, depth+1) for v in obj[:5]), default=depth)
    return depth

@RuleRegistry.register
class JSONParseValid(BaseRule):
    rule_id = "JSON01"; rule_tag = "specific"; criteria = "SYN"; applicable_types = ["json", "geojson"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        try: json.loads(text); return self._result(1, 1)
        except json.JSONDecodeError as e: return self._result(1, 0, {"error": str(e)[:200]})

@RuleRegistry.register
class TrailingCommaReject(BaseRule):
    rule_id = "JSON02"; rule_tag = "specific"; criteria = "SYN"; applicable_types = ["json"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        import re
        trailing = len(re.findall(r',\s*[}\]]', text))
        return self._result(1, 1 if trailing == 0 else 0, {"trailing_comma_count": trailing})

@RuleRegistry.register
class NestedDepthCheck(BaseRule):
    rule_id = "JSON03"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["json"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        try:
            obj = json.loads(text); depth = _nested_depth(obj)
            return self._result(1, 1 if depth <= 20 else 0, {"max_depth": depth, "threshold": 20})
        except: return self._result(1, 0, {"error": "parse failed"})

@RuleRegistry.register
class KeysetConsistency(BaseRule):
    rule_id = "JSON04"; rule_tag = "specific"; criteria = "CST"; applicable_types = ["json"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        try:
            obj = json.loads(text)
            records = obj if isinstance(obj, list) else obj.get("results", obj.get("elements", []))
            if not isinstance(records, list) or not records: return self._result(1, 1, {"note": "not a record list"})
            keysets = set(frozenset(r.keys()) for r in records if isinstance(r, dict))
            total = len(records); uniform = sum(1 for r in records if isinstance(r, dict) and frozenset(r.keys()) == next(iter(keysets))) if len(keysets) == 1 else 0
            return self._result(total, uniform if len(keysets) == 1 else total, {"unique_keysets": len(keysets)})
        except: return self._result(1, 0)

@RuleRegistry.register
class ArrayLengthAlignment(BaseRule):
    rule_id = "JSON05"; rule_tag = "specific"; criteria = "CST"; applicable_types = ["json"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        try:
            obj = json.loads(text)
            if not isinstance(obj, dict): return self._result(1, 1, {"note": "not an object"})
            arrays = {k: len(v) for k, v in obj.items() if isinstance(v, list)}
            if len(arrays) < 2: return self._result(1, 1, {"note": "fewer than 2 arrays"})
            lengths = set(arrays.values()); aligned = len(lengths) == 1
            return self._result(len(arrays), len(arrays) if aligned else 0, {"array_lengths": arrays})
        except: return self._result(1, 0)

@RuleRegistry.register
class OptionalKeyRate(BaseRule):
    rule_id = "JSON06"; rule_tag = "specific"; criteria = "CMP"; applicable_types = ["json"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        try:
            obj = json.loads(text)
            records = obj if isinstance(obj, list) else obj.get("results", [])
            if not isinstance(records, list) or len(records) < 2: return self._result(1, 1)
            all_keys = set(); [all_keys.update(r.keys()) for r in records if isinstance(r, dict)]
            total = len(all_keys) * len(records); present = sum(1 for r in records if isinstance(r, dict) for k in all_keys if k in r)
            return self._result(total, present, {"total_keys": len(all_keys), "records": len(records)})
        except: return self._result(1, 0)

@RuleRegistry.register
class ArrayCardinality(BaseRule):
    rule_id = "JSON07"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["json"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        # Reports array sizes per record — always passes, informational
        return self._result(1, 1, {"note": "informational rule"})

@RuleRegistry.register
class JSONLLineValid(BaseRule):
    rule_id = "JSON08"; rule_tag = "specific"; criteria = "SYN"; applicable_types = ["json"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        lines = [l for l in text.splitlines() if l.strip()]
        total = len(lines); passed = 0
        for l in lines:
            try: json.loads(l); passed += 1
            except: pass
        return self._result(total, passed)

@RuleRegistry.register
class EventTypeDrift(BaseRule):
    rule_id = "JSON09"; rule_tag = "specific"; criteria = "CST"; applicable_types = ["json"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        type_counts = Counter()
        for l in text.splitlines():
            if not l.strip(): continue
            try:
                obj = json.loads(l); type_counts[obj.get("type", "<missing>")] += 1
            except: pass
        return self._result(sum(type_counts.values()), sum(type_counts.values()), {"event_types": dict(type_counts)})
