# ONE-CLICK WEEKLY SEARCH: ROSALIND GAHAMIRE — v3.1

**This prompt does:** SEARCH + SCORE only (Phase 1)  
**This prompt does NOT do:** URL verification — that's Phase 2, run separately

---

## PIPELINE CONTEXT

This is **Phase 1 of 7**. After this prompt completes:

```bash
python3 JC3/check_urls.py results/For_Others/Rosalind_Gahamire/Week_of_[DATE]/Rosalind_Gahamire_[DATE].csv
```

---

**Owner:** Joey Clark (running on behalf of Rosalind Gahamire)  
**Resume file:** RosalindGahamireCV__2026__1_.pdf  
**Last updated:** 2026-03-02

---

## THE PROMPT

Calculate today's date and determine:
- Current week start date (most recent Monday): CURRENT_WEEK
- Previous week start date (Monday before that): PREVIOUS_WEEK

Define path variables:
- BASE_PATH = /Users/jc3/GitHub/ai-automation-portfolio
- RESULTS_PATH = {BASE_PATH}/results/For_Others/Rosalind_Gahamire/Week_of_CURRENT_WEEK

---

### CONFIGURATION

**Job Boards (3 boards):**
- site:boards.greenhouse.io
- site:jobs.lever.co
- site:jobs.ashbyhq.com

**Roles:**
- Brand Strategist
- Creative Strategist
- Marketing Manager
- Head of Marketing
- Brand Manager
- Creative Director

**Locations:**
- Lisbon, Portugal
- Remote-Global
- Remote-Europe
- Europe

**Deal-breaker:** Exclude US-only or US-timezone-required roles.

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
- Salary_USD (convert €1 = $1.08; "N/A" if not listed)
- Job_Summary (2-3 sentences)
- URL, Found_On (board name)

**Work Arrangement** — exactly one of: Remote-Global, Remote-Europe, Hybrid, In-Office, Unclear

---

### DEDUPLICATION

Same Company + Job_Title across boards → keep highest score, merge Found_On.

---

### SCORING

Using attached resume (RosalindGahamireCV__2026__1_.pdf), score each job 1-100:

**Location Flexibility (30 points):** — HIGHEST PRIORITY
- Lisbon-based: 30/30
- Remote-Global or Remote-Europe: 30/30
- Other European with remote flexibility: 20/30
- Hybrid in non-Lisbon Europe: 15/30
- US-only: 0/30 (exclude entirely)

**Skills Match (25 points):**
- Key skills: Brand strategy, creative direction, insight-led research, workshop facilitation, D2C marketing, content strategy
- Direct match: full credit
- Adjacent (product marketing, growth): 18/25
- Tangential (social media only): 10/25

**Industry Fit (20 points):**
- D2C consumer brands, creative agencies: full credit
- Consumer tech, lifestyle: 15/20
- B2B SaaS with strong brand: 12/20
- Other: 8/20

**Salary Fit (15 points):**
- €70K+ or equivalent: full credit
- €50K-€70K: 10/15
- Below €50K: 5/15
- Not listed: 8/15

**Seniority Match (10 points):** — LOWEST PRIORITY
- Senior/Lead/Head: full credit
- Manager: 8/10
- Director/VP: 7/10
- Junior: 3/10

Provide 1-2 sentence Score_Rationale.

**Filter to 70+ only. Rank by score descending.**

---

### NEW/REPEAT DETECTION

Compare to: {BASE_PATH}/results/For_Others/Rosalind_Gahamire/Week_of_PREVIOUS_WEEK/Rosalind_Gahamire_PREVIOUS_WEEK.csv

- File exists → mark NEW or REPEAT
- No file → mark all NEW

---

### OUTPUT FILES

**Weekly CSV:** {RESULTS_PATH}/Rosalind_Gahamire_CURRENT_WEEK.csv

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

**Branded XLSX:** {RESULTS_PATH}/Rosalind_Gahamire_CURRENT_WEEK.xlsx

---

### VERIFICATION

Show summary:
| Metric | Count |
|--------|-------|
| Total jobs found | X |
| Jobs scoring 70+ | Y |
| NEW jobs | Z |
| REPEAT jobs | W |
| Excluded (US-only) | X |

Files saved at: [list paths]

---

## STOP HERE

**Phase 1 complete.** Run Phase 2:

```bash
python3 JC3/check_urls.py results/For_Others/Rosalind_Gahamire/Week_of_CURRENT_WEEK/Rosalind_Gahamire_CURRENT_WEEK.csv
```

---

*v3.1 | 2026-03-02*
