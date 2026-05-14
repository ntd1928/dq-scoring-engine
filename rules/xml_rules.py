"""XML-specific rules (XML01–XML06)."""
from __future__ import annotations
import xml.etree.ElementTree as ET
from .base import BaseRule, RuleContext, RuleRegistry, RuleResult

@RuleRegistry.register
class WellformedCheck(BaseRule):
    rule_id = "XML01"; rule_tag = "specific"; criteria = "SYN"; applicable_types = ["xml"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        try: ET.parse(str(ctx.file_path)); return self._result(1, 1)
        except ET.ParseError as e: return self._result(1, 0, {"error": str(e)[:200]})

@RuleRegistry.register
class NamespaceAware(BaseRule):
    rule_id = "XML02"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["xml"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        try:
            tree = ET.parse(str(ctx.file_path)); root = tree.getroot()
            ns = set(); 
            for elem in root.iter():
                if "}" in elem.tag: ns.add(elem.tag.split("}")[0] + "}")
            return self._result(1, 1, {"namespaces": list(ns)[:10], "count": len(ns)})
        except: return self._result(1, 0)

@RuleRegistry.register
class XSDValidate(BaseRule):
    rule_id = "XML03"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["xml"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        return self._result(1, 1, {"note": "XSD validation skipped — no schema provided"})

@RuleRegistry.register
class AttributeCompleteness(BaseRule):
    rule_id = "XML04"; rule_tag = "specific"; criteria = "CMP"; applicable_types = ["xml"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        try:
            tree = ET.parse(str(ctx.file_path)); all_attrs = set(); rows = 0
            for elem in tree.getroot().iter("row"):
                all_attrs.update(elem.attrib.keys()); rows += 1
            if rows == 0: return self._result(1, 1, {"note": "no row elements"})
            total = rows * len(all_attrs); present = 0
            for elem in tree.getroot().iter("row"):
                present += sum(1 for a in all_attrs if a in elem.attrib)
            return self._result(total, present, {"unique_attrs": len(all_attrs), "rows": rows})
        except: return self._result(0, 0)

@RuleRegistry.register
class EscapedHTMLDetect(BaseRule):
    rule_id = "XML05"; rule_tag = "specific"; criteria = "SYN"; applicable_types = ["xml"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        import re; html_entities = len(re.findall(r'&lt;|&gt;|&amp;', text))
        return self._result(1, 1, {"html_entity_count": html_entities})

@RuleRegistry.register
class NullableAttrRate(BaseRule):
    rule_id = "XML06"; rule_tag = "specific"; criteria = "CMP"; applicable_types = ["xml"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        try:
            tree = ET.parse(str(ctx.file_path)); all_attrs = set(); rows = []
            for elem in tree.getroot().iter("row"):
                all_attrs.update(elem.attrib.keys()); rows.append(elem)
            if not rows: return self._result(1, 1)
            missing = {}
            for attr in all_attrs:
                miss = sum(1 for r in rows if attr not in r.attrib)
                if miss > 0: missing[attr] = miss
            total = len(rows) * len(all_attrs)
            present = total - sum(missing.values())
            return self._result(total, present, {"missing_attrs": missing})
        except: return self._result(0, 0)
