"""Parquet-specific rules (PQ01–PQ08)."""
from __future__ import annotations
from .base import BaseRule, RuleContext, RuleRegistry, RuleResult

@RuleRegistry.register
class MagicNumberCheck(BaseRule):
    rule_id = "PQ01"; rule_tag = "specific"; criteria = "SYN"; applicable_types = ["parquet"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        raw = ctx.file_path.read_bytes()
        ok = raw[:4] == b"PAR1" and raw[-4:] == b"PAR1"
        return self._result(1, 1 if ok else 0, {"has_magic": ok})

@RuleRegistry.register
class SchemaMatch(BaseRule):
    rule_id = "PQ02"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["parquet"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        import pyarrow.parquet as pq
        try:
            meta = pq.read_metadata(str(ctx.file_path))
            schema = pq.read_schema(str(ctx.file_path))
            cols = [f.name for f in schema]
            return self._result(1, 1, {"columns": cols, "num_columns": len(cols), "num_rows": meta.num_rows})
        except Exception as e: return self._result(1, 0, error=str(e))

@RuleRegistry.register
class SchemaDriftDetect(BaseRule):
    rule_id = "PQ03"; rule_tag = "specific"; criteria = "CST"; applicable_types = ["parquet"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        return self._result(1, 1, {"note": "single-file check — drift detection needs multi-file comparison"})

@RuleRegistry.register
class NullRatePerColumn(BaseRule):
    rule_id = "PQ04"; rule_tag = "specific"; criteria = "CMP"; applicable_types = ["parquet"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        import pandas as pd
        df = ctx.parsed_obj
        if not isinstance(df, pd.DataFrame): return self._result(0, 0, error="No DataFrame")
        total = int(df.size); nulls = int(df.isnull().sum().sum())
        null_per_col = {c: int(df[c].isnull().sum()) for c in df.columns if df[c].isnull().any()}
        return self._result(total, total - nulls, {"null_columns": null_per_col})

@RuleRegistry.register
class NestedColumnAudit(BaseRule):
    rule_id = "PQ05"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["parquet"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        import pyarrow.parquet as pq
        try:
            schema = pq.read_schema(str(ctx.file_path)); nested = []
            for f in schema:
                t = str(f.type)
                if any(k in t for k in ["list", "struct", "map"]): nested.append(f.name)
            total = len(schema)
            return self._result(total, total, {"nested_columns": nested, "nested_count": len(nested)})
        except Exception as e: return self._result(0, 0, error=str(e))

@RuleRegistry.register
class NegativeValueFlag(BaseRule):
    rule_id = "PQ06"; rule_tag = "specific"; criteria = "ACC"; applicable_types = ["parquet"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        import numpy as np, pandas as pd
        df = ctx.parsed_obj
        if not isinstance(df, pd.DataFrame): return self._result(0, 0, error="No DataFrame")
        num_cols = df.select_dtypes(include=[np.number]).columns
        total = 0; negatives = {}
        for c in num_cols:
            vals = df[c].dropna(); total += len(vals)
            neg = int((vals < 0).sum())
            if neg > 0: negatives[c] = neg
        passed = total - sum(negatives.values())
        return self._result(total, passed, {"negative_columns": negatives})

@RuleRegistry.register
class ZeroValueFlag(BaseRule):
    rule_id = "PQ07"; rule_tag = "specific"; criteria = "ACC"; applicable_types = ["parquet"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        import numpy as np, pandas as pd
        df = ctx.parsed_obj
        if not isinstance(df, pd.DataFrame): return self._result(0, 0, error="No DataFrame")
        num_cols = df.select_dtypes(include=[np.number]).columns
        total = 0; zeros = {}
        for c in num_cols:
            vals = df[c].dropna(); total += len(vals)
            z = int((vals == 0).sum())
            if z > 0: zeros[c] = z
        passed = total - sum(zeros.values())
        return self._result(total, passed, {"zero_columns": zeros})

@RuleRegistry.register
class MetadataStatsCheck(BaseRule):
    rule_id = "PQ08"; rule_tag = "specific"; criteria = "SEC"; applicable_types = ["parquet"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        import pyarrow.parquet as pq
        try:
            meta = pq.read_metadata(str(ctx.file_path))
            return self._result(1, 1, {"num_row_groups": meta.num_row_groups, "num_rows": meta.num_rows, "num_columns": meta.num_columns})
        except Exception as e: return self._result(1, 0, error=str(e))
