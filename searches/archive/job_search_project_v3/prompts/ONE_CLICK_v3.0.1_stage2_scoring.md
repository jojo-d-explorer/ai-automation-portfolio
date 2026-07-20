# ONE_CLICK_v3.0.1_stage2_scoring.md — Verification + Scoring

**User:** Joey Clark
**Resume:** `resume/Joey_Clark_Resume_4-25_FINAL.pdf`
**Schema version:** v3.0.1 (locked 2026-05-11)
**Replaces:** v3.0 Stage 2
**Prerequisite:** Stage 1 v3.0 has run for `CURRENT_WEEK` and produced
`candidates_CURRENT_WEEK.csv`.

---

## What changed from v3.0

v3.0's first run produced 42/42 rows scored from snippets — the JD-fetch
step was effectively skipped, not blocked. Direct curl of all four ATS
boards (Greenhouse, Lever, Ashby, WTTJ) returns HTTP 200 with full JD
content, so the issue was prompt ambiguity rather than network failure.

v3.0.1 makes three specific edits to prevent silent fallback:

1. **Step 2 names the tool call explicitly.** "Fetch the JD body" is
   replaced with "call `web_fetch(URL)`" so the runtime can't interpret
   the step as optional.
2. **Step 3 narrows the fallback trigger.** Snippet-scoring is now only
   permitted on documented fetch failures (4xx/5xx/timeout/empty body),
   not on "I didn't try."
3. **New Step 3.5 adds a sanity check.** If fewer than 80% of rows have
   `jd_fetch = success`, the pipeline halts with a clear error before
   scoring. That catches a silent-fallback run as the failure it is.

No other architectural changes. Scoring rubric, tiers, output schema
unchanged from v3.0.

---

## CONTEXT CALCULATION

Calculate today's date.
Determine `CURRENT_WEEK`: most recent Monday (ISO format YYYY-MM-DD).
Determine `PREVIOUS_WEEK`: the Monday before that.

---

## EXECUTION SEQUENCE

### STEP 0 — Verify prerequisites

Check that `results/joey/Week_of_CURRENT_WEEK/candidates_CURRENT_WEEK.csv`
exists. If missing, halt and prompt to run Stage 1.

If `api_verified_CURRENT_WEEK.csv` exists (from optional separate ATS API
checker run), union it with candidates.csv, deduping by `(slug, job_id)`.
Source becomes `"API + Google"` for rows in both files.

### STEP 1 — Apply Stage 1 structural pre-filters

Before any JD fetching or scoring effort:

- Drop rows where `stretch_count` is 2+
- Drop rows where `intl_flex_ok` is `false`
- Drop rows where `seniority_floor_ok` is `false`

Log the drops to `pre_filter_drops_CURRENT_WEEK.csv` for visibility (Joey
may want to audit whether the filters are calibrated too tight).

**Everything that survives gets scored.** The Stage 1 funnel did the
structural work; Stage 2 does fit assessment.

### STEP 2 — Fetch JDs for the survivor set

**The JD fetch is the primary, non-optional path.** Snippet scoring is the
documented fallback for individual rows that fail to fetch — not a global
default. Skipping this step entirely is a pipeline error, not graceful
degradation. See Step 3.5 for the sanity check that enforces this.

**For each surviving row, execute a JD fetch:**

```
result = web_fetch(row.URL)
```

(Or if running under Cowork / a browser-based agent: open the URL,
wait for body content to render, extract page text. Whatever the actual
fetch primitive is in the runtime, call it explicitly per row. Do not
substitute "use the snippet" because reading the URL feels expensive.)

**Parse the response body for:**
- Job location (full string, including remote-modifier language)
- Reporting line (to whom)
- Team size signals (first-hire, lead-team-of-N, IC)
- Remote-mode language
- Salary band if listed
- Builder vs Manager signals

**Set `jd_fetch` per row based on the fetch outcome:**
- HTTP 200 with non-empty body containing recognizable JD keywords
  (responsibilities / qualifications / requirements / about the role):
  `jd_fetch = success`
- HTTP 404: `jd_fetch = closed_listing` — log to closed_listings CSV,
  do not score
- HTTP 4xx (not 404) or 5xx: `jd_fetch = http_error`
- Timeout (>20s): `jd_fetch = timeout`
- Empty body or body < 1KB: `jd_fetch = empty`
- JS-shell only (no JD keywords in returned HTML): `jd_fetch = js_shell`

All non-success, non-404 outcomes route to the per-row fallback in Step 3.
The 80%+ success-rate threshold in Step 3.5 catches systemic failure.

