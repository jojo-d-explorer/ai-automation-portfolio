# CONSOLIDATE TO MASTER DATABASE — Joey Clark

**Purpose:** Merge all weekly search CSVs into a single master database with deduplication, metadata tracking, and application tracking columns.
**Runtime:** 1-2 minutes
**When to run:** After each weekly search (ONE_CLICK_WEEKLY_SEARCH)

---

## How to Use
1. Copy everything from "Calculate today's date..." to "...where everything was saved"
2. Paste into CoWork
3. Hit enter (no resume needed)
4. Check master database at the path below

---

## THE PROMPT

Calculate today's date and determine:
- Current week start date (most recent Monday): CURRENT_WEEK

Define path variables:
- BASE_PATH = /Users/jc3/GitHub/ai-automation-portfolio
- MASTER_DB = {BASE_PATH}/results/master_job_database.csv
- RESULTS_DIR = {BASE_PATH}/results

---

### STEP 1: READ EXISTING MASTER DATABASE

Check if {MASTER_DB} exists.

**If it exists:**
- Read all rows
- Count total jobs before consolidation
- **CRITICAL: Preserve all tracking data** — save the values of these columns for every row:
  - Interest
  - Interest_Notes
  - Applied_Date
  - Response
  - Response_Date
- Store this tracking data indexed by Company + Job_Title (the match key)

**If it doesn't exist (first run):**
- Note: will create fresh master with all jobs marked as new entries

---

### STEP 2: READ ALL WEEKLY CSVs

Scan all weekly result folders:
- {RESULTS_DIR}/Week_of_*/data/Master_List_*.csv (new v2.0 structure)
- {RESULTS_DIR}/Week_of_*/Master_List_*.csv (legacy structure)

For each CSV found:
- Read all rows
- Note the source folder date (Week_of_YYYY-MM-DD → extract date)
- Track which file each job came from

Show progress: "Reading Week_of_2026-XX-XX... [N] jobs found"

---

### STEP 3: CONSOLIDATE & DEDUPLICATE

For each job across all weekly CSVs:

**Match key:** Company + Job_Title (case-insensitive, punctuation-normalized comparison)

**Title normalization rule (apply before every comparison):**
Strip all commas and collapse multiple spaces to one before comparing Job_Title values.
Example: "Director, Strategic Partnerships" → "Director Strategic Partnerships"
This prevents comma/spacing variants of the same title from creating duplicate rows.

**If job already exists in master (DUPLICATE):**
- Keep the version with the highest Score
- Update Last_Seen_Date to the most recent week where this job appeared
- Increment Times_Seen by count of additional weeks
- Append new week to Search_Sources (comma-separated)
- **PRESERVE tracking columns** — carry forward Interest, Interest_Notes, Applied_Date, Response, Response_Date from the existing master entry

**If job is new (UNIQUE):**
- Add all search columns from the CSV
- Set metadata:
  - First_Seen_Date = earliest week this job appeared
  - Last_Seen_Date = most recent week this job appeared
  - Times_Seen = number of weeks where this job appeared
  - Search_Sources = comma-separated list of Week_of_YYYY-MM-DD
- Set tracking columns to blank:
  - Interest = ""
  - Interest_Notes = ""
  - Applied_Date = ""
  - Response = ""
  - Response_Date = ""

---

### STEP 4: SAVE UPDATED MASTER

**File:** {MASTER_DB}

**Columns (22 total, in this order):**

*Search data (14):*
Status | Score | Score_Rationale | Company | Job_Title | Sector | Location | Language_Requirement | Work_Arrangement | Salary_USD | Job_Summary | URL | URL_Status | Found_On

*Consolidation metadata (3):*
First_Seen_Date | Last_Seen_Date | Times_Seen | Search_Sources

*Application tracking (5):*
Interest | Interest_Notes | Applied_Date | Response | Response_Date

Sort by Score descending (highest scores first).

Confirm file saved at {MASTER_DB}.

---

### STEP 5: REPORT SUMMARY

Show:

| Metric | Count |
|--------|-------|
| Jobs in master BEFORE consolidation | X |
| Total jobs across all weekly CSVs | Y |
| Duplicates found (already in master) | Z |
| New unique jobs added | W |
| Jobs in master AFTER consolidation | X + W |
| Jobs with tracking data preserved | T |

**Also show:**
- Top 5 jobs by Times_Seen (most persistent — these companies are actively hiring)
- Any jobs where you previously entered Interest or Applied_Date (confirmation tracking data survived)
- Total weekly CSVs processed: [list of Week_of dates]

---

### TRACKING COLUMN REFERENCE

**When you open the master CSV after consolidation, scroll right to fill in these columns:**

| Column | Valid Values | When to Fill |
|--------|-------------|--------------|
| Interest | Shortlisted / Not Interested / Maybe | While scanning results |
| Interest_Notes | Free text ("love this company", "too junior") | While scanning results |
| Applied_Date | YYYY-MM-DD | When you submit application |
| Response | Interview / Rejection / Ghosted / Withdrew | When you hear back |
| Response_Date | YYYY-MM-DD | When you hear back |

**Your tracking entries are preserved every time CONSOLIDATE runs.**
You never lose your markups.

---

*Run every Sunday after ONE_CLICK_WEEKLY_SEARCH completes.*
*Version: 2.0 — Added tracking columns with preservation logic*
*Updated: 2026-02-17*
