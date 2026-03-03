# Technical Setup & Environment

*Current state as of Week 3*

---

## Working Directory

**Primary location:** `/Users/jc3/GitHub/ai-automation-portfolio/`

**Why this location:**

- Out of iCloud Drive (Git + iCloud conflict)
- Local-only storage (faster, more reliable)
- Standard GitHub convention

**Legacy location (DO NOT USE):**

- `/Users/jc3/JobSearch/` - old experimental folder, not tracked by Git

---

## Repository Structure

```
ai-automation-portfolio/
├── .git/                          (Git internals - don't touch)
├── .gitignore                     (Files to ignore)
├── README.md                      (Repository homepage — updated Week 3)
│
├── learning_philosophy.md         (My learning style & context)
├── curriculum_plan.md             (12-week roadmap)
├── prompt_engineering_principles.md
├── git_workflows.md
├── technical_setup.md             (this file)
│
├── JC3/                           (Python scripts & utilities)
│   ├── check_urls.py              (URL verification — v2 with Ashby API, staleness detection)
│   ├── linkedin_links.py          (LinkedIn direct search URL generator per friend)
│   └── verify_linkedin_removal.py (Dry-run checker for LinkedIn removal edits)
│
├── searches/                      (Prompts & templates)
│   ├── FORMAT_SPEC.md             (Column schema & formatting standards)
│   ├── joey/                      (Joey's personal search files)
│   │   ├── ONE_CLICK_WEEKLY_SEARCH.md
│   │   └── CONSOLIDATE_TO_MASTER.md
│   ├── For_Others/                (Friend search operations)
│   │   ├── ONE_CLICK_TEMPLATE_Friends.md
│   │   ├── MASTER_ANALYSIS.md     (6-query analysis pipeline + PDF output)
│   │   ├── FUNDING_INTEL.md       (Standalone funding intelligence prompt)
│   │   ├── Aaron_Kimson/
│   │   │   └── ONE_CLICK_Aaron_Kimson.md
│   │   ├── Phil_Tassi/
│   │   │   └── ONE_CLICK_Phil_Tassi.md
│   │   ├── Vivienne_Pham/
│   │   │   └── ONE_CLICK_Vivienne_Pham.md
│   │   └── Rosalind/
│   │       └── ONE_CLICK_Rosalind.md
│   └── archive/                   (Old/deprecated prompts)
│
├── results/                       (Search outputs — Joey's personal)
│   ├── Week_of_2026-01-26/        (Week 1)
│   ├── Week_of_2026-02-02/        (Week 2)
│   ├── Week_of_2026-02-10/        (Week 3)
│   ├── funding_intel/             (Funding intelligence reports)
│   └── For_Others/                (Friend results)
│       ├── Aaron_Kimson/
│       │   ├── Master_Job_Database_Aaron_Kimson.csv
│       │   └── Week_of_YYYY-MM-DD/
│       ├── Phil_Tassi/
│       │   ├── Master_Job_Database_Phil_Tassi.csv
│       │   └── Week_of_YYYY-MM-DD/
│       ├── Vivienne_Pham/
│       │   └── Week_of_YYYY-MM-DD/
│       └── Rosalind/
│           └── Week_of_YYYY-MM-DD/
│
└── learning_log/                  (Documentation)
    ├── week1_insights.md
    ├── week2_reflection.md
    └── TEMPLATE_weekly_reflection.md
```

---

## Tools & Platforms

### Primary Tools (Daily Use)

**CoWork (Claude Browser Automation)**

- Accessed through: claude.ai web interface
- Purpose: Job search automation, web scraping, data extraction, newsletter scanning
- Key limitation: Each prompt is independent — no persistent memory between runs

**Claude (Anthropic)**

- Model: Sonnet 4.5
- Subscription: Max (higher usage limits)
- Used for: Teaching/curriculum, prompt engineering, analysis, CoWork orchestration
- Projects feature: Stores context files (this file, curriculum, learning philosophy)

**Claude Code (Terminal)**

- Purpose: Running Python scripts, file verification, repo management
- Used for: check_urls.py, verify_linkedin_removal.py, linkedin_links.py
- Access: Terminal command line

**GitHub Desktop**

- Version: Latest (Mac Apple Silicon)
- Purpose: Git commits, pushes, history visualization
- Why not command line: Visual diff makes reviewing changes easier

**Mac Computer**

- Chip: Apple Silicon (M-series)
- OS: macOS (latest)

---

### Supporting Tools

**Finder** — macOS file manager, primary navigation

**TextEdit** — Creating/editing .md, .txt files (Format → Make Plain Text for code)

**Numbers** — Opens .csv files by default on Mac; sufficient for reviewing search results

**Gmail** — Central hub for funding newsletter intelligence (StrictlyVC, FINSmes, EU-Startups, Sunday CET, Remote100K)

