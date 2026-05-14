"""Unit tests for the DQ Scoring Engine rules and scorer."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rules.base import RuleContext, RuleRegistry  # noqa: E402

# Force all rule modules to load
import rules.general       # noqa: F401, E402
import rules.csv_rules     # noqa: F401, E402
import rules.json_rules    # noqa: F401, E402
import rules.xml_rules     # noqa: F401, E402
import rules.parquet_rules # noqa: F401, E402
import rules.other_rules   # noqa: F401, E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class TestRuleRegistry(unittest.TestCase):
    def test_all_rules_registered(self):
        all_rules = RuleRegistry.get_all()
        # We expect at least 60 rules
        self.assertGreaterEqual(len(all_rules), 60,
                                f"Expected 60+ rules, got {len(all_rules)}: {sorted(all_rules.keys())}")

    def test_general_rules_present(self):
        all_rules = RuleRegistry.get_all()
        for i in range(1, 16):
            rid = f"G{i:02d}"
            self.assertIn(rid, all_rules, f"Missing general rule {rid}")

    def test_specific_rules_present(self):
        all_rules = RuleRegistry.get_all()
        expected_prefixes = ["CSV", "JSON", "XML", "PQ", "AVRO", "ORC",
                             "XLS", "FW", "LOG", "GEO", "OSM", "ARC"]
        for prefix in expected_prefixes:
            matches = [k for k in all_rules if k.startswith(prefix)]
            self.assertTrue(len(matches) > 0,
                            f"No rules found with prefix {prefix}")


class TestGeneralRulesOnCSV(unittest.TestCase):
    def setUp(self):
        self.csv_path = FIXTURES / "test019.csv"
        if not self.csv_path.exists():
            self.skipTest("CSV fixture not found")
        import pandas as pd
        self.ctx = RuleContext(
            file_path=self.csv_path,
            data_type="csv",
            dataset_id="test_csv",
            raw_bytes=self.csv_path.read_bytes(),
            raw_text=self.csv_path.read_text(encoding="utf-8", errors="replace"),
            parsed_obj=pd.read_csv(self.csv_path),
        )

    def test_g01_not_null(self):
        result = RuleRegistry.get("G01")().evaluate(self.ctx)
        self.assertGreater(result.pass_rate, 0.0)
        self.assertIsNone(result.error)

    def test_g02_type_match(self):
        result = RuleRegistry.get("G02")().evaluate(self.ctx)
        self.assertGreater(result.total_records, 0)

    def test_g03_duplicate(self):
        result = RuleRegistry.get("G03")().evaluate(self.ctx)
        self.assertIsNone(result.error)

    def test_g05_encoding(self):
        result = RuleRegistry.get("G05")().evaluate(self.ctx)
        self.assertEqual(result.pass_rate, 1.0)

    def test_g06_bom(self):
        result = RuleRegistry.get("G06")().evaluate(self.ctx)
        self.assertEqual(result.pass_rate, 1.0)  # No BOM expected

    def test_g14_sha256(self):
        result = RuleRegistry.get("G14")().evaluate(self.ctx)
        self.assertEqual(result.pass_rate, 1.0)
        self.assertIn("sha256", result.details)

    def test_g15_file_size(self):
        result = RuleRegistry.get("G15")().evaluate(self.ctx)
        self.assertEqual(result.pass_rate, 1.0)


class TestCSVRules(unittest.TestCase):
    def setUp(self):
        self.csv_path = FIXTURES / "test019.csv"
        if not self.csv_path.exists():
            self.skipTest("CSV fixture not found")
        self.ctx = RuleContext(
            file_path=self.csv_path,
            data_type="csv",
            raw_text=self.csv_path.read_text(encoding="utf-8", errors="replace"),
            raw_bytes=self.csv_path.read_bytes(),
        )

    def test_csv01_delimiter(self):
        result = RuleRegistry.get("CSV01")().evaluate(self.ctx)
        self.assertEqual(result.pass_rate, 1.0)

    def test_csv06_field_count(self):
        result = RuleRegistry.get("CSV06")().evaluate(self.ctx)
        self.assertGreater(result.total_records, 0)


class TestJSONRules(unittest.TestCase):
    def test_json01_valid(self):
        path = FIXTURES / "y_object_empty.json"
        if not path.exists():
            self.skipTest("JSON fixture not found")
        ctx = RuleContext(file_path=path, data_type="json",
                          raw_text=path.read_text(encoding="utf-8"))
        result = RuleRegistry.get("JSON01")().evaluate(ctx)
        self.assertEqual(result.pass_rate, 1.0)

    def test_json02_trailing_comma(self):
        path = FIXTURES / "n_object_trailing_comma.json"
        if not path.exists():
            self.skipTest("JSON fixture not found")
        ctx = RuleContext(file_path=path, data_type="json",
                          raw_text=path.read_text(encoding="utf-8", errors="replace"))
        result = RuleRegistry.get("JSON02")().evaluate(ctx)
        self.assertEqual(result.pass_rate, 0.0)  # Should reject trailing comma


class TestLogRules(unittest.TestCase):
    def setUp(self):
        self.log_path = FIXTURES / "apache_sample_100.log"
        if not self.log_path.exists():
            self.skipTest("Log fixture not found")
        self.ctx = RuleContext(
            file_path=self.log_path,
            data_type="txt_log",
            raw_text=self.log_path.read_text(encoding="utf-8", errors="replace"),
        )

    def test_log01_timestamp(self):
        result = RuleRegistry.get("LOG01")().evaluate(self.ctx)
        self.assertEqual(result.pass_rate, 1.0)

    def test_log02_levels(self):
        result = RuleRegistry.get("LOG02")().evaluate(self.ctx)
        self.assertIn("levels", result.details)
        self.assertIn("error", result.details["levels"])


class TestScoringEngine(unittest.TestCase):
    def test_score_csv(self):
        from engine.scorer import ScoringEngine
        config = Path(__file__).resolve().parents[1] / "config" / "scoring_framework.json"
        csv_path = FIXTURES / "test019.csv"
        if not csv_path.exists():
            self.skipTest("CSV fixture not found")
        engine = ScoringEngine(str(config))
        report = engine.score_dataset(csv_path, "csv", "test_csv")
        self.assertGreater(report.final_score, 0)
        self.assertLessEqual(report.final_score, 100)
        self.assertEqual(report.standard_name, "W3C CSVW + ISO/IEC 25012")
        self.assertIn("SYN", report.criteria_scores)
        self.assertIn("SEC", report.criteria_scores)


if __name__ == "__main__":
    unittest.main()
