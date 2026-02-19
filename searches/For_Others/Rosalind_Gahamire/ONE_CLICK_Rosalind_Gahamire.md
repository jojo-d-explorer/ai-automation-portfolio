# ONE-CLICK WEEKLY SEARCH: ROSALIND GAHAMIRE

**Owner:** Joey Clark (running on behalf of Rosalind Gahamire)
**Resume file:** Rosalind_Gahamire_CV_2026.pdf
**Created:** 2026-02-18
**Last updated:** 2026-02-18

---

**Setup checklist:**
- [x] Friend completed intake questionnaire
- [x] Resume received (PDF)
- [x] Replaced all bracketed fields
- [x] Created results folder: `results/For_Others/Rosalind_Gahamire/`
- [x] Saved ONE_CLICK file

---

## USAGE INSTRUCTIONS

1. Copy everything from "Calculate today's date..." to "...where everything was saved"
2. Paste into CoWork
3. Attach: Rosalind_Gahamire_CV_2026.pdf
4. Hit enter
5. Walk away for 10-15 minutes
6. Come back to results

---

## THE PROMPT

Calculate today's date and determine:
- Current week start date (most recent Monday): CURRENT_WEEK
- Previous week start date (Monday before that): PREVIOUS_WEEK

Use these dates for file paths and comparisons below.

Define path variables:
- BASE_PATH = /Users/jc3/GitHub/ai-automation-portfolio
- RESULTS_PATH = {BASE_PATH}/results/For_Others/Rosalind_Gahamire/Week_of_CURRENT_WEEK

---

### CONFIGURATION

**Job Boards (search all):**
- site:boards.greenhouse.io
- site:jobs.lever.co
- site:jobs.ashbyhq.com
- site:linkedin.com/jobs

Note: Rosalind is based in Lisbon and targets European/global remote roles. LinkedIn will likely produce the strongest results for European creative roles. Greenhouse and Lever have decent coverage for D2C brands with international presence. If first search yields <15 results, consider supplementing with: WeWorkRemotely, Remote OK, or targeted career page checks for major D2C brands and creative agencies with Lisbon/European presence.

**Roles:**
- Brand Strategist
- Creative Strategist
- Marketing Manager

**Search Archetypes:**
These roles cluster into two career path archetypes:
1. **Strategy Track:** Brand Strategist, Creative Strategist, Brand Strategy Manager, Creative Strategy Lead, Head of Brand Strategy
2. **Marketing Leadership Track:** Marketing Manager, Brand Marketing Manager, Creative Marketing Lead, Senior Marketing Manager

When searching, use both the exact titles above AND these related variants to maximize coverage.

**Locations:**
- Lisbon, Portugal
- Remote

**HARD LOCATION FILTER:** Only include roles where the primary work location is Lisbon, Portugal OR the role is fully remote (Remote-Global or Remote-Europe/EMEA). Exclude Remote-US and Remote-Americas roles — Rosalind is based in Lisbon and cannot work US/Americas-restricted remote roles. Also exclude In-Office roles outside of Lisbon.

**Language Note:** Rosalind speaks English (Native) and Portuguese (B2). Roles requiring fluent Portuguese are acceptable. Flag roles requiring any other language in the Language_Requirement field.

**Filters:**
- Posted within last 7 days
- EXCLUDE roles that are Remote-US only or Remote-Americas only
- EXCLUDE In-Office roles outside Lisbon
- Full-time roles only (no contract/freelance unless explicitly "freelance-to-permanent")
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
- Salary (convert to USD if in EUR or other currency; "N/A" if not listed)
- Job Summary (2-3 sentences)
- URL

---

### WORK ARRANGEMENT STANDARDIZATION

Normalize Work_Arrangement to one of these 5 categories:

- **Remote-US** — Any variant of "Remote" + "US/USA/United States", or remote with US city qualifier
- **Remote-Americas** — Any variant of "Remote" + "Americas/LATAM/Canada", or remote with Latin American country
- **Remote-Global** — Generic "Remote" without geographic qualifier, or "Remote Worldwide/EMEA/Europe"
- **Hybrid** — Any hybrid arrangement, including "Remote/Hybrid" variants
- **In-Office** — Location-specific roles without Remote/Hybrid (e.g., "Lisbon", "London", "Berlin")

Do not leave Work_Arrangement as generic "Remote" — always classify into the specific category above.

**For Rosalind's search:** After classification, EXCLUDE any jobs classified as Remote-US or Remote-Americas. Keep: Remote-Global, Hybrid (Lisbon only), In-Office (Lisbon only).

---

### DEDUPLICATION

Eliminate duplicate jobs (same Company + same Job Title across boards). Keep highest-scoring version and list all boards where found in "Found_On" column.

---

### SCORING

Using attached resume (Rosalind_Gahamire_CV_2026.pdf), score each job 1-100 based on:

**Rosalind's priority ranking:** Location #1, Skills Match #2, Industry Fit #3, Salary #4, Seniority #5

**Location Flexibility (30 points):**
- Lisbon-based (In-Office or Hybrid): 30/30
- Remote-Global with no geographic restriction: 30/30
- Remote-Europe/EMEA: 25/30
- Hybrid in another European city: 10/30
- Remote-US or Remote-Americas: 0/30 (auto-exclude, but score 0 if somehow included)

**Skills Match (25 points):**
Rosalind's core skills from her CV:
- Brand strategy & positioning
- Insight-led research (qualitative + quantitative)
- Workshop planning & facilitation
- Creative direction & concept development
- Brand purpose, value propositions & messaging frameworks
- Client & stakeholder communication
- Design literacy & collaboration with creative teams