---

### Accounts & Services

**GitHub**

- Username: jojo-d-explorer
- Repository: ai-automation-portfolio (currently private, going public Week 8-12)

**Claude.ai**

- Plan: Max
- Purpose: Learning curriculum, CoWork access, project context

---

## Multi-User System Architecture

### Users Currently Served

| Person | Role Types | Locations | Status |
|--------|-----------|-----------|--------|
| **Joey** (personal) | Chief of Staff, Strategic Ops, Partnerships | DC, Remote-US, Lisbon, EU-Remote | 3+ weeks of data, master database (118+ jobs) |
| **Aaron Kimson** | L/S Hedge Fund Analyst, HF PM, Equity Research, Investment Analyst | NYC, SF, Chicago, Miami, Boston | 2-3 weeks |
| **Phil Tassi** | Chief of Staff, Partnerships, BD | Washington DC, London UK | 2-3 weeks |
| **Vivienne Pham** | 3 archetypes: Operator (CFO/VP Finance), Capital Markets (IR), Ecosystem (BD/Portfolio Ops) | NYC, DC, Remote | 1 week |
| **Rosalind** | TBD | TBD | New — first run pending |

### Search Pipeline (per person, per week)

```
ONE_CLICK → Weekly CSV outputs → CONSOLIDATE_TO_MASTER → Master Database
                                                              ↓
                                                    MASTER_ANALYSIS (6 queries)
                                                              ↓
                                                    Branded XLSX + PDF report
                                                              ↓
                                                    Delivery email to friend
```

### Job Boards Searched (3 boards)

- `site:boards.greenhouse.io`
- `site:jobs.lever.co`
- `site:jobs.ashbyhq.com`

**LinkedIn removed from automated search** (Feb 2026) — Google's index of LinkedIn job pages returns months-old stale listings. Friends receive personalized LinkedIn direct search links instead, generated by `JC3/linkedin_links.py`.

**Workday** — Planned addition, pending testing of dead link behavior.

### Funding Intelligence Sources (4 newsletters)

| Source | Sender | Frequency |
|--------|--------|-----------|
| StrictlyVC | connie@strictlyvc.com | ~4-5x/week |
| FINSmes | info@finsmes.com | Daily |
| EU-Startups | thomas.ohr@eu-startups.com | Weekly (Thu) |
| Sunday CET | sundaycet@mail.beehiiv.com | Weekly (Sun) |

Scanned via Gmail search in FUNDING_INTEL prompt. Identifies recently funded companies matching user's target sectors/locations before jobs are posted.

---

## Python Scripts (JC3/ folder)

### check_urls.py (v2)

**Purpose:** Verify job listing URLs are still live after search results are generated.

**Platform-specific detection:**
- **Ashby:** GraphQL API call (`ApiJobPosting` query) — definitive live/dead status
- **Greenhouse/Lever:** HTTP status + content scanning for 23 closed-job phrases + JSON-LD date extraction
- **Cross-domain redirects:** Detects when ATS URL redirects to company careers page
- **Date staleness:** Flags jobs >45 days old via JSON-LD `datePosted`

**Usage:**
```bash
python3 JC3/check_urls.py results/For_Others/Phil_Tassi/Master_Job_Database_Phil_Tassi.csv
```

**Output columns added:** `Close_Reason`, `Posting_Age_Days`

### linkedin_links.py

**Purpose:** Generate personalized LinkedIn direct search URLs for each friend.

**Usage:**
```bash
python3 JC3/linkedin_links.py          # all users
python3 JC3/linkedin_links.py phil     # one user
```

**Output:** Formatted links + email-ready block for delivery emails.

### verify_linkedin_removal.py

**Purpose:** Dry-run checker to confirm LinkedIn was properly removed from all ONE_CLICK files.

**Usage:**
```bash
python3 JC3/verify_linkedin_removal.py
```

**Checks:** No `site:linkedin.com/jobs`, correct board counts, updated dates, no stale "4 boards" references.

---

## File Conventions & Standards

### Date Formats

**Always use ISO 8601:** `YYYY-MM-DD`

- ✅ `2026-02-25` (unambiguous, sorts correctly)
- ❌ `2-4` or `02/04/26` (ambiguous)

### File Naming

**Pattern:** `[Category]_[Description]_[Date].[extension]`

Examples:
- `Master_List_Phil_Tassi_2026-02-24.csv`
- `Top10_New_Aaron_Kimson_2026-02-17.csv`
- `ONE_CLICK_Vivienne_Pham.md`

Rules: No spaces (use underscores), descriptive names, always include extension.

### Column Schema (14 columns, standard across all users)

