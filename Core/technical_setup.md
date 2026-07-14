# Technical Setup & Environment

*Updated for Phase 2 transition — Aula, July 2026*

---

## Active Projects

| Project | Repo | Directory | Status |
|---------|------|-----------|--------|
| **Aula** (Phase 2) | `spanish-aula` | `/Users/jc3/GitHub/spanish-aula/` | Active development |
| **Job Search Platform** (Phase 1) | `ai-automation-portfolio` | `/Users/jc3/GitHub/ai-automation-portfolio/` | Production / maintenance |
| ~~Personal OS~~ (shelved) | `personal-os` | — | Scoped, never built — superseded by Aula |

---

## Phase 2: Aula

*Personal OS was the original Phase 2 plan — scoped, never built, shelved in favor of Aula. See `curriculum_plan.md` for the record.*

### Working Directory

**Location:** `/Users/jc3/GitHub/spanish-aula/`

### Repository Structure

```
spanish-aula/
├── src/
│   ├── features/       (writing, word-bank, lessons, workbook, flashcards)
│   └── shared/          (grading, prompts, flashcards, db)
├── api/                  (Vercel serverless functions — Anthropic proxy)
├── scripts/              (Anki .colpkg parser, plain Python)
├── supabase/migrations/
├── docs/                 (PRD.md, ANKI_SCHEMA.md)
└── CLAUDE.md
```

Full technical detail lives in that repo's own `CLAUDE.md` and `docs/PRD.md` — not duplicated here.

### Tools & Integrations

**AI Platform:**
- Anthropic API (Claude Sonnet for grading/lessons/flashcards, Haiku for workbook generation) via a Vercel serverless proxy — no client-side API key
- Claude Code (terminal-based development)

**Stack:**
- React + Vite frontend
- Supabase (Postgres), versioned SQL migrations
- Vercel (serverless functions + hosting)

**Development:**
- GitHub Desktop (version control)
- VS Code / Cursor (code editing)
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
- Phase 2 repo: spanish-aula (public)

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

*Last updated: 2026-07-14*
*Active project: Phase 2 (Aula / spanish-aula)*
