"""General rules (G01–G15) — applicable across multiple data types.

These rules cover universal DQ concerns like nulls, types, duplicates,
encoding, timestamps, and file integrity.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

from .base import BaseRule, RuleContext, RuleRegistry, RuleResult


# ---------------------------------------------------------------------------
# G01 – Not Null Check
# ---------------------------------------------------------------------------
@RuleRegistry.register
class NotNullCheck(BaseRule):
    rule_id = "G01"
    rule_tag = "general"
    criteria = "CMP"

    def evaluate(self, ctx: RuleContext) -> RuleResult:
        """Check required fields are not null/empty in parsed data."""
        import pandas as pd

        df = ctx.parsed_obj
        if not isinstance(df, pd.DataFrame) or df.empty:
            return self._result(0, 0, error="No DataFrame available")
        total = int(df.size)
        nulls = int(df.isnull().sum().sum())
        return self._result(total, total - nulls, {"null_count": nulls})


# ---------------------------------------------------------------------------
# G02 – Type Match
# ---------------------------------------------------------------------------
@RuleRegistry.register
class TypeMatch(BaseRule):
    rule_id = "G02"
    rule_tag = "general"
    criteria = "STR"

    def evaluate(self, ctx: RuleContext) -> RuleResult:
        """Verify column types are inferrable and not all-object."""
        import pandas as pd

        df = ctx.parsed_obj
        if not isinstance(df, pd.DataFrame) or df.empty:
            return self._result(0, 0, error="No DataFrame available")
        cols = len(df.columns)
        object_cols = sum(1 for dt in df.dtypes if dt == object)
        typed_cols = cols - object_cols
        return self._result(cols, typed_cols, {
            "typed_columns": typed_cols,
            "object_columns": object_cols,
        })


# ---------------------------------------------------------------------------
# G03 – Duplicate Check
# ---------------------------------------------------------------------------
@RuleRegistry.register
class DuplicateCheck(BaseRule):
    rule_id = "G03"
    rule_tag = "general"
    criteria = "CST"

    def evaluate(self, ctx: RuleContext) -> RuleResult:
        import pandas as pd

        df = ctx.parsed_obj
        if not isinstance(df, pd.DataFrame) or df.empty:
            return self._result(0, 0, error="No DataFrame available")
        total = len(df)
        dups = int(df.duplicated().sum())
        return self._result(total, total - dups, {"duplicate_rows": dups})


# ---------------------------------------------------------------------------
# G04 – Row Count Range
# ---------------------------------------------------------------------------
@RuleRegistry.register
class RowCountRange(BaseRule):
    rule_id = "G04"
    rule_tag = "general"
    criteria = "CMP"

    def evaluate(self, ctx: RuleContext) -> RuleResult:
        import pandas as pd

        df = ctx.parsed_obj
        if not isinstance(df, pd.DataFrame):
            return self._result(0, 0, error="No DataFrame available")
        rows = len(df)
        # Pass if at least 1 row present
        passed = 1 if rows > 0 else 0
        return self._result(1, passed, {"row_count": rows})


# ---------------------------------------------------------------------------
# G05 – Encoding UTF-8
# ---------------------------------------------------------------------------
@RuleRegistry.register
class EncodingUTF8(BaseRule):
    rule_id = "G05"
    rule_tag = "general"
    criteria = "SYN"

    def evaluate(self, ctx: RuleContext) -> RuleResult:
        raw = ctx.raw_bytes
        if raw is None:
            try:
                raw = ctx.file_path.read_bytes()
            except Exception as e:
                return self._result(0, 0, error=str(e))
        try:
            raw.decode("utf-8")
            return self._result(1, 1, {"encoding": "utf-8"})
        except UnicodeDecodeError as e:
            return self._result(1, 0, {"error_position": e.start})


# ---------------------------------------------------------------------------
# G06 – BOM Detection
# ---------------------------------------------------------------------------
@RuleRegistry.register
class BOMDetection(BaseRule):
    rule_id = "G06"
    rule_tag = "general"
    criteria = "SYN"

    def evaluate(self, ctx: RuleContext) -> RuleResult:
        raw = ctx.raw_bytes
        if raw is None:
            try:
                raw = ctx.file_path.read_bytes()[:4]
            except Exception as e:
                return self._result(0, 0, error=str(e))
        has_bom = raw[:3] == b"\xef\xbb\xbf"
        # BOM is a warning, not necessarily failure, but we flag it
        return self._result(1, 0 if has_bom else 1, {"has_bom": has_bom})


# ---------------------------------------------------------------------------
# G07 – Timestamp Parseable (ISO 8601)
# ---------------------------------------------------------------------------
@RuleRegistry.register
class TimestampParseable(BaseRule):
    rule_id = "G07"
    rule_tag = "general"
    criteria = "ACC"

    def evaluate(self, ctx: RuleContext) -> RuleResult:
        import pandas as pd

        df = ctx.parsed_obj
        if not isinstance(df, pd.DataFrame) or df.empty:
            return self._result(0, 0, error="No DataFrame available")
        # Find datetime columns or columns with 'date'/'time' in name
        ts_cols = [c for c in df.columns
                   if "date" in c.lower() or "time" in c.lower()]
        if not ts_cols:
            return self._result(1, 1, {"note": "no timestamp columns detected"})
        total = 0
        passed = 0
        for col in ts_cols:
            series = df[col].dropna()
            total += len(series)
            try:
                parsed = pd.to_datetime(series, errors="coerce")
                passed += int(parsed.notna().sum())
            except Exception:
                pass
        return self._result(total, passed, {"timestamp_columns": ts_cols})


# ---------------------------------------------------------------------------
# G08 – Numeric Range
# ---------------------------------------------------------------------------
@RuleRegistry.register
class NumericRange(BaseRule):
    rule_id = "G08"
    rule_tag = "general"
    criteria = "ACC"

    def evaluate(self, ctx: RuleContext) -> RuleResult:
        import numpy as np
        import pandas as pd

        df = ctx.parsed_obj
        if not isinstance(df, pd.DataFrame) or df.empty:
            return self._result(0, 0, error="No DataFrame available")
        num_cols = df.select_dtypes(include=[np.number]).columns
        if len(num_cols) == 0:
            return self._result(1, 1, {"note": "no numeric columns"})
        total = 0
        passed = 0
        details: Dict[str, Any] = {}
        for col in num_cols:
            vals = df[col].dropna()
            total += len(vals)
            # Flag extreme outliers (> 1e15 or < -1e15) as suspicious
            reasonable = vals.between(-1e15, 1e15)
            passed += int(reasonable.sum())
            if not reasonable.all():
                details[col] = {"outlier_count": int((~reasonable).sum())}
        return self._result(total, passed, details)


# ---------------------------------------------------------------------------
# G09 – Date Order Check
# ---------------------------------------------------------------------------
@RuleRegistry.register
class DateOrderCheck(BaseRule):
    rule_id = "G09"
    rule_tag = "general"
    criteria = "CST"

    def evaluate(self, ctx: RuleContext) -> RuleResult:
        import pandas as pd

        df = ctx.parsed_obj
        if not isinstance(df, pd.DataFrame) or df.empty:
            return self._result(0, 0, error="No DataFrame available")
        # Look for pickup/dropoff or start/end date pairs
        pairs = []
        cols_lower = {c.lower(): c for c in df.columns}
        for s, e in [("pickup", "dropoff"), ("start", "end"),
                      ("begin", "end"), ("from", "to")]:
            start_cols = [v for k, v in cols_lower.items() if s in k and ("date" in k or "time" in k)]
            end_cols = [v for k, v in cols_lower.items() if e in k and ("date" in k or "time" in k)]
            if start_cols and end_cols:
                pairs.append((start_cols[0], end_cols[0]))
        if not pairs:
            return self._result(1, 1, {"note": "no date pairs found"})
        total = 0
        passed = 0
        for sc, ec in pairs:
            try:
                s_dt = pd.to_datetime(df[sc], errors="coerce")
                e_dt = pd.to_datetime(df[ec], errors="coerce")
                valid = s_dt.notna() & e_dt.notna()
                total += int(valid.sum())
                passed += int((s_dt[valid] <= e_dt[valid]).sum())
            except Exception:
                pass
        return self._result(total, passed, {"date_pairs": [list(p) for p in pairs]})


# ---------------------------------------------------------------------------
# G10 – Column Count Stable
# ---------------------------------------------------------------------------
@RuleRegistry.register
class ColumnCountStable(BaseRule):
    rule_id = "G10"
    rule_tag = "general"
    criteria = "STR"

    def evaluate(self, ctx: RuleContext) -> RuleResult:
        """Check field count stability from raw text lines."""
        text = ctx.raw_text
        if text is None:
            try:
                text = ctx.file_path.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                return self._result(0, 0, error=str(e))
        lines = [l for l in text.splitlines() if l.strip()][:1000]
        if not lines:
            return self._result(0, 0, error="empty file")
        # Try to detect delimiter
        for delim in ["\t", ",", "|", ";"]:
            counts = Counter(len(l.split(delim)) for l in lines)
            if len(counts) <= 2 and max(counts.values()) > len(lines) * 0.8:
                mode_count = counts.most_common(1)[0][0]
                total = len(lines)
                passed = sum(1 for l in lines if len(l.split(delim)) == mode_count)
                return self._result(total, passed, {
                    "delimiter": repr(delim),
                    "mode_field_count": mode_count,
                    "distribution": dict(counts),
                })
        return self._result(len(lines), len(lines), {"note": "no clear delimiter"})


# ---------------------------------------------------------------------------
# G11 – String Length Check
# ---------------------------------------------------------------------------
@RuleRegistry.register
class StringLengthCheck(BaseRule):
    rule_id = "G11"
    rule_tag = "general"
    criteria = "ACC"

    def evaluate(self, ctx: RuleContext) -> RuleResult:
        import pandas as pd

        df = ctx.parsed_obj
        if not isinstance(df, pd.DataFrame) or df.empty:
            return self._result(0, 0, error="No DataFrame available")
        str_cols = df.select_dtypes(include=["object"]).columns
        if len(str_cols) == 0:
            return self._result(1, 1, {"note": "no string columns"})
        total = 0
        passed = 0
        max_len = 10000
        for col in str_cols:
            vals = df[col].dropna().astype(str)
            total += len(vals)
            passed += int((vals.str.len() <= max_len).sum())
        return self._result(total, passed, {"max_allowed": max_len})


# ---------------------------------------------------------------------------
# G12 – Whitespace Trim
# ---------------------------------------------------------------------------
@RuleRegistry.register
class WhitespaceTrim(BaseRule):
    rule_id = "G12"
    rule_tag = "general"
    criteria = "SYN"

    def evaluate(self, ctx: RuleContext) -> RuleResult:
        import pandas as pd

        df = ctx.parsed_obj
        if not isinstance(df, pd.DataFrame) or df.empty:
            return self._result(0, 0, error="No DataFrame available")
        str_cols = df.select_dtypes(include=["object"]).columns
        total = 0
        violations = 0
        for col in str_cols:
            vals = df[col].dropna().astype(str)
            total += len(vals)
            has_space = vals.str.startswith(" ") | vals.str.endswith(" ")
            violations += int(has_space.sum())
        return self._result(total, total - violations,
                            {"whitespace_violations": violations})


# ---------------------------------------------------------------------------
# G13 – Enum Membership
# ---------------------------------------------------------------------------
@RuleRegistry.register
class EnumMembership(BaseRule):
    rule_id = "G13"
    rule_tag = "general"
    criteria = "ACC"

    def evaluate(self, ctx: RuleContext) -> RuleResult:
        # This rule needs enum config per column — skip if not configured
        return self._result(1, 1, {"note": "enum config not provided; skipped"})


# ---------------------------------------------------------------------------
# G14 – SHA-256 Integrity
# ---------------------------------------------------------------------------
@RuleRegistry.register
class SHA256Integrity(BaseRule):
    rule_id = "G14"
    rule_tag = "general"
    criteria = "SEC"

    def evaluate(self, ctx: RuleContext) -> RuleResult:
        try:
            data = ctx.file_path.read_bytes()
            sha = hashlib.sha256(data).hexdigest()
            return self._result(1, 1, {"sha256": sha, "size_bytes": len(data)})
        except Exception as e:
            return self._result(1, 0, error=str(e))


# ---------------------------------------------------------------------------
# G15 – File Size Range
# ---------------------------------------------------------------------------
@RuleRegistry.register
class FileSizeRange(BaseRule):
    rule_id = "G15"
    rule_tag = "general"
    criteria = "SEC"

    def evaluate(self, ctx: RuleContext) -> RuleResult:
        try:
            size = ctx.file_path.stat().st_size
            # Flag empty files or files > 500MB as suspicious
            ok = 0 < size < 500 * 1024 * 1024
            return self._result(1, 1 if ok else 0, {
                "size_bytes": size,
                "size_mb": round(size / (1024 * 1024), 2),
            })
        except Exception as e:
            return self._result(1, 0, error=str(e))
