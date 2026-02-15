# Phil Tassi - One-Click Weekly Job Search

## How to Use
1. Copy everything below the line into CoWork
2. Attach resume: `Phillip Tassi - Resume - November 2025 (3).pdf`
3. Hit enter
4. Wait 10-15 minutes
5. Check output folder for results

---

## Prompt (copy from here)

**[CONTEXT CALCULATION]**

Calculate today's date.
Determine CURRENT_WEEK = most recent Monday (if today is Monday, use today).
Determine PREVIOUS_WEEK = Monday before CURRENT_WEEK.

Set BASE_PATH = /Users/jc3/GitHub/ai-automation-portfolio
Set RESULTS_PATH = {BASE_PATH}/results/For_Others/Phil_Tassi/Week_of_{CURRENT_WEEK}
Set PREVIOUS_RESULTS = {BASE_PATH}/results/For_Others/Phil_Tassi/Week_of_{PREVIOUS_WEEK}

Create RESULTS_PATH folder if it doesn't exist.

**[CONFIGURATION]**

Search these job boards for roles posted in the last 7 days:

- site:ashbyhq.com
- site:jobs.lever.co
- site:boards.greenhouse.io

Roles:

- Chief of Staff
- Partnerships
- Business Development

Locations:

- Washington, DC
- London, UK

**[EXECUTION]**

Show progress matrix as you search each board/role/location combination (3 boards × 3 roles × 2 locations = 18 combinations).

**[EXTRACTION]**

Extract these fields (use "N/A" if not available):

- Company
- Company Sector
- Job Title
- Location
- Salary (convert to USD if listed in other currency; "N/A" if not listed)
- Work Arrangement (Remote/Hybrid/In-Office; "N/A" if not specified)
- Job Summary (1-2 sentences)
- URL

**[LOGIC & PROCESSING]**

Deduplication:
If same Company + same Job Title appears across multiple boards, keep highest-scoring version. List all boards where found in "Found_On" column.

Scoring:
Using attached resume, score each job 1-100 based on:

- Skills fit (40 points)
- Industry alignment (35 points)
- Experience match (25 points)

Provide 1-2 sentence score rationale for each job.
Filter to jobs scoring 70+ only.
Rank by score (highest to lowest).

**[NEW JOB DETECTION]**

Look for the most recent previous results file:

1. First check: {PREVIOUS_RESULTS}/Master_List_*.csv
2. If not found, check: {BASE_PATH}/results/For_Others/Phil_Tassi_Search_2026-02-01.csv (legacy file from first run)

Compare current results against previous file:

- If previous file exists AND has data: Mark jobs not in previous file as "NEW", returning jobs as "REPEAT"
- If previous file exists but is empty: Mark all as "NEW"
- If no previous file found (first run): Mark all as "NEW"

Add "Status" column with "NEW" or "REPEAT".

**[OUTPUT]**

1. **Master List:** {RESULTS_PATH}/Master_List_{CURRENT_WEEK}.csv

   Columns (in this order): Status | Score | Score_Rationale | Company | Job_Title | Sector | Location | Work_Arrangement | Salary_USD | Job_Summary | URL | Found_On

2. **Top 10 New:** {RESULTS_PATH}/Top10_New_{CURRENT_WEEK}.csv

   Same columns, only top 10 jobs marked "NEW" (ranked by score).
   If fewer than 10 new jobs, include all new jobs.
   If zero new jobs, create file with headers only and note "No new jobs scoring 70+ this week."

3. **Save Executed Prompt:** {RESULTS_PATH}/Executed_Prompt_{CURRENT_WEEK}.txt

   Save a copy of this prompt with the calculated dates filled in for reproducibility.

**[VERIFICATION]**

Confirm all files saved. Show final summary:

- Total jobs found (before filtering): X
- Jobs scoring 70+: Y
- NEW jobs: Z
- REPEAT jobs: W
- Files saved at: [list full paths]

Show top 10 results in a summary table.

**[JOB SEARCH TRACKING UPDATE]**

After all output files are saved, update the tracking spreadsheet:

**File:** /Users/jc3/GitHub/ai-automation-portfolio/Job_Search_Tracking.xlsx
**Sheet:** "Job Search Tracking"

Find the rows for **Phil Tassi** (look for name in column A). Add a new continuation row immediately after the last Phil row with:

| Column | Value |
|--------|-------|
| C (Search Ran) | Today's date (YYYY-MM-DD) |
| D (Results 70+) | Total jobs scoring 70+ |
| E (Top Score) | Highest score in this search |
| F (Search Config) | Boards searched \| Roles \| Locations (short summary) |
| G (Next Search) | CURRENT_WEEK + 7 days (YYYY-MM-DD) |
| H (Link to Folder) | Phil_Tassi/Week_of_CURRENT_WEEK/ |

Also mark the previous Phil row's "Next Search" (column G) as completed by appending " ✓".

Save the updated spreadsheet back to the same path.
