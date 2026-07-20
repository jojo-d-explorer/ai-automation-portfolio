#!/usr/bin/env python3
"""
linkedin_daily_links.py — v4 Phase 3, Strategy Addendum §1.2.

Separate from JC3/linkedin_links.py deliberately — that script serves the
frozen v5.x friends track (roadmap §7: "do not modify anything under
searches/For_Others/"), and while it isn't itself under that path, it's
shared infrastructure their weekly runs depend on. Touching it risks their
pipeline for a Joey-only, LATAM-specific redesign. This is a new, separate
file instead.

Generates LinkedIn_Daily_Links.md: a 5 (role cluster) x 4 (geography)
matrix, one past-24h link per cell (f_TPR=r86400&sortBy=DD), plus a weekly
backstop version (r604800) — per addendum §1.2. No network calls; this is
pure URL construction, same "LinkedIn stays manual by design" principle
(addendum §1.4: no scraping, no automation against LinkedIn itself).

Role cluster boolean strings are built from config/joey_profile.yaml's
actual role_families keywords (reused, not reinvented) so the LinkedIn
matrix stays in sync with the ATS-sweep keyword vocabulary. geoId values
are the addendum's own resolved values (§1.1), used as given.

Usage:
    python3 JC3/linkedin_daily_links.py
"""

import os
import urllib.parse

import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.dirname(SCRIPT_DIR)
PROFILE_PATH = os.path.join(BASE_PATH, "config", "joey_profile.yaml")

GEO_IDS = {
    "Argentina": "100446943",
    "Mexico": "103323778",
    "Latin America (region)": "104514572",
}

# Addendum §1.2 — 5 role-cluster rows. Boolean strings pull the 3-4 most
# distinctive keywords per matching profile.yaml role_family, quoted and
# OR-joined, so this stays traceable to the same vocabulary discover.py
# actually matches against rather than diverging over time.
ROLE_CLUSTERS = {
    "Chief of Staff / Strategic Initiatives": [
        "chief of staff", "strategic initiatives", "head of strategy", "strategic operations",
    ],
    "Country Manager / General Manager / Market Entry": [
        "country manager", "general manager", "market entry", "international expansion",
    ],
    "Partnerships / Business Development (director+)": [
        "director of partnerships", "vp partnerships", "head of partnerships", "head of business development",
    ],
    "Strategy and Operations / Corporate Development": [
        "strategy and operations", "corporate development", "director of strategy and operations",
    ],
    "VC Platform / Operating Partner / Portfolio Operations": [
        "operating partner", "venture partner", "corporate development",
    ],
}


def _boolean_keywords(terms):
    quoted = " OR ".join(f'"{t}"' for t in terms)
    return f"({quoted})"


def _build_url(keywords, *, geo_id=None, remote=False, time_posted="r86400"):
    params = {
        "keywords": keywords,
        "f_TPR": time_posted,
        "f_E": "4,5,6",  # mid-senior, director, executive — addendum §1.1
        "sortBy": "DD",
    }
    if geo_id:
        params["geoId"] = geo_id
    if remote:
        params["f_WT"] = "2"
    return "https://www.linkedin.com/jobs/search/?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)


def _load_profile_role_families():
    if not os.path.exists(PROFILE_PATH):
        return {}
    with open(PROFILE_PATH) as f:
        profile = yaml.safe_load(f)
    return profile.get("role_families", {})


def build_matrix(time_posted="r86400"):
    """
    Returns a list of (role_cluster_name, geo_column_name, url) covering
    the 5x4 matrix: Argentina, Mexico, Latin America region (all f_WT=2
    per addendum — Joey's search is remote-first even within-country),
    and Remote-worldwide (LATAM/Latin America keywords + f_WT=2, no geoId).
    """
    rows = []
    for cluster_name, terms in ROLE_CLUSTERS.items():
        base_keywords = _boolean_keywords(terms)

        for geo_name, geo_id in GEO_IDS.items():
            url = _build_url(base_keywords, geo_id=geo_id, remote=True, time_posted=time_posted)
            rows.append((cluster_name, geo_name, url))

        remote_keywords = f'{base_keywords} AND ("LATAM" OR "Latin America")'
        url = _build_url(remote_keywords, remote=True, time_posted=time_posted)
        rows.append((cluster_name, "Remote-worldwide (LATAM keywords)", url))

    return rows


def write_matrix_md(path, title, matrix):
    with open(path, "w") as f:
        f.write(f"# {title}\n\n")
        f.write(f"{len(matrix)} links — 5 role clusters x 4 geographies. ")
        f.write("Sorted newest-first; most cells return zero to a handful of results.\n\n")
        current_cluster = None
        for cluster_name, geo_name, url in matrix:
            if cluster_name != current_cluster:
                f.write(f"\n## {cluster_name}\n\n")
                current_cluster = cluster_name
            f.write(f"- **{geo_name}**: {url}\n")


def main():
    role_families = _load_profile_role_families()
    if role_families:
        print(f"  (profile.yaml has {len(role_families)} role families available for reference; "
              f"this matrix uses its own {len(ROLE_CLUSTERS)}-cluster grouping per addendum §1.2)")

    daily_matrix = build_matrix(time_posted="r86400")
    weekly_matrix = build_matrix(time_posted="r604800")

    daily_path = os.path.join(BASE_PATH, "results", "joey", "LinkedIn_Daily_Links.md")
    weekly_path = os.path.join(BASE_PATH, "results", "joey", "LinkedIn_Weekly_Links.md")
    os.makedirs(os.path.dirname(daily_path), exist_ok=True)

    write_matrix_md(daily_path, "LinkedIn Daily Links (past 24h)", daily_matrix)
    write_matrix_md(weekly_path, "LinkedIn Weekly Links (past week, backstop)", weekly_matrix)

    print(f"\n{'='*70}")
    print(f"  linkedin_daily_links.py — {len(daily_matrix)} daily links, {len(weekly_matrix)} weekly links")
    print(f"  Daily:  {daily_path}")
    print(f"  Weekly: {weekly_path}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
