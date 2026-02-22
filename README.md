# AI Automation Portfolio

## About This Project

I'm Joey Clark — a program manager and ecosystem builder transitioning into startup operations and partnerships roles. This repository documents my 12-week journey learning AI automation and agent development through real projects that solve real problems.

**Goal:** Build practical automation skills that solve real problems while creating a technical portfolio for growth-stage startup roles.

**Time Commitment:** 8-12 hours/week (Jan-April 2026)

---

## What I've Built

### Job Search Intelligence Platform (Weeks 0-3)

What started as a personal job search automation evolved into a multi-user intelligence platform serving 5 people with personalized, data-driven job search support.

**Core system:**
- Multi-board search automation across LinkedIn, Greenhouse, Lever, and Ashby
- AI-powered resume-matching algorithm scoring jobs 1-100 with weighted criteria customized per user
- Master database architecture with deduplication, weekly consolidation, and application tracking
- 6-query strategic analysis engine (score distributions, sector concentration, company hiring signals, geographic patterns, search evolution, and proactive funding intelligence)

**Intelligence layer:**
- Gmail integration scanning funding newsletters (StrictlyVC, FINSmes) to identify companies likely to hire before roles are posted
- Job search advice corpus auto-refreshed weekly from newsletter sources and woven into personalized strategy recommendations
- Strict filtering (2+ criteria match) to surface only high-signal funded companies per user's target profile

**Professional deliverables:**
- Branded Excel reports with conditional formatting, score color-coding, and auto-filters
- Strategic analysis reports with actionable recommendations
- Templated email delivery system for weekly updates

**Multi-user operations:**
- Onboarded 5 users with customized search configurations spanning hedge fund equity research, partnerships/BD, finance/capital markets, and brand strategy
- Each user has personalized scoring weights, sector targets, location filters, and seniority thresholds
- Searches span US and European markets (DC, NYC, Lisbon, Remote-Global)

**Scale:**
- 118+ jobs in personal master database
- Average match scores improved from 73.6 to 86.5 over 12 days of parameter tuning
- Remote roles consistently score 10+ points higher than location-specific positions

---

## Week-by-Week Progress

### Week 0: CoWork Foundations ✅
**Completed:** January 28, 2026

**What I Built:**
- Organized file structure for job search automation
- First working search automation (LinkedIn + Greenhouse)
- Reusable search templates

**What I Learned:**
- Browser automation vs. direct web scraping
- File system navigation and organization
- Prompt engineering for AI agents
- How to scope projects appropriately

---

### Week 1: Multi-Board Searches & GitHub Setup ✅
**Completed:** February 4, 2026

**What I Built:**
- Multi-board search across LinkedIn, Greenhouse, Lever, Ashby in a single command
- CSV output with structured fields and edge case handling
- GitHub repository with version control workflow

**What I Learned:**
- Prompt structure (config → execution → extraction → verification)
- Dynamic date handling (no manual updates week to week)
- Git fundamentals (commit, push, .gitignore, staging)

---

### Week 2: One-Click Automation & Scoring ✅
**Completed:** February 9, 2026

**What I Built:**
- One-click weekly search with AI scoring against resume
- Deduplication across boards with NEW/REPEAT detection
- Friend search template and intake questionnaire system
- Onboarded first friend (Aaron — hedge fund equity research)

**What I Learned:**
- Scoring system design (weighted criteria, rationale generation)
- Template architecture (build once, customize per user)
- Git workflow as daily habit (commit grouping, meaningful messages)

---

### Week 3: Multi-User Operations & Intelligence ✅
**Completed:** February 19, 2026

**What I Built:**
- Master database consolidation with application tracking columns
- 6-query strategic analysis engine (MASTER_ANALYSIS)
- Gmail intelligence pipeline (Remote100K advice + StrictlyVC/FINSmes funding data)
- Branded Excel deliverables with professional formatting
- Onboarded 4 additional users (Phil, Vivienne, Rosalind + personal search)
- Job search tracking spreadsheet across all users
- Standalone funding intelligence prompt for proactive company prospecting

**What I Learned:**
- Data consolidation patterns (weekly → master with preservation logic)
- Gmail as an intelligence source (newsletter parsing, structured extraction)
- Multi-user system design (shared templates, personalized configs)
- Professional output design (branded reports, strategic narratives)
- The difference between reactive search (posted jobs) and proactive intelligence (funded companies)

---

### Weeks 4-12: Upcoming
- Application tracking pipeline and follow-up automation
- Advanced pattern analysis and predictive scoring
- Error handling and edge case hardening
- Tool landscape survey (Zapier, Make, Cursor)
- Portfolio polish and public launch

---

## Technologies & Tools

- **Claude / CoWork** — AI agent orchestration and browser automation
- **GitHub** — Version control and portfolio documentation
- **Python** — Data processing (planned)
- **Gmail API** — Newsletter intelligence gathering
- **Prompt Engineering** — Structured templates, scoring systems, multi-step workflows

---

## Repository Structure

```
ai-automation-portfolio/
├── searches/           # Prompt templates (ONE_CLICK, CONSOLIDATE, MASTER_ANALYSIS, FUNDING_INTEL)
├── results/            # Weekly search outputs and deliverables per user
├── learning_log/       # Weekly reflections and insights
├── Core/               # Core prompt templates and system files
├── JC3/                # Personal search configuration and results
└── Job_Search_Tracking.xlsx  # Multi-user search operations tracker
```

---

## Contact

Connect with me on [LinkedIn](https://www.linkedin.com/in/joseph-clark-iii/)

*This is a learning portfolio documenting my technical skill development.*
- Location: Washington, DC / Lisbon, Portugal

---

*Last updated: February 21, 2026*
