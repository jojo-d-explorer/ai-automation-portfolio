# ONE-CLICK WEEKLY SEARCH: PHIL TASSI — v5.0

**Unified Pipeline:** ATS API checker → Wide-net search → Merge/Dedup → Score → Output
**This prompt orchestrates the full weekly process in one run.**

---

## PIPELINE OVERVIEW

```
┌─────────────────────────────────────────────────────────────┐
│  PRE-STEP (local, before CoWork)                            │
│  1. Run: python3 ats_api_checker.py                         │
│     → reads companies.json (52+ companies, growing weekly)  │
│     → outputs api_verified_{DATE}.csv                       │
│                                                             │
│  2. (Optional) Run funding intel scan                       │
│     → new companies append to companies.json tier_4         │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│  PHASE 1: INGEST + SEARCH (this prompt, in CoWork)          │
│                                                             │
│  1A. Ingest api_verified_{DATE}.csv                         │
│      → Score all API-sourced jobs                           │
│      → Mark URL_Status = "API-Verified"                     │
│                                                             │
│  1B. Wide-net search (7 sources)                            │
│      → Google site: searches + platform searches            │
│      → Score all search-sourced jobs                        │
│      → Mark URL_Status = "Not Checked"                      │
│                                                             │
│  PHASE 2: MERGE + DEDUP                                     │
│      → Combine 1A + 1B                                      │
│      → Dedup on Company + Job_Title                         │
│      → API-sourced URL wins over Google-sourced URL         │
│                                                             │
│  PHASE 3: OUTPUT                                            │
│      → Phil_Tassi_{DATE}.csv (merged, scored, ranked)       │
│      → Phil_Tassi_{DATE}.xlsx (branded)                     │
│      → LinkedIn_Links_{DATE}.md                             │
│      → companies.json update (new companies from search)    │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│  POST-STEP (local, after CoWork)                            │
│  Run: python3 JC3/check_urls.py \                           │
│       results/For_Others/Phil_Tassi/Week_of_{DATE}/         │
│       Phil_Tassi_{DATE}.csv                                 │
│  → Only checks rows where URL_Status = "Not Checked"        │
│  → Skips "API-Verified" rows (already live)                 │
└─────────────────────────────────────────────────────────────┘
```

---

**Owner:** Joey Clark (running on behalf of Phil Tassi)
**Resume file:** Phil_Tassi_Resume.pdf
**Last updated:** 2026-03-17

---

## CHANGELOG

### v4.1 → v5.0
- Unified pipeline: ATS API checker + wide-net search + merge/dedup in one prompt
- API-sourced results marked "API-Verified" and skip check_urls
- New companies from each search automatically added to companies.json
- Funding intel feeds companies.json tier_4 (documented in pipeline)
- Added companies.json update step after search completes
- Streamlined merge/dedup logic with API-sourced URL priority

### v3.1 → v4.1
- Added 7 role titles based on resume profile analysis
- Added 4 job boards: Otta, Welcome to the Jungle, efinancialcareers, Workday
- Added 2 location targets: Remote-EMEA, Remote-Europe
- Added LinkedIn pre-built search links as standalone deliverable
- Reorganized roles into Primary (high-hit) and Secondary (expansion) tiers

---

## THE PROMPT

Calculate today's date and determine:
- Current week start date (most recent Monday): CURRENT_WEEK
- Previous week start date (Monday before that): PREVIOUS_WEEK

Define path variables:
- BASE_PATH = /Users/jc3/GitHub/ai-automation-portfolio
- RESULTS_PATH = {BASE_PATH}/results/For_Others/Phil_Tassi/Week_of_CURRENT_WEEK
- SEARCHES_PATH = {BASE_PATH}/searches/For_Others/Phil_Tassi
- API_CSV = {RESULTS_PATH}/api_verified_CURRENT_WEEK.csv

---

### PHASE 1A: INGEST API-VERIFIED RESULTS

**If `api_verified_CURRENT_WEEK.csv` exists in RESULTS_PATH:**

