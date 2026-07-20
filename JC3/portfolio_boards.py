#!/usr/bin/env python3
"""
portfolio_boards.py — v4 Phase 3, VC portfolio job boards as discovery
sources (Strategy Addendum §3).

No existing code to refactor from — new build. The addendum listed 13
funds from memory; per its own explicit warning ("do not trust remembered
URLs"), every one was verified for real before being hardcoded here. Only
5 of 13 turned out to have a real, findable board:

  CONFIRMED (built in below):
    Kaszek, QED Investors, Endeavor — consider.com/boards/vc/{slug}/jobs
    a16z — jobs.a16z.com (same Consider platform, white-labeled domain)
    General Catalyst — jobs.generalcatalyst.com (Getro platform)

  NOT FOUND despite real search + multiple slug variants — not hardcoded,
  do not guess further without new information:
    monashees, NXTP, Valor Capital Group, Atlantico, Nazca,
    SoftBank Latin America, Founders Fund (only appears inside a
    third-party Getro aggregator, not its own board)
    ALLVP — notable finding: allvp.mx now redirects to hi.vc ("Hi
    Ventures"); the fund appears to have rebranded. No board found on
    either domain.

Getro/Consider both require a real browser session — their JSON APIs
return {"code": "EXPIRED"} to a bare requests.get(), even with a Referer
header. This isn't optional-header laziness; it's session-token gating.
Playwright loads the real page (establishing a real session naturally),
then replays the search-jobs POST from inside that authenticated context
with the max batch size, same pattern as fetch_jds.py's JS-rendered-page
fallback but going one step further than just reading what the page
itself fetched.

Consider platform (Kaszek/QED/Endeavor/a16z): full job-level extraction
via the /api-boards/search-jobs response — real title, company, location,
remote/hybrid flags, region tags (Consider already tags "Latin America"
natively), and critically `applyUrl`, the actual underlying ATS URL
(e.g. a real job-boards.greenhouse.io link) — these rows plug directly
into the existing pipeline the same way discover.py's primary/secondary
rows do.

Batch size, not true pagination: the endpoint's own offset/page/from
parameters are all no-ops (tried four variants; results come back
relevance-scored, not stably ordered, so "page 2" isn't coherent here
anyway) — but it does accept size up to a hard server-enforced cap of
1000 in one call (confirmed via its own 422 validation message). That's
exhaustive for Kaszek (912 jobs) and Endeavor (currently 0), and a large
but not complete sample for QED (~1463) and a16z (~15,455).

Getro platform (General Catalyst): only company-list extraction
(organizations/all) was mapped in the time available — the actual
jobs-search endpoint wasn't isolated. This still serves the addendum's
"double duty: direct job source and corpus growth engine" half-way —
companies feed corpus growth, just not direct job rows this phase.

Usage:
    python3 JC3/portfolio_boards.py
"""

import os
import re
import sys
from datetime import datetime, timedelta

from playwright.sync_api import sync_playwright

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.dirname(SCRIPT_DIR)
COMPANIES_JSON = os.path.join(BASE_PATH, "searches", "joey", "companies.json")

sys.path.insert(0, SCRIPT_DIR)
from discover import ROLE_FAMILIES, ALL_KEYWORDS, KEYWORD_TO_FAMILY, passes_seniority_gate, match_role  # noqa: E402

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# CONFIRMED boards only — see module docstring for what was checked and
# ruled out. provenance value per addendum §3 integration rule 4:
# portfolio_board:{fund}
#
# board_id is Consider's internal identifier, captured from each board's
# real initial request — do NOT assume it matches the URL slug. It usually
# does (kaszek, qed-investors, endeavor all confirmed identical to their
# slug) but a16z's is "andreessen-horowitz", found only by inspecting its
# actual outgoing request. Guessing this field wrong doesn't error loudly;
# it silently 500s ("Cannot wrap undefined with r.expr()") or, worse,
# could silently return the wrong board's jobs — always verify per-board.
CONSIDER_BOARDS = {
    "kaszek": {"url": "https://consider.com/boards/vc/kaszek/jobs", "board_id": "kaszek"},
    "qed-investors": {"url": "https://consider.com/boards/vc/qed-investors/jobs", "board_id": "qed-investors"},
    "endeavor": {"url": "https://consider.com/boards/vc/endeavor/jobs", "board_id": "endeavor"},
    "a16z": {"url": "https://jobs.a16z.com", "board_id": "andreessen-horowitz"},
}

# Consider's search-jobs endpoint has no working offset/page/from parameter
# — tried all three plus pageSize; every variant either got silently
# ignored (same first result each time) or 422'd. Results appear to be
# relevance-scored, not stable-ordered, so "page 2" isn't a coherent
# concept here anyway. The endpoint does enforce a hard server-side cap of
# 1000 (confirmed via its own validation error), so requesting the max in
# one call is the actual ceiling, not partial pagination — for Kaszek (912
# jobs) and Endeavor (0) this is exhaustive; for QED (~1463) and a16z
# (~15,455) it's a large, but not complete, sample.
MAX_BATCH_SIZE = 1000

