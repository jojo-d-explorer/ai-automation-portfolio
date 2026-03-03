# ONE-CLICK WEEKLY SEARCH: VIVIENNE PHAM — v3.1

**This prompt does:** SEARCH + SCORE only (Phase 1)  
**This prompt does NOT do:** URL verification — that's Phase 2, run separately

---

## PIPELINE CONTEXT

This is **Phase 1 of 7**. After this prompt completes:

```bash
python3 JC3/check_urls.py results/For_Others/Vivienne_Pham/Week_of_[DATE]/Vivienne_Pham_[DATE].csv
```

---

**Owner:** Joey Clark (running on behalf of Vivienne Pham)  
**Resume file:** Vivienne_Pham_Resume.pdf  
**Last updated:** 2026-03-02

**Note:** 3 role archetypes — Operator (Finance), Capital Markets (IR), Ecosystem (BD)

---

## THE PROMPT

Calculate today's date and determine:
- Current week start date (most recent Monday): CURRENT_WEEK
- Previous week start date (Monday before that): PREVIOUS_WEEK

Define path variables:
- BASE_PATH = /Users/jc3/GitHub/ai-automation-portfolio
- RESULTS_PATH = {BASE_PATH}/results/For_Others/Vivienne_Pham/Week_of_CURRENT_WEEK

---

### CONFIGURATION

**Job Boards (3 boards):**
- site:boards.greenhouse.io
- site:jobs.lever.co
- site:jobs.ashbyhq.com

**Roles (3 archetypes):**

*Operator:*
- VP Finance
- CFO
- Head of Finance
- Director of Finance

*Capital Markets:*
- IR Director
- Investor Relations
- Head of IR

*Ecosystem:*
- Director of Business Development
- Portfolio Operations
- Director of Growth

**Locations:**
- New York, NY
- Washington DC
- Remote-US

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

Using attached resume (Vivienne_Pham_Resume.pdf), score each job 1-100:

**Seniority Match (30 points):**
- Director, VP, C-suite: full credit
- Senior Manager: 22/30
- Manager: 15/30
- Below: 5/30

**Skills Match (25 points):**
- Key skills: Investment banking, legal, infrastructure policy, deal execution, financial modeling

**Location Flexibility (20 points):**
- NYC, DC: full credit
- Remote-US: full credit
- Other major US: 10/20

**Industry Fit (15 points):**
- Defense tech, AI/ML, energy, cybersecurity: full credit
- Adjacent (govtech, aerospace, climate): 10/15
- Other: 5/15

**Salary Fit (10 points):**
- $200K+ total comp: full credit
- $150K-$200K: 7/10
- Below $150K: 4/10
- Not listed: 5/10

**Clearance handling:** If TS/SCI required, apply -15 penalty (still include if 70+).

Provide 1-2 sentence Score_Rationale.

**Filter to 70+ only. Rank by score descending.**

---

### NEW/REPEAT DETECTION

Compare to: {BASE_PATH}/results/For_Others/Vivienne_Pham/Week_of_PREVIOUS_WEEK/Vivienne_Pham_PREVIOUS_WEEK.csv

- File exists → mark NEW or REPEAT
- No file → mark all NEW

---

### OUTPUT FILES

**Weekly CSV:** {RESULTS_PATH}/Vivienne_Pham_CURRENT_WEEK.csv

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

**Branded XLSX:** {RESULTS_PATH}/Vivienne_Pham_CURRENT_WEEK.xlsx

---

### VERIFICATION

Show summary with job counts, files saved.

---

## STOP HERE

**Phase 1 complete.** Run Phase 2:

```bash
python3 JC3/check_urls.py results/For_Others/Vivienne_Pham/Week_of_CURRENT_WEEK/Vivienne_Pham_CURRENT_WEEK.csv
```

---

*v3.1 | 2026-03-02*
