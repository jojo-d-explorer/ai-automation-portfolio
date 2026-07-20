#!/usr/bin/env python3
"""
ATS API Checker for Joey Clark — v2.2
Hits Greenhouse, Lever, and Ashby APIs for the curated company list.
Reads flat v2.2 schema from companies.json.
Outputs API-verified open jobs with corpus metadata enrichment + eligibility flag pre-tagging.

The output is consumed by the ONE_CLICK_v2.md prompt for scoring.

Usage:
    python3 ats_api_checker_v2.py

Output:
    results/joey/Week_of_{DATE}/api_verified_{DATE}.csv
    (consumed by ONE_CLICK_v2.md for scoring + dedup against Google-indexed results)

Requires: requests (pip install requests)
"""

import requests
import csv
import re
import os
import json
from datetime import datetime, timedelta

# ============================================================
# CONFIG
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.now()
MONDAY = TODAY - timedelta(days=TODAY.weekday())
WEEK_DATE = MONDAY.strftime("%Y-%m-%d")
# Results land inside job_search_project/results/joey/Week_of_YYYY-MM-DD/
RESULTS_DIR = os.path.join(SCRIPT_DIR, f"results/joey/Week_of_{WEEK_DATE}")
OUTPUT_CSV = os.path.join(RESULTS_DIR, f"api_verified_{WEEK_DATE}.csv")
COMPANIES_JSON = os.path.join(SCRIPT_DIR, "companies.json")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ============================================================
# ROLE KEYWORDS — v2.2 family-based structure
# ============================================================
ROLE_FAMILIES = {
    "chief_of_staff": [
        "chief of staff", "founding chief of staff", "head of ceo office",
        "office of the ceo", "principal to the ceo", "strategic advisor to ceo",
        "chief of staff to ceo", "chief of staff to founder",
    ],
    "partnerships_bd": [
        "head of partnerships", "director of partnerships", "vp partnerships",
        "vp of partnerships", "partnerships director",
        "head of business development", "director of business development",
        "bd director", "head of bd", "strategic alliances",
        "head of strategic alliances", "platform partnerships",
        "ecosystem partnerships", "channel partnerships", "institutional partnerships",
    ],
    "strategic_ops": [
        "strategic operations", "head of strategic operations",
        "strategy & operations", "strategy and operations",
        "director of strategy and operations", "director of strategy & operations",
        "director of strategy", "head of strategy",
        "strategic initiatives", "director of strategic initiatives",
        "strategic projects", "strategic projects director",
        "strategic programs",
        "business operations director", "director of business operations",
        "head of business operations", "chief operating officer",
    ],
    "market_entry": [
        "market entry", "market launch", "country manager", "country lead",
        "general manager", "head of emea", "head of europe",
        "head of latam", "head of americas", "head of france",
        "head of uk", "head of portugal", "head of brazil",
        "regional director", "regional lead", "expansion lead",
        "international expansion", "global expansion",
        "go-to-market lead", "market development",
    ],
    "govt_defense": [
        "government partnerships", "government affairs",
        "public sector partnerships", "defense partnerships",
        "federal partnerships", "head of federal",
        "mission operations", "head of mission", "public sector lead",
    ],
    "growth_commercial": [
        "head of growth", "head of gtm", "go-to-market",
        "commercial director", "head of commercial",
        "corporate development", "operating partner",
        "operator-in-residence", "entrepreneur-in-residence", "venture partner",
    ],
    "program": [
        "program director", "senior program manager",
        "head of programs", "director of programs",
        "strategic programs manager",
    ],
}

ALL_KEYWORDS = []
KEYWORD_TO_FAMILY = {}
for family, kws in ROLE_FAMILIES.items():
    for kw in kws:
        ALL_KEYWORDS.append(kw)
        KEYWORD_TO_FAMILY[kw] = family

# ============================================================
# SENIORITY GATE — two-layer per v2.2 spec
# ============================================================
HARD_REJECT = [
    "associate", "coordinator", "specialist", "intern",
    "assistant", "junior", "entry-level", "entry level",
]
HARD_REJECT_EXCEPTIONS = ["senior associate", "senior specialist", "principal associate"]
SOFT_FLOOR_MARKERS = [
    "manager", "senior manager", "principal", "lead", "head of",
    "director", "vp", "vice president", "chief", "founding",
]

def passes_seniority_gate(title):
    t = title.lower()
    if any(ex in t for ex in HARD_REJECT_EXCEPTIONS):
        return True
    for hr in HARD_REJECT:
        if hr in t and not any(s in t for s in ["senior", "lead", "principal", "head", "director", "vp", "chief"]):
            return False
    return True  # everything else passes; archetype scoring handles it later

