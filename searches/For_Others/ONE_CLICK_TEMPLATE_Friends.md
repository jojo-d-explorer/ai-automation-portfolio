# ONE-CLICK WEEKLY SEARCH: [FRIEND NAME] — TEMPLATE v3.0

**Purpose:** Duplicate this file for each new friend. Replace all [BRACKETED] values with their intake questionnaire responses. Save as `ONE_CLICK_[First_Last].md` in `/searches/For_Others/[First_Last]/`.

**Runtime:** 8-10 minutes (Phase 1 of 7-phase pipeline)
**Prerequisites:** Friend's resume (PDF), completed intake questionnaire

**Setup checklist before first run:**
- [ ] Friend completed intake questionnaire
- [ ] Resume received (PDF)
- [ ] Replaced all [BRACKETED] fields below
- [ ] Created results folder: `/results/For_Others/[First_Last]/`
- [ ] Saved this file as `ONE_CLICK_[First_Last].md`

---

**Owner:** Joey Clark (running on behalf of [FRIEND NAME])
**Resume file:** [RESUME FILENAME.pdf]
**Created:** [DATE]
**Last updated:** [DATE]

---

## WHAT'S NEW IN v3.0

- **21-column schema** — Language_Requirement dropped, tracking columns added
- **Pipeline reorder** — URL verification runs BEFORE consolidation (dead links never enter master)
- **No Top 10 file** — Full results delivered; friend decides what's interesting
- **Simplified output** — Single weekly CSV + branded XLSX
- **Anti-hallucination strengthened** — Explicit rules against fabricated listings

---

## USAGE INSTRUCTIONS

1. Copy everything from "Calculate today's date..." to "...where everything was saved"
2. Paste into CoWork
3. Attach: [RESUME FILENAME.pdf]
4. Hit enter
5. Wait 8-10 minutes
6. Proceed to Phase 2 (VERIFY) per ops_playbook_v2

**Pipeline reminder:** This prompt is Phase 1 (SEARCH). After completion:
- Phase 2: Run `check_urls.py` on weekly output
- Phase 3: Run master-db-cleanup SKILL
- Phase 4: Consolidate to master database
- Phases 5-7: Analyze, Package, Deliver

---

## THE PROMPT

Calculate today's date and determine:
- Current week start date (most recent Monday): CURRENT_WEEK
- Previous week start date (Monday before that): PREVIOUS_WEEK

Use these dates for file paths and comparisons below.

Define path variables:
- BASE_PATH = /Users/jc3/GitHub/ai-automation-portfolio
- RESULTS_PATH = {BASE_PATH}/results/For_Others/[First_Last]/Week_of_CURRENT_WEEK

---

### CONFIGURATION

**Job Boards (3 boards):**
- site:boards.greenhouse.io
- site:jobs.lever.co
- site:jobs.ashbyhq.com

**LinkedIn is NOT searched** — Google's index returns stale listings. Friend receives LinkedIn direct search links separately via `linkedin_links.py`.

**Roles:**
[FROM INTAKE — list 2-5 specific titles]
- [Role 1]
- [Role 2]
- [Role 3]

**Locations:**
[FROM INTAKE]
- [Location 1]
- [Location 2]
- [Location 3]

**Filters:**
- Posted within last 7 days
- [FROM INTAKE — deal-breakers become exclusion filters]
- For each board/role/location combination, extract up to 20 results

Show progress matrix as you search each combination.

---

### SOURCE FILTERING & URL INTEGRITY

**Only include results hosted directly on the target ATS boards.**

**Exclude all third-party job aggregators** including but not limited to: Jobgether, Talent.com, Lensa, Jooble, Adzuna, SimplyHired, ZipRecruiter, Snagajob.

**URL Integrity (CRITICAL):**

Every job included MUST have a direct, job-specific URL containing a unique job ID.

