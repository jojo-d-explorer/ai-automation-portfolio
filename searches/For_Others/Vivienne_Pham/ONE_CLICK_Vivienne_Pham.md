# ONE-CLICK WEEKLY SEARCH: VIVIENNE PHAM

**Owner:** Joey Clark (running on behalf of Vivienne Pham)
**Resume file:** Vivienne_Pham_Resume_2026.pdf
**Created:** 2026-02-15
**Last updated:** 2026-02-17 (v2.0 — added data/deliverables subfolders, branded xlsx output, path variables, security clearance handling)

---

## How to Use
1. Copy everything from "Calculate today's date..." to "...where everything was saved"
2. Paste into CoWork
3. Attach: Vivienne_Pham_Resume_2026.pdf
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
- RESULTS_PATH = {BASE_PATH}/results/For_Others/Vivienne_Pham/Week_of_CURRENT_WEEK
- PREVIOUS_RESULTS = {BASE_PATH}/results/For_Others/Vivienne_Pham/Week_of_PREVIOUS_WEEK

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

**Roles (organized by archetype — search all):**

*Archetype 1: Operator / Finance Leader*
- CFO
- VP Finance
- Head of Finance

*Archetype 2: Capital Markets & Investor Relations*
- Capital Markets Advisory
- Investor Relations
- Head of Investor Relations

*Archetype 3: Ecosystem / Platform / BD*
- Portfolio Operations
- Platform Manager
- Business Development

**Locations:**
- New York, NY
- Washington, DC
- Remote

**Hard Location Filter:**
Only include roles where the primary work location is New York, Washington DC, or Remote-US. If a role lists dual locations (e.g., "Costa Mesa, CA / Washington, DC"), include it only if NYC or DC is one of the options. Exclude all roles based solely in other cities (SF, Austin, Germany, etc.) even if they appear in search results.

**Filters:**
- Posted within last 7 days
- Exclude roles with "Investment Banking Analyst" or "Investment Banking Associate" in the title
- For each board/role/location combination, extract up to 20 results (paginate to page 2 if needed)

Show progress matrix as you search each combination (4 boards × 9 roles × 3 locations = 108 combinations).

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
- **Remote-Americas** — Any variant of "Remote" + "Americas/LATAM/Canada"
- **Remote-Global** — Generic "Remote" without geographic qualifier, or "Remote Worldwide/EMEA/Europe"
- **Hybrid** — Any hybrid arrangement, including "Remote/Hybrid" variants
- **In-Office** — Location-specific roles without Remote/Hybrid (e.g., "New York, NY", "Washington, DC")

Do not leave Work_Arrangement as generic "Remote" — always classify into the specific category above.

---

### COMPANY SIZE FILTERING

Vivienne targets small and mid-cap companies. Apply these guidelines:

