#!/usr/bin/env python3
"""
Verify LinkedIn Removal Changes — Dry Run Checker

Run this after applying the edits from LINKEDIN_REMOVAL_CHANGES.md.
It scans all ONE_CLICK files and related docs to confirm LinkedIn
references have been properly removed.

Usage:
  python3 JC3/verify_linkedin_removal.py

Exit codes:
  0 = All checks passed
  1 = Issues found (see output)
"""

import os
import re
import sys

# ─────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────

REPO_ROOT = "/Users/jc3/GitHub/ai-automation-portfolio"

# Files that MUST be checked
ONE_CLICK_FILES = [
    "searches/joey/ONE_CLICK_WEEKLY_SEARCH.md",
    "searches/For_Others/Aaron_Kimson/ONE_CLICK_Aaron_Kimson.md",
    "searches/For_Others/Phil_Tassi/ONE_CLICK_Phil_Tassi.md",
    "searches/For_Others/Vivienne_Pham/ONE_CLICK_Vivienne_Pham.md",
    "searches/For_Others/Rosalind_Gahamire/ONE_CLICK_Rosalind_Gahamire.md",
    "searches/For_Others/ONE_CLICK_TEMPLATE_Friends.md",
]

# Files that SHOULD be checked if they exist
OPTIONAL_FILES = [
    "searches/FORMAT_SPEC.md",
    "README.md",
]

# Expected board configuration (what SHOULD be present)
EXPECTED_BOARDS = [
    "site:boards.greenhouse.io",
    "site:jobs.lever.co",
    "site:jobs.ashbyhq.com",
]

# Strings that should NOT appear anywhere
FORBIDDEN_STRINGS = [
    "site:linkedin.com/jobs",
    "site:linkedin.com",
]

# URL reconstruction line that should be gone
FORBIDDEN_URL_RECON = [
    "LinkedIn: linkedin.com/jobs/view/",
    "linkedin.com/jobs/view/[id]",
]

# Expected combo counts per file (boards × roles × locations)
EXPECTED_COMBOS = {
    "ONE_CLICK_WEEKLY_SEARCH.md": 36,       # 3 × 3 × 4
    "ONE_CLICK_Aaron_Kimson.md": 72,         # 3 × 4 × 6
    "ONE_CLICK_Phil_Tassi.md": 18,           # 3 × 3 × 2
    "ONE_CLICK_Vivienne_Pham.md": 81,        # 3 × 9 × 3
}


# ─────────────────────────────────────────────────────────────
# Checks
# ─────────────────────────────────────────────────────────────

def check_file(filepath, filename):
    """Run all checks on a single file. Returns list of issues."""
    issues = []
    
    full_path = os.path.join(REPO_ROOT, filepath)
    
    if not os.path.exists(full_path):
        return [f"FILE NOT FOUND: {filepath}"]
    
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
    lines = content.split("\n")
    
    # CHECK 1: No forbidden LinkedIn strings
    for forbidden in FORBIDDEN_STRINGS:
        for i, line in enumerate(lines, 1):
            if forbidden.lower() in line.lower():
                # Skip if it's in a comment or note explaining the removal
                if "removed" in line.lower() or "no longer" in line.lower() or "note:" in line.lower():
                    continue
                issues.append(
                    f"  ❌ FOUND '{forbidden}' on line {i}: {line.strip()}"
                )
    
    # CHECK 2: No LinkedIn URL reconstruction reference
    for forbidden in FORBIDDEN_URL_RECON:
        for i, line in enumerate(lines, 1):
            if forbidden.lower() in line.lower():
                issues.append(
                    f"  ❌ FOUND URL recon reference on line {i}: {line.strip()}"
                )
    
    # CHECK 3: Expected boards ARE present
    for board in EXPECTED_BOARDS:
        if board not in content:
            issues.append(f"  ⚠️  MISSING expected board: {board}")
    
    # CHECK 4: Combination count is correct (if applicable)
    base = os.path.basename(filepath)
    if base in EXPECTED_COMBOS:
        expected = EXPECTED_COMBOS[base]
        # Look for pattern like "= 48 combinations" or "= 80"
        combo_pattern = re.findall(r"=\s*(\d+)\s+combinations?", content)
        if combo_pattern:
            found_count = int(combo_pattern[-1])  # take the last match
            if found_count != expected:
                issues.append(
                    f"  ❌ COMBO COUNT: found {found_count}, expected {expected}"
                )
        # Also check for "N boards ×" pattern
        board_count_matches = re.findall(r"(\d+)\s*boards?\s*[×x]", content)
        for match in board_count_matches:
            if int(match) == 4:
                issues.append(
                    f"  ❌ BOARD COUNT: still says '4 boards' — should be '3 boards'"
                )
    
    # CHECK 5: "Last updated" is 2026-02-25
    if "Last updated:" in content:
        date_match = re.search(r"Last updated:\*?\*?\s*([\d-]+)", content)
        if date_match and date_match.group(1) != "2026-02-25":
            issues.append(
                f"  ⚠️  LAST UPDATED: {date_match.group(1)} — expected 2026-02-25"
            )
    
    # CHECK 6: Should reference "3" boards somewhere (not "4")
    if "4 boards" in content.lower() or "4 job boards" in content.lower():
        issues.append(
            f"  ❌ REFERENCE TO '4 boards' found — should be '3 boards'"
        )
    
    return issues


