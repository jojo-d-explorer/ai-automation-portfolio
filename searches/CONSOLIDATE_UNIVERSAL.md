# CONSOLIDATE TO MASTER — Universal

**Purpose:** Merge all weekly search CSVs for any user into their master database.
Does exactly three things: deduplicates, increments repeat-job counters, and preserves
application tracking data. Everything else (URL validation, schema migration, formatting)
happens upstream or downstream — not here.

**Runtime:** 1–2 minutes
**When to run:** After each weekly ONE_CLICK search completes.
**Requires:** User name argument (see usage below)

---

## How to Use

1. Copy everything from "You are running..." to the end of THE PROMPT
2. Replace `[USER]` with the user's name (e.g. `joey`, `phil`, `aaron`, `vivienne`, `rosalind`)
3. Paste into CoWork — no attachments needed
4. Hit enter

---

## THE PROMPT

You are running the universal consolidation for **[USER]**.

Define:
- BASE_PATH = /Users/jc3/GitHub/ai-automation-portfolio

---

### STEP 0: RESOLVE USER PATHS

Use the user argument `[USER]` to locate the correct files. Apply the same discovery
logic as `JC3/dashboard.py`:

**If [USER] is "joey" (case-insensitive):**
```
MASTER_DB   = {BASE_PATH}/results/master_job_database.csv
RESULTS_DIR = {BASE_PATH}/results
```

**For all other users:**
Match [USER] against folder names in `{BASE_PATH}/results/For_Others/` using a
case-insensitive prefix match on the first word of each folder name
(e.g. "phil" → "Phil_Tassi", "aaron" → "Aaron_Kimson").

```
FOLDER_NAME = [matched folder, e.g. Phil_Tassi]
MASTER_DB   = {BASE_PATH}/results/For_Others/{FOLDER_NAME}/Master_Job_Database_{FOLDER_NAME}.csv
RESULTS_DIR = {BASE_PATH}/results/For_Others/{FOLDER_NAME}
```

If no folder matches, stop and report: "No results folder found for '[USER]'. Available
users: [list folders in results/For_Others/ plus 'joey']."

Confirm the resolved paths before proceeding.

---

### STEP 1: READ EXISTING MASTER DATABASE

Check if {MASTER_DB} exists.

**If it exists:**
- Read all rows
- Save the values of these five tracking columns for every row, indexed by match key
  (Company + Job_Title, normalized — see normalization rule in Step 3):
  - Interest
  - Interest_Notes
  - Applied_Date
  - Response
  - Response_Date
- Note total job count before consolidation

**If it does not exist (first run):**
- Note: master will be created fresh from weekly CSVs
- No tracking data to preserve

---

### STEP 2: SCAN WEEKLY CSVs

Find all weekly Master List CSVs under {RESULTS_DIR}. Check both structures:

```
{RESULTS_DIR}/Week_of_*/data/Master_List_*.csv    ← v2.0 (data/ subfolder)
{RESULTS_DIR}/Week_of_*/Master_List_*.csv          ← legacy (flat)
```

Also check for any loose CSV files directly in {RESULTS_DIR} that look like early
one-off search outputs (e.g. `Phil_Tassi_Search_2026-02-01.csv`) and include them.

For each file found:
- Read all rows
- Extract the week date from the folder name (`Week_of_YYYY-MM-DD` → date string)
  For loose files, use the date in the filename if present; otherwise use file modification date
- Report: "Found {N} jobs in {file_path}"

If no weekly CSVs are found, stop and report the paths that were searched.

---

### STEP 3: MERGE AND DEDUPLICATE

**Normalization rule (match key only — do NOT rewrite stored values):**
To build the match key from Company + Job_Title:
1. Convert to lowercase
2. Strip all commas
3. Collapse multiple spaces to a single space
4. Trim leading/trailing whitespace

This normalization is used only for comparison. The original Company and Job_Title
values are always preserved as-is in the output.

**Before merging, skip any row where ANY of the following are true:**
- URL contains "linkedin.com" (stale Google index — LinkedIn removed from automated search Feb 2026)
- Close_Reason column is not empty (previously flagged as dead by check_urls.py)
- URL_Status contains "closed", "dead", or "stale" (previously flagged)

Report skipped rows at the end: "Filtered out {N} rows ({X} LinkedIn, {Y} flagged dead)"

**For each remaining job across all weekly CSVs, apply:**

**If the normalized match key already exists in the master:**
- Keep whichever version has the higher Score; if equal, keep the master version
- Set Last_Seen_Date to the most recent week date this job has appeared
- Increment Times_Seen by the number of additional appearances
- Append the new week date to Search_Sources (comma-separated, no duplicates)
- **Restore tracking columns** from the saved values in Step 1 — do not overwrite
  with blank values from the incoming weekly CSV

**If the normalized match key is new:**
- Add the job with all columns from the weekly CSV
- Set consolidation metadata:
  - First_Seen_Date = earliest week date this job appears in the scanned CSVs
  - Last_Seen_Date = most recent week date
  - Times_Seen = total number of weekly CSVs this job appeared in (minimum 1)
  - Search_Sources = comma-separated list of week dates
- Set tracking columns to blank:
  - Interest = ""
  - Interest_Notes = ""
  - Applied_Date = ""
  - Response = ""
  - Response_Date = ""

---

### STEP 4: SAVE UPDATED MASTER

Write all rows to {MASTER_DB}.

**Column order (preserve whatever columns exist in the data — do not add or remove columns):**

Required columns that must be present:
- From search data: Status, Score, Score_Rationale, Company, Job_Title, Sector,
  Location, Language_Requirement, Work_Arrangement, Salary_USD, Job_Summary,
  URL, URL_Status, Found_On
- Consolidation metadata: First_Seen_Date, Last_Seen_Date, Times_Seen, Search_Sources
- Application tracking: Interest, Interest_Notes, Applied_Date, Response, Response_Date

If any required column is missing from all source CSVs, add it as a blank column.
Do not remove columns that exist in the current master but are absent from weekly CSVs.

Sort by Score descending.

Confirm: "Saved {N} jobs to {MASTER_DB}"

---

### STEP 5: REPORT

Show:

| Metric | Count |
|--------|-------|
| Jobs in master before consolidation | — |
| Total jobs across all weekly CSVs | — |
| New unique jobs added | — |
| Repeat jobs (already in master) | — |
| Jobs in master after consolidation | — |
| Tracking rows preserved (had any tracking data) | — |
| Weekly CSVs processed | — |

Also list:
- Weekly files processed (path + job count each)
- Any jobs where Applied_Date or Interest was carried forward (confirmation tracking survived)
- Top 5 by Times_Seen (most persistent — active hiring signal)

Report any files that were found but could not be read.

---

*Version: 1.0 — Universal rewrite of CONSOLIDATE_TO_MASTER.md*
*Created: 2026-02-25*
*Scope: deduplication + Times_Seen + tracking preservation only*
