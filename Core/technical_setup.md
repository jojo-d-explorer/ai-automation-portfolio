# Technical Setup & Environment

*Updated for Phase 2 transition — March 2026*

---

## Active Projects

| Project | Repo | Directory | Status |
|---------|------|-----------|--------|
| **Personal OS** (Phase 2) | `personal-os` | `/Users/jc3/GitHub/personal-os/` | Active development |
| **Job Search Platform** (Phase 1) | `ai-automation-portfolio` | `/Users/jc3/GitHub/ai-automation-portfolio/` | Production / maintenance |

---

## Phase 2: Personal OS

### Working Directory

**Location:** `/Users/jc3/GitHub/personal-os/`

### Repository Structure (Initial)

```
personal-os/
├── README.md
├── .gitignore
├── docs/
│   ├── architecture.md
│   └── learning_log/
├── agents/
│   ├── email/                 (Gmail agent)
│   ├── calendar/              (Google Calendar agent)
│   └── tasks/                 (Notion agent)
├── prompts/                   (Agent system prompts)
└── scripts/                   (Utility scripts)
```

### Tools & Integrations

**AI Platform:**
- Claude API (tool-calling, MCP integrations)
- Claude.ai (CoWork for browser tasks, Projects for context)
- Claude Code (terminal-based development)

**Target Integrations (MCP):**
- Gmail — email triage, priority classification, draft responses
- Google Calendar — schedule analysis, meeting prep, conflict detection
- Notion — task tracking, project status, meeting notes

**Development:**
- GitHub Desktop (version control)
- VS Code / Cursor (code editing)
- Python (scripting, API calls)
- Mac (Apple Silicon)

---

## Phase 1: Job Search Platform (Reference)

*This section preserved for reference when running weekly searches.*

### Working Directory

**Location:** `/Users/jc3/GitHub/ai-automation-portfolio/`

### Key File Paths

```
Joey's search:
/Users/jc3/GitHub/ai-automation-portfolio/searches/joey/ONE_CLICK_WEEKLY_SEARCH.md

Friend template:
/Users/jc3/GitHub/ai-automation-portfolio/searches/For_Others/ONE_CLICK_TEMPLATE_Friends.md

Friend ONE_CLICK:
/Users/jc3/GitHub/ai-automation-portfolio/searches/For_Others/[Name]/ONE_CLICK_[Name].md

Friend results:
/Users/jc3/GitHub/ai-automation-portfolio/results/For_Others/[Name]/Week_of_YYYY-MM-DD/

Friend master database:
/Users/jc3/GitHub/ai-automation-portfolio/results/For_Others/[Name]/Master_Job_Database_[Name].csv

Scripts:
/Users/jc3/GitHub/ai-automation-portfolio/JC3/

Funding intel:
/Users/jc3/GitHub/ai-automation-portfolio/results/funding_intel/
```

### Active Users (Phase 1)

| Person | Role Types | Locations | Status |
|--------|-----------|-----------|--------|
| **Joey** | Chief of Staff, Strategic Ops, Partnerships | DC, Remote-US, Lisbon, EU-Remote | Active |
| **Aaron Kimson** | L/S Hedge Fund Analyst, HF PM, Equity Research | NYC, SF, Chicago, Miami, Boston | Active |
| **Phil Tassi** | Chief of Staff, Partnerships, BD | Washington DC, London UK | Active |
| **Vivienne Pham** | CFO/VP Finance, Capital Markets/IR, BD/Portfolio Ops | NYC, DC, Remote | Active |
| **Rosalind** | Brand Strategy | Lisbon, Remote-Global | Active |

### Funding Intelligence Sources (4 newsletters)

| Source | Sender | Frequency |
|--------|--------|-----------|
| StrictlyVC | connie@strictlyvc.com | ~4-5x/week |
| FINSmes | info@finsmes.com | Daily |
| EU-Startups | thomas.ohr@eu-startups.com | Weekly (Thu) |
| Sunday CET | sundaycet@mail.beehiiv.com | Weekly (Sun) |

### Weekly Search Pipeline (per user)

```
ONE_CLICK → VERIFY (check_urls.py) → CLEAN → CONSOLIDATE → ANALYZE → PACKAGE → DELIVER
```

### Python Scripts (JC3/ folder)

| Script | Purpose | Usage |
|--------|---------|-------|
| `check_urls.py` | URL verification with platform-specific detection | `python3 JC3/check_urls.py [csv_path]` |
| `linkedin_links.py` | LinkedIn direct search URL generator | `python3 JC3/linkedin_links.py [name]` |
| `verify_linkedin_removal.py` | Dry-run checker for LinkedIn removal | `python3 JC3/verify_linkedin_removal.py` |
| `dashboard.py` | Terminal stats dashboard | `python3 JC3/dashboard.py [user]` |
| `serve.py` | Local web dashboard | `python3 JC3/serve.py` |

---

## Accounts & Services

**GitHub**
- Username: jojo-d-explorer
- Phase 1 repo: ai-automation-portfolio (public)
- Phase 2 repo: personal-os (private → public when ready)

**Claude.ai**
- Plan: Max
- Purpose: Projects, CoWork, Claude Code

**Email:** joey.clark3@gmail.com

---

## File Conventions

### Date Formats
**Always use ISO 8601:** `YYYY-MM-DD`

### File Naming
**Pattern:** `[Category]_[Description]_[Date].[extension]`
- No spaces (use underscores)
- Descriptive names
- Always include extension

### Paths
**Always use absolute paths in prompts** — relative paths break if the working directory changes.

---

*Last updated: 2026-03-10*
*Active project: Phase 2 (Personal OS)*