# ============================================================
# ELIGIBILITY FLAGS — three-scenario per v2.2 spec
# ============================================================
def evaluate_eligibility(location_text):
    """
    Returns (latam, dc, portugal, summary) where each flag is 'true', 'false', or 'unclear'.
    """
    if not location_text:
        return ("unclear", "unclear", "unclear", "unclear")
    
    loc = location_text.lower()
    
    # Universal remote signals
    universal_remote = any(kw in loc for kw in [
        "remote-global", "remote (worldwide)", "remote (global)",
        "remote - worldwide", "work from anywhere", "fully remote",
        "remote anywhere", "anywhere in the world",
    ])
    
    # Remote-US signals
    remote_us = any(kw in loc for kw in [
        "remote us", "remote - us", "remote (us)", "remote united states",
        "us-based remote", "remote within the us", "anywhere in the us",
        "anywhere in the united states",
    ])
    
    # Remote-Americas / Remote-LATAM signals
    remote_americas = any(kw in loc for kw in [
        "remote americas", "remote - americas", "remote latam",
        "remote - latam", "americas remote", "remote latin america",
    ])
    
    # Remote-EU / Remote-EMEA signals
    remote_eu = any(kw in loc for kw in [
        "remote europe", "remote - europe", "remote emea", "remote - emea",
        "remote eu", "eu remote", "europe-based",
    ])
    
    # Target city signals
    in_la_cities = any(kw in loc for kw in ["buenos aires", "panama city", "bogotá", "bogota"])
    in_dc = any(kw in loc for kw in ["washington dc", "washington, dc", "dc-based", "remote - dc", "remote dc"])
    in_portugal = any(kw in loc for kw in ["lisbon", "portugal", "porto"])
    
    # Hard non-viable city detection (in-office only)
    in_office_signals = any(kw in loc for kw in ["in-office", "on-site", "in office", "on site"])
    non_viable_cities = ["new york", "nyc", "san francisco", "berlin", "madrid",
                         "barcelona", "amsterdam", "dublin", "stockholm", "zurich",
                         "copenhagen", "singapore", "dubai", "tokyo", "hong kong"]
    locked_to_non_viable = in_office_signals and any(c in loc for c in non_viable_cities)
    
    # Generic "remote" without geography
    remote_generic = "remote" in loc and not (universal_remote or remote_us or remote_americas or remote_eu or in_la_cities or in_dc or in_portugal)
    
    # ----- LATAM Mode -----
    if universal_remote or remote_us or remote_americas or in_la_cities:
        latam = "true"
    elif locked_to_non_viable or remote_eu and not universal_remote:
        latam = "false"
    elif remote_generic:
        latam = "unclear"
    else:
        latam = "false"
    
    # ----- DC Mode -----
    if universal_remote or remote_us or in_dc:
        dc = "true"
    elif locked_to_non_viable:
        dc = "false"
    elif remote_americas or remote_eu:
        dc = "false" if not universal_remote else "true"
    elif remote_generic:
        dc = "unclear"
    else:
        dc = "false"
    
    # ----- Portugal Mode -----
    if universal_remote or remote_eu or in_portugal:
        portugal = "true"
    elif remote_us:
        portugal = "unclear"  # depends on whether they accept Portugal-based; flag for review
    elif locked_to_non_viable:
        portugal = "false"
    elif remote_generic:
        portugal = "unclear"
    else:
        portugal = "false"
    
    # Summary
    parts = []
    if latam == "true": parts.append("L")
    elif latam == "unclear": parts.append("L?")
    if dc == "true": parts.append("D")
    elif dc == "unclear": parts.append("D?")
    if portugal == "true": parts.append("P")
    elif portugal == "unclear": parts.append("P?")
    summary = ", ".join(parts) if parts else "none"
    
    return (latam, dc, portugal, summary)

# ============================================================
# CORPUS LOADING — v2.2 flat schema
# ============================================================
def load_companies(path):
    with open(path) as f:
        data = json.load(f)
    if "companies" in data and isinstance(data["companies"], list):
        return [c for c in data["companies"] if c.get("status") == "active"]
    raise ValueError("companies.json must contain a top-level 'companies' array (v2.2 schema)")