def main():
    print("=" * 60)
    print("  LinkedIn Removal Verification — Dry Run")
    print("=" * 60)
    print()
    
    total_issues = 0
    files_checked = 0
    files_missing = 0
    
    # Check required ONE_CLICK files
    print("📋 ONE_CLICK Files (required):\n")
    for filepath in ONE_CLICK_FILES:
        filename = os.path.basename(filepath)
        full_path = os.path.join(REPO_ROOT, filepath)
        
        if not os.path.exists(full_path):
            print(f"  ⚠️  {filename} — FILE NOT FOUND at {filepath}")
            files_missing += 1
            continue
        
        issues = check_file(filepath, filename)
        files_checked += 1
        
        if issues:
            print(f"  ❌ {filename} — {len(issues)} issue(s):")
            for issue in issues:
                print(f"    {issue}")
            total_issues += len(issues)
        else:
            print(f"  ✅ {filename} — CLEAN")
    
    # Check optional files
    print(f"\n📋 Supporting Files (optional):\n")
    for filepath in OPTIONAL_FILES:
        filename = os.path.basename(filepath)
        full_path = os.path.join(REPO_ROOT, filepath)
        
        if not os.path.exists(full_path):
            print(f"  ⏭️  {filename} — not found (skipping)")
            continue
        
        files_checked += 1
        
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        opt_issues = []
        if "4 boards" in content.lower() or "4 job boards" in content.lower():
            opt_issues.append("  ❌ References '4 boards' — should be '3 boards'")
        
        for forbidden in FORBIDDEN_STRINGS:
            if forbidden.lower() in content.lower():
                opt_issues.append(f"  ❌ Contains '{forbidden}'")
        
        if opt_issues:
            print(f"  ❌ {filename} — {len(opt_issues)} issue(s):")
            for issue in opt_issues:
                print(f"    {issue}")
            total_issues += len(opt_issues)
        else:
            print(f"  ✅ {filename} — CLEAN")
    
    # Check that key JC3 tools exist
    print(f"\n📋 JC3 Tools (should exist):\n")
    urls_path = os.path.join(REPO_ROOT, "JC3/check_urls.py")
    if os.path.exists(urls_path):
        print(f"  ✅ JC3/check_urls.py — present")
    else:
        print(f"  ⚠️  JC3/check_urls.py — NOT FOUND (place in repo)")
        files_missing += 1
    
    # Summary
    print(f"\n{'=' * 60}")
    print(f"  SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Files checked:  {files_checked}")
    print(f"  Files missing:  {files_missing}")
    print(f"  Issues found:   {total_issues}")
    print()
    
    if total_issues == 0 and files_missing == 0:
        print("  ✅ ALL CHECKS PASSED — LinkedIn removal complete!")
        print()
        sys.exit(0)
    elif total_issues == 0 and files_missing > 0:
        print("  ⚠️  No content issues, but some files are missing.")
        print("     Place missing files and re-run.")
        print()
        sys.exit(1)
    else:
        print(f"  ❌ {total_issues} issue(s) to fix. See details above.")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