### STEP 3 — Per-row fallback for individual fetch failures

This rule applies **only to individual rows where `jd_fetch` is in
{http_error, timeout, empty, js_shell}**. It is not a global default.

For those rows:
- Score from snippet + Stage 1 metadata
- Set `score_source = snippet`
- Prefix the rationale with `[snippet-only, verify before applying]`
- Continue to the next row

For rows where `jd_fetch = success`:
- Score from JD content
- Set `score_source = jd`
- No prefix tag in the rationale

If a Master CSV has 100% `score_source = snippet`, the pipeline did not
actually run as designed — Step 3.5 should have halted it.

### STEP 3.5 — Sanity check on JD fetch success rate

After Step 2 completes for all rows, count:

```
total_rows = count of rows after Step 1 pre-filters
success_rows = count of rows with jd_fetch = success
success_rate = success_rows / total_rows
```

**If `success_rate < 0.80`, HALT with the following message:**

```
STAGE 2 HALTED — JD fetch success rate below threshold.

Of N rows that survived pre-filters, only M had successful JD fetches.
Success rate: X% (threshold: 80%).

This usually means one of:
  1. The runtime is not actually calling web_fetch (treating it as
     unavailable when it isn't). Verify the tool is enabled.
  2. ATS-board egress is genuinely blocked at the network layer.
     Test manually: curl one of the URLs from the candidates CSV.
  3. The fetch primitive is being substituted with snippet read.
     Check whether the runtime is following Step 2 literally.

Do not proceed with a snippet-only Master — that's a false output.
Fix the fetch path and re-run from Stage 2.

Per-row jd_fetch breakdown:
  success:        M
  http_error:     X
  timeout:        Y
  empty:          Z
  js_shell:       W
  closed_listing: V
```

**Why the threshold is 80% and not 100%:** some closures, transient
5xx errors, and JS-shell pages are normal. A run where 70% of fetches
succeed is operating correctly. A run where 0% succeed is not.

### STEP 4 — JD-based remote re-check

For rows where the JD was successfully fetched, re-evaluate
`intl_flex_ok` and `remote_eligible` against actual JD content. Override
the Stage 1 snippet-based guess if the JD contradicts it.

Auto-drop rows where the JD confirms `intl_flex_ok = false` (e.g., JD
explicitly requires in-person federal-cleared work in DC).

### STEP 5 — Refine role family + archetype from JD

Override Stage 1's snippet-based guesses if JD scope contradicts. Set:
- `role_family` (final)
- `archetype` (builder_leaning | manager_leaning | mixed)

### STEP 6 — Apply the v3.0 scoring rubric

**Three dimensions, 0–3 scale each. Total range: 0–9.**

#### Dimension 1: Role Fit (0–3)

How well does this specific role match Joey's profile?

- **3:** Same role family as Joey's strongest experience, same archetype
  (Builder for early-stage, Manager for established). Direct hit.
- **2:** Same family different archetype; OR adjacent family same
  archetype. Plausible stretch in one direction.
- **1:** Partial relevant skills. Real translation work required to
  position.
- **0:** Weak match. Joey would be a non-obvious candidate.

#### Dimension 2: Company Fit (0–3)

Is this the kind of company Joey wants to be at?

Three sub-considerations: (a) target sector — fintech, defense-tech,
dual-use, AI-ML, govtech, industrials, energy, financial services,
market-entry services; (b) growth stage — seed through Series D, VC/PE
backed; (c) plausibly reaches Lisbon/EU or accommodates Daniel's posting.

- **3:** Strong on all three (target sector + growth stage + plausibly
  reaches Lisbon/EU)
- **2:** Strong on two of three
- **1:** Strong on one of three
- **0:** None

#### Dimension 3: Combination Signal (0–3)

Would the hiring manager specifically want Joey's
JD+MBA+MPP+banking+VC+DoD combination — or is the combination a
liability?

This is the load-bearing dimension for differentiating *Joey could do this
role* from *Joey is the obvious right person for this role*.

- **3:** The combination is the headline. Examples: regulated-industry
  market entry with policy sensitivity (JD+MBA+MPP+DoD compounds); deep
  tech VC platform role (legal+finance+gov); cross-border partnerships at
  a fintech selling into banks (banking+legal+ops).
- **2:** Combination meaningfully helps. The hiring manager sees the JD
  and notices the policy/legal/finance trifecta as a plus.
