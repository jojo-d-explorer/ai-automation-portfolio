#!/usr/bin/env python3
"""
URL classifier for ATS job-board URLs.

Given a job-posting URL, returns the ATS, the company slug, and the job ID.
Used by the v2.3 discovery pipeline to:
  (1) standardize candidate metadata across boards, and
  (2) drive automatic corpus growth (stub append for previously-unseen slugs).

Supported boards:
  - Greenhouse (boards.greenhouse.io and job-boards.greenhouse.io)
  - Lever      (jobs.lever.co)
  - Ashby      (jobs.ashbyhq.com)
  - Workday    (*.myworkdayjobs.com — slug is the tenant subdomain)
  - SmartRecruiters (jobs.smartrecruiters.com)
  - Welcome to the Jungle (app.welcometothejungle.com — opaque hash IDs;
                            slug is "unknown" unless a /companies/[slug] hop is added)

Usage as a module:
    from classify_url import classify_url
    classify_url("https://jobs.ashbyhq.com/rescale/1598f382-...")
    # -> {"ats": "ashby", "slug": "rescale", "job_id": "1598f382-...", "url_type": "job"}

CLI:
    python3 classify_url.py <url>          # classify one
    python3 classify_url.py --test         # run built-in self-tests
    python3 classify_url.py --stdin        # one URL per line on stdin
"""
from __future__ import annotations

import re
import sys
import json
from typing import Optional
from urllib.parse import urlparse


# Regex patterns per board. Each pattern's groups should yield (slug, job_id)
# unless otherwise noted. Patterns are evaluated in declaration order; first
# match wins, so place more-specific patterns first.
_PATTERNS = [
    # Greenhouse — newer "job-boards" subdomain
    ("greenhouse",
     re.compile(r"^job-boards\.greenhouse\.io/(?P<slug>[^/]+)/jobs/(?P<job_id>\d+)")),
    # Greenhouse — classic "boards" subdomain
    ("greenhouse",
     re.compile(r"^boards\.greenhouse\.io/(?P<slug>[^/]+)/jobs/(?P<job_id>\d+)")),
    # Greenhouse — embedded job_app token style (slug embedded in query, fallback)
    ("greenhouse",
     re.compile(r"^boards\.greenhouse\.io/embed/job_(?:app|board)\?[^#]*for=(?P<slug>[^&]+)")),
    # Lever
    ("lever",
     re.compile(r"^jobs\.lever\.co/(?P<slug>[^/]+)/(?P<job_id>[0-9a-f-]{8,})")),
    # Ashby
    ("ashby",
     re.compile(r"^jobs\.ashbyhq\.com/(?P<slug>[^/]+)/(?P<job_id>[0-9a-f-]{8,})")),
    # SmartRecruiters
    ("smartrecruiters",
     re.compile(r"^jobs\.smartrecruiters\.com/(?P<slug>[^/]+)/(?P<job_id>[0-9-a-zA-Z]+)")),
    # Workday — slug is the tenant subdomain (e.g., "servicetitan" from
    # servicetitan.wd1.myworkdayjobs.com). Job ID is the trailing requisition
    # token after the final underscore in the path, typically "JR123456",
    # "R230696-2", or similar. Pattern matches by anchoring to the underscore
    # before the req ID, since the title segment uses double-dashes and isn't
    # the canonical identifier.
    ("workday",
     re.compile(
         r"^(?P<slug>[^.]+)\.wd\d+\.myworkdayjobs\.com/"
         r".*?_(?P<job_id>[A-Z][A-Za-z0-9-]*)/?$"
     )),
    # Welcome to the Jungle — opaque hash, no company slug in URL
    ("wttj",
     re.compile(r"^app\.welcometothejungle\.com/jobs/(?P<job_id>[A-Za-z0-9_-]+)")),
    # WTTJ company page (not a specific job)
    ("wttj",
     re.compile(r"^app\.welcometothejungle\.com/companies/(?P<slug>[^/]+)")),
]


