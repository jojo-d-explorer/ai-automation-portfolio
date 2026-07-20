# ONE_CLICK_v2.3_stage2_scoring.md — Verification + Scoring

**User:** Joey Clark
**Resume:** `resume/Joey_Clark_Resume_4-25_FINAL.pdf`
  - Interactive runs: attach the PDF via the Cowork UI when prompted.
  - Scheduled runs: read the file directly from the workspace path above.
    The full resume content is required for Dimension 1 scoring.
**Schema version:** v2.3 (locked 2026-04-25)
**Spec reference:** `WORKFLOW_v2.3.md`
**Prerequisite:** Stage 1 has run for `CURRENT_WEEK` and `candidates_CURRENT_WEEK.csv`
exists. The ATS API checker has produced `api_verified_CURRENT_WEEK.csv`.

---

## What this prompt does

Stage 2 of the v2.3 two-stage pipeline. Verification + scoring only — no
discovery. Reads the union of Stage 1 candidates + API-verified rows, fetches
the JD for every row, applies the v2.3 scoring rubric to JD content (not
snippet content), writes the Master CSV.

This prompt **requires JD egress**. If job-board domains are not on the
network allowlist, this prompt halts at the verification step and surfaces
a clear error. Snippet-based scoring is not a fallback in v2.3.

---

## CONTEXT CALCULATION

Calculate today's date.
Determine `CURRENT_WEEK`: most recent Monday (ISO format YYYY-MM-DD).
Determine `PREVIOUS_WEEK`: the Monday before that.

---

## EXECUTION SEQUENCE

### STEP 0 — Verify prerequisites

Check that both files exist:
- `results/joey/Week_of_CURRENT_WEEK/candidates_CURRENT_WEEK.csv` (Stage 1 output)
- `results/joey/Week_of_CURRENT_WEEK/api_verified_CURRENT_WEEK.csv` (ATS API output)

If either is missing, halt and prompt the user to run the missing prerequisite.

Test JD egress with a single fetch against any URL from candidates.csv. If the
fetch returns a network-allowlist error, halt and instruct the user to allowlist
the six ATS domains in Settings → Capabilities → Network. Do not proceed with
snippet scoring.

### STEP 1 — Build the working set

Union the two input files and dedup by `(slug, job_id)`:

- A row appearing in both candidates.csv and api_verified.csv keeps the API
  metadata (sector, stage, investor_signal, location, posting_date) and the
  candidates `Snippet` for context. Source becomes `"API + Google"`.
- A row only in candidates.csv: source `"Google"`.
- A row only in api_verified.csv: source `"API"`.

Drop any row where the URL classifier returns `url_type != "job"`.

### STEP 2 — Fetch the JD for every row