```
Status | Score | Score_Rationale | Company | Job_Title | Sector | Location |
Language_Requirement | Work_Arrangement | Salary_USD | Job_Summary | URL |
URL_Status | Found_On
```

Plus 5 application tracking columns (when used):
```
Interest_Level | Applied_Date | Application_Method | Response_Status | Notes
```

### Work Arrangement Categories (standardized)

- Remote-US
- Remote-Global
- Hybrid
- In-Office
- Unclear

---

## File Paths

### Absolute vs Relative

**Always use absolute paths in prompts:**
```
/Users/jc3/GitHub/ai-automation-portfolio/results/For_Others/Phil_Tassi/Master_Job_Database_Phil_Tassi.csv
```

**Relative paths** break if CoWork is in the wrong directory.

### Common Paths Quick Reference

```
Joey's search:
/Users/jc3/GitHub/ai-automation-portfolio/searches/joey/ONE_CLICK_WEEKLY_SEARCH.md

Friend template:
/Users/jc3/GitHub/ai-automation-portfolio/searches/For_Others/ONE_CLICK_TEMPLATE_Friends.md

Friend ONE_CLICK:
/Users/jc3/GitHub/ai-automation-portfolio/searches/For_Others/[Name]/ONE_CLICK_[Name].md

Friend results:
/Users/jc3/GitHub/ai-automation-portfolio/results/For_Others/[Name]/Week_of_YYYY-MM-DD/

Friend master database:
/Users/jc3/GitHub/ai-automation-portfolio/results/For_Others/[Name]/Master_Job_Database_[Name].csv

Scripts:
/Users/jc3/GitHub/ai-automation-portfolio/JC3/

Funding intel:
/Users/jc3/GitHub/ai-automation-portfolio/results/funding_intel/
```

---

## Typical Workflows

### Running a Weekly Search (per person)

1. Open the person's ONE_CLICK file
2. Copy prompt (from "Calculate today's date..." to end)
3. Paste into CoWork
4. Attach their resume PDF
5. Hit enter, wait 10-15 minutes
6. Check results folder for outputs (CSV + XLSX)

### Consolidating to Master Database

1. After weekly search completes, run CONSOLIDATE_TO_MASTER prompt
2. Merges new weekly results into cumulative master database
3. Handles deduplication (Company + Job_Title match)

### Running Analysis (for users with 2+ weeks of data)

1. Run MASTER_ANALYSIS prompt (6 queries)
2. Produces branded PDF with scoring trends, sector analysis, location patterns, funding intel
3. Attach to delivery email with XLSX

### Verifying URL Quality (post-search)

```bash
python3 JC3/check_urls.py results/For_Others/[Name]/Master_Job_Database_[Name].csv
```

Removes dead links, adds Close_Reason column, flags stale postings.

### Delivering Results to Friends

1. Run search → consolidate → analysis
2. Run `python3 JC3/linkedin_links.py [name]` for their LinkedIn supplement
3. Email: XLSX attachment + key findings + LinkedIn direct search links

---

## Known Issues & Quirks

### Issue 1: Google Index Staleness

**What:** Google's `site:` operator returns cached pages that may be weeks/months old.
**Impact:** Job listings appear in search but are actually closed/filled.
**Mitigation:** check_urls.py v2 catches most dead links via platform-specific detection. LinkedIn removed entirely from automated search due to worst staleness.

### Issue 2: Ashby Client-Side Rendering

**What:** Ashby uses React. Standard HTTP requests see empty HTML shell.
**Fix:** check_urls.py uses Ashby's GraphQL API (`ApiJobPosting`) to get definitive status.

### Issue 3: CoWork File Creation Locations

**What:** CoWork sometimes saves to unexpected locations.
**Fix:** Always specify full absolute paths with verification step in prompts.

### Issue 4: Duplicate Master List Locations (Phil)

**What:** Phil has master database in both `results/For_Others/Phil_Tassi/` and weekly subfolders.
**Status:** Needs consolidation — pending cleanup.

---

## Backups & Redundancy

**Where work is stored:**

1. Local: `/Users/jc3/GitHub/ai-automation-portfolio/` (primary)
2. GitHub: github.com/jojo-d-explorer/ai-automation-portfolio (cloud backup)
3. Push to GitHub after each work session

**Not backed up:**

- `/Users/jc3/JobSearch/` (old location, not in Git)
- Files outside the repo folder

---

## Future Additions (Planned)

**Near-term:**
- Workday as 4th job board (pending dead-link testing)
- Additional funding newsletter sources
- Proactive company prospecting from funding announcements

**Weeks 9-10:**
- Zapier/Make accounts (landscape survey)
- Cursor or Copilot (AI coding assistant)

**Week 12:**
- Make GitHub repo public
- Portfolio polish

---

*Last updated: 2026-02-26*
*Reflects Week 3 environment*
