#!/usr/bin/env python3
"""
diff.py — v4 Phase 1 item 5 (Strategy Addendum §2), week-over-week diff
upgraded to daily-new detection.

No existing script to refactor from — new build. Compares this run's
candidates_{date}.csv (discover.py's raw output, before health/fetch
filtering — this is meant to be fast and free, "costs 2-3 minutes and no
model tokens" per the addendum) against the most recent prior snapshot.
Rows whose URL wasn't seen in the prior snapshot are "new since last run"
and get written to new_since_last_run.csv plus a human-readable
FRESH_{date}.md alert. This run's candidates then become the new snapshot
for next time.

Sits between discover.py and health.py in the daily fast-path:
    python3 JC3/discover.py && python3 JC3/diff.py && python3 JC3/health.py

The full weekly run (fetch_jds.py, package.py, Master update) stays
separate and weekly — diff.py is purely an early-warning layer on top of
the same corpus, not a replacement for it.

Usage:
    python3 JC3/diff.py
"""

import csv
import os
import shutil
from datetime import datetime, timedelta

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.dirname(SCRIPT_DIR)
SNAPSHOTS_DIR = os.path.join(BASE_PATH, "snapshots")
os.makedirs(SNAPSHOTS_DIR, exist_ok=True)


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


def _most_recent_snapshot(exclude_date):
    """Find the latest snapshot strictly before today's — snapshot files
    are named api_results_{date}.csv, sorted lexically = chronologically
    since the date format is YYYY-MM-DD."""
    candidates = sorted(
        f for f in os.listdir(SNAPSHOTS_DIR)
        if f.startswith("api_results_") and f.endswith(".csv") and f != f"api_results_{exclude_date}.csv"
    )
    return os.path.join(SNAPSHOTS_DIR, candidates[-1]) if candidates else None


def run_diff(candidates_csv=None):
    week_date, week_dir = _week_paths()
    candidates_csv = candidates_csv or os.path.join(week_dir, f"candidates_{week_date}.csv")

    if not os.path.exists(candidates_csv):
        print(f"No candidates CSV found at {candidates_csv}. Run discover.py first.")
        return None

    current_rows = _load_csv(candidates_csv)
    prior_snapshot_path = _most_recent_snapshot(exclude_date=week_date)
    prior_urls = {r.get("url") for r in _load_csv(prior_snapshot_path)} if prior_snapshot_path else set()

    new_rows = [r for r in current_rows if r.get("url") and r.get("url") not in prior_urls]

    print(f"\n{'─'*70}")
    print(f"  diff.py — {week_date}")
    print(f"  Prior snapshot: {prior_snapshot_path or '(none — first run)'}")
    print(f"  Current candidates: {len(current_rows)} | New since last run: {len(new_rows)}")
    print(f"{'─'*70}")

    new_csv_path = os.path.join(week_dir, "new_since_last_run.csv")
    if new_rows:
        fieldnames = list(new_rows[0].keys())
        with open(new_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(new_rows)
        print(f"  New candidates: {new_csv_path}")

        fresh_md_path = os.path.join(week_dir, f"FRESH_{datetime.now().strftime('%Y-%m-%d')}.md")
        with open(fresh_md_path, "w") as f:
            f.write(f"# Fresh postings — {datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write(f"{len(new_rows)} new posting(s) since the last discover.py run.\n\n")
            for r in new_rows:
                f.write(f"- **{r.get('company_name','')}** — {r.get('title','')} "
                        f"({r.get('location','')})\n  {r.get('url','')}\n")
        print(f"  Alert file: {fresh_md_path}")
    else:
        print("  Nothing new — no alert file written.")

    # This run's candidates become the new snapshot for next time.
    snapshot_path = os.path.join(SNAPSHOTS_DIR, f"api_results_{week_date}.csv")
    shutil.copy(candidates_csv, snapshot_path)
    print(f"  Snapshot saved: {snapshot_path}")

    return new_csv_path if new_rows else None


if __name__ == "__main__":
    run_diff()
