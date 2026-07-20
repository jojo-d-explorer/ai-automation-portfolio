#!/usr/bin/env python3
"""
package.py — v4 Phase 1, dedup + NEW/REPEAT + CSV/XLSX packaging.

No existing dedup/XLSX code was found anywhere in the repo (checked
thoroughly — grep for openpyxl across every .py file). v3.x's XLSX
building most likely only ever happened live inside prompt-driven agent
sessions, never as a persisted script. Built fresh per
HANDOFF_ROADMAP_v4_Claude_Code.md §4 item 4.

Roadmap spec says dedup should "keep highest score" — that assumes Phase 2
(score.py) has already run. It hasn't yet; this phase's acceptance
criterion is explicitly "before any scoring exists" (roadmap §4). Dedup
here keeps first-occurrence instead and merges provenance across
duplicates. Once Phase 2 lands, dedup_key's tie-break should switch to
score — flagged inline below, not silently done differently than spec'd.

The old 3-tab XLSX shape (Verified Jobs / Non-Queryable Companies /
LinkedIn Search Links) doesn't map cleanly onto v4's architecture —
LinkedIn is handled separately by linkedin_links.py per the Strategy
Addendum, not through this pipeline. Built a 3-tab shape that reflects
what v4 actually produces at this phase instead: Verified Jobs / Dropped
(diagnostics) / Run Metrics.

Usage:
    python3 JC3/package.py
"""

import csv
import os
import sys
from datetime import datetime, timedelta

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.dirname(SCRIPT_DIR)
MASTER_CSV = os.path.join(BASE_PATH, "results", "joey", "Master_LATAM_Joey.csv")

HEADER_FILL = PatternFill(start_color="1F2A44", end_color="1F2A44", fill_type="solid")
HEADER_FONT = Font(bold=True, color="FFFFFF")
NEW_FILL = PatternFill(start_color="E3F2E1", end_color="E3F2E1", fill_type="solid")


def _week_paths():
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    week_date = monday.strftime("%Y-%m-%d")
    week_dir = os.path.join(BASE_PATH, "results", "joey", "LATAM", f"Week_of_{week_date}")
    return week_date, week_dir


