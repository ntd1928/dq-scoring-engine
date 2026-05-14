"""CSV-specific rules (CSV01–CSV07)."""
from __future__ import annotations
import csv, io
from collections import Counter
from .base import BaseRule, RuleContext, RuleRegistry, RuleResult

@RuleRegistry.register
class DelimiterDetection(BaseRule):
    rule_id = "CSV01"; rule_tag = "specific"; criteria = "SYN"; applicable_types = ["csv"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        try:
            d = csv.Sniffer().sniff(text[:8192]).delimiter
            return self._result(1, 1, {"detected_delimiter": repr(d)})
        except csv.Error:
            return self._result(1, 0, {"error": "cannot detect delimiter"})

@RuleRegistry.register
class HeaderPresence(BaseRule):
    rule_id = "CSV02"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["csv"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        try:
            h = csv.Sniffer().has_header(text[:8192])
            return self._result(1, 1, {"has_header": h})
        except csv.Error:
            return self._result(1, 0)

@RuleRegistry.register
class QuotedNewline(BaseRule):
    rule_id = "CSV03"; rule_tag = "specific"; criteria = "SYN"; applicable_types = ["csv"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        rows = list(csv.reader(io.StringIO(text)))
        phys = len(text.splitlines()); logic = len(rows)
        return self._result(logic, logic, {"physical_lines": phys, "logical_records": logic, "has_quoted_newline": logic < phys})

@RuleRegistry.register
class EmbeddedSeparator(BaseRule):
    rule_id = "CSV04"; rule_tag = "specific"; criteria = "SYN"; applicable_types = ["csv"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        rows = list(csv.reader(io.StringIO(text)))
        if not rows: return self._result(0, 0)
        exp = len(rows[0]); total = len(rows)
        passed = sum(1 for r in rows if len(r) == exp)
        return self._result(total, passed, {"expected_columns": exp, "mismatched_rows": total - passed})

@RuleRegistry.register
class CommentRowSkip(BaseRule):
    rule_id = "CSV05"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["csv"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        comments = [i for i, l in enumerate(lines) if l.strip().startswith("#")]
        return self._result(len(lines), len(lines), {"comment_count": len(comments)})

@RuleRegistry.register
class FieldCountDistribution(BaseRule):
    rule_id = "CSV06"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["csv"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        counts = Counter(len(r) for r in csv.reader(io.StringIO(text)))
        total = sum(counts.values()); mode = counts.most_common(1)[0][0] if counts else 0
        return self._result(total, counts.get(mode, 0), {"mode_field_count": mode, "distribution": dict(counts)})

@RuleRegistry.register
class NonASCIIHandling(BaseRule):
    rule_id = "CSV07"; rule_tag = "specific"; criteria = "SYN"; applicable_types = ["csv"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        raw = ctx.raw_bytes or ctx.file_path.read_bytes()
        non_ascii = sum(1 for b in raw if b > 127)
        try: raw.decode("utf-8"); ok = True
        except UnicodeDecodeError: ok = False
        return self._result(1, 1 if ok else 0, {"non_ascii_bytes": non_ascii, "utf8_decodable": ok})