# Domains we recognize but are explicitly aggregator/board roots, not specific
# job postings. Returning these as-classified would let bad URLs through, so we
# mark them url_type="generic" and skip the corpus_append step downstream.
_GENERIC_HOSTS = {
    "boards.greenhouse.io",            # board root with no /jobs/[id]
    "job-boards.greenhouse.io",
    "jobs.lever.co",
    "jobs.ashbyhq.com",
    "jobs.smartrecruiters.com",
    "app.welcometothejungle.com",
}


def classify_url(url: str) -> dict:
    """
    Parse a job-posting URL and return its ATS, company slug, and job ID.

    Returns dict with keys:
        ats:      one of {"greenhouse", "lever", "ashby", "workday",
                          "smartrecruiters", "wttj", "unknown"}
        slug:     company slug as it appears in the URL, or None if not
                  extractable (WTTJ job pages, malformed URLs)
        job_id:   job-specific ID, or None if not present (board roots)
        url_type: "job" if URL points to a specific job, "generic" if it
                  points to a board/company root, "unrecognized" otherwise
    """
    if not url or not isinstance(url, str):
        return {"ats": "unknown", "slug": None, "job_id": None, "url_type": "unrecognized"}

    parsed = urlparse(url.strip())
    host = (parsed.netloc or "").lower()
    # Reconstruct host+path for matching (drops scheme, query, fragment)
    target = host + parsed.path
    # Some boards put real path under query (e.g., embed token); preserve those:
    if parsed.query:
        target_with_q = target + "?" + parsed.query
    else:
        target_with_q = target

    for ats, pat in _PATTERNS:
        m = pat.match(target) or pat.match(target_with_q)
        if m:
            d = m.groupdict()
            return {
                "ats": ats,
                "slug": _normalize_slug(d.get("slug")),
                "job_id": d.get("job_id"),
                "url_type": "job" if d.get("job_id") else "generic",
            }

    # No pattern matched. Classify as generic if it's a known board host
    # without a specific job path.
    if host in _GENERIC_HOSTS:
        return {"ats": _ats_from_host(host), "slug": None, "job_id": None, "url_type": "generic"}

    return {"ats": "unknown", "slug": None, "job_id": None, "url_type": "unrecognized"}


def _normalize_slug(slug: Optional[str]) -> Optional[str]:
    """
    Normalize slugs to lowercase. Companies in the corpus use lowercase
    slugs (e.g., "rescale", "the-flex"), but URLs sometimes have mixed
    case ("Delphina", "FannieMae", "The-Flex"). Lowercase makes dedup
    against companies.json reliable.
    """
    if slug is None:
        return None
    return slug.lower()


def _ats_from_host(host: str) -> str:
    if "greenhouse" in host:
        return "greenhouse"
    if "lever" in host:
        return "lever"
    if "ashby" in host:
        return "ashby"
    if "myworkdayjobs" in host:
        return "workday"
    if "smartrecruiters" in host:
        return "smartrecruiters"
    if "welcometothejungle" in host:
        return "wttj"
    return "unknown"


