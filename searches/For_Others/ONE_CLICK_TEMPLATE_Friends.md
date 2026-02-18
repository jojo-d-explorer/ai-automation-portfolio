# ONE-CLICK WEEKLY SEARCH: [FRIEND NAME] — TEMPLATE

**Purpose:** Duplicate this file for each new friend. Replace all [BRACKETED] values with their intake questionnaire responses. Save as `ONE_CLICK_[First_Last].md` in `/searches/prompts/for_others/[First_Last]/`.
**Runtime:** 10-15 minutes
**Prerequisites:** Friend's resume (PDF), completed intake questionnaire

**Setup checklist before first run:**
- [ ] Friend completed intake questionnaire
- [ ] Resume received (PDF) at joey.clark3@gmail.com
- [ ] Replaced all [BRACKETED] fields below
- [ ] Created results folder: `/results/For_Others/[First_Last]/`
- [ ] Saved this file as `ONE_CLICK_[First_Last].md`

---

**Owner:** Joey Clark (running on behalf of [FRIEND NAME])
**Resume file:** [RESUME FILENAME.pdf]
**Created:** [DATE]
**Last updated:** [DATE]

---

## CUSTOMIZATION CHECKLIST

Before running, collect from friend:
- [ ] **Name:** [Friend's full name]
- [ ] **Resume:** [Attach their resume PDF]
- [ ] **Target Roles:** [2-3 specific role titles]
  - Examples: "Chief of Staff", "Partnerships", "Business Development"
- [ ] **Target Locations:** [Specific cities or Remote]
  - Examples: "Remote-US", "London, UK", "New York, NY"
- [ ] **Target Sectors:** (optional — for context)
  - Examples: "Fintech", "Healthcare Tech", "AI/ML"
- [ ] **Salary Range:** (optional)
  - Example: "$120K-$180K"
- [ ] **Deal-Breakers:** (optional — becomes exclusion filters)
  - Examples: "Exclude fully in-office roles", "Full-time only, no contract", "Exclude roles requiring 10+ years travel"
- [ ] **Priority Ranking 1-5:** Industry Fit, Skills Match, Seniority, Location, Salary
  - Used to adjust scoring weights (see Weight Adjustment Guide at bottom)

---

## USAGE INSTRUCTIONS

1. Copy everything from "Calculate today's date..." to "...where everything was saved"
2. Paste into CoWork
3. Attach: [RESUME FILENAME.pdf]
4. Hit enter
5. Walk away for 10-15 minutes
6. Come back to results

**Note:** Remote-US roles consistently score 10+ points higher than location-specific roles. Consider focusing searches on Remote unless friend specifically targets a city.

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

**Job Boards (search all):**
- site:boards.greenhouse.io
- site:jobs.lever.co
- site:jobs.ashbyhq.com
- site:linkedin.com/jobs

[ADD/REMOVE BOARDS AS NEEDED — e.g., for finance roles, these ATS boards may have limited coverage. Consider supplementing with industry-specific channels.]

**Roles:**
[FROM INTAKE — list 3-5 specific titles]
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
- For each board/role/location combination, extract up to 20 results (paginate to page 2 if needed)

Show progress matrix as you search each combination.

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
- **In-Office** — Location-specific roles without Remote/Hybrid (e.g., "New York, NY", "Paris", "Vienna")

Do not leave Work_Arrangement as generic "Remote" — always classify into the specific category above.

---

### DEDUPLICATION

Eliminate duplicate jobs (same Company + same Job Title across boards). Keep highest-scoring version and list all boards where found in "Found_On" column.

---

### SCORING

Using attached resume ([RESUME FILENAME.pdf]), score each job 1-100 based on:

[SCORING WEIGHTS — adjust based on intake priority ranking. Default weights below. See Weight Adjustment Guide at bottom of this file.]

**Industry Fit ([X] points):**
[FROM INTAKE — define what "good fit" means for this person's target industry]
- [Full credit criteria]
- [Partial credit criteria]
- [Minimal credit criteria]

**Skills Match ([X] points):**
[FROM INTAKE — their top skills]
- Key skills to match: [Skill 1], [Skill 2], [Skill 3]
- Score based on overlap between resume skills and job requirements

**Seniority Match ([X] points):**
- Score based on resume experience alignment with role requirements

**Location Flexibility ([X] points):**
- Role is in a target location: full credit
- Remote with flexibility: full credit
- Hybrid in target city: [X]/[max]
- Outside target locations: [X]/[max]

**Salary Fit ([X] points):**
[FROM INTAKE]
- Target: $[X]K+ base salary, $[X]K+ total compensation
- If salary listed and meets target: full credit
- If salary listed but below target: score proportionally
- If salary not listed ("N/A"): award [half points] (neutral — don't penalize unknown)

Provide 1-2 sentence score rationale for each job.

Filter to jobs scoring 70+ only. Rank by score (highest to lowest).

---

### NEW JOB DETECTION

Compare against previous week's Master List. Check in this order:
1. First check: {BASE_PATH}/results/For_Others/[First_Last]/Week_of_PREVIOUS_WEEK/data/Master_List_PREVIOUS_WEEK.csv
2. Legacy fallback: {BASE_PATH}/results/For_Others/[First_Last]/Week_of_PREVIOUS_WEEK/Master_List_PREVIOUS_WEEK.csv

- If file exists (either location): Mark jobs not in previous file as "NEW", matching jobs as "REPEAT"
- If no previous file found (first run): Mark all jobs as "NEW"
- Add "Status" column with "NEW" or "REPEAT"

---

### OUTPUT FILES

Create folders if they don't exist:
- {RESULTS_PATH}/data/
- {RESULTS_PATH}/deliverables/
- {BASE_PATH}/searches/prompts/for_others/[First_Last]/

**Data files (backbone for consolidation — not shared with friend):**

1. **Master List CSV:** {RESULTS_PATH}/data/Master_List_CURRENT_WEEK.csv
   Columns (in this order): Status | Score | Score_Rationale | Company | Job_Title | Sector | Location | Language_Requirement | Work_Arrangement | Salary_USD | Job_Summary | URL | URL_Status | Found_On

2. **Top 10 New CSV:** {RESULTS_PATH}/data/Top10_New_CURRENT_WEEK.csv
   Same columns, only top 10 jobs marked "NEW". If <10 new jobs, include all new jobs. If zero new jobs, create file with headers and note "No new jobs this week."

3. **Executed prompt:** {BASE_PATH}/searches/prompts/for_others/[First_Last]/executed_CURRENT_WEEK.txt

**Deliverable files (shared with friend):**

4. **Branded Excel — Master List:** {RESULTS_PATH}/deliverables/[First_Last]_Master_List_CURRENT_WEEK.xlsx

   Generate a formatted .xlsx version of the Master List CSV:
   - Row 1: Title "[Friend Name] — Master Job List" (bold, 18pt, navy #1F3864, merged across all columns)
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

5. **Branded Excel — Top 10:** {RESULTS_PATH}/deliverables/[First_Last]_Top10_New_CURRENT_WEEK.xlsx
   Same formatting as item 4, with title: "[Friend Name] — Top 10 New Opportunities"

---

### VERIFICATION

Verify all files saved. Show:

| Metric | Count |
|--------|-------|
| Total jobs found (pre-filter) | X |
| Jobs scoring 70+ (post-filter) | Y |
| NEW jobs | Z |
| REPEAT jobs | W |
| Boards searched | [N] |
| Role/location combinations | [N] |

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

Find the rows for **[FRIEND NAME]** (look for name in column A). Add a new continuation row immediately after the last [FRIEND NAME] row with:

| Column | Value |
|--------|-------|
| C (Search Ran) | Today's date (YYYY-MM-DD) |
| D (Results 70+) | Total jobs scoring 70+ |
| E (Top Score) | Highest score in this search |
| F (Search Config) | Boards searched \| Roles \| Locations (short summary) |
| G (Next Search) | CURRENT_WEEK + 7 days (YYYY-MM-DD) |
| H (Link to Folder) | [First_Last]/Week_of_CURRENT_WEEK/ |

Also mark the previous [FRIEND NAME] row's "Next Search" (column G) as completed by appending " ✓".

Save the updated spreadsheet back to the same path.

---

⚠️  REMINDER: After reviewing results, run CONSOLIDATE_TO_MASTER to update [First_Last]'s master database. After consolidation (Week 2+), run MASTER_ANALYSIS to generate the PDF analysis report in {RESULTS_PATH}/deliverables/.

---

## USAGE NOTES

**Before sharing with friend:**
- Run the search yourself first
- Review results for quality
- Customize score threshold if needed (might be 65+ or 75+ depending on their profile)
- Check that excluded aggregators didn't sneak through

**After running:**
- Send friend the .xlsx files from the deliverables/ folder (NOT the raw CSVs)
- Explain scoring methodology briefly
- Highlight top 3-5 jobs worth applying to immediately
- If Week 2+, include the PDF analysis report from MASTER_ANALYSIS

---

*Run every Sunday. Attach [First_Last]'s resume each time.*

---
---

## WEIGHT ADJUSTMENT GUIDE (Joey's reference — don't copy into prompt)

**Default weights (100 points total):**
- Industry Fit: 35
- Skills Match: 25
- Seniority Match: 20
- Location Flexibility: 10
- Salary Fit: 10

**How to adjust based on intake priority ranking (1-5):**

| Their #1 Priority | Suggested Adjustment |
|---|---|
| Salary | Salary → 30pts, reduce Industry to 25 |
| Location | Location → 25pts, reduce Skills to 20 |
| Skills Match | Skills → 35pts, reduce Industry to 25 |
| Industry Fit | Industry → 40pts (already high, keep) |
| Seniority | Seniority → 30pts, reduce Location to 10 |

**General principle:** Their #1 gets 35-40pts, #5 gets 10pts, middle three split the rest. Use judgment — some categories overlap for certain industries.

---

*Template version: 2.0*
*Updated: 2026-02-17*
*Changes from v1.0: Added data/deliverables subfolder structure, branded xlsx output, corrected path convention to For_Others/[First_Last], added path variables, legacy fallback for NEW detection, PDF reminder for MASTER_ANALYSIS*
