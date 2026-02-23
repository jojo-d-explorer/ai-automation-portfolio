#!/usr/bin/env python3
"""Quick dashboard summary of the JC3 master job database."""

import csv
import os
from collections import Counter

DB_PATH = os.path.join(os.path.dirname(__file__), "master_job_database.csv")


def load_jobs(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


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


def parse_score(row):
    try:
        return float(row["Score"])
    except (ValueError, KeyError):
        return None


def main():
    jobs = load_jobs(DB_PATH)
    scored = [(j, parse_score(j)) for j in jobs if parse_score(j) is not None]

    # --- Overview ---
    print("=" * 60)
    print("  JC3 JOB SEARCH DASHBOARD")
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

    rows = []
    for sector, scores in sector_scores.items():
        rows.append((sector, len(scores), sum(scores) / len(scores)))

    rows.sort(key=lambda r: r[1], reverse=True)

    print(f"  {'Sector':<30} {'Jobs':>5}  {'Avg Score':>9}")
    print(f"  {'─'*28:<30} {'─'*5:>5}  {'─'*9:>9}")
    for sector, count, avg in rows:
        print(f"  {sector:<30} {count:>5}  {avg:>9.1f}")

    # --- Status breakdown ---
    print(f"\n{'─' * 60}")
    print("  NEW vs REPEAT")
    print(f"{'─' * 60}")
    status_counts = Counter(j.get("Status", "Unknown") for j in jobs)
    for status, count in status_counts.most_common():
        print(f"  {status:<12} {count}")

    print()


if __name__ == "__main__":
    main()
