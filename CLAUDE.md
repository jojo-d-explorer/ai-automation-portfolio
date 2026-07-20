# CLAUDE.md

Persistent context for every Claude Code session working in this repo. Read
this first, then `Core/HANDOFF_ROADMAP_v4_Claude_Code.md` (full plan) and
`Core/STRATEGY_ADDENDUM_v4.md` (sourcing strategy) before doing v4 work.

## What this is

A job intelligence platform: automated discovery, verification, and AI-judged
scoring of job postings, run weekly. Two tracks: a frozen v5.x production
track serving five other users (`searches/For_Others/`, `results/For_Others/`
— **do not modify**), and Joey's own search, now being rebuilt as v4:
deterministic Python for discovery/fetch/verification, the model used only as
a judgment layer for scoring fetched JD text against a fixed rubric. See the
roadmap for the full v3→v4 architectural rationale.

## Where things actually are (read before assuming a path)

Phase 0 (2026-07-20) consolidated three parallel, drifted copies of Joey's
own pipeline that had accumulated across past pivots (a Europe-focused pass,
a LATAM-focused pass, an attempt at expanding the tool for other users):

- `searches/joey/` — the tracked, git-visible copy. Was stale (last touched
  March) until Phase 0 replaced its `companies.json` and `ats_api_checker.py`
  with the live versions below. **This is the canonical, single path going
  forward.**
- `job_search_project/` — Joey's real, actively-used working directory.
  **Deliberately gitignored**, not part of the public portfolio. Held the
  live 587-company corpus (`companies.json`, schema v2.2, last updated
  2026-06-10) and the working `ats_api_checker_v2.py`, both brought forward
  into `searches/joey/` during Phase 0. Also contains other users' data
  (config/results for Phil Tassi, Vivienne Pham, etc.) — leave those alone,
  same as the frozen v5.x track. Left in place, untouched, as a historical/
  backup copy — no longer the live driver.
- `job_search_project_v3/` — an incomplete May-11 migration draft (its own
  README describes it as meant to merge into `job_search_project/`; never
  happened). Archived wholesale to `searches/archive/job_search_project_v3/`.
- Joey's own ONE_CLICK prompt version history (v2.3, v2.3.1, v2.4 addendum,
  the most recent `ONE_CLICK_WEEKLY_SEARCH.md`) archived to
  `searches/archive/joey_one_clicks_v2/`. Reference only, not runbooks.
