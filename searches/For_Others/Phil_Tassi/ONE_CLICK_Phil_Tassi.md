# ONE-CLICK WEEKLY SEARCH: PHIL TASSI — v3.1

**This prompt does:** SEARCH + SCORE only (Phase 1)  
**This prompt does NOT do:** URL verification — that's Phase 2, run separately

---

## PIPELINE CONTEXT

This is **Phase 1 of 7**. After this prompt completes:

```bash
python3 JC3/check_urls.py results/For_Others/Phil_Tassi/Week_of_[DATE]/Phil_Tassi_[DATE].csv
```

---

**Owner:** Joey Clark (running on behalf of Phil Tassi)  
**Resume file:** Phil_Tassi_Resume.pdf  
**Last updated:** 2026-03-02

---

## THE PROMPT

Calculate today's date and determine:
- Current week start date (most recent Monday): CURRENT_WEEK
- Previous week start date (Monday before that): PREVIOUS_WEEK

Define path variables:
- BASE_PATH = /Users/jc3/GitHub/ai-automation-portfolio
- RESULTS_PATH = {BASE_PATH}/results/For_Others/Phil_Tassi/Week_of_CURRENT_WEEK

---

### CONFIGURATION

**Job Boards (3 boards):**
- site:boards.greenhouse.io
- site:jobs.lever.co
- site:jobs.ashbyhq.com

**Roles:**
- Chief of Staff
- Partnerships
- Business Development
- Director of Partnerships
- Head of BD

**Locations:**
- Washington DC
- London, UK
- Remote-US
- Remote-Global

**Filters:**
- Posted within last 7 days
- For each board/role/location combination, extract up to 20 results

Show progress matrix as you search.

---

### SOURCE FILTERING

**Only include results from target ATS boards.**

**Exclude aggregators:** Jobgether, Talent.com, Lensa, Jooble, Adzuna, SimplyHired, ZipRecruiter, Snagajob, Indeed, Glassdoor.

**URL rules:**
- Must be job-specific URL with job ID
- Exclude board roots without job ID
- Exclude generic career pages

**Anti-hallucination:** Only include jobs you actually visited. Zero results = report zero.

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

Using attached resume (Phil_Tassi_Resume.pdf), score each job 1-100:

**Industry Fit (35 points):**
- Defense tech, AI/ML, fintech, B2B SaaS, climate tech: full credit
- Adjacent tech sectors: 25/35
- Non-tech: 10/35

**Skills Match (25 points):**
- Key skills: Startup ecosystem building, partnership development, VC/investor relations, strategic operations

**Seniority Match (20 points):**
- Director/VP/Head level: full credit
- Manager level: 15/20
- Entry/junior: 5/20

**Location Flexibility (10 points):**
- London, Washington DC: full credit
- Remote-US, Remote-Global: full credit
- Other: 5/10

**Salary Fit (10 points):**
- $150K+ or £120K+: full credit
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
- **URL_Status: "Not Checked"**
- Applied_Date through Notes: leave blank

**Branded XLSX:** {RESULTS_PATH}/Phil_Tassi_CURRENT_WEEK.xlsx

---

### VERIFICATION

Show summary with job counts, files saved.

---

## STOP HERE

**Phase 1 complete.** Run Phase 2:

```bash
python3 JC3/check_urls.py results/For_Others/Phil_Tassi/Week_of_CURRENT_WEEK/Phil_Tassi_CURRENT_WEEK.csv
```

---

*v3.1 | 2026-03-02*