**Valid URL patterns:**
- Greenhouse: `boards.greenhouse.io/[company]/jobs/[numeric-id]`
- Lever: `jobs.lever.co/[company]/[uuid]`
- Ashby: `jobs.ashbyhq.com/[company]/[uuid]`

**EXCLUDE any result where:**
- URL is only a board root (e.g., `jobs.lever.co/stripe`)
- URL points to a general careers page
- Job ID is absent, guessed, or fabricated

**Anti-hallucination rule:** Only include jobs you actually navigated to and extracted data from in this session. If a board/role/location returns zero results, report "0 results" — do not fill gaps with assumed listings.

**Pre-save audit:** Before writing output files, count how many results were excluded for invalid URLs. Report this in verification summary.

---

### FIELD EXTRACTION

Extract these fields (use "N/A" if not available):

| Field | Notes |
|-------|-------|
| Company | Exact company name |
| Job_Title | Exact title from listing |
| Location | City, State/Country or "Remote" |
| Work_Arrangement | See standardization below |
| Sector | Company's primary industry |
| Salary_USD | Convert to USD; "N/A" if not listed |
| Job_Summary | 2-3 sentences |
| URL | Full job-specific URL |
| Found_On | Board name (Greenhouse, Lever, Ashby) |

---

### WORK ARRANGEMENT STANDARDIZATION

Normalize to exactly one of these 5 categories:

- **Remote-US** — Remote limited to US
- **Remote-Global** — Remote worldwide or no geographic restriction
- **Hybrid** — Any hybrid arrangement
- **In-Office** — Location-specific, no remote option
- **Unclear** — Cannot determine from listing

Do not leave as generic "Remote" — always classify into specific category.

---

### DEDUPLICATION

If same Company + same Job_Title appears across multiple boards:
- Keep highest-scoring version
- Merge all boards into "Found_On" column (e.g., "Greenhouse, Lever")

---

### SCORING

Using attached resume ([RESUME FILENAME.pdf]), score each job 1-100 based on:

[SCORING WEIGHTS — adjust based on intake priority ranking]

**Industry Fit ([X] points):**
[FROM INTAKE — define target sectors]
- Full credit: [criteria]
- Partial credit: [criteria]
- Minimal credit: [criteria]

**Skills Match ([X] points):**
[FROM INTAKE — their top skills]
- Key skills: [Skill 1], [Skill 2], [Skill 3]
- Score based on overlap with job requirements

**Seniority Match ([X] points):**
- Score based on experience alignment with role level

**Location Flexibility ([X] points):**
- Target location or Remote: full credit
- Hybrid in target city: partial credit
- Outside targets: minimal credit

**Salary Fit ([X] points):**
[FROM INTAKE — target compensation]
- Listed and meets target: full credit
- Listed but below: score proportionally
- Not listed ("N/A"): half points (neutral)

Provide 1-2 sentence Score_Rationale for each job.

**Filter to jobs scoring 70+ only. Rank by score descending.**

---

### NEW/REPEAT DETECTION

Compare against previous week's results:

**Check location:** {BASE_PATH}/results/For_Others/[First_Last]/Week_of_PREVIOUS_WEEK/[First_Last]_PREVIOUS_WEEK.csv

- If file exists: Jobs not in previous = "NEW", matching jobs = "REPEAT"
- If no file (first run): Mark all as "NEW"

Add "Status" column with NEW or REPEAT.

---

### OUTPUT FILES

Create folder if needed: {RESULTS_PATH}/

**Primary output (1 file):**

**Weekly Results CSV:** {RESULTS_PATH}/[First_Last]_CURRENT_WEEK.csv

**Columns (21 total, in this exact order):**
```
Score | Company | Job_Title | Location | Work_Arrangement | Sector | Salary_USD | Job_Summary | URL | Score_Rationale | Times_Seen | First_Seen_Date | Last_Seen_Date | Status | Found_On | URL_Status | Applied_Date | Application_Method | Response_Status | Interview_Stage | Notes
```

