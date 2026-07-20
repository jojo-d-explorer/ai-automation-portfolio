#!/usr/bin/env python3
"""
discover.py — v4 Phase 1, primary/secondary/tertiary discovery.

Refactored from searches/joey/ats_api_checker.py (v2.2), which is now
transitional/superseded — its role-family keywords, seniority gate,
eligibility evaluator, and ATS fetchers/normalizers all move here
unchanged. See CLAUDE.md and Core/HANDOFF_ROADMAP_v4_Claude_Code.md §4.

Three sources, in priority order:
  1. PRIMARY — full-corpus ATS API sweep (Greenhouse, Lever, Ashby) for
     companies with status=active. This is what ats_api_checker.py already
     did; unchanged logic, just relocated and given a `source` column.
  2. SECONDARY — SmartRecruiters public postings API, for companies tagged
     ats=smartrecruiters. Queried regardless of status (active or
     pending_review) — unlike the primary sweep, gating this on `status`
     would make it a permanent no-op: all 34 smartrecruiters-tagged
     companies in the corpus are currently pending_review, none active.
     `status` is a review/triage axis, not an ATS-resolution axis; the
     same role-family/seniority/eligibility gates below still filter the
     actual output rows, so including pending_review companies here
     doesn't bypass any real quality check.
  3. TERTIARY — targeted web discovery for NEW companies only (never for
     sourcing rows directly). Deliberately a stub in Phase 1: the roadmap
     and Strategy Addendum both scope the real discovery-breadth sources
     (Getonbrd, VC portfolio boards, SerpAPI, LinkedIn daily links) to
     Phase 3, not Phase 1. Building an ad hoc scraper here would also
     violate the "deterministic Python, no model/browser touching a
     network primitive for pipeline-critical steps" hard rule without a
     real API behind it. This function returns an empty list and logs
     why, rather than faking coverage.

Output: candidates_{date}.csv at repo root results/joey/LATAM/Week_of_{date}/,
with a `source` column (api / smartrecruiters / discovery) and a
`latam_relevance` column (added to companies.json this phase, default
"none" for all 587 — no backfill source was found; see CLAUDE.md).

Usage:
    python3 JC3/discover.py
"""

import csv
import json
import os
import sys
from datetime import datetime, timedelta

import requests

# ============================================================
# CONFIG / PATHS
# ============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.dirname(SCRIPT_DIR)  # repo root
COMPANIES_JSON = os.path.join(BASE_PATH, "searches/joey/companies.json")

TODAY = datetime.now()
MONDAY = TODAY - timedelta(days=TODAY.weekday())
WEEK_DATE = MONDAY.strftime("%Y-%m-%d")
RESULTS_DIR = os.path.join(BASE_PATH, f"results/joey/LATAM/Week_of_{WEEK_DATE}")
CANDIDATES_CSV = os.path.join(RESULTS_DIR, f"candidates_{WEEK_DATE}.csv")
os.makedirs(RESULTS_DIR, exist_ok=True)

sys.path.insert(0, os.path.join(BASE_PATH, "scripts"))

# ============================================================
# ROLE KEYWORDS — v2.2 family-based structure (unchanged from
# ats_api_checker.py; also mirrored in config/joey_profile.yaml)
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
        "general manager", "regional director", "regional lead",
        "expansion lead", "international expansion", "global expansion",
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
# SENIORITY GATE — unchanged from ats_api_checker.py
# ============================================================
HARD_REJECT = [
    "associate", "coordinator", "specialist", "intern",
    "assistant", "junior", "entry-level", "entry level",
]
HARD_REJECT_EXCEPTIONS = ["senior associate", "senior specialist", "principal associate"]


def passes_seniority_gate(title):
    t = title.lower()
    if any(ex in t for ex in HARD_REJECT_EXCEPTIONS):
        return True
    for hr in HARD_REJECT:
        if hr in t and not any(s in t for s in ["senior", "lead", "principal", "head", "director", "vp", "chief"]):
            return False
    return True


