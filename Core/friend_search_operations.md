# Friend Job Search Operations Guide

*System-level reference for running weekly job searches on behalf of friends. Friend-specific configurations live in their individual ONE_CLICK files and results folders.*

---

## System Overview

Joey runs a weekly AI-powered job search service for friends using CoWork. The system combines direct ATS API querying, wide-net web search, URL verification, and professional deliverable packaging into a unified pipeline.

Each friend receives:
- **Verified Jobs XLSX** — scored, ranked, URL-verified jobs in a branded spreadsheet with conditional formatting
- **Non-Queryable Companies Tab** — companies tracked in the corpus but not yet queryable via API, with resolution instructions
- **LinkedIn Search Links** — pre-built one-click LinkedIn URLs filtered to Director+ level, posted in the last 7 days
- **Funding Intelligence** (periodic) — newly funded companies likely to hire before roles are posted
- **Delivery Email** — personalized HTML email with highlights, statistics, system changes, and action items

---

## Architecture: The Unified Pipeline (v5.0)

The system has three execution phases — two local, one in CoWork:

```
┌─────────────────────────────────────────────────────────────┐
│  PRE-STEP (local, before CoWork)                            │
│  1. (Optional) Run funding intel scan                       │
│     → new companies append to companies.json tier_4         │
│  2. Run: python3 ats_api_checker.py                         │
│     → reads companies.json (200+ companies)                 │
│     → queries Greenhouse/Lever/Ashby APIs directly          │
│     → outputs api_verified_{DATE}.csv                       │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│  COWORK STEP (ONE_CLICK prompt)                             │
│                                                             │
│  Phase 1A: Ingest api_verified_{DATE}.csv                   │
│    → Score all API-sourced jobs                             │
│    → Mark URL_Status = "API-Verified"                       │
│                                                             │
│  Phase 1B: Wide-net search (7 sources)                      │
│    → Google site: searches + platform searches              │
│    → Score all search-sourced jobs                          │
│    → Mark URL_Status = "Not Checked"                        │
│                                                             │
│  Phase 2: Merge + Dedup                                     │
│    → Combine 1A + 1B                                        │
│    → Dedup on Company + Job_Title                           │
│    → API-sourced URL wins over Google-sourced URL           │
│                                                             │
│  Phase 3: Output                                            │
│    → Phil_Tassi_{DATE}.csv (merged, scored, ranked)         │
│    → Phil_Tassi_{DATE}.xlsx (branded, 3-tab)                │
│    → LinkedIn_Links_{DATE}.md                               │
│    → Reports new companies for companies.json               │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│  POST-STEP (local, after CoWork)                            │
│  Run: python3 JC3/check_urls.py [csv_path]                  │
│  → Only checks rows where URL_Status = "Not Checked"        │
│  → Skips "API-Verified" rows (already live)                 │
│  → Rebuild XLSX with verified results                       │
└─────────────────────────────────────────────────────────────┘
```

### Why This Architecture

The core problem: Google's index of ATS job boards lags by days or weeks. A search that finds 30 jobs might yield only 5 live URLs. Direct ATS API calls bypass Google entirely — querying the source of truth in real time. The unified pipeline combines both approaches: API-verified jobs (high confidence) merged with wide-net search results (broader coverage, needs verification).

---

## The Company Corpus: companies.json

Each friend with an ATS API checker has a `companies.json` file containing their target company corpus. This is the heart of the API-first approach.

### Structure

```json
{
  "_meta": {
    "description": "Phil Tassi target companies — ATS API checker corpus",
    "total_companies": 200,
    "api_queryable": 126,
    "non_queryable": 74,
    "last_updated": "2026-03-17"
  },
  "tier_1_multi_role_signals": [...],
  "tier_2_strong_signals": [...],
  "tier_3_search_hits": [...],
  "tier_4_funding_intel": [...]
}
```

### Tiers

