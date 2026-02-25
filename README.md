# Job Search Intelligence Platform

> A multi-user job search automation system built as part of a 12-week AI engineering portfolio. Covers the full pipeline from job discovery through scored results, strategic analysis, funded company intelligence, and professional deliverables — running weekly across five active users.

---

## About

[Joey Clark](https://www.linkedin.com/in/joseph-clark-iii/) — program manager and ecosystem builder — built this system during a 12-week AI automation learning project (Jan–Apr 2026). What started as personal job search tooling evolved into a production-grade intelligence platform serving five people with distinct search profiles, custom scoring configurations, and weekly deliverables.

This repository documents both the working system and the learning journey behind it.

**Time commitment:** 8–12 hours/week · Washington, DC / Lisbon, Portugal

---

## Platform Overview

The system automates the full weekly job search cycle:

- **Multi-board search** across LinkedIn, Greenhouse, Lever, and Ashby
- **AI scoring engine** matching jobs against each user's resume using weighted criteria (industry fit, skills match, seniority, location, compensation) — customized per user
- **Master database** with deduplication, NEW/REPEAT detection, and application history tracking
- **Funding intelligence** pipeline scanning StrictlyVC, FINSmes, EU-Startups, and Sunday CET to surface companies likely to hire before roles are posted
- **Strategic analysis** engine generating score distributions, sector concentration, company hiring signals, and geographic breakdowns
- **Professional deliverables** — branded Excel reports with conditional formatting and templated HTML email delivery

---

## Tools

Python tools live in `JC3/` and run from the repo root.

| Tool | Description | Run |
|------|-------------|-----|
| `dashboard.py` | Terminal dashboard showing scores, sectors, and application status per user | `python3 JC3/dashboard.py [user]` |
| `serve.py` + `dashboard.html` | Local web server serving an interactive job browser at `localhost:8765` | `python3 JC3/serve.py` |
| `check_urls.py` | Weekly URL health check — pings every job link and auto-removes confirmed-closed listings | `python3 JC3/check_urls.py [user] [--dry-run]` |

---

## Weekly Workflow

Each user's search follows a five-step cycle, run every Sunday:

```
1. ONE_CLICK search   →  Multi-board scrape, AI score against resume, save Master List + Top 10
2. CONSOLIDATE        →  Merge weekly results into user's master database, preserve application history
3. check_urls.py      →  Ping all job URLs, drop confirmed-closed listings, flag blocked/error for review
4. MASTER_ANALYSIS    →  Generate strategic analysis (score trends, sector patterns, funded company matches)
5. Deliverables       →  Branded Excel files + delivery email drafted and sent to user
```

Funding intelligence and strategic analysis run from Week 2 onward, once enough data exists for trends.

---

## Users

The platform currently supports five active users with distinct search profiles:

- **Venture capital operator** — Chief of Staff and strategy roles, London and European fintech
- **Equity research analyst** — Long/short TMT, hedge fund buy-side, New York
- **Partnerships & BD** — Growth-stage startup roles, US remote and major markets
- **Defense technology** — Program management and operations, DC metro
- **European brand strategy** — Senior creative and brand leadership, international markets

Each user has a dedicated search configuration (target roles, locations, sector weights, scoring criteria) and receives personalized deliverables weekly.

---

## Repo Structure

```
ai-automation-portfolio/
├── searches/                     # Templates and prompts — edit here, not in results/
│   ├── For_Others/               # Per-user ONE_CLICK search configurations
│   ├── FRIEND_DELIVERY_EMAIL.md  # Email template + CoWork generation prompt
│   ├── MASTER_ANALYSIS_1.md      # Strategic analysis prompt
│   ├── FUNDING_INTEL.md          # Funding intelligence prompt
│   └── FORMAT_SPEC.md            # Output formatting reference
│
├── results/                      # Generated outputs — do not edit manually
│   └── For_Others/               # Per-user weekly results
│       └── [User]/Week_of_[date]/
│           ├── data/             # Master List CSV, Top 10 CSV (system backbone)
│           └── deliverables/     # Branded Excel, analysis PDF, delivery email HTML
│
├── JC3/                          # Python tools + personal search config
│   ├── dashboard.py              # Terminal stats dashboard
│   ├── serve.py                  # Local web dashboard server
│   ├── dashboard.html            # Web dashboard UI
│   └── check_urls.py             # Weekly URL health check
│
├── Core/                         # System reference files and curriculum
├── learning_log/                 # Weekly reflections and learning notes
└── Job_Search_Tracking.xlsx      # Cross-user operations and scheduling tracker
```

> **Templates and prompts live in `searches/`.** All generated outputs (CSVs, Excel files, PDFs, HTML emails) live in `results/`. Re-run the relevant prompt rather than editing output files directly.

---

## Week-by-Week Progress

### Week 0: CoWork Foundations ✅
**Completed:** January 28, 2026

- Organized file structure for job search automation
- First working search automation (LinkedIn + Greenhouse)
- Reusable search templates

*Learned: browser automation vs. direct web scraping, prompt engineering for AI agents, project scoping*

---

### Week 1: Multi-Board Searches & GitHub Setup ✅
**Completed:** February 4, 2026

- Multi-board search across LinkedIn, Greenhouse, Lever, Ashby in a single command
- CSV output with structured fields and edge case handling
- GitHub repository with version control workflow

*Learned: prompt structure (config → execution → extraction → verification), dynamic date handling, Git fundamentals*

---

### Week 2: One-Click Automation & Scoring ✅
**Completed:** February 9, 2026

- One-click weekly search with AI scoring against resume
- Deduplication across boards with NEW/REPEAT detection
- Friend search template and intake questionnaire system
- Onboarded first user (hedge fund equity research)

*Learned: scoring system design, template architecture, Git workflow as daily habit*

---

### Week 3: Multi-User Operations & Intelligence ✅
**Completed:** February 19, 2026

- Master database consolidation with application tracking columns
- 6-query strategic analysis engine (MASTER_ANALYSIS)
- Gmail intelligence pipeline (job search advice + StrictlyVC/FINSmes funding data)
- Branded Excel deliverables with professional formatting
- Onboarded 4 additional users across 5 search profiles
- Standalone funding intelligence prompt for proactive company prospecting

*Learned: data consolidation patterns, Gmail as an intelligence source, multi-user system design, the difference between reactive search (posted jobs) and proactive intelligence (funded companies)*

---

### Week 4: Python Tooling & Data Quality 🔄
**Started:** February 23, 2026

- Claude Code installation and local development environment setup
- Python terminal dashboard (`dashboard.py`) with multi-user support
- Local web application (`serve.py` + `dashboard.html`) for interactive job browsing
- URL health check system (`check_urls.py`) with auto-removal of confirmed-closed listings
- Data quality audit removing 107+ hallucinated and closed jobs from master databases
- URL integrity rules upgraded and enforced across all 6 active prompts

*In progress*

---

### Weeks 5–12: Upcoming

- Application tracking pipeline and follow-up automation
- Advanced pattern analysis and predictive scoring
- Error handling and edge case hardening
- Tool landscape survey (Zapier, Make, Cursor)
- Portfolio polish and public launch

---

## Technologies

- **Claude / CoWork** — AI agent orchestration, browser automation, and analysis generation
- **Python** — URL health checking, terminal dashboard, local web server (`dashboard.py`, `serve.py`, `check_urls.py`)
- **Gmail API** — Funding newsletter intelligence gathering
- **openpyxl** — Branded Excel report generation with conditional formatting
- **GitHub** — Version control and portfolio documentation

---

## Contact

Connect on [LinkedIn](https://www.linkedin.com/in/joseph-clark-iii/)

---

*Last updated: February 25, 2026*
