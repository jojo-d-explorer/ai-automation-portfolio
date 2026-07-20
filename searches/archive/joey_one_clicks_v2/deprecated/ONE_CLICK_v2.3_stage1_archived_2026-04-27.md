# ONE_CLICK_v2.3_stage1_discovery.md — Discovery (no scoring)

**User:** Joey Clark
**Resume:** `resume/Joey_Clark_Resume_4-25_FINAL.pdf`
  - Interactive runs: attach the PDF via the Cowork UI when prompted.
  - Scheduled runs: read the file directly from the workspace path above
    (no UI attachment needed — the resume content is used by Stage 2 scoring,
    not Stage 1 discovery, but Stage 1 still references it for context).
**Schema version:** v2.3 (locked 2026-04-25)
**Spec reference:** `WORKFLOW_v2.3.md`

---

## What this prompt does

Stage 1 of the v2.3 two-stage pipeline. Discovery only — finds candidate roles
from Google ATS-board searches, classifies each by URL, applies a single remote
gate, and writes:

1. `candidates_CURRENT_WEEK.csv` — every job that survived the title+remote gate.
2. **Auto-appended corpus stubs** — any previously-unseen company slug is added
   to `companies.json` via `scripts/corpus_append.py`.

This prompt **does not score**. Scoring happens in Stage 2 against the JD itself,
not against a search snippet. If JD egress is unavailable, Stage 1 still ships;
Stage 2 waits.

This prompt **does not produce a Master CSV**. It produces the input to scoring.

---

## CONTEXT CALCULATION

Calculate today's date.
Determine `CURRENT_WEEK`: most recent Monday (ISO format YYYY-MM-DD).

---

## EXECUTION SEQUENCE

### STEP 1 — Run all queries

The query budget is **6 boards × 7 role families × 2 anchor variants = 84 Google
searches**.

**Boards:**
1. `site:boards.greenhouse.io` (and `site:job-boards.greenhouse.io`)
2. `site:jobs.lever.co`
3. `site:jobs.ashbyhq.com`
4. `site:myworkdayjobs.com`
5. `site:app.welcometothejungle.com`
6. `site:jobs.smartrecruiters.com`

**Role families** (one search per family per board per anchor):
1. `"chief of staff"`
2. `"head of partnerships"`
3. `"country manager" OR "country lead"`
4. `"market entry" OR "international expansion"`
5. `"head of strategic operations" OR "strategic initiatives director"`
6. `"founding chief of staff" OR "founding operator"`
7. `"government affairs" OR "defense partnerships"` — Joey's DoD background

**Anchor variants** — each query is run twice with different geographic anchors,
because per-query precision is the dominant lever for actionable yield:

- **Anchor A — open remote:** `[role] "remote" 2026`
  Catches roles labeled Remote-Global / Remote-Worldwide / Remote-US that don't
  reference a specific country.
- **Anchor B — geo-specific remote:** `[role] "remote" (Lisbon OR Portugal OR
  Europe OR LATAM OR "Latin America" OR Brazil OR Mexico OR DC OR "Washington")
  2026`
  Catches roles where the listing is anchored on geography that matches one of
  Joey's three bases.

**Discovery thoroughness requirements (do not skip — same constraint as v2.2.1):**

- Pull at least the top 10 Google results per query.
- Run all 84 anchored search combinations before any output is written.
- Track progress and surface "X of 84 attempted" in the summary so thoroughness
  is verifiable.
- If a search returns 0, record 0. Never invent listings.

### STEP 2 — Classify every URL

For each result URL, call `python3 scripts/classify_url.py <url>` (or import the
function from a Python session). Returns `{ats, slug, job_id, url_type}`.

- If `url_type == "unrecognized"`: drop from candidates list (board-root, news
  article, aggregator, etc.).
- If `url_type == "generic"`: drop from candidates list — these are board roots
  or company landing pages with no specific job ID.
- If `url_type == "job"`: keep for further filtering.

**URL integrity (mandatory, same as v2.2):** the classifier enforces that every
kept URL has a job-specific ID. Do not pass through a URL the classifier rejects.

### STEP 3 — Title-only seniority gate

Apply on the search-result title alone (no JD fetch yet):

**Hard reject** (drop from candidates):
- Associate, Coordinator, Specialist, Analyst, Intern, Assistant, Junior, Entry-level
- Engineer I, Engineer II (IC engineer track)
- Exception: "Senior [X]" titles where the search snippet describes
  Director-equivalent scope.

**Pass through** (keep):
- Manager, Senior Manager, Principal, Lead, Senior IC, Founding [X]
- Operator-in-Residence, Entrepreneur-in-Residence, Operating Partner, Venture Partner
- Director, VP, Head of, Chief, SVP, GM

### STEP 4 — Single remote gate (v2.3 simplification)

Replaces the v2.2 three-mode eligibility framework. One boolean per role:

`remote_eligible: yes | no | unclear`

Set based on the search-result snippet (title + first 1-2 sentences):

- **yes** if the snippet contains any of: "remote", "fully remote",
  "remote-first", "work from anywhere", "Remote-US", "Remote-Global",
  "Remote-EMEA", "Remote-LATAM", a city explicitly tagged "Remote", or
  a multi-location list including a Remote variant.
