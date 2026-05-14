# DQ Scoring Engine

**3-Layer Data Quality Scoring Framework** for the Multi-Agent Data Quality Analysis Platform.

## Architecture

```
Layer 3: International Standards (W3C CSVW, JSON Schema, XSD, Parquet Spec...)
    ↓ defines criteria & weights
Layer 2: Evaluation Criteria (Syntax, Structure, Completeness, Consistency, Accuracy, Security)
    ↓ maps to rules
Layer 1: Static Rules (15 General + 48 Specific = 63 rules)
    ↓ produces scores
Output:  Final Score per dataset (0–100)
```

## Quick Start

```bash
cd dq-scoring-engine
pip install -r requirements.txt
python run_scoring_demo.py
```

## Project Structure

```
config/scoring_framework.json   # Standards → Criteria → Rules mapping
rules/
  base.py                       # BaseRule, RuleResult, RuleRegistry
  general.py                    # 15 General rules (G01–G15)
  csv_rules.py                  # 7 CSV-specific rules
  json_rules.py                 # 9 JSON-specific rules
  xml_rules.py                  # 6 XML-specific rules
  parquet_rules.py              # 8 Parquet-specific rules
  other_rules.py                # 23 rules (Avro/ORC/XLSX/FW/Log/Geo/Archive)
engine/
  scorer.py                     # Scoring engine (orchestration)
  reporter.py                   # Report generator (MD/CSV/JSON)
reports/                        # Generated output
```

## Integration with Multi-Agent Platform

```python
from engine.scorer import ScoringEngine

engine = ScoringEngine("config/scoring_framework.json")
report = engine.score_dataset("path/to/file.parquet", "parquet", "my_dataset")
print(report.final_score)  # e.g. 96.5
```
