#!/usr/bin/env python3
"""
run.py — v4 Phase 1 orchestrator.

Target command from HANDOFF_ROADMAP_v4_Claude_Code.md §2:
    python3 JC3/run.py --user joey --variant latam

Default (full weekly run): discover -> diff -> health -> fetch_jds -> package.
--fresh-only (daily sweep, Strategy Addendum §2): discover -> diff -> health only,
no JD fetch, no scoring, no Master update. Costs ~2-3 minutes, no model tokens.

Scoring (score.py, Phase 2) doesn't exist yet — this orchestrator completes
after package.py and reports that plainly rather than pretending a pause-
for-scoring step exists. Wire it in once Phase 2 is built.

Usage:
    python3 JC3/run.py --user joey --variant latam
    python3 JC3/run.py --user joey --variant latam --fresh-only
"""

import argparse
import sys

import discover
import diff as diff_module
import health
import fetch_jds
import package


SUPPORTED_USERS = {"joey"}
SUPPORTED_VARIANTS = {"latam"}  # RemoteGlobal is a documented future Phase 4 variant, not built yet


def main():
    ap = argparse.ArgumentParser(description="v4 job intelligence pipeline orchestrator")
    ap.add_argument("--user", required=True)
    ap.add_argument("--variant", required=True)
    ap.add_argument("--fresh-only", action="store_true",
                     help="discover + diff + health only (daily sweep, no JD fetch/scoring/Master update)")
    args = ap.parse_args()

    if args.user not in SUPPORTED_USERS:
        print(f"ERROR: --user {args.user!r} not supported. This pipeline is Joey-only "
              f"(roadmap §7: 'Friends are frozen on v5.x'). Supported: {SUPPORTED_USERS}")
        sys.exit(1)
    if args.variant not in SUPPORTED_VARIANTS:
        print(f"ERROR: --variant {args.variant!r} not supported yet. "
              f"RemoteGlobal is documented (roadmap §7) but not built. Supported: {SUPPORTED_VARIANTS}")
        sys.exit(1)

    mode = "fresh-only (daily sweep)" if args.fresh_only else "full weekly run"
    print(f"\n{'='*70}")
    print(f"  JC3/run.py — user={args.user} variant={args.variant} mode={mode}")
    print(f"{'='*70}")

    print("\n[1/5] discover.py")
    candidates_csv = discover.main()

    print("\n[2/5] diff.py")
    diff_module.run_diff(candidates_csv)

    print("\n[3/5] health.py")
    verified, _dropped = health.run_health_check(candidates_csv)

    if args.fresh_only:
        print(f"\n{'='*70}")
        print(f"  Fresh sweep complete. {len(verified)} verified candidates.")
        print(f"  Run without --fresh-only for the full weekly pipeline (fetch JDs, package).")
        print(f"{'='*70}\n")
        return

    print("\n[4/5] fetch_jds.py")
    week_dir = candidates_csv.rsplit("/", 1)[0]
    week_date = candidates_csv.rsplit("candidates_", 1)[1].replace(".csv", "")
    verified_csv = f"{week_dir}/verified_candidates_{week_date}.csv"
    _fetched_path, jd_ok = fetch_jds.run_fetch(verified_csv)
    if not jd_ok:
        print(f"\n{'='*70}")
        print("  HALTED after fetch_jds.py — success rate below floor. See above.")
        print("  Not running package.py against a degraded JD set.")
        print(f"{'='*70}\n")
        sys.exit(1)

    print("\n[5/5] package.py")
    package.run_package()

    print(f"\n{'='*70}")
    print("  Full weekly run complete.")
    print("  Scoring (score.py, Phase 2) is not built yet — this run stops")
    print("  after package.py. See CLAUDE.md / roadmap §5 for Phase 2 scope.")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
