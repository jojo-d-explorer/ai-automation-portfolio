# Aaron Kimson - One-Click Weekly Job Search

## How to Use
1. Copy everything below the line into CoWork
2. Attach resume: `Aaron Kimson Resume -2.4.2026.pdf`
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
Set RESULTS_PATH = {BASE_PATH}/results/For_Others/Aaron_Kimson/Week_of_{CURRENT_WEEK}
Set PREVIOUS_RESULTS = {BASE_PATH}/results/For_Others/Aaron_Kimson/Week_of_{PREVIOUS_WEEK}

Create RESULTS_PATH folder if it doesn't exist.

**[CONFIGURATION]**

Job Boards (search all):
- site:boards.greenhouse.io
- site:jobs.lever.co
- site:jobs.ashbyhq.com
- site:linkedin.com/jobs

Roles:
- Long/Short Hedge Fund Analyst
- Hedge Fund Portfolio Manager
- Director of Equity Research
- Investment Analyst

Additional LinkedIn search queries (run these as supplementary searches):
- "equity research" analyst
- "L/S equity" analyst
- "long short" equity analyst
- "buy side" equity analyst

Locations:
- New York, NY
- San Francisco, CA
- Chicago, IL
- Boston, MA
- Stamford / Greenwich, CT
- Miami, FL

Filters:
- Posted within last 7 days
- For each board/role/location combination, extract up to 20 results (paginate to page 2 if needed)

Show progress matrix as you search each board/role/location combination (4 boards × 4 roles × 5 locations = 80 combinations + supplementary LinkedIn queries).

**Supplementary Company Career Page Checks:**
After board searches, also check career pages directly for relevant openings at:
- Two Sigma, Point72, Verition Fund Management, Abdiel Capital
- Millennium Management, Citadel, Balyasny, Schonfeld
- ExodusPoint, Sculptor, Viking Global, Coatue, D1 Capital
- iCapital Network, BlackRock, Lone Pine, Whale Rock

**[SOURCE FILTERING]**

Only include results hosted directly on the target ATS boards, company career pages, or LinkedIn direct postings.

Exclude all third-party job aggregators including but not limited to: Jobgether, Talent.com, Lensa, Jooble, Adzuna, SimplyHired, ZipRecruiter, Snagajob.

Recruiter-posted LinkedIn roles (e.g., Selby Jennings, Long Ridge Partners, Arootah, Odyssey Search Partners, Glocap, SG Partners) ARE allowed but must be labeled with "(Recruiter)" in the Company field.

URL Verification: For each result, verify the URL resolves to an active job listing. If the URL is broken or redirects to a general careers page, attempt to reconstruct the direct ATS link using standard board URL formats:
- Greenhouse: boards.greenhouse.io/[company]/jobs/[id]
- Lever: jobs.lever.co/[company]/[id]
- Ashby: jobs.ashby.com/[company]/[id] or [company].ashbyhq.com
- LinkedIn: linkedin.com/jobs/view/[id]

If the URL cannot be verified or reconstructed, mark URL_Status as "Unverified." Otherwise mark as "Verified."

**[FIELD EXTRACTION]**

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

**[WORK ARRANGEMENT STANDARDIZATION]**

Normalize Work_Arrangement to one of these 5 categories:
- **Remote-US** — Any variant of "Remote" + "US/USA/United States", or remote with US city qualifier
- **Remote-Americas** — Any variant of "Remote" + "Americas/LATAM/Canada"
- **Remote-Global** — Generic "Remote" without geographic qualifier, or "Remote Worldwide/EMEA/Europe"
- **Hybrid** — Any hybrid arrangement, including "Remote/Hybrid" variants
- **In-Office** — Location-specific roles without Remote/Hybrid (e.g., "New York, NY", "Greenwich, CT")

Do not leave Work_Arrangement as generic "Remote" — always classify into the specific category above.

**[DEDUPLICATION]**

Eliminate duplicate jobs (same Company + same Job Title across boards). Keep highest-scoring version and list all boards where found in "Found_On" column.

