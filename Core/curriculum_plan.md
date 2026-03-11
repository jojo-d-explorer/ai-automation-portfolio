# AI Automation Portfolio — Curriculum Plan

## Overall Goal

Build practical automation skills for startup operator roles through real projects, documented publicly as a portfolio.

## Portfolio Structure

This curriculum runs across two projects (phases), each in its own GitHub repository:

**Phase 1: Job Search Intelligence Platform** ✅ Complete
- Repo: `ai-automation-portfolio`
- Duration: Weeks 0-5 (Jan 27 – Mar 2026)
- Status: Production / maintenance mode

**Phase 2: Personal OS** 🔄 Active
- Repo: `personal-os`
- Duration: Starting March 2026
- Status: Building

---

## Phase 1: Job Search Intelligence Platform (Weeks 0-5)

### What Was Planned vs. What Happened

The original plan was a 12-week linear curriculum. Reality was better — real problems drove parallel skill development, and the project reached production status by Week 5:

- Week 3 data consolidation surfaced Week 7 error handling problems (URL verification)
- Week 2 friend onboarding surfaced Week 6 multi-user architecture decisions
- Week 3 analysis work surfaced Week 5 scoring pattern insights

By Week 5, the system was serving 5 users with branded deliverables, funding intelligence, and a 7-phase pipeline. Continuing to pad it to 12 weeks would have been artificial.

### Weekly Progress

- **Week 0:** CoWork foundations, first search automation
- **Week 1:** Multi-board search (Greenhouse, Lever, Ashby), GitHub setup, CSV output
- **Week 2:** One-click automation, AI scoring, friend template system, first user onboarded
- **Week 3:** Master database consolidation, 6-query analysis engine, Gmail funding intelligence (4 sources), branded xlsx/PDF deliverables, 4 more users onboarded
- **Week 4:** Pipeline hardening (check_urls.py, LinkedIn removal, platform-specific detection), 7-phase pipeline formalized, operations playbook
- **Week 5:** Funding intel expanded to 4 sources, production operations, system declared complete

### Skills Developed

- Prompt engineering (structured, version-controlled, multi-user)
- Git workflow (commit grouping, daily push habit, 117+ commits)
- Python scripting (check_urls.py, linkedin_links.py, verify_linkedin_removal.py, dashboard.py, serve.py)
- API integration (Ashby GraphQL)
- Data pipeline architecture (7-phase: SEARCH → VERIFY → CLEAN → CONSOLIDATE → ANALYZE → PACKAGE → DELIVER)
- Multi-user system design (config separation, template inheritance)
- Quality assurance (URL verification, anti-hallucination rules, dry-run checking)
- Gmail intelligence integration (StrictlyVC, FINSmes, EU-Startups, Sunday CET)
- Professional deliverable design (branded Excel, PDF reports, HTML email templates)

### System Status

Production / maintenance. Weekly searches continue for 5 users. No new features planned.

---

## Phase 2: Personal OS (Starting March 2026)

### Why This Project

Chief of Staff and Strategic Ops roles are fundamentally about managing information flow — knowing what needs attention, when, and from whom. This project builds a working system that does exactly that, while adding tool breadth (Claude API, MCP integrations, Gmail/Calendar/Notion) that Phase 1 didn't cover.

### Planned Architecture

**Core Integrations:**
- Gmail — email triage, priority classification, draft responses, newsletter extraction
- Google Calendar — schedule analysis, meeting prep, conflict detection
- Notion — task tracking, project status, meeting notes organization

**Intelligence Layer:**
- Cross-system awareness (email context + calendar context + task context)
- Priority scoring based on sender importance, topic urgency, and calendar proximity
- Weekly briefing generation

**Technical Approach:**
- Claude API with tool-calling / MCP integrations
- Modular agent design (email agent, calendar agent, task agent, orchestrator)
- Personal-use first, then extensible patterns

### Skills Transfer from Phase 1

| Phase 1 Skill | Phase 2 Application |
|---|---|
| Prompt engineering | Agent system prompts, tool-calling patterns |
| Pipeline architecture (7-phase) | Multi-agent orchestration |
| Gmail intelligence extraction | Email triage and classification |
| Multi-user config management | Personal preference system |
| Quality gates (URL verification) | Response quality verification |
| Anti-hallucination rules | Grounded responses from real data |

### Estimated Effort

~15-20 focused hours for a compelling MVP. Structured as weekly milestones, duration flexible based on complexity discovered.

---

## Decision Rationale

### Why depth-first?
- Depth transfers, breadth doesn't
- Startup roles need builders, not tool collectors
- Fundamentals apply across tools
- Second project is faster because of first project's foundation

### Why two phases instead of one 12-week plan?
- Phase 1 reached production naturally at Week 5 — padding to 12 weeks would be artificial
- Phase 2 is a genuinely different system (different integrations, different architecture patterns)
- Two completed projects with clear scope > one sprawling repo
- Each repo tells a coherent story independently

### Why Personal OS?
- Maps directly to target roles (COS, Strategic Ops)
- Adds tool breadth missing from Phase 1 (Claude API, MCP, Calendar, Notion)
- Personal-use system = always-relevant, always-testable
- Demonstrates progression: from browser automation → API-driven agents

---

*Last updated: 2026-03-10*
*Phase 1: Complete (ai-automation-portfolio)*
*Phase 2: Active (personal-os)*