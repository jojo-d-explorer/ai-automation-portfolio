#!/usr/bin/env python3
"""Weekly URL health check for all master job databases.

Pings every job URL and marks jobs as Closed when the posting is gone.
Removes confirmed-closed jobs from the database (they're not worth applying to).

Usage:
  python3 JC3/check_urls.py           # check all users
  python3 JC3/check_urls.py joey      # check one user
  python3 JC3/check_urls.py --dry-run # report only, don't modify CSVs

Rules:
  CLOSED  — 404, or redirect to a board root / ?error=true
  BLOCKED — 403 / bot-wall (skip, leave as-is)
  OPEN    — 200 with no closed-redirect
  ERROR   — timeout or connection failure (skip, leave as-is)
"""

import csv
import glob
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DELAY = 0.4   # seconds between requests (be polite)
TIMEOUT = 8   # seconds per request


# ---------------------------------------------------------------------------
# Database discovery (mirrors dashboard.py)
# ---------------------------------------------------------------------------

def find_databases():
    users = {}
    joey_path = os.path.join(_REPO, "results", "master_job_database.csv")
    if os.path.exists(joey_path):
        users["joey"] = ("Joey Clark", joey_path)
    for_others = os.path.join(_REPO, "results", "For_Others")
    if os.path.isdir(for_others):
        for name in sorted(os.listdir(for_others)):
            folder = os.path.join(for_others, name)
            if not os.path.isdir(folder):
                continue
            candidate = os.path.join(folder, f"Master_Job_Database_{name}.csv")
            if os.path.exists(candidate):
                slug = name.lower().replace("_", " ").split()[0]
                if slug in users:
                    slug = name.lower().replace("_", "-")
                users[slug] = (name.replace("_", " "), candidate)
    return users


# ---------------------------------------------------------------------------
# URL status detection
# ---------------------------------------------------------------------------

def _is_board_root(original_url, final_url):
    """True if the redirect destination is just the company's board root."""
    orig = original_url.rstrip("/")
    final = final_url.rstrip("/")
    if orig == final:
        return False
    # Lever: jobs.lever.co/{company}/{uuid} → jobs.lever.co/{company}
    if "lever.co" in final:
        parts = final.split("lever.co/")[-1].split("/")
        if len(parts) == 1 and parts[0]:   # only company slug, no UUID
            return True
    # Greenhouse: redirect to board or ?error=true
    if "greenhouse.io" in final:
        if "error=true" in final:
            return True
        if "/jobs/" not in final and "job_app" not in final:
            return True
    # Ashby: jobs.ashbyhq.com/{company} with no UUID
    if "ashbyhq.com" in final:
        parts = final.split("ashbyhq.com/")[-1].split("/")
        if len(parts) == 1 and parts[0]:
            return True
    return False


def check_url(url):
    """
    Returns one of: 'open', 'closed', 'blocked', 'error'
    """
    if not url or not url.startswith("http"):
        return "error"
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; job-checker/1.0)"},
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            status = resp.status
            final_url = resp.url
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "closed"
        if e.code in (403, 429):
            return "blocked"
        return "error"
    except Exception:
        return "error"

    if status == 404:
        return "closed"
    if status in (403, 429):
        return "blocked"
    if _is_board_root(url, final_url):
        return "closed"
    return "open"


# ---------------------------------------------------------------------------
# Main check loop
# ---------------------------------------------------------------------------

def check_database(display_name, db_path, dry_run=False):
    with open(db_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys())

    # Add URL_Status column if missing
    if "URL_Status" not in fieldnames:
        fieldnames.append("URL_Status")
        for r in rows:
            r["URL_Status"] = ""

    # Only check jobs not already applied to and not already marked Closed
    to_check = [
        r for r in rows
        if not r.get("Applied_Date", "").strip()
        and r.get("URL_Status", "").strip().lower() != "closed"
        and r.get("URL", "").strip().startswith("http")
    ]

    print(f"\n{'─'*60}")
    print(f"  {display_name}  ({len(to_check)} URLs to check, {len(rows)} total jobs)")
    print(f"{'─'*60}")

    results = defaultdict(list)

    for i, row in enumerate(to_check, 1):
        url = row["URL"].strip()
        company = row.get("Company", "")
        title = row.get("Job_Title", "")
        status = check_url(url)
        row["URL_Status"] = status.capitalize()
        results[status].append((company, title, url))
        symbol = {"open": "✓", "closed": "✗", "blocked": "~", "error": "?"}[status]
        print(f"  [{i:>3}/{len(to_check)}] {symbol} {status:<8}  {company[:30]} — {title[:35]}")
        time.sleep(DELAY)

    # Report
    closed = results["closed"]
    print(f"\n  Summary: {len(results['open'])} open · {len(closed)} closed · "
          f"{len(results['blocked'])} blocked · {len(results['error'])} error")

    if closed:
        print(f"\n  Closed jobs to remove ({len(closed)}):")
        for company, title, url in closed:
            print(f"    ✗  {company} — {title}")

    if dry_run:
        print("\n  [dry-run] No changes written.")
        return len(closed)

    # Remove closed jobs
    if closed:
        closed_urls = {url for _, _, url in closed}
        rows = [r for r in rows if r.get("URL", "").strip() not in closed_urls]
        print(f"\n  Removed {len(closed)} closed jobs. {len(rows)} jobs remain.")

    with open(db_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return len(closed)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    dry_run = "--dry-run" in sys.argv

    users = find_databases()

    if args:
        slug = args[0].lower()
        match = [k for k in users if k.startswith(slug)]
        if not match:
            print(f"User '{slug}' not found. Available: {', '.join(users)}")
            sys.exit(1)
        targets = {match[0]: users[match[0]]}
    else:
        targets = users

    if dry_run:
        print("  [dry-run mode — no files will be modified]")

    total_removed = 0
    for slug, (display_name, db_path) in targets.items():
        removed = check_database(display_name, db_path, dry_run=dry_run)
        total_removed += removed

    print(f"\n{'='*60}")
    print(f"  Done. Total closed jobs removed: {total_removed}")
    if dry_run:
        print("  (dry-run — nothing written)")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