**Column notes:**
- Times_Seen: Set to 1 for all (will be updated during consolidation)
- First_Seen_Date: CURRENT_WEEK date
- Last_Seen_Date: CURRENT_WEEK date
- URL_Status: "Not Checked" (will be updated by check_urls.py in Phase 2)
- Applied_Date through Notes: Leave blank (tracking columns for friend's use)

**Branded XLSX:** {RESULTS_PATH}/[First_Last]_CURRENT_WEEK.xlsx

Generate formatted .xlsx version:
- Row 1: Title "[Friend Name] — Job Search Results" (bold, 18pt, navy #1F3864)
- Row 2: Subtitle "Week of [Month Day, Year] | Prepared by Joey Clark" (11pt, blue #2F5496)
- Row 3: Stats "[N] jobs | Score range: [min]-[max] | Avg: [avg] | [N] NEW, [N] REPEAT" (10pt, gray)
- Row 4: Blank separator
- Row 5: Column headers (bold, white text, blue #2F5496 background, auto-filters)
- Data rows starting Row 6:
  - Font: Arial 10pt
  - Alternating row shading: even #F2F2F2, odd white
  - Score color-coded: green (90+), blue (80-89), yellow (70-79)
  - Status: NEW = bold green, REPEAT = gray
  - Text wrapping on Score_Rationale and Job_Summary
- Freeze panes below row 5
- Column widths optimized for readability

**Executed prompt:** {BASE_PATH}/searches/For_Others/[First_Last]/executed_CURRENT_WEEK.txt

---

### VERIFICATION

Show completion summary:

| Metric | Count |
|--------|-------|
| Total jobs found (pre-filter) | X |
| Jobs scoring 70+ (post-filter) | Y |
| NEW jobs | Z |
| REPEAT jobs | W |
| Excluded (invalid URLs) | X |
| Boards searched | 3 |
| Role/location combinations | [N] |

**Files saved at:**
- Weekly CSV: [full path]
- Weekly XLSX: [full path]
- Executed prompt: [full path]

Report any boards that returned zero results.

---

### NEXT STEPS (after this prompt completes)

**Phase 2 — VERIFY:** Run check_urls.py on the weekly CSV:
```bash
python3 JC3/check_urls.py {RESULTS_PATH}/[First_Last]_CURRENT_WEEK.csv
```

**Phase 3 — CLEAN:** Run master-db-cleanup SKILL to standardize data.

**Phase 4 — CONSOLIDATE:** Merge into master database.

**Phases 5-7:** See ops_playbook_v2.docx for ANALYZE, PACKAGE, DELIVER instructions.

---

## WEIGHT ADJUSTMENT GUIDE

**Default weights (100 points total):**
- Industry Fit: 35
- Skills Match: 25
- Seniority Match: 20
- Location Flexibility: 10
- Salary Fit: 10

**Adjust based on friend's priority ranking (1-5):**

| Their #1 Priority | Adjustment |
|-------------------|------------|
| Salary | Salary → 30pts, Industry → 25pts |
| Location | Location → 25pts, Skills → 20pts |
| Skills Match | Skills → 35pts, Industry → 25pts |
| Industry Fit | Industry → 40pts (keep high) |
| Seniority | Seniority → 30pts, Location → 10pts |

**Principle:** #1 priority gets 35-40pts, #5 gets 10pts, middle three split the rest.

---

*Template version: 3.0*
*Updated: 2026-03-01*

**Changes from v2.0:**
- 21-column schema (Language_Requirement dropped, tracking columns added)
- Removed Top 10 output file (full results only)
- Simplified folder structure (no data/deliverables split)
- Added pipeline phase references to ops_playbook_v2
- Strengthened anti-hallucination language
- URL_Status defaults to "Not Checked" (check_urls.py fills in Phase 2)
- LinkedIn explicitly excluded from boards