GETRO_COMPANY_LIST_BOARDS = {
    "general-catalyst": "https://jobs.generalcatalyst.com/jobs",
}


def _week_paths():
    today = datetime.now()
    monday = today - timedelta(days=today.weekday())
    week_date = monday.strftime("%Y-%m-%d")
    week_dir = os.path.join(BASE_PATH, "results", "joey", "LATAM", f"Week_of_{week_date}")
    os.makedirs(week_dir, exist_ok=True)
    return week_date, week_dir


def fetch_consider_jobs(board_url, board_id, browser):
    """Load a Consider-hosted board for real (establishing the session its
    API requires — see module docstring on session-gating), then replay
    the search-jobs POST from inside that authenticated page context with
    the max batch size, instead of settling for whatever the page's own
    initial 15-job load happened to fetch. Relative URL so this works
    identically whether the board lives on consider.com or a white-labeled
    domain like jobs.a16z.com — it resolves against the page's own origin."""
    page = browser.new_page(user_agent=UA)
    try:
        page.goto(board_url, timeout=30000, wait_until="networkidle")
        page.wait_for_timeout(1000)
        result = page.evaluate(
            """
            async ({boardId, size}) => {
                const resp = await fetch('/api-boards/search-jobs', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    credentials: 'include',
                    body: JSON.stringify({
                        meta: {size: size},
                        board: {id: boardId, isParent: true},
                        query: {promoteFeatured: true}
                    })
                });
                const data = await resp.json();
                return {status: resp.status, jobs: data.jobs || [], errors: data.errors || []};
            }
            """,
            {"boardId": board_id, "size": MAX_BATCH_SIZE},
        )
        if result["errors"]:
            print(f"    API errors for {board_id}: {result['errors']}")
        return result["jobs"]
    except Exception as e:
        print(f"    error loading {board_url}: {e}")
        return []
    finally:
        page.close()


def fetch_getro_companies(board_url, browser):
    """Company-list-only extraction — see module docstring. Returns
    [{name, slug}, ...]."""
    captured = {}

    def handle(response):
        if "organizations/all" in response.url:
            try:
                captured["data"] = response.json()
            except Exception:
                pass

    page = browser.new_page(user_agent=UA)
    page.on("response", handle)
    try:
        page.goto(board_url, timeout=30000, wait_until="networkidle")
        page.wait_for_timeout(1500)
    except Exception as e:
        print(f"    error loading {board_url}: {e}")
    finally:
        page.close()

    return captured.get("data", {}).get("items", [])


def normalize_consider_job(job, fund_slug):
    return {
        "source": f"portfolio_board:{fund_slug}",
        "company_slug": job.get("companySlug", ""),
        "company_name": job.get("companyName", ""),
        "title": job.get("title", ""),
        "location": ", ".join(job.get("locations", [])) or ("Remote" if job.get("remote") else ""),
        "url": job.get("applyUrl") or job.get("url", ""),
        "updated": job.get("timeStamp", ""),
        "ats": "",  # resolved downstream from the applyUrl's domain, not asserted here
    }


def enrich_and_filter(row, stats):
    family = match_role(row["title"])
    if not family:
        return None
    if not passes_seniority_gate(row["title"]):
        stats["rejected_seniority"] += 1
        return None
    row["role_family"] = family
    return row


def run_portfolio_boards():
    week_date, week_dir = _week_paths()
    stats = {"rejected_seniority": 0, "matches": 0, "companies_seen": set()}
    all_rows = []

    with sync_playwright() as p:
        browser = p.chromium.launch()

        print(f"\n{'─'*70}")
        print(f"  portfolio_boards.py — Consider boards (job-level)")
        print(f"{'─'*70}")
        for fund_slug, board in CONSIDER_BOARDS.items():
            jobs = fetch_consider_jobs(board["url"], board["board_id"], browser)
            print(f"  {fund_slug:20} {len(jobs)} jobs (max batch, capped at {MAX_BATCH_SIZE})")
            for job in jobs:
                row = normalize_consider_job(job, fund_slug)
                stats["companies_seen"].add(row["company_slug"])
                enriched = enrich_and_filter(row, stats)
                if enriched:
                    all_rows.append(enriched)
                    stats["matches"] += 1

        print(f"\n{'─'*70}")
        print(f"  portfolio_boards.py — Getro boards (company-list only)")
        print(f"{'─'*70}")
        getro_companies = []
        for fund_slug, url in GETRO_COMPANY_LIST_BOARDS.items():
            companies = fetch_getro_companies(url, browser)
            print(f"  {fund_slug:20} {len(companies)} portfolio companies")
            getro_companies.extend(companies)

        browser.close()

    print(f"\n{'='*70}")
    print(f"  Consider: {len(all_rows)} role-family-matched jobs across "
          f"{len(stats['companies_seen'])} companies seen")
    print(f"  Getro: {len(getro_companies)} companies discovered (no job-level data this phase)")
    print(f"  Rejected on seniority: {stats['rejected_seniority']}")
    print(f"{'='*70}\n")

    return all_rows, getro_companies, week_dir, week_date


if __name__ == "__main__":
    run_portfolio_boards()
