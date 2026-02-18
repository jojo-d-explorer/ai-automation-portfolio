# Friend Job Search Operations Guide

*System-level reference for running weekly job searches on behalf of friends. Friend-specific configurations live in their individual ONE_CLICK files and results folders.*

---

## System Overview

Joey runs a weekly AI-powered job search service for friends using CoWork. Each friend receives:
- **Weekly Top 10 New** — highest-scoring new jobs that week
- **Weekly Master List** — all jobs scoring 70+ from that week's search
- **Strategic Analysis** (after 2+ weeks of data) — multi-week patterns, sector mapping, company signals, networking guidance
- **Delivery Email** — personalized summary with highlights, statistics, and prompt tuning suggestions

---

## Folder Structure & Path Conventions

**Standard path:** `/Users/jc3/GitHub/ai-automation-portfolio/`

```
results/
├── For_Others/
│   ├── [First_Last]/
│   │   ├── Week_of_YYYY-MM-DD/
│   │   │   ├── Master_List_YYYY-MM-DD.csv
│   │   │   ├── Top10_New_YYYY-MM-DD.csv
│   │   │   └── (analysis files after 2+ weeks)
│   │   └── Master_Job_Database_[First_Last].csv  (consolidated)
│   └── [Next_Friend]/
│       └── ...
│
searches/
├── prompts/
│   ├── for_others/
│   │   ├── [First_Last]/
│   │   │   ├── ONE_CLICK_[First_Last].md
│   │   │   └── executed_YYYY-MM-DD.txt
│   │   └── [Next_Friend]/
│   └── ...
```

**Key rules:**
- Friend folders use `First_Last` format (e.g., `Aaron_Kimson`, `Phil_Tassi`)
- Week folders use ISO date of Monday: `Week_of_2026-02-16`
- All paths are absolute in prompts — never relative
- ONE_CLICK files live with the friend's executed prompts, not in results

---

## Onboarding Workflow

### Step 1: Collect Intake

Send intake questionnaire (email or text/Slack version). Collect:
1. 3-5 target job titles
2. Preferred locations (include Remote if open)
3. Target industries/sectors
4. Minimum salary
5. Priority ranking 1-5: Industry Fit, Skills Match, Seniority, Location, Salary
6. Top 3 skills
7. Deal-breakers
8. Company size preference

### Step 2: Build ONE_CLICK File

Start from `ONE_CLICK_TEMPLATE_Friends.md`. Key customizations:
- Replace all bracketed fields with intake responses
- Choose appropriate job boards (see Board Selection below)
- Set scoring weights based on priority ranking (see Weight System below)
- Define industry fit criteria specific to their background
- Add any deal-breaker filters
- Set correct output paths using `results/For_Others/[First_Last]/`
- Save as `ONE_CLICK_[First_Last].md`

### Step 3: First Run

- Attach friend's resume PDF
- Run in CoWork
- Review results for quality before sending
- All jobs marked NEW on first run (no previous data to compare)

### Step 4: Deliver Results

- Send Top 10 CSV + Master List CSV
- First email explains the system, scoring methodology, archetype strategy
- Ask for feedback: "Do these weights feel right? Which roles are on/off target?"

---

## Weekly Run Workflow

**Every Sunday (or chosen cadence):**

1. Open friend's ONE_CLICK file
2. Copy prompt section into CoWork
3. Attach their resume
4. Run (10-15 min)
5. Review results
6. After 2+ weeks: run CONSOLIDATE_TO_MASTER, then analysis
7. Draft delivery email with highlights and suggestions
8. Send Top 10, Master List, and analysis (if available)
9. Git commit results

---

## Standard Data Format

### 14-Column CSV Format

All friend searches use this column order:

```
Status | Score | Score_Rationale | Company | Job_Title | Sector | Location | Language_Requirement | Work_Arrangement | Salary_USD | Job_Summary | URL | URL_Status | Found_On
```

**Status:** NEW or REPEAT (compared to previous week)
**Score:** 1-100 based on weighted scoring
**Language_Requirement:** "N/A" if English only; list language if non-English required
**Work_Arrangement:** One of 5 standardized categories (see below)
**URL_Status:** Verified or Unverified
**Found_On:** Which board(s) the job appeared on

### Work Arrangement Categories

Normalize to exactly one of:
- **Remote-US** — Remote limited to US
- **Remote-Americas** — Remote including LATAM/Canada
- **Remote-Global** — Remote without geographic restriction
- **Hybrid** — Any hybrid arrangement
- **In-Office** — Location-specific, no remote option

Never leave as generic "Remote" — always classify.

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

| Their #1 Priority | Suggested Adjustment |
|---|---|
| Salary | Salary → 30, reduce Industry to 25 |
| Location | Location → 25, reduce Skills to 20 |
| Skills Match | Skills → 35, reduce Industry to 25 |
| Industry Fit | Industry → 40 (already high) |
| Seniority | Seniority → 30, reduce Location to 10 |

**Important:** Some categories overlap depending on the industry. For finance-specific searches, "Skills Match" and "Industry Fit" may be nearly identical — in that case, combine them or embed skills into industry scoring.

### Salary Scoring Rule

