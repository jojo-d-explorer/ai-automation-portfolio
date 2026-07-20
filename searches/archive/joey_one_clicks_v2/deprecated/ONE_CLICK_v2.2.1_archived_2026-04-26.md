# ONE_CLICK_v2.md — Unified Job Search (v2.2.1)

**User:** Joey Clark
**Resume:** `/Users/jc3/GitHub/ai-automation-portfolio/job_search_project/resume/Joey_Clark_Resume_4-25_FINAL.pdf` (attach when running)
**Schema version:** v2.2 (locked Apr 23, 2026); prompt patched 2026-04-25 (v2.2.1)
**Spec reference:** `JOB_SEARCH_TOOL_SPEC_v2.md`

**v2.2.1 patches (2026-04-25):**
- Removed `Top10_NEW` output file. The check_urls validation step (post-processing) replaces that workflow — stale jobs filtered out, focus on top of Master CSV.
- Added explicit discovery thoroughness requirements to Step 2 to prevent shallow first-run behavior. Discovery must attempt all board × role-family combinations and gracefully handle JD fetch failures rather than silently dropping roles.
- Strengthened NEXT STEP language: check_urls is the GATING step before review, not a validation afterthought.

---

## CONTEXT CALCULATION

Calculate today's date.
Determine `CURRENT_WEEK`: most recent Monday (ISO format YYYY-MM-DD).
Determine `PREVIOUS_WEEK`: Monday before that.

---

## EXECUTION SEQUENCE

This run produces a single unified weekly output by combining:
1. **API-direct results** (run by `ats_api_checker_v2.py` separately, output at `job_search_project/job_search_project/results/joey/Week_of_CURRENT_WEEK/api_verified_CURRENT_WEEK.csv`)
2. **Google-indexed results** (this prompt searches Google for roles at companies NOT yet in the corpus)

Both feed into the same scoring rubric (Section 3) and the same final master CSV.

### STEP 1 — Verify API-direct output exists

Check for: `job_search_project/job_search_project/results/joey/Week_of_CURRENT_WEEK/api_verified_CURRENT_WEEK.csv`

If missing, prompt the user to run: `python3 ats_api_checker_v2.py`
If present, load it; these rows enter the pipeline already enriched with corpus metadata + eligibility flags. They still need to be SCORED by this prompt (Section 3).

### STEP 2 — Google-indexed discovery (find roles at NEW companies)

Search the following ATS domains for roles posted in the last 7 days:
- `site:boards.greenhouse.io`
- `site:jobs.lever.co`
- `site:jobs.ashbyhq.com`
- `site:myworkdayjobs.com`
- `site:app.welcometothejungle.com`

For each board, run two passes:

**Pass A — Role-family searches** (focus on discovery of new companies):
- "chief of staff" "remote"
- "head of partnerships" "remote"
- "country manager" OR "country lead" (LATAM, Europe, Portugal)
- "market entry" OR "international expansion"
- "head of strategic operations" OR "strategic initiatives director"
- "founding chief of staff" OR "founding operator"

**Pass B — Geography-anchored searches** (catch location-specific opportunities):
- "remote" + LATAM/Brazil/Mexico/Argentina + (chief of staff OR partnerships OR strategic ops)
- "remote" + Portugal/Lisbon/EMEA + (chief of staff OR partnerships OR strategic ops)
- DC + (chief of staff OR partnerships) at growth-stage companies

**Discovery thoroughness requirements (do not skip — first run was too shallow):**

- For each board × role-family combination, pull at least the top 10 Google results before moving on.
- Do not stop discovery after the first 5 promising results. Run all 5 boards × 6 Pass-A queries = 30 search combinations minimum, plus all Pass-B searches.
- For every URL that passes the seniority gate by title alone (Step 3), attempt to fetch the full JD.
- If a JD fetch fails (403 error, JS-rendered shell, empty body), do NOT silently drop the role. Either: (a) score it from the search snippet with `score_confidence: low` flagged in Score_Rationale, or (b) note it in `companies_to_add_*.txt` for manual review next session.
- Do not write outputs until all search combinations have been attempted. Track progress and surface "X of Y combinations attempted" in the summary so thoroughness is verifiable.

**Anti-hallucination:** Only include results from actual search. If a search returns 0, record 0.

**URL integrity (mandatory):** Reject any result without a job-specific URL containing a unique job ID. Acceptable patterns:
- `boards.greenhouse.io/[company]/jobs/[id]`
- `jobs.lever.co/[company]/[uuid]`
- `jobs.ashbyhq.com/[company]/[uuid]`
- `myworkdayjobs.com/.../[id]`
- `app.welcometothejungle.com/jobs/[id]`

Reject board roots, generic careers pages, and guessed IDs.

### STEP 3 — Apply the seniority gate to ALL results

**Hard reject** (auto-reject before scoring):
- Associate, Coordinator, Specialist, Analyst, Intern, Assistant, Junior, Entry-level
- Exception: "Senior [X]" titles where JD describes Director-equivalent scope

