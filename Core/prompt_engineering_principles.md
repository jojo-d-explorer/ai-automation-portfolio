# Prompt Engineering Principles & Best Practices

*Learned through Weeks 1-3 of AI Automation Curriculum*

---

## Core Principles

### 1. Be Explicit, Not Implicit

**Bad:** "Search for jobs"
**Good:** "Search boards.greenhouse.io for 'Chief of Staff' roles posted in last 24 hours"

**Why:** AI interprets literally. Assumptions lead to unexpected results.

---

### 2. Structure Beats Stream-of-Consciousness

**Bad:** Long paragraph with everything mixed together
**Good:** Clear sections (Config, Extraction, Output, Verification)

**Why:** Structured prompts are easier to debug, modify, and reuse.

---

### 3. Handle Edge Cases Upfront

**Bad:** "Compare to last week's file"
**Good:** "If previous week file exists, compare. If not (first run), mark all jobs as NEW."

**Why:** Automation breaks on edge cases if not anticipated.

---

### 4. Verify Everything

**Bad:** "Save the file"
**Good:** "Save to [path], then confirm the file was saved and show me the location"

**Why:** Silent failures waste time. Verification catches issues immediately.

---

### 5. Platform-Specific Behavior Matters

**Bad:** "Check if this URL is still active" (assumes all platforms behave the same)
**Good:** "For Ashby URLs, call the GraphQL API. For Greenhouse/Lever, check HTTP status + scan for closed-job phrases. For LinkedIn, skip automated checking entirely."

**Why:** Generic solutions produce false results. Each platform has unique failure modes:
- Ashby: Client-side rendered (JavaScript). HTTP request returns empty HTML shell. Need GraphQL API.
- LinkedIn: Never returns 404 for dead jobs. "No longer accepting applications" rendered client-side.
- Greenhouse/Lever: Server-rendered. HTTP status + content scanning works.
- Cross-domain redirects: Dead ATS jobs redirect to company careers page (different domain).

---

### 6. Separate Configuration from Logic

**Bad:** Roles, locations, and scoring weights scattered throughout a prompt
**Good:** Clear CONFIGURATION block at the top, reusable logic engine below

**Why:** When serving multiple users, only the config changes. The engine stays the same. This is how ONE_CLICK_TEMPLATE_Friends.md works — swap 10-15 lines of config per person, everything else is shared.

---

## Prompt Structure Template

```markdown
[CONTEXT CALCULATION]
Calculate dates, determine states, set variables

[CONFIGURATION]
Boards: X, Y, Z
Roles: A, B, C
Locations: 1, 2, 3

[EXECUTION]
Step-by-step what to do
Show progress as you work

[EXTRACTION]
Field 1 (use "N/A" if not available)
Field 2 (convert to X format)
Field 3

[LOGIC & PROCESSING]
Deduplication rules
Scoring criteria
Filtering thresholds

[OUTPUT]
File 1: [full path] with columns [exact order]
File 2: [full path] with columns [exact order]

[VERIFICATION]
Confirm files saved
Show summary of results
Report any errors
```

---

## Field Extraction Best Practices

### Always Specify Missing Data Behavior

```markdown
Extract these fields (use "N/A" if not available):
- Company
- Salary (convert to USD; "N/A" if not listed)
- Language_Requirement (if no language mentioned, "N/A"; if other than English, list it)
```

**Why:** Prevents blank cells, inconsistent data formats.

---

### Be Explicit About Data Transformation

**Bad:** "Get the salary"
**Good:** "Salary (if listed, convert to USD if in other currency; if not listed, 'N/A')"

**Why:** Different currencies, formats, missing data all need handling.

---

### Specify Column Order

```markdown
CSV columns (in this order):
Status | Score | Score_Rationale | Company | Job_Title | Sector | Location |
Language_Requirement | Work_Arrangement | Salary_USD | Job_Summary | URL |
URL_Status | Found_On
```

**Why:** Makes scanning results easier, consistency across files and users.

---

### Standardize Categorical Fields

```markdown
Work Arrangement — classify as exactly one of:
Remote-US, Remote-Global, Hybrid, In-Office, Unclear
```

**Why:** Without standardization, you get "remote", "Remote", "WFH", "Work from home", "Distributed" — all meaning the same thing but impossible to filter.

---

## File Path Best Practices

### Always Use Full Absolute Paths