| Tier | Description | Source |
|---|---|---|
| tier_1 | Companies with multiple role matches or strong hiring signals | Historical search results with 2+ matches |
| tier_2 | Companies with strong single-role matches | Historical search results, high-score hits |
| tier_3 | Companies that appeared in any search | All historical CSVs, one-time hits |
| tier_4 | Companies from funding intelligence | Crunchbase, TechCrunch, newsletter scans |

### Company Entry Format

```json
{"slug": "stripe", "ats": "greenhouse", "source": "search_2026-02-01", "added": "2026-02-01"}
```

Valid `ats` values: `greenhouse`, `lever`, `ashby`, `workday`, `unknown`

Only `greenhouse`, `lever`, and `ashby` are API-queryable. Companies with `workday` or `unknown` are tracked but skipped by the API checker — they appear in the Non-Queryable Companies tab of the deliverable.

### Growing the Corpus

The corpus grows through three channels:
1. **Search results** — new companies found during ONE_CLICK searches are reported for manual addition to tier_3
2. **Funding intelligence** — newly funded companies added to tier_4
3. **Manual additions** — companies identified through networking, news, or friend suggestions

### ATS Detection for New Companies

Check these URLs in order:
- `https://boards-api.greenhouse.io/v1/boards/{slug}/jobs` → if 200, it's Greenhouse
- `https://api.lever.co/v0/postings/{slug}` → if 200, it's Lever
- `https://api.ashbyhq.com/posting-api/job-board/{slug}` → if 200, it's Ashby
- If none work → mark as `unknown` (may use Workday or custom ATS)

---

## ATS API Checker (ats_api_checker.py)

### What It Does

Reads `companies.json`, queries every API-queryable company (Greenhouse, Lever, Ashby) for current open roles, filters by role keywords and location, and outputs a verified CSV of live jobs.

### Location

`searches/For_Others/[First_Last]/ats_api_checker.py`

### Key Features

- Reads companies.json directly — no hardcoded company list
- Filters by 17+ role keywords (Chief of Staff, Partnerships, Business Development, Strategic Alliances, Commercial Director, Strategy & Operations, Growth, Ecosystem, Corporate Development, Operating Partner, GTM, Go-to-Market, etc.)
- Filters by location (London, UK, Remote, EMEA, Europe, DC, Washington, NYC, New York, Global)
- Outputs `api_verified_{DATE}.csv` with columns: company_slug, title, location, url, ats, URL_Status, Close_Reason, Posting_Age_Days
- Reports: total corpus size, API-queryable count, skipped (unknown/workday) count

### Running It

```bash
cd ~/GitHub/ai-automation-portfolio/searches/For_Others/Phil_Tassi
python3 ats_api_checker.py
```

Output goes to: `results/For_Others/Phil_Tassi/Week_of_{DATE}/api_verified_{DATE}.csv`

### What It Does NOT Do

- Does not search Otta, Welcome to the Jungle, efinancialcareers, or Workday boards
- Does not do Google site: searches
- Does not generate LinkedIn links
- Does not produce the final XLSX deliverable

These are handled by the ONE_CLICK prompt in CoWork. The API checker and ONE_CLICK are complementary — the API checker provides high-confidence verified results, and ONE_CLICK provides broad coverage that needs URL verification.

---

## Search Configuration

### Job Boards (7 sources)

**ATS Board Searches (Google site: operator):**
- site:boards.greenhouse.io
- site:jobs.lever.co
- site:jobs.ashbyhq.com
- site:myworkdayjobs.com — covers large enterprises, banks, and mature fintechs

**Platform Searches (direct on platform):**
- otta.com — London-heavy, strong for UK fintech/tech
- welcometothejungle.com — strong for European tech
- efinancialcareers.com — finance-adjacent, fintech, banking CoS

### Role Tiers

**Primary roles** (searched across all 7 sources):
- Chief of Staff
- Director/Head of Partnerships
- Director/Head of Business Development
- Head of Strategic Alliances
- Commercial Director / Head of Commercial

