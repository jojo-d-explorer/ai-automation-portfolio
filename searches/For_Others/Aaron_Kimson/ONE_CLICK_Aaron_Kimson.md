# ONE-CLICK WEEKLY SEARCH: AARON KIMSON

**Owner:** Joey Clark (running on behalf of Aaron Kimson)
**Resume file:** Aaron Kimson Resume -2.4.2026.pdf
**Created:** 2026-02-15
**Last updated:** 2026-02-17 (v2.0 — added data/deliverables subfolders, branded xlsx output)

---

## How to Use
1. Copy everything from "Calculate today's date..." to "...where everything was saved"
2. Paste into CoWork
3. Attach resume: `Aaron Kimson Resume -2.4.2026.pdf`
4. Hit enter
5. Wait 10-15 minutes
6. Come back to results in deliverables/ folder

---

## THE PROMPT

Calculate today's date and determine:
- Current week start date (most recent Monday): CURRENT_WEEK
- Previous week start date (Monday before that): PREVIOUS_WEEK

Define path variables:
- BASE_PATH = /Users/jc3/GitHub/ai-automation-portfolio
- RESULTS_PATH = {BASE_PATH}/results/For_Others/Aaron_Kimson/Week_of_CURRENT_WEEK
- PREVIOUS_RESULTS = {BASE_PATH}/results/For_Others/Aaron_Kimson/Week_of_PREVIOUS_WEEK

Create folders if they don't exist:
- {RESULTS_PATH}/data/
- {RESULTS_PATH}/deliverables/

---

### CONFIGURATION

**Job Boards (search all):**
- site:boards.greenhouse.io
- site:jobs.lever.co
- site:jobs.ashbyhq.com
- site:linkedin.com/jobs

**Roles:**
- Long/Short Hedge Fund Analyst
- Hedge Fund Portfolio Manager
- Director of Equity Research
- Investment Analyst

**Additional LinkedIn search queries (run as supplementary searches):**
- "equity research" analyst
- "L/S equity" analyst
- "long short" equity analyst
- "buy side" equity analyst

**Locations:**
- New York, NY
- San Francisco, CA
- Chicago, IL
- Boston, MA
- Stamford / Greenwich, CT
- Miami, FL

**Filters:**
- Posted within last 7 days
- For each board/role/location combination, extract up to 20 results (paginate to page 2 if needed)

Show progress matrix as you search each board/role/location combination (4 boards × 4 roles × 6 locations = 96 combinations + supplementary LinkedIn queries).

**Supplementary Company Career Page Checks:**
After board searches, also check career pages directly for relevant openings at:
- Two Sigma, Point72, Verition Fund Management, Abdiel Capital
- Millennium Management, Citadel, Balyasny, Schonfeld
- ExodusPoint, Sculptor, Viking Global, Coatue, D1 Capital
- iCapital Network, BlackRock, Lone Pine, Whale Rock

---

### SOURCE FILTERING

Only include results hosted directly on the target ATS boards, company career pages, or LinkedIn direct postings.

**Exclude all third-party job aggregators** including but not limited to: Jobgether, Talent.com, Lensa, Jooble, Adzuna, SimplyHired, ZipRecruiter, Snagajob.

**Recruiter-posted LinkedIn roles** (e.g., Selby Jennings, Long Ridge Partners, Arootah, Odyssey Search Partners, Glocap, SG Partners) ARE allowed but must be labeled with "(Recruiter)" in the Company field.

**URL Integrity (CRITICAL — enforced before any result is included):**

Every job included in output MUST have a direct, job-specific URL containing a unique job ID. Valid patterns:
- Greenhouse: `boards.greenhouse.io/[company]/jobs/[numeric-id]`
- Lever: `jobs.lever.co/[company]/[uuid]`
- Ashby: `jobs.ashbyhq.com/[company]/[uuid]`
- LinkedIn: `linkedin.com/jobs/view/[numeric-id]`

**EXCLUDE any result where:**
- The URL is only a board root (e.g., `jobs.lever.co/stripe`, `boards.greenhouse.io/anthropic`)
- The URL points to a general careers page or company homepage
- You cannot navigate to the specific listing URL
- The job ID is absent, guessed, or a placeholder

**Do not fabricate job IDs.** If you cannot find the specific listing URL, omit the result entirely. Do not mark it "Unverified" and include it anyway. A job without a verified, job-specific URL must not enter the database.

**No hallucinated results:** Only include jobs you actually navigated to and read in this search session. If a board/role/location combination returns zero results, report "0 results" — do not fill the gap with companies you believe are likely hiring.

Mark all included URLs as `URL_Status = "Verified"`.

**Pre-save URL audit:** Before writing any output files, count how many raw results were excluded for missing or invalid URLs. Report this number in the verification summary (e.g., "Excluded 4 results — no job-specific URL found").

---

### FIELD EXTRACTION

