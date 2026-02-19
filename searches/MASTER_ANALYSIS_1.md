# MASTER ANALYSIS PROMPT — Multi-Week Search Intelligence

*Use this after a friend has 2+ weeks of search results consolidated into their master database.*
*Runs all 6 analysis queries in a single pass and produces a comprehensive strategy report.*

---

## ⚙️ CONFIGURATION — Update These Per Person

```
FRIEND_NAME: [Name]
MASTER_DATABASE: /Users/jc3/GitHub/ai-automation-portfolio/friends/[NAME]/master_job_database.csv
RESUME_FILE: [Name]_Resume.pdf
OUTPUT_FILE: /Users/jc3/GitHub/ai-automation-portfolio/friends/[NAME]/analysis_[NAME]_[YYYY-MM-DD].md
TARGET_SECTORS: [e.g., defense tech, AI/ML, fintech, B2B SaaS]
TARGET_LOCATIONS: [e.g., Washington DC, Remote-US, NYC]
TARGET_SENIORITY: [e.g., Director/Head-of → Series A+ / $15M+]
NETWORK_CONTEXT: [e.g., "Anzu Partners portfolio", "JPM alumni", or "None specified"]
```

---

## PROMPT — Copy Everything Below This Line

---

Calculate today's date. Use it for the OUTPUT_FILE path above.

---

### STEP 0: WEEKLY INTELLIGENCE REFRESH

Before running analyses, gather fresh intelligence from my Gmail:

**0A — ADVICE REFRESH:**

Search my Gmail for emails from "Remote100K" (sender: hey@remote100k.com) received in the last 7 days.
- If a new email exists, extract the advice/editorial section (ignore the job listings).
- Append the new advice to the reference corpus below, noting the newsletter number and date.
- If no new email, proceed with the existing corpus.

**0B — FUNDING INTELLIGENCE SCAN:**

Search my Gmail for:
1. Emails from "StrictlyVC" (sender: connie@strictlyvc.com) received in the last 7 days
2. Emails from "FinSMEs" (sender: info@finsmes.com) received in the last 7 days

From each email, extract ALL funding announcements into a working list with these fields:
- Company name
- Location (city, country)
- What they do (1 sentence)
- Stage (Pre-Seed / Seed / Series A / B / C / D+)
- Round size (USD — convert if in EUR/GBP)
- Key investors (lead investor at minimum)
- Source (StrictlyVC / FINSmes / both)

Deduplicate across sources. Store this list for use in Analysis 6.

Show me: "Found [X] funding announcements across [Y] newsletter emails this week."

---

### STEP 1: SITUATION CHECK

Before generating the strategic summary later, **pause and ask me**:

> "Before I write [FRIEND_NAME]'s strategy section — any context on where they are right now? For example:
> - Just starting their search / actively applying / getting callbacks / interviewing / evaluating offers
> - Anything specific going on (frustrated, changing direction, got a rejection, excited about a company, etc.)
> - Any feedback on last week's results?
>
> Or say 'no context' and I'll infer from the data."

**Wait for my response before proceeding to the Strategic Summary.**

Use my response to select which advice themes are most relevant from the advice corpus below. Do NOT label advice as coming from Remote100K or call it "tips" — weave it naturally into the strategic recommendations as if it's part of the analysis.

---

Now read the master job database at:
`[MASTER_DATABASE path from config above]`

Also reference the attached resume for scoring context: `[RESUME_FILE from config above]`

First, perform a DATA QUALITY CHECK. Show me:
1. Total rows in database
2. Total columns and their names (confirm schema)
3. How many jobs have scores (Score > 0) vs unscored (Score = 0 or blank)
4. Date range covered (earliest Source_Date to latest)
5. Number of distinct Search_Batch values (how many weekly searches are consolidated)
6. Any blank or missing fields to flag (especially Score, Sector, Work_Arrangement)

Then run ALL 6 ANALYSES below sequentially. For each analysis, show results AND interpretation.

---

### ANALYSIS 1: Score Distribution Patterns

Focus on scored jobs only (Score > 0).

Show me:

1. SCORE RANGES:
   - 90-100: X jobs (elite matches) — list them
   - 80-89: Y jobs (strong matches)
   - 70-79: Z jobs (good matches)
   - Below 70: W jobs (flag these — why are they in the database?)

2. TOP 10 HIGHEST SCORING JOBS:
   - Score | Company | Job_Title | Sector | Location | Work_Arrangement
   - Sorted by Score descending

3. SECTOR PERFORMANCE (only sectors with 3+ jobs):
   - Sector | Avg_Score | Job_Count
   - Sorted by Avg_Score descending

