#!/usr/bin/env python3
"""
Append newly-discovered companies to companies.json as stub entries.

v2.3.1 — adds:
  - Disqualifier filter (reads scripts/disqualifiers.json)
  - Proposed-additions log (proposed_corpus_additions_<week>.csv)
  - Disqualified log (disqualified_<week>.csv)

Reads classified job URLs (from candidates.csv produced by Stage 1 discovery
or piped on stdin), dedups against the existing corpus by slug, runs each
candidate through the disqualifier filter, and appends stub records for
previously-unseen, non-disqualified slugs.

USAGE
    # Dry run — print proposed stubs, don't modify corpus
    python3 corpus_append.py --candidates candidates.csv --dry-run

    # Real run — modify companies.json in place (creates timestamped backup)
    python3 corpus_append.py --candidates candidates.csv

    # From stdin (one URL per line). Note: snippet-based disqualification
    # cannot run from stdin since it has no snippet column; only slug/name
    # checks apply.
    cat urls.txt | python3 corpus_append.py --stdin

    # Specify alternate corpus path
    python3 corpus_append.py --candidates c.csv --corpus path/to/companies.json

    # Specify alternate disqualifier config
    python3 corpus_append.py --candidates c.csv \
            --disqualifiers path/to/disqualifiers.json

    # Skip the disqualifier filter entirely (legacy v2.3 behavior)
    python3 corpus_append.py --candidates c.csv --no-disqualify

EXIT CODES
    0  success (or no new companies to add)
    1  malformed input
    2  corpus file not writable
    3  disqualifiers file missing or malformed (when filter active)
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import shutil
from datetime import date
from pathlib import Path

# Allow running from anywhere by being explicit about script location
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from classify_url import classify_url  # noqa: E402


def _today() -> str:
    return date.today().strftime("%Y-%m-%d")


def _humanize_slug(slug: str) -> str:
    """
    Convert a URL slug into a human-readable name guess.

    Examples:
      "rescale"        -> "Rescale"
      "the-flex"       -> "The Flex"
      "loftorbital"    -> "Loftorbital"      (best-effort; user can rename)
    """
    if not slug:
        return ""
    parts = slug.replace("_", "-").split("-")
    return " ".join(p.capitalize() for p in parts if p)


def _build_stub(ats: str, slug: str, name: str, today: str, source_note: str) -> dict:
    """Construct a corpus stub entry for a newly-discovered company."""
    return {
        "slug": slug,
        "name": name or _humanize_slug(slug),
        "ats": ats,
        "sector": ["unknown"],
        "stage": "unknown",
        "geography_hq": "unknown",
        "remote_posture": "unknown",
        "us_investor_signal": "needs_verification",
        "priority_tier": None,
        "status": "pending_review",
        "notes": source_note,
        "source": "auto_discovery_v2.3",
        "added": today,
        "schema_origin": "v2.3",
    }


def _read_urls_from_csv(path: Path) -> list[dict]:
    """
    Pull job URLs and surrounding context from a candidates.csv (Stage 1 output).

    Returns a list of dicts with: url, snippet (if present), company (if present),
    job_title (if present). The snippet and company are passed through to the
    disqualifier filter for richer matching.
    """
    rows: list[dict] = []
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Find the URL column tolerantly
        url_field = None
        for fld in reader.fieldnames or []:
            if fld and fld.lower() in ("url", "link", "job_url"):
                url_field = fld
                break
        if url_field is None:
            print(f"ERROR: no URL column found in {path}. "
                  f"Expected one of: URL, url, link, job_url. Got: {reader.fieldnames}",
                  file=sys.stderr)
            sys.exit(1)
        # Find optional context columns
        snip_field = next(
            (f for f in (reader.fieldnames or []) if f and f.lower() in ("snippet", "description")),
            None
        )
        company_field = next(
            (f for f in (reader.fieldnames or []) if f and f.lower() in ("company", "company_name")),
            None
        )
        title_field = next(
            (f for f in (reader.fieldnames or []) if f and f.lower() in ("job_title", "title", "role")),
            None
        )
        for row in reader:
            u = (row.get(url_field) or "").strip()
            if not u:
                continue
            rows.append({
                "url": u,
                "snippet": (row.get(snip_field) or "").strip() if snip_field else "",
                "company": (row.get(company_field) or "").strip() if company_field else "",
                "job_title": (row.get(title_field) or "").strip() if title_field else "",
            })
    return rows


# ---------------------------------------------------------------------------
# Disqualifier filter (v2.3.1)
# ---------------------------------------------------------------------------

def _load_disqualifiers(path: Path) -> dict:
    """Load and validate the disqualifier config."""
    if not path.exists():
        print(f"ERROR: disqualifiers config not found at {path}. "
              f"Either create it or pass --no-disqualify.", file=sys.stderr)
        sys.exit(3)
    try:
        with open(path, encoding="utf-8") as f:
            cfg = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: disqualifiers config at {path} is not valid JSON: {e}",
              file=sys.stderr)
        sys.exit(3)
    # Sanity-check expected sections
    for section in ("slug_blocklist", "name_keyword_blocklist", "sector_keyword_clusters"):
        if section not in cfg:
            print(f"WARNING: disqualifiers config missing section '{section}' — "
                  f"that filter will be skipped.", file=sys.stderr)
    return cfg


def _check_disqualified(
    slug: str,
    name: str,
    snippet: str,
    cfg: dict,
) -> tuple[bool, str, list[str]]:
    """
    Check a single candidate against the disqualifier rules.

    Returns (is_disqualified, rule_matched, matched_keywords).
    rule_matched is "" if not disqualified.
    """
    slug_l = (slug or "").lower()
    name_l = (name or "").lower()
    snippet_l = (snippet or "").lower()
    haystack = f"{name_l} {snippet_l}".strip()

    # Rule 1: slug exact-match blocklist
    for blocked_slug in cfg.get("slug_blocklist", []):
        if slug_l == blocked_slug.lower():
            return (True, "slug_blocklist", [blocked_slug])

    # Rule 2: name keyword substring blocklist
    for kw in cfg.get("name_keyword_blocklist", []):
        if kw.lower() in name_l:
            return (True, "name_keyword_blocklist", [kw])

    # Rule 3: sector clusters — 2+ keywords within a single cluster
    for cluster_name, cluster_data in cfg.get("sector_keyword_clusters", {}).items():
        keywords = cluster_data.get("keywords", []) if isinstance(cluster_data, dict) else []
        hits = [kw for kw in keywords if kw.lower() in haystack]
        if len(hits) >= 2:
            return (True, f"sector_cluster:{cluster_name}", hits)

    return (False, "", [])


# ---------------------------------------------------------------------------
# Main append logic
# ---------------------------------------------------------------------------

def append_corpus(
    candidates: list[dict],
    corpus_path: Path,
    *,
    dry_run: bool = False,
    today: str | None = None,
    disqualifiers_cfg: dict | None = None,
    propose_log_path: Path | None = None,
    disqualified_log_path: Path | None = None,
) -> dict:
    """
    Append stubs for unseen, non-disqualified slugs. Returns a summary dict.

    candidates is a list of dicts with keys: url, snippet, company, job_title.
    """
    today = today or _today()
    summary = {
        "total_urls": len(candidates),
        "classified_jobs": 0,
        "skipped_unrecognized": 0,
        "skipped_generic": 0,
        "skipped_no_slug": 0,
        "already_in_corpus": 0,
        "disqualified": 0,
        "new_stubs": 0,
        "stubs_added": [],
        "disqualified_entries": [],
    }

    # Load existing corpus
    if not corpus_path.exists():
        print(f"ERROR: corpus not found at {corpus_path}", file=sys.stderr)
        sys.exit(2)
    with open(corpus_path, encoding="utf-8") as f:
        corpus = json.load(f)
    existing_slugs = {c["slug"].lower() for c in corpus["companies"]}

    seen_in_batch: set[str] = set()

    for cand in candidates:
        url = cand["url"]
        info = classify_url(url)
        if info["url_type"] == "unrecognized":
            summary["skipped_unrecognized"] += 1
            continue
        if info["url_type"] == "generic":
            summary["skipped_generic"] += 1
            continue
        # url_type == "job"
        summary["classified_jobs"] += 1
        slug = info.get("slug")
        if not slug:
            summary["skipped_no_slug"] += 1
            continue
        slug = slug.lower()
        if slug in existing_slugs:
            summary["already_in_corpus"] += 1
            continue
        if slug in seen_in_batch:
            continue
        seen_in_batch.add(slug)

        candidate_name = cand.get("company") or _humanize_slug(slug)

        # Apply disqualifier filter (v2.3.1) — skip if no config provided
        if disqualifiers_cfg is not None:
            disq, rule, hits = _check_disqualified(
                slug=slug,
                name=candidate_name,
                snippet=cand.get("snippet", ""),
                cfg=disqualifiers_cfg,
            )
            if disq:
                summary["disqualified"] += 1
                summary["disqualified_entries"].append({
                    "slug": slug,
                    "name": candidate_name,
                    "ats": info["ats"],
                    "rejected_by_rule": rule,
                    "matched_keywords": "; ".join(hits),
                    "snippet": (cand.get("snippet", "") or "")[:280],
                    "url": url,
                })
                continue

        stub = _build_stub(
            ats=info["ats"],
            slug=slug,
            name=candidate_name,
            today=today,
            source_note=f"Auto-discovered via Google search {today}.",
        )
        summary["stubs_added"].append(stub)
        summary["new_stubs"] += 1

    # Write proposed-additions log (always, even on dry-run)
    if propose_log_path is not None:
        propose_log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(propose_log_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["slug", "name", "ats", "added_date", "source"])
            w.writeheader()
            for s in summary["stubs_added"]:
                w.writerow({
                    "slug": s["slug"],
                    "name": s["name"],
                    "ats": s["ats"],
                    "added_date": s["added"],
                    "source": s["source"],
                })

    # Write disqualified log (always when disqualifier active)
    if disqualified_log_path is not None and disqualifiers_cfg is not None:
        disqualified_log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(disqualified_log_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=[
                "slug", "name", "ats", "rejected_by_rule",
                "matched_keywords", "snippet", "url"
            ])
            w.writeheader()
            for d in summary["disqualified_entries"]:
                w.writerow(d)

    # Write corpus update unless dry-run
    if not dry_run and summary["new_stubs"] > 0:
        # Backup name format: <corpus>.bak.<date>.json (e.g., companies.json.bak.2026-04-27.json)
        backup = corpus_path.parent / f"{corpus_path.name}.bak.{today}.json"
        shutil.copy(corpus_path, backup)
        corpus["companies"].extend(summary["stubs_added"])
        if "_meta" in corpus:
            corpus["_meta"]["last_updated"] = today
            corpus["_meta"]["total_companies"] = len(corpus["companies"])
            corpus["_meta"]["active"] = sum(
                1 for c in corpus["companies"] if c.get("status") == "active"
            )
            corpus["_meta"]["manual_review"] = sum(
                1 for c in corpus["companies"] if c.get("status") == "manual-review"
            )
            corpus["_meta"]["pending_review"] = sum(
                1 for c in corpus["companies"] if c.get("status") == "pending_review"
            )
            corpus["_meta"]["from_v2_3_auto"] = sum(
                1 for c in corpus["companies"] if c.get("source") == "auto_discovery_v2.3"
            )
            ats_breakdown: dict[str, int] = {}
            for c in corpus["companies"]:
                a = c.get("ats", "unknown")
                ats_breakdown[a] = ats_breakdown.get(a, 0) + 1
            corpus["_meta"]["ats_breakdown"] = ats_breakdown
        with open(corpus_path, "w", encoding="utf-8") as f:
            json.dump(corpus, f, indent=2, ensure_ascii=False)
            f.write("\n")
        summary["backup_written"] = str(backup)

    return summary


def _resolve_log_dir(candidates_path: Path | None) -> Path | None:
    """
    Place the log files alongside the candidates CSV (i.e., the same
    Week_of_<date> folder Stage 1 wrote into).
    """
    if candidates_path is None:
        return None
    return candidates_path.parent


def _main():
    ap = argparse.ArgumentParser(
        description="Append newly-discovered companies to companies.json as stubs.",
    )
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--candidates", type=Path,
                     help="Path to candidates.csv (Stage 1 output)")
    src.add_argument("--stdin", action="store_true",
                     help="Read URLs from stdin (one per line)")
    ap.add_argument("--corpus", type=Path,
                    default=_HERE.parent / "companies.json",
                    help="Path to companies.json (default: ../companies.json)")
    ap.add_argument("--disqualifiers", type=Path,
                    default=_HERE / "disqualifiers.json",
                    help="Path to disqualifiers.json (default: scripts/disqualifiers.json)")
    ap.add_argument("--no-disqualify", action="store_true",
                    help="Skip the disqualifier filter (legacy v2.3 behavior)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print proposed stubs without modifying corpus")
    args = ap.parse_args()

    # Build candidate list with context where available
    if args.candidates:
        candidates = _read_urls_from_csv(args.candidates)
    else:
        candidates = [
            {"url": line.strip(), "snippet": "", "company": "", "job_title": ""}
            for line in sys.stdin
            if line.strip()
        ]

    # Load disqualifier config (unless --no-disqualify)
    cfg: dict | None = None
    if not args.no_disqualify:
        cfg = _load_disqualifiers(args.disqualifiers)

    # Resolve log paths (next to the candidates file)
    log_dir = _resolve_log_dir(args.candidates)
    propose_log = (log_dir / f"proposed_corpus_additions_{_today()}.csv") if log_dir else None
    disq_log = (log_dir / f"disqualified_{_today()}.csv") if log_dir else None

    summary = append_corpus(
        candidates,
        args.corpus,
        dry_run=args.dry_run,
        disqualifiers_cfg=cfg,
        propose_log_path=propose_log,
        disqualified_log_path=disq_log,
    )

    # Pretty-print summary
    print(f"\n=== corpus_append summary ({_today()}) ===")
    print(f"  URLs processed:           {summary['total_urls']}")
    print(f"  Classified as job posts:  {summary['classified_jobs']}")
    print(f"  Skipped (unrecognized):   {summary['skipped_unrecognized']}")
    print(f"  Skipped (generic root):   {summary['skipped_generic']}")
    print(f"  Skipped (no slug — WTTJ): {summary['skipped_no_slug']}")
    print(f"  Already in corpus:        {summary['already_in_corpus']}")
    if cfg is not None:
        print(f"  Disqualified at append:   {summary['disqualified']}")
    print(f"  New stubs:                {summary['new_stubs']}")

    if summary["stubs_added"]:
        print("\nNew companies queued for corpus:")
        for s in summary["stubs_added"]:
            print(f"  + {s['slug']:30}  ats={s['ats']:15}  name={s['name']}")

    if summary["disqualified_entries"]:
        print("\nDisqualified at append (review the log to tune rules):")
        for d in summary["disqualified_entries"][:15]:
            print(f"  x {d['slug']:30}  rule={d['rejected_by_rule']:30}  hits={d['matched_keywords']}")
        if len(summary["disqualified_entries"]) > 15:
            print(f"  ... and {len(summary['disqualified_entries']) - 15} more")

    if propose_log:
        print(f"\nProposed-additions log: {propose_log}")
    if disq_log and cfg is not None:
        print(f"Disqualified log:       {disq_log}")

    if args.dry_run and summary["new_stubs"] > 0:
        print(f"\n(dry-run — corpus not modified. Re-run without --dry-run to apply.)")
    elif summary["new_stubs"] > 0:
        print(f"\nBackup written: {summary.get('backup_written')}")
        print(f"Corpus updated: {args.corpus}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
