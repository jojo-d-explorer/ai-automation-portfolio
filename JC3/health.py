#!/usr/bin/env python3
"""health.py — v4 Phase 1, URL health check.

Refactored from searches/archive/job_search_project_v3/scripts/check_urls.py
(the v3.0 draft's copy — check_url() and everything it depends on, lines
1-604 below, are unchanged). What changed is WHEN and WHAT it runs against:

  - v3.x ran this AFTER scoring, against an existing Master CSV, to prune
    dead rows post hoc — Stage 2 budget had already been spent on dead
    URLs by the time this caught them (roadmap failure mode #4).
  - v4 runs this BEFORE JD fetch, directly against discover.py's
    candidates_{date}.csv, and only on non-API rows — API rows (source=
    api/smartrecruiters) are live by definition, since they came from a
    real-time API query this same run; checking them again would be
    redundant network calls for zero new information.

Today, this is a no-op on the actual pipeline: every row discover.py
produces is source=api or source=smartrecruiters (tertiary/discovery-
sourced rows don't exist until Phase 3 builds a real source for them).
The orchestration below is still correctly wired for when they do —
see discover.py's docstring for why the tertiary source is a stub.

Usage:
  python3 JC3/health.py                    # this week's candidates
  python3 JC3/health.py --dry-run          # report only, don't write files

Rules:
  CLOSED  — 404, redirect to board root, page content says job is closed,
            Ashby API confirms job doesn't exist, OR posting expired
  STALE   — posting date found and exceeds MAX_AGE_DAYS (auto-removed)
  GENERIC — URL points to a company careers page, not a specific job listing
            (no job ID in path). Auto-removed.
  BLOCKED — 403 / bot-wall (skip, leave as-is)
  OPEN    — confirmed active job listing with specific job ID in URL
  ERROR   — timeout or connection failure (skip, leave as-is)

Anti-hallucination note:
  CoWork sometimes generates plausible-looking ATS URLs that point to company
  careers pages rather than specific job listings (e.g. jobs.ashbyhq.com/kernel
  instead of jobs.ashbyhq.com/kernel/<uuid>). The GENERIC check catches these
  by requiring a job ID pattern in the URL path before marking anything OPEN.

v2 UPGRADE (2026-02-25):
  1. ASHBY API CHECK: Ashby uses client-side rendering (React), so urllib sees
     an empty shell even for dead jobs. v2 calls Ashby's public GraphQL API
     directly to confirm if a job exists and get its published date.
  2. LINKEDIN CHECK: LinkedIn also client-renders. v2 detects LinkedIn job
     URLs and reads the page title/body for "no longer accepting" signals,
     plus checks JSON-LD datePosted for staleness.
  3. CONTENT SCANNING: Reads page body after HTTP 200 to detect "soft closed"
     jobs on Lever/Greenhouse where the server returns 200 but the page says
     "no longer accepting applications", etc.
  4. DATE STALENESS: Parses JSON-LD structured data (schema.org/JobPosting) to
     extract datePosted/validThrough. Flags jobs older than MAX_AGE_DAYS.
  5. CROSS-DOMAIN REDIRECT: If a Greenhouse/Lever URL redirects to a completely
     different domain (e.g. the company's own careers page), marks as closed.
  6. CAREERS REDIRECT: Detects redirects to generic careers pages.
  7. Close_Reason column explains why each job was removed.
  8. Posting_Age_Days column shows job freshness for open listings.

v2.1 UPGRADE (2026-02-26):
  9. URL SPECIFICITY CHECK: Detects generic company careers pages that lack a
     specific job ID in the URL path. URLs like jobs.ashbyhq.com/kernel (no UUID)
     or boards.greenhouse.io/anthropic (no /jobs/12345) are flagged as GENERIC
     and auto-removed. This catches CoWork hallucinations where plausible ATS
     URLs are generated without actual job IDs.
  10. Anti-hallucination defense: GENERIC check runs BEFORE any HTTP request,
      saving time and preventing false "OPEN" results on company pages that
      return HTTP 200 but aren't actual job listings.

v2.2 UPGRADE (2026-03-11):
  11. WTTJ SUPPORT: Added /jobs/[a-zA-Z0-9]{6,12} pattern to _JOB_ID_PATTERNS
      so Welcome to the Jungle short alphanumeric slugs (e.g. /jobs/mGUwqlPc)
      are recognised as valid specific job URLs rather than flagged as GENERIC.
"""

