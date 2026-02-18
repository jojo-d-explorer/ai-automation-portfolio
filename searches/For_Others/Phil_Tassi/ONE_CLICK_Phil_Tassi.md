# ONE-CLICK WEEKLY SEARCH: PHIL TASSI

**Owner:** Joey Clark (running on behalf of Phil Tassi)
**Resume file:** Phillip Tassi - Resume - November 2025 (3).pdf
**Created:** 2026-02-01
**Last updated:** 2026-02-17 (v2.0 — added xlsx output, 14-column format, LinkedIn, data/deliverables subfolders)

---

## How to Use
1. Copy everything from "Calculate today's date..." to "...where everything was saved"
2. Paste into CoWork
3. Attach resume: `Phillip Tassi - Resume - November 2025 (3).pdf`
4. Hit enter
5. Walk away for 10-15 minutes
6. Come back to results in deliverables/ folder

---

## THE PROMPT

Calculate today's date and determine:
- Current week start date (most recent Monday): CURRENT_WEEK
- Previous week start date (Monday before that): PREVIOUS_WEEK

Define path variables:
- BASE_PATH = /Users/jc3/GitHub/ai-automation-portfolio
- RESULTS_PATH = {BASE_PATH}/results/For_Others/Phil_Tassi/Week_of_CURRENT_WEEK
- PREVIOUS_RESULTS = {BASE_PATH}/results/For_Others/Phil_Tassi/Week_of_PREVIOUS_WEEK

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
- Chief of Staff
- Partnerships
- Business Development

**Locations:**
- Washington, DC
- London, UK

**Filters:**
- Posted within last 7 days
- For each board/role/location combination, extract up to 20 results (paginate to page 2 if needed)

Show progress matrix as you search each combination (4 boards × 3 roles × 2 locations = 24 combinations).

---

### SOURCE FILTERING

Only include results hosted directly on the target ATS boards or the company's own careers domain.

**Exclude all third-party job aggregators** including but not limited to: Jobgether, Talent.com, Lensa, Jooble, Adzuna, SimplyHired, ZipRecruiter, Snagajob.

**URL Verification:**
For each result, verify the URL resolves to an active job listing. If the URL is broken or redirects to a general careers page, attempt to reconstruct the direct ATS link using standard board URL formats:
- Greenhouse: boards.greenhouse.io/[company]/jobs/[id]
- Lever: jobs.lever.co/[company]/[id]
- Ashby: jobs.ashby.com/[company]/[id] or [company].ashbyhq.com
- LinkedIn: linkedin.com/jobs/view/[id]

If the URL cannot be verified or reconstructed, mark URL_Status as "Unverified." Otherwise mark as "Verified."

---

### FIELD EXTRACTION

Extract these fields (use "N/A" if not available):
- Company
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
- **Remote-Americas** — Any variant of "Remote" + "Americas/LATAM/Canada", or remote with Latin American country
- **Remote-Global** — Generic "Remote" without geographic qualifier, or "Remote Worldwide/EMEA/Europe"
- **Hybrid** — Any hybrid arrangement, including "Remote/Hybrid" variants
- **In-Office** — Location-specific roles without Remote/Hybrid (e.g., "London", "Washington DC")

Do not leave Work_Arrangement as generic "Remote" — always classify into the specific category above.

---

### DEDUPLICATION

Eliminate duplicate jobs (same Company + same Job Title across boards). Keep highest-scoring version and list all boards where found in "Found_On" column.

---

### SCORING

Using attached resume (Phillip Tassi - Resume - November 2025 (3).pdf), score each job 1-100 based on:

**Skills Fit (40 points):**
- Key skills: Strategic partnerships, business development, stakeholder management, cross-functional leadership
- Score based on overlap between resume skills and job requirements

**Industry Alignment (35 points):**
- Strong fit: Fintech, AI/ML, financial services, payments, digital banking
- Moderate fit: B2B SaaS, enterprise technology, marketplace platforms
- Lower fit: Consumer tech, non-tech sectors