4. INTERPRETATION:
   - What's the "sweet spot" score range? (where most jobs cluster)
   - Should the 70+ threshold be adjusted?
   - Which sectors consistently score highest?

---

### ANALYSIS 2: Sector Concentration Mapping

Analyze ALL jobs (scored and unscored).

Show me:

1. SECTOR BREAKDOWN:
   - Sector | Total_Jobs | Scored_Jobs | Avg_Score | Highest_Score
   - Sort by Total_Jobs descending

2. SECTOR DIVERSITY:
   - How many distinct sectors are represented?
   - Is the search too concentrated in 1-2 sectors, or well diversified?

3. EMERGING SECTORS:
   - Any sectors appearing only in recent batches (not earlier ones)?
   - Could signal new opportunities or search parameter changes

4. INTERPRETATION:
   - Which 3 sectors should be the primary focus?
   - Any sectors worth dropping from future searches?
   - Any underexplored sectors worth adding?

---

### ANALYSIS 3: Company Patterns & Hiring Signals

Analyze ALL jobs (scored and unscored).

Show me:

1. COMPANY FREQUENCY (companies appearing 2+ times):
   - Company | Job_Count | Roles_Posted | Avg_Score (if scored) | Sector
   - Sort by Job_Count descending

2. MULTI-ROLE COMPANIES:
   - Which companies posted multiple DIFFERENT roles?
   - Example: "Company X posted COS, Partnerships, and Strategy"
   - This signals broad hiring or team expansion

3. SCORE CONSISTENCY (for multi-job companies):
   - Do scores vary widely or cluster tightly?
   - Tight cluster = consistent fit. Wide range = role-dependent fit.

4. HIRING SIGNAL STRENGTH:
   - Companies with 2 jobs = active hiring
   - Companies with 3+ jobs = aggressive expansion
   - Which companies should be prioritized for networking/outreach?

5. INTERPRETATION:
   - Top 5 companies to prioritize and why
   - Should multi-role companies be treated as higher-priority targets?

---

### ANALYSIS 4: Work Arrangement & Geographic Distribution

Analyze ALL jobs.

Show me:

1. WORK ARRANGEMENT BREAKDOWN:
   - Remote (all variants): X jobs (Y%)
   - Hybrid: X jobs (Y%)
   - In-Office: X jobs (Y%)
   - Unclear/N/A: X jobs (Y%)

2. REMOTE DETAIL (break down Remote variants if present):
   - Remote-US | Remote-Americas | Remote-Global | Other variants
   - Note: flag any inconsistent labeling for cleanup

3. SCORE BY ARRANGEMENT (scored jobs only):
   - Avg Score: Remote vs Hybrid vs In-Office
   - Do higher-scoring jobs tend toward a particular arrangement?

4. LOCATION CLUSTERING (for non-fully-remote jobs):
   - City/Region | Job_Count | Avg_Score
   - Which geographic areas have the most opportunities?

5. LOCATION + SECTOR CROSS-REFERENCE:
   - Do certain sectors cluster geographically?
   - Is Remote more common in specific sectors?

6. INTERPRETATION:
   - Should future searches focus on Remote, specific cities, or both?
   - Are there geographic hubs worth targeting?
   - Any locations underperforming (low scores) that could be dropped?

---

### ANALYSIS 5: Search Evolution & Efficiency

Group jobs by Search_Batch (or Source_Date week).

Show me:

1. VOLUME BY BATCH:
   - Batch/Week | Total_Jobs | Scored_Jobs | Avg_Score | Score_Range
   - Chronological order

2. PARAMETER CHANGES:
   - What changed between batches? (roles searched, locations, boards)
   - Infer from the data: different locations appearing, new sectors, etc.

3. EFFICIENCY TREND:
   - Are later searches finding BETTER matches (higher avg scores)?
   - Are later searches finding MORE relevant jobs per search?
   - Or same volume but different composition?

4. NEW vs REPEAT:
   - How many jobs appear in multiple batches (Times_Seen > 1)?
   - Are repeat sightings increasing? (signals persistent demand)
   - If no repeats yet, note this and explain what it will show with more data

5. BOARD PERFORMANCE (if Found_On or Search_Source data exists):
   - Which boards/sources produced the highest-scoring results?
   - Which boards had the most unique finds (not found elsewhere)?

6. INTERPRETATION:
   - Is the search improving over time?
   - What should the NEXT search focus on based on trends?
   - Predict: expected results if current parameters continue

---

### ANALYSIS 6: Proactive Company Intelligence (Freshly Funded Companies)

Using the funding list extracted in Step 0B, cross-reference against [FRIEND_NAME]'s search criteria from CONFIGURATION.