- **1:** Combination is neutral. Joey has the right skills but the
  combination doesn't differentiate.
- **0:** Combination is a liability — over-credentialed, too senior, or
  signals "won't stay long enough."

**Discipline:** Default to 1 unless a signal clearly applies. The v2.3
rubric over-credited transferable skills; v3.0 reserves 2 and 3 for cases
where the combination is doing real work.

### STEP 7 — Compute total + assign tier

`Total = D1 + D2 + D3` (range 0–9).

**Tiers:**
- **7–9: Top — action this week.** Tailor and apply, or network in if
  Joey identifies a warm route on review.
- **5–6: Borderline — review.** Quick read of the JD, decide whether to
  invest tailoring effort.
- **0–4: Skip.** Logged in the Master but flagged for low effort.

Bottom-tier (0–4) rows still appear in the Master CSV for transparency —
Joey can spot a misclassification — but are visually grouped at the bottom.

### STEP 8 — NEW vs. REPEAT

Compare `(slug, job_id)` against the previous week's Master in either
`Master_v3_0_1_PREVIOUS_WEEK.csv` or `Master_v3_0_PREVIOUS_WEEK.csv`
(checking both lets the comparison work during the v3.0 → v3.0.1
transition). If neither exists, mark all rows `NEW`.

### STEP 9 — Write Master CSV

**Folder:** `results/joey/Week_of_CURRENT_WEEK/`
**File:** `Master_v3_0_1_CURRENT_WEEK.csv`

Columns (13 total):

```
Status | Tier | Total | D1_Role | D2_Company | D3_Combo |
Archetype | Score_Source |
Company | Job_Title | Role_Family |
Location | URL | Rationale_One_Line
```

`Score_Source` is `jd` or `snippet` — tells Joey at a glance whether the
score is high-confidence or needs verification.

`Rationale_One_Line` is exactly that — one sentence. Examples:

- "Direct CoS fit at seed-stage fintech; hiring manager will see the
  banking+legal combination as a plus."
- "Adjacent Strategy-Ops role at later-stage defense; combination
  neutral; worth tailoring if Tekever doesn't move first."
- "[snippet-only, verify before applying] Country Manager Brazil at LATAM
  fintech; combination strong on regulated cross-border."

**Sort:** Tier (Top → Borderline → Skip), then Total desc within tier.

### STEP 10 — Final summary (display in chat)

```
STAGE 2 v3.0 COMPLETE — Week of CURRENT_WEEK

Input pipeline:
  Stage 1 candidates:     X
  After pre-filter drops: X (Y dropped at structural filters)

JD fetches:
  Success:        X (scored from JD)
  Snippet-only:   X (scored from snippet, flagged for verify)
  Closed (404):   X (logged separately)
  JD-fetch success rate: X% (must be ≥80% for run to proceed)

Tier distribution:
  Top (7–9):       X    (Y NEW, Z REPEAT)
  Borderline (5–6): X    (Y NEW, Z REPEAT)
  Skip (0–4):      X

Role family breakdown (Top + Borderline):
  Chief of Staff:      X
  Partnerships/BD:     X
  Market Entry:        X
  Strategy & Ops:      X
  Other:               X

Top 5 by total:
  [list with Company - Title - Tier/Total - Score Source]

Files saved:
  Master:       results/joey/Week_of_CURRENT_WEEK/Master_v3_0_1_CURRENT_WEEK.csv
  Pre-filter:   results/joey/Week_of_CURRENT_WEEK/pre_filter_drops_CURRENT_WEEK.csv
  Failed JD:    results/joey/Week_of_CURRENT_WEEK/failed_fetches_CURRENT_WEEK.csv (if any)
  Closed:       results/joey/Week_of_CURRENT_WEEK/closed_listings_CURRENT_WEEK.csv (if any)

NEXT STEP:
  Review the Master. The Top tier is the decision-ready list.
  The Borderline tier is the watch list. Run check_urls.py against the
  Master one last time before applying to catch any closures since the
  fetch.
```

---

## NOTES FOR THIS PROMPT

- **Score from JDs when possible, snippets when not.** Either is better
  than the pipeline halting.
- **Tighten D3, not D1.** The Combination Signal dimension is where the
  v2.3 rubric leaked credit. v3.0 defaults to 1 and reserves 2–3 for
  signals doing real work.
- **One-line rationales.** Anything longer doesn't get read.

---

*v3.0.1 Stage 2. Patch on v3.0: explicit JD-fetch tool call, narrower
fallback trigger, sanity-check halt at 80% success threshold.*