- **no** if the snippet is unambiguously in-office and locked to a city
  Joey can't reach (e.g., "On-site Bangalore", "In-office San Francisco
  3 days a week", "Hybrid Tel Aviv").
- **unclear** for everything else, including snippets that just say "hybrid"
  without a city, or mention a city but don't specify on-site/remote.

**Auto-reject `no` only.** Both `yes` and `unclear` survive to candidates.csv.
Free-text geography hints (e.g., "Remote-US, NY-headquartered") go in a
`geography_notes` column, not as gating booleans.

This is a deliberate widening of the funnel relative to v2.2. The price is
that some `unclear` rows will fail Stage 2's JD-based remote check; the gain
is no in-mode roles get hedged out of candidates over a snippet ambiguity.

### STEP 5 — Tag role family by title keyword

For each surviving row, tag `role_family_guess` with one of:
- `chief_of_staff` | `partnerships_bd` | `strategic_ops` | `market_entry`
- `govt_defense` | `growth_commercial` | `program` | `other`

This is a guess, refined in Stage 2. Default to the matching search-family.

### STEP 6 — Write candidates.csv

**Folder:** `results/joey/Week_of_CURRENT_WEEK/` (create if needed)
**File:** `candidates_CURRENT_WEEK.csv`

Columns (in order):
```
URL | ATS | Slug | Job_ID |
Company | Job_Title | Role_Family_Guess |
Remote_Eligible | Geography_Notes |
Search_Anchor | Found_On_Board |
Snippet | Discovered_Date
```

**Sort:** alphabetical by Company, then by Role_Family_Guess. (No score, no
desc-sort. The list is meant to be read top-to-bottom or filtered by family.)

### STEP 7 — Auto-grow the corpus

Run:

```bash
python3 scripts/corpus_append.py \
  --candidates results/joey/Week_of_CURRENT_WEEK/candidates_CURRENT_WEEK.csv
```

This:
- Classifies every URL in the candidates file
- Dedups against `companies.json` by lowercased slug
- Appends stub entries for previously-unseen companies with
  `status: "pending_review"` and `source: "auto_discovery_v2.3"`
- Writes a timestamped backup of `companies.json` before modifying it
- Updates the `_meta` block with new totals + ATS breakdown

**First-run note:** expect 20-40 stubs added on the first v2.3 run as previously
hand-tracked companies (and net-new ones) get formally registered.

### STEP 8 — Final summary (display in chat)

```
STAGE 1 COMPLETE — Week of CURRENT_WEEK

Search coverage: X of 84 board × role-family × anchor combinations attempted
Total raw search hits: X
Classified as job posts: X (out of X URLs)
Skipped — board roots/generics: X
Skipped — unrecognized hosts: X

After title seniority gate: X
After remote gate (yes + unclear): X
Auto-rejected as in-person locked: X

Final candidates: X

Role family distribution:
  Chief of Staff:       X
  Partnerships/BD:      X
  Strategic Ops:        X
  Market Entry:         X
  Govt/Defense:         X
  Growth/Commercial:    X
  Program:              X
  Other:                X

Remote eligibility distribution:
  yes:                  X
  unclear:              X

ATS distribution:
  greenhouse: X | lever: X | ashby: X | workday: X | wttj: X | smartrecruiters: X

Corpus growth this run:
  Companies in corpus before: X
  Auto-stubs added:           X
  Companies in corpus after:  X
  (X of the new stubs are sectorally pre-tagged via title heuristics; the rest
   sit at status=pending_review for later enrichment.)

Files saved:
  results/joey/Week_of_CURRENT_WEEK/candidates_CURRENT_WEEK.csv
  companies.json (updated in place; backup at companies.json.bak.YYYY-MM-DD.json)

NEXT STEP REQUIRED:
  (a) Run ats_api_checker_v2.py against the now-updated corpus to harvest
      freshness-verified rows. Output: api_verified_CURRENT_WEEK.csv.
  (b) Then run ONE_CLICK_v2.3_stage2_scoring.md against the union of
      candidates_CURRENT_WEEK.csv + api_verified_CURRENT_WEEK.csv.
```

---

## NOTES FOR THIS PROMPT

- **No JD fetching in Stage 1.** Stage 1 is intentionally cheap and reliable.
  Even if egress to job boards is blocked, Stage 1 still ships a useful
  candidates list and grows the corpus.
- **No scoring in Stage 1.** Snippet scoring is the failure mode v2.3 was
  designed to fix. If you find yourself estimating scores from snippets, stop
  and move that work to Stage 2.
- **Recall over precision.** Stage 1's job is to surface candidates. Stage 2
  filters them. Default to `unclear` and let Stage 2 read the JD before
  rejecting.
- **Anti-hallucination:** Only include results from actual searches. If a
  search returns 0, record 0. Never invent listings.
- **Copyright:** When summarizing snippets, paraphrase. Never quote 15+ words
  from a single posting.

---

*v2.3 Stage 1. Replaces the discovery-half of ONE_CLICK_v2.md.*