**Soft floor** (passes to scoring):
- Manager, Senior Manager, Principal, Lead, Senior IC, Founding [X]
- Operator-in-Residence, Entrepreneur-in-Residence, Operating Partner, Venture Partner
- Director, VP, Head of, Chief, SVP

### STEP 4 — Apply the three-scenario eligibility flags to ALL results

For every result, evaluate three booleans against the JD location text:

**`eligible_latam_mode` = true** if any:
- Remote-Global, Remote-Worldwide, Work-from-anywhere, Fully remote
- Remote-US (DC residency-of-record acceptable)
- Remote-LATAM, Remote-Americas, Remote-Latin-America
- Located in Buenos Aires, Panama City, or Bogotá
- LATAM-based with remote flexibility

**`eligible_dc_mode` = true** if any:
- Remote-Global, Remote-Worldwide, Work-from-anywhere
- Remote-US, US-based remote
- DC-based (in-office, hybrid, or remote-DC)
- Global/international role explicitly permitting DC base

**`eligible_portugal_mode` = true** if any:
- Remote-Global, Remote-Worldwide, Work-from-anywhere
- Remote-EU, Remote-EMEA, Remote-Europe
- Portuguese or EU-based with visa sponsorship
- Located in Lisbon or Porto
- Remote-US **explicitly permits** working from Portugal/elsewhere

**`unclear`** when JD says "remote" without geographic specification, or signals conflict.

**`eligibility_summary`** is the compact letter code (e.g., `"L, D, P"` for all three; `"P only"` for Portugal-only; `"L?, D"` for LATAM-unclear plus DC-eligible).

If all three flags are `false` → auto-reject.

### STEP 5 — Tag role family

For each remaining result, tag `role_family` with one of:
- `chief_of_staff` | `partnerships_bd` | `strategic_ops` | `market_entry` | `govt_defense` | `growth_commercial` | `program`

If no family clearly matches, set `role_family = "other"` and continue.

### STEP 6 — Apply the v2.2 scoring rubric (100 + 3 bonus points)

For each result, score using the attached resume.

#### Dimension 1: Skills & Experience Match — 45 points (split into 1a + 1b)

**1a. Direct Experience Match — 25 points**
- 22–25: Direct match — same role family at same archetype (VC-backed growth-stage, financial services, government-adjacent)
- 16–21: Strong match — same family, different archetype; or adjacent family at same archetype
- 8–15: Partial match — relevant skills, meaningful step from past
- <8: Weak match

**1b. Combination Fit — 20 points** (use signal library)

Signals (one or more apply):
1. Regulatory/policy sensitivity in commercial role (JD + MPP rare)
2. Cross-sector translation as core ask (corp VC at industrials, BD selling to gov/regulated, etc.)
3. Dual-geographic fluency as core ask (US-EU, US-LATAM market entry/structuring)
4. Deal structuring + operator hybrid (M&A + operator)
5. Institutional credibility + startup speed (selling into banks/gov/insurers)
6. Legal operator hybrid (JD load-bearing, role operational)

Discipline: ask "would the hiring manager specifically want Joey's combination?" — not "does Joey have transferable skills?"

- 17–20: Two+ signals clearly apply, or one signal at high intensity
- 11–16: One signal moderately applies
- 5–10: Combination doesn't help or hurt
- 0–4: Combination irrelevant or liability

**Total Dimension 1 = 1a + 1b** (max 45)

#### Dimension 2: Company & Industry Fit — 25 points

For corpus companies: use `company_sector`, `company_stage`, `company_priority_tier` from API output.
For new companies (Google-indexed): infer from JD/company website. Flag the company for corpus addition.

- 21–25: Growth-stage (seed, Series A–D), in target sector (fintech, defense-tech, dual-use, AI-ML, govtech, industrials, energy, financial-services, market-entry-services), VC/PE-backed
- 15–20: Adjacent industries; or target sector with stage mismatch
- 9–14: Weaker industry fit (large enterprise, mature, slow-moving) OR pre-seed stage
- <9: Poor fit (crypto retail, healthcare admin, nonprofit, lifestyle)

#### Dimension 3 (removed in v2.2)

Location is a gate (Step 4), not scored.

#### Dimension 4: Growth & Role Context — 20 points

Considers: role scope at this company (first-in-role > narrow IC), company growth moment (recent funding, expansion, acquisition), reporting relationship (CEO/Founder direct > 3 layers), JD scope signals (P&L, hiring authority, cross-functional mandate, board exposure).

- 17–20: High-scope role at company in clear growth moment, direct exec reporting, function-defining
- 12–16: Solid scope, growth signals present, real mandate
- 6–11: Narrower scope or less clear growth context
- <6: Maintenance/execution within established function

#### Dimension 5: Role Archetype Signal — 10 points

Information-forward. Tag `Role_Archetype` as `Builder-leaning`, `Manager-leaning`, or `Mixed`.

**Builder signals:** "first [role] hire", "first in role", "0-to-1", "establish the function", "stand up", "design the playbook", "report directly to CEO" + early-stage, "no existing team", "build the team", "architect", "operationalize"

