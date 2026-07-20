#!/usr/bin/env python3
"""
fetch_jds.py — v4 Phase 1, full JD text fetching.

No existing script to refactor from (checked the whole repo — the three
ats_api_checker.py variants and check_urls.py fetch job *listings*/ping
URLs for liveness, never full JD body text). Built fresh per
HANDOFF_ROADMAP_v4_Claude_Code.md §4 item 3.

requests first; falls back to Playwright headless Chromium for empty/short
bodies or known JS-rendered domains (Workday, Oracle Cloud/Taleo, Notion-
hosted career pages). Per-row status: success / closed_listing / http_error
/ empty / js_shell. JD text cached at jd_cache/{sha256[:16]}.txt so re-runs
don't re-fetch. Halts (non-zero exit) rather than silently degrading if the
batch success rate falls below 80%, per the roadmap's anti-hallucination
invariant — score.py (Phase 2) must never see a corpus where most rows
lack real JD text.

Usage:
    python3 JC3/fetch_jds.py                 # this week's verified candidates
    python3 JC3/fetch_jds.py <path-to-csv>    # explicit input
"""

import csv
import hashlib
import os
import re
import sys
import time

import requests
from bs4 import BeautifulSoup

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.dirname(SCRIPT_DIR)
JD_CACHE_DIR = os.path.join(BASE_PATH, "jd_cache")
os.makedirs(JD_CACHE_DIR, exist_ok=True)

TIMEOUT = 15
MIN_JD_LENGTH = 500  # matches score_jd_v4.md's own "insufficient_jd_text" floor
SUCCESS_RATE_FLOOR = 0.80

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Domains known to client-side render the JD body — requests/urllib see an
# empty shell. Route straight to Playwright rather than wasting a request.
JS_RENDERED_DOMAIN_PATTERNS = [
    r"myworkdayjobs\.com",
    r"\.wd\d+\.myworkday",
    r"oraclecloud\.com",
    r"taleo\.net",
    r"\.notion\.site",
]
_JS_DOMAIN_RE = re.compile("|".join(JS_RENDERED_DOMAIN_PATTERNS), re.IGNORECASE)

# Reused from health.py's closed-listing phrase list — same signal, same
# meaning, don't maintain two copies of what "closed" looks like.
sys.path.insert(0, SCRIPT_DIR)
from health import CLOSED_PHRASES  # noqa: E402

_CLOSED_RE = re.compile("|".join(re.escape(p) for p in CLOSED_PHRASES), re.IGNORECASE)


def _url_hash(url):
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]


