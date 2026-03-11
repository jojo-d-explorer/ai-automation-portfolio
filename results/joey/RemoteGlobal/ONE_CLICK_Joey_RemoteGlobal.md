# ONE_CLICK_Joey_RemoteGlobal.md
# Remote-Global Variant | 5 Boards | Joey Clark
# Last updated: 2026-03-09
# v1.1 — Removed JazzHR (applytojob.com): URLs redirect to generic landing page,
#         incompatible with URL verification pipeline.

---

## CONTEXT CALCULATION

Calculate today's date.
Determine CURRENT_WEEK: the most recent Monday on or before today (ISO format: YYYY-MM-DD).
Determine PREVIOUS_WEEK: the Monday before CURRENT_WEEK.
All date references below use these calculated values.

---

## CONFIGURATION

**User:** Joey Clark  
**Resume:** Attached PDF  
**Search variant:** Remote-Global only (standalone — does not replace the main weekly search)

**Target roles (search all):**
- "Chief of Staff"
- "Strategic Operations"
- "Head of Partnerships"
- "VP Partnerships"
- "Director of Partnerships"
- "Business Development" (senior/director/VP level only — filter out junior titles)

**Location filter:** Remote-Global ONLY  
- Include: Remote, Remote-Global, Remote (Worldwide), Remote (International), Remote (Europe), Work from anywhere
- Exclude: Remote-US only, roles requiring US residency/work authorization, roles requiring location in a specific city

**Boards to search (5 total):**
1. `site:boards.greenhouse.io`
2. `site:jobs.lever.co`
3. `site:jobs.ashbyhq.com`
4. `site:myworkdayjobs.com`
5. `site:app.welcometothejungle.com`

**Board notes:**
- `myworkdayjobs.com` — skews toward larger companies (Series D+, public). Score company fit accordingly.
- `app.welcometothejungle.com` — skews toward European companies and remote-first startups. Expect higher WTTJ representation for truly global remote roles. WTTJ uses short alphanumeric slugs (e.g. `/jobs/mGUwqlPc`) — these ARE valid specific job URLs, not generic pages.
- JazzHR (`applytojob.com`) was evaluated and excluded. Their URLs redirect to a generic JazzHR landing page rather than stable job posting pages — incompatible with URL verification.

---

## EXECUTION

For each combination of [role] × [board], run a Google search:

```
[role] "remote" site:[board]
```

Examples:
- `"Chief of Staff" "remote" site:boards.greenhouse.io`
- `"Head of Partnerships" "remote" site:myworkdayjobs.com`
- `"Strategic Operations" "remote" site:app.welcometothejungle.com`

**Show a progress matrix as you work.** Format:

```
Board                        | Role                    | Results
-----------------------------|-------------------------|--------
boards.greenhouse.io         | Chief of Staff          | X
boards.greenhouse.io         | Strategic Operations    | X
...
```

**Anti-hallucination rule:** Every job listing must come from an actual Google search result. Do not invent or estimate listings. If a board/role combination returns zero results, record 0 — do not create placeholder entries.

**URL integrity rule:** Only extract URLs that point to a specific job posting. A valid URL must contain a job ID. Reject generic career pages:
- ✅ KEEP: `boards.greenhouse.io/anthropic/jobs/5021140008` (numeric ID)
- ✅ KEEP: `jobs.ashbyhq.com/openai/abcdef12-3456-7890-abcd-ef1234567890` (UUID)
- ✅ KEEP: `myworkdayjobs.com/en-US/careers/job/Remote/Chief-of-Staff_JR1234` (titled path with ID)
- ✅ KEEP: `app.welcometothejungle.com/jobs/mGUwqlPc` (WTTJ 8-char slug — valid specific posting)
- ❌ REMOVE: `jobs.ashbyhq.com/kernel` (company name only, no job ID)
- ❌ REMOVE: `boards.greenhouse.io/anthropic` (no job path)

---

## EXTRACTION

For each valid job listing, extract the following fields. Use "N/A" if not available.

