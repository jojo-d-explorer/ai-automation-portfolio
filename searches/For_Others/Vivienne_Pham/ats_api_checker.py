#!/usr/bin/env python3
"""
ATS API Checker for Vivienne Pham — v1.0
Hits Greenhouse, Lever, and Ashby APIs for a curated company list.
Returns LIVE, verified-open jobs matching Vivienne's target role titles.

Reads company list from companies.json (grows each week via funding intel).
Skips companies with ats="unknown" or ats="workday" (no public API).

Three role archetypes:
  - Operator (Finance): VP Finance, CFO, Head/Director of Finance
  - Capital Markets (IR): IR Director, Investor Relations, Head of IR
  - Ecosystem (BD): Director of Business Development, Portfolio Operations, Director of Growth

Usage:
    python3 ats_api_checker.py

Output:
    results/For_Others/Vivienne_Pham/Week_of_{DATE}/api_verified_{DATE}.csv

Requires: requests (pip install requests)
"""

import requests
import csv
import re
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# ============================================================
# CONFIG
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.expanduser("~/GitHub/ai-automation-portfolio")
TODAY = datetime.now()
MONDAY = TODAY - timedelta(days=TODAY.weekday())
WEEK_DATE = MONDAY.strftime("%Y-%m-%d")
RESULTS_DIR = os.path.join(BASE_PATH, f"results/For_Others/Vivienne_Pham/Week_of_{WEEK_DATE}")
OUTPUT_CSV = os.path.join(RESULTS_DIR, f"api_verified_{WEEK_DATE}.csv")
COMPANIES_JSON = os.path.join(SCRIPT_DIR, "companies.json")

os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# ROLE KEYWORDS — 3 archetypes
# ============================================================

# Archetype 1: Operator (Finance)
OPERATOR_KEYWORDS = [
    "vp finance", "vp of finance", "vice president finance",
    "vice president of finance",
    "cfo", "chief financial officer",
    "head of finance", "director of finance", "finance director",
    "head of fp&a", "director of fp&a", "fp&a director",
    "head of financial planning", "director of financial planning",
    "controller", "vp controller",
    "head of accounting", "director of accounting",
    "treasurer", "head of treasury",
]

# Archetype 2: Capital Markets / Investor Relations
CAPITAL_MARKETS_KEYWORDS = [
    "ir director", "director of investor relations",
    "investor relations", "head of ir",
    "head of investor relations", "vp investor relations",
    "vp of investor relations",
    "capital markets", "head of capital markets",
    "director of capital markets",
    "head of fundraising", "director of fundraising",
]

# Archetype 3: Ecosystem (BD / Growth / Portfolio Ops)
ECOSYSTEM_KEYWORDS = [
    "director of business development", "head of business development",
    "business development director",
    "portfolio operations", "head of portfolio operations",
    "director of portfolio operations", "portfolio ops",
    "director of growth", "head of growth", "vp growth",
    "vp of growth", "growth director",
    "director of strategic finance", "head of strategic finance",
    "chief of staff",
]

ALL_KEYWORDS = OPERATOR_KEYWORDS + CAPITAL_MARKETS_KEYWORDS + ECOSYSTEM_KEYWORDS

# Location keywords to match
LOCATION_KEYWORDS = [
    "new york", "nyc", "ny", "manhattan", "brooklyn",
    "washington", "dc", "d.c.",
    "remote", "united states", "us", "usa",
]

# ============================================================
# TARGET COMPANIES — loaded from companies.json
# ============================================================

def load_companies(json_path):
    """Load all companies from companies.json, flatten all tiers."""
    with open(json_path, 'r') as f:
        data = json.load(f)
    companies = []
    seen = set()
    for key, entries in data.items():
        if key.startswith("_"):
            continue
        if not isinstance(entries, list):
            continue
        for entry in entries:
            slug = entry.get("slug")
            ats = entry.get("ats")
            if slug and ats and slug not in seen:
                companies.append((slug, ats))
                seen.add(slug)
    return companies

COMPANIES = load_companies(COMPANIES_JSON)
print(f"Loaded {len(COMPANIES)} companies from {COMPANIES_JSON}")

# ============================================================
# API FETCHERS
# ============================================================

def fetch_greenhouse(slug):
    """Fetch all jobs from a Greenhouse board."""
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json().get("jobs", [])
        else:
            print(f"  [{slug}] Greenhouse HTTP {r.status_code}")
            return []
    except Exception as e:
        print(f"  [{slug}] Greenhouse error: {e}")
        return []

def fetch_lever(slug):
    """Fetch all jobs from a Lever board."""
    url = f"https://api.lever.co/v0/postings/{slug}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
        else:
            print(f"  [{slug}] Lever HTTP {r.status_code}")
            return []
    except Exception as e:
        print(f"  [{slug}] Lever error: {e}")
        return []

def fetch_ashby(slug):
    """Fetch all jobs from an Ashby board via their API."""
    url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            return data.get("jobs", [])
        else:
            print(f"  [{slug}] Ashby HTTP {r.status_code}")
            return []
    except Exception as e:
        print(f"  [{slug}] Ashby error: {e}")
        return []

# ============================================================
# NORMALIZERS
# ============================================================

def normalize_greenhouse(job, slug):
    title = job.get("title", "")
    location = job.get("location", {}).get("name", "N/A")
    url = job.get("absolute_url", "")
    updated = job.get("updated_at", "")
    return {"company_slug": slug, "title": title, "location": location,
            "url": url, "updated": updated, "ats": "Greenhouse"}

