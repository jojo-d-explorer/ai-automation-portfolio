# Prompt Engineering Principles & Best Practices

*Learned through Weeks 1-2 of AI Automation Curriculum*

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
**Good:** "Salary (if listed, convert to USD; if in other currency, use wise.com rates; if not listed, 'N/A')"

**Why:** Different currencies, formats, missing data all need handling.

---

### Specify Column Order

```markdown
CSV columns (in this order):
Score | Company | Job_Title | Location | Salary | URL
```

**Why:** Makes scanning results easier, consistency across files.

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

**Bad:** `results_2-4.csv` (ambiguous: Feb 4? Day 4 of month 2?)
**Good:** `results_2026-02-04.csv` (unambiguous, sorts correctly)

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
Compare to /results/Week_of_2026-01-26/file.csv
```

**Do this:**

```markdown
Calculate today's date.
Determine CURRENT_WEEK (most recent Monday).
Determine PREVIOUS_WEEK (Monday before that).
Search for jobs posted after PREVIOUS_WEEK.
Compare to /results/Week_of_PREVIOUS_WEEK/file.csv
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

### Request Explanations

**Just numbers:** "Score: 85"
**Actionable:** "Score: 85. Rationale: Strong strategic partnerships background (40/40), fintech sector aligns with banking experience (28/35), role expects 10+ years (23/25)."

**Why:** Understand why job scored high/low. Helps refine scoring logic.

---

## Progress & Monitoring

### Request Progress Updates for Long Tasks

```markdown
Show progress matrix as you search each board/role/location combination.
```

**Why:** 27 search combinations = 10-15 min runtime. Progress matrix shows it's working, not stuck.

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

---

### Pitfall 2: Vague Time Filters

**Bad:** "Recent jobs"
**Good:** "Posted within last 7 days"

**Why:** "Recent" is subjective. Be precise.

---

### Pitfall 3: Not Handling Missing Data

**Bad:** Extract salary (assumes it exists)
**Good:** Extract salary (use "N/A" if not listed)

**Why:** Most jobs don't list salary. Handle it gracefully.

---

### Pitfall 4: Overly Complex Single Prompt

**Problem:** 500-line prompt trying to do 10 things
**Fix:** Break into steps or multiple prompts

**When to split:**

- Prompt tries to do >5 distinct tasks
- Runtime >15 minutes
- Hard to debug when something fails

---

## Iteration & Refinement

### Start Simple, Add Complexity

**Week 1 prompt:** "Search LinkedIn for Chief of Staff jobs"
**Week 2 prompt:** "Search 3 boards, score against resume, compare to last week"

**Why:** Get basic version working first. Layer in sophistication.

---

### Document What Works

**After successful prompt:**

- Save to prompt library
- Note runtime, results, any issues
- Mark what could be improved

**Why:** Build knowledge over time. Don't reinvent each search.

---

### Debug Systematically

**When prompt fails:**

1. Check file paths (most common issue)
2. Check date formatting
3. Check edge cases (first run? no previous file?)
4. Simplify: remove sections until it works, then add back

---

## Advanced Techniques

### Nested Conditionals

```markdown
If previous file exists:
  If jobs in previous file:
    Compare and mark NEW/REPEAT
  Else:
    Mark all as NEW (previous file was empty)
Else:
  Mark all as NEW (first run)
```

---

### Multi-Output Strategy

**Single search → Multiple deliverables:**

- Master_List.csv (all results)
- Top10_New.csv (actionable subset)
- executed_prompt.txt (reproducibility)

**Why:** Different audiences, different needs.

---

## Syntax & Technical Notes

### Comments in Code/Config

`#` = Comment (ignored by system)

```markdown
# This is a comment
role = "Chief of Staff"  # This part runs, this part is a comment
```

---

### Boolean Search Operators

- `AND` = Both terms must appear
- `OR` = Either term can appear
- `"exact phrase"` = Exact match
- `site:domain.com` = Restrict to domain

**Example:** `site:boards.greenhouse.io ("Chief of Staff" OR "Strategy" OR "Operations") AND "remote"`

---

### File Extensions Matter

- `.md` = Markdown (formatted text, rendered nicely on GitHub)
- `.txt` = Plain text (no formatting)
- `.csv` = Comma-separated values (spreadsheet data)

**Always specify explicitly.** Don't let system guess.

---

## Measuring Prompt Quality

**Good prompts have:**

- ✅ Clear structure (sections, headers)
- ✅ Explicit instructions (no assumptions)
- ✅ Edge case handling (what if X doesn't exist?)
- ✅ Verification steps (confirm it worked)
- ✅ Appropriate length (not too terse, not too verbose)

**Success rate:**

- Week 1: 40-50% work on first try
- Week 2: 70-80% work on first try
- Week 8 target: 90%+ work on first try

**Goal isn't perfection** - it's faster iteration and fewer surprises.

---

*Last updated: 2026-02-06*
*Reflects learnings through Week 2*