**Bad:** `results/file.csv`
**Good:** `/Users/jc3/GitHub/ai-automation-portfolio/results/file.csv`

**Why:** Relative paths depend on where CoWork thinks it is. Absolute paths always work.

---

### Always Include File Extensions

**Bad:** `Save as prompt_library`
**Good:** `Save as prompt_library.md`

**Why:** System might default to .txt when you want .md. Be explicit.

---

### Use ISO Date Format in Filenames

**Bad:** `results_2-4.csv`
**Good:** `results_2026-02-04.csv`

**Why:** Consistency, sortability, clarity.

---

### Create Folders If Needed

```markdown
Create folder if doesn't exist: /path/to/folder/
Then save file: /path/to/folder/file.csv
```

**Why:** Prevents "folder not found" errors.

---

## Dynamic Variables & State Management

### Let the System Calculate Dates

**Instead of manually updating:**
```markdown
Search for jobs posted after 2026-01-26
```

**Do this:**
```markdown
Calculate today's date.
Determine CURRENT_WEEK (most recent Monday).
Determine PREVIOUS_WEEK (Monday before that).
Search for jobs posted after PREVIOUS_WEEK.
```

**Why:** Eliminates manual updates. Same prompt works every week.

---

### Handle State Gracefully

```markdown
Compare results to /path/to/previous.csv
If file exists: Mark jobs not in previous as "NEW"
If file doesn't exist (first run): Mark all as "NEW"
```

**Why:** First run has no previous file. System shouldn't error.

---

## Deduplication Logic

### Be Specific About What Constitutes a Duplicate

**Vague:** "Remove duplicates"
**Clear:** "If same Company + same Job_Title across different boards, keep highest-scoring version. List all boards where found in 'Found_On' column."

**Why:** "Duplicate" is ambiguous. Same job title at different companies? Same company, slightly different title? Define it.

---

## Scoring & Filtering

### Make Criteria Explicit

**Vague:** "Score jobs based on fit"
**Clear:**
```markdown
Score 1-100 based on:
- Skills fit (40 points)
- Industry alignment (35 points)
- Experience match (25 points)
Provide 1-2 sentence rationale.
Filter to 70+ only.
```

**Why:** Reproducibility. You can refine weights if results aren't good.

---

### Scoring Doesn't Need to Be Precise — It Needs to Be Consistent and Useful

Key insight from Week 3: Whether healthcare gets -10 or -12 doesn't matter. What matters is "does healthcare end up lower than fintech in my ranked list?" Scoring systems are useful if they rank jobs in an order that matches priorities, filter out jobs you'd never apply to, and surface jobs you're excited about.

**Approach:** Start simple (no sector adjustments), let data accumulate, then refine based on actual application patterns — not arbitrary guesses.

---

### Handle Missing Salary Data

```markdown
Salary scoring rule:
- Listed and meets target: full credit
- Listed but below target: score proportionally
- Not listed ("N/A"): award half points (neutral — don't penalize unknown)
```

**Why:** Most jobs don't list salary. Penalizing unknown salary would eliminate 70%+ of results.

---

### Request Explanations

**Just numbers:** "Score: 85"
**Actionable:** "Score: 85. Rationale: Strong strategic partnerships background (40/40), fintech sector aligns with banking experience (28/35), role expects 10+ years (23/25)."

**Why:** Understand why job scored high/low. Helps refine scoring logic.

---

## Multi-User Prompt Architecture

### Template Inheritance Pattern

```
ONE_CLICK_TEMPLATE_Friends.md     ← Master template (shared logic engine)
    ↓ customize config block
ONE_CLICK_Aaron_Kimson.md         ← Aaron's specific roles/locations/weights
ONE_CLICK_Phil_Tassi.md           ← Phil's specific roles/locations/weights
ONE_CLICK_Vivienne_Pham.md        ← Vivienne's (3 archetype approach)
```

**Why:** Improvements to the template engine flow to everyone. Only config differs per person.

### Scoring Weight Customization

Friends provide priority ranking (1-5: Industry, Salary, Skills, Location, Seniority). General principle: #1 priority gets 30-40 pts, #5 gets 10 pts.

**But:** Some categories overlap per industry. For finance-specific searches, "Skills Match" and "Industry Fit" may be nearly identical — combine them or embed skills into industry scoring.

### Board Selection by Industry

