# ONE_CLICK_v3.0_stage1_discovery.md — Discovery (no scoring)

**User:** Joey Clark
**Resume:** `resume/Joey_Clark_Resume_4-25_FINAL.pdf`
**Schema version:** v3.0 (locked 2026-05-11)
**Replaces:** v2.3.1 Stage 1

---

## What changed from v2.3.1

v3.0 is a deliberate strip-down. The previous pipeline accumulated regret-driven
complexity — every miss added a rule, nothing got removed. The result was a
108-query exhaustive search feeding a corpus-maintenance system that did
database work for a future state that may not arrive.

v3.0 prioritizes **decision support over data purity**. The goal is 30–50
candidates per week, decision-ready, with structural filters applied up front
so scoring effort lands on roles Joey could actually take.

**Stripped:**
- 9 role families compressed to 4 (rolled up overlaps; dropped corp dev and
  govt-defense-as-family — the latter is now a target-company filter)
- 6 ATS boards reduced to 3 + 1 Europe-specific (Workday and SmartRecruiters
  removed — Workday skewed enterprise = stretch-dimension liability;
  SmartRecruiters was low-yield at Joey's level)
- Corpus auto-grow, enrichment writeback, disqualifier audit logs — removed.
  Replaced with a thin `seen_companies.txt` dedup file.
- MODE flag — removed. The geographic anchors run as separate queries now,
  not as a toggle.
- The single bundled geo-OR-string Anchor B (8 geographies in one query
  Google couldn't rank well) — replaced with three discrete anchors.

**Added:**
- Three structural pre-filters populated at the candidate-row level
  (`stretch_count`, `intl_flex_ok`, `seniority_floor_ok`)
- Three discrete geographic anchors (EU, LATAM, DC/Defense) replacing the
  bundled disjunction
- A separate named-target sweep for priority companies
- Earlier deduplication — by (slug, job_id) before the title gate, so the
  10-per-query Google rule yields 10 *unique* candidates

---

## CONTEXT CALCULATION

Calculate today's date.
Determine `CURRENT_WEEK`: most recent Monday (ISO format YYYY-MM-DD).

---

## EXECUTION SEQUENCE

### STEP 1 — Run role-family queries

**Query budget at default:** 4 boards × 4 role families × 4 anchors = **64
queries**. Down from 108 in v2.3.1.

**Boards:**
1. `site:boards.greenhouse.io` (and `site:job-boards.greenhouse.io`)
2. `site:jobs.lever.co`
3. `site:jobs.ashbyhq.com`
4. `site:app.welcometothejungle.com` — Europe-only; this board's results are
   weighted to EU/EMEA listings, so it serves Joey's international chapter

**Role families** (4 total):
1. **`chief_of_staff`** — queries: `"chief of staff" OR "founding chief of staff" OR "founding operator"`
2. **`partnerships_bd`** — queries: `"head of partnerships" OR "VP partnerships" OR "director of strategic partnerships"`
3. **`market_entry`** — queries: `"country manager" OR "country lead" OR "market entry" OR "international expansion" OR "head of expansion"`
4. **`strategy_ops`** — queries: `"head of strategy" OR "strategy and operations" OR "strategic initiatives director" OR "head of strategic operations"`

**Anchors** (4 per family per board):

- **A — open remote:**
  `[role] "remote" 2026`
  Catches Remote-Global / Remote-US listings. Top 10 results.

- **B-EU — Europe-anchored:**
  `[role] "remote" (Europe OR EMEA OR Lisbon OR Portugal OR "Remote-EMEA")`
  Joey's planned international chapter. Top 10 results.

- **B-LATAM — LATAM-anchored:**
  `[role] (Brazil OR Mexico OR "Latin America" OR LATAM OR "Remote-LATAM")`
  Lusophone corridor + Scenius LATAM coverage area. Top 10 results.

- **B-DC — DC/Defense-anchored:**
  `[role] (Washington OR "Washington DC" OR defense OR "dual-use" OR NATO)`
  Joey's current base + DoD background. Note: this is not the same as a
  govt-affairs role family — it's a geographic/sector anchor applied to the
  four existing families. Top 10 results.

**Per-query rules:**
- Pull top 10 results per query
- If a query returns 0, record 0. Never invent listings.
- Track progress: "X of 64 attempted"

### STEP 2 — Named-target sweep (priority companies)

Separate from the role-family queries. Single Google site search per target,
across all four role families implicitly (no role keywords — just the company
name + "careers" or "jobs"):

**Default target list:**
- `tekever.com` (Portuguese defense — explicit Joey priority from memory)
- Scenius LATAM newsletter named companies (highest-signal LATAM source per
  Joey's notes — pull current issue's named companies)
- Any other names Joey adds to `results/joey/named_targets.txt`

For each target, run: `site:[target_domain] OR "[company] careers" 2026`

Output goes into candidates.csv with `Found_On_Board = "named_target"` and
`Search_Anchor = "priority_company"`.

**This is the single biggest lever for Joey's specific situation** — four
generic anchors won't surface Tekever's PM Southern Europe role as reliably
as a direct sweep.

### STEP 3 — Deduplicate before any filtering

This step is new in v3.0 and meaningful.

Take all results from Step 1 + Step 2. Call
`python3 scripts/classify_url.py <url>` for each. Drop `url_type != "job"`.

**Then dedup by `(slug, job_id)` immediately.** Earlier versions deduped after
title-gating and remote-gating, which meant the same Greenhouse posting
returned by 4 different anchors counted as 4 candidates against the recall
budget. v3.0 dedups first, then filters.

### STEP 4 — Title-only seniority gate

On the search-result title alone (no JD fetch):

**Hard reject:** Associate, Coordinator, Specialist, Analyst, Intern,
Assistant, Junior, Entry-level, Engineer I/II.

**Exception:** "Senior [X]" titles where the snippet describes
director-equivalent scope (people management, P&L, function ownership).

**Pass through:** Manager, Senior Manager, Principal, Lead, Founding [X],
Director, VP, Head of, Chief, SVP, GM, Operating Partner, Operator-in-Residence.

This step sets `seniority_floor_ok = true | false`. The whole row stays in
the file either way — Stage 2 can re-evaluate if needed — but `false` rows
will not be scored.

### STEP 5 — Snippet-based remote gate

Single boolean: `remote_eligible = yes | no | unclear`. Same logic as v2.3.1.

- **yes:** snippet contains "remote", "fully remote", "remote-first",
  "Remote-US", "Remote-Global", "Remote-EMEA", "Remote-LATAM", or a
  multi-location list with a Remote variant.
- **no:** unambiguous in-office, locked to an unreachable city.
- **unclear:** everything else.

**Auto-reject `no`.** Both `yes` and `unclear` survive.

### STEP 6 — Apply the three structural pre-filters

For each surviving row, populate three booleans that Stage 2 will use as
gates before scoring effort is invested:

#### 6a. `stretch_count` (integer 0, 1, or 2+)

Count the dimensions where this role asks Joey to stretch:
- **Function:** role family Joey hasn't held before
- **Domain:** sector Joey hasn't worked in
- **Geography:** location Joey isn't currently based in (DC/Lisbon/EU
  remote)
- **Level:** seniority above Joey's last title
- **Comp band:** below $150K base implies a comp stretch downward

Score from title + snippet evidence only. If unclear, default to 0 (Stage 2
will refine from JD).

Rule: **2+ stretches in combination → flag for skip.** Single-stretch is
workable; two-or-more is a structural no by Joey's hiring-filter principle.

#### 6b. `intl_flex_ok` (true | false | unclear)

Could this role accommodate Daniel's potential international posting?

- **true:** Remote-Global, Remote-EMEA, Lisbon/Portugal-based, or
  US-East-Coast-flex with no clear in-person federal/government tether
- **false:** DC-centered government affairs requiring federal-cleared
  in-person work, Bay Area in-office, or nominally-remote-but-actually-
  tethered-to-a-US-office signals
- **unclear:** everything else (Stage 2 reads the JD)

#### 6c. `seniority_floor_ok` — already set in Step 4.

### STEP 7 — Tag role family + archetype

Tag `role_family` to one of the four families above (or `other` if a
named-target hit doesn't fit). Snippet-based archetype guess
(`builder_leaning | manager_leaning | unclear`) — final call happens in
Stage 2.

### STEP 8 — Write candidates.csv

**Folder:** `results/joey/Week_of_CURRENT_WEEK/`
**File:** `candidates_CURRENT_WEEK.csv`

Columns (in order):

```
URL | ATS | Slug | Job_ID |
Company | Job_Title | Role_Family | Archetype_Guess |
Remote_Eligible | Geography_Notes |
Stretch_Count | Intl_Flex_OK | Seniority_Floor_OK |
Search_Anchor | Found_On_Board |
Snippet | Discovered_Date
```

**Sort:** alphabetical by Company.

### STEP 9 — Update seen-companies dedup file

Replaces the v2.3.1 corpus auto-grow + enrichment writeback. Single line per
company:

```
results/joey/seen_companies.txt
```

Append any new company slug encountered this run. No JSON, no metadata, no
backups. The file's only job is letting future runs flag REPEAT vs NEW.

### STEP 10 — Final summary (display in chat)

```
STAGE 1 v3.0 COMPLETE — Week of CURRENT_WEEK

Query coverage:
  Role-family queries:   X of 64 attempted
  Named-target queries:  X attempted
  Raw hits total:        X
  After URL classify:    X (jobs only)
  After dedup:           X (unique slug+job_id)

Filter funnel:
  After seniority gate:        X
  After remote gate:           X
  Flagged 2+ stretches:        X (will skip in Stage 2)
  Flagged intl_flex=false:     X (will skip in Stage 2)
  Final candidates for Stage 2: X

Role family distribution:
  Chief of Staff:           X
  Partnerships/BD:          X
  Market Entry:             X
  Strategy & Ops:           X
  Other (named-target):     X

Anchor distribution:
  Open remote:    X
  EU-anchored:    X
  LATAM-anchored: X
  DC/Defense:     X
  Named target:   X

ATS distribution:
  greenhouse: X | lever: X | ashby: X | wttj: X | other: X

New vs. repeat companies:
  New companies this run:  X
  Repeat companies:        X

Files saved:
  results/joey/Week_of_CURRENT_WEEK/candidates_CURRENT_WEEK.csv
  results/joey/seen_companies.txt (appended)

NEXT STEP:
  Run ONE_CLICK_v3.0_stage2_scoring.md against
  candidates_CURRENT_WEEK.csv. If you also want the API freshness
  verification (faster, more reliable than Google for known companies),
  run ats_api_checker_v2.py separately and Stage 2 will union the results.
```

---

## NOTES FOR THIS PROMPT

- **Recall over precision.** Stage 1 surfaces; Stage 2 filters. Default to
  `unclear` on ambiguous gates and let Stage 2 read the JD.
- **No JD fetching in Stage 1.** Stage 1 stays cheap and reliable even when
  egress is constrained.
- **No scoring in Stage 1.** If you find yourself estimating fit from a
  snippet, that's Stage 2's job.
- **Anti-hallucination:** Only include results from actual searches. If a
  search returns 0, record 0.
- **Copyright:** Paraphrase snippets. Never quote 15+ words from a posting.
- **The named-target sweep is the highest-leverage addition.** If something
  has to be cut for time, cut Anchor A (open remote) before cutting Step 2.

---

*v3.0 Stage 1. Architectural simplification of v2.3.1.*