**Secondary roles** (searched on ATS boards + Otta only):
- Head/Director of Strategy & Operations
- Head of Growth
- Head of Ecosystem / Platform Partnerships
- Corporate Development (Director/Head)
- Operating Partner (VC firms only)
- GTM Lead / Head of Go-to-Market

### Locations

- London, UK
- Washington DC
- Remote-US
- Remote-Global
- Remote-EMEA
- Remote-Europe

### Work Arrangement Categories

Normalize to exactly one of:
- **Remote-US** — Remote limited to US
- **Remote-EMEA** — Remote limited to EMEA
- **Remote-Europe** — Remote limited to Europe
- **Remote-Global** — Remote without geographic restriction
- **Hybrid** — Any hybrid arrangement
- **In-Office** — Location-specific, no remote option
- **Unclear** — Cannot determine from posting

---

## Folder Structure & Path Conventions

**Standard path:** `/Users/jc3/GitHub/ai-automation-portfolio/`

```
searches/
├── For_Others/
│   ├── [First_Last]/
│   │   ├── ONE_CLICK_[First_Last].md     # Unified pipeline prompt (v5.0)
│   │   ├── companies.json                # Target company corpus
│   │   ├── ats_api_checker.py            # ATS API checker script
│   │   └── executed_YYYY-MM-DD.txt       # Run logs
│   └── [Next_Friend]/
│       └── ...
│
results/
├── For_Others/
│   ├── [First_Last]/
│   │   ├── Week_of_YYYY-MM-DD/
│   │   │   ├── api_verified_YYYY-MM-DD.csv         # ATS API checker output
│   │   │   ├── [First_Last]_YYYY-MM-DD.csv         # Merged/scored results
│   │   │   ├── [First_Last]_Complete_YYYY-MM-DD.xlsx  # 3-tab branded XLSX
│   │   │   ├── LinkedIn_Links_YYYY-MM-DD.md        # Pre-built search URLs
│   │   │   ├── funding_intel_[First_Last]_YYYY-MM-DD.csv  # Funding intel
│   │   │   └── deliverables/
│   │   │       └── delivery_email_YYYY-MM-DD.html  # HTML delivery email
│   │   └── Master_Job_Database_[First_Last].csv    # Consolidated
│   └── [Next_Friend]/
│       └── ...
```

**Key rules:**
- Friend folders use `First_Last` format (e.g., `Phil_Tassi`)
- Week folders use ISO date of Monday: `Week_of_2026-03-16`
- All paths are absolute in prompts — never relative
- ONE_CLICK files, companies.json, and ats_api_checker.py live together in the friend's searches folder

---

## Standard Data Format

### 21-Column CSV Format

All friend searches use this column order:

```
Score | Company | Job_Title | Location | Work_Arrangement | Sector | Salary_USD | Job_Summary | URL | Score_Rationale | Times_Seen | First_Seen_Date | Last_Seen_Date | Status | Found_On | URL_Status | Applied_Date | Application_Method | Response_Status | Interview_Stage | Notes
```

**Key fields:**
- **Status:** NEW or REPEAT (compared to previous week)
- **Score:** 1-100 based on weighted scoring
- **URL_Status:** "API-Verified", "Open", "Closed", "Not Checked", or "Error"
- **Found_On:** Source board(s), with "API" suffix for API-sourced results (e.g., "Greenhouse API + Otta")
- **Applied_Date through Notes:** Application tracking fields, initially blank

---

## Scoring Weight System

### Default Weights (100 points total)

| Category | Default | Description |
|---|---|---|
| Industry Fit | 35 | Alignment with target sectors |
| Skills Match | 25 | Resume skills vs. job requirements |
| Seniority Match | 20 | Experience level alignment |
| Location Flexibility | 10 | Target location match |
| Salary Fit | 10 | Compensation alignment |

### Adjusting Based on Priority Ranking