1. Read the CSV (columns: company_slug, title, location, url, updated, ats)
2. These are LIVE, verified-open jobs from direct ATS API calls
3. Score each job using the scoring rubric below
4. Apply the 70+ score filter
5. Set `URL_Status = "API-Verified"` for all rows
6. Set `Found_On` to the ATS name (Greenhouse/Lever/Ashby + "API")
7. Hold these results for merge in Phase 2

**If the file does not exist:** Skip Phase 1A entirely. Proceed to Phase 1B.

Report: "Phase 1A: Ingested X API-verified jobs, Y scored 70+"

---

### PHASE 1B: WIDE-NET SEARCH (7 sources)

#### CONFIGURATION

**Job Boards (7 sources):**

ATS Board Searches (Google site: operator):
- site:boards.greenhouse.io
- site:jobs.lever.co
- site:jobs.ashbyhq.com
- site:myworkdayjobs.com — covers large enterprises, banks, and mature fintechs that use Workday ATS

Platform Searches (search directly on platform):
- otta.com — search roles directly on Otta (London-heavy, strong for UK fintech/tech)
- welcometothejungle.com — search roles directly (strong for European tech)
- efinancialcareers.com — search roles directly (finance-adjacent, fintech, banking CoS)

**Roles (2 tiers):**

Primary roles (search all 7 sources):
- Chief of Staff
- Director of Partnerships / Head of Partnerships
- Director of Business Development / Head of BD
- Head of Strategic Alliances
- Commercial Director / Head of Commercial

Secondary roles (search ATS boards + Otta only):
- Head of Strategy & Operations / Director of Strategy & Operations
- Head of Growth
- Head of Ecosystem / Platform Partnerships
- Corporate Development (Director / Head)
- Operating Partner (VC firms only)
- GTM Lead / Head of Go-to-Market

**Locations:**
- London, UK
- Washington DC
- Remote-US
- Remote-Global
- Remote-EMEA
- Remote-Europe

**Filters:**
- Posted within last 7 days
- For each board/role/location combination, extract up to 20 results
- For Otta/WTTJ/efinancialcareers: use their built-in filters for location + role title + date posted

Show progress matrix as you search.

---

#### SOURCE FILTERING

**Only include results from target boards and platforms.**

**Exclude aggregators:** Jobgether, Talent.com, Lensa, Jooble, Adzuna, SimplyHired, ZipRecruiter, Snagajob, Indeed, Glassdoor.

**URL rules:**
- Must be job-specific URL with job ID
- Exclude board roots without job ID
- Exclude generic career pages
- For Otta/WTTJ/efinancialcareers: include the platform-specific job URL

**Anti-hallucination:** Only include jobs you actually visited. Zero results = report zero.

Set `URL_Status = "Not Checked"` for all Phase 1B rows.
Set `Found_On` to the board or platform name.

Report: "Phase 1B: Found X jobs across 7 sources"

---

### PHASE 2: MERGE + DEDUP

Combine Phase 1A (API-verified) and Phase 1B (wide-net search) results.