| Field | Instructions |
|-------|-------------|
| `Status` | Leave blank — will be filled in consolidation |
| `Score` | See scoring rubric below |
| `Score_Rationale` | 1-2 sentences explaining the score |
| `Company` | Company name |
| `Job_Title` | Exact title from listing |
| `Sector` | Industry/sector of the company |
| `Location` | As listed (e.g., "Remote (Worldwide)", "Remote - Europe") |
| `Language_Requirement` | If listing specifies a language requirement other than English, note it. Otherwise "N/A" |
| `Work_Arrangement` | Must be exactly: Remote-Global (for this search, all results should be Remote-Global; flag any that are not) |
| `Salary_USD` | If listed, convert to USD range. If not listed, "N/A" |
| `Job_Summary` | 2-3 sentence summary of the role |
| `URL` | Full specific URL to the job posting |
| `URL_Status` | Leave as "Not Checked" — will be verified by check_urls.py run locally |
| `Found_On` | Board name (e.g., "Greenhouse", "Lever", "Ashby", "Workday", "WTTJ") |

---

## SCORING RUBRIC (100 points)

Score each job 1–100 based on fit against the attached resume.

**Skills & Experience Match (40 points)**
- 36–40: Direct match — Chief of Staff, strategic ops, partnerships, BD at growth-stage startup or VC-backed company
- 28–35: Strong match — operations, strategy, or partnerships with executive exposure
- 20–27: Partial match — some relevant skills but significant gaps
- <20: Weak match

**Seniority Alignment (25 points)**
- 22–25: Director, VP, Head of, or Chief of Staff level
- 16–21: Senior Manager or equivalent with clear upward path
- <16: Too junior or too senior

**Industry & Company Fit (20 points)**
- 18–20: Growth-stage startup (Series A–D), VC/PE-backed, defense tech, fintech, AI/ML, govtech, climate tech
- 13–17: Adjacent industries — consulting, financial services with startup feel
- <13: Poor industry fit (large enterprise, nonprofit, healthcare admin, etc.)

**Remote-Global Eligibility (15 points)**
- 13–15: Explicitly "Remote (Worldwide)", "Work from anywhere", or Europe/international remote welcomed
- 8–12: Remote but ambiguous on geography — flag in Score_Rationale
- <8: Likely Remote-US only despite appearing in results — flag and consider excluding

**Score cutoff:** Include all results with Score ≥ 65. Flag but include scores 55–64 with a note.

---

## DEDUPLICATION

If the same Company + Job_Title appears on multiple boards:
- Keep the highest-scoring version
- Merge board names in `Found_On` (e.g., "Greenhouse, WTTJ")
- Do not create duplicate rows

---

## NEW vs. REPEAT

Compare results against the previous remote-global search file, if it exists:
`/Users/jc3/GitHub/ai-automation-portfolio/results/joey/RemoteGlobal/Master_RemoteGlobal_Joey.csv`

- If previous file exists: Mark jobs not in the previous file as `NEW`, jobs seen before as `REPEAT`
- If no previous file exists (first run): Mark all jobs as `NEW`

---

## OUTPUT

**Save the following files:**

**1. Weekly results CSV:**
```
/Users/jc3/GitHub/ai-automation-portfolio/results/joey/RemoteGlobal/Week_of_CURRENT_WEEK/Joey_RemoteGlobal_CURRENT_WEEK.csv
```
Create the folder if it doesn't exist.

**2. Also save an XLSX version** (same data, same path, `.xlsx` extension) for easy viewing in Numbers.

**Column order (14 columns):**
```
Status | Score | Score_Rationale | Company | Job_Title | Sector | Location |
Language_Requirement | Work_Arrangement | Salary_USD | Job_Summary | URL |
URL_Status | Found_On
```

Sort rows by Score descending.

---

## VERIFICATION

After saving both files, confirm:
1. Files saved at the correct paths — print full paths
2. Total jobs found (all scores)
3. Jobs scoring 65+
4. NEW vs. REPEAT breakdown
5. Jobs per board (how many results from each of the 5 boards)
6. Any boards that returned 0 results — note them explicitly
7. Any jobs flagged as "may be Remote-US only" — list them

If any output file cannot be saved, report the error immediately rather than proceeding silently.

---

## POST-SEARCH: URL VERIFICATION

Run check_urls.py from your local machine (not CoWork or any sandbox):

```bash
cd ~/GitHub/ai-automation-portfolio
python3 JC3/check_urls.py results/joey/RemoteGlobal/Week_of_CURRENT_WEEK/Joey_RemoteGlobal_CURRENT_WEEK.csv
```

**Note:** check_urls.py v2.1+ is required for correct WTTJ URL handling.
If running v2.0, WTTJ URLs will be incorrectly flagged as "generic" — apply the
WTTJ pattern patch before running (see check_urls_patch.md).

---

*Part of the 12-Week AI Automation Curriculum | Joey Clark | 2026*
*Boards: Greenhouse · Lever · Ashby · Workday · WTTJ*