For each working-set URL, fetch the JD body. Parse out:
- **Job location** (full string, including hybrid/in-office/remote-modifier)
- **Reporting line** (CEO / COO / CRO / CAO / VP-X / etc.)
- **Team size signals** (e.g., "lead a team of N", "first hire", "individual
  contributor")
- **Remote-mode language** (e.g., "Remote-US", "Remote-Global, with restrictions",
  "Remote, Portugal-friendly")
- **Builder signals:** "first [role] hire", "first in role", "0-to-1",
  "establish the function", "stand up", "design the playbook", "report directly
  to CEO" + early-stage, "no existing team", "build the team"
- **Manager signals:** "manage existing", "own established", "lead a team of N"
  with N substantial, "inherit", "take over", "step into", "continue to scale"
- **Salary band** if listed
- **Posting date** if listed (cross-check against API freshness)

If a JD fetch fails:
- 403 / blocked: log the row to `failed_fetches_CURRENT_WEEK.csv` and skip
- 404: log to `closed_listings_CURRENT_WEEK.csv` (closed since indexing)
- JS-rendered shell with no useful body: log to `failed_fetches` and skip
- Empty body: log to `failed_fetches` and skip

**Do not score from snippets.** Failed JDs do not land on the Master.

### STEP 3 — JD-based remote check (replaces Stage 1's snippet check)

For each successfully-fetched row, set `remote_eligible_jd: true | false | unclear`
based on the JD's actual location and remote-policy text.

Auto-reject `false`. Keep `true` and `unclear`.

The `geography_notes` column is now JD-quality, not snippet-quality. Capture
specific notes:
- "Remote-US, NY-headquartered, no restriction"
- "Remote-EMEA only, no LATAM"
- "Hybrid Lisbon, 2 days/week"
- "In-office San Francisco, 3 days/week" → remote_eligible_jd=false → reject

### STEP 4 — Tag role family from JD

Refine `role_family_guess` from Stage 1 into final `role_family` using JD scope:
- `chief_of_staff` | `partnerships_bd` | `strategic_ops` | `market_entry`
- `govt_defense` | `growth_commercial` | `program` | `other`

If the JD scope contradicts the guess (e.g., "Head of Partnerships" turns out
to be a frontline channel-sales role), retag accordingly.

### STEP 5 — Apply the v2.3 scoring rubric

The rubric is unchanged from v2.2 — D1 + D2 + D4 + D5 + Builder Bonus.

#### Dimension 1: Skills & Experience Match — 45 points (1a + 1b)

**1a. Direct Experience Match — 25 points**
- 22–25: Direct match — same role family at same archetype (VC-backed
  growth-stage, financial services, government-adjacent)
- 16–21: Strong match — same family, different archetype; or adjacent family
  at same archetype
- 8–15: Partial match — relevant skills, meaningful step from past
- <8: Weak match

**1b. Combination Fit — 20 points** (use signal library)

Signals (one or more apply):
1. Regulatory/policy sensitivity in commercial role (JD + MPP rare)
2. Cross-sector translation as core ask (corp VC at industrials, BD selling to
   gov/regulated, etc.)
3. Dual-geographic fluency as core ask (US-EU, US-LATAM market entry/structuring)
4. Deal structuring + operator hybrid (M&A + operator)
5. Institutional credibility + startup speed (selling into banks/gov/insurers)
6. Legal operator hybrid (JD load-bearing, role operational)

Discipline: ask "would the hiring manager specifically want Joey's combination?"
— not "does Joey have transferable skills?"

- 17–20: Two+ signals clearly apply, or one signal at high intensity
- 11–16: One signal moderately applies
- 5–10: Combination doesn't help or hurt
- 0–4: Combination irrelevant or liability

**Total Dimension 1 = 1a + 1b** (max 45)

#### Dimension 2: Company & Industry Fit — 25 points

For corpus companies (status=active or manual-review): use `sector`, `stage`,
`priority_tier`, `us_investor_signal` from the corpus.
For pending_review stubs and corpus-unknowns: infer from JD/company website.
Stage 2 should also enrich the stub if a confident sector/stage read is
available — write the enrichment back to companies.json at the end of the run.

- 21–25: Growth-stage (seed, Series A–D), in target sector (fintech,
  defense-tech, dual-use, AI-ML, govtech, industrials, energy, financial-services,
  market-entry-services), VC/PE-backed
- 15–20: Adjacent industries; or target sector with stage mismatch
- 9–14: Weaker industry fit (large enterprise, mature, slow-moving) OR pre-seed
- <9: Poor fit (crypto retail, healthcare admin, nonprofit, lifestyle)

#### Dimension 4: Growth & Role Context — 20 points

Considers: role scope at this company (first-in-role > narrow IC), company
growth moment (recent funding, expansion, acquisition), reporting relationship
(CEO/Founder direct > 3 layers), JD scope signals (P&L, hiring authority,
cross-functional mandate, board exposure).

- 17–20: High-scope role at company in clear growth moment, direct exec
  reporting, function-defining
- 12–16: Solid scope, growth signals present, real mandate
- 6–11: Narrower scope or less clear growth context
- <6: Maintenance/execution within established function

#### Dimension 5: Role Archetype Signal — 10 points

Tag `Role_Archetype` as `Builder-leaning`, `Manager-leaning`, or `Mixed`.

Use corpus stage as tiebreaker: Series A/B → builder default; Series D+/public
→ manager default.

- 8–10: Clear signal (strongly one or the other)
- 4–7: Mixed or genuinely ambiguous
- 0–3: JD too thin to read

#### Bonus: Builder Bonus — up to +3

Fires when **both**:
1. Strong builder signals in JD
2. Corpus stage is `seed`, `series-a`, or `series-b`

### STEP 6 — Compute total and apply cutoffs

`Total = D1 + D2 + D4 + D5 + Builder_Bonus` (range 0 to 103)

**Single threshold:** Score ≥ 70 → Master CSV. (No bubble band in v2.3 — the
65–69 band was hedged-snippet scoring artifact, not a meaningful tier.)

Score 60–69 still get logged for diagnostic purposes in
`below_threshold_CURRENT_WEEK.csv` so the rubric's calibration can be
audited week over week.

### STEP 7 — NEW vs. REPEAT

Compare `(slug, job_id)` against
`results/joey/Week_of_PREVIOUS_WEEK/Master_v2_3_PREVIOUS_WEEK.csv`.

If file exists: mark roles not in previous week as `NEW`, others as `REPEAT`.
If missing (first v2.3 run): mark all as `NEW`.

### STEP 8 — Enrich corpus stubs

For any pending_review stub where Stage 2's JD read produced a confident sector
or stage tag, write the enrichment back to `companies.json`:
- `sector`: replace `["unknown"]` with the inferred sector tags
- `stage`: replace `"unknown"` with the inferred stage
- `geography_hq`: if HQ is now confirmed, write it
- `status`: leave at `pending_review` until human review unless the company is
  clearly active and well-known (then promote to `active`)

This is the JD's secondary use: in addition to scoring the role, JD reads also
opportunistically tag the company. Over 4-6 weeks, this turns most pending_review
stubs into fully-tagged corpus entries without dedicated enrichment work.

### STEP 9 — Write Master CSV

**Folder:** `results/joey/Week_of_CURRENT_WEEK/`
**File:** `Master_v2_3_CURRENT_WEEK.csv`

Columns (in order):
```
Status | Score | Score_Rationale | Role_Archetype |
Remote_Eligible_JD | Geography_Notes |
Company | Job_Title | Role_Family |
Company_Sector | Company_Stage | Company_HQ | Priority_Tier |
US_Investor_Signal | US_Investors |
Location | Work_Arrangement | Salary_USD | Job_Summary |
URL | ATS | Slug | Job_ID | Found_On
```

Sort by Score descending. No bubble section, no Top10_NEW (the Master sorted
desc IS the top-N view).

### STEP 10 — Final summary (display in chat)

```
STAGE 2 COMPLETE — Week of CURRENT_WEEK

Working set: X (Stage 1 + API, deduped)
JD fetches: X successful, X failed (logged separately)
After JD remote check: X
Auto-rejected as in-person locked at JD level: X

Master rows (Score 70+): X (Y NEW, Z REPEAT)
Below-threshold log: X (60-69 logged for diagnostics)

By Role Family:
  Chief of Staff:       X
  Partnerships/BD:      X
  Strategic Ops:        X
  Market Entry:         X
  Govt/Defense:         X
  ...

By Source:
  API + Google (both):  X
  API only:             X
  Google only:          X

By US Investor Signal:
  High:                 X
  Needs verification:   X
  Low:                  X

Builder Bonus triggered: X

Top 5 by score:
  [list with Company - Title - Score - Remote_Eligible_JD - Geography_Notes]

Corpus enrichment this run:
  pending_review → active:        X
  pending_review stubs enriched (sector/stage tagged): X

Files saved:
  Master:     results/joey/Week_of_CURRENT_WEEK/Master_v2_3_CURRENT_WEEK.csv
  Below-thr:  results/joey/Week_of_CURRENT_WEEK/below_threshold_CURRENT_WEEK.csv
  Failed JD:  results/joey/Week_of_CURRENT_WEEK/failed_fetches_CURRENT_WEEK.csv
  Closed:     results/joey/Week_of_CURRENT_WEEK/closed_listings_CURRENT_WEEK.csv

NEXT STEP REQUIRED:
  Run check_urls.py against the Master CSV one last time before review. This
  catches anything that closed between the JD fetch and now.
```

---

## NOTES FOR THIS PROMPT

- **JD egress is mandatory.** If you can't fetch JDs, halt — do not produce a
  Master CSV with snippet-based scores. Stage 1's candidates list remains the
  artifact of record until egress is restored.
- **Score from JD content only.** No `[score_confidence: low]` tags exist in
  v2.3. Every Master row was scored against a real JD or it's not a Master row.
- **Stage 2 is also corpus-enrichment.** Every JD read is a chance to upgrade
  a pending_review stub. Don't skip Step 8.
- **Conservative on remote_eligible_jd `true`.** When in doubt between `true`
  and `unclear`, choose `unclear`. The JD has the answer; if it doesn't say,
  surface for human review.
- **Conservative on Combination Fit scoring.** Default to "doesn't help or
  hurt" (5–10) unless a signal clearly applies. Don't over-credit transferable
  skills.
- **Score Rationale must be specific.** Reference the dimension and the
  specific JD language or corpus signal that drove the score.
- **No Top10_NEW.** The Master sorted desc is the top-10 view. Removed in
  v2.2.1 and remains removed.
- **No companies_to_add.txt.** Corpus auto-grows in Stage 1. The text log is
  obsolete.

---

*v2.3 Stage 2. Replaces the scoring-half of ONE_CLICK_v2.md.*
