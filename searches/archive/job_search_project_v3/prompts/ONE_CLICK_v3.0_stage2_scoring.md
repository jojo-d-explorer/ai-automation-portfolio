# ONE_CLICK_v3.0_stage2_scoring.md — Verification + Scoring

**User:** Joey Clark
**Resume:** `resume/Joey_Clark_Resume_4-25_FINAL.pdf`
**Schema version:** v3.0 (locked 2026-05-11)
**Prerequisite:** Stage 1 v3.0 has run for `CURRENT_WEEK` and produced
`candidates_CURRENT_WEEK.csv`.

---

## What changed from v2.3

v3.0 Stage 2 compresses the scoring rubric from 5 dimensions / 11 sub-bands /
six-signal combination library to **3 dimensions × 0–3 scale each, max 9
points**. Three reasons:

1. The 70-point rubric implied a precision the underlying decisions don't
   need. Joey reads the top 10–15 rows and flags 3–5 for action. A 0–9
   scale fits that workflow.
2. Pre-filters from Stage 1 (`stretch_count`, `intl_flex_ok`,
   `seniority_floor_ok`) now do the gatekeeping that D1's lower bands used
   to do. No need to score roles Joey couldn't structurally take.
3. The Builder Bonus, six-signal Combination Fit library, and below-threshold
   diagnostic log were calibration-team artifacts. Joey isn't a calibration
   team.

**Stripped:**
- Combination Fit signal library (6 named signals)
- Builder Bonus (+3 conditional bump)
- 65–69 below-threshold diagnostic log
- Corpus enrichment writeback to companies.json
- Mandatory JD egress (now graceful degradation — see Step 3)

**Added:**
- Pre-filter enforcement (drops happen before JD fetch)
- Snippet-only scoring as documented fallback, not hard halt
- Tier-based output (Top / Borderline / Skip) instead of point thresholds

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

For each surviving row, fetch the JD body. Parse:
- Job location (full string, including remote-modifier)
- Reporting line (to whom)
- Team size signals (first-hire, lead-team-of-N, IC)
- Remote-mode language
- Salary band if listed
- Builder vs Manager signals

If a JD fetch fails:
- 403 / blocked / JS-shell: mark row `jd_fetch = failed`
- 404: mark row `jd_fetch = closed_listing`, log separately, do not score
- Otherwise: mark row `jd_fetch = success`

### STEP 3 — Graceful degradation rule (NEW in v3.0)

**v2.3 hard-halted if JD egress failed.** v3.0 does not. If JDs can't be
fetched:

- Score from snippet + Stage 1 metadata
- Flag the row with `score_source = snippet` instead of `score_source = jd`
- Add a `[snippet-only, verify before applying]` tag in the rationale
- Continue producing the Master CSV

The point is decision support, not data purity. If snippet-scored rows
make the top tier, Joey will know to verify before tailoring. The pipeline
should never produce zero output because of an egress problem.

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

Compare `(slug, job_id)` against
`results/joey/Week_of_PREVIOUS_WEEK/Master_v3_0_PREVIOUS_WEEK.csv`. If file
exists: mark roles not in previous week as `NEW`. If not (first v3.0 run),
mark all as `NEW`.

### STEP 9 — Write Master CSV

**Folder:** `results/joey/Week_of_CURRENT_WEEK/`
**File:** `Master_v3_0_CURRENT_WEEK.csv`

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
  Master:       results/joey/Week_of_CURRENT_WEEK/Master_v3_0_CURRENT_WEEK.csv
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

*v3.0 Stage 2. Architectural simplification of v2.3 + v2.3.1.*