Friend provides ranking 1-5. General principle: #1 priority gets 30-40 pts, #5 gets 10 pts, middle three split the rest.

### Salary Scoring Rule

Most jobs don't list salary. Standard approach:
- Listed and meets target: full credit
- Listed but below target: score proportionally
- Not listed ("N/A"): award half points (neutral — don't penalize unknown)

---

## Source Filtering

### Always exclude aggregators:
Jobgether, Talent.com, Lensa, Jooble, Adzuna, SimplyHired, ZipRecruiter, Snagajob, Indeed, Glassdoor

### URL Rules
- Must be job-specific URL with job ID
- Exclude board roots without job ID
- Exclude generic career pages
- For Otta/WTTJ/efinancialcareers: include platform-specific job URLs

### Anti-hallucination
Only include jobs actually visited. Zero results = report zero.

---

## 3-Tab XLSX Deliverable

The branded Excel deliverable contains three tabs:

### Tab 1: Verified Jobs
- All jobs scoring 70+ that passed URL verification
- Navy header row with white bold text
- Score 90+: light blue row fill
- REPEAT status: light orange row fill
- API-Verified rows: light green left border
- Clickable hyperlinks in URL column
- Frozen top row, auto-filters enabled
- Auto-fit column widths

### Tab 2: Non-Queryable Companies
- Companies in the corpus with `ats: "unknown"` or `ats: "workday"`
- Grouped by source (Search Hits vs. Funding Intel)
- Includes company name, source, date added
- Serves as a manual check list — friend can visit career pages directly

### Tab 3: LinkedIn Search Links
- Pre-built LinkedIn URLs filtered to Director+ level, posted last 7 days
- Grouped by location (London, Remote UK, Washington DC)
- Primary and secondary role tiers separated
- Clickable hyperlinks

---

## Delivery Email Structure

### System Upgrade Email (when architecture changes)
1. What changed and why (the problem it solves)
2. Before vs. after stats (the breakthrough)
3. Top role highlights with Apply links
4. System upgrades explained (expanded roles, boards, locations, company corpus)
5. Funding intelligence integration
6. Non-queryable companies with step-by-step ATS resolution guide
7. LinkedIn search links
8. Specific asks for the friend

### Recurring Weekly Email
1. This week's numbers (total, new, repeat, API-verified vs. search-sourced)
2. Highlights (best new finds, notable companies)
3. Repeat job signals (persistent hiring = prioritize these)
4. Pattern insights from analysis (if available)
5. Attachments: XLSX deliverable + any supplementary files
6. Prompt tuning suggestions (with specific questions to get feedback)

### Email Template
HTML format, Arial 14px, 680px max-width, colored section boxes, emoji section headers. Template in `searches/EMAIL_DELIVERY_TEMPLATE_v1.html`.

---

## Weekly Run Checklist

```
□ (Optional) Run funding intel scan
  → Append new companies to companies.json tier_4
  → Output funding_intel_[First_Last]_{DATE}.csv

□ Run ATS API checker locally:
  cd ~/GitHub/ai-automation-portfolio/searches/For_Others/[First_Last]
  python3 ats_api_checker.py
  → Creates results/For_Others/[First_Last]/Week_of_{DATE}/api_verified_{DATE}.csv

□ Run ONE_CLICK in CoWork:
  → Attach resume PDF + api_verified CSV
  → Creates [First_Last]_{DATE}.csv, .xlsx, LinkedIn_Links_{DATE}.md
  → Reports new companies for companies.json

□ Run URL checker locally:
  python3 JC3/check_urls.py results/For_Others/[First_Last]/Week_of_{DATE}/[First_Last]_{DATE}.csv

□ Rebuild XLSX with verified results (in CoWork)
  → Final 3-tab deliverable: [First_Last]_Complete_{DATE}.xlsx

□ Update companies.json with new tier_3 companies from search

□ Draft delivery email

□ Git commit results
```

---

## Onboarding Workflow

### Step 1: Collect Intake

Send intake questionnaire. Collect:
1. 3-5 target job titles
2. Preferred locations (include Remote variants if open)
3. Target industries/sectors
4. Minimum salary
5. Priority ranking 1-5: Industry Fit, Skills Match, Seniority, Location, Salary
6. Top 3 skills
7. Deal-breakers
8. Company size preference

### Step 2: Build Configuration

For each new friend:
1. Create ONE_CLICK file from template with their specific roles, locations, sectors, and scoring weights
2. Build initial companies.json by scanning their target sector for known companies on Greenhouse/Lever/Ashby
3. Create ats_api_checker.py configured for their companies.json
4. Set correct output paths

### Step 3: First Run

- Run ats_api_checker.py to verify the corpus
- Run ONE_CLICK in CoWork with resume attached
- Run check_urls.py on results
- Review quality before sending
- All jobs marked NEW on first run (no previous data)

### Step 4: Deliver Results

- Send 3-tab XLSX deliverable
- First email explains the system, scoring methodology, and how to read the spreadsheet
- Ask for feedback: "Do these weights feel right? Which roles are on/off target?"

---

## Funding Intelligence Pipeline

### Sources
- StrictlyVC (daily, US focus)
- FINSmes (daily, global)
- EU-Startups (daily, European focus)
- Sunday CET (weekly, European focus)

### Workflow
1. Scan newsletters for Series A+ rounds in target sectors
2. Score relevance to friend's profile (1-10)
3. For companies scoring 7+, detect ATS system using the URL check method
4. Add to companies.json tier_4
5. Next ats_api_checker.py run will automatically include the new companies
6. Output funding_intel_[First_Last]_{DATE}.csv

### Integration with Main Pipeline
Funding intel feeds the company corpus → API checker queries new companies → verified jobs appear in next week's deliverable. This creates a proactive intelligence loop: companies are tracked before they even post roles in the friend's target titles.

---

## Known Issues & Lessons Learned

### Google Stale Index Problem (SOLVED)
**Problem:** Google's cache of ATS boards lags by days/weeks. Searches returning 30+ results might yield only 5 live URLs.
**Solution:** ATS API checker bypasses Google entirely by querying ATS APIs directly. This was the breakthrough that took Phil's search from 2 verified jobs to 42 in one week.

### Non-Queryable Companies
**Problem:** Companies using Workday, custom ATS, or unidentified systems can't be queried via API.
**Solution:** Track them in companies.json as `unknown`/`workday`, surface them in Tab 2 of the deliverable, and provide step-by-step ATS detection instructions so the friend or Joey can resolve them over time.

### Location Drift
**Problem:** Searches for "Remote" sometimes return roles in non-target cities.
**Fix:** Hard location filter in prompt + location scoring at 0 for non-target locations.

### Board Coverage Gaps by Industry
**Problem:** Finance (hedge funds, PE) and some defense roles don't appear on standard ATS boards.
**Fix:** Supplement with platform searches (Otta, WTTJ, efinancialcareers), LinkedIn search links, and company career page checks.

### Score Inflation on First Batch
**Problem:** First batches sometimes score higher due to broader initial capture.
**Fix:** Note in analysis that cross-batch comparisons should be cautious. Standardize scoring in ONE_CLICK before first run.

---

## Planned Improvements

- **Automated companies.json updates** — script to parse ONE_CLICK search reports and auto-append new companies
- **Workday API integration** — some Workday boards have queryable endpoints; investigate coverage
- **Cross-friend corpus sharing** — companies relevant to multiple friends could be shared across corpuses
- **Application tracking dashboard** — web UI showing application status across all friends
- **Automated email generation** — templated delivery emails with auto-populated stats

---

*Last updated: 2026-03-17*
*System version: v5.0 — Unified pipeline, 200-company corpus, 7-board search, ATS API checker, 3-tab XLSX deliverables*
