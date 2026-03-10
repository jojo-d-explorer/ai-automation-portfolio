# Job Search Intelligence Platform

A multi-user job search automation system built as Phase 1 of an AI engineering portfolio. Covers the full pipeline from job discovery through scored results, strategic analysis, funded company intelligence, and professional deliverables — running weekly across five active users.

## About

Joey Clark is an operator — most recently SVP at Anzu Partners — targeting Chief of Staff and strategic operations roles, who designed and built this system independently to develop hands-on AI automation capability. What started as personal job search tooling became a production intelligence platform: 5 active users, weekly deliverables, real feedback loops, and a system that gets better each week.

This repository documents both the working system and the learning journey behind it. **Phase 2** (Personal OS) continues in a [separate repository](https://github.com/jojo-d-explorer/personal-os).

**Time commitment:** 8–12 hours/week · Washington, DC / Lisbon, Portugal

---

## Platform Overview

The system automates the full weekly job search cycle:

* **Multi-board search** across Greenhouse, Lever, and Ashby (LinkedIn removed Feb 2026 due to Google index staleness — users receive direct LinkedIn search links instead)
* **AI scoring engine** matching jobs against each user's resume using weighted criteria (industry fit, skills match, seniority, location, compensation) — customized per user
* **URL verification pipeline** with platform-specific detection (Ashby GraphQL API, Greenhouse/Lever content scanning, JSON-LD staleness checking)
* **Master database** with deduplication, NEW/REPEAT detection, and application history tracking (21-column schema)
* **Funding intelligence pipeline** scanning StrictlyVC, FINSmes, EU-Startups, and Sunday CET to surface companies likely to hire before roles are posted
* **Strategic analysis engine** generating score distributions, sector concentration, company hiring signals, and geographic breakdowns
* **Professional deliverables** — branded Excel reports with conditional formatting and templated HTML email delivery

---

## Tools

Python tools live in `JC3/` and run from the repo root.

| Tool | Description | Run |
| --- | --- | --- |
| `check_urls.py` | URL health check with platform-specific detection (Ashby GraphQL, JSON-LD dates, content scanning) | `python3 JC3/check_urls.py [csv_path]` |
| `linkedin_links.py` | Generate personalized LinkedIn direct search URLs per user | `python3 JC3/linkedin_links.py [user]` |
| `verify_linkedin_removal.py` | Dry-run checker confirming LinkedIn removed from all ONE_CLICK files | `python3 JC3/verify_linkedin_removal.py` |
| `dashboard.py` | Terminal dashboard showing scores, sectors, and application status per user | `python3 JC3/dashboard.py [user]` |
| `serve.py` | Local web server serving an interactive job browser at localhost:8765 | `python3 JC3/serve.py` |

---

## Weekly Workflow (7 Phases)

Each user's search follows a standardized pipeline:

| Phase | Tool | Action | Time |
| --- | --- | --- | --- |
| 1. SEARCH | CoWork | ONE_CLICK prompt + resume | 8-10 min |
| 2. VERIFY | Terminal | `python3 JC3/check_urls.py [weekly.csv]` | 5 min |
| 3. CLEAN | Claude | "Clean [name]'s database" (master-db-cleanup skill) | 3-5 min |
| 4. CONSOLIDATE | CoWork | Merge weekly → master (CONSOLIDATE_UNIVERSAL.md) | 3-5 min |
| 5. ANALYZE | CoWork | MASTER_ANALYSIS (Week 3+) | 8-10 min |
| 6. PACKAGE | Manual | Build XLSX + PDF | 5-8 min |
| 7. DELIVER | Claude | "Draft email for [name]" (job-search-delivery skill) | 5 min |

**Key principle:** ONE_CLICK only does SEARCH. URL verification is Phase 2, run separately in Terminal.

See `searches/PIPELINE_QUICK_REFERENCE.md` for commands and `JC3/ops_playbook_v2.docx` for detailed instructions.

---

## Users

The platform currently supports five active users with distinct search profiles:

* **Venture capital operator** — Chief of Staff and strategy roles, DC and European markets
* **Equity research analyst** — Long/short TMT, hedge fund buy-side, New York metro
* **Partnerships & BD** — Growth-stage startup roles, DC and London
* **Defense technology** — Finance and IR leadership, DC and NYC
* **European brand strategy** — Senior creative and brand leadership, Lisbon and remote-global

Each user has a dedicated ONE_CLICK configuration (target roles, locations, sector weights, scoring criteria) and receives personalized deliverables weekly.

---

## Repo Structure

```
ai-automation-portfolio/
├── searches/                         # Templates and prompts
│   ├── For_Others/                   # Per-user ONE_CLICK search configurations
│   │   └── [User]/ONE_CLICK_[User].md
│   ├── ONE_CLICK_TEMPLATE_Friends_v3.md  # Master template for new users
│   ├── CONSOLIDATE_UNIVERSAL.md      # Database consolidation prompt
│   ├── PIPELINE_QUICK_REFERENCE.md   # Quick reference for 7-phase pipeline
│   ├── MASTER_ANALYSIS.md            # Strategic analysis prompt
│   ├── FUNDING_INTEL.md              # Funding intelligence prompt
│   └── EMAIL_DELIVERY_TEMPLATE_v1.html   # Delivery email template
│
├── results/                          # Generated outputs — do not edit manually
│   └── For_Others/                   # Per-user weekly results
│       └── [User]/
│           ├── Week_of_[date]/       # Weekly CSV + XLSX
│           └── Master_Job_Database_[User].csv
│
├── JC3/                              # Python tools
│   ├── check_urls.py                 # URL verification (Ashby GraphQL, JSON-LD, content scan)
│   ├── linkedin_links.py             # LinkedIn direct search URL generator
│   ├── verify_linkedin_removal.py    # Dry-run checker for LinkedIn removal
│   ├── dashboard.py                  # Terminal stats dashboard
│   ├── serve.py                      # Local web dashboard server
│   ├── ops_playbook_v2.docx          # Detailed operations manual
│   └── Skills/                       # Claude skill modules
│
├── Core/                             # Curriculum and learning philosophy
│   ├── curriculum_plan.md
│   ├── learning_philosophy.md
│   ├── technical_setup.md
│   └── prompt_engineering_principles.md
│
├── learning_log/                     # Weekly reflections
└── Job_Search_Tracking.xlsx          # Cross-user operations tracker
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

*Completed: March 2026*

* Expanded funding intelligence to 4 newsletter sources (added EU-Startups, Sunday CET)
* System running in production — weekly deliveries to all 5 users
* Operations playbook, pipeline reference, and delivery templates finalized
* Platform declared production-ready; transitioned to maintenance mode

**Learned:** when to stop building features and ship, documentation as a product, the difference between "done" and "perfect"

---

## What's Next: Phase 2

**Project:** Personal OS
**Repository:** [personal-os](https://github.com/jojo-d-explorer/personal-os)

Phase 2 applies the prompt engineering, pipeline architecture, and systems thinking from this project to personal executive operations — Gmail triage, calendar coordination, and task management through Claude API with MCP integrations.

This maps directly to Chief of Staff and Strategic Ops roles where managing information flow, scheduling, and cross-functional coordination are core responsibilities.

| Phase 1 Skill | Phase 2 Application |
|---|---|
| Prompt engineering | Agent system prompts, tool-calling patterns |
| Pipeline architecture (7-phase) | Multi-agent orchestration |
| Gmail intelligence extraction | Email triage and classification |
| Multi-user config management | Personal preference system |
| Quality gates (URL verification) | Response quality verification |
| Anti-hallucination rules | Grounded responses from real data |

---

## Technologies

* **Claude / CoWork** — AI agent orchestration, browser automation, and analysis generation
* **Python** — URL health checking (`check_urls.py`), LinkedIn link generation, terminal dashboard, local web server
* **Gmail** — Funding newsletter intelligence gathering
* **Ashby GraphQL API** — Programmatic job status verification
* **openpyxl** — Branded Excel report generation with conditional formatting
* **GitHub** — Version control and portfolio documentation

---

## Contact

[Connect on LinkedIn](https://www.linkedin.com/in/joeyclarkiii/)

---

*Phase 1 completed: March 2026 · 117+ commits*
*Phase 2: [personal-os](https://github.com/jojo-d-explorer/personal-os)*
