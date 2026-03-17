# Job Search Intelligence Platform

A multi-user job search automation system built as Phase 1 of an AI engineering portfolio. Covers the full pipeline from job discovery through scored results, strategic analysis, funded company intelligence, and professional deliverables — running weekly across five active users.

## About

Joey Clark is an operator — most recently SVP at Anzu Partners — targeting Chief of Staff and strategic operations roles, who designed and built this system independently to develop hands-on AI automation capability. What started as personal job search tooling became a production intelligence platform: 5 active users, weekly deliverables, real feedback loops, and a system that gets better each week.

This repository documents both the working system and the learning journey behind it. **Phase 2** (Personal OS) continues in a [separate repository](https://github.com/jojo-d-explorer/personal-os).

**Time commitment:** 8–12 hours/week · Washington, DC / Lisbon, Portugal

---

## Platform Overview

The system automates the full weekly job search cycle through a unified pipeline combining direct ATS API querying with broad web search:

* **ATS API checker** — Python script querying 126+ companies directly via Greenhouse, Lever, and Ashby APIs, bypassing Google's stale index entirely. Returns only live, verified-open jobs.
* **200-company corpus** (`companies.json`) — tiered company database (multi-role signals, strong signals, search hits, funding intel) that feeds the API checker and grows weekly through search results and funding intelligence.
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

The breakthrough: query ATS APIs directly. Greenhouse, Lever, and Ashby all expose public board APIs that return real-time job data. By maintaining a growing corpus of target companies and querying their APIs before each search, the system gets verified-live results without touching Google at all.

The unified pipeline merges these high-confidence API results with broader web search results (which still catch companies not in the corpus), deduplicates, scores, and verifies — producing a deliverable where every job is confirmed live.

**Result:** Phil Tassi's search went from 2 verified jobs to 42 in one week after deploying this architecture.

---

## Tools

Python tools live in `JC3/` and per-user tools live in `searches/For_Others/[User]/`.

| Tool | Description | Run |
| --- | --- | --- |
| `ats_api_checker.py` | Queries 126+ companies via Greenhouse/Lever/Ashby APIs for live open roles matching target criteria | `python3 searches/For_Others/[User]/ats_api_checker.py` |
| `check_urls.py` | URL health check with platform-specific detection (Ashby GraphQL, JSON-LD dates, content scanning) | `python3 JC3/check_urls.py [csv_path]` |
| `linkedin_links.py` | Generate personalized LinkedIn direct search URLs per user | `python3 JC3/linkedin_links.py [user]` |
| `verify_linkedin_removal.py` | Dry-run checker confirming LinkedIn removed from all ONE_CLICK files | `python3 JC3/verify_linkedin_removal.py` |
| `dashboard.py` | Terminal dashboard showing scores, sectors, and application status per user | `python3 JC3/dashboard.py [user]` |
| `serve.py` | Local web server serving an interactive job browser at localhost:8765 | `python3 JC3/serve.py` |

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
| 2. API CHECK | Terminal | `python3 ats_api_checker.py` — query 126+ companies via API | 2-3 min |
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
* **Partnerships & BD** — Growth-stage startup roles, DC and London; first user on the v5.0 unified pipeline with 200-company corpus and ATS API checker
* **Defense technology** — Finance and IR leadership, DC and NYC
* **European brand strategy** — Senior creative and brand leadership, Lisbon and remote-global

Each user has a dedicated ONE_CLICK configuration (target roles, locations, sector weights, scoring criteria) and receives personalized deliverables weekly. Users with the v5.0 pipeline also have a companies.json corpus and ats_api_checker.py.

---

## Repo Structure

```
ai-automation-portfolio/
├── searches/                              # Templates and prompts
│   ├── For_Others/                        # Per-user search configurations
│   │   └── [User]/
│   │       ├── ONE_CLICK_[User].md        # Unified pipeline prompt (v5.0)
│   │       ├── companies.json             # Target company corpus (200+)
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

### Week 6: ATS API-First Architecture & 200-Company Corpus ✅

*Completed: March 17, 2026*

The biggest system upgrade since launch. Diagnosed the root cause of low verified-job counts (Google's stale ATS board index) and built a fundamentally different approach: query ATS APIs directly instead of searching Google.

* **ATS API checker** (`ats_api_checker.py`) — Python script querying Greenhouse, Lever, and Ashby board APIs directly for real-time job data. Bypasses Google's stale index entirely. Filters by 17+ role keywords and 10+ location targets.
* **200-company corpus** (`companies.json`) — expanded from 52 to 200 target companies by mining every historical search result and funding intel file. Organized in 4 tiers: multi-role signals, strong signals, search hits, funding intel. 126 API-queryable (Greenhouse/Lever/Ashby), 74 non-queryable (Workday/unknown).
* **Unified pipeline (ONE_CLICK v5.0)** — single prompt orchestrating: API result ingestion → wide-net search across 7 sources → merge/dedup with API-URL priority → scoring → 3-tab XLSX output. Replaces the previous search-only prompt.
* **7-source search system** — added Workday (Google site:), Otta, Welcome to the Jungle, and efinancialcareers as search sources alongside existing Greenhouse/Lever/Ashby boards.
* **2-tier role system** — Primary roles (CoS, Partnerships, BD, Strategic Alliances, Commercial Director) searched everywhere; Secondary roles (Strategy & Ops, Growth, Ecosystem Partnerships, Corporate Development, Operating Partner, GTM Lead) searched on ATS + Otta only.
* **3-tab branded XLSX deliverable** — Tab 1: Verified Jobs with conditional formatting (score 90+, REPEAT, API-Verified indicators). Tab 2: Non-Queryable Companies with ATS resolution guide. Tab 3: LinkedIn Search Links grouped by location and role tier.
* **Funding intel → corpus integration** — newly funded companies automatically feed into companies.json tier_4, picked up by next API checker run. Closes the loop between proactive intelligence and verified job discovery.

**Result:** Phil Tassi's search went from 2 verified jobs (Week 5) to 42 verified jobs (Week 6) — a 21x improvement. Of the 42, all had confirmed-live URLs via either API verification or URL health check.

**Learned:** when the data source is the problem, no amount of post-processing helps — go to the source of truth. API-first architectures are more reliable than search-first. Growing the company corpus is a compounding advantage: more companies → more API queries → more verified jobs → more new companies discovered → repeat.

---

## What's Next: Phase 2

**Project:** Personal OS
**Repository:** [personal-os](https://github.com/jojo-d-explorer/personal-os)

Phase 2 applies the prompt engineering, pipeline architecture, and systems thinking from this project to personal executive operations — Gmail triage, calendar coordination, and task management through Claude API with MCP integrations.

This maps directly to Chief of Staff and Strategic Ops roles where managing information flow, scheduling, and cross-functional coordination are core responsibilities.

| Phase 1 Skill | Phase 2 Application |
|---|---|
| Prompt engineering | Agent system prompts, tool-calling patterns |
| Pipeline architecture (unified v5.0) | Multi-agent orchestration |
| ATS API integration | External API design patterns |
| Gmail intelligence extraction | Email triage and classification |
| Multi-user config management | Personal preference system |
| Quality gates (URL verification) | Response quality verification |
| Company corpus management | Knowledge base maintenance |
| Anti-hallucination rules | Grounded responses from real data |

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
*Phase 2: [personal-os](https://github.com/jojo-d-explorer/personal-os)*