# ---------------------------------------------------------------------------
# Self-tests — run with: python3 classify_url.py --test
# ---------------------------------------------------------------------------
_SELF_TESTS = [
    # Greenhouse classic
    ("https://boards.greenhouse.io/capellaspace/jobs/4738426004",
     {"ats": "greenhouse", "slug": "capellaspace", "job_id": "4738426004", "url_type": "job"}),
    # Greenhouse newer "job-boards"
    ("https://job-boards.greenhouse.io/remotecom/jobs/7681691003",
     {"ats": "greenhouse", "slug": "remotecom", "job_id": "7681691003", "url_type": "job"}),
    # Greenhouse with query string
    ("https://www.coinbase.com/careers/positions/7298274?gh_jid=7298274",
     {"ats": "unknown", "slug": None, "job_id": None, "url_type": "unrecognized"}),  # external host wraps gh
    # Lever
    ("https://jobs.lever.co/yuno/12b94079-5efe-4102-96e7-60d8850d0517",
     {"ats": "lever", "slug": "yuno", "job_id": "12b94079-5efe-4102-96e7-60d8850d0517", "url_type": "job"}),
    # Lever with /apply suffix
    ("https://jobs.lever.co/dlocal/752f72b4-fdc7-4bd5-9a53-a7f8668e7588/apply",
     {"ats": "lever", "slug": "dlocal", "job_id": "752f72b4-fdc7-4bd5-9a53-a7f8668e7588", "url_type": "job"}),
    # Ashby with mixed-case slug — should be lowercased
    ("https://jobs.ashbyhq.com/Delphina/ac77d59f-5182-47f7-9160-e39d332740b8",
     {"ats": "ashby", "slug": "delphina", "job_id": "ac77d59f-5182-47f7-9160-e39d332740b8", "url_type": "job"}),
    # Ashby with /application suffix
    ("https://jobs.ashbyhq.com/rescale/1598f382-54da-40fe-9946-8bac2fad8514/application",
     {"ats": "ashby", "slug": "rescale", "job_id": "1598f382-54da-40fe-9946-8bac2fad8514", "url_type": "job"}),
    # Ashby with mixed-case "The-Flex"
    ("https://jobs.ashbyhq.com/The-Flex/8a60fd2c-73fb-4cad-ba5a-587bb09c63a9/application",
     {"ats": "ashby", "slug": "the-flex", "job_id": "8a60fd2c-73fb-4cad-ba5a-587bb09c63a9", "url_type": "job"}),
    # Workday — slug from tenant subdomain
    ("https://servicetitan.wd1.myworkdayjobs.com/ServiceTitan/job/US-Remote/Director--Legal-Operations--Chief-of-Staff-_JR112954",
     {"ats": "workday", "slug": "servicetitan", "job_id": "JR112954", "url_type": "job"}),
    # Workday with multi-segment subdomain (Capital One)
    ("https://capitalone.wd12.myworkdayjobs.com/en-US/Capital_One/job/Manager--Chief-of-Staff---Capital-One-Software--Remote-_R230696-2",
     {"ats": "workday", "slug": "capitalone", "job_id": "R230696-2", "url_type": "job"}),
    # SmartRecruiters
    ("https://jobs.smartrecruiters.com/FannieMae/743999742560361-internal-audit-chief-of-staff-director",
     {"ats": "smartrecruiters", "slug": "fanniemae", "job_id": "743999742560361-internal-audit-chief-of-staff-director", "url_type": "job"}),
    # WTTJ job page (no slug recoverable from URL alone)
    ("https://app.welcometothejungle.com/jobs/4v68lVGl",
     {"ats": "wttj", "slug": None, "job_id": "4v68lVGl", "url_type": "job"}),
    # WTTJ company page
    ("https://app.welcometothejungle.com/companies/Holded",
     {"ats": "wttj", "slug": "holded", "job_id": None, "url_type": "generic"}),
    # Greenhouse embedded board (token style, no specific job)
    ("https://boards.greenhouse.io/embed/job_board?for=openzeppelin",
     {"ats": "greenhouse", "slug": "openzeppelin", "job_id": None, "url_type": "generic"}),
    # Garbage
    ("not a url", {"ats": "unknown", "slug": None, "job_id": None, "url_type": "unrecognized"}),
    # Empty
    ("", {"ats": "unknown", "slug": None, "job_id": None, "url_type": "unrecognized"}),
]


def _run_self_tests() -> int:
    """Run the built-in test suite. Returns 0 on success, non-zero on failure."""
    failures = 0
    for i, (url, expected) in enumerate(_SELF_TESTS, 1):
        actual = classify_url(url)
        if actual != expected:
            failures += 1
            print(f"FAIL #{i}: {url}")
            print(f"  expected: {expected}")
            print(f"  actual:   {actual}")
        else:
            print(f"OK   #{i}: {url[:80]}")
    print(f"\n{len(_SELF_TESTS) - failures}/{len(_SELF_TESTS)} passed")
    return 0 if failures == 0 else 1


def _main_cli(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[1] == "--test":
        return _run_self_tests()
    if argv[1] == "--stdin":
        for line in sys.stdin:
            url = line.strip()
            if not url:
                continue
            print(json.dumps({"url": url, **classify_url(url)}))
        return 0
    # Single-URL mode
    print(json.dumps(classify_url(argv[1]), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main_cli(sys.argv))