import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DELAY = 0.5   # seconds between requests (be polite)
TIMEOUT = 10  # seconds per request

# Jobs posted more than this many days ago are flagged as STALE and removed.
MAX_AGE_DAYS = 45


# ---------------------------------------------------------------------------
# Ashby GraphQL API check (bypasses client-side rendering)
# ---------------------------------------------------------------------------

_ASHBY_URL_RE = re.compile(
    r'jobs\.ashbyhq\.com/([^/]+)/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',
    re.IGNORECASE,
)

# LinkedIn job view URLs: linkedin.com/jobs/view/{slug}-{numeric_id}/
_LINKEDIN_URL_RE = re.compile(
    r'linkedin\.com/jobs/view/',
    re.IGNORECASE,
)

# Known ATS domains — if a URL starts on one of these and redirects OFF,
# the job is almost certainly closed (company redirects to their own careers page)
_ATS_DOMAINS = {"greenhouse.io", "lever.co", "ashbyhq.com"}

# ---------------------------------------------------------------------------
# URL specificity check (catches generic company pages / hallucinated URLs)
# ---------------------------------------------------------------------------

# A valid job listing URL must contain a specific job ID in its path.
# Generic company pages (e.g. jobs.ashbyhq.com/kernel) pass HTTP checks
# but aren't actual job listings.
_JOB_ID_PATTERNS = [
    # Greenhouse: /jobs/12345 or /jobs/1234567890
    r'/jobs/\d{4,}',
    # Lever: /company/<uuid>
    r'/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
    # Ashby: /company/<uuid> (same UUID pattern)
    # Also catches shorter hex IDs (some platforms use these)
    r'/[0-9a-f]{24,}',
    # Generic numeric job IDs (catch-all for other ATS platforms)
    r'/jobs?/\d{5,}',
    # Workday-style: /job/<slug>/<numeric-id>
    r'/job/[^/]+/\d{5,}',
    # WTTJ (Welcome to the Jungle): /jobs/<short-alphanumeric-slug>
    r'/jobs/[a-zA-Z0-9]{6,12}',
]

_JOB_ID_RE = re.compile('|'.join(_JOB_ID_PATTERNS), re.IGNORECASE)


def _has_specific_job_id(url):
    """
    Check if a URL contains a specific job ID in its path.
    Returns True if the URL points to a specific listing, False if it's
    just a company careers page.

    Examples:
        boards.greenhouse.io/anthropic/jobs/5021140008  → True
        jobs.lever.co/stripe/abc123de-f456-7890-abcd    → True
        jobs.ashbyhq.com/openai/abcdef12-...            → True
        jobs.ashbyhq.com/kernel                         → False
        boards.greenhouse.io/anthropic                  → False
    """
    return bool(_JOB_ID_RE.search(url))

# LinkedIn-specific closed phrases (rendered in page even for urllib in some cases)
LINKEDIN_CLOSED_PHRASES = [
    "no longer accepting applications",
    "this job is no longer available",
    "this job has expired",
]

_LINKEDIN_CLOSED_RE = re.compile(
    "|".join(re.escape(phrase) for phrase in LINKEDIN_CLOSED_PHRASES),
    re.IGNORECASE,
)

ASHBY_GRAPHQL_ENDPOINT = "https://jobs.ashbyhq.com/api/non-user-graphql?op=ApiJobPosting"