**Manager signals:** "manage existing", "own established", "lead a team of [N]" with N substantial, "inherit", "take over", "step into", "continue to drive/scale", reports to VP+ with multiple layers above

**Mixed:** ambiguous JD, generic language, or senior title at early-stage without explicit builder language

Use corpus stage as tiebreaker: Series A/B → builder default; Series D+/public → manager default.

- 8–10: Clear signal (strongly one or the other)
- 4–7: Mixed or genuinely ambiguous
- 0–3: JD too thin to read

#### Bonus: Builder Bonus — up to +3

Fires when **both**:
1. Strong builder signals in JD
2. Corpus stage is `seed`, `series-a`, or `series-b`

### STEP 7 — Compute total score and apply cutoffs

`Total = D1 + D2 + D4 + D5 + Builder_Bonus` (range 0 to 103)

- **Score ≥ 70** → main output
- **Score 65–69** → "On the Bubble" section. Populate `Gap_Factor` with the single dimension that kept it from 70 (e.g., `Growth & Role Context (8/20) — narrow IC scope, otherwise strong fit`)
- **Score < 65** → exclude

### STEP 8 — Deduplicate

If same `Company + Job_Title` appears in both API-direct and Google-indexed results, keep one record. Note both sources in `Found_On` (e.g., `"API (Ashby), Google (Greenhouse)"`).

### STEP 9 — NEW vs. REPEAT

Compare against: `job_search_project/results/joey/Week_of_PREVIOUS_WEEK/Master_v2_PREVIOUS_WEEK.csv`

If the file exists: mark roles not in previous as `NEW`, others as `REPEAT`.
If missing (first run under v2.2): mark all as `NEW`.

### STEP 10 — Write outputs

**Folder:** `job_search_project/results/joey/Week_of_CURRENT_WEEK/` (create if needed)

**File 1 — Master CSV:** `Master_v2_CURRENT_WEEK.csv`

Columns (in order):
```
Status | Score | Score_Rationale | Gap_Factor | Role_Archetype |
Eligibility_Summary | Eligible_LATAM | Eligible_DC | Eligible_Portugal |
Company | Job_Title | Role_Family |
Company_Sector | Company_Stage | Company_HQ | Priority_Tier |
US_Investor_Signal | US_Investors | Lusophone_Exposure | LATAM_Exposure |
Location | Work_Arrangement | Salary_USD | Job_Summary | URL | Found_On
```

Sort by Score descending. Roles 65–69 appear in a separate section labeled "ON THE BUBBLE" within the same file.

**File 2 — Companies-To-Add log:** `companies_to_add_CURRENT_WEEK.txt` — list any company surfaced in Google-indexed results that is NOT in `companies.json`. Format: `slug | name | ats_detected | url_pattern | sector_inferred`

### STEP 11 — Final summary (display in chat)

```
WEEKLY SEARCH COMPLETE — Week of CURRENT_WEEK

Total roles scored: X
  Score 70+:        X (Y NEW, Z REPEAT)
  Score 65-69:      X (bubble band)
  Rejected seniority: X
  Rejected eligibility (failed all 3 scenarios): X

By Eligibility Summary (top tier only):
  L, D, P (universal):  X
  L, D:                 X
  D, P:                 X
  L only:               X
  D only:               X
  P only:               X

By Role Family:
  Chief of Staff:       X
  Partnerships/BD:      X
  Strategic Ops:        X
  Market Entry:         X
  ...

By US Investor Signal (top tier only):
  High:                 X (warm network paths)
  Medium:               X
  Low:                  X
  None/needs_verify:    X

Builder Bonus triggered: X roles

Top 5 by score:
  [list with Company - Title - Score - Eligibility]

New companies for corpus addition: X (see companies_to_add_CURRENT_WEEK.txt)

Files saved:
  Master:  job_search_project/results/joey/Week_of_CURRENT_WEEK/Master_v2_CURRENT_WEEK.csv
  Add log: job_search_project/results/joey/Week_of_CURRENT_WEEK/companies_to_add_CURRENT_WEEK.txt

NEXT STEP REQUIRED: Run check_urls.py against the Master CSV. This removes stale
listings and is the GATING STEP before reviewing results — the Master CSV should
not be acted on before validation. Stale listings inflate apparent supply and
waste review time.
```

---

## NOTES FOR THIS PROMPT

- **Copyright:** When summarizing JDs, use original wording. Never quote 15+ words from any single JD.
- **No hallucination:** If a search returns nothing, record 0. Never invent listings.
- **Conservative on eligibility "true":** When in doubt between `true` and `unclear`, choose `unclear`. Better to surface for human review than auto-include something that doesn't actually qualify.
- **Conservative on Combination Fit scoring:** Default to the "doesn't help or hurt" band (5–10) unless a signal clearly applies. Don't over-credit transferable skills as combination fit.
- **Score Rationale must be specific:** Reference the dimension and the specific JD language or corpus signal that drove the score. "Strong fit" is not a rationale.

---

*v2.2.1 unified one-click. Replaces ONE_CLICK_WEEKLY_SEARCH.md and ONE_CLICK_Joey_RemoteGlobal.md.*