**Experience Match (25 points):**
- Score based on resume experience level alignment with role requirements
- Phil has 10+ years of experience — roles expecting <5 years should be penalized

Provide 1-2 sentence score rationale for each job.

Filter to jobs scoring 70+ only. Rank by score (highest to lowest).

---

### NEW JOB DETECTION

Compare against previous week's Master List. Check in this order:
1. First check: {PREVIOUS_RESULTS}/data/Master_List_PREVIOUS_WEEK.csv
2. Legacy fallback: {PREVIOUS_RESULTS}/Master_List_PREVIOUS_WEEK.csv
3. Original legacy: {BASE_PATH}/results/For_Others/Phil_Tassi_Search_2026-02-01.csv

- If file exists (any location): Mark jobs not in previous file as "NEW", matching jobs as "REPEAT"
- If no previous file found (first run): Mark all jobs as "NEW"
- Add "Status" column with "NEW" or "REPEAT"

---

### OUTPUT FILES

**Data files (backbone for consolidation — not shared with Phil):**

1. **Master List CSV:** {RESULTS_PATH}/data/Master_List_CURRENT_WEEK.csv
   Columns (in this order): Status | Score | Score_Rationale | Company | Job_Title | Sector | Location | Language_Requirement | Work_Arrangement | Salary_USD | Job_Summary | URL | URL_Status | Found_On

2. **Top 10 New CSV:** {RESULTS_PATH}/data/Top10_New_CURRENT_WEEK.csv
   Same columns, only top 10 jobs marked "NEW". If <10 new jobs, include all new jobs. If zero new jobs, create file with headers and note "No new jobs this week."

3. **Executed prompt:** {BASE_PATH}/searches/For_Others/Phil_Tassi/executed_CURRENT_WEEK.txt

**Deliverable files (shared with Phil):**

4. **Branded Excel — Master List:** {RESULTS_PATH}/deliverables/Phil_Tassi_Master_List_CURRENT_WEEK.xlsx

   Generate a formatted .xlsx version of the Master List CSV:
   - Row 1: Title "Phil Tassi — Master Job List" (bold, 18pt, navy #1F3864, merged across all columns)
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

5. **Branded Excel — Top 10:** {RESULTS_PATH}/deliverables/Phil_Tassi_Top10_New_CURRENT_WEEK.xlsx
   Same formatting as item 4, with title: "Phil Tassi — Top 10 New Opportunities"

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
| Role/location combinations | 24 |

**Files saved at:**
- Master List CSV: [full path]
- Top 10 CSV: [full path]
- Master List Excel: [full path]
- Top 10 Excel: [full path]
- Executed prompt: [full path]

Report any errors, broken URLs, or boards that returned zero results.

---

### JOB SEARCH TRACKING UPDATE

After all output files are saved, update the tracking spreadsheet:

**File:** {BASE_PATH}/Job_Search_Tracking.xlsx
**Sheet:** "Job Search Tracking"

Find the rows for **Phil Tassi** (look for name in column A). Add a new continuation row immediately after the last Phil row with:

| Column | Value |
|--------|-------|
| C (Search Ran) | Today's date (YYYY-MM-DD) |
| D (Results 70+) | Total jobs scoring 70+ |
| E (Top Score) | Highest score in this search |
| F (Search Config) | 4 boards \| COS, Partnerships, BD \| DC, London |
| G (Next Search) | CURRENT_WEEK + 7 days (YYYY-MM-DD) |
| H (Link to Folder) | Phil_Tassi/Week_of_CURRENT_WEEK/ |

Also mark the previous Phil row's "Next Search" (column G) as completed by appending " ✓".

Save the updated spreadsheet back to the same path.

---

⚠️  REMINDER: After reviewing results, run CONSOLIDATE_TO_MASTER to update Phil's master database. After consolidation (Week 2+), run MASTER_ANALYSIS to generate the PDF analysis report in {RESULTS_PATH}/deliverables/.

---

*Run every Sunday. Attach Phil's resume each time.*
*Template version: 2.0 | Updated: 2026-02-17*