ASHBY_QUERY = """query ApiJobPosting($organizationHostedJobsPageName: String!, $jobPostingId: String!) {
    jobPosting(organizationHostedJobsPageName: $organizationHostedJobsPageName, jobPostingId: $jobPostingId) {
        id
        title
        publishedDate
        isListed
    }
}"""


def _check_ashby_api(url):
    """
    For Ashby URLs, call the GraphQL API directly instead of relying on
    page content (which is client-side rendered and invisible to urllib).

    Returns: (status, detail, age_days) or None if not an Ashby URL.
    """
    match = _ASHBY_URL_RE.search(url)
    if not match:
        return None  # Not an Ashby URL, use standard checks

    org_name = match.group(1)
    job_id = match.group(2)

    try:
        payload = json.dumps({
            "operationName": "ApiJobPosting",
            "variables": {
                "organizationHostedJobsPageName": org_name,
                "jobPostingId": job_id,
            },
            "query": ASHBY_QUERY,
        }).encode("utf-8")

        req = urllib.request.Request(
            ASHBY_GRAPHQL_ENDPOINT,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            },
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        job = data.get("data", {}).get("jobPosting")

        if job is None:
            return "closed", "Ashby API: job not found", None

        # Job exists — check if it's listed
        if not job.get("isListed", True):
            return "closed", "Ashby API: job unlisted", None

        # Job exists and is listed — check staleness via publishedDate
        age_days = None
        published = job.get("publishedDate")
        if published:
            pub_date = _parse_date(published)
            if pub_date:
                today = datetime.now(timezone.utc).date()
                age_days = (today - pub_date).days
                if age_days > MAX_AGE_DAYS:
                    return ("stale",
                            f"Ashby API: posted {age_days}d ago ({published})",
                            age_days)

        return "open", None, age_days

    except urllib.error.HTTPError as e:
        if e.code in (403, 429):
            return "blocked", f"Ashby API HTTP {e.code}", None
        return "error", f"Ashby API HTTP {e.code}", None
    except Exception as e:
        return "error", f"Ashby API error: {str(e)[:60]}", None


# ---------------------------------------------------------------------------
# "Soft closed" content patterns (for Lever / Greenhouse / generic)
# ---------------------------------------------------------------------------

CLOSED_PHRASES = [
    # Lever patterns
    "this posting is no longer accepting applications",
    "this position is no longer available",
    "this position has been filled",
    "this job is no longer available",
    "this job is no longer accepting applications",
    "this role has been filled",
    "this role is no longer available",
    "this posting has been closed",
    "the job posting you're looking for might have closed",
    # Greenhouse patterns
    "the job you are looking for is no longer open",
    "this job post is no longer active",
    "sorry, this position has been closed",
    "job not found",
    # Generic ATS / company career page patterns
    "this opportunity is no longer available",
    "this vacancy has been filled",
    "this listing has expired",
    "this requisition is no longer active",
    "the position you requested is no longer available",
    "we're sorry, this job has been removed",
    "this job has been removed",
    "page not found",
    "404 not found",
    "error 404",
]

_CLOSED_RE = re.compile(
    "|".join(re.escape(phrase) for phrase in CLOSED_PHRASES),
    re.IGNORECASE,
)

CAREERS_PAGE_PHRASES = [
    "browse all jobs",
    "browse open positions",
    "view all openings",
    "search our open roles",
    "explore careers",
    "find your next role",
]

_CAREERS_RE = re.compile(
    "|".join(re.escape(phrase) for phrase in CAREERS_PAGE_PHRASES),
    re.IGNORECASE,
)

ACTIVE_JOB_SIGNALS = [
    "apply now",
    "apply for this job",
    "apply for this position",
    "apply for this role",
    "submit application",
    "submit your application",
]

