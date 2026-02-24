#!/usr/bin/env python3
"""Job search dashboard — run for any user in the repo.

Usage:
  python3 dashboard.py            # list available users
  python3 dashboard.py joey       # run dashboard for Joey
  python3 dashboard.py aaron      # run dashboard for Aaron Kimson
"""

import csv
import os
import sys
from collections import Counter

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# User discovery
# ---------------------------------------------------------------------------

def find_databases():
    """Return a dict of {slug: (display_name, csv_path)} for every user found."""
    users = {}

    # Joey — fixed location
    joey_path = os.path.join(_REPO, "results", "master_job_database.csv")
    if os.path.exists(joey_path):
        users["joey"] = ("Joey Clark", joey_path)

    # Friends — results/For_Others/{Name}/Master_Job_Database_{Name}.csv
    for_others = os.path.join(_REPO, "results", "For_Others")
    if os.path.isdir(for_others):
        for name in sorted(os.listdir(for_others)):
            folder = os.path.join(for_others, name)
            if not os.path.isdir(folder):
                continue
            candidate = os.path.join(folder, f"Master_Job_Database_{name}.csv")
            if os.path.exists(candidate):
                slug = name.lower().replace("_", " ").split()[0]  # first name only
                # Ensure uniqueness — use full name slug if collision
                if slug in users:
                    slug = name.lower().replace("_", "-")
                display = name.replace("_", " ")
                users[slug] = (display, candidate)

    return users


def resolve_user(arg, users):
    """Match a CLI argument to a user slug (case-insensitive prefix match)."""
    arg = arg.lower()
    # Exact match first
    if arg in users:
        return arg
    # Prefix match
    matches = [slug for slug in users if slug.startswith(arg)]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        print(f"Ambiguous user '{arg}' — matches: {', '.join(matches)}")
        sys.exit(1)
    return None


# ---------------------------------------------------------------------------
# Data helpers
# ---------------------------------------------------------------------------

def load_jobs(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_score(row):
    try:
        return float(row["Score"])
    except (ValueError, KeyError):
        return None


SECTOR_MAP = {
    "Fintech": ["fintech", "crypto", "blockchain", "banking", "payments", "tax tech",
                "alternative investments", "market intelligence", "identity", "fraud",
                "insurtech", "web3"],
    "Health Tech": ["health", "wellness", "fitness", "biotech"],
    "AI / ML": ["ai/", "ai ", "/ai", " ai", "speech tech", "ml"],
    "SaaS / Software": ["saas", "developer tools", "devtools", "cloud", "automation",
                        "martech", "adtech", "analytics"],
    "E-commerce / Consumer": ["e-commerce", "commerce", "consumer tech", "marketplace",
                               "restaurant tech", "social media", "media/sports"],
}


def normalize_sector(raw):
    if not raw:
        return "Other"
    low = raw.lower()
    for parent, keywords in SECTOR_MAP.items():
        if any(kw in low for kw in keywords):
            return parent
    return raw


# ---------------------------------------------------------------------------
# Dashboard rendering
# ---------------------------------------------------------------------------

def run_dashboard(display_name, db_path):
    jobs = load_jobs(db_path)
    scored = [(j, parse_score(j)) for j in jobs if parse_score(j) is not None]

    # --- Overview ---
    print("=" * 60)
    print(f"  JOB SEARCH DASHBOARD — {display_name.upper()}")
    print("=" * 60)
    print(f"\n  Total jobs in database : {len(jobs)}")
    print(f"  Jobs with scores       : {len(scored)}")

    if scored:
        avg = sum(s for _, s in scored) / len(scored)
        top = max(s for _, s in scored)
        low = min(s for _, s in scored)
        print(f"  Average score          : {avg:.1f}")
        print(f"  Score range            : {low:.0f} – {top:.0f}")

    # --- Top 10 ---
    print(f"\n{'─' * 60}")
    print("  TOP 10 JOBS BY SCORE")
    print(f"{'─' * 60}")
    print(f"  {'Score':<7} {'Company':<25} {'Title'}")
    print(f"  {'─'*5:<7} {'─'*23:<25} {'─'*25}")

    for job, score in sorted(scored, key=lambda x: x[1], reverse=True)[:10]:
        company = job["Company"][:23]
        title = job["Job_Title"][:40]
        print(f"  {score:<7.0f} {company:<25} {title}")

    # --- Sector breakdown ---
    print(f"\n{'─' * 60}")
    print("  BREAKDOWN BY SECTOR")
    print(f"{'─' * 60}")

    sector_scores: dict[str, list[float]] = {}
    for job, score in scored:
        sector = normalize_sector(job.get("Sector", ""))
        sector_scores.setdefault(sector, []).append(score)

    sector_rows = sorted(
        [(s, len(v), sum(v) / len(v)) for s, v in sector_scores.items()],
        key=lambda r: r[1], reverse=True
    )

    print(f"  {'Sector':<30} {'Jobs':>5}  {'Avg Score':>9}")
    print(f"  {'─'*28:<30} {'─'*5:>5}  {'─'*9:>9}")
    for sector, count, avg in sector_rows:
        print(f"  {sector:<30} {count:>5}  {avg:>9.1f}")

    # --- Apply Next ---
    apply_next = sorted(
        [(j, s) for j, s in scored if s >= 85 and not j.get("Applied_Date", "").strip()],
        key=lambda x: x[1], reverse=True
    )

    print(f"\n{'─' * 60}")
    print(f"  APPLY NEXT  ({len(apply_next)} jobs scoring 85+ with no application)")
    print(f"{'─' * 60}")

    if apply_next:
        print(f"  {'Score':<7} {'Company':<20} {'Title':<28} URL")
        print(f"  {'─'*5:<7} {'─'*18:<20} {'─'*26:<28} {'─'*30}")
        for job, score in apply_next:
            company = job["Company"][:18]
            title = job["Job_Title"][:26]
            url = job.get("URL", "")
            print(f"  {score:<7.0f} {company:<20} {title:<28} {url}")
    else:
        print("  All 85+ jobs have been applied to!")

    # --- Status breakdown ---
    print(f"\n{'─' * 60}")
    print("  NEW vs REPEAT")
    print(f"{'─' * 60}")
    status_counts = Counter(j.get("Status", "Unknown") for j in jobs)
    for status, count in status_counts.most_common():
        print(f"  {status:<12} {count}")

    print()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    users = find_databases()

    if len(sys.argv) < 2:
        print("\nAvailable users:\n")
        for slug, (display, path) in users.items():
            print(f"  {slug:<20} {display}  ({os.path.relpath(path, _REPO)})")
        print(f"\nUsage: python3 dashboard.py <user>\n")
        sys.exit(0)

    slug = resolve_user(sys.argv[1], users)
    if slug is None:
        print(f"User '{sys.argv[1]}' not found. Available: {', '.join(users)}")
        sys.exit(1)

    display_name, db_path = users[slug]
    run_dashboard(display_name, db_path)


if __name__ == "__main__":
    main()