**FILTER CRITERIA (strict — must match 2+ of the following):**

1. **SECTOR MATCH**: Company operates in one of [FRIEND_NAME]'s TARGET_SECTORS, or in an adjacent sector where their skills clearly transfer.
   - Direct match = strong signal
   - Adjacent match = note the connection explicitly

2. **LOCATION MATCH**: Company is based in one of [FRIEND_NAME]'s TARGET_LOCATIONS, OR is known to hire remote in relevant geographies, OR has a secondary office in a target location.

3. **STAGE MATCH**: Company is at a growth stage where [FRIEND_NAME]'s target roles typically get created. Use TARGET_SENIORITY from config:
   - C-suite / VP roles → Series B+ or $30M+ total raised
   - Director / Head-of roles → Series A+ or $15M+ total raised
   - Manager / Senior IC roles → Seed+ or $5M+ total raised

4. **INVESTOR SIGNAL**: Backed by a top-tier firm known for helping portfolio companies build strong leadership teams (a16z, Sequoia, Founders Fund, Lightspeed, Accel, General Catalyst, Benchmark, Index, Bessemer, NEA, GIC, Thrive Capital, Iconiq, Y Combinator, First Round, Felicis, Greylock, Sapphire, Eclipse — use judgment for unlisted firms).

**OUTPUT:**

If 0 companies pass the filter:
> "No freshly funded companies this week matched 2+ of [FRIEND_NAME]'s criteria. This is normal — strict filtering means only high-signal matches surface."

If 1+ companies pass the filter, present as a ranked table:

| # | Company | What They Do | Round | Location | Criteria Matched | Why Relevant |
|---|---------|-------------|-------|----------|-----------------|-------------|
| 1 | [Name] | [1 sentence] | [Stage, $Amount] | [City] | [e.g., Sector ✓ Stage ✓] | [Rationale tied to FRIEND_NAME's background] |

For each company, recommend an action:
- 🔍 **MONITOR** — Just raised; check their careers page in 2-4 weeks
- 📨 **REACH OUT** — At a stage where they'd need this role type now; proactive outreach to founder/COO/Head of People
- 🔗 **NETWORK** — Warm intro path likely exists through NETWORK_CONTEXT

Format each as:
```
[Company Name] → [ACTION]
Timing: [Now / 2-4 weeks / When they post]
Suggested entry point: [Who to contact — title, not name]
Connection path: [How to get introduced, or "Cold outreach — use LinkedIn"]
```

**PATTERN NOTES** (if applicable):
- Sectors showing repeated funding activity (market momentum)
- Companies appearing in BOTH job search results AND funding list (double signal — flag prominently)
- Geographic or investor clusters worth noting

---

## STRATEGIC SUMMARY

After all 6 analyses, provide a consolidated strategic summary:

1. **TOP FINDINGS** (3-5 bullet points — most important insights)

2. **RECOMMENDED ACTIONS** (what to do next):
   - Which jobs to apply to first (top 5-10 from the data)
   - Which companies to target for networking
   - Whether to adjust search parameters (boards, roles, locations, scoring weights)

3. **SEARCH OPTIMIZATION** (for next weekly search):
   - Keep: parameters that are working
   - Add: new parameters to try
   - Drop: parameters that aren't producing results
   - Watch: emerging trends to monitor

4. **DATA GAPS** (what's missing):
   - Unscored jobs that need scoring
   - Sparse fields (salary, etc.)
   - Analyses that will become possible with more data (application tracking, conversion rates, etc.)

5. **PROACTIVE TARGETS** (from Analysis 6):
   - Companies to watch from this week's funding activity
   - Suggested outreach timing (now vs. 2-4 weeks)
   - Cross-reference: any overlap between freshly funded companies and companies already in the job search results

6. **STRATEGIC ADVICE** (woven naturally into recommendations above):
   Based on Joey's context about where [FRIEND_NAME] is in their search process, integrate relevant job search strategy advice into the TOP FINDINGS, SEARCH OPTIMIZATION, and NETWORKING sections above. Do NOT create a separate tips section.

   The advice should feel like natural strategic recommendations emerging from the data, not generic tips. Connect advice to specific findings from the 6 analyses.

   Examples of good integration:
   - If Analysis 3 shows companies posting multiple roles → weave in advice about reaching out to hiring managers directly at those companies
   - If Analysis 1 shows high scores but Joey mentions no callbacks → integrate resume optimization advice tied to the specific sectors performing well
   - If Analysis 4 shows remote roles scoring highest → connect to advice about proactively addressing timezone challenges in applications
   - If Analysis 6 shows freshly funded companies in target sectors → weave in advice about proactive outreach timing and how to approach companies before roles are posted

---

Save the complete analysis to:
`[OUTPUT_FILE path from config above]`

Confirm the file was saved and show the file path.

---

### ADVICE REFERENCE CORPUS

**Stage: Early Search (first 1-2 weeks)**
- Every resume bullet should pass the "So what?" test — outcomes over responsibilities
- LinkedIn headline should lead with impact, not just title
- Set up job alerts on target boards so you're not manually scanning
- Tell your network you're looking — the hidden job market is real
- Optimize LinkedIn skills section with keywords from target job descriptions

**Stage: Active Applications (weeks 2-4)**
- Use AI/automation to scale application volume — manual-only doesn't work in 2026
- Focus human time on networking, resume tailoring for top-5 targets, and interview prep
- Cover letters: skip unless required; if writing, 3 paragraphs max, ultra-specific
- Track where you're applying — patterns in responses reveal what's working
- Follow up 5-7 business days after applying if no response

**Stage: Getting Callbacks / Interviewing**
- Questions to ASK: decision-making process, autonomy level, growth paths, why the role is open, what concerns they have about your candidacy
- Questions to AVOID: what the company does (shows no research), work-life balance (signals disengagement), promotions before starting, salary too early
- Prepare 3-5 stories using STAR format that map to the job description's top requirements
- After each interview, send a thank-you within 24 hours referencing something specific discussed

**Stage: Evaluating Offers**
- Calculate total comp (base + bonus + equity + benefits), not just salary
- Test if remote culture is real: ask about async vs sync, timezone expectations, in-person cadence
- Evaluate stability: runway, revenue trajectory, recent layoffs, leadership turnover
- Red flags: "we're a family," vague role descriptions, wide unexplained salary ranges, mandatory all-timezone meetings
- Trust your gut — if something feels off during the process, it usually is

**Stage: Negotiation**
- Document your impact with numbers before the conversation
- Frame as business value: "Based on market data and my track record of [specific impact], I'd like to discuss..."
- If they say no: ask "What would I need to accomplish to revisit this in 3-6 months?" Get specifics.
- Your company will pay the minimum they think keeps you from leaving. Job-hopping averages 10-20% increases vs 3-5% internal raises.

---

## NOTES FOR JOEY (Don't paste this part into CoWork)

### When to run this:
- After consolidating 2+ weeks of search results into a friend's master database
- Before running the next weekly search (use insights to adjust parameters)
- Monthly for friends with ongoing searches (track trends over time)

### Prerequisites:
- Friend must have a master_job_database.csv with consolidated results
- Database should follow the standard schema
- At least 2 Search_Batch values (otherwise Analysis 5 has nothing to compare)
- Gmail access for Step 0 (Remote100K advice + StrictlyVC/FINSmes funding intelligence)

### What this replaces:
- Running 5 separate analysis queries manually
- Running FUNDING_INTEL.md separately (now integrated as Analysis 6)
- Previously these were: Score Distribution, Sector Concentration, Company Patterns, Work Arrangement/Geography, Search Evolution
- This single prompt runs all 6 + adds a strategic summary with advice + funding intelligence

### The "copy everything below this line" boundary:
- CONFIGURATION section: update per person, paste into CoWork
- Everything from "Calculate today's date" through "Confirm the file was saved": this is the prompt
- ADVICE REFERENCE CORPUS: paste this too — it's the reference material the prompt draws from
- NOTES FOR JOEY: don't paste, this is just for you

### Adapting for specific friends:
- If a friend cares more about location than remote, emphasize Analysis 4 results
- If a friend is in finance (e.g., Aaron), note that board coverage may differ
- TARGET_SECTORS, TARGET_LOCATIONS, TARGET_SENIORITY drive the Analysis 6 filter — set these carefully per person
- NETWORK_CONTEXT enables the 🔗 NETWORK action in Analysis 6 — include any relevant connections

### How Analysis 6 connects to the standalone FUNDING_INTEL.md:
- FUNDING_INTEL.md: standalone, runs anytime, own config. Use for first-run intel or mid-week checks.
- Analysis 6 here: integrated, runs as part of the full analysis sequence, pulls config from CONFIGURATION block above.
- Don't run both for the same person in the same week — they do the same thing.

### Schema reminder (22 columns with tracking):
Score | Company | Job_Title | Location | Work_Arrangement | Salary | URL | Posted_Date | Board | Role_Category | Sector | Score_Rationale | Source_Date | Search_Batch | Found_On | First_Seen_Date | Last_Seen_Date | Times_Seen | Status | Interest | Interest_Notes | Applied_Date | Response | Response_Date
