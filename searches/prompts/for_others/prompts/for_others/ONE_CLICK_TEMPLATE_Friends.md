# ONE-CLICK WEEKLY SEARCH: [FRIEND NAME] — TEMPLATE

**Purpose:** Duplicate this file for each new friend. Replace all [BRACKETED] values with their intake questionnaire responses. Save as `ONE_CLICK_[Name].md` in `/searches/prompts/for_others/`.

**Setup checklist before first run:**
- [ ] Friend completed intake questionnaire
- [ ] Resume received (PDF) at joey.clark3@gmail.com
- [ ] Replaced all [BRACKETED] fields below
- [ ] Created results folder: `/results/[Name]/`
- [ ] Saved this file as `ONE_CLICK_[Name].md`

---

**Owner:** Joey Clark (running on behalf of [FRIEND NAME])
**Resume file:** [RESUME FILENAME.pdf]
**Created:** [DATE]
**Last updated:** [DATE]

---

## USAGE INSTRUCTIONS

1. Copy everything from "Calculate today's date..." to "...where everything was saved"
2. Paste into CoWork
3. Attach: [RESUME FILENAME.pdf]
4. Hit enter
5. Walk away for 10-15 minutes
6. Come back to results

---

## THE PROMPT

Calculate today's date and determine:
- Current week start date (most recent Monday): CURRENT_WEEK
- Previous week start date (Monday before that): PREVIOUS_WEEK

Use these dates for file paths and comparisons below.

---

### CONFIGURATION

**Job Boards (search all):**
- site:boards.greenhouse.io
- site:jobs.lever.co
- site:jobs.ashbyhq.com
- site:linkedin.com/jobs
[ADD/REMOVE BOARDS AS NEEDED — e.g., for finance roles, these ATS boards may have limited coverage. Consider supplementing with industry-specific channels.]

**Roles:**
[FROM INTAKE Q1 — list 3-5 specific titles]
- [Role 1]
- [Role 2]
- [Role 3]

**Locations:**
[FROM INTAKE Q2]
- [Location 1]
- [Location 2]
- [Location 3]

**Filters:**
- Posted within last 7 days
- [FROM INTAKE Q7 — deal-breakers become exclusion filters. Examples: "Exclude fully in-office roles" or "Full-time employment only, no contract" or "Exclude roles requiring 10+ years travel"]
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
- Working Arrangement (Remote / Hybrid / In-Office)
- Salary (convert to USD if in other currency; "N/A" if not listed)
- Job Summary (2-3 sentences)
- URL

---

### DEDUPLICATION

Eliminate duplicate jobs (same Company + same Job Title across boards). Keep highest-scoring version and list all boards where found in "Found_On" column.

---

### SCORING

Using attached resume ([RESUME FILENAME.pdf]), score each job 1-100 based on:

[SCORING WEIGHTS — adjust based on intake Q5 priority ranking. Default weights below. See weight adjustment guide at bottom of this file.]

**Industry Fit ([X] points):**
[FROM INTAKE Q3 — define what "good fit" means for this person's target industry]
- [Full credit criteria]
- [Partial credit criteria]
- [Minimal credit criteria]

**Salary Fit ([X] points):**
[FROM INTAKE Q4]
- Target: $[X]K+ base salary, $[X]K+ total compensation
- If salary listed and meets target: full credit
- If salary listed but below target: score proportionally
- If salary not listed ("N/A"): award [half points] (neutral — don't penalize unknown)

**Skills Match ([X] points):**
[FROM INTAKE Q6 — their top skills]
- Key skills to match: [Skill 1], [Skill 2], [Skill 3]
- Score based on overlap between resume skills and job requirements

**Location Flexibility ([X] points):**
- Role is in a target location: full credit
- Remote with flexibility: full credit
- Hybrid in target city: [X]/[max]
- Outside target locations: [X]/[max]

**Seniority Match ([X] points):**
- Score based on resume experience alignment with role requirements

Provide 1-2 sentence score rationale for each job.

Filter to jobs scoring 70+ only. Rank by score (highest to lowest).

---

### NEW JOB DETECTION

Compare against: /Users/jc3/GitHub/ai-automation-portfolio/results/[NAME]/Week_of_PREVIOUS_WEEK/Master_List_PREVIOUS_WEEK.csv

- If file exists: Mark jobs not in previous file as "NEW"
- If file doesn't exist (first run): Mark all jobs as "NEW"
- Add "Status" column with "NEW" or "REPEAT"

---

### OUTPUT FILES

Create folders if they don't exist:
- /Users/jc3/GitHub/ai-automation-portfolio/results/[NAME]/Week_of_CURRENT_WEEK/
- /Users/jc3/GitHub/ai-automation-portfolio/searches/prompts/for_others/[NAME]/

1. **Master List:**
/Users/jc3/GitHub/ai-automation-portfolio/results/[NAME]/Week_of_CURRENT_WEEK/Master_List_CURRENT_WEEK.csv

Columns (in this order): Status | Score | Company | Job_Title | Sector | Location | Salary_USD | Job_Summary | Work_Arrangement | Score_Rationale | URL | URL_Status | Found_On

2. **Top 10 New:**
/Users/jc3/GitHub/ai-automation-portfolio/results/[NAME]/Week_of_CURRENT_WEEK/Top10_New_CURRENT_WEEK.csv

Same columns, only top 10 jobs marked "NEW". If <10 new jobs, include all new jobs. If zero new jobs, create file with headers and note "No new jobs this week."

3. **Save executed prompt:**
/Users/jc3/GitHub/ai-automation-portfolio/searches/prompts/for_others/[NAME]/executed_CURRENT_WEEK.txt

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
- Master List: [full path]
- Top 10 New: [full path]
- Executed prompt: [full path]

Report any errors, broken URLs, or boards that returned zero results.

---

⚠️  REMINDER: After reviewing results, run CONSOLIDATE_TO_MASTER.md to update [NAME]'s master database (if applicable).

---

*Run every Sunday. Attach [NAME]'s resume each time.*

---
---

## WEIGHT ADJUSTMENT GUIDE (Joey's reference — don't copy into prompt)

**Default weights (100 points total):**
- Industry Fit: 35
- Skills Match: 25
- Seniority Match: 20
- Location Flexibility: 10
- Salary Fit: 10

**How to adjust based on intake Q5 (priority ranking 1-5):**

| Their #1 Priority | Suggested Adjustment |
|---|---|
| Salary | Salary → 30pts, reduce Industry to 25 |
| Location | Location → 25pts, reduce Skills to 20 |
| Skills Match | Skills → 35pts, reduce Industry to 25 |
| Industry Fit | Industry → 40pts (already high, keep) |
| Seniority | Seniority → 30pts, reduce Location to 10 |

**Aaron's example:** Ranked Industry > Salary > Skills > Location > Seniority
→ Industry 40, Salary 20, Location 20, Seniority 20 (Skills embedded in Industry for his finance-specific search)

**General principle:** Their #1 gets 35-40pts, #5 gets 10pts, middle three split the rest. Use judgment — some categories overlap for certain industries.