def _extract_text_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [ln.strip() for ln in text.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def _is_js_rendered_domain(url):
    return bool(_JS_DOMAIN_RE.search(url))


def _fetch_via_requests(url):
    """Returns (text, http_status) or (None, status) on failure."""
    try:
        r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
    except Exception as e:
        return None, f"request_error: {str(e)[:80]}"
    if r.status_code != 200:
        return None, r.status_code
    return _extract_text_from_html(r.text), 200


_playwright_ctx = {"instance": None, "browser": None}


def _get_playwright_browser():
    """Lazily start one shared Playwright browser for the whole run instead
    of one per row — launching Chromium per-JD would be needlessly slow."""
    if _playwright_ctx["browser"] is None:
        from playwright.sync_api import sync_playwright
        _playwright_ctx["instance"] = sync_playwright().start()
        _playwright_ctx["browser"] = _playwright_ctx["instance"].chromium.launch()
    return _playwright_ctx["browser"]


def _close_playwright():
    if _playwright_ctx["browser"] is not None:
        _playwright_ctx["browser"].close()
        _playwright_ctx["instance"].stop()
        _playwright_ctx["browser"] = None
        _playwright_ctx["instance"] = None


def _fetch_via_playwright(url):
    try:
        browser = _get_playwright_browser()
        page = browser.new_page(user_agent=USER_AGENT)
        page.goto(url, timeout=TIMEOUT * 1000, wait_until="networkidle")
        text = page.inner_text("body")
        page.close()
        lines = [ln.strip() for ln in text.splitlines()]
        return "\n".join(ln for ln in lines if ln)
    except Exception as e:
        print(f"    playwright error: {str(e)[:100]}")
        return None


def fetch_jd(url):
    """
    Returns (status, jd_text, cache_path).
    status: success / closed_listing / http_error / empty / js_shell
    """
    cache_path = os.path.join(JD_CACHE_DIR, f"{_url_hash(url)}.txt")
    if os.path.exists(cache_path):
        with open(cache_path, encoding="utf-8") as f:
            cached = f.read()
        if len(cached) >= MIN_JD_LENGTH:
            return "success", cached, cache_path

    needs_js = _is_js_rendered_domain(url)
    text, http_result = (None, None) if needs_js else _fetch_via_requests(url)

    if not needs_js:
        if isinstance(http_result, int) and http_result != 200:
            if http_result == 404:
                return "http_error", None, None
            return "http_error", None, None
        if text and _CLOSED_RE.search(text):
            return "closed_listing", None, None
        if text and len(text) >= MIN_JD_LENGTH:
            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(text)
            return "success", text, cache_path
        # Empty/short body via requests — try Playwright before giving up.

    text = _fetch_via_playwright(url)
    if text is None:
        return ("js_shell" if needs_js else "empty"), None, None
    if _CLOSED_RE.search(text):
        return "closed_listing", None, None
    if len(text) < MIN_JD_LENGTH:
        return "empty", None, None

    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(text)
    return "success", text, cache_path


def _latest_verified_csv():
    latam_dir = os.path.join(BASE_PATH, "results", "joey", "LATAM")
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
    path = os.path.join(latam_dir, latest, f"verified_candidates_{date_str}.csv")
    return path if os.path.exists(path) else None


def run_fetch(verified_csv):
    with open(verified_csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys()) if rows else []

    for extra in ("jd_fetch_status", "jd_cache_path"):
        if extra not in fieldnames:
            fieldnames.append(extra)

    print(f"\n{'─'*70}")
    print(f"  fetch_jds.py — {len(rows)} candidates")
    print(f"{'─'*70}")

    status_counts = {}
    try:
        for i, row in enumerate(rows, 1):
            url = row.get("url", "").strip()
            status, _text, cache_path = fetch_jd(url)
            row["jd_fetch_status"] = status
            row["jd_cache_path"] = os.path.relpath(cache_path, BASE_PATH) if cache_path else ""
            status_counts[status] = status_counts.get(status, 0) + 1
            symbol = {"success": "✓", "closed_listing": "✗", "http_error": "!",
                      "empty": "⚠", "js_shell": "⚙"}.get(status, "?")
            print(f"  [{i:>3}/{len(rows)}] {symbol} {status:<15} "
                  f"{row.get('company_name','')[:28]:<28} — {row.get('title','')[:32]}")
            time.sleep(0.3)
    finally:
        _close_playwright()

    total = len(rows)
    success = status_counts.get("success", 0)
    success_rate = (success / total) if total else 0

    print(f"\n  Status breakdown: {status_counts}")
    print(f"  Success rate: {success_rate:.0%} ({success}/{total})")

    week_dir = os.path.dirname(verified_csv)
    date_str = os.path.basename(verified_csv).replace("verified_candidates_", "").replace(".csv", "")
    output_path = os.path.join(week_dir, f"fetched_candidates_{date_str}.csv")
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\n  Output: {output_path}")

    if success_rate < SUCCESS_RATE_FLOOR:
        print(f"\n  HALT: success rate {success_rate:.0%} is below the "
              f"{SUCCESS_RATE_FLOOR:.0%} floor (roadmap §4 item 3).")
        print("  Not degrading silently — investigate before running package.py/score.py.")
        return output_path, False

    return output_path, True


def main():
    args = sys.argv[1:]
    verified_csv = args[0] if args else _latest_verified_csv()
    if not verified_csv or not os.path.exists(verified_csv):
        print(f"No verified candidates CSV found (looked for: {verified_csv}). "
              f"Run discover.py then health.py first, or pass a path explicitly.")
        sys.exit(1)

    _output_path, ok = run_fetch(verified_csv)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