**[SCORING]**

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

**[NEW JOB DETECTION]**

Look for the most recent previous results file:

1. First check: {PREVIOUS_RESULTS}/Master_List_*.csv
2. If not found, check: {BASE_PATH}/results/For_Others/Aaron_Kimson/Week_of_2026-02-09/Master_List_2026-02-09.csv (first run baseline)

Compare current results against previous file (match on Company + Job_Title):
- If previous file exists AND has data: Mark jobs not in previous file as "NEW", returning jobs as "REPEAT"
- If previous file exists but is empty: Mark all as "NEW"
- If no previous file found: Mark all as "NEW"

Add "Status" column with "NEW" or "REPEAT".

**[OUTPUT FILES]**

Create folders if they don't exist:
- {RESULTS_PATH}/
- {BASE_PATH}/searches/prompts/for_others/Aaron_Kimson/

1. **Master List:** {RESULTS_PATH}/Master_List_{CURRENT_WEEK}.csv

   Columns (in this order): Status | Score | Score_Rationale | Company | Job_Title | Sector | Location | Language_Requirement | Work_Arrangement | Salary_USD | Job_Summary | URL | URL_Status | Found_On

2. **Top 10 New:** {RESULTS_PATH}/Top10_New_{CURRENT_WEEK}.csv

   Same columns, only top 10 jobs marked "NEW" (ranked by score).
   If fewer than 10 new jobs, include all new jobs.
   If zero new jobs, create file with headers only and note "No new jobs scoring 70+ this week."

3. **Save Executed Prompt:** {BASE_PATH}/searches/prompts/for_others/Aaron_Kimson/executed_{CURRENT_WEEK}.txt

   Save a copy of this prompt with the calculated dates filled in for reproducibility.

**[VERIFICATION]**

Confirm all files saved. Show final summary:

| Metric | Count |
|--------|-------|
| Total jobs found (pre-filter) | X |
| Jobs scoring 70+ (post-filter) | Y |
| NEW jobs | Z |
| REPEAT jobs | W |
| Boards searched | 4 |
| Role/location combinations | 80+ |

Files saved at:
- Master List: [full path]
- Top 10 New: [full path]
- Executed prompt: [full path]

Show top 10 results in a summary table.

Report any errors, broken URLs, or boards/locations that returned zero results.

**[JOB SEARCH TRACKING UPDATE]**

After all output files are saved, update the tracking spreadsheet:

**File:** /Users/jc3/GitHub/ai-automation-portfolio/Job_Search_Tracking.xlsx
**Sheet:** "Job Search Tracking"

Find the rows for **Aaron Kimson** (look for name in column A). Add a new continuation row immediately after the last Aaron row with:

| Column | Value |
|--------|-------|
| C (Search Ran) | Today's date (YYYY-MM-DD) |
| D (Results 70+) | Total jobs scoring 70+ |
| E (Top Score) | Highest score in this search |
| F (Search Config) | Boards searched \| Roles \| Locations (short summary) |
| G (Next Search) | CURRENT_WEEK + 7 days (YYYY-MM-DD) |
| H (Link to Folder) | Aaron_Kimson/Week_of_CURRENT_WEEK/ |

Also mark the previous Aaron row's "Next Search" (column G) as completed by appending " ✓".

Save the updated spreadsheet back to the same path.

---

⚠️  REMINDER: After reviewing results, run CONSOLIDATE_TO_MASTER.md to update Aaron's master database (if applicable).

---

*Run every Sunday. Attach Aaron's resume each time.*
*Created: 2026-02-15*
*Based on executed search from 2026-02-12 (Week of Feb 9)*

---

## SEARCH NOTES (Joey's reference — don't copy into prompt)

### Observations from Week 1 (Feb 9):
- Miami returned zero results — dropped from locations, replaced with Stamford/Greenwich CT
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
5. Drop Miami, add Stamford/Greenwich CT (done)
6. Consider adding salary floor filter ($130K minimum)