**Include:**
- Startups (Series A through pre-IPO / growth stage)
- Public companies that are NOT Fortune 200 / mega-cap
- VC/PE firms (any size — she's interested in platform/BD roles)
- Government contractors and defense tech companies (any size — sector fit overrides size)

**Exclude:**
- Fortune 200 companies (e.g., JPMorgan, Goldman Sachs, Microsoft, Amazon, Google)
- Exception: If a Fortune 200 company has a standalone venture arm, defense tech subsidiary, or growth-stage spinout that operates independently, include it

Use judgment — the spirit is "growth-stage and mid-market," not "only tiny companies."

---

### SECURITY CLEARANCE HANDLING

Many defensetech roles require or prefer US security clearance. Vivienne does not currently hold a clearance.

- If a posting mentions security clearance as "required": apply -15 point penalty in scoring, flag in Score_Rationale as "Clearance required — Vivienne does not currently hold clearance"
- If a posting mentions clearance as "preferred" or "ability to obtain": apply -5 point penalty, note in rationale
- If no mention of clearance: no penalty
- Do NOT exclude clearance-required roles entirely — some companies sponsor clearances for strong candidates

---

### DEDUPLICATION

Eliminate duplicate jobs (same Company + same Job Title across boards). Keep highest-scoring version and list all boards where found in "Found_On" column.

---

### SCORING

Using attached resume (Vivienne_Pham_Resume_2026.pdf), score each job 1-100 based on:

**Seniority Match (30 points):**
Vivienne is an Executive Director at JPM with 15+ years of experience spanning IB, law, and infrastructure policy. She should be targeting Director, VP, Head-of, or C-suite roles.
- C-suite / Head of / Director level at growth company: full credit
- VP level: 25/30
- Senior Manager / Principal: 20/30
- Manager or below: 10/30
- Entry-level / Associate: 0/30

**Skills Match (25 points):**
Key skills: building networks, bringing relevant content and ideas, building trust and credibility, understanding business models. Also has deep IB execution skills (M&A advisory, capital markets, debt/equity), legal/regulatory background, and resource management experience.
- Role requires capital markets, fundraising, investor-facing, or financial strategy skills: full credit
- Role requires business development, partnerships, or ecosystem building: full credit
- Role requires operational finance (FP&A, budgeting, financial modeling): 20/25
- Role requires general management but not finance-specific: 15/25
- Role requires skills outside her background: 5/25

**Location Flexibility (20 points):**
- New York, NY: full credit
- Washington, DC: full credit
- Remote-US: full credit
- Hybrid in NYC or DC: 18/20
- Remote-Global: 15/20
- Other US cities: 0/20 (hard filter — should not appear, but if they slip through, score at 0)

**Industry Fit (15 points):**
Vivienne targets tech, defensetech, cybersecurity, and AI — especially companies with public sector, federal defense, or energy exposure.
- Defensetech / cybersecurity / national security tech: full credit
- AI/ML companies with government or defense contracts: full credit
- Energy tech / climate tech with infrastructure angle: 13/15
- General enterprise tech (SaaS, fintech): 10/15
- Adjacent sectors (govtech, aerospace, dual-use): 10/15
- Unrelated sectors (consumer, healthcare, retail): 5/15

**Salary Fit (10 points):**
- Target: $250K+ total compensation
- If salary listed and meets target: full credit
- If salary listed but below target: score proportionally
- If salary not listed ("N/A"): award 5/10 (neutral — don't penalize unknown)

Provide 1-2 sentence score rationale for each job.

Filter to jobs scoring 70+ only. Rank by score (highest to lowest).

---

### NEW JOB DETECTION

Compare against previous week's Master List. Check in this order:
1. First check: {PREVIOUS_RESULTS}/data/Master_List_PREVIOUS_WEEK.csv
2. Legacy fallback: {PREVIOUS_RESULTS}/Master_List_PREVIOUS_WEEK.csv

- If file exists (either location): Mark jobs not in previous file as "NEW", matching jobs as "REPEAT"
- If no previous file found (first run): Mark all jobs as "NEW"
- Add "Status" column with "NEW" or "REPEAT"

---

### OUTPUT FILES

**Data files (backbone for consolidation — not shared with Vivienne):**

1. **Master List CSV:** {RESULTS_PATH}/data/Master_List_CURRENT_WEEK.csv
   Columns (in this order): Status | Score | Score_Rationale | Company | Job_Title | Sector | Location | Language_Requirement | Work_Arrangement | Salary_USD | Job_Summary | URL | URL_Status | Found_On

2. **Top 10 New CSV:** {RESULTS_PATH}/data/Top10_New_CURRENT_WEEK.csv
   Same columns, only top 10 jobs marked "NEW". If <10 new jobs, include all new jobs. If zero new jobs, create file with headers and note "No new jobs this week."

3. **Executed prompt:** {BASE_PATH}/searches/For_Others/Vivienne_Pham/executed_CURRENT_WEEK.txt

**Deliverable files (shared with Vivienne):**

4. **Branded Excel — Master List:** {RESULTS_PATH}/deliverables/Vivienne_Pham_Master_List_CURRENT_WEEK.xlsx

   Generate a formatted .xlsx version of the Master List CSV:
   - Row 1: Title "Vivienne Pham — Master Job List" (bold, 18pt, navy #1F3864, merged across all columns)
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

5. **Branded Excel — Top 10:** {RESULTS_PATH}/deliverables/Vivienne_Pham_Top10_New_CURRENT_WEEK.xlsx
   Same formatting as item 4, with title: "Vivienne Pham — Top 10 New Opportunities"

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
| Role/location combinations | 108 |

**Files saved at:**
- Master List CSV: [full path]
- Top 10 CSV: [full path]
- Master List Excel: [full path]
- Top 10 Excel: [full path]
- Executed prompt: [full path]

Report any errors, broken URLs, or boards that returned zero results.

Also show breakdown by archetype:
- Operator / Finance Leader roles found: X
- Capital Markets & IR roles found: X
- Ecosystem / Platform / BD roles found: X

---

### JOB SEARCH TRACKING UPDATE

After all output files are saved, update the tracking spreadsheet:

**File:** {BASE_PATH}/Job_Search_Tracking.xlsx
**Sheet:** "Job Search Tracking"

Find the rows for **Vivienne Pham** (look for name in column A). Add a new continuation row immediately after the last Vivienne row with:

| Column | Value |
|--------|-------|
| C (Search Ran) | Today's date (YYYY-MM-DD) |
| D (Results 70+) | Total jobs scoring 70+ |
| E (Top Score) | Highest score in this search |
| F (Search Config) | 4 boards \| 9 roles (3 archetypes) \| NYC, DC, Remote |
| G (Next Search) | CURRENT_WEEK + 7 days (YYYY-MM-DD) |
| H (Link to Folder) | Vivienne_Pham/Week_of_CURRENT_WEEK/ |

Also mark the previous Vivienne row's "Next Search" (column G) as completed by appending " ✓".

Save the updated spreadsheet back to the same path.

---

⚠️  REMINDER: After reviewing results, run CONSOLIDATE_TO_MASTER to update Vivienne's master database. After consolidation (Week 2+), run MASTER_ANALYSIS to generate the PDF analysis report in {RESULTS_PATH}/deliverables/.

---

*Run every Sunday. Attach Vivienne's resume each time.*
*Template version: 2.0 | Updated: 2026-02-17*

---
---

## SEARCH NOTES (Joey's reference — don't copy into prompt)

### Vivienne's profile summary:
- Executive Director, JPM Tech IB (2017-present) + Tech Commercial Banking (2023-present)
- Associate, Morgan Stanley Global Power & Utilities IB (2014-2017, NYC + London)
- Senior Policy Analyst, Powercor/CKI Infrastructure (2010-2012, Melbourne)
- Attorney, DLA Piper Antitrust Law (2008-2010, Melbourne)
- Columbia MBA (2014), GMAT 740
- LLB + B.Econ (Hons) First Class, La Trobe University
- US Green Card holder, admitted to Australian Supreme Court and High Court
- Extensive defensetech/cybersecurity/AI coverage in DMV region
- Network across DIU, Army Fuze, Navy, Australian/Canadian Embassies, defense tech investors

### Key notes from Joey's intake conversation:
- Interpret job titles broadly — she has a wide aperture
- BD/Platform roles at VCs means early-stage ecosystem work, not fund management
- Sectors: broadly tech, but especially those with public sector/federal defense/energy exposure
- "Investment banking" as deal-breaker means IB execution work (deal teams, pitch books, live transactions), NOT roles that require IB background as a prerequisite
- 90+ hour week concern — not filtering on this, too hard to discern from postings
- Small/mid-cap = Series A+ startups through non-Fortune-200 public companies
- Similar profile to Joey (program management, ecosystem building, stakeholder coordination + finance)

### Scoring weights rationale:
Vivienne ranked: Seniority > Skills > Location > Industry > Salary
→ Seniority 30, Skills 25, Location 20, Industry 15, Salary 10
Industry is lower because she's open to broad tech — the sector preference is a tilt, not a hard filter. Seniority is #1 because at ED level she shouldn't be looking at Manager-level roles.

### Archetype search strategy:
The three archetypes capture her range without creating noise:
1. Operator (CFO, VP Finance, Head of Finance) — leverages IB financial skills in operating roles
2. Capital Markets/IR (Capital Markets Advisory, IR, Head of IR) — direct extension of IB skill set
3. Ecosystem/Platform (Portfolio Ops, Platform Manager, BD) — leverages network-building and ecosystem skills

### Board coverage notes:
- Defensetech companies (Anduril, Shield AI, Palantir, etc.) tend to post on Greenhouse and their own career pages
- VC platform roles often appear on Lever and Ashby
- LinkedIn will be important for DC-based defense/govtech roles
- May want to add defense-specific boards in future weeks if ATS coverage is thin

### Issues from first run (2026-02-16):
- Location drift: 10 of 31 results were outside NYC/DC/Remote (SF had 5, Austin, Germany, ambiguous "TBD")
- Fix applied: Hard location filter added to CONFIGURATION section, location scoring tightened to 0/20 for non-target
- Security clearance: Shield AI, Anduril, Saronic likely require clearance Vivienne doesn't hold
- Fix applied: Security clearance handling section added with -15 point penalty for required, -5 for preferred
