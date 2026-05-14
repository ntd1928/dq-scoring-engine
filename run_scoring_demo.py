#!/usr/bin/env python3
"""Demo: Score all sample datasets and generate reports.

Usage:
    cd dq-scoring-engine
    python run_scoring_demo.py                                  # auto-discover sibling Prep_data
    python run_scoring_demo.py --data-dir /path/to/data         # explicit data directory
    python run_scoring_demo.py --data-dir ../Prep_data/dq_raw_probe/data
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Ensure imports work
sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine.scorer import ScoringEngine
from engine.reporter import generate_markdown, generate_csv, generate_json

PROJECT_ROOT = Path(__file__).resolve().parent
CONFIG = PROJECT_ROOT / "config" / "scoring_framework.json"
REPORTS = PROJECT_ROOT / "reports"


def _discover_data_dir() -> Path:
    """Try to find data directory automatically."""
    # 1. Check sibling Prep_data (when repos are side by side)
    sibling = PROJECT_ROOT.parent / "Prep_data" / "dq_raw_probe" / "data"
    if sibling.exists():
        return sibling
    # 2. Check parent (when inside Prep_data)
    parent = PROJECT_ROOT.parent / "dq_raw_probe" / "data"
    if parent.exists():
        return parent
    # 3. Check tests/fixtures as fallback
    fixtures = PROJECT_ROOT / "tests" / "fixtures"
    if fixtures.exists():
        return fixtures
    return Path("./data")


def _parse_args():
    parser = argparse.ArgumentParser(description="DQ Scoring Engine Demo")
    parser.add_argument("--data-dir", type=Path, default=None,
                        help="Path to data directory containing sample files")
    return parser.parse_args()


args = _parse_args()
PREP_DATA = args.data_dir if args.data_dir else _discover_data_dir()

# Dataset definitions: (file_path_relative_to_PREP_DATA, data_type, dataset_id)
DATASETS = [
    # CSV
    ("csvw/test019.csv",                                        "csv",        "csvw_dialect"),
    ("csv_spectrum/comma_in_quotes.csv",                        "csv",        "csv_spectrum_edges"),
    ("gdelt_events/gdelt_events_20260506_sample_1000.csv",      "csv",        "gdelt_events"),
    # JSON
    ("openfda_drug_event/drug_event_limit_10.json",             "json",       "openfda_drug_event"),
    ("sec_edgar/CIK0000320193_submissions.json",                "json",       "sec_edgar"),
    # JSONL (treated as json)
    ("gharchive/gharchive_2026_05_01_00_sample_1000.jsonl",     "json",       "gharchive"),
    # GeoJSON
    ("usgs_geojson/all_day.geojson",                            "geojson",    "usgs_geojson"),
    # OSM
    ("osm_overpass/hoankiem_osm_sample.json",                   "osm",        "osm_overpass"),
    # XML
    ("stackexchange_xml/posts_sample.xml",                      "xml",        "stackexchange_xml"),
    # Parquet
    ("nyc_tlc/yellow_tripdata_2026_01_sample_1000.parquet",     "parquet",    "nyc_tlc"),
    ("open_targets/disease_sample_100.parquet",                  "parquet",    "open_targets"),
    # XLSX
    ("uci_online_retail/online_retail_sample_1000.xlsx",        "xlsx",       "uci_online_retail"),
    ("worldbank/pop_india.xls",                                  "xlsx",       "worldbank_wdi"),
    # Fixed-width
    ("noaa_ghcn/VM000048900_sample_200_lines.dly",              "fixed_width","noaa_ghcn"),
    # Log
    ("loghub_apache/apache_sample_100.log",                     "txt_log",    "loghub_apache"),
    # Pageviews (text)
    ("wikimedia_pageviews/pageviews_20260501_00_sample_1000.txt","txt_log",   "wikimedia_pageviews"),
]


def main():
    engine = ScoringEngine(str(CONFIG))
    reports = []

    print("=" * 70)
    print("  DQ SCORING ENGINE — Multi-Agent Data Quality Platform")
    print("=" * 70)
    print()

    for rel_path, dtype, did in DATASETS:
        fpath = PREP_DATA / rel_path
        if not fpath.exists():
            print(f"  ⏭  SKIP {did:30s} — file not found: {rel_path}")
            continue

        try:
            rpt = engine.score_dataset(fpath, dtype, did)
            reports.append(rpt)

            # Print summary
            bar = "█" * int(rpt.final_score / 2) + "░" * (50 - int(rpt.final_score / 2))
            print(f"  {'✅' if rpt.final_score >= 80 else '⚠️'} {did:30s}  {bar}  {rpt.final_score:6.1f}/100")

            # Print criteria breakdown
            for cid, cs in rpt.criteria_scores.items():
                print(f"     └─ {cs.criteria_name:25s}  {cs.score_100:6.1f}/100 × {cs.weight:.0%} = {cs.weighted_score:5.1f}")

            print()
        except Exception as e:
            print(f"  ❌ {did:30s} — ERROR: {e}")
            print()

    # Generate reports
    REPORTS.mkdir(parents=True, exist_ok=True)
    if reports:
        generate_markdown(reports, REPORTS / "scoring_summary.md")
        generate_csv(reports, REPORTS / "scoring_results.csv")
        generate_json(reports, REPORTS / "scoring_results.json")
        print("=" * 70)
        print(f"  📊 Reports generated in {REPORTS}/")
        print(f"     - scoring_summary.md")
        print(f"     - scoring_results.csv")
        print(f"     - scoring_results.json")
        print(f"  📈 Datasets scored: {len(reports)}")
        avg = sum(r.final_score for r in reports) / len(reports)
        print(f"  📊 Average score: {avg:.1f}/100")
        print("=" * 70)
    else:
        print("  No datasets scored.")


if __name__ == "__main__":
    main()
