# DQ Scoring Engine

**3-Layer Data Quality Scoring Framework** cho Multi-Agent Data Quality Analysis Platform.

> **Repo liên quan:** Data samples nằm tại [Prep_data](https://github.com/DrMutHo/Prep_data) (repo của nhóm).
> Repo này hoạt động **độc lập** — chỉ cần Prep_data khi muốn chạy demo trên dữ liệu thật.

---

## 🚀 Quick Start (cho team member)

### Cách 1: Setup tự động (recommended)

```bash
git clone https://github.com/<your-username>/dq-scoring-engine.git
cd dq-scoring-engine
bash setup.sh
```

Script sẽ tự:
1. Tạo venv + cài dependencies
2. Tìm/clone Prep_data nếu cần
3. Chạy tests + demo

### Cách 2: Manual setup

```bash
git clone https://github.com/<your-username>/dq-scoring-engine.git
cd dq-scoring-engine

# Cài đặt
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# Chạy tests (KHÔNG cần Prep_data)
.venv/bin/python -m unittest tests.test_rules -v

# Chạy demo (CẦN Prep_data cạnh bên)
git clone https://github.com/DrMutHo/Prep_data.git ../Prep_data
.venv/bin/python run_scoring_demo.py
```

---

## 📁 Cấu Trúc Thư Mục

```
dq-scoring-engine/
├── config/
│   └── scoring_framework.json    # Chuẩn QT + Trọng số + Rule mapping
├── rules/
│   ├── base.py                   # BaseRule, RuleResult, RuleRegistry
│   ├── general.py                # 15 General rules (G01–G15)
│   ├── csv_rules.py              # 7 CSV rules (CSV01–CSV07)
│   ├── json_rules.py             # 9 JSON rules (JSON01–JSON09)
│   ├── xml_rules.py              # 6 XML rules (XML01–XML06)
│   ├── parquet_rules.py          # 8 Parquet rules (PQ01–PQ08)
│   └── other_rules.py            # 18 rules (Avro/ORC/XLSX/FW/Log/Geo/OSM/Archive)
├── engine/
│   ├── scorer.py                 # Scoring engine chính
│   └── reporter.py               # Sinh report (MD/CSV/JSON)
├── tests/
│   ├── fixtures/                 # Test data có sẵn (không cần Prep_data)
│   └── test_rules.py             # 17 unit tests
├── reports/                      # Output demo
├── setup.sh                      # Script setup tự động
├── run_scoring_demo.py           # Demo chấm điểm
└── requirements.txt
```

---

## 🏗️ Architecture

```
Layer 3: International Standards (W3C CSVW, JSON Schema, XSD, Parquet Spec...)
    ↓ defines criteria & weights
Layer 2: Evaluation Criteria (Syntax, Structure, Completeness, Consistency, Accuracy, Security)
    ↓ maps to rules
Layer 1: Static Rules (15 General + 48 Specific = 63 rules)
    ↓ produces scores
Output:  Final Score per dataset (0–100)
```

Hỗ trợ **12 loại data**: CSV, JSON, XML, Parquet, Avro, ORC, XLSX, Fixed-width, Log, GeoJSON, OSM, Archives.

---

## 💻 API Usage

```python
from engine.scorer import ScoringEngine

engine = ScoringEngine("config/scoring_framework.json")
report = engine.score_dataset("path/to/file.parquet", "parquet", "my_dataset")

print(report.final_score)           # → 99.4
print(report.criteria_scores)       # → {SYN: ..., STR: ..., ...}
print(report.to_dict())             # → JSON-serializable dict
```

---

## 📊 Kết Quả Demo

| Dataset | Type | Score | Status |
|---|---|---|---|
| csvw_dialect | CSV | 100.0 | ✅ |
| nyc_tlc | Parquet | 99.4 | ✅ |
| usgs_geojson | GeoJSON | 100.0 | ✅ |
| noaa_ghcn | Fixed-width | 100.0 | ✅ |
| gharchive | JSONL | 73.2 | ⚠️ |
| **Average (16 datasets)** | | **91.7** | |

Chi tiết xem: [reports/TEAM_REPORT.md](reports/TEAM_REPORT.md)

---

## 🔧 Thêm Rule Mới

```python
# rules/my_rules.py
from rules.base import BaseRule, RuleContext, RuleRegistry, RuleResult

@RuleRegistry.register
class MyRule(BaseRule):
    rule_id = "CUSTOM01"
    rule_tag = "specific"
    criteria = "ACC"
    applicable_types = ["csv"]

    def evaluate(self, ctx: RuleContext) -> RuleResult:
        return self._result(total=100, passed=95, details={"info": "..."})
```

Sau đó import trong `engine/scorer.py` → rule tự đăng ký.
