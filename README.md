# Job Search Intelligence Platform

A multi-user job search automation system built as Phase 1 of an AI engineering portfolio. Covers the full pipeline from job discovery through scored results, strategic analysis, funded company intelligence, and professional deliverables — running weekly across five active users.

## About

I'm Joey Clark, most recently SVP at Anzu Partners, with about a decade across DoD program management, banking, and venture capital. I built this system because I needed it. I was running my own job search and helping a few friends with theirs, and the existing tools weren't doing what I needed. So I started building, one piece at a time, and ended up with something I now run weekly for five people including myself.

The repo has two tracks. A production system (v5.x) runs weekly searches and produces deliverables for the five active users. An R&D track is where I prototype more sophisticated patterns against my own search first, before bringing them into the production track — now on its fourth major architecture, v4 (see Week 13 below). The two-stage discovery and scoring split, the auto-growing corpus, the JD-based filtering: all started as experiments on my search before they earned their way into the broader system.

Phase 2 — [Aula](https://github.com/jojo-d-explorer/spanish-aula), a full-stack Spanish-learning app — is live in a separate repository.

Time commitment: 8-12 hours/week · Washington, DC / Lisbon, Portugal

---

## Platform Overview

The system automates the full weekly job search cycle through a unified pipeline combining direct ATS API querying with broad web search:

* **ATS API checker** — per-user Python script querying target companies directly via Greenhouse, Lever, and Ashby APIs, bypassing Google's stale index entirely. Returns only live, verified-open jobs. The company corpus grows weekly as new companies are discovered through search results and funding intelligence.
* **Growing company corpus** (companies.json) a tiered list of target companies that feeds the API checker. Each user has their own. They start small and grow week over week. My own corpus has gone from 52 companies in February to 430 in May, covering Chief of Staff, Strategic Operations, International GM and Country Manager roles, and Government Affairs/Defense. 254 of those are API-queryable today (Greenhouse, Lever, Ashby); the rest sit on Workday, SmartRecruiters, WTTJ, or proprietary careers pages.
* **7-source wide-net search** across Greenhouse, Lever, Ashby, and Workday (via Google site:), plus Otta, Welcome to the Jungle, and efinancialcareers (direct platform searches)
* **AI scoring engine** matching jobs against each user's resume using weighted criteria (industry fit, skills match, seniority, location, compensation) — customized per user
* **Merge/dedup engine** combining API-verified results with search-sourced results, with API URLs taking priority and duplicate detection on Company + Job Title
* **URL verification pipeline** with platform-specific detection (Ashby GraphQL API, Greenhouse/Lever content scanning, JSON-LD staleness checking) — only checks non-API-sourced results
* **Master database** with deduplication, NEW/REPEAT detection, and application history tracking (21-column schema)
* **Funding intelligence pipeline** scanning StrictlyVC, FINSmes, EU-Startups, and Sunday CET to surface companies likely to hire before roles are posted — feeds directly into the company corpus
* **Strategic analysis engine** generating score distributions, sector concentration, company hiring signals, and geographic breakdowns
* **Professional deliverables** — branded 3-tab Excel reports (Verified Jobs, Non-Queryable Companies, LinkedIn Search Links) with conditional formatting and templated HTML email delivery

---

## The Core Insight: API-First Search

The fundamental problem with AI-powered job search is Google's stale index. Google's cache of ATS job boards lags by days or weeks — a search returning 30+ results might yield only 5 live URLs after verification. This erodes trust and wastes time.

The breakthrough: query ATS APIs directly. Greenhouse, Lever, and Ashby all expose public board APIs that return real-time job data. By maintaining a growing corpus of target companies per user and querying their APIs before each search, the system gets verified-live results without touching Google at all. The corpus compounds — each week's search results surface new companies that get added to the corpus, expanding next week's API coverage.

The unified pipeline merges these high-confidence API results with broader web search results (which still catch companies not yet in the corpus), deduplicates, scores, and verifies — producing a deliverable where every job is confirmed live.

**Example:** One user's search went from 2 verified jobs to 42 in a single week after deploying this architecture, driven by a corpus that had grown to 126 API-queryable companies across Greenhouse, Lever, and Ashby.

---

## Tools

Python tools live in `JC3/` and per-user tools live in `searches/For_Others/[User]/`.

| Tool | Description | Run |
| --- | --- | --- |
| `ats_api_checker.py` | Per-user script querying the user's company corpus via Greenhouse/Lever/Ashby APIs for live open roles | `python3 searches/For_Others/[User]/ats_api_checker.py` |
| `check_urls.py` | URL health check with platform-specific detection (Ashby GraphQL, JSON-LD dates, content scanning) | `python3 JC3/check_urls.py [csv_path]` |
| `linkedin_links.py` | Generate personalized LinkedIn direct search URLs per user | `python3 JC3/linkedin_links.py [user]` |
| `verify_linkedin_removal.py` | Dry-run checker confirming LinkedIn removed from all ONE_CLICK files | `python3 JC3/verify_linkedin_removal.py` |
| `dashboard.py` | Terminal dashboard showing scores, sectors, and application status per user | `python3 JC3/dashboard.py [user]` |
| `serve.py` | Local web server serving an interactive job browser at localhost:8765 | `python3 JC3/serve.py` |
| `verify_ats.py` | Three-step ATS verification. Auto-discovery first, then manual fill-in for the misses, then apply changes back with a backup. | `python3 scripts/verify_ats.py auto` |
| `install_gm_expansion.py` | Adds the GM lane corpus expansion to the right places, with validation and backup. | `python3 scripts/install_gm_expansion.py` |
| `corpus_append.py` | Adds newly discovered companies to the corpus automatically, filtering out ones that don't fit. | `python3 scripts/corpus_append.py --candidates [csv]` |
---

## Weekly Workflow

Each user's search follows a unified pipeline:

```
LOCAL                    COWORK                         LOCAL
─────                    ──────                         ─────
1. Funding intel    →    3. ONE_CLICK prompt:           5. check_urls.py
   (optional)               - Ingest API results           (only "Not Checked")
                             - Wide-net search (7 src)
2. ats_api_checker.py       - Merge + dedup             6. Rebuild XLSX
   → api_verified.csv       - Score + rank                 with verified data
                             - Output CSV + XLSX
                             - LinkedIn links            7. Deliver + commit
                          4. Report new companies
```

| Step | Tool | Action | Time |
| --- | --- | --- | --- |
| 1. FUNDING INTEL | CoWork / Manual | Scan newsletters, add companies to corpus (optional, biweekly) | 10-15 min |
| 2. API CHECK | Terminal | `python3 ats_api_checker.py` — query user's company corpus via API | 2-3 min |
| 3. SEARCH + MERGE | CoWork | ONE_CLICK prompt: ingest API results + wide-net search + merge/dedup + score | 10-15 min |
| 4. VERIFY | Terminal | `python3 JC3/check_urls.py [csv]` — only checks "Not Checked" rows | 5 min |
| 5. PACKAGE | CoWork | Rebuild 3-tab XLSX with verified results | 5-8 min |
| 6. DELIVER | CoWork | Draft delivery email, send XLSX + links | 5 min |
| 7. COMMIT | Terminal | Git commit all results | 1 min |

**Key principle:** API-verified jobs skip URL checking entirely. Only search-sourced results go through check_urls.py.

See `Core/friend_search_operations.md` for detailed instructions and `searches/For_Others/[User]/ONE_CLICK_[User].md` for per-user configurations.

---

## Users

The platform currently supports five active users with distinct search profiles:

* **Venture capital operator** — Chief of Staff and strategy roles, DC and European markets
* **Equity research analyst** — Long/short TMT, hedge fund buy-side, New York metro
* **Partnerships & BD** — Growth-stage startup roles, DC and London; first user on the v5.0 unified pipeline with ATS API checker and growing company corpus
* **Defense technology** — Finance and IR leadership, DC and NYC
* **European brand strategy** — Senior creative and brand leadership, Lisbon and remote-global

Each user has a dedicated ONE_CLICK configuration (target roles, locations, sector weights, scoring criteria) and receives personalized deliverables weekly. As users are upgraded to the v5.0 pipeline, each gets their own companies.json corpus and ats_api_checker.py — the corpus starts with companies from their sector and grows weekly through search results and funding intelligence.

---

## Repo Structure

```
ai-automation-portfolio/
├── searches/                              # Templates and prompts
│   ├── For_Others/                        # Per-user search configurations
│   │   └── [User]/
│   │       ├── ONE_CLICK_[User].md        # Unified pipeline prompt (v5.0)
│   │       ├── companies.json             # Target company corpus
│   │       ├── ats_api_checker.py         # ATS API checker script
│   │       └── executed_YYYY-MM-DD.txt    # Run logs
│   ├── ONE_CLICK_TEMPLATE_Friends_v3.md   # Master template for new users
│   ├── CONSOLIDATE_UNIVERSAL.md           # Database consolidation prompt
│   ├── PIPELINE_QUICK_REFERENCE.md        # Quick reference for pipeline
│   ├── MASTER_ANALYSIS.md                 # Strategic analysis prompt
│   ├── FUNDING_INTEL.md                   # Funding intelligence prompt
│   └── EMAIL_DELIVERY_TEMPLATE_v1.html    # Delivery email template
│
├── results/                               # Generated outputs
│   └── For_Others/
│       └── [User]/
│           ├── Week_of_[date]/
│           │   ├── api_verified_[date].csv           # ATS API output
│           │   ├── [User]_[date].csv                 # Merged/scored results
│           │   ├── [User]_Complete_[date].xlsx        # 3-tab branded XLSX
│           │   ├── LinkedIn_Links_[date].md           # Pre-built search URLs
│           │   ├── funding_intel_[User]_[date].csv    # Funding intel
│           │   └── deliverables/
│           │       └── delivery_email_[date].html     # HTML delivery email
│           └── Master_Job_Database_[User].csv
│
├── JC3/                                   # Shared Python tools
│   ├── check_urls.py                      # URL verification
│   ├── linkedin_links.py                  # LinkedIn search URL generator
│   ├── verify_linkedin_removal.py         # Dry-run checker
│   ├── dashboard.py                       # Terminal stats dashboard
│   ├── serve.py                           # Local web dashboard server
│   ├── ops_playbook_v2.docx               # Operations manual
│   └── Skills/                            # Claude skill modules
│
├── Core/                                  # System docs and learning philosophy
│   ├── friend_search_operations.md        # Operations guide (v5.0)
│   ├── curriculum_plan.md
│   ├── learning_philosophy.md
│   ├── technical_setup.md
│   └── prompt_engineering_principles.md
│
├── learning_log/                          # Weekly reflections
└── Job_Search_Tracking.xlsx               # Cross-user operations tracker
```

---

## Week-by-Week Progress

### Week 0: CoWork Foundations ✅

*Completed: January 28, 2026*

* Organized file structure for job search automation
* First working search automation (LinkedIn + Greenhouse)
* Reusable search templates

**Learned:** browser automation vs. direct web scraping, prompt engineering for AI agents, project scoping

### Week 1: Multi-Board Searches & GitHub Setup ✅

*Completed: February 4, 2026*

* Multi-board search across LinkedIn, Greenhouse, Lever, Ashby in a single command
* CSV output with structured fields and edge case handling
* GitHub repository with version control workflow

**Learned:** prompt structure (config → execution → extraction → verification), dynamic date handling, Git fundamentals

### Week 2: One-Click Automation & Scoring ✅

*Completed: February 9, 2026*

* One-click weekly search with AI scoring against resume
* Deduplication across boards with NEW/REPEAT detection
* Friend search template and intake questionnaire system
* Onboarded first user (hedge fund equity research)

**Learned:** scoring system design, template architecture, Git workflow as daily habit

### Week 3: Multi-User Operations & Intelligence ✅

*Completed: February 19, 2026*

* Master database consolidation with application tracking columns
* 6-query strategic analysis engine (MASTER_ANALYSIS)
* Gmail intelligence pipeline (StrictlyVC, FINSmes, EU-Startups, Sunday CET)
* Branded Excel deliverables with professional formatting
* Onboarded 4 additional users across 5 search profiles
* Standalone funding intelligence prompt for proactive company prospecting

**Learned:** data consolidation patterns, Gmail as intelligence source, multi-user system design, reactive search vs. proactive intelligence

### Week 4: Data Quality & Pipeline Standardization ✅

*Completed: March 2, 2026*

* **URL verification system v2** with platform-specific detection:
  + Ashby: GraphQL API (`ApiJobPosting` query) for definitive status
  + Greenhouse/Lever: HTTP status + 23 closed-job phrase scanning
  + JSON-LD `datePosted` extraction for staleness detection (>45 days)
  + Cross-domain redirect detection (ATS → generic careers page)
* **LinkedIn removal** from automated search due to Google index staleness — replaced with `linkedin_links.py` generating direct search URLs
* **21-column schema** standardized across all users (dropped Language_Requirement, added tracking columns)
* **7-phase pipeline** formalized: SEARCH → VERIFY → CLEAN → CONSOLIDATE → ANALYZE → PACKAGE → DELIVER
* **ONE_CLICK v3.1** deployed with clear separation: "This prompt does SEARCH only"
* **Data purge:** 150+ dead/stale jobs removed from master databases across all users
* **Operations playbook v2** documenting the complete weekly workflow

**Learned:** platform-specific API behavior, the cost of hallucinated data (trust erosion), pipeline separation (do one thing well), verification before consolidation

### Week 5: Production & Closeout ✅

*Completed: March 9, 2026*

* Expanded funding intelligence to 4 newsletter sources (added EU-Startups, Sunday CET)
* System running in production — weekly deliveries to all 5 users
* Operations playbook, pipeline reference, and delivery templates finalized
* Platform declared production-ready; transitioned to maintenance mode

**Learned:** when to stop building features and ship, documentation as a product, the difference between "done" and "perfect"

### Week 6: ATS API-First Architecture & Growing Company Corpus ✅

*Completed: March 17, 2026*

The biggest system upgrade since launch. Diagnosed the root cause of low verified-job counts (Google's stale ATS board index) and built a fundamentally different approach: query ATS APIs directly instead of searching Google.

* **ATS API checker** (`ats_api_checker.py`) — per-user Python script querying Greenhouse, Lever, and Ashby board APIs directly for real-time job data. Bypasses Google's stale index entirely. Filters by configurable role keywords and location targets.
* **Growing company corpus** (`companies.json`) — per-user tiered company database that compounds weekly. Companies are added from three sources: historical search results, funding intelligence, and manual additions. For the first user deployed, the corpus grew from 52 to 200 companies over 6 weeks by mining every historical search result and funding intel file — 126 API-queryable (Greenhouse/Lever/Ashby), 74 non-queryable (Workday/unknown). Each user's corpus starts small and grows as the system runs.
* **Unified pipeline (ONE_CLICK v5.0)** — single prompt orchestrating: API result ingestion → wide-net search across 7 sources → merge/dedup with API-URL priority → scoring → 3-tab XLSX output. Replaces the previous search-only prompt.
* **7-source search system** — added Workday (Google site:), Otta, Welcome to the Jungle, and efinancialcareers as search sources alongside existing Greenhouse/Lever/Ashby boards.
* **2-tier role system** — Primary roles (CoS, Partnerships, BD, Strategic Alliances, Commercial Director) searched everywhere; Secondary roles (Strategy & Ops, Growth, Ecosystem Partnerships, Corporate Development, Operating Partner, GTM Lead) searched on ATS + Otta only.
* **3-tab branded XLSX deliverable** — Tab 1: Verified Jobs with conditional formatting (score 90+, REPEAT, API-Verified indicators). Tab 2: Non-Queryable Companies with ATS resolution guide. Tab 3: LinkedIn Search Links grouped by location and role tier.
* **Funding intel → corpus integration** — newly funded companies automatically feed into companies.json tier_4, picked up by next API checker run. Closes the loop between proactive intelligence and verified job discovery.

**Result:** First deployment went from 2 verified jobs to 42 in one week — a 21x improvement — driven by a corpus of 126 API-queryable companies built from 6 weeks of historical data. All 42 had confirmed-live URLs via either API verification or URL health check.

**Learned:** when the data source is the problem, no amount of post-processing helps — go to the source of truth. API-first architectures are more reliable than search-first. The company corpus is a compounding advantage: more companies → more API queries → more verified jobs → new companies discovered in results → corpus grows → repeat. Each user's corpus gets more powerful over time.

### Week 7-9: Splitting Discovery from Scoring (v2.3) ✅
Completed: April 25, 2026

The biggest architecture change since the API-first switch in March. Running the system weekly, I noticed scores weren't always matching reality. Some near-miss roles were getting strong scores, and some genuinely good fits were getting middling scores. Tracing it back, the problem was that scoring was happening against search snippets (a sentence or two) rather than the full job description. The fix was to split the work into two stages.

- Stage 1, discovery only. Find candidate roles. Apply a title gate (drop anything clearly junior) and a remote gate (drop in-person-locked roles). No scoring. Produce a clean candidate list and grow the corpus with new companies that surfaced.
- Stage 2, verification and scoring. Fetch every candidate's full job description, then apply the scoring rubric to actual JD content. The remote check runs again at this stage against the JD itself, which catches cases where a snippet said "remote" but the JD specified "remote-EMEA only."
- Auto-grow corpus with a disqualifier list. New companies surfaced in discovery get added automatically, but a blocklist filters out categories that aren't a fit (consumer crypto retail, dating, gambling, healthcare admin, recruiting agencies). The list is conservative on purpose. Easier to remove a disqualifier than to manually filter the corpus every week.
- One threshold instead of two. Earlier versions had a "bubble band" of borderline scores I'd review manually each week. After watching it for a month, the bubble was usually noise. Removed it, kept a single 70+ cutoff for the master list, and started logging 60-69 separately for diagnostics.

Learned: when scoring is misbehaving, the problem is almost never the rubric. It's the data the rubric is being applied to. Snippet scoring was a load-bearing failure mode for months before I diagnosed it.

### Week 10: Two New Role Families and a Mode Flag (v2.3.1) ✅
Completed: April 26, 2026

Three small additive changes. Running v2.3 for a week surfaced gaps in the role family list. Strategy & Operations roles weren't being captured because they were getting tagged as "other" rather than fitting any of the existing seven families. Same with Corporate Development. Added both as their own families.

The other change was a MODE flag for which anchor variants to run. Some weeks I want everything (open remote plus geo-specific). Other weeks I want to sprint on a specific geography (Lisbon, EMEA, LATAM). Added a single config line that controls which anchors fire, so I don't have to comment out queries to focus a search.

Learned: the right time to add a configuration flag is the second time I want to do something different at run time. Not the first time, and not the fifth.

### Week 11-12: GM Lane Expansion and ATS Verification Tooling (v2.4) ✅
Completed: May 6, 2026

Two related projects.

The first was a deliberate corpus expansion. Reviewing several months of search results, I noticed the corpus was thin on International GM, Country Manager, and Vertical GM roles. Exactly the role types where my combination (DoD background, JD/MBA/MPP, planned Lisbon move) is most useful. So I built a target list of 35 new companies across four lanes (EMEA expansion plays, LATAM expansion plays, multi-region distributed, and Portuguese-rooted), then wrote a v2.4 addendum to the prompts. The addendum adds three new role families (international_gm, country_manager, vertical_gm) and expands the geographic anchor list to include the cities where these roles actually post (Lisbon, Madrid, London, Berlin, São Paulo, Mexico City, Bogotá, Buenos Aires, Miami).

The second was a verification tool I needed for myself. After the corpus expansion, I had about 48 companies whose ATS metadata was either unknown, marked needs-verification, or had notes like "real ATS but slug needs checking." Manually verifying 48 entries at a time isn't sustainable, so I wrote verify_ats.py. Three commands (auto, manual, apply) that probe Greenhouse/Lever/Ashby for what's findable, surface the rest for manual review, and apply the changes back with a backup.

Result: corpus grew from 395 to 430 companies. The ATS verification tool now handles a class of maintenance task that used to be one-off manual edits.

Learned: an automation system needs maintenance tooling at least as much as it needs feature tooling. Most of what's gone wrong with this system over six months has been data quality issues, not logic bugs.

### Week 13: v4 Rebuild — Code-as-Pipeline, Model-as-Judge ✅
Completed: July 2026

A full architectural rebuild of my own search track, moving it off CoWork-orchestrated prompts entirely. The prior R&D versions (v2.x–v2.4) used the model to drive search execution as well as scoring. Watching failure modes accumulate across six months of runs, the pattern was consistent: every real bug was a data-quality bug (stale URLs, snippet scoring, silent corpus drift), never a reasoning bug. So v4 flips the division of labor — deterministic Python owns discovery, fetching, and verification end to end; the model's only job is judgment, scoring a fixed rubric against full JD text that Python already fetched and cached.

Four phases, each committed and verified against real runs before moving to the next:

* **Phase 0 — Consolidation.** Three parallel, drifted copies of my own pipeline had accumulated across past pivots (a Europe-focused pass, a LATAM-focused pass, an attempt at generalizing the tool for other users). Merged them into one canonical, tracked path, and wrote down five recurring failure modes as hard rules for the rebuild: stale-index discovery, snippet scoring, runtime coupling (the model calling network tools instead of pure Python), late URL verification, and a LATAM recall gap (Country Manager / market-entry roles post disproportionately off the usual US-centric ATS boards).
* **Phase 1 — Orchestrator.** Built `JC3/run.py`, a six-stage pipeline (`discover → diff → health → fetch_jds → package → score`) — each stage a standalone, independently runnable script, deterministic except the final scoring call.
* **Phase 2 — Judgment layer.** Locked a scoring prompt (`prompts/score_jd_v4.md`) that runs against full fetched JD text, never a search snippet, with a resume digest generated from my actual resume. Verified two scoring backends end to end — a CLI backend and a direct-API backend using tool-forced structured output after a live test showed the API returning malformed freeform JSON.
* **Phase 3 — Recall expansion.** Extended discovery past standard ATS boards: a LinkedIn direct-search-link generator, and a VC-portfolio job board miner covering the "posts to portfolio-company boards before it ever hits an ATS" pathway. Of 13 funds on the target list, verified 5 as real, live, scrapable boards (Kaszek, QED Investors, Endeavor, a16z, General Catalyst) and documented the other 8 as not found rather than guessing — one had quietly rebranded. Wired the new source into the main discovery pipeline with full eligibility filtering, not a parallel, partially-filtered copy.

**Learned:** the "verify, don't trust remembered state" discipline that governs the pipeline's data has to govern its own build process too — several of this rebuild's real fixes (a fund's actual API shape, a platform's real auth requirement, whether a document was scrapable data or a personal contact list) only surfaced because each assumption got tested against a live source before being coded against.
---

## Phase 2: Aula (Spanish Learning Platform)

**Project:** Aula — a full-stack Spanish-learning web app
**Repository:** [spanish-aula](https://github.com/jojo-d-explorer/spanish-aula)

Phase 1 built automation on top of systems that already existed — Claude, ATS APIs, Gmail — orchestrating and querying them well. Phase 2 is building the tool itself: a full-stack app from scratch, including the data layer, the frontend, and my own LLM-orchestration API, that I use daily studying for the DELE exam.

Where Phase 1's hardest problems were pipeline and data-quality problems (stale indexes, snippet-vs-JD scoring, dedup), Phase 2's hardest problems are systems-design problems: structured LLM output a UI can trust, a real schema with migrations, and model routing decided per task instead of one-size-fits-all.

| Phase 1 Skill | Phase 2 Application |
|---|---|
| Prompt engineering | Tool-forced structured JSON output ("grading contracts"), prompt caching on stable system prompts |
| Pipeline architecture (unified v5.0) | React + Vite frontend, Vercel serverless API layer |
| Multi-user config management | Supabase/Postgres schema design with versioned migrations |
| Quality gates (URL verification) | Truncation detection and runtime contract validation on every LLM response |
| Company corpus + funding intel | Anki deck/schema-aware flashcard generation with a dedup ledger |
| Anti-hallucination rules | Grounded generation against a fixed error taxonomy and level-calibrated prompts |
| — | Full-stack ownership: schema design, frontend, mobile-first responsive UI, offline caching |
| — | Cost metering (token usage logged per call) built in from day one, not retrofitted |

**Status:** in active development. Writing practice with structured grading, threaded lessons, generated workbook exercises, and Anki-integrated flashcard generation are shipped; multi-user auth is deliberately deferred.

---

## Technologies

* **Claude / CoWork** — AI agent orchestration, search execution, scoring, and analysis generation
* **Python** — ATS API checker (`ats_api_checker.py`), URL health checking (`check_urls.py`), LinkedIn link generation, terminal dashboard, local web server
* **Greenhouse Board API** — Direct job board querying (`boards-api.greenhouse.io/v1/boards/{slug}/jobs`)
* **Lever Postings API** — Direct job board querying (`api.lever.co/v0/postings/{slug}`)
* **Ashby Posting API** — Direct job board querying (`api.ashbyhq.com/posting-api/job-board/{slug}`)
* **Ashby GraphQL API** — Programmatic job status verification
* **Gmail** — Funding newsletter intelligence gathering
* **openpyxl** — Branded 3-tab Excel report generation with conditional formatting
* **GitHub** — Version control and portfolio documentation

---

## Contact

[Connect on LinkedIn](https://www.linkedin.com/in/joeyclarkiii/)

---

*Phase 1 active: January–March 2026 · 120+ commits*
*Phase 2: [spanish-aula](https://github.com/jojo-d-explorer/spanish-aula) — active*