- Resume: `resume/Joey_Clark_Resume_4-25_FINAL.pdf` (new top-level dir,
  matching the roadmap's path — brought forward from `job_search_project/`).

If a future session finds `job_search_project/` still present: it is
intentionally untouched, private scratch space. Do not delete it without
asking; do not treat it as more current than `searches/joey/` going forward
— Phase 0 already pulled everything current out of it.

## Joey's search parameters (authoritative as of 2026-07-19)

- **Role families:** Chief of Staff; Country Manager/GM (Mexico, Argentina,
  LATAM); Head/Director/VP Partnerships; Senior BD; Market Entry /
  International Expansion; Director+ Operations/BizOps; Strategic
  Initiatives; Corporate Development; Operating Partner / VC Platform /
  Portfolio Ops; Ecosystem Lead; Government Affairs / Institutional
  Partnerships.
- **Geography (priority order):** Tier 1 — Mexico City/CDMX, Buenos Aires,
  Argentina, Mexico. Tier 2 — Remote-LATAM/Americas/Global, genuinely open
  remote only (no US residency/state/hybrid restriction; "Remote (US)" is
  excluded). Tier 3 — Remote-Global with explicit LATAM expansion mandate.
  Hard exclude: in-person-locked non-LATAM cities, US-residency-restricted
  roles. Warm-connection exceptions to the US-restriction exclusion are
  added to the corpus manually by Joey — the pipeline never guesses at them.
- **Sectors (priority order):** fintech/payments, EOR/cross-border ops,
  defense/dual-use, energy/industrial tech, VC/PE platform with LATAM
  mandate.
- **Seniority:** Director/VP/Head/CoS/Country Manager. Two-stretch cap
  applies (`prompts/score_jd_v4.md`).
- **Spanish:** beginner, actively learning. Spanish-required roles are
  flagged, not excluded.

## Hard rules — five failure modes, diagnosed from run history

Do not reintroduce these:

1. **Stale-index discovery.** Google `site:` search of ATS boards returns
   dead listings (one run: 32% already closed by fetch time). Fix: API-first
   (Greenhouse/Lever/Ashby direct). Search-sourced rows are the contamination
   vector — treat them as lower-trust than API rows.
2. **Snippet scoring.** Never score against a search snippet. No JD text,
   fetched and cached, means no score — a fetch-failure status instead.
3. **Runtime coupling.** Pipeline-critical steps (discovery, fetch,
   verification) are deterministic Python, never a model calling a network
   tool. The model is scoring-judgment only.
4. **Late URL verification.** Health checks run *before* JD fetch, not
   after — don't burn fetch/scoring budget on dead URLs.
5. **LATAM recall gap.** Country Manager / market entry roles in LATAM post
   disproportionately to LinkedIn, Getonbrd, and direct career pages, not
   US-centric ATS boards. Source list must reflect this (see addendum).

## File layout

```
CLAUDE.md                          this file
Core/HANDOFF_ROADMAP_v4_Claude_Code.md   full phase plan
Core/STRATEGY_ADDENDUM_v4.md       sourcing strategy (LinkedIn, diff, boards, SerpAPI)
config/joey_profile.yaml           consolidated search config (Phase 0)
config/load_profile.py             validates profile.yaml, fails loudly on missing keys
prompts/score_jd_v4.md             locked scoring prompt (Phase 2, built + wired into run.py)
config/joey_resume_digest.md       1-page resume digest for scoring, generated from the PDF (Phase 2)
resume/Joey_Clark_Resume_4-25_FINAL.pdf
scripts/corpus_append.py           appends new companies to companies.json (disqualifier-filtered)
scripts/classify_url.py            URL -> {ats, slug, job_id, url_type}; corpus_append.py dependency
scripts/disqualifiers.json         corpus_append.py's disqualifier rules
searches/joey/companies.json       live corpus (587 companies as of 2026-06-10; latam_relevance
                                    field added Phase 1, default "none" for all — no backfill
                                    source found, confirmed with Joey to leave as-is)
searches/joey/ats_api_checker.py   transitional; superseded by JC3/discover.py (Phase 1, built)
searches/archive/                  old prompts, deprecated scripts, Phase 0 backups — reference only
searches/For_Others/               frozen v5.x friends track — do not modify
JC3/run.py                         Phase 1 orchestrator — the roadmap's target command, built+verified
JC3/discover.py                    primary (ATS API sweep) + secondary (SmartRecruiters) + tertiary
                                    (stub — real recall sources are Phase 3, not built)
JC3/diff.py                        week-over-week/daily-new detection (Strategy Addendum §2)
JC3/health.py                      URL health check, runs before JD fetch, non-API rows only
JC3/fetch_jds.py                   full JD text fetch, requests + Playwright fallback
JC3/package.py                     dedup + NEW/REPEAT + CSV/XLSX packaging
JC3/score.py                       judgment layer (Phase 2) — both backends verified end-to-end:
                                    --backend api uses tool-forced structured output (freeform-text
                                    JSON proved unreliable in a live test: markdown fencing + a real
                                    JSON syntax error mid-response); --backend claude-p (roadmap
                                    default) shells out to the CLI, unwraps its --output-format json
                                    envelope, verified working too
jd_cache/                          cached JD text, keyed by sha256(url)[:16]
snapshots/                         diff.py's daily API-result snapshots
results/joey/LATAM/                v4 run output (Phase 1+), one Week_of_ folder per run
results/joey/Master_LATAM_Joey.csv running master list, NEW/REPEAT tracked by URL
results/For_Others/                frozen v5.x friends track — do not modify
```

## Run commands

- Full weekly run, including scoring: `python3 JC3/run.py --user joey --variant latam`
  (defaults to --backend claude-p per roadmap §8) or `--backend api`. Built and verified
  end-to-end against real data (2026-07-20): 114 companies checked, 3166 jobs scanned,
  14/15 JDs fetched (93%, above the 80% floor), 13 scored on both backends, branded XLSX
  + Master CSV produced. This week's real run scored 0 apply / 0 review / 13 skip — 11 of
  those correctly geo_restricted (real "Remote, United States" postings). Honest result,
  not a bug: the corpus isn't LATAM-enriched yet (Phase 3), so nothing this week should
  have scored well.
- Daily fast sweep (no JD fetch/scoring, ~2-3 min, no model tokens): `python3 JC3/run.py
  --user joey --variant latam --fresh-only`
- Individual stages are also directly runnable: `python3 JC3/discover.py`, `JC3/diff.py`,
  `JC3/health.py`, `JC3/fetch_jds.py`, `JC3/package.py`, `JC3/score.py [--backend api]` —
  each finds the current week's input automatically if run standalone.

## Reserved decisions — do not decide autonomously

1. **LATAM compensation floor** — unresolved (`config/joey_profile.yaml`
   marks this explicitly). Affects the comp subscore and two-stretch
   calculus. Do not guess a default.
2. Any change to the 60-point score cutoff or rubric weights.
3. Whether the RemoteGlobal secondary variant runs weekly alongside LATAM or
   biweekly.

## Conventions

- Small, reviewable commits.
- Never modify `searches/For_Others/` or `results/For_Others/`.
- Verify API terms/endpoints/URLs at build time — do not code against
  remembered URLs for new integrations (Getonbrd, fund portfolio boards,
  SmartRecruiters, SerpAPI).
