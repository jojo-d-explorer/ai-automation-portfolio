#!/usr/bin/env python3
"""
ATS API Checker for Joey Clark — Remote-Global Variant v1.0
Hits Greenhouse, Lever, and Ashby APIs for a curated company list.
Returns LIVE, verified-open jobs matching Joey's target role titles.

Reads company list from companies.json (grows each week via search results).
Skips companies with ats="unknown", "workday", or "wttj" (no public API).

Usage:
    python3 ats_api_checker.py

Output:
    results/joey/RemoteGlobal/Week_of_{DATE}/api_verified_{DATE}.csv

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
RESULTS_DIR = os.path.join(BASE_PATH, f"results/joey/RemoteGlobal/Week_of_{WEEK_DATE}")
OUTPUT_CSV = os.path.join(RESULTS_DIR, f"api_verified_{WEEK_DATE}.csv")
COMPANIES_JSON = os.path.join(SCRIPT_DIR, "companies.json")

os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# ROLE KEYWORDS — Expanded for ops, programs, strategic projects
# ============================================================

# Core roles (original RemoteGlobal search)
CORE_KEYWORDS = [
    "chief of staff",
    "head of partnerships", "director of partnerships", "partnerships director",
    "vp partnerships", "vp of partnerships",
    "head of business development", "director of business development",
    "business development director", "head of bd",
    "strategic operations", "head of strategic operations",
    "strategic alliances", "head of strategic alliances",
]

# Expanded roles (business operations, programs, strategic projects)
EXPANDED_KEYWORDS = [
    "director of operations", "head of operations",
    "business operations director", "director of business operations",
    "head of business operations",
    "program director", "senior program manager",
    "director of strategic initiatives", "strategic initiatives director",
    "director of strategic projects", "strategic projects director",
    "strategic projects manager",
    "director of strategy", "head of strategy",
    "strategy and operations", "strategy & operations",
    "director of strategy and operations", "director of strategy & operations",
]

# Secondary (catch broader matches)
SECONDARY_KEYWORDS = [
    "head of growth",
    "head of ecosystem", "platform partnerships", "ecosystem partnerships",
    "corporate development",
    "head of gtm", "go-to-market",
    "operating partner",
    "head of commercial", "commercial director",
]

ALL_KEYWORDS = CORE_KEYWORDS + EXPANDED_KEYWORDS + SECONDARY_KEYWORDS

# Seniority filter — reject titles that are too junior
JUNIOR_REJECT = [
    "associate", "coordinator", "specialist", "analyst", "intern",
    "assistant", "junior", "entry",
]

def is_senior_enough(title):
    """Check if title indicates director+ seniority. Be inclusive but filter clear juniors."""
    t = title.lower()
    # Always accept these
    senior_markers = ["chief", "head of", "director", "vp ", "vice president",
                      "senior program manager", "lead", "principal"]
    for marker in senior_markers:
        if marker in t:
            return True
    # Reject clear junior titles
    for reject in JUNIOR_REJECT:
        if reject in t and "senior" not in t and "director" not in t:
            return False
    # Accept by default (let scoring handle the rest)
    return True

# Location keywords — Remote-Global focus
REMOTE_GLOBAL_KEYWORDS = [
    "remote", "global", "worldwide", "anywhere", "international",
    "europe", "emea", "uk", "london", "berlin", "paris",
    "distributed", "work from anywhere",
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

def matches_location(location):
    """Check if location matches remote-global criteria."""
    loc = location.lower()
    for kw in REMOTE_GLOBAL_KEYWORDS:
        if kw in loc:
            return True
    return False

# ============================================================
# MAIN
# ============================================================

def main():
    api_companies = [(s, a) for s, a in COMPANIES if a in ("greenhouse", "lever", "ashby")]
    skipped = len(COMPANIES) - len(api_companies)

    print(f"\nATS API Checker v1.0 — Joey Clark (Remote-Global)")
    print(f"Week of {WEEK_DATE}")
    print(f"Total in corpus: {len(COMPANIES)} | API-queryable: {len(api_companies)} | Skipped (wttj/unknown/workday): {skipped}")
    print(f"Role categories: Core ({len(CORE_KEYWORDS)}) + Expanded ({len(EXPANDED_KEYWORDS)}) + Secondary ({len(SECONDARY_KEYWORDS)}) = {len(ALL_KEYWORDS)} keywords")
    print(f"{'='*60}")

    all_matches = []
    stats = {"greenhouse": 0, "lever": 0, "ashby": 0,
             "total_jobs_scanned": 0, "companies_checked": 0,
             "companies_with_matches": 0, "rejected_junior": 0}

    for slug, ats in api_companies:
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
                # Seniority check
                if not is_senior_enough(normalized["title"]):
                    stats["rejected_junior"] += 1
                    continue
                # Location filter is soft — include if matches OR ambiguous
                loc = normalized["location"]
                if matches_location(loc) or loc in ("N/A", "", "Flexible", "Multiple"):
                    company_matches.append(normalized)

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
    print(f"Rejected (too junior):  {stats['rejected_junior']}")
    print(f"  Greenhouse: {stats['greenhouse']}")
    print(f"  Lever:      {stats['lever']}")
    print(f"  Ashby:      {stats['ashby']}")

    if all_matches:
        with open(OUTPUT_CSV, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["company_slug", "title", "location", "url", "updated", "ats"])
            writer.writeheader()
            for m in all_matches:
                writer.writerow(m)
        print(f"\nOutput: {OUTPUT_CSV}")
        print(f"\nMatching roles:")
        for m in all_matches:
            print(f"  [{m['ats']}] {m['company_slug']} — {m['title']} ({m['location']})")
            print(f"    {m['url']}")
    else:
        print("\nNo matching roles found. Check company slugs and try expanding keywords.")

if __name__ == "__main__":
    main()