Extract these fields (use "N/A" if not available):
- Company (append "(Recruiter)" if posted by a recruiting firm rather than the hiring company)
- Company Sector
- Job Title
- Location
- Language Requirement (if no language mentioned: "N/A"; if other than English: list it)
- Work Arrangement (see standardization below)
- Salary (convert to USD if in other currency; "N/A" if not listed)
- Job Summary (2-3 sentences)
- URL

---

### WORK ARRANGEMENT STANDARDIZATION

Normalize Work_Arrangement to one of these 5 categories:
- **Remote-US** — Any variant of "Remote" + "US/USA/United States", or remote with US city qualifier
- **Remote-Americas** — Any variant of "Remote" + "Americas/LATAM/Canada"
- **Remote-Global** — Generic "Remote" without geographic qualifier, or "Remote Worldwide/EMEA/Europe"
- **Hybrid** — Any hybrid arrangement, including "Remote/Hybrid" variants
- **In-Office** — Location-specific roles without Remote/Hybrid (e.g., "New York, NY", "Greenwich, CT")

Do not leave Work_Arrangement as generic "Remote" — always classify into the specific category above.

---

### DEDUPLICATION

Eliminate duplicate jobs (same Company + same Job Title across boards). Keep highest-scoring version and list all boards where found in "Found_On" column.

---

### SCORING

Using attached resume (Aaron Kimson Resume -2.4.2026.pdf), score each job 1-100 based on:

**Industry Fit (40 points):**
- Hedge fund equity research (L/S, fundamental) = full credit
- TMT / software / fintech coverage = strong credit (35+)
- Sell-side equity research at a top-tier firm = 25-30 (lateral, not a step up)
- Adjacent finance (asset management, investment banking) = partial (15-25)
- Unrelated sectors = minimal (0-10)

