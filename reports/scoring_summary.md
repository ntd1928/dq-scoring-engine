# DQ Scoring Report
**Generated:** 2026-05-14 08:38 UTC
**Datasets scored:** 16

## csvw_dialect
- **Data type:** csv
- **Standard:** W3C CSVW + ISO/IEC 25012
- **FINAL SCORE: 100.0/100**

| Criteria | Weight | Score | Weighted |
|---|---|---|---|
| Syntax Validity | 25% | 100.0/100 | 25.0 |
| Structural Conformance | 25% | 100.0/100 | 25.0 |
| Completeness | 20% | 100.0/100 | 20.0 |
| Consistency | 15% | 100.0/100 | 15.0 |
| Accuracy / Range | 10% | 100.0/100 | 10.0 |
| Security / Integrity | 5% | 100.0/100 | 5.0 |

<details><summary>Rule Details</summary>

| Rule | Tag | Criteria | Pass Rate | Details |
|---|---|---|---|---|
| G05 | general | SYN | 100.00% | {"encoding": "utf-8"} |
| G06 | general | SYN | 100.00% | {"has_bom": false} |
| G12 | general | SYN | 100.00% | {"whitespace_violations": 0} |
| CSV01 | specific | SYN | 100.00% | {"detected_delimiter": "','"} |
| CSV03 | specific | SYN | 100.00% | {"physical_lines": 2, "logical_records": 2, "has_quoted_newline": false} |
| CSV04 | specific | SYN | 100.00% | {"expected_columns": 5, "mismatched_rows": 0} |
| CSV07 | specific | SYN | 100.00% | {"non_ascii_bytes": 0, "utf8_decodable": true} |
| G02 | general | STR | 100.00% | {"typed_columns": 5, "object_columns": 0} |
| G10 | general | STR | 100.00% | {"delimiter": "'\\t'", "mode_field_count": 1, "distribution": {"1": 2}} |
| CSV02 | specific | STR | 100.00% | {"has_header": false} |
| CSV05 | specific | STR | 100.00% | {"comment_count": 0} |
| CSV06 | specific | STR | 100.00% | {"mode_field_count": 5, "distribution": {"5": 2}} |
| G01 | general | CMP | 100.00% | {"null_count": 0} |
| G04 | general | CMP | 100.00% | {"row_count": 1} |
| G03 | general | CST | 100.00% | {"duplicate_rows": 0} |
| G09 | general | CST | 100.00% | {"note": "no date pairs found"} |
| G07 | general | ACC | 100.00% | {"note": "no timestamp columns detected"} |
| G08 | general | ACC | 100.00% |  |
| G13 | general | ACC | 100.00% | {"note": "enum config not provided; skipped"} |
| G14 | general | SEC | 100.00% | {"sha256": "6045e523b338c8934b7e9c918c3de59925f9ff90a26fb17a86c9388da41bbaad", " |
| G15 | general | SEC | 100.00% | {"size_bytes": 137, "size_mb": 0.0} |

</details>

---

## csv_spectrum_edges
- **Data type:** csv
- **Standard:** W3C CSVW + ISO/IEC 25012
- **FINAL SCORE: 100.0/100**

| Criteria | Weight | Score | Weighted |
|---|---|---|---|
| Syntax Validity | 25% | 100.0/100 | 25.0 |
| Structural Conformance | 25% | 100.0/100 | 25.0 |
| Completeness | 20% | 100.0/100 | 20.0 |
| Consistency | 15% | 100.0/100 | 15.0 |
| Accuracy / Range | 10% | 100.0/100 | 10.0 |
| Security / Integrity | 5% | 100.0/100 | 5.0 |

<details><summary>Rule Details</summary>

| Rule | Tag | Criteria | Pass Rate | Details |
|---|---|---|---|---|
| G05 | general | SYN | 100.00% | {"encoding": "utf-8"} |
| G06 | general | SYN | 100.00% | {"has_bom": false} |
| G12 | general | SYN | 100.00% | {"whitespace_violations": 0} |
| CSV01 | specific | SYN | 100.00% | {"detected_delimiter": "','"} |
| CSV03 | specific | SYN | 100.00% | {"physical_lines": 2, "logical_records": 2, "has_quoted_newline": false} |
| CSV04 | specific | SYN | 100.00% | {"expected_columns": 5, "mismatched_rows": 0} |
| CSV07 | specific | SYN | 100.00% | {"non_ascii_bytes": 0, "utf8_decodable": true} |
| G02 | general | STR | 100.00% | {"typed_columns": 5, "object_columns": 0} |
| G10 | general | STR | 100.00% | {"delimiter": "'\\t'", "mode_field_count": 1, "distribution": {"1": 2}} |
| CSV02 | specific | STR | 100.00% | {"has_header": true} |
| CSV05 | specific | STR | 100.00% | {"comment_count": 0} |
| CSV06 | specific | STR | 100.00% | {"mode_field_count": 5, "distribution": {"5": 2}} |
| G01 | general | CMP | 100.00% | {"null_count": 0} |
| G04 | general | CMP | 100.00% | {"row_count": 1} |
| G03 | general | CST | 100.00% | {"duplicate_rows": 0} |
| G09 | general | CST | 100.00% | {"note": "no date pairs found"} |
| G07 | general | ACC | 100.00% | {"note": "no timestamp columns detected"} |
| G08 | general | ACC | 100.00% |  |
| G13 | general | ACC | 100.00% | {"note": "enum config not provided; skipped"} |
| G14 | general | SEC | 100.00% | {"sha256": "f7654bf8e69586c8fe7f7f89392d2ed551be0e468e7101187bb482357d9a7815", " |
| G15 | general | SEC | 100.00% | {"size_bytes": 68, "size_mb": 0.0} |

</details>

---

## gdelt_events
- **Data type:** csv
- **Standard:** W3C CSVW + ISO/IEC 25012
- **FINAL SCORE: 93.76/100**

| Criteria | Weight | Score | Weighted |
|---|---|---|---|
| Syntax Validity | 25% | 88.66/100 | 22.2 |
| Structural Conformance | 25% | 86.38/100 | 21.6 |
| Completeness | 20% | 100.0/100 | 20.0 |
| Consistency | 15% | 100.0/100 | 15.0 |
| Accuracy / Range | 10% | 100.0/100 | 10.0 |
| Security / Integrity | 5% | 100.0/100 | 5.0 |

<details><summary>Rule Details</summary>

| Rule | Tag | Criteria | Pass Rate | Details |
|---|---|---|---|---|
| G05 | general | SYN | 100.00% | {"encoding": "utf-8"} |
| G06 | general | SYN | 100.00% | {"has_bom": false} |
| G12 | general | SYN | 100.00% | ERROR: No DataFrame available |
| CSV01 | specific | SYN | 100.00% | {"detected_delimiter": "'\\t'"} |
| CSV03 | specific | SYN | 100.00% | {"physical_lines": 1000, "logical_records": 1000, "has_quoted_newline": false} |
| CSV04 | specific | SYN | 20.60% | {"expected_columns": 1, "mismatched_rows": 794} |
| CSV07 | specific | SYN | 100.00% | {"non_ascii_bytes": 106, "utf8_decodable": true} |
| G02 | general | STR | 100.00% | ERROR: No DataFrame available |
| G10 | general | STR | 100.00% | {"delimiter": "'\\t'", "mode_field_count": 58, "distribution": {"58": 1000}} |
| CSV02 | specific | STR | 100.00% | {"has_header": false} |
| CSV05 | specific | STR | 100.00% | {"comment_count": 0} |
| CSV06 | specific | STR | 31.90% | {"mode_field_count": 5, "distribution": {"1": 206, "5": 319, "3": 162, "7": 226, |
| G01 | general | CMP | 100.00% | ERROR: No DataFrame available |
| G04 | general | CMP | 100.00% | ERROR: No DataFrame available |
| G03 | general | CST | 100.00% | ERROR: No DataFrame available |
| G09 | general | CST | 100.00% | ERROR: No DataFrame available |
| G07 | general | ACC | 100.00% | ERROR: No DataFrame available |
| G08 | general | ACC | 100.00% | ERROR: No DataFrame available |
| G13 | general | ACC | 100.00% | {"note": "enum config not provided; skipped"} |
| G14 | general | SEC | 100.00% | {"sha256": "18f8eb5e1375f306f95475fb8d56985e348ffbfcef70cb58da92f6a09625fec7", " |
| G15 | general | SEC | 100.00% | {"size_bytes": 376305, "size_mb": 0.36} |

</details>

---

## openfda_drug_event
- **Data type:** json
- **Standard:** JSON Schema Draft 2020-12 + RFC 8259
- **FINAL SCORE: 93.36/100**

| Criteria | Weight | Score | Weighted |
|---|---|---|---|
| Syntax Validity | 30% | 80.39/100 | 24.1 |
| Structural Conformance | 25% | 100.0/100 | 25.0 |
| Completeness | 15% | 94.93/100 | 14.2 |
| Consistency | 15% | 100.0/100 | 15.0 |
| Accuracy / Range | 10% | 100.0/100 | 10.0 |
| Security / Integrity | 5% | 100.0/100 | 5.0 |

<details><summary>Rule Details</summary>

| Rule | Tag | Criteria | Pass Rate | Details |
|---|---|---|---|---|
| G05 | general | SYN | 100.00% | {"encoding": "utf-8"} |
| G06 | general | SYN | 100.00% | {"has_bom": false} |
| JSON01 | specific | SYN | 100.00% |  |
| JSON02 | specific | SYN | 100.00% | {"trailing_comma_count": 0} |
| JSON08 | specific | SYN | 1.97% |  |
| G02 | general | STR | 100.00% | ERROR: No DataFrame available |
| JSON03 | specific | STR | 100.00% | {"max_depth": 8, "threshold": 20} |
| JSON07 | specific | STR | 100.00% | {"note": "informational rule"} |
| G01 | general | CMP | 100.00% | ERROR: No DataFrame available |
| G04 | general | CMP | 100.00% | ERROR: No DataFrame available |
| JSON06 | specific | CMP | 84.78% | {"total_keys": 23, "records": 10} |
| G03 | general | CST | 100.00% | ERROR: No DataFrame available |
| JSON04 | specific | CST | 100.00% | {"unique_keysets": 4} |
| JSON05 | specific | CST | 100.00% | {"note": "fewer than 2 arrays"} |
| JSON09 | specific | CST | 100.00% | {"event_types": {}} |
| G07 | general | ACC | 100.00% | ERROR: No DataFrame available |
| G08 | general | ACC | 100.00% | ERROR: No DataFrame available |
| G11 | general | ACC | 100.00% | ERROR: No DataFrame available |
| G14 | general | SEC | 100.00% | {"sha256": "66880f746f993c50cb6aa40b668b959e9c4ac4aa3fa8f7ac5d732beba8b534a8", " |
| G15 | general | SEC | 100.00% | {"size_bytes": 612444, "size_mb": 0.58} |

</details>

---

## sec_edgar
- **Data type:** json
- **Standard:** JSON Schema Draft 2020-12 + RFC 8259
- **FINAL SCORE: 96.25/100**

| Criteria | Weight | Score | Weighted |
|---|---|---|---|
| Syntax Validity | 30% | 100.0/100 | 30.0 |
| Structural Conformance | 25% | 100.0/100 | 25.0 |
| Completeness | 15% | 100.0/100 | 15.0 |
| Consistency | 15% | 75.0/100 | 11.2 |
| Accuracy / Range | 10% | 100.0/100 | 10.0 |
| Security / Integrity | 5% | 100.0/100 | 5.0 |

<details><summary>Rule Details</summary>

| Rule | Tag | Criteria | Pass Rate | Details |
|---|---|---|---|---|
| G05 | general | SYN | 100.00% | {"encoding": "utf-8"} |
| G06 | general | SYN | 100.00% | {"has_bom": false} |
| JSON01 | specific | SYN | 100.00% |  |
| JSON02 | specific | SYN | 100.00% | {"trailing_comma_count": 0} |
| JSON08 | specific | SYN | 100.00% |  |
| G02 | general | STR | 100.00% | ERROR: No DataFrame available |
| JSON03 | specific | STR | 100.00% | {"max_depth": 4, "threshold": 20} |
| JSON07 | specific | STR | 100.00% | {"note": "informational rule"} |
| G01 | general | CMP | 100.00% | ERROR: No DataFrame available |
| G04 | general | CMP | 100.00% | ERROR: No DataFrame available |
| JSON06 | specific | CMP | 100.00% |  |
| G03 | general | CST | 100.00% | ERROR: No DataFrame available |
| JSON04 | specific | CST | 100.00% | {"note": "not a record list"} |
| JSON05 | specific | CST | 0.00% | {"array_lengths": {"tickers": 1, "exchanges": 1, "formerNames": 3}} |
| JSON09 | specific | CST | 100.00% | {"event_types": {"<missing>": 1}} |
| G07 | general | ACC | 100.00% | ERROR: No DataFrame available |
| G08 | general | ACC | 100.00% | ERROR: No DataFrame available |
| G11 | general | ACC | 100.00% | ERROR: No DataFrame available |
| G14 | general | SEC | 100.00% | {"sha256": "3f737dc9c53367e65f6131057e597f8d389fac6127acf012c1b5b15331b0cfbe", " |
| G15 | general | SEC | 100.00% | {"size_bytes": 164555, "size_mb": 0.16} |

</details>

---

## gharchive
- **Data type:** json
- **Standard:** JSON Schema Draft 2020-12 + RFC 8259
- **FINAL SCORE: 73.17/100**

| Criteria | Weight | Score | Weighted |
|---|---|---|---|
| Syntax Validity | 30% | 80.0/100 | 24.0 |
| Structural Conformance | 25% | 66.67/100 | 16.7 |
| Completeness | 15% | 66.67/100 | 10.0 |
| Consistency | 15% | 50.0/100 | 7.5 |
| Accuracy / Range | 10% | 100.0/100 | 10.0 |
| Security / Integrity | 5% | 100.0/100 | 5.0 |

<details><summary>Rule Details</summary>

| Rule | Tag | Criteria | Pass Rate | Details |
|---|---|---|---|---|
| G05 | general | SYN | 100.00% | {"encoding": "utf-8"} |
| G06 | general | SYN | 100.00% | {"has_bom": false} |
| JSON01 | specific | SYN | 0.00% | {"error": "Extra data: line 2 column 1 (char 616)"} |
| JSON02 | specific | SYN | 100.00% | {"trailing_comma_count": 0} |
| JSON08 | specific | SYN | 100.00% |  |
| G02 | general | STR | 100.00% | ERROR: No DataFrame available |
| JSON03 | specific | STR | 0.00% | {"error": "parse failed"} |
| JSON07 | specific | STR | 100.00% | {"note": "informational rule"} |
| G01 | general | CMP | 100.00% | ERROR: No DataFrame available |
| G04 | general | CMP | 100.00% | ERROR: No DataFrame available |
| JSON06 | specific | CMP | 0.00% |  |
| G03 | general | CST | 100.00% | ERROR: No DataFrame available |
| JSON04 | specific | CST | 0.00% |  |
| JSON05 | specific | CST | 0.00% |  |
| JSON09 | specific | CST | 100.00% | {"event_types": {"PushEvent": 851, "CreateEvent": 52, "DeleteEvent": 20, "PullRe |
| G07 | general | ACC | 100.00% | ERROR: No DataFrame available |
| G08 | general | ACC | 100.00% | ERROR: No DataFrame available |
| G11 | general | ACC | 100.00% | ERROR: No DataFrame available |
| G14 | general | SEC | 100.00% | {"sha256": "f91ce371e7c90f8a65a670b5bc6b39174372b4e77fa92bd330448bb2b37f069a", " |
| G15 | general | SEC | 100.00% | {"size_bytes": 903995, "size_mb": 0.86} |

</details>

---

## usgs_geojson
- **Data type:** geojson
- **Standard:** RFC 7946 (GeoJSON)
- **FINAL SCORE: 100.0/100**

| Criteria | Weight | Score | Weighted |
|---|---|---|---|
| Syntax Validity | 20% | 100.0/100 | 20.0 |
| Structural Conformance | 25% | 100.0/100 | 25.0 |
| Completeness | 20% | 100.0/100 | 20.0 |
| Consistency | 15% | 100.0/100 | 15.0 |
| Accuracy / Range | 15% | 100.0/100 | 15.0 |
| Security / Integrity | 5% | 100.0/100 | 5.0 |

<details><summary>Rule Details</summary>

| Rule | Tag | Criteria | Pass Rate | Details |
|---|---|---|---|---|
| G05 | general | SYN | 100.00% | {"encoding": "utf-8"} |
| JSON01 | specific | SYN | 100.00% |  |
| G02 | general | STR | 100.00% | ERROR: No DataFrame available |
| GEO01 | specific | STR | 100.00% | {"type": "FeatureCollection"} |
| G01 | general | CMP | 100.00% | ERROR: No DataFrame available |
| GEO02 | specific | CMP | 100.00% | {"missing_geometry": 0} |
| G03 | general | CST | 100.00% | ERROR: No DataFrame available |
| GEO03 | specific | ACC | 100.00% |  |
| GEO04 | specific | ACC | 100.00% | {"geometry_types": {"Point": 557}} |
| G14 | general | SEC | 100.00% | {"sha256": "d8d9c17abf4881591d7a8fc42903500cf97dbbac9cd96d7aa4330a863b8086c8", " |
| G15 | general | SEC | 100.00% | {"size_bytes": 404409, "size_mb": 0.39} |

</details>

---

## osm_overpass
- **Data type:** osm
- **Standard:** OSM XML/PBF Specification
- **FINAL SCORE: 92.07/100**

| Criteria | Weight | Score | Weighted |
|---|---|---|---|
| Syntax Validity | 15% | 100.0/100 | 15.0 |
| Structural Conformance | 25% | 100.0/100 | 25.0 |
| Completeness | 25% | 68.26/100 | 17.1 |
| Consistency | 15% | 100.0/100 | 15.0 |
| Accuracy / Range | 15% | 100.0/100 | 15.0 |
| Security / Integrity | 5% | 100.0/100 | 5.0 |

<details><summary>Rule Details</summary>

| Rule | Tag | Criteria | Pass Rate | Details |
|---|---|---|---|---|
| G05 | general | SYN | 100.00% | {"encoding": "utf-8"} |
| JSON01 | specific | SYN | 100.00% |  |
| G02 | general | STR | 100.00% | ERROR: No DataFrame available |
| OSM01 | specific | STR | 100.00% | {"types": {"node": 35104, "way": 4963, "relation": 94}} |
| G01 | general | CMP | 100.00% | ERROR: No DataFrame available |
| OSM02 | specific | CMP | 100.00% | {"missing_latlon": 0} |
| OSM03 | specific | CMP | 4.79% | {"tagged": 1923, "untagged": 38238} |
| G03 | general | CST | 100.00% | ERROR: No DataFrame available |
| GEO03 | specific | ACC | 100.00% |  |
| G14 | general | SEC | 100.00% | {"sha256": "5f34e92a19692dd6659fb4fc22a66da8b07013efcffa727d7e89afd2b84a933f", " |
| G15 | general | SEC | 100.00% | {"size_bytes": 6894107, "size_mb": 6.57} |

</details>

---

## stackexchange_xml
- **Data type:** xml
- **Standard:** W3C XML Schema (XSD 1.1)
- **FINAL SCORE: 96.71/100**

| Criteria | Weight | Score | Weighted |
|---|---|---|---|
| Syntax Validity | 25% | 100.0/100 | 25.0 |
| Structural Conformance | 30% | 100.0/100 | 30.0 |
| Completeness | 15% | 78.1/100 | 11.7 |
| Consistency | 15% | 100.0/100 | 15.0 |
| Accuracy / Range | 10% | 100.0/100 | 10.0 |
| Security / Integrity | 5% | 100.0/100 | 5.0 |

<details><summary>Rule Details</summary>

| Rule | Tag | Criteria | Pass Rate | Details |
|---|---|---|---|---|
| G05 | general | SYN | 100.00% | {"encoding": "utf-8"} |
| XML01 | specific | SYN | 100.00% |  |
| XML05 | specific | SYN | 100.00% | {"html_entity_count": 1430} |
| G02 | general | STR | 100.00% | ERROR: No DataFrame available |
| XML02 | specific | STR | 100.00% | {"namespaces": [], "count": 0} |
| XML03 | specific | STR | 100.00% | {"note": "XSD validation skipped — no schema provided"} |
| G01 | general | CMP | 100.00% | ERROR: No DataFrame available |
| G04 | general | CMP | 100.00% | ERROR: No DataFrame available |
| XML04 | specific | CMP | 56.19% | {"unique_attrs": 22, "rows": 80} |
| XML06 | specific | CMP | 56.19% | {"missing_attrs": {"LastEditorUserId": 43, "OwnerDisplayName": 73, "ClosedDate": |
| G03 | general | CST | 100.00% | ERROR: No DataFrame available |
| G07 | general | ACC | 100.00% | ERROR: No DataFrame available |
| G08 | general | ACC | 100.00% | ERROR: No DataFrame available |
| G14 | general | SEC | 100.00% | {"sha256": "5848a9e6ec7bd387c0fa3560771a2c2cb46445dea07e9da8f4416af467a9a070", " |
| G15 | general | SEC | 100.00% | {"size_bytes": 65648, "size_mb": 0.06} |

</details>

---

## nyc_tlc
- **Data type:** parquet
- **Standard:** Apache Parquet Format Spec + ISO/IEC 25012
- **FINAL SCORE: 99.42/100**

| Criteria | Weight | Score | Weighted |
|---|---|---|---|
| Syntax Validity | 10% | 100.0/100 | 10.0 |
| Structural Conformance | 30% | 100.0/100 | 30.0 |
| Completeness | 25% | 100.0/100 | 25.0 |
| Consistency | 15% | 100.0/100 | 15.0 |
| Accuracy / Range | 15% | 96.1/100 | 14.4 |
| Security / Integrity | 5% | 100.0/100 | 5.0 |

<details><summary>Rule Details</summary>

| Rule | Tag | Criteria | Pass Rate | Details |
|---|---|---|---|---|
| PQ01 | specific | SYN | 100.00% | {"has_magic": true} |
| G02 | general | STR | 100.00% | {"typed_columns": 20, "object_columns": 0} |
| PQ02 | specific | STR | 100.00% | {"columns": ["VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime", "passe |
| PQ05 | specific | STR | 100.00% | {"nested_columns": [], "nested_count": 0} |
| G01 | general | CMP | 100.00% | {"null_count": 0} |
| G04 | general | CMP | 100.00% | {"row_count": 1000} |
| PQ04 | specific | CMP | 100.00% | {"null_columns": {}} |
| G03 | general | CST | 100.00% | {"duplicate_rows": 0} |
| PQ03 | specific | CST | 100.00% | {"note": "single-file check — drift detection needs multi-file comparison"} |
| G07 | general | ACC | 100.00% | {"timestamp_columns": ["tpep_pickup_datetime", "tpep_dropoff_datetime"]} |
| G08 | general | ACC | 100.00% |  |
| PQ06 | specific | ACC | 99.74% | {"negative_columns": {"fare_amount": 7, "extra": 6, "mta_tax": 7, "improvement_s |
| PQ07 | specific | ACC | 84.66% | {"zero_columns": {"passenger_count": 12, "trip_distance": 7, "fare_amount": 1, " |
| G14 | general | SEC | 100.00% | {"sha256": "f41ede50ef7434a6646c89cfb21528a1debd906789fecb97afb143c1828a351d", " |
| G15 | general | SEC | 100.00% | {"size_bytes": 33080, "size_mb": 0.03} |
| PQ08 | specific | SEC | 100.00% | {"num_row_groups": 1, "num_rows": 1000, "num_columns": 20} |

</details>

---

## open_targets
- **Data type:** parquet
- **Standard:** Apache Parquet Format Spec + ISO/IEC 25012
- **FINAL SCORE: 92.86/100**

| Criteria | Weight | Score | Weighted |
|---|---|---|---|
| Syntax Validity | 10% | 100.0/100 | 10.0 |
| Structural Conformance | 30% | 76.19/100 | 22.9 |
| Completeness | 25% | 100.0/100 | 25.0 |
| Consistency | 15% | 100.0/100 | 15.0 |
| Accuracy / Range | 15% | 100.0/100 | 15.0 |
| Security / Integrity | 5% | 100.0/100 | 5.0 |

<details><summary>Rule Details</summary>

| Rule | Tag | Criteria | Pass Rate | Details |
|---|---|---|---|---|
| PQ01 | specific | SYN | 100.00% | {"has_magic": true} |
| G02 | general | STR | 28.57% | {"typed_columns": 4, "object_columns": 10} |
| PQ02 | specific | STR | 100.00% | {"columns": ["id", "code", "name", "description", "dbXRefs", "parents", "synonym |
| PQ05 | specific | STR | 100.00% | {"nested_columns": ["dbXRefs", "parents", "synonyms", "obsoleteTerms", "obsolete |
| G01 | general | CMP | 100.00% | {"null_count": 0} |
| G04 | general | CMP | 100.00% | {"row_count": 100} |
| PQ04 | specific | CMP | 100.00% | {"null_columns": {}} |
| G03 | error | CST | 100.00% | ERROR: unhashable type: 'numpy.ndarray' |
| PQ03 | specific | CST | 100.00% | {"note": "single-file check — drift detection needs multi-file comparison"} |
| G07 | general | ACC | 100.00% | {"note": "no timestamp columns detected"} |
| G08 | general | ACC | 100.00% | {"note": "no numeric columns"} |
| PQ06 | specific | ACC | 100.00% | {"negative_columns": {}} |
| PQ07 | specific | ACC | 100.00% | {"zero_columns": {}} |
| G14 | general | SEC | 100.00% | {"sha256": "f59d771af58987d71624862207409ebed3d2ead3814ce5e3ba8defde07e563a8", " |
| G15 | general | SEC | 100.00% | {"size_bytes": 34441, "size_mb": 0.03} |
| PQ08 | specific | SEC | 100.00% | {"num_row_groups": 1, "num_rows": 100, "num_columns": 20} |

</details>

---

## uci_online_retail
- **Data type:** xlsx
- **Standard:** ISO/IEC 29500 (OOXML) + ISO/IEC 25012
- **FINAL SCORE: 82.48/100**

| Criteria | Weight | Score | Weighted |
|---|---|---|---|
| Syntax Validity | 15% | 0.0/100 | 0.0 |
| Structural Conformance | 25% | 90.62/100 | 22.7 |
| Completeness | 25% | 99.99/100 | 25.0 |
| Consistency | 15% | 98.85/100 | 14.8 |
| Accuracy / Range | 15% | 100.0/100 | 15.0 |
| Security / Integrity | 5% | 100.0/100 | 5.0 |

<details><summary>Rule Details</summary>

| Rule | Tag | Criteria | Pass Rate | Details |
|---|---|---|---|---|
| G05 | general | SYN | 0.00% | {"error_position": 12} |
| G02 | general | STR | 75.00% | {"typed_columns": 6, "object_columns": 2} |
| XLS01 | specific | STR | 100.00% | {"sheets": ["Sheet1"], "count": 1} |
| XLS02 | specific | STR | 100.00% | {"first_row_all_string": true} |
| XLS04 | specific | STR | 87.50% | {"mixed_columns": ["StockCode"]} |
| G01 | general | CMP | 99.98% | {"null_count": 2} |
| G04 | general | CMP | 100.00% | {"row_count": 1000} |
| XLS03 | specific | CMP | 100.00% | {"blank_cells": 0, "blank_rate": 0.0} |
| G03 | general | CST | 97.70% | {"duplicate_rows": 23} |
| G09 | general | CST | 100.00% | {"note": "no date pairs found"} |
| G07 | general | ACC | 100.00% | {"timestamp_columns": ["InvoiceDate"]} |
| G08 | general | ACC | 100.00% |  |
| XLS05 | specific | ACC | 100.00% | {"date_columns": ["InvoiceDate"]} |
| G14 | general | SEC | 100.00% | {"sha256": "e6ecfe3ee110ea4e665539b11da8ca0c1bdcf6041082f3d30a0c6979426a3e71", " |
| G15 | general | SEC | 100.00% | {"size_bytes": 52747, "size_mb": 0.05} |

</details>

---

## worldbank_wdi
- **Data type:** xlsx
- **Standard:** ISO/IEC 29500 (OOXML) + ISO/IEC 25012
- **FINAL SCORE: 72.89/100**

| Criteria | Weight | Score | Weighted |
|---|---|---|---|
| Syntax Validity | 15% | 0.0/100 | 0.0 |
| Structural Conformance | 25% | 98.21/100 | 24.6 |
| Completeness | 25% | 53.33/100 | 13.3 |
| Consistency | 15% | 100.0/100 | 15.0 |
| Accuracy / Range | 15% | 100.0/100 | 15.0 |
| Security / Integrity | 5% | 100.0/100 | 5.0 |

<details><summary>Rule Details</summary>

| Rule | Tag | Criteria | Pass Rate | Details |
|---|---|---|---|---|
| G05 | general | SYN | 0.00% | {"error_position": 0} |
| G02 | general | STR | 98.57% | {"typed_columns": 69, "object_columns": 1} |
| XLS01 | specific | STR | 100.00% | {"sheets": ["Data", "Metadata - Countries", "Metadata - Indicators"], "count": 3 |
| XLS02 | specific | STR | 100.00% | {"first_row_all_string": true} |
| XLS04 | specific | STR | 94.29% | {"mixed_columns": ["Data Source", "World Development Indicators", "Unnamed: 2",  |
| G01 | general | CMP | 30.00% | {"null_count": 196} |
| G04 | general | CMP | 100.00% | {"row_count": 4} |
| XLS03 | specific | CMP | 30.00% | {"blank_cells": 196, "blank_rate": 0.7} |
| G03 | general | CST | 100.00% | {"duplicate_rows": 0} |
| G09 | general | CST | 100.00% | {"note": "no date pairs found"} |
| G07 | general | ACC | 100.00% | {"note": "no timestamp columns detected"} |
| G08 | general | ACC | 100.00% |  |
| XLS05 | specific | ACC | 100.00% | {"note": "no date columns"} |
| G14 | general | SEC | 100.00% | {"sha256": "6f0e43eef04f8ae997e26853ce2da1d00a768fc337282882e969fc95a853dd21", " |
| G15 | general | SEC | 100.00% | {"size_bytes": 16384, "size_mb": 0.02} |

</details>

---

## noaa_ghcn
- **Data type:** fixed_width
- **Standard:** Domain Spec (NOAA GHCN) + ISO/IEC 25012
- **FINAL SCORE: 100.0/100**

| Criteria | Weight | Score | Weighted |
|---|---|---|---|
| Syntax Validity | 30% | 100.0/100 | 30.0 |
| Structural Conformance | 25% | 100.0/100 | 25.0 |
| Completeness | 20% | 100.0/100 | 20.0 |
| Consistency | 10% | 100.0/100 | 10.0 |
| Accuracy / Range | 10% | 100.0/100 | 10.0 |
| Security / Integrity | 5% | 100.0/100 | 5.0 |

<details><summary>Rule Details</summary>

| Rule | Tag | Criteria | Pass Rate | Details |
|---|---|---|---|---|
| G05 | general | SYN | 100.00% | {"encoding": "utf-8"} |
| FW01 | specific | SYN | 100.00% | {"mode_length": 269, "distribution": {"269": 200}} |
| G10 | general | STR | 100.00% | {"delimiter": "'\\t'", "mode_field_count": 1, "distribution": {"1": 200}} |
| FW02 | specific | STR | 100.00% | {"note": "offset spec required for full check"} |
| G01 | general | CMP | 100.00% | {"null_count": 0} |
| G04 | general | CMP | 100.00% | {"row_count": 200} |
| FW03 | specific | CMP | 100.00% | {"sentinel_count": 2834, "sentinel_value": "-9999"} |
| G03 | general | CST | 100.00% | {"duplicate_rows": 0} |
| G08 | general | ACC | 100.00% | {"note": "no numeric columns"} |
| FW04 | specific | ACC | 100.00% | {"elements": {"TMAX": 52, "TMIN": 52, "TAVG": 52, "PRCP": 44}} |
| G14 | general | SEC | 100.00% | {"sha256": "7bcf2995fec6247531aa7ab2cd37e8607a62fb8afcc04ec39d9516fca18141ac", " |
| G15 | general | SEC | 100.00% | {"size_bytes": 54000, "size_mb": 0.05} |

</details>

---

## loghub_apache
- **Data type:** txt_log
- **Standard:** Syslog RFC 5424 + ISO/IEC 25012
- **FINAL SCORE: 93.7/100**

| Criteria | Weight | Score | Weighted |
|---|---|---|---|
| Syntax Validity | 30% | 100.0/100 | 30.0 |
| Structural Conformance | 20% | 68.5/100 | 13.7 |
| Completeness | 15% | 100.0/100 | 15.0 |
| Consistency | 15% | 100.0/100 | 15.0 |
| Accuracy / Range | 15% | 100.0/100 | 15.0 |
| Security / Integrity | 5% | 100.0/100 | 5.0 |

<details><summary>Rule Details</summary>

| Rule | Tag | Criteria | Pass Rate | Details |
|---|---|---|---|---|
| G05 | general | SYN | 100.00% | {"encoding": "utf-8"} |
| LOG01 | specific | SYN | 100.00% |  |
| LOG03 | specific | SYN | 100.00% |  |
| LOG02 | specific | STR | 100.00% | {"levels": {"notice": 30, "error": 70}} |
| LOG04 | specific | STR | 37.00% | {"mode_fields": 13} |
| G01 | general | CMP | 100.00% | ERROR: No DataFrame available |
| G04 | general | CMP | 100.00% | ERROR: No DataFrame available |
| G03 | general | CST | 100.00% | ERROR: No DataFrame available |
| G07 | general | ACC | 100.00% | ERROR: No DataFrame available |
| G08 | general | ACC | 100.00% | ERROR: No DataFrame available |
| G14 | general | SEC | 100.00% | {"sha256": "7a879a01dcf8421f61ecd0e149f708990322f4f75d4c4d365f2420a72839a27d", " |
| G15 | general | SEC | 100.00% | {"size_bytes": 9718, "size_mb": 0.01} |

</details>

---

## wikimedia_pageviews
- **Data type:** txt_log
- **Standard:** Syslog RFC 5424 + ISO/IEC 25012
- **FINAL SCORE: 80.0/100**

| Criteria | Weight | Score | Weighted |
|---|---|---|---|
| Syntax Validity | 30% | 33.33/100 | 10.0 |
| Structural Conformance | 20% | 100.0/100 | 20.0 |
| Completeness | 15% | 100.0/100 | 15.0 |
| Consistency | 15% | 100.0/100 | 15.0 |
| Accuracy / Range | 15% | 100.0/100 | 15.0 |
| Security / Integrity | 5% | 100.0/100 | 5.0 |

<details><summary>Rule Details</summary>

| Rule | Tag | Criteria | Pass Rate | Details |
|---|---|---|---|---|
| G05 | general | SYN | 100.00% | {"encoding": "utf-8"} |
| LOG01 | specific | SYN | 0.00% |  |
| LOG03 | specific | SYN | 0.00% |  |
| LOG02 | specific | STR | 100.00% | {"levels": {}} |
| LOG04 | specific | STR | 100.00% | {"mode_fields": 4} |
| G01 | general | CMP | 100.00% | ERROR: No DataFrame available |
| G04 | general | CMP | 100.00% | ERROR: No DataFrame available |
| G03 | general | CST | 100.00% | ERROR: No DataFrame available |
| G07 | general | ACC | 100.00% | ERROR: No DataFrame available |
| G08 | general | ACC | 100.00% | ERROR: No DataFrame available |
| G14 | general | SEC | 100.00% | {"sha256": "8d47e37ef1407b29c7d65d37e5cbe67ae6ce5903f17842965e05fc37956768e4", " |
| G15 | general | SEC | 100.00% | {"size_bytes": 25655, "size_mb": 0.02} |

</details>

---
