---
name: master-db-cleanup
description: "Clean, verify, and standardize a friend's master job database CSV. Use this skill whenever Joey asks to clean, fix, verify, deduplicate, or standardize any master database or job list — including phrases like 'clean [name]'s database', 'fix the master list', 'check [name]'s data', 'standardize the CSV', 'remove dead links', 'dedupe', or 'prep [name]'s data for delivery'. Also trigger when Joey uploads a CSV that looks like job search results and asks to do anything corrective to it. This skill contains the proven 16-column schema, URL specificity rules, deduplication logic, and quality checks developed through the Phil Tassi database disaster recovery."
---

# Master Database Cleanup Skill

## When to Use
- Joey asks to clean, fix, verify, or standardize any friend's master database
- Joey uploads a CSV of job results and asks to correct, deduplicate, or prepare it
- Joey says "prep [name]'s data", "remove dead links", "check the master list"
- Before any delivery — the master database must be clean first

## Target Schema (16 columns, this exact order)

```
Score | Company | Job_Title | Location | Work_Arrangement | Sector | Salary_USD | Job_Summary | URL | Score_Rationale | Times_Seen | First_Seen_Date | Last_Seen_Date | Status | Found_On | URL_Status
```

If the input CSV has different column names, map them:
- `Role` → `Job_Title`
- `Board` → `Found_On`
- `Reason Ranked` or `Reason_Ranked` → `Score_Rationale`
- `Job Summary` → `Job_Summary`
- `Arrangement` → `Work_Arrangement`
- `Salary` → `Salary_USD`

Drop any columns not in the 16-column schema (e.g., `Interest_Level`, `Applied_Date`, `Application_Method`, `Response_Status`, `Notes` — these are application tracking columns that belong in a separate workflow, not the master database).

## Cleanup Steps (execute in order)

### Step 1: Schema Normalization
1. Read the input CSV
2. Map column names to standard schema (see mapping above)
3. Add any missing columns with empty values
4. Reorder to match the 16-column schema exactly
5. Report: "Mapped X columns, added Y missing columns, dropped Z extra columns"

### Step 2: Remove LinkedIn URLs
Any row where URL contains `linkedin.com` → remove entirely.
LinkedIn was removed from automated search in Feb 2026 due to Google index staleness. Friends receive LinkedIn direct search links separately.

Report: "Removed X LinkedIn URLs"

### Step 3: URL Specificity Check
A valid job listing URL must contain a specific job ID — not just a company careers page.

**Specific (KEEP):** URL path contains a numeric job ID or UUID
- Pattern: `/jobs/\d+` or `/[a-f0-9-]{20,}` or `/jobs/[a-f0-9-]{8,}`
- Examples:
  - `boards.greenhouse.io/anthropic/jobs/5021140008` ✅
  - `jobs.lever.co/stripe/abc123de-f456-7890` ✅
  - `jobs.ashbyhq.com/openai/abcdef12-3456-7890-abcd-ef1234567890` ✅

**Generic (REMOVE):** URL is just a company careers page
- Pattern: URL ends at company name with no job ID path segment
- Examples:
  - `jobs.ashbyhq.com/kernel` ❌
  - `boards.greenhouse.io/anthropic` ❌
  - `jobs.lever.co/stripe` ❌

Report: "Kept X specific job URLs, removed Y generic company pages"

### Step 4: Deduplication
Duplicate = same `Company` AND same `Job_Title` (case-insensitive match).

When duplicates found:
- Keep the row with the highest `Score`
- Merge `Found_On` values (e.g., "Greenhouse, Lever")
- Keep the earliest `First_Seen_Date` and latest `Last_Seen_Date`
- Increment `Times_Seen` to reflect total appearances

Report: "Removed X duplicates, Y unique jobs remain"

### Step 5: Standardize Categorical Fields

**Work_Arrangement** must be exactly one of:
- Remote-US
- Remote-Global
- Hybrid
- In-Office
- Unclear

Map variations: "remote" → "Remote-US" (if US-based) or "Remote-Global", "WFH" → "Remote-US", "on-site" → "In-Office", blank → "Unclear"

**Status** must be exactly one of:
- NEW (first time seen)
- REPEAT (seen in previous weeks)
- CLOSED (URL verified dead)
- APPLIED (user has applied)

### Step 6: Sort and Validate
1. Sort by Score descending
2. Verify no blank Company or Job_Title fields
3. Verify all URLs start with `http`
4. Verify Score is numeric and between 1-100
5. Fill any blank `URL_Status` with "Not Checked"

### Step 7: Save and Report

Save cleaned CSV to the same location as the input file (overwrite) AND save a backup of the original with `_backup_YYYY-MM-DD` suffix.

**Final report must include:**
```
CLEANUP SUMMARY
===============
Input:  X rows, Y columns
Output: A rows, 16 columns

Removed:
- LinkedIn URLs: N
- Generic company pages: N
- Duplicates: N

Schema changes:
- Mapped columns: [list]
- Added columns: [list]
- Dropped columns: [list]

Files:
- Cleaned: [full path]
- Backup:  [full path]
```

## Common Issues

**Mixed old/new schema:** Phil's database had 36 columns from multiple schema versions. The column mapping in Step 1 handles this — map what matches, drop what doesn't.

**Duplicate master databases:** Some friends have master databases in both the root folder and weekly subfolders. The canonical location is always:
`results/For_Others/[First_Last]/Master_Job_Database_[First_Last].csv`

**Scores as text:** If Score column contains text like "85/100" or "High", extract the numeric value or flag for manual review.

## Anti-Hallucination Rules
- Do not fabricate or estimate job listings during cleanup. If a row has incomplete data (missing Company, missing URL), flag it for Joey's review rather than guessing.
- Do not invent URLs, scores, or job titles to "fill in" gaps in the data.
- If the input CSV has zero rows after cleanup (all removed as LinkedIn, generic, or duplicate), report that honestly. An empty clean database is better than a fabricated one.