# ============================================================
# ELIGIBILITY FLAGS — unchanged from ats_api_checker.py
# ============================================================
def evaluate_eligibility(location_text):
    """Returns (latam, dc, portugal, summary) — dc/portugal are legacy
    modes from earlier pivots (see CLAUDE.md); kept for parity with the
    corpus's existing enrichment fields, not treated as active targets."""
    if not location_text:
        return ("unclear", "unclear", "unclear", "unclear")

    loc = location_text.lower()

    universal_remote = any(kw in loc for kw in [
        "remote-global", "remote (worldwide)", "remote (global)",
        "remote - worldwide", "work from anywhere", "fully remote",
        "remote anywhere", "anywhere in the world",
    ])
    remote_us = any(kw in loc for kw in [
        "remote us", "remote - us", "remote (us)", "remote united states",
        "us-based remote", "remote within the us", "anywhere in the us",
        "anywhere in the united states",
    ])
    remote_americas = any(kw in loc for kw in [
        "remote americas", "remote - americas", "remote latam",
        "remote - latam", "americas remote", "remote latin america",
    ])
    remote_eu = any(kw in loc for kw in [
        "remote europe", "remote - europe", "remote emea", "remote - emea",
        "remote eu", "eu remote", "europe-based",
    ])
    in_la_cities = any(kw in loc for kw in ["buenos aires", "panama city", "bogotá", "bogota", "mexico city", "cdmx"])
    in_dc = any(kw in loc for kw in ["washington dc", "washington, dc", "dc-based", "remote - dc", "remote dc"])
    in_portugal = any(kw in loc for kw in ["lisbon", "portugal", "porto"])

    in_office_signals = any(kw in loc for kw in ["in-office", "on-site", "in office", "on site"])
    non_viable_cities = ["new york", "nyc", "san francisco", "berlin", "madrid",
                          "barcelona", "amsterdam", "dublin", "stockholm", "zurich",
                          "copenhagen", "singapore", "dubai", "tokyo", "hong kong"]
    locked_to_non_viable = in_office_signals and any(c in loc for c in non_viable_cities)

    remote_generic = "remote" in loc and not (universal_remote or remote_us or remote_americas or remote_eu or in_la_cities or in_dc or in_portugal)

    if universal_remote or remote_us or remote_americas or in_la_cities:
        latam = "true"
    elif locked_to_non_viable or (remote_eu and not universal_remote):
        latam = "false"
    elif remote_generic:
        latam = "unclear"
    else:
        latam = "false"

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

    if universal_remote or remote_eu or in_portugal:
        portugal = "true"
    elif remote_us:
        portugal = "unclear"
    elif locked_to_non_viable:
        portugal = "false"
    elif remote_generic:
        portugal = "unclear"
    else:
        portugal = "false"

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
# CORPUS LOADING
# ============================================================
def load_companies(path):
    with open(path) as f:
        data = json.load(f)
    if "companies" not in data or not isinstance(data["companies"], list):
        raise ValueError("companies.json must contain a top-level 'companies' array (v2.2 schema)")
    return data["companies"]


