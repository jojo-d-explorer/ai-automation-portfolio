# 12-Week AI Automation Curriculum

## Overall Goal

Build practical automation skills for startup operator roles through real projects.

## Curriculum Structure

**Weeks 1-8: Deep Mastery (Claude/CoWork)**

- Week 1: ✅ Foundations, first automation
- Week 2: ✅ One-click automation, Git basics
- Week 3: 🔄 Data consolidation & analysis ← CURRENT
  - Also pulling forward Week 5 (scoring patterns) and Week 7 (error handling) organically
- Week 4: Application tracking (columns added, usage tracking in progress)
- Week 5: Advanced scoring & patterns (partially started — scoring refinement, sector analysis)
- Week 6: Multi-user systems (partially started — 5 users operational)
- Week 7: Error handling & edge cases (partially started — check_urls.py, platform-specific detection)
- Week 8: Production polish

**Weeks 9-10: Strategic Survey**

- Week 9: Landscape (Zapier/Make/n8n)
- Week 10: AI coding assistants (Cursor/Copilot)

**Weeks 11-12: Integration & Portfolio**

- Week 11: Transfer skills to new tool
- Week 12: Portfolio polish, go public

## What Actually Happened (vs. Plan)

The clean linear progression evolved into parallel skill-building driven by real problems:

- **Week 3 work surfaced Week 7 problems** — URL verification failures during data consolidation led to building check_urls.py with platform-specific error handling (Ashby GraphQL API, cross-domain redirect detection, JSON-LD staleness checking)
- **Week 3 work surfaced Week 5 patterns** — analyzing search results across users revealed LinkedIn index staleness as a systemic pattern, leading to an architecture decision (remove LinkedIn from automated search)
- **Week 6 multi-user system** started in Week 2 — now serving 5 users with personalized configs, branded deliverables, and funding intelligence

This is how real projects work: you don't encounter edge cases on a schedule.

## Skills Developed (through Week 3)

- Prompt engineering (structured, version-controlled, multi-user)
- Git workflow (commit grouping, daily push habit)
- Python scripting (check_urls.py, linkedin_links.py, verify_linkedin_removal.py)
- API integration (Ashby GraphQL)
- Data pipeline architecture (search → consolidate → analyze → deliver)
- Multi-user system design (config separation, template inheritance)
- Quality assurance (URL verification, dry-run checking)
- Strategic analysis (funding intelligence from 4 newsletter sources)

## Decision Rationale

Chose depth-first over breadth because:

- Depth transfers, breadth doesn't
- 12 weeks insufficient for both
- Startup roles need builders, not tool collectors
- Fundamentals apply across tools

---

*Last updated: 2026-02-26*
*Current week: 3 (in progress)*
