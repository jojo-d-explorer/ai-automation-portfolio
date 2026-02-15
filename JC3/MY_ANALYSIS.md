# MY ANALYSIS PROMPT — Personal Search Intelligence

*Run this after consolidating weekly search results into my master database.*
*Runs all 5 analysis queries in a single pass and produces a comprehensive strategy report.*

---

## ⚙️ CONFIGURATION

```
MASTER_DATABASE: /Users/jc3/GitHub/ai-automation-portfolio/master_job_database.csv
RESUME_FILE: Joey_Clark_Resume_2026.pdf
OUTPUT_FILE: /Users/jc3/GitHub/ai-automation-portfolio/learning_log/analysis_joey_[YYYY-MM-DD].md
```

---

## PROMPT — Copy Everything Below This Line

---

Calculate today's date. Use it for the OUTPUT_FILE path.

Read my master job database at:
`/Users/jc3/GitHub/ai-automation-portfolio/master_job_database.csv`

Also reference the attached resume: `Joey_Clark_Resume_2026.pdf`

First, perform a DATA QUALITY CHECK. Show me:
1. Total rows in database
2. Total columns and their names (confirm 19-column schema)
3. How many jobs have scores (Score > 0) vs unscored (Score = 0 or blank)
4. Date range covered (earliest Source_Date to latest)
5. Number of distinct Search_Batch values (how many weekly searches consolidated)
6. Any blank or missing fields to flag (especially Score, Sector, Work_Arrangement)
7. If any unscored jobs exist: flag them for retroactive scoring after this analysis

Then run ALL 5 ANALYSES below sequentially. For each analysis, show results AND interpretation.

---

### ANALYSIS 1: Score Distribution Patterns

Focus on scored jobs only (Score > 0).

Show me:

1. SCORE RANGES:
   - 90-100: X jobs (elite matches) — list them all
   - 80-89: Y jobs (strong matches)
   - 70-79: Z jobs (good matches)
   - Below 70: W jobs (flag — why are these in the database?)

2. TOP 10 HIGHEST SCORING JOBS:
   - Score | Company | Job_Title | Sector | Location | Work_Arrangement
   - Sorted by Score descending

3. SECTOR PERFORMANCE (only sectors with 3+ jobs):
   - Sector | Avg_Score | Job_Count
   - Sorted by Avg_Score descending

4. COMPARISON TO LAST ANALYSIS (if previous analysis file exists):
   - Has the score distribution shifted?
   - Any new entries in the 90+ tier?
   - Did sector rankings change?

5. INTERPRETATION:
   - What's my "sweet spot" score range?
   - Should I adjust the 70+ threshold?
   - Which sectors consistently score highest for my background?

---

### ANALYSIS 2: Sector Concentration Mapping

Analyze ALL jobs (scored and unscored).

Show me:

1. SECTOR BREAKDOWN:
   - Sector | Total_Jobs | Scored_Jobs | Avg_Score | Highest_Score
   - Sort by Total_Jobs descending

2. SECTOR DIVERSITY:
   - How many distinct sectors are represented?
   - Is the search too concentrated or well diversified?

3. EMERGING SECTORS:
   - Any sectors appearing only in recent batches?
   - New opportunities or search parameter changes?

4. MY SECTOR SWEET SPOTS (based on resume alignment):
   - Fintech (banking/VC background)
   - AI/ML (current learning trajectory)
   - Defense/Gov Tech (DoD program management experience)
   - B2B SaaS (ecosystem building experience)
   - Are these sectors actually producing the best matches?

5. INTERPRETATION:
   - Which 3 sectors should I prioritize?
   - Any sectors worth dropping?
   - Any underexplored sectors worth adding?

---

### ANALYSIS 3: Company Patterns & Hiring Signals

Analyze ALL jobs (scored and unscored).

Show me:

1. COMPANY FREQUENCY (companies appearing 2+ times):
   - Company | Job_Count | Roles_Posted | Avg_Score | Sector
   - Sort by Job_Count descending

2. MULTI-ROLE COMPANIES:
   - Which companies posted multiple DIFFERENT roles?
   - This signals team expansion — worth prioritizing for outreach

3. SCORE CONSISTENCY (for multi-job companies):
   - Tight cluster = consistent fit. Wide range = role-dependent.