# ============================================================
# API FETCHERS
# ============================================================
def fetch_greenhouse(slug):
    try:
        r = requests.get(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs", timeout=10)
        return r.json().get("jobs", []) if r.status_code == 200 else []
    except Exception as e:
        print(f"  [{slug}] Greenhouse error: {e}")
        return []

def fetch_lever(slug):
    try:
        r = requests.get(f"https://api.lever.co/v0/postings/{slug}", timeout=10)
        return r.json() if r.status_code == 200 else []
    except Exception as e:
        print(f"  [{slug}] Lever error: {e}")
        return []

def fetch_ashby(slug):
    try:
        r = requests.get(f"https://api.ashbyhq.com/posting-api/job-board/{slug}", timeout=10)
        return r.json().get("jobs", []) if r.status_code == 200 else []
    except Exception as e:
        print(f"  [{slug}] Ashby error: {e}")
        return []

# ============================================================
# NORMALIZERS
# ============================================================
def normalize_greenhouse(job, slug):
    return {
        "company_slug": slug,
        "title": job.get("title", ""),
        "location": job.get("location", {}).get("name", "N/A"),
        "url": job.get("absolute_url", ""),
        "updated": job.get("updated_at", ""),
        "ats": "Greenhouse",
    }

def normalize_lever(job, slug):
    ts = job.get("createdAt")
    updated = datetime.fromtimestamp(ts / 1000).isoformat() if ts else ""
    return {
        "company_slug": slug,
        "title": job.get("text", ""),
        "location": job.get("categories", {}).get("location", "N/A"),
        "url": job.get("hostedUrl", ""),
        "updated": updated,
        "ats": "Lever",
    }

def normalize_ashby(job, slug):
    job_id = job.get("id", "")
    return {
        "company_slug": slug,
        "title": job.get("title", ""),
        "location": job.get("location", "N/A"),
        "url": f"https://jobs.ashbyhq.com/{slug}/{job_id}" if job_id else "",
        "updated": job.get("publishedAt", ""),
        "ats": "Ashby",
    }

# ============================================================
# ROLE MATCHING
# ============================================================
def match_role(title):
    t = title.lower()
    for kw in ALL_KEYWORDS:
        if kw in t:
            return KEYWORD_TO_FAMILY[kw]
    return None

# ============================================================
# MAIN
# ============================================================
def main():
    companies = load_companies(COMPANIES_JSON)
    api_companies = [c for c in companies if c.get("ats") in ("greenhouse", "lever", "ashby")]
    skipped = len(companies) - len(api_companies)

    print(f"\nATS API Checker v2.2 — Joey Clark")
    print(f"Week of {WEEK_DATE}")
    print(f"Total active companies: {len(companies)} | API-queryable: {len(api_companies)} | Skipped: {skipped}")
    print(f"Role families: {len(ROLE_FAMILIES)} families, {len(ALL_KEYWORDS)} keywords")
    print(f"{'='*70}")

    fetchers = {"greenhouse": (fetch_greenhouse, normalize_greenhouse),
                "lever": (fetch_lever, normalize_lever),
                "ashby": (fetch_ashby, normalize_ashby)}

    all_matches = []
    stats = {"greenhouse": 0, "lever": 0, "ashby": 0,
             "total_jobs_scanned": 0, "companies_checked": 0,
             "companies_with_matches": 0, "rejected_seniority": 0,
             "rejected_eligibility": 0}

    for company in api_companies:
        slug = company["slug"]
        ats = company["ats"]
        stats["companies_checked"] += 1
        fetcher, normalizer = fetchers[ats]
        raw_jobs = fetcher(slug)
        stats["total_jobs_scanned"] += len(raw_jobs)
        
        company_matches = []
        for job in raw_jobs:
            normalized = normalizer(job, slug)
            
            # Role family match
            family = match_role(normalized["title"])
            if not family:
                continue
            
            # Seniority gate
            if not passes_seniority_gate(normalized["title"]):
                stats["rejected_seniority"] += 1
                continue
            
            # Eligibility flags
            latam, dc, portugal, summary = evaluate_eligibility(normalized["location"])
            if summary == "none":
                stats["rejected_eligibility"] += 1
                continue
            
            # Enrich with corpus metadata + eligibility
            normalized.update({
                "role_family": family,
                "company_name": company.get("name", slug),
                "company_sector": ",".join(company.get("sector", [])),
                "company_stage": company.get("stage", "unknown"),
                "company_geography_hq": company.get("geography_hq", "unknown"),
                "company_priority_tier": company.get("priority_tier", 3),
                "us_investor_signal": company.get("us_investor_signal", "unknown"),
                "us_investors": ", ".join(company.get("us_investors", [])) if company.get("us_investors") else "",
                "lusophone_exposure": company.get("lusophone_exposure", "none"),
                "latam_exposure": company.get("latam_exposure", "none"),
                "eligible_latam_mode": latam,
                "eligible_dc_mode": dc,
                "eligible_portugal_mode": portugal,
                "eligibility_summary": summary,
            })
            company_matches.append(normalized)
        
        if company_matches:
            stats["companies_with_matches"] += 1
            stats[ats] += len(company_matches)
            all_matches.extend(company_matches)
            print(f"  ✓ {slug:30s} ({ats:10s}): {len(company_matches)} matches")

    # ============ OUTPUT ============
    print(f"\n{'='*70}")
    print(f"Companies checked: {stats['companies_checked']} | Jobs scanned: {stats['total_jobs_scanned']}")
    print(f"Matches: {len(all_matches)} | Rejected seniority: {stats['rejected_seniority']} | Rejected eligibility: {stats['rejected_eligibility']}")
    print(f"By ATS: GH={stats['greenhouse']} | Lever={stats['lever']} | Ashby={stats['ashby']}")
    
    if all_matches:
        fieldnames = ["company_slug", "company_name", "title", "role_family", "location",
                      "eligibility_summary", "eligible_latam_mode", "eligible_dc_mode", "eligible_portugal_mode",
                      "company_sector", "company_stage", "company_geography_hq",
                      "company_priority_tier", "us_investor_signal", "us_investors",
                      "lusophone_exposure", "latam_exposure",
                      "url", "updated", "ats"]
        with open(OUTPUT_CSV, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for m in all_matches:
                writer.writerow({k: m.get(k, "") for k in fieldnames})
        print(f"\nOutput: {OUTPUT_CSV}")
    else:
        print("\nNo matching roles found.")

if __name__ == "__main__":
    main()