def normalize_lever(job, slug):
    title = job.get("text", "")
    location = job.get("categories", {}).get("location", "N/A")
    url = job.get("hostedUrl", "")
    updated = ""
    ts = job.get("createdAt")
    if ts:
        updated = datetime.fromtimestamp(ts / 1000).isoformat()
    return {"company_slug": slug, "title": title, "location": location,
            "url": url, "updated": updated, "ats": "Lever"}

def normalize_ashby(job, slug):
    title = job.get("title", "")
    location = job.get("location", "N/A")
    # Ashby job URL format
    job_id = job.get("id", "")
    url = f"https://jobs.ashbyhq.com/{slug}/{job_id}" if job_id else ""
    updated = job.get("publishedAt", "")
    return {"company_slug": slug, "title": title, "location": location,
            "url": url, "updated": updated, "ats": "Ashby"}

# ============================================================
# FILTERS
# ============================================================

def matches_role(title):
    """Check if job title matches any target role keyword."""
    t = title.lower()
    for kw in ALL_KEYWORDS:
        if kw in t:
            return True
    return False

def get_archetype(title):
    """Return which archetype(s) a title matches."""
    t = title.lower()
    archetypes = []
    for kw in OPERATOR_KEYWORDS:
        if kw in t:
            archetypes.append("Operator")
            break
    for kw in CAPITAL_MARKETS_KEYWORDS:
        if kw in t:
            archetypes.append("Capital Markets")
            break
    for kw in ECOSYSTEM_KEYWORDS:
        if kw in t:
            archetypes.append("Ecosystem")
            break
    return " + ".join(archetypes) if archetypes else "Unknown"

def matches_location(location):
    """Check if location matches any target location."""
    loc = location.lower()
    for kw in LOCATION_KEYWORDS:
        if kw in loc:
            return True
    return False

# ============================================================
# MAIN
# ============================================================

def main():
    api_companies = [(s, a) for s, a in COMPANIES if a in ("greenhouse", "lever", "ashby")]
    skipped = len(COMPANIES) - len(api_companies)

    print(f"ATS API Checker v1.0 — Vivienne Pham")
    print(f"Week of {WEEK_DATE}")
    print(f"Total in corpus: {len(COMPANIES)} | API-queryable: {len(api_companies)} | Skipped (unknown/workday): {skipped}")
    print(f"Role archetypes: Operator (Finance) | Capital Markets (IR) | Ecosystem (BD)")
    print(f"Locations: NYC, DC, Remote-US")
    print(f"{'='*60}")

    all_matches = []
    stats = {"greenhouse": 0, "lever": 0, "ashby": 0,
             "total_jobs_scanned": 0, "companies_checked": 0, "companies_with_matches": 0,
             "archetype_operator": 0, "archetype_capital_markets": 0, "archetype_ecosystem": 0}

    for slug, ats in COMPANIES:
        stats["companies_checked"] += 1

        if ats == "greenhouse":
            raw_jobs = fetch_greenhouse(slug)
            normalizer = normalize_greenhouse
        elif ats == "lever":
            raw_jobs = fetch_lever(slug)
            normalizer = normalize_lever
        elif ats == "ashby":
            raw_jobs = fetch_ashby(slug)
            normalizer = normalize_ashby
        else:
            continue

        stats["total_jobs_scanned"] += len(raw_jobs)
        company_matches = []

        for job in raw_jobs:
            normalized = normalizer(job, slug)
            if matches_role(normalized["title"]):
                # Location filter is soft — include if location matches OR location is ambiguous
                loc = normalized["location"]
                if matches_location(loc) or loc in ("N/A", "", "Flexible", "Multiple"):
                    archetype = get_archetype(normalized["title"])
                    normalized["archetype"] = archetype
                    company_matches.append(normalized)
                    # Track archetype stats
                    if "Operator" in archetype:
                        stats["archetype_operator"] += 1
                    if "Capital Markets" in archetype:
                        stats["archetype_capital_markets"] += 1
                    if "Ecosystem" in archetype:
                        stats["archetype_ecosystem"] += 1

        if company_matches:
            stats["companies_with_matches"] += 1
            stats[ats] += len(company_matches)
            all_matches.extend(company_matches)
            print(f"  ✓ {slug} ({ats}): {len(company_matches)} matching roles")
        else:
            print(f"    {slug} ({ats}): {len(raw_jobs)} jobs, 0 matches")

    # ============ OUTPUT ============
    print(f"\n{'='*60}")
    print(f"RESULTS")
    print(f"{'='*60}")
    print(f"Companies checked:      {stats['companies_checked']}")
    print(f"Total jobs scanned:     {stats['total_jobs_scanned']}")
    print(f"Companies with matches: {stats['companies_with_matches']}")
    print(f"Total matching roles:   {len(all_matches)}")
    print(f"  Greenhouse: {stats['greenhouse']}")
    print(f"  Lever:      {stats['lever']}")
    print(f"  Ashby:      {stats['ashby']}")
    print(f"\nBy archetype:")
    print(f"  Operator (Finance):     {stats['archetype_operator']}")
    print(f"  Capital Markets (IR):   {stats['archetype_capital_markets']}")
    print(f"  Ecosystem (BD/Growth):  {stats['archetype_ecosystem']}")

    if all_matches:
        fieldnames = ["company_slug", "title", "location", "url", "updated", "ats", "archetype"]
        with open(OUTPUT_CSV, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for m in all_matches:
                writer.writerow(m)
        print(f"\nOutput: {OUTPUT_CSV}")
        print(f"\nMatching roles:")
        for m in all_matches:
            print(f"  [{m['ats']}] [{m['archetype']}] {m['company_slug']} — {m['title']} ({m['location']})")
            print(f"    {m['url']}")
    else:
        print("\nNo matching roles found. Check company slugs and try expanding keywords.")

if __name__ == "__main__":
    main()