Most jobs don't list salary. Standard approach:
- Listed and meets target: full credit
- Listed but below target: score proportionally
- Not listed ("N/A"): award half points (neutral — don't penalize unknown)

---

## Board Selection by Industry

### Default (tech/startup roles): 4 boards
- Greenhouse, Lever, Ashby, LinkedIn

### Finance / Hedge Fund roles
- Standard 4 boards have limited coverage for HF/PE roles
- LinkedIn authenticated browser session is critical — produces best results
- Add supplementary company career page checks for specific target firms
- Allow recruiter-posted roles (Selby Jennings, etc.) with "(Recruiter)" label
- Consider adding eFinancialCareers, Built In for supplementary coverage

### Defense Tech / Government
- Standard 4 boards work well for larger defensetech (Shield AI, Anduril)
- Smaller defensetech may post on company career pages only
- Add targeted career page checks for specific defense companies
- Security clearance filtering may be needed (see Known Issues)

### General principle
If first search yields <15 results on standard boards, the industry may need supplementary sources.

---

## Source Filtering

### Always exclude aggregators:
Jobgether, Talent.com, Lensa, Jooble, Adzuna, SimplyHired, ZipRecruiter, Snagajob

### URL Verification
Reconstruct broken URLs using standard formats:
- Greenhouse: `boards.greenhouse.io/[company]/jobs/[id]`
- Lever: `jobs.lever.co/[company]/[id]`
- Ashby: `jobs.ashby.com/[company]/[id]`
- LinkedIn: `linkedin.com/jobs/view/[id]`

Mark as Verified or Unverified.

---

## Delivery Email Structure

### First Run Email (onboarding)
1. How the system works (scan, score, deduplicate, rank)
2. Time savings pitch (3-4 hours manual → 15 min automated)
3. Iteration framing ("first search is calibration, your feedback makes it better")
4. Search strategy explanation (archetypes, board selection)
5. First run statistics (total found, score range, sector breakdown)
6. Top 10 highlights with brief commentary
7. Scoring methodology explanation + "does this feel right?"
8. Location/arrangement notes
9. Known issues or caveats (clearance, board coverage gaps)
10. Suggestions for broadening/narrowing
11. What to expect next week (REPEAT tracking, analysis if 2+ weeks)

### Recurring Weekly Email
1. This week's numbers (total, new, repeat)
2. Highlights (best new finds, notable companies)
3. Repeat job signals (persistent hiring = prioritize these)
4. Pattern insights from analysis (if available)
5. Networking suggestions tied to data
6. Prompt tuning suggestions (with specific questions to get feedback)
7. Attachments: Top 10, Master List, Analysis (if available)

---

## Analysis & Consolidation

### When to run CONSOLIDATE_TO_MASTER
After each weekly search. Merges new week's results into cumulative master database. Tracks First_Seen_Date, Last_Seen_Date, Times_Seen, and updates Status.

### When to run MASTER_ANALYSIS
After 2+ weeks of data (minimum 2 search batches consolidated). Produces:
- Score distribution patterns
- Sector concentration mapping
- Company hiring signals (multi-role companies, repeat postings)
- Geographic analysis
- Search evolution and efficiency trends
- Strategic summary with recommended actions

### Analysis Output
Currently: markdown text file
Planned upgrade: Professional PDF with formatted tables and charts

---

## Known Issues & Lessons Learned

### Location Drift
**Problem:** Searches for "Remote" sometimes return roles headquartered in non-target cities. Broad role titles (e.g., "Head of Finance") pull results from any location.
**Fix:** Add hard location filter in prompt: "Only include roles where primary work location is [target cities] or Remote-US." Score non-target locations at 0 points.

### Security Clearance
**Problem:** Many defensetech roles require clearance not mentioned in the posting.
**Fix:** Add clearance detection in scoring. If posting mentions clearance, flag in rationale and apply score penalty (suggest -15 points). Don't exclude — some companies sponsor.

### Board Coverage Gaps by Industry
**Problem:** Finance (hedge funds, PE) and some defense roles don't appear on standard ATS boards.
**Fix:** Supplement with LinkedIn authenticated sessions, company career page checks, and industry-specific boards. Recruiters are a valid source for finance roles.

### Score Inflation on First Batch
**Problem:** Legacy/first batches sometimes score higher due to different methodology or broader initial capture.
**Fix:** Note in analysis that cross-batch score comparisons should be interpreted cautiously. Standardize scoring in ONE_CLICK before first run.

### Template Version Management
**Problem:** Old ONE_CLICK files may use outdated column formats (12 vs 14 columns) or wrong path conventions.
**Fix:** When updating a friend's template, run backfill script on existing data to add missing columns before running new search. This ensures NEW/REPEAT comparison works cleanly.

---

## Planned Improvements

- **Job tracking integration** — Add application status columns to master databases, integrate into weekly reports
- **Excel (.xlsx) output** — Formatted spreadsheets with filters, sorting, conditional formatting (replaces raw CSV)
- **PDF analysis reports** — Professional documents with tables and charts (replaces markdown text)
- **Email template standardization** — Consistent structure across friends with tracking data included
- **Archetype-based search strategy** — Organize role titles into distinct career path archetypes per friend for better targeting

---

*Last updated: 2026-02-17*
*System version: 14-column format, 4-board standard, For_Others path convention*