- **Default (tech/startup):** Greenhouse, Lever, Ashby (3 boards)
- **Finance/Hedge Fund:** ATS boards have limited coverage. LinkedIn supplement via direct search links is critical.
- **Defense Tech:** Standard boards work for larger companies (Shield AI, Anduril). Smaller defensetech may need company career page checks.

**General principle:** If first search yields <15 results on standard boards, the industry may need supplementary sources.

---

## Verification & Quality Assurance

### Post-Search URL Verification

```bash
python3 JC3/check_urls.py results/For_Others/[Name]/Master_Job_Database_[Name].csv
```

Run after every search cycle. Catches dead links before they reach the friend's email.

### Dry-Run Verification for System Changes

```bash
python3 JC3/verify_linkedin_removal.py
```

When making changes that cascade across multiple files, build a verification script that checks all affected files. Cheaper than debugging wrong outputs later.

### Trust = Verification

A system that delivers 10 great links is more valuable than one that delivers 30 links where 10 are dead. The check_urls.py work wasn't optional polish — it was foundational to the service being credible.

---

## Progress & Monitoring

### Request Progress Updates for Long Tasks

```markdown
Show progress matrix as you search each board/role/location combination.
```

**Why:** 36+ search combinations = 10-15 min runtime. Progress matrix shows it's working, not stuck.

---

### Request Summary at End

```markdown
After completing search, show:
- Total jobs found: X
- Jobs scoring 70+: Y
- NEW jobs: Z
- REPEAT jobs: W
- Files saved at: [paths]
```

**Why:** Quick verification everything worked as expected.

---

## Common Pitfalls & How to Avoid

### Pitfall 1: Assuming Context from Previous Runs

**Wrong assumption:** "CoWork remembers what I asked for yesterday"
**Reality:** Each prompt is independent.
**Fix:** Include all context in the prompt.

### Pitfall 2: Vague Time Filters

**Bad:** "Recent jobs"
**Good:** "Posted within last 7 days"

### Pitfall 3: Not Handling Missing Data

**Bad:** Extract salary (assumes it exists)
**Good:** Extract salary (use "N/A" if not listed)

### Pitfall 4: Overly Complex Single Prompt

**Problem:** 500-line prompt trying to do 10 things
**Fix:** Break into steps (ONE_CLICK → CONSOLIDATE → ANALYSIS)

### Pitfall 5: Assuming All Platforms Behave the Same

**Problem:** Generic URL check returns "open" for a dead Ashby job
**Fix:** Platform-specific detection logic

### Pitfall 6: Using Google Index for LinkedIn

**Problem:** `site:linkedin.com/jobs` returns months-old cached listings
**Fix:** Remove from automated search. Provide direct LinkedIn search links instead.

### Pitfall 7: Hardcoding Paths That Change

**Problem:** Script expects `searches/friends/` but actual folder is `searches/For_Others/`
**Fix:** Verify paths against actual repo structure before deploying scripts.

---

## Iteration & Refinement

### Start Simple, Add Complexity

**Week 1 prompt:** "Search LinkedIn for Chief of Staff jobs"
**Week 2 prompt:** "Search 3 boards, score against resume, compare to last week"
**Week 3 prompt:** "Search 3 boards for 5 users, verify URLs, scan funding newsletters, generate branded XLSX + PDF analysis"

**Why:** Get basic version working first. Layer in sophistication as real problems surface.

---

### Debug Systematically

**When prompt fails:**

1. Check file paths (most common issue)
2. Check date formatting
3. Check edge cases (first run? no previous file?)
4. Simplify: remove sections until it works, then add back
5. Check platform-specific behavior (is it an Ashby URL? LinkedIn?)

---

## Measuring Prompt Quality

**Good prompts have:**

- ✅ Clear structure (sections, headers)
- ✅ Explicit instructions (no assumptions)
- ✅ Edge case handling (what if X doesn't exist?)
- ✅ Verification steps (confirm it worked)
- ✅ Platform-aware logic (different platforms, different handling)
- ✅ Appropriate length (not too terse, not too verbose)

**Success rate:**

- Week 1: 40-50% work on first try
- Week 2: 70-80% work on first try
- Week 3: ~80% work on first try (failures are usually edge cases, not structural)
- Week 8 target: 90%+ work on first try

**Goal isn't perfection** - it's faster iteration and fewer surprises.

---

*Last updated: 2026-02-26*
*Reflects learnings through Week 3*
