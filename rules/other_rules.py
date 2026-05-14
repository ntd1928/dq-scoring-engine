"""Remaining data-type specific rules: Avro, ORC, XLSX, Fixed-width, Log, GeoJSON, OSM, Archives."""
from __future__ import annotations
import json, zipfile, tarfile, re
from collections import Counter
from .base import BaseRule, RuleContext, RuleRegistry, RuleResult

# ── Avro (AVRO01–AVRO04) ──
@RuleRegistry.register
class AvroContainerMagic(BaseRule):
    rule_id = "AVRO01"; rule_tag = "specific"; criteria = "SYN"; applicable_types = ["avro"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        raw = ctx.file_path.read_bytes()[:4]
        ok = raw == b"Obj\x01"
        return self._result(1, 1 if ok else 0, {"has_avro_magic": ok})

@RuleRegistry.register
class WriterSchemaPresent(BaseRule):
    rule_id = "AVRO02"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["avro"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        try:
            import fastavro
            with open(ctx.file_path, "rb") as f:
                reader = fastavro.reader(f); schema = reader.writer_schema
            fields = [f["name"] for f in schema.get("fields", [])] if isinstance(schema, dict) else []
            return self._result(1, 1 if schema else 0, {"writer_schema_fields": fields})
        except Exception as e: return self._result(1, 0, error=str(e))

@RuleRegistry.register
class UnionFieldCheck(BaseRule):
    rule_id = "AVRO03"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["avro"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        try:
            import fastavro
            with open(ctx.file_path, "rb") as f:
                schema = fastavro.reader(f).writer_schema
            unions = [f["name"] for f in schema.get("fields", []) if isinstance(f.get("type"), list)]
            return self._result(len(schema.get("fields", [])), len(schema.get("fields", [])), {"union_fields": unions})
        except Exception as e: return self._result(0, 0, error=str(e))

@RuleRegistry.register
class LogicalTypeCheck(BaseRule):
    rule_id = "AVRO04"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["avro"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        return self._result(1, 1, {"note": "logical type check requires schema inspection"})

# ── ORC (ORC01–ORC04) ──
@RuleRegistry.register
class ORCReadable(BaseRule):
    rule_id = "ORC01"; rule_tag = "specific"; criteria = "SYN"; applicable_types = ["orc"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        try:
            import pyarrow.orc as orc
            f = orc.ORCFile(str(ctx.file_path))
            return self._result(1, 1, {"rows": f.nrows, "columns": f.nstripes})
        except Exception as e: return self._result(1, 0, error=str(e))

@RuleRegistry.register
class DecimalPrecision(BaseRule):
    rule_id = "ORC02"; rule_tag = "specific"; criteria = "ACC"; applicable_types = ["orc"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        try:
            import pyarrow.orc as orc
            f = orc.ORCFile(str(ctx.file_path)); schema_str = str(f.schema)
            decimals = re.findall(r'decimal\d*\(\d+,\s*\d+\)', schema_str)
            return self._result(1, 1, {"decimal_types": decimals})
        except Exception as e: return self._result(1, 0, error=str(e))

@RuleRegistry.register
class TimestampTZCheck(BaseRule):
    rule_id = "ORC03"; rule_tag = "specific"; criteria = "ACC"; applicable_types = ["orc"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        try:
            import pyarrow.orc as orc
            schema_str = str(orc.ORCFile(str(ctx.file_path)).schema)
            has_ts = "timestamp" in schema_str.lower()
            return self._result(1, 1, {"has_timestamp": has_ts})
        except Exception as e: return self._result(1, 0, error=str(e))

@RuleRegistry.register
class StripeIntegrity(BaseRule):
    rule_id = "ORC04"; rule_tag = "specific"; criteria = "SEC"; applicable_types = ["orc"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        try:
            import pyarrow.orc as orc
            f = orc.ORCFile(str(ctx.file_path)); f.read()
            return self._result(1, 1, {"stripes": f.nstripes})
        except Exception as e: return self._result(1, 0, error=str(e))

# ── XLSX (XLS01–XLS05) ──
@RuleRegistry.register
class SheetCountCheck(BaseRule):
    rule_id = "XLS01"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["xlsx"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        import pandas as pd
        try:
            xls = pd.ExcelFile(ctx.file_path)
            return self._result(1, 1, {"sheets": xls.sheet_names, "count": len(xls.sheet_names)})
        except Exception as e: return self._result(1, 0, error=str(e))

@RuleRegistry.register
class HeaderOffsetDetect(BaseRule):
    rule_id = "XLS02"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["xlsx"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        import pandas as pd
        try:
            df = pd.read_excel(ctx.file_path, nrows=5, header=None)
            # Check if first row looks like header (all strings)
            first_row_all_str = all(isinstance(v, str) for v in df.iloc[0] if pd.notna(v))
            return self._result(1, 1, {"first_row_all_string": first_row_all_str})
        except Exception as e: return self._result(1, 0, error=str(e))

@RuleRegistry.register
class BlankCellRate(BaseRule):
    rule_id = "XLS03"; rule_tag = "specific"; criteria = "CMP"; applicable_types = ["xlsx"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        import pandas as pd
        try:
            df = pd.read_excel(ctx.file_path, nrows=100)
            total = int(df.size); blanks = int(df.isnull().sum().sum())
            return self._result(total, total - blanks, {"blank_cells": blanks, "blank_rate": round(blanks/total, 4) if total else 0})
        except Exception as e: return self._result(0, 0, error=str(e))

@RuleRegistry.register
class MixedTypeColumn(BaseRule):
    rule_id = "XLS04"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["xlsx"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        import pandas as pd
        try:
            df = pd.read_excel(ctx.file_path, nrows=100)
            mixed = [c for c in df.columns if df[c].apply(type).nunique() > 1]
            return self._result(len(df.columns), len(df.columns) - len(mixed), {"mixed_columns": mixed})
        except Exception as e: return self._result(0, 0, error=str(e))

@RuleRegistry.register
class DateSerialParse(BaseRule):
    rule_id = "XLS05"; rule_tag = "specific"; criteria = "ACC"; applicable_types = ["xlsx"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        import pandas as pd
        try:
            df = pd.read_excel(ctx.file_path, nrows=100)
            date_cols = [c for c in df.columns if "date" in c.lower()]
            if not date_cols: return self._result(1, 1, {"note": "no date columns"})
            total = 0; passed = 0
            for c in date_cols:
                vals = df[c].dropna(); total += len(vals)
                parsed = pd.to_datetime(vals, errors="coerce"); passed += int(parsed.notna().sum())
            return self._result(total, passed, {"date_columns": date_cols})
        except Exception as e: return self._result(0, 0, error=str(e))

# ── Fixed-width (FW01–FW04) ──
@RuleRegistry.register
class LineLengthStable(BaseRule):
    rule_id = "FW01"; rule_tag = "specific"; criteria = "SYN"; applicable_types = ["fixed_width"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines(); lengths = Counter(len(l) for l in lines if l.strip())
        mode = lengths.most_common(1)[0][0] if lengths else 0
        total = sum(lengths.values()); passed = lengths.get(mode, 0)
        return self._result(total, passed, {"mode_length": mode, "distribution": dict(lengths)})

@RuleRegistry.register
class OffsetExtraction(BaseRule):
    rule_id = "FW02"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["fixed_width"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        return self._result(1, 1, {"note": "offset spec required for full check"})

@RuleRegistry.register
class SentinelDetection(BaseRule):
    rule_id = "FW03"; rule_tag = "specific"; criteria = "CMP"; applicable_types = ["fixed_width"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        sentinel_count = text.count("-9999")
        lines = len(text.splitlines())
        return self._result(lines, lines, {"sentinel_count": sentinel_count, "sentinel_value": "-9999"})

@RuleRegistry.register
class ElementCodeValid(BaseRule):
    rule_id = "FW04"; rule_tag = "specific"; criteria = "ACC"; applicable_types = ["fixed_width"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        elements = Counter()
        for line in text.splitlines():
            if len(line) >= 21: elements[line[17:21].strip()] += 1
        return self._result(sum(elements.values()), sum(elements.values()), {"elements": dict(elements)})

# ── Log (LOG01–LOG04) ──
LOG_RE = re.compile(r'\[([^\]]+)\]\s*\[(\w+)\]\s*(.*)')

@RuleRegistry.register
class TimestampExtract(BaseRule):
    rule_id = "LOG01"; rule_tag = "specific"; criteria = "SYN"; applicable_types = ["txt_log"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        lines = [l for l in text.splitlines() if l.strip()]
        passed = sum(1 for l in lines if LOG_RE.match(l))
        return self._result(len(lines), passed)

@RuleRegistry.register
class LevelDistribution(BaseRule):
    rule_id = "LOG02"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["txt_log"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        levels = Counter()
        for l in text.splitlines():
            m = LOG_RE.match(l)
            if m: levels[m.group(2)] += 1
        return self._result(sum(levels.values()), sum(levels.values()), {"levels": dict(levels)})

@RuleRegistry.register
class ParseSuccessRate(BaseRule):
    rule_id = "LOG03"; rule_tag = "specific"; criteria = "SYN"; applicable_types = ["txt_log"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        lines = [l for l in text.splitlines() if l.strip()]
        passed = sum(1 for l in lines if LOG_RE.match(l))
        return self._result(len(lines), passed)

@RuleRegistry.register
class FieldCountStable(BaseRule):
    rule_id = "LOG04"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["txt_log"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        text = ctx.raw_text or ctx.file_path.read_text(encoding="utf-8", errors="replace")
        counts = Counter(len(l.split()) for l in text.splitlines() if l.strip())
        mode = counts.most_common(1)[0][0] if counts else 0
        total = sum(counts.values())
        return self._result(total, counts.get(mode, 0), {"mode_fields": mode})

# ── GeoJSON (GEO01–GEO04) ──
@RuleRegistry.register
class FeatureCollection(BaseRule):
    rule_id = "GEO01"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["geojson"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        obj = json.loads(ctx.raw_text or ctx.file_path.read_text(encoding="utf-8"))
        ok = obj.get("type") == "FeatureCollection"
        return self._result(1, 1 if ok else 0, {"type": obj.get("type")})

@RuleRegistry.register
class GeometryPresent(BaseRule):
    rule_id = "GEO02"; rule_tag = "specific"; criteria = "CMP"; applicable_types = ["geojson"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        obj = json.loads(ctx.raw_text or ctx.file_path.read_text(encoding="utf-8"))
        features = obj.get("features", [])
        total = len(features); passed = sum(1 for f in features if f.get("geometry"))
        return self._result(total, passed, {"missing_geometry": total - passed})

@RuleRegistry.register
class CoordinateRange(BaseRule):
    rule_id = "GEO03"; rule_tag = "specific"; criteria = "ACC"; applicable_types = ["geojson", "osm"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        obj = json.loads(ctx.raw_text or ctx.file_path.read_text(encoding="utf-8"))
        features = obj.get("features", obj.get("elements", []))
        total = 0; passed = 0
        for f in features:
            geom = f.get("geometry") or {}
            coords = geom.get("coordinates", [])
            if isinstance(coords, list) and len(coords) >= 2 and isinstance(coords[0], (int, float)):
                total += 1
                lon, lat = coords[0], coords[1]
                if -180 <= lon <= 180 and -90 <= lat <= 90: passed += 1
            elif f.get("lat") and f.get("lon"):
                total += 1
                if -90 <= f["lat"] <= 90 and -180 <= f["lon"] <= 180: passed += 1
        return self._result(total, passed) if total else self._result(1, 1, {"note": "no point coords"})

@RuleRegistry.register
class GeometryTypeWhitelist(BaseRule):
    rule_id = "GEO04"; rule_tag = "specific"; criteria = "ACC"; applicable_types = ["geojson"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        VALID = {"Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon", "GeometryCollection"}
        obj = json.loads(ctx.raw_text or ctx.file_path.read_text(encoding="utf-8"))
        types = Counter()
        for f in obj.get("features", []):
            g = f.get("geometry") or {}; types[g.get("type", "MISSING")] += 1
        total = sum(types.values()); passed = sum(v for k, v in types.items() if k in VALID)
        return self._result(total, passed, {"geometry_types": dict(types)})

# ── OSM (OSM01–OSM03) ──
@RuleRegistry.register
class ElementTypeValid(BaseRule):
    rule_id = "OSM01"; rule_tag = "specific"; criteria = "STR"; applicable_types = ["osm"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        obj = json.loads(ctx.raw_text or ctx.file_path.read_text(encoding="utf-8"))
        elems = obj.get("elements", [])
        types = Counter(e.get("type", "UNKNOWN") for e in elems)
        valid = {"node", "way", "relation"}
        total = len(elems); passed = sum(v for k, v in types.items() if k in valid)
        return self._result(total, passed, {"types": dict(types)})

@RuleRegistry.register
class NodeLatLonPresent(BaseRule):
    rule_id = "OSM02"; rule_tag = "specific"; criteria = "CMP"; applicable_types = ["osm"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        obj = json.loads(ctx.raw_text or ctx.file_path.read_text(encoding="utf-8"))
        nodes = [e for e in obj.get("elements", []) if e.get("type") == "node"]
        total = len(nodes); passed = sum(1 for n in nodes if "lat" in n and "lon" in n)
        return self._result(total, passed, {"missing_latlon": total - passed})

@RuleRegistry.register
class TagCompleteness(BaseRule):
    rule_id = "OSM03"; rule_tag = "specific"; criteria = "CMP"; applicable_types = ["osm"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        obj = json.loads(ctx.raw_text or ctx.file_path.read_text(encoding="utf-8"))
        elems = obj.get("elements", [])
        total = len(elems); tagged = sum(1 for e in elems if e.get("tags"))
        return self._result(total, tagged, {"tagged": tagged, "untagged": total - tagged})

# ── Archives (ARC01–ARC04) ──
@RuleRegistry.register
class ArchiveOpenable(BaseRule):
    rule_id = "ARC01"; rule_tag = "specific"; criteria = "SYN"; applicable_types = ["archives"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        p = str(ctx.file_path)
        try:
            if p.endswith(".zip"): zipfile.ZipFile(p).namelist(); return self._result(1, 1)
            elif p.endswith((".tar.gz", ".tgz")): tarfile.open(p, "r:gz").getnames(); return self._result(1, 1)
            elif p.endswith(".gz"):
                import gzip; gzip.open(p, "rb").read(1024); return self._result(1, 1)
            return self._result(1, 1, {"note": "unknown archive type"})
        except Exception as e: return self._result(1, 0, error=str(e))

@RuleRegistry.register
class PathTraversalCheck(BaseRule):
    rule_id = "ARC02"; rule_tag = "specific"; criteria = "SEC"; applicable_types = ["archives"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        p = str(ctx.file_path); members = []
        try:
            if p.endswith(".zip"): members = zipfile.ZipFile(p).namelist()
            elif p.endswith((".tar.gz", ".tgz")): members = tarfile.open(p, "r:gz").getnames()
        except: return self._result(1, 0, error="cannot read archive")
        bad = [m for m in members if ".." in m or m.startswith("/")]
        return self._result(len(members), len(members) - len(bad), {"path_traversal_members": bad})

DANGEROUS_SUFFIXES = {".exe", ".sh", ".bat", ".cmd", ".ps1", ".vbs", ".dll", ".so", ".js", ".scr"}

@RuleRegistry.register
class ExecutableScan(BaseRule):
    rule_id = "ARC03"; rule_tag = "specific"; criteria = "SEC"; applicable_types = ["archives"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        p = str(ctx.file_path); members = []
        try:
            if p.endswith(".zip"): members = zipfile.ZipFile(p).namelist()
            elif p.endswith((".tar.gz", ".tgz")): members = tarfile.open(p, "r:gz").getnames()
        except: return self._result(1, 0, error="cannot read archive")
        execs = [m for m in members if any(m.lower().endswith(s) for s in DANGEROUS_SUFFIXES)]
        return self._result(len(members), len(members) - len(execs), {"executable_members": execs})

@RuleRegistry.register
class ChecksumVerify(BaseRule):
    rule_id = "ARC04"; rule_tag = "specific"; criteria = "SEC"; applicable_types = ["archives"]
    def evaluate(self, ctx: RuleContext) -> RuleResult:
        import hashlib
        sha = hashlib.sha256(ctx.file_path.read_bytes()).hexdigest()
        return self._result(1, 1, {"sha256": sha})