**Deduplication rules:**
- Match on: Company name (normalized) + Job Title (fuzzy — same role, different wording = duplicate)
- When duplicate found:
  - **Keep API-sourced URL** (it's verified live)
  - Keep higher score
  - Set `URL_Status = "API-Verified"` if either source was API
  - Merge `Found_On` (e.g., "Greenhouse API + Otta")
- When no duplicate: keep as-is with original URL_Status

**Priority order for URL source:** API-Verified > Platform (Otta/WTTJ/eFin) > Google site:

Report: "Phase 2: Merged to X unique jobs (Y API-verified, Z need checking)"

---

### FIELD EXTRACTION

Extract (use "N/A" if not available):
- Company, Job_Title, Location, Work_Arrangement, Sector
- Salary_USD (convert currencies; "N/A" if not listed)
- Job_Summary (2-3 sentences)
- URL, Found_On (board/platform name, with "API" suffix if API-sourced)

**Work Arrangement** — exactly one of: Remote-US, Remote-EMEA, Remote-Europe, Remote-Global, Hybrid, In-Office, Unclear

---

### SCORING

Using attached resume (Phil_Tassi_Resume.pdf), score each job 1-100:

**Industry Fit (35 points):**
- Fintech, banking, payments, crypto: 35/35
- AI/ML, defense tech, B2B SaaS: 30/35
- Climate tech, marketplace tech: 25/35
- Adjacent tech sectors: 20/35
- Non-tech: 10/35

**Skills Match (25 points):**
- Key skills: Startup ecosystem building, partnership development, VC/investor relations, strategic operations, zero-to-one builds, GTM/commercial scaling, cross-functional leadership
- Exact match to Phil's JPMorgan startup banking + VC background: 25/25
- Strong transferable match: 20/25
- Partial match: 15/25

**Seniority Match (20 points):**
- Director/VP/Head/C-suite level: 20/20
- Senior Manager / Principal: 15/20
- Manager level: 10/20
- Entry/junior: 5/20

**Location Flexibility (10 points):**
- London, Washington DC: 10/10
- Remote-US, Remote-Global, Remote-EMEA, Remote-Europe: 10/10
- New York, San Francisco (top-tier company only): 7/10
- Other: 3/10

**Salary Fit (10 points):**
- $150K+ or £120K+: 10/10
- $120K-$150K: 7/10
- Below $120K: 4/10
- Not listed: 5/10

Provide 1-2 sentence Score_Rationale.

**Filter to 70+ only. Rank by score descending.**

---

### NEW/REPEAT DETECTION

Compare to: {BASE_PATH}/results/For_Others/Phil_Tassi/Week_of_PREVIOUS_WEEK/Phil_Tassi_PREVIOUS_WEEK.csv

- File exists → mark NEW or REPEAT
- No file → mark all NEW

---

### COMPANIES.JSON UPDATE

After search completes, identify any new companies found in Phase 1B that are NOT already in `{SEARCHES_PATH}/companies.json`.

For each new company:
1. Determine the ATS (greenhouse, lever, or ashby) from the job URL
2. Extract the company slug from the URL
3. Report the additions needed:

```
New companies to add to companies.json tier_3:
  {"slug": "newcompany", "ats": "greenhouse", "source": "search_CURRENT_WEEK", "added": "CURRENT_WEEK"}
  ...
```

**Do not modify companies.json directly** — just report the additions so Joey can append them. (The funding intel process handles tier_4 additions separately.)

---

### OUTPUT FILES

**Weekly CSV:** {RESULTS_PATH}/Phil_Tassi_CURRENT_WEEK.csv

**Columns (21, this exact order):**
```
Score | Company | Job_Title | Location | Work_Arrangement | Sector | Salary_USD | Job_Summary | URL | Score_Rationale | Times_Seen | First_Seen_Date | Last_Seen_Date | Status | Found_On | URL_Status | Applied_Date | Application_Method | Response_Status | Interview_Stage | Notes
```

**Default values:**
- Times_Seen: 1
- First_Seen_Date: CURRENT_WEEK
- Last_Seen_Date: CURRENT_WEEK
- **URL_Status: "API-Verified" (from Phase 1A) or "Not Checked" (from Phase 1B)**
- Applied_Date through Notes: leave blank

**Branded XLSX:** {RESULTS_PATH}/Phil_Tassi_CURRENT_WEEK.xlsx

Formatting:
- Header row: dark blue background, white text, bold
- Score 90+: light blue row fill
- REPEAT status: light orange row fill
- API-Verified rows: light green left border (visual indicator of verified jobs)
- Auto-fit column widths
- Freeze top row

---

### LINKEDIN PRE-BUILT SEARCH LINKS

After completing the board search, generate LinkedIn search URLs. Output: {RESULTS_PATH}/LinkedIn_Links_CURRENT_WEEK.md

URL format:
```
https://www.linkedin.com/jobs/search/?keywords={ROLE}&location={LOCATION}&f_TPR=r604800&f_E=4
```
- `f_TPR=r604800` = posted in last 7 days
- `f_E=4` = Director level and above

**Generate links for these combinations:**

Primary roles × London:
- Chief of Staff + London
- Head of Partnerships + London
- Director of Partnerships + London
- Director Business Development + London
- Commercial Director + London
- Head of Strategic Alliances + London

Primary roles × Remote:
- Chief of Staff + United Kingdom (Remote)
- Head of Partnerships + United Kingdom (Remote)
- Director Business Development + United Kingdom (Remote)

Primary roles × Washington DC:
- Chief of Staff + Washington DC
- Director of Partnerships + Washington DC
- Director Business Development + Washington DC

Secondary / expansion roles × London:
- Head of Strategy Operations + London
- Head of Growth + London
- Corporate Development Director + London
- Operating Partner + London
- Head of Ecosystem Partnerships + London

Format as clean markdown with clickable links, grouped by location. Include note at top: "One-click LinkedIn searches — filtered to Director+ level, posted in the last 7 days. Scan takes ~5 minutes."

---

### VERIFICATION SUMMARY

Show summary with:
- **Phase 1A stats:** API-verified jobs ingested, scored 70+
- **Phase 1B stats:** Jobs found by source (Greenhouse/Lever/Ashby/Workday/Otta/WTTJ/eFin)
- **Merge stats:** Total unique after dedup, API-verified count, need-checking count
- Job counts by role tier (Primary vs Secondary)
- Job counts by location
- New companies identified for companies.json
- Files saved
- LinkedIn links generated

---

## STOP HERE

**Phases 1-3 complete.** Run post-step locally:

```bash
python3 JC3/check_urls.py results/For_Others/Phil_Tassi/Week_of_CURRENT_WEEK/Phil_Tassi_CURRENT_WEEK.csv
```

This only checks rows with `URL_Status = "Not Checked"`. API-Verified rows are skipped.

---

## APPENDIX: FUNDING INTEL → COMPANIES.JSON WORKFLOW

When running funding intel for Phil (separate process), new companies should be added to `companies.json` tier_4:

1. Run funding intel scan (Crunchbase, TechCrunch, etc.)
2. For each relevant company (score 7+), determine:
   - ATS system (check if they have a Greenhouse/Lever/Ashby board)
   - Company slug (the URL path component)
3. Append to `{SEARCHES_PATH}/companies.json` under `tier_4_funding_intel`:
   ```json
   {"slug": "newcompany", "ats": "greenhouse", "source": "funding_intel", "added": "CURRENT_WEEK"}
   ```
4. Update `_meta.total_companies` count
5. Next time `ats_api_checker.py` runs, it will automatically include the new companies

**ATS detection shortcut:** Check these URLs in order:
- `https://boards-api.greenhouse.io/v1/boards/{slug}/jobs` → if 200, it's Greenhouse
- `https://api.lever.co/v0/postings/{slug}` → if 200, it's Lever
- `https://api.ashbyhq.com/posting-api/job-board/{slug}` → if 200, it's Ashby
- If none work, company may use Workday or a custom ATS (skip for API checker, still searchable via Google)

---

## APPENDIX: WEEKLY CHECKLIST

```
□ Run funding intel (optional — biweekly or when newsworthy rounds land)
  → Append new companies to companies.json tier_4
  → Output funding_intel_Phil_Tassi_{DATE}.csv

□ Run ATS API checker locally:
  cd ~/GitHub/ai-automation-portfolio/searches/For_Others/Phil_Tassi
  python3 ats_api_checker.py
  → Creates results/For_Others/Phil_Tassi/Week_of_{DATE}/api_verified_{DATE}.csv

□ Run this ONE_CLICK in CoWork:
  → Attach Phil_Tassi_Resume.pdf
  → Paste THE PROMPT section above
  → Creates Phil_Tassi_{DATE}.csv, .xlsx, LinkedIn_Links_{DATE}.md
  → Reports new companies for companies.json

□ Run URL checker locally:
  python3 JC3/check_urls.py results/For_Others/Phil_Tassi/Week_of_{DATE}/Phil_Tassi_{DATE}.csv

□ Update companies.json with new tier_3 companies from search

□ Draft delivery email

□ Git commit results
```

---

*v5.0 | 2026-03-17*