def ensure_latam_relevance_field(path):
    """Phase 1 schema addition (roadmap §4): add latam_relevance to every
    company, default "none". No backfill source was found (checked the
    archived ONE_CLICK prompts and job_search_project_v3/ for a LATAM
    sector-focus list — doesn't exist under that description); confirmed
    with Joey to leave it at "none" for now rather than guess. Idempotent
    — safe to run every invocation."""
    with open(path) as f:
        data = json.load(f)
    changed = False
    for c in data["companies"]:
        if "latam_relevance" not in c:
            c["latam_relevance"] = "none"
            changed = True
    if changed:
        with open(path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
    return data


# ============================================================
# API FETCHERS — unchanged from ats_api_checker.py
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


def fetch_smartrecruiters(slug):
    """SECONDARY source. SmartRecruiters public postings API — new in
    Phase 1, no prior implementation existed. `slug` here is the
    SmartRecruiters company identifier stored as the corpus entry's
    `slug` field for ats=smartrecruiters entries."""
    try:
        r = requests.get(f"https://api.smartrecruiters.com/v1/companies/{slug}/postings", timeout=10)
        return r.json().get("content", []) if r.status_code == 200 else []
    except Exception as e:
        print(f"  [{slug}] SmartRecruiters error: {e}")
        return []


# ============================================================
# NORMALIZERS
# ============================================================
def normalize_greenhouse(job, slug):
    return {
        "company_slug": slug, "title": job.get("title", ""),
        "location": job.get("location", {}).get("name", "N/A"),
        "url": job.get("absolute_url", ""), "updated": job.get("updated_at", ""),
        "ats": "Greenhouse",
    }


def normalize_lever(job, slug):
    ts = job.get("createdAt")
    updated = datetime.fromtimestamp(ts / 1000).isoformat() if ts else ""
    return {
        "company_slug": slug, "title": job.get("text", ""),
        "location": job.get("categories", {}).get("location", "N/A"),
        "url": job.get("hostedUrl", ""), "updated": updated, "ats": "Lever",
    }


def normalize_ashby(job, slug):
    job_id = job.get("id", "")
    return {
        "company_slug": slug, "title": job.get("title", ""),
        "location": job.get("location", "N/A"),
        "url": f"https://jobs.ashbyhq.com/{slug}/{job_id}" if job_id else "",
        "updated": job.get("publishedAt", ""), "ats": "Ashby",
    }


def normalize_smartrecruiters(job, slug):
    ref = job.get("id", "")
    return {
        "company_slug": slug, "title": job.get("name", ""),
        "location": (job.get("location") or {}).get("city", "N/A"),
        "url": f"https://jobs.smartrecruiters.com/{slug}/{ref}" if ref else "",
        "updated": job.get("releasedDate", ""), "ats": "SmartRecruiters",
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


def enrich_and_filter(normalized, company, source, stats):
    """Shared row-processing path for every source (primary/secondary):
    role match, seniority gate, eligibility, corpus metadata enrichment.
    Returns the enriched dict or None if the row is filtered out."""
    family = match_role(normalized["title"])
    if not family:
        return None
    if not passes_seniority_gate(normalized["title"]):
        stats["rejected_seniority"] += 1
        return None
    latam, dc, portugal, summary = evaluate_eligibility(normalized["location"])
    if summary == "none":
        stats["rejected_eligibility"] += 1
        return None

    normalized.update({
        "source": source,
        "role_family": family,
        "company_name": company.get("name", normalized["company_slug"]),
        "company_sector": ",".join(company.get("sector", [])),
        "company_stage": company.get("stage", "unknown"),
        "company_geography_hq": company.get("geography_hq", "unknown"),
        "company_priority_tier": company.get("priority_tier") or 3,
        "latam_relevance": company.get("latam_relevance", "none"),
        "us_investor_signal": company.get("us_investor_signal", "unknown"),
        "eligible_latam_mode": latam,
        "eligible_dc_mode": dc,
        "eligible_portugal_mode": portugal,
        "eligibility_summary": summary,
    })
    return normalized


# ============================================================
# TERTIARY — deliberately a stub in Phase 1 (see module docstring)
# ============================================================
def discover_tertiary_web():
    print("\n[tertiary] Targeted web discovery: not built this phase.")
    print("[tertiary] Real recall-breadth sources (Getonbrd, VC portfolio")
    print("[tertiary] boards, SerpAPI, LinkedIn daily links) are explicitly")
    print("[tertiary] Phase 3 per the Strategy Addendum. Returning 0 new")
    print("[tertiary] company candidates for corpus_append.py this run.")
    return []


# ============================================================
# MAIN
# ============================================================
def main():
    data = ensure_latam_relevance_field(COMPANIES_JSON)
    companies = data["companies"]

    stats = {
        "companies_checked": 0, "total_jobs_scanned": 0,
        "rejected_seniority": 0, "rejected_eligibility": 0,
        "api_matches": 0, "smartrecruiters_matches": 0,
    }
    all_matches = []

    # ---------- PRIMARY: ATS API sweep, active companies only ----------
    primary_companies = [c for c in companies if c.get("status") == "active" and c.get("ats") in ("greenhouse", "lever", "ashby")]
    fetchers = {
        "greenhouse": (fetch_greenhouse, normalize_greenhouse),
        "lever": (fetch_lever, normalize_lever),
        "ashby": (fetch_ashby, normalize_ashby),
    }

    print(f"\ndiscover.py — Joey Clark, week of {WEEK_DATE}")
    print(f"{'='*70}")
    print(f"[primary] {len(primary_companies)} active API-queryable companies (greenhouse/lever/ashby)")

    for company in primary_companies:
        slug = company["slug"]
        ats = company["ats"]
        stats["companies_checked"] += 1
        fetcher, normalizer = fetchers[ats]
        raw_jobs = fetcher(slug)
        stats["total_jobs_scanned"] += len(raw_jobs)
        for job in raw_jobs:
            normalized = normalizer(job, slug)
            enriched = enrich_and_filter(normalized, company, "api", stats)
            if enriched:
                all_matches.append(enriched)
                stats["api_matches"] += 1

    # ---------- SECONDARY: SmartRecruiters, any status ----------
    sr_companies = [c for c in companies if c.get("ats") == "smartrecruiters"]
    print(f"[secondary] {len(sr_companies)} smartrecruiters-tagged companies (any status)")

    for company in sr_companies:
        slug = company["slug"]
        stats["companies_checked"] += 1
        raw_jobs = fetch_smartrecruiters(slug)
        stats["total_jobs_scanned"] += len(raw_jobs)
        for job in raw_jobs:
            normalized = normalize_smartrecruiters(job, slug)
            enriched = enrich_and_filter(normalized, company, "smartrecruiters", stats)
            if enriched:
                all_matches.append(enriched)
                stats["smartrecruiters_matches"] += 1

    # ---------- TERTIARY: capped web discovery, corpus growth only ----------
    new_company_candidates = discover_tertiary_web()
    if new_company_candidates:
        sys.path.insert(0, os.path.join(BASE_PATH, "scripts"))
        from corpus_append import append_corpus  # noqa: E402
        from pathlib import Path
        append_corpus(new_company_candidates, Path(COMPANIES_JSON), dry_run=False)

    # ---------- OUTPUT ----------
    print(f"\n{'='*70}")
    print(f"Companies checked: {stats['companies_checked']} | Jobs scanned: {stats['total_jobs_scanned']}")
    print(f"Matches: api={stats['api_matches']} smartrecruiters={stats['smartrecruiters_matches']} | "
          f"Rejected seniority={stats['rejected_seniority']} eligibility={stats['rejected_eligibility']}")

    fieldnames = ["source", "company_slug", "company_name", "title", "role_family", "location",
                  "eligibility_summary", "eligible_latam_mode", "eligible_dc_mode", "eligible_portugal_mode",
                  "latam_relevance", "company_sector", "company_stage", "company_geography_hq",
                  "company_priority_tier", "us_investor_signal", "url", "updated", "ats"]
    with open(CANDIDATES_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for m in all_matches:
            writer.writerow({k: m.get(k, "") for k in fieldnames})

    print(f"\nOutput: {CANDIDATES_CSV}")
    return CANDIDATES_CSV


if __name__ == "__main__":
    main()