**Salary Fit (20 points):**
- Target: $150K+ base salary, $250K+ total compensation
- If salary listed and meets target: full credit
- If salary listed but below target: score proportionally
- If salary not listed ("N/A"): award 10/20 (neutral — don't penalize unknown)

**Location Flexibility (20 points):**
- Remote or hybrid in target city (NY, SF, Chicago, Boston, Stamford/Greenwich): full credit
- In-office in target city: 15/20
- Outside target cities: 5/20

**Seniority Match (20 points):**
- Mid-level analyst / VP / Senior Analyst (4-10 years): full credit
- Director / PM level: full credit (aspirational but reachable)
- Junior / entry-level (1-3 years): partial (10/20)
- C-suite / CIO: minimal (5/20 — too senior)

Provide 1-2 sentence score rationale for each job.

Filter to jobs scoring 70+ only. Rank by score (highest to lowest).

---

### NEW JOB DETECTION

Compare against previous week's Master List. Check in this order:
1. First check: {PREVIOUS_RESULTS}/data/Master_List_PREVIOUS_WEEK.csv
2. Legacy fallback: {PREVIOUS_RESULTS}/Master_List_PREVIOUS_WEEK.csv
3. Original baseline: {BASE_PATH}/results/For_Others/Aaron_Kimson/Week_of_2026-02-09/Master_List_2026-02-09.csv

Compare on Company + Job_Title:
- If previous file exists AND has data: Mark jobs not in previous file as "NEW", returning jobs as "REPEAT"
- If previous file exists but is empty: Mark all as "NEW"
- If no previous file found: Mark all as "NEW"

Add "Status" column with "NEW" or "REPEAT".

---

### OUTPUT FILES

**Data files (backbone for consolidation — not shared with Aaron):**

1. **Master List CSV:** {RESULTS_PATH}/data/Master_List_CURRENT_WEEK.csv
   Columns (in this order): Status | Score | Score_Rationale | Company | Job_Title | Sector | Location | Language_Requirement | Work_Arrangement | Salary_USD | Job_Summary | URL | URL_Status | Found_On

2. **Top 10 New CSV:** {RESULTS_PATH}/data/Top10_New_CURRENT_WEEK.csv
   Same columns, only top 10 jobs marked "NEW". If <10 new jobs, include all new jobs. If zero new jobs, create file with headers and note "No new jobs this week."

3. **Executed prompt:** {BASE_PATH}/searches/For_Others/Aaron_Kimson/executed_CURRENT_WEEK.txt

**Deliverable files (shared with Aaron):**

4. **Branded Excel — Master List:** {RESULTS_PATH}/deliverables/Aaron_Kimson_Master_List_CURRENT_WEEK.xlsx

   Generate a formatted .xlsx version of the Master List CSV:
   - Row 1: Title "Aaron Kimson — Master Job List" (bold, 18pt, navy #1F3864, merged across all columns)
   - Row 2: Subtitle "Week of [Month Day, Year]  |  Prepared by Joey Clark" (11pt, blue #2F5496)
   - Row 3: Stats "[N] jobs  |  Score range: [min]-[max]  |  Avg: [avg]  |  [N] NEW, [N] REPEAT" (10pt, gray #595959, medium blue bottom border)
   - Row 4: Blank separator
   - Row 5: Column headers (bold, 10pt, white text, blue #2F5496 background, auto-filters enabled)
   - Data rows starting Row 6:
     - Font: Arial 10pt
     - Row height: 45px
     - Alternating row shading: even rows #F2F2F2, odd rows white
     - Light grid borders: #D9D9D9
     - Score cells color-coded: green #C6EFCE (90+), blue #D6E4F0 (80-89), yellow #FFF2CC (70-79), red #F2DCDB (<70)
     - Status cells: NEW = bold dark green #006100, REPEAT = gray #808080
     - Text wrapping on Score_Rationale and Job_Summary columns
   - Freeze panes below header row (row 5)
   - Legend row 2 rows below last data: "Score Key: 🟢 90+ Elite | 🔵 80-89 Strong | 🟡 70-79 Good | 🔴 Below 70" (9pt italic gray)
   - Column widths: Status 8, Score 7, Score_Rationale 40, Company 22, Job_Title 35, Sector 20, Location 20, Language_Requirement 12, Work_Arrangement 14, Salary_USD 18, Job_Summary 45, URL 35, URL_Status 10, Found_On 12

5. **Branded Excel — Top 10:** {RESULTS_PATH}/deliverables/Aaron_Kimson_Top10_New_CURRENT_WEEK.xlsx
   Same formatting as item 4, with title: "Aaron Kimson — Top 10 New Opportunities"

---

### VERIFICATION

Verify all files saved. Show:

| Metric | Count |
|--------|-------|
| Total jobs found (pre-filter) | X |
| Jobs scoring 70+ (post-filter) | Y |
| NEW jobs | Z |
| REPEAT jobs | W |
| Boards searched | 4 |
| Role/location combinations | 96+ |

**Files saved at:**
- Master List CSV: [full path]
- Top 10 CSV: [full path]
- Master List Excel: [full path]
- Top 10 Excel: [full path]
- Executed prompt: [full path]

Show top 10 results in a summary table.

Report any errors, broken URLs, or boards/locations that returned zero results.

---

### JOB SEARCH TRACKING UPDATE

After all output files are saved, update the tracking spreadsheet:

**File:** {BASE_PATH}/Job_Search_Tracking.xlsx
**Sheet:** "Job Search Tracking"

Find the rows for **Aaron Kimson** (look for name in column A). Add a new continuation row immediately after the last Aaron row with:

| Column | Value |
|--------|-------|
| C (Search Ran) | Today's date (YYYY-MM-DD) |
| D (Results 70+) | Total jobs scoring 70+ |
| E (Top Score) | Highest score in this search |
| F (Search Config) | 4 boards + career pages \| HF Analyst, PM, ER Dir, Inv Analyst \| NY, SF, CHI, BOS, CT, MIA |
| G (Next Search) | CURRENT_WEEK + 7 days (YYYY-MM-DD) |
| H (Link to Folder) | Aaron_Kimson/Week_of_CURRENT_WEEK/ |

Also mark the previous Aaron row's "Next Search" (column G) as completed by appending " ✓".

Save the updated spreadsheet back to the same path.

---

⚠️  REMINDER: After reviewing results, run CONSOLIDATE_TO_MASTER to update Aaron's master database. After consolidation (Week 2+), run MASTER_ANALYSIS to generate the PDF analysis report in {RESULTS_PATH}/deliverables/.

---

*Run every Sunday. Attach Aaron's resume each time.*
*Template version: 2.0 | Updated: 2026-02-17*

---
---

## SEARCH NOTES (Joey's reference — don't copy into prompt)

### Observations from Week 1 (Feb 9):
- Miami returned zero results — consider dropping from locations
- LinkedIn authenticated browser session produced top 3 results — critical for HF job searches
- Most hedge funds recruit through headhunters, not public ATS boards
- Recruiter-posted roles (Selby Jennings, Long Ridge, Arootah) were among best results
- Added recruiter firms as allowed sources with labeling requirement

### Aaron's profile summary:
- VP Software Equity Research, Citizens JMP Securities (2021-Present)
- CFA Charterholder, Series 87/63, Bloomberg Market Concepts
- Covers vertical software & fintech (BLND, EVCM, EXFY, GWRE, etc.)
- Ranked 4th/26 Senior Analysts in 2025 for buy-side touchpoints
- J.P. Morgan Private Bank (2019-2021), J.P. Morgan LDP (2017-2019)
- ~9 years total finance experience, based in New York

### Scoring weights rationale:
Aaron ranked: Industry > Salary > Skills > Location > Seniority
→ Industry 40, Salary 20, Location 20, Seniority 20
(Skills embedded in Industry Fit for his finance-specific search — TMT/software coverage IS the skill)

### Tuning suggestions from email (pending Aaron's feedback):
1. Add specific target fund career page checks (done — added to supplementary)
2. Adjust seniority filter to exclude <5 year roles (not yet implemented)
3. Consider narrowing to TMT/software-only coverage roles
4. Add recruiter firm searches (done — Selby Jennings, Long Ridge, etc. allowed)
5. Drop Miami, add Stamford/Greenwich CT (done — both included currently)
6. Consider adding salary floor filter ($130K minimum)