def _load_csv(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _dedup_key(row):
    return (row.get("company_name", "").strip().lower(), row.get("title", "").strip().lower())


def dedup(rows):
    """Keep first occurrence per (company, title); merge source/ats across
    duplicates into a single comma-joined `found_via` field. TODO Phase 2:
    once score.py exists, prefer the highest-scored duplicate instead of
    first-occurrence — roadmap's literal spec ("keep highest score")."""
    seen = {}
    order = []
    for row in rows:
        key = _dedup_key(row)
        if key not in seen:
            seen[key] = dict(row)
            seen[key]["found_via"] = row.get("source", "")
            order.append(key)
        else:
            existing_sources = set(seen[key]["found_via"].split(", ")) if seen[key]["found_via"] else set()
            existing_sources.add(row.get("source", ""))
            seen[key]["found_via"] = ", ".join(sorted(s for s in existing_sources if s))
    return [seen[k] for k in order]


def load_master(path):
    if not os.path.exists(path):
        return {}, []
    rows = _load_csv(path)
    by_url = {r["url"]: r for r in rows if r.get("url")}
    return by_url, rows


def classify_new_repeat(deduped_rows, master_by_url):
    for row in deduped_rows:
        row["status"] = "REPEAT" if row.get("url") in master_by_url else "NEW"
    return deduped_rows


def update_master(deduped_rows, master_path, master_rows, week_date):
    existing_urls = {r.get("url") for r in master_rows}
    new_rows = [r for r in deduped_rows if r.get("url") not in existing_urls]
    if not new_rows:
        return 0

    fieldnames = list(master_rows[0].keys()) if master_rows else list(new_rows[0].keys())
    for r in new_rows:
        for k in fieldnames:
            r.setdefault(k, "")
        r["first_seen_week"] = week_date

    if "first_seen_week" not in fieldnames:
        fieldnames.append("first_seen_week")
        for r in master_rows:
            r.setdefault("first_seen_week", "")

    os.makedirs(os.path.dirname(master_path), exist_ok=True)
    with open(master_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(master_rows + new_rows)

    return len(new_rows)


def _autosize_and_style(ws, rows, highlight_new=False):
    if not rows:
        return
    headers = list(rows[0].keys())
    ws.append(headers)
    for cell in ws[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
    for row in rows:
        ws.append([row.get(h, "") for h in headers])
        if highlight_new and row.get("status") == "NEW":
            for cell in ws[ws.max_row]:
                cell.fill = NEW_FILL
    for i, h in enumerate(headers, 1):
        width = max(12, min(45, max(len(h), *(len(str(r.get(h, ""))) for r in rows)) + 2))
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.freeze_panes = "A2"


def build_xlsx(verified_rows, dropped_rows, metrics, output_path):
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "Verified Jobs"
    _autosize_and_style(ws1, verified_rows, highlight_new=True)

    ws2 = wb.create_sheet("Dropped (diagnostics)")
    _autosize_and_style(ws2, dropped_rows)

    ws3 = wb.create_sheet("Run Metrics")
    ws3.append(["Metric", "Value"])
    for cell in ws3[1]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
    for k, v in metrics.items():
        ws3.append([k, v])
    ws3.column_dimensions["A"].width = 32
    ws3.column_dimensions["B"].width = 20

    wb.save(output_path)


def run_package():
    week_date, week_dir = _week_paths()
    fetched_csv = os.path.join(week_dir, f"fetched_candidates_{week_date}.csv")
    dropped_health_csv = os.path.join(week_dir, f"health_dropped_{week_date}.csv")

    if not os.path.exists(fetched_csv):
        print(f"No fetched candidates found at {fetched_csv}. "
              f"Run discover.py -> health.py -> fetch_jds.py first.")
        sys.exit(1)

    all_fetched = _load_csv(fetched_csv)
    success_rows = [r for r in all_fetched if r.get("jd_fetch_status") == "success"]
    dropped_fetch_rows = [r for r in all_fetched if r.get("jd_fetch_status") != "success"]
    dropped_health_rows = _load_csv(dropped_health_csv)
    dropped_rows = dropped_fetch_rows + dropped_health_rows

    deduped = dedup(success_rows)
    master_by_url, master_rows = load_master(MASTER_CSV)
    classified = classify_new_repeat(deduped, master_by_url)
    classified.sort(key=lambda r: (r.get("company_name", ""), r.get("title", "")))

    new_count = sum(1 for r in classified if r["status"] == "NEW")
    repeat_count = len(classified) - new_count
    added_to_master = update_master(classified, MASTER_CSV, master_rows, week_date)

    metrics = {
        "week_date": week_date,
        "candidates_total": len(all_fetched),
        "jd_fetch_success": len(success_rows),
        "jd_fetch_dropped": len(dropped_fetch_rows),
        "health_dropped": len(dropped_health_rows),
        "deduped_verified_jobs": len(classified),
        "new": new_count,
        "repeat": repeat_count,
        "added_to_master": added_to_master,
        "master_total_rows": len(master_rows) + added_to_master,
    }

    print(f"\n{'─'*70}")
    print(f"  package.py — week of {week_date}")
    for k, v in metrics.items():
        print(f"    {k}: {v}")
    print(f"{'─'*70}")

    csv_out = os.path.join(week_dir, f"Verified_Jobs_LATAM_Joey_{week_date}.csv")
    xlsx_out = os.path.join(week_dir, f"LATAM_Joey_Complete_{week_date}.xlsx")

    if classified:
        fieldnames = list(classified[0].keys())
        with open(csv_out, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(classified)

    build_xlsx(classified, dropped_rows, metrics, xlsx_out)

    print(f"\n  CSV:  {csv_out}")
    print(f"  XLSX: {xlsx_out}")
    print(f"  Master updated: {MASTER_CSV}")

    return csv_out, xlsx_out


if __name__ == "__main__":
    run_package()
