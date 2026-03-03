# ONE-CLICK WEEKLY SEARCH: [FRIEND NAME] — TEMPLATE v3.1

**Purpose:** Duplicate this file for each new friend. Replace all [BRACKETED] values. Save as `ONE_CLICK_[First_Last].md`.

**This prompt does:** SEARCH + SCORE only (Phase 1)  
**This prompt does NOT do:** URL verification — that's Phase 2, run separately

---

## PIPELINE CONTEXT

This is **Phase 1 of 7**. After this prompt completes:

```bash
# Phase 2 — run this in Terminal:
python3 JC3/check_urls.py results/For_Others/[First_Last]/Week_of_[DATE]/[First_Last]_[DATE].csv
```

Then continue with Phases 3-7 per ops_playbook_v2.

---

**Owner:** Joey Clark (running on behalf of [FRIEND NAME])  
**Resume file:** [RESUME FILENAME.pdf]  
**Last updated:** [DATE]

---

## THE PROMPT

Calculate today's date and determine:
- Current week start date (most recent Monday): CURRENT_WEEK
- Previous week start date (Monday before that): PREVIOUS_WEEK

Define path variables:
- BASE_PATH = /Users/jc3/GitHub/ai-automation-portfolio
- RESULTS_PATH = {BASE_PATH}/results/For_Others/[First_Last]/Week_of_CURRENT_WEEK

---

### CONFIGURATION

**Job Boards (3 boards):**
- site:boards.greenhouse.io
- site:jobs.lever.co
- site:jobs.ashbyhq.com

**Roles:**
- [Role 1]
- [Role 2]
- [Role 3]

**Locations:**
- [Location 1]
- [Location 2]
- [Location 3]

**Filters:**
- Posted within last 7 days
- For each board/role/location combination, extract up to 20 results

Show progress matrix as you search each combination.

---

### SOURCE FILTERING

**Only include results from target ATS boards.**

**Exclude aggregators:** Jobgether, Talent.com, Lensa, Jooble, Adzuna, SimplyHired, ZipRecruiter, Snagajob, Indeed, Glassdoor.

**URL rules:**
- Must be job-specific URL with job ID (e.g., `/jobs/12345` or `/[uuid]`)
- Exclude board roots without job ID (e.g., `jobs.lever.co/stripe`)
- Exclude generic career pages

**Anti-hallucination:** Only include jobs you actually visited and extracted data from. Zero results = report zero.

---

### FIELD EXTRACTION

Extract (use "N/A" if not available):
- Company, Job_Title, Location, Work_Arrangement, Sector
- Salary_USD (convert currencies; "N/A" if not listed)
- Job_Summary (2-3 sentences)
- URL, Found_On (board name)

**Work Arrangement** — exactly one of: Remote-US, Remote-Global, Hybrid, In-Office, Unclear

---

### DEDUPLICATION

Same Company + Job_Title across boards → keep highest score, merge Found_On.

---

### SCORING

Using attached resume, score each job 1-100:

**[CUSTOMIZE WEIGHTS PER FRIEND]**
- Industry Fit: [X] points
- Skills Match: [X] points  
- Seniority Match: [X] points
- Location Flexibility: [X] points
- Salary Fit: [X] points

Provide 1-2 sentence Score_Rationale.

**Filter to 70+ only. Rank by score descending.**

---

### NEW/REPEAT DETECTION

Compare to: {BASE_PATH}/results/For_Others/[First_Last]/Week_of_PREVIOUS_WEEK/[First_Last]_PREVIOUS_WEEK.csv

- File exists → mark NEW or REPEAT
- No file → mark all NEW

---

### OUTPUT FILES

**Weekly CSV:** {RESULTS_PATH}/[First_Last]_CURRENT_WEEK.csv

**Columns (21, this exact order):**
```
Score | Company | Job_Title | Location | Work_Arrangement | Sector | Salary_USD | Job_Summary | URL | Score_Rationale | Times_Seen | First_Seen_Date | Last_Seen_Date | Status | Found_On | URL_Status | Applied_Date | Application_Method | Response_Status | Interview_Stage | Notes
```

**Default values:**
- Times_Seen: 1
- First_Seen_Date: CURRENT_WEEK
- Last_Seen_Date: CURRENT_WEEK
- **URL_Status: "Not Checked"** ← check_urls.py fills this in Phase 2
- Applied_Date through Notes: leave blank

**Branded XLSX:** {RESULTS_PATH}/[First_Last]_CURRENT_WEEK.xlsx

**Executed prompt:** {BASE_PATH}/searches/For_Others/[First_Last]/executed_CURRENT_WEEK.txt

---

### VERIFICATION

Show summary:
| Metric | Count |
|--------|-------|
| Total jobs found | X |
| Jobs scoring 70+ | Y |
| NEW jobs | Z |
| REPEAT jobs | W |

Files saved at: [list paths]

---

## STOP HERE

**Phase 1 complete.** Next step is Phase 2 (VERIFY):

```bash
python3 JC3/check_urls.py results/For_Others/[First_Last]/Week_of_CURRENT_WEEK/[First_Last]_CURRENT_WEEK.csv
```

---

*Template v3.1 | 2026-03-02 | Pipeline-aligned*