4. HIRING SIGNAL STRENGTH:
   - 2 jobs = active hiring
   - 3+ jobs = aggressive expansion
   - Which companies should I prioritize for networking?

5. NETWORKING PRIORITY LIST:
   - Top 10 companies to research and find warm intros
   - Cross-reference: do any overlap with Anzu Partners portfolio or my existing network?

6. INTERPRETATION:
   - Top 5 companies to prioritize and why
   - Any company patterns worth building outreach around?

---

### ANALYSIS 4: Work Arrangement & Geographic Distribution

Analyze ALL jobs.

Show me:

1. WORK ARRANGEMENT BREAKDOWN:
   - Remote (all variants): X jobs (Y%)
   - Hybrid: X jobs (Y%)
   - In-Office: X jobs (Y%)
   - Unclear/N/A: X jobs (Y%)

2. REMOTE DETAIL:
   - Remote-US | Remote-Americas | Remote-Global | Other variants
   - Flag any inconsistent labeling for cleanup

3. SCORE BY ARRANGEMENT (scored jobs only):
   - Avg Score: Remote vs Hybrid vs In-Office
   - Confirm whether Remote continues to outperform for my profile

4. LOCATION CLUSTERING (non-fully-remote jobs):
   - City/Region | Job_Count | Avg_Score
   - Focus on: DC, NYC, SF, Lisbon, and any other cities appearing

5. DUAL-BASE ANALYSIS:
   - I split time between Washington DC and Lisbon, Portugal
   - Which jobs accommodate either location?
   - Are there opportunities specifically in Lisbon or EU-remote?

6. INTERPRETATION:
   - Should I continue Remote + city searches, or narrow focus?
   - Are DC-based opportunities competitive with Remote scores?
   - Any geographic hubs worth adding to searches?

---

### ANALYSIS 5: Search Evolution & Efficiency

Group jobs by Search_Batch (or Source_Date week).

Show me:

1. VOLUME BY BATCH:
   - Batch/Week | Total_Jobs | Scored_Jobs | Avg_Score | Score_Range
   - Chronological order

2. PARAMETER CHANGES:
   - What changed between batches?
   - Locations, roles, boards — infer from the data

3. EFFICIENCY TREND:
   - Are later searches finding BETTER matches?
   - Are later searches finding MORE relevant jobs?
   - Quality vs quantity tradeoff?

4. NEW vs REPEAT:
   - Jobs appearing in multiple batches (Times_Seen > 1)?
   - Repeat sightings = persistent demand signal
   - If no repeats yet, note what this will show with more data

5. BOARD PERFORMANCE (if Found_On data exists):
   - Which boards produced the highest-scoring results?
   - Which boards had the most unique finds?
   - LinkedIn vs Greenhouse vs Lever vs Ashby performance

6. LEARNING CURVE:
   - Am I getting better at searching? (prompt refinement over time)
   - What did early batches teach me that improved later ones?

7. INTERPRETATION:
   - Is the search improving over time?
   - What should my NEXT search focus on?
   - Predict: expected results if current parameters continue

---

## STRATEGIC SUMMARY

After all 5 analyses, provide a consolidated strategic summary:

1. **TOP FINDINGS** (3-5 most important insights)

2. **APPLY NOW** (immediate actions):
   - Top 10 jobs to apply to, ranked by score + strategic fit
   - For each: Company | Role | Score | Why prioritize

3. **NETWORK NOW** (outreach targets):
   - Top 5 companies for warm intro research
   - Cross-reference with Anzu Partners network where possible

4. **SEARCH OPTIMIZATION** (for next weekly search):
   - Keep: parameters that are working
   - Add: new parameters to try
   - Drop: parameters that aren't producing
   - Watch: emerging trends to monitor

5. **DATA GAPS**:
   - Unscored jobs that need retroactive scoring
   - Sparse fields (salary, etc.)
   - What becomes possible with more weeks of data

6. **WEEK-OVER-WEEK DELTA** (if previous analysis exists):
   - What changed since last analysis?
   - New companies entering the pipeline
   - Score trend direction

---

Save the complete analysis to:
`/Users/jc3/GitHub/ai-automation-portfolio/learning_log/analysis_joey_[TODAY'S DATE].md`

Confirm the file was saved and show the file path.