Score based on overlap between these skills and job requirements:
- 5+ skills overlap: 25/25
- 3-4 skills overlap: 18/25
- 1-2 skills overlap: 10/25
- No overlap: 5/25

**Industry Fit (20 points):**
Target sectors (from intake):
- D2C consumer brands: 20/20 (perfect fit — she has direct D2C experience at Undandy and Bond Touch)
- Creative/brand agencies: 20/20 (perfect fit — she has agency experience at ACT.3 and Rankin)
- Consumer tech / lifestyle brands: 15/20
- Fashion, beauty, wellness, food & beverage: 15/20
- SaaS/B2B with strong brand focus: 12/20
- Traditional corporate / heavy industry: 5/20

**Salary Fit (15 points):**
No salary floor specified. Score generously:
- Salary listed and appears competitive for role level: 15/15
- Salary listed but appears below market: 10/15
- Salary not listed ("N/A"): 12/15 (neutral-positive — don't penalize unknown)

**Seniority Match (10 points):**
Rosalind has 8+ years of experience. Target seniority: Mid-Senior (Manager, Lead, Senior Strategist level).
- Manager / Lead / Senior level: 10/10
- Director level: 8/10 (stretch but possible)
- Junior / Associate level: 3/10
- VP / C-level: 5/10 (likely overqualified requirements)

Provide 1-2 sentence score rationale for each job.

Filter to jobs scoring 70+ only. Rank by score (highest to lowest).

---

### NEW JOB DETECTION

Compare against previous week's Master List. Check in this order:
1. First check: {BASE_PATH}/results/For_Others/Rosalind_Gahamire/Week_of_PREVIOUS_WEEK/data/Master_List_PREVIOUS_WEEK.csv
2. Legacy fallback: {BASE_PATH}/results/For_Others/Rosalind_Gahamire/Week_of_PREVIOUS_WEEK/Master_List_PREVIOUS_WEEK.csv

- If file exists (either location): Mark jobs not in previous file as "NEW", matching jobs as "REPEAT"
- If no previous file found (first run): Mark all jobs as "NEW"
- Add "Status" column with "NEW" or "REPEAT"

---

### OUTPUT FILES

Create folders if they don't exist:
- {RESULTS_PATH}/data/
- {RESULTS_PATH}/deliverables/
- {BASE_PATH}/searches/For_Others/Rosalind_Gahamire/

**Data files (backbone for consolidation — not shared with friend):**

1. **Master List CSV:** {RESULTS_PATH}/data/Master_List_CURRENT_WEEK.csv
   Columns (in this order): Status | Score | Score_Rationale | Company | Job_Title | Sector | Location | Language_Requirement | Work_Arrangement | Salary_USD | Job_Summary | URL | URL_Status | Found_On

2. **Top 10 New CSV:** {RESULTS_PATH}/data/Top10_New_CURRENT_WEEK.csv
   Same columns, only top 10 jobs marked "NEW". If <10 new jobs, include all new jobs. If zero new jobs, create file with headers and note "No new jobs this week."

3. **Executed prompt:** {BASE_PATH}/searches/For_Others/Rosalind_Gahamire/executed_CURRENT_WEEK.txt

**Deliverable files (shared with friend):**

4. **Branded Excel — Master List:** {RESULTS_PATH}/deliverables/Rosalind_Gahamire_Master_List_CURRENT_WEEK.xlsx

   Generate a formatted .xlsx version of the Master List CSV:
   - Row 1: Title "Rosalind Gahamire — Master Job List" (bold, 18pt, navy #1F3864, merged across all columns)
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

5. **Branded Excel — Top 10:** {RESULTS_PATH}/deliverables/Rosalind_Gahamire_Top10_New_CURRENT_WEEK.xlsx
   Same formatting as item 4, with title: "Rosalind Gahamire — Top 10 New Opportunities"

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

Find the rows for **Rosalind Gahamire** (look for name in column A). Add a new continuation row immediately after the last Rosalind Gahamire row with:

| Column | Value |
|--------|-------|
| C (Search Ran) | Today's date (YYYY-MM-DD) |
| D (Results 70+) | Total jobs scoring 70+ |
| E (Top Score) | Highest score in this search |
| F (Search Config) | Boards searched \| Roles \| Locations (short summary) |
| G (Next Search) | CURRENT_WEEK + 7 days (YYYY-MM-DD) |
| H (Link to Folder) | Rosalind_Gahamire/Week_of_CURRENT_WEEK/ |

Also mark the previous Rosalind Gahamire row's "Next Search" (column G) as completed by appending " ✓".

Save the updated spreadsheet back to the same path.

---

⚠️  REMINDER: After reviewing results, run CONSOLIDATE_TO_MASTER to update Rosalind_Gahamire's master database. After consolidation (Week 2+), run MASTER_ANALYSIS to generate the PDF analysis report in {RESULTS_PATH}/deliverables/.

---

## NOTES

**Rosalind's unique considerations:**
- **Europe-based search:** Unlike other friends (US-focused), Rosalind is in Lisbon. Remote-US roles are useless to her. Focus on Remote-Global and Lisbon-based.
- **Creative/brand background:** She has a design + strategy hybrid background (UAL + IADE). This is a differentiator — she bridges visual design and strategic thinking.
- **Agency + brand-side experience:** ACT.3 (agency), Bond Touch (D2C brand), Undandy (D2C brand), Rankin (agency). She can go either direction.
- **Portuguese B2 is an asset:** For Lisbon-based roles, this opens doors at Portuguese companies and international companies with Lisbon offices.
- **8+ years experience:** Target mid-senior roles (Manager, Lead, Senior). Not entry level, not yet Director unless it's a smaller company.

---

*Run every Sunday. Attach Rosalind_Gahamire_CV_2026.pdf each time.*