_ACTIVE_RE = re.compile(
    "|".join(re.escape(phrase) for phrase in ACTIVE_JOB_SIGNALS),
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# JSON-LD date extraction (for Lever / Greenhouse server-rendered pages)
# ---------------------------------------------------------------------------

def _extract_job_posting_dates(body):
    """
    Parse JSON-LD structured data from the page to find datePosted and
    validThrough from schema.org/JobPosting.
    """
    result = {"datePosted": None, "validThrough": None}

    json_ld_pattern = re.compile(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        re.DOTALL | re.IGNORECASE,
    )

    for match in json_ld_pattern.finditer(body):
        try:
            data = json.loads(match.group(1))
        except (json.JSONDecodeError, ValueError):
            continue

        items = data if isinstance(data, list) else [data]

        for item in items:
            if not isinstance(item, dict):
                continue

            candidates = [item]
            if "@graph" in item and isinstance(item["@graph"], list):
                candidates.extend(item["@graph"])

            for candidate in candidates:
                if not isinstance(candidate, dict):
                    continue
                item_type = candidate.get("@type", "")
                if isinstance(item_type, list):
                    is_job = "JobPosting" in item_type
                else:
                    is_job = item_type == "JobPosting"

                if not is_job:
                    continue

                for field in ("datePosted", "validThrough"):
                    raw = candidate.get(field)
                    if not raw or not isinstance(raw, str):
                        continue
                    parsed = _parse_date(raw)
                    if parsed and result[field] is None:
                        result[field] = parsed

    return result


def _parse_date(date_str):
    """Parse an ISO 8601 date string into a date object."""
    date_str = date_str.strip()
    for fmt in (
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M%z",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    tz_stripped = re.sub(r'[+-]\d{2}:\d{2}$', '', date_str)
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"):
        try:
            return datetime.strptime(tz_stripped, fmt).date()
        except ValueError:
            continue

    return None


def _check_staleness(dates, today=None):
    """Check if extracted dates indicate a stale posting."""
    if today is None:
        today = datetime.now(timezone.utc).date()

    valid_through = dates.get("validThrough")
    date_posted = dates.get("datePosted")

    if valid_through and valid_through < today:
        days_expired = (today - valid_through).days
        return True, f"expired {days_expired}d ago (validThrough: {valid_through})", None

    if date_posted:
        age_days = (today - date_posted).days
        if age_days > MAX_AGE_DAYS:
            return True, f"posted {age_days}d ago (datePosted: {date_posted})", age_days
        return False, None, age_days

    return False, None, None


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
# URL status detection (v2: platform-aware + content-aware + date-aware)
# ---------------------------------------------------------------------------

def _is_board_root(original_url, final_url):
    """True if the redirect destination is just the company's board root."""
    orig = original_url.rstrip("/")
    final = final_url.rstrip("/")
    if orig == final:
        return False
    if "lever.co" in final:
        parts = final.split("lever.co/")[-1].split("/")
        if len(parts) == 1 and parts[0]:
            return True
    if "greenhouse.io" in final:
        if "error=true" in final:
            return True
        if "/jobs/" not in final and "job_app" not in final:
            return True
    if "ashbyhq.com" in final:
        parts = final.split("ashbyhq.com/")[-1].split("/")
        if len(parts) == 1 and parts[0]:
            return True
    return False


def _is_careers_index(original_url, final_url, body):
    """True if redirected to a generic careers page."""
    orig = original_url.rstrip("/")
    final = final_url.rstrip("/")
    if orig == final:
        return False
    has_careers_language = bool(_CAREERS_RE.search(body))
    has_apply_button = bool(_ACTIVE_RE.search(body))
    if has_careers_language and not has_apply_button:
        return True
    return False


def _domain(url):
    """Extract domain from URL."""
    try:
        from urllib.parse import urlparse
        return urlparse(url).netloc.lower()
    except Exception:
        return ""


def _is_cross_domain_redirect(original_url, final_url):
    """
    True if the URL started on a known ATS domain (greenhouse.io, lever.co,
    ashbyhq.com) but redirected to a completely different domain.
    
    This catches the pattern where a company's Greenhouse/Lever listing is
    closed and redirects to their own careers page (e.g. ebury.com/careers).
    """
    orig_domain = _domain(original_url)
    final_domain = _domain(final_url)
    
    if orig_domain == final_domain:
        return False
    
    # Check if original URL was on a known ATS domain
    for ats in _ATS_DOMAINS:
        if ats in orig_domain:
            # Redirected off the ATS platform entirely
            return True
    
    return False


def _check_body_for_closed(body):
    """Scan page body for known 'job closed' phrases."""
    match = _CLOSED_RE.search(body)
    if match:
        return match.group(0)
    return None


def check_url(url):
    """
    Returns a tuple: (status, detail, age_days)
      status:   'open', 'closed', 'stale', 'blocked', 'error'
      detail:   reason string for closed/stale/blocked/error, None for open
      age_days: number of days since posting (if found), None otherwise
    """
    if not url or not url.startswith("http"):
        return "error", "invalid URL", None

    # ── GENERIC CHECK: URL must contain a specific job ID ──
    # Runs BEFORE any HTTP request. Catches hallucinated/generic company URLs
    # that would pass HTTP 200 checks but aren't actual job listings.
    if not _has_specific_job_id(url):
        return "generic", f"no job ID in URL path", None

    # ── ASHBY: Use GraphQL API (bypasses client-side rendering) ──
    ashby_result = _check_ashby_api(url)
    if ashby_result is not None:
        return ashby_result

    # ── LEVER / GREENHOUSE / OTHER: Standard HTTP + content checks ──
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            },
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            status = resp.status
            final_url = resp.url
            try:
                raw = resp.read(100000)
                body = raw.decode("utf-8", errors="replace")
            except Exception:
                body = ""
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "closed", "HTTP 404", None
        if e.code in (403, 429):
            return "blocked", f"HTTP {e.code}", None
        return "error", f"HTTP {e.code}", None
    except Exception as e:
        return "error", str(e)[:80], None

    # Check 1: HTTP status
    if status == 404:
        return "closed", "HTTP 404", None
    if status in (403, 429):
        return "blocked", f"HTTP {status}", None

    # Check 2: Redirect to board root
    if _is_board_root(url, final_url):
        return "closed", "redirect to board root", None

    # Check 2b (NEW): Cross-domain redirect — ATS URL redirected off-platform
    # e.g. greenhouse.io/ebury/jobs/123 → ebury.com/careers
    if _is_cross_domain_redirect(url, final_url):
        return "closed", f"cross-domain redirect: {_domain(final_url)}", None

    # Check 3: Page content contains "job closed" language
    closed_phrase = _check_body_for_closed(body)
    if closed_phrase:
        return "closed", f'page says: "{closed_phrase}"', None

    # Check 3b (NEW): LinkedIn-specific closed signals
    if _LINKEDIN_URL_RE.search(url):
        li_match = _LINKEDIN_CLOSED_RE.search(body)
        if li_match:
            return "closed", f'LinkedIn: "{li_match.group(0)}"', None
        # Also check page title for LinkedIn
        title_match = re.search(r'<title[^>]*>(.*?)</title>', body, re.IGNORECASE | re.DOTALL)
        if title_match:
            title_text = title_match.group(1)
            if _LINKEDIN_CLOSED_RE.search(title_text):
                return "closed", f'LinkedIn title: closed', None

    # Check 4: Redirected to generic careers page
    if _is_careers_index(url, final_url, body):
        return "closed", "redirect to careers index page", None

    # Check 5: Extract posting dates from JSON-LD and check staleness
    dates = _extract_job_posting_dates(body)
    is_stale, stale_reason, age_days = _check_staleness(dates)
    if is_stale:
        return "stale", stale_reason, age_days

    return "open", None, age_days




# ---------------------------------------------------------------------------
# v4 orchestration — reads discover.py's candidates_{date}.csv, checks only
# non-API rows, splits into verified (passed / API-live-by-definition) and
# dropped (closed/stale/generic), writes both for fetch_jds.py to consume.
# ---------------------------------------------------------------------------

API_SOURCES = {"api", "smartrecruiters"}


def run_health_check(candidates_csv, dry_run=False):
    with open(candidates_csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys()) if rows else []

    for extra in ("health_status", "health_detail", "posting_age_days"):
        if extra not in fieldnames:
            fieldnames.append(extra)

    api_rows = [r for r in rows if r.get("source", "") in API_SOURCES]
    non_api_rows = [r for r in rows if r.get("source", "") not in API_SOURCES]

    print(f"\n{'─'*70}")
    print(f"  health.py — {len(rows)} total candidates")
    print(f"  {len(api_rows)} API rows (live by definition, skipped)")
    print(f"  {len(non_api_rows)} non-API rows to check")
    print(f"  Staleness threshold: {MAX_AGE_DAYS} days")
    print(f"{'─'*70}")

    for r in api_rows:
        r["health_status"] = "open"
        r["health_detail"] = "api-live"

    verified = list(api_rows)
    dropped = []

    for i, row in enumerate(non_api_rows, 1):
        url = row.get("url", "").strip()
        status, detail, age_days = check_url(url)
        row["health_status"] = status
        row["health_detail"] = detail or ""
        row["posting_age_days"] = str(age_days) if age_days is not None else ""

        symbol = {"open": "✓", "closed": "✗", "stale": "⏰",
                  "generic": "⚠", "blocked": "~", "error": "?"}[status]
        print(f"  [{i:>3}/{len(non_api_rows)}] {symbol} {status:<8}  "
              f"{row.get('company_name','')[:28]:<28} — {row.get('title','')[:32]}")
        time.sleep(DELAY)

        if status in ("closed", "stale", "generic"):
            dropped.append(row)
        else:
            # blocked / error: can't confirm dead — keep, flagged, matching
            # check_url()'s original "skip, leave as-is" semantics.
            verified.append(row)

    print(f"\n  Verified: {len(verified)} ({len(api_rows)} API + "
          f"{len(verified) - len(api_rows)} non-API passed) | Dropped: {len(dropped)}")

    if dry_run:
        print("\n  [dry-run] No files written.")
        return verified, dropped

    week_dir = os.path.dirname(candidates_csv)
    week_date = os.path.basename(candidates_csv).replace("candidates_", "").replace(".csv", "")
    verified_path = os.path.join(week_dir, f"verified_candidates_{week_date}.csv")
    dropped_path = os.path.join(week_dir, f"health_dropped_{week_date}.csv")

    with open(verified_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(verified)

    if dropped:
        with open(dropped_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(dropped)

    print(f"\n  Verified candidates: {verified_path}")
    if dropped:
        print(f"  Dropped (diagnostics): {dropped_path}")

    return verified, dropped


def _latest_candidates_csv():
    """Find this week's candidates_{date}.csv under results/joey/LATAM/."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    latam_dir = os.path.join(repo_root, "results", "joey", "LATAM")
    if not os.path.isdir(latam_dir):
        return None
    week_dirs = sorted(
        d for d in os.listdir(latam_dir)
        if d.startswith("Week_of_") and os.path.isdir(os.path.join(latam_dir, d))
    )
    if not week_dirs:
        return None
    latest = week_dirs[-1]
    date_str = latest.replace("Week_of_", "")
    candidates = os.path.join(latam_dir, latest, f"candidates_{date_str}.csv")
    return candidates if os.path.exists(candidates) else None


def main():
    dry_run = "--dry-run" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--dry-run"]

    candidates_csv = args[0] if args else _latest_candidates_csv()
    if not candidates_csv or not os.path.exists(candidates_csv):
        print(f"No candidates CSV found (looked for: {candidates_csv}). "
              f"Run discover.py first, or pass a path explicitly.")
        sys.exit(1)

    print(f"\n  health.py — checking {candidates_csv}")
    if dry_run:
        print("  [dry-run mode — no files will be modified]")

    run_health_check(candidates_csv, dry_run=dry_run)


if __name__ == "__main__":
    main()
