# 12-Week AI Automation Curriculum

## Overall Goal

Build practical automation skills for startup operator roles through real projects.

## Curriculum Structure

**Weeks 1-8: Deep Mastery (Claude/CoWork)**

- Week 1: ✅ Foundations, first automation
- Week 2: ✅ One-click automation, Git basics
- Week 3: ✅ Data consolidation & analysis, multi-user onboarding
- Week 4: ✅ URL verification, pipeline standardization, data quality ← COMPLETED
- Week 5: Application tracking & follow-up automation
- Week 6: Advanced pattern analysis
- Week 7: Error handling & edge cases
- Week 8: Production polish, Claude Skills packaging

**Weeks 9-10: Strategic Survey**

- Week 9: Landscape (Zapier/Make/n8n)
- Week 10: AI coding assistants (Cursor/Copilot/Claude Code)

**Weeks 11-12: Integration & Portfolio**

- Week 11: Transfer skills to new tool
- Week 12: Portfolio polish, go public

## What Actually Happened (vs. Plan)

The clean linear progression evolved into parallel skill-building driven by real problems:

- **Week 3 work surfaced Week 7 problems** — URL verification failures during data consolidation led to building check_urls.py with platform-specific error handling (Ashby GraphQL API, cross-domain redirect detection, JSON-LD staleness checking)
- **Week 3 work surfaced Week 5 patterns** — analyzing search results across users revealed LinkedIn index staleness as a systemic pattern, leading to an architecture decision (remove LinkedIn from automated search)
- **Week 4 formalized the pipeline** — what was implicit became explicit: 7-phase workflow with clear handoffs, ONE_CLICK v3.1 that only does search, verification as a separate phase
- **Week 6 multi-user system** started in Week 2 — now serving 5 users with personalized configs, branded deliverables, and funding intelligence

This is how real projects work: you don't encounter edge cases on a schedule.

## Skills Developed (through Week 4)

**Prompt Engineering**
- Structured prompts with config/execution/extraction/verification pattern
- Version-controlled templates with inheritance (ONE_CLICK_TEMPLATE → per-user configs)
- Anti-hallucination discipline (explicit URL integrity rules, zero-fabrication instructions)
- Multi-user architecture (shared logic engine, personalized config blocks)

**Python Scripting**
- check_urls.py v2: Platform-specific URL verification
  - Ashby GraphQL API integration
  - JSON-LD metadata extraction for staleness detection
  - Content scanning for 23 closed-job phrases
  - Cross-domain redirect detection
- linkedin_links.py: Personalized LinkedIn search URL generation
- verify_linkedin_removal.py: Dry-run verification for system changes
- dashboard.py + serve.py: Terminal and web dashboards

**API Integration**
- Ashby GraphQL API (ApiJobPosting query)
- Gmail search for newsletter intelligence
- HTTP/content-based verification for Greenhouse/Lever

**Data Pipeline Architecture**
- 7-phase pipeline: SEARCH → VERIFY → CLEAN → CONSOLIDATE → ANALYZE → PACKAGE → DELIVER
- 21-column schema standardized across all users
- Deduplication logic (Company + Job_Title match)
- NEW/REPEAT detection with Times_Seen tracking

**Multi-User System Design**
- Template inheritance pattern
- Per-user scoring weight customization
- Config separation from logic engine
- 5 users operational with distinct search profiles

**Quality Assurance**
- URL verification as a quality gate (run before consolidation, not after)
- Platform-specific detection (generic solutions fail)
- Dry-run verification scripts for system changes
- Trust = verification (10 good links > 30 links with 10 dead)

**Strategic Analysis**
- Funding intelligence from 4 newsletter sources
- 6-query analysis pipeline (score distribution, sector breakdown, location patterns, repeat listings, work arrangement, funding matches)
- Branded deliverables (Excel + PDF + HTML email)

**Git Workflow**
- Daily commit habit
- Logical commit grouping
- Clean commit messages with context

## Decision Rationale

Chose depth-first over breadth because:

- Depth transfers, breadth doesn't
- 12 weeks insufficient for both
- Startup roles need builders, not tool collectors
- Fundamentals apply across tools

## Key Insights (Week 4)

1. **Platform-specific behavior matters** — Generic URL checks fail. Ashby needs GraphQL, LinkedIn can't be verified programmatically, Greenhouse/Lever need content scanning. Each platform has unique failure modes.

2. **Pipeline separation > monolithic prompts** — ONE_CLICK trying to do search + verification caused confusion. Clear handoffs between phases made the system understandable and debuggable.

3. **Verification before consolidation** — Dead links should never enter the master database. Moving check_urls.py to Phase 2 (before consolidation) was an architectural improvement.

4. **Trust erodes faster than it builds** — A 33% false-positive rate on URL checks eroded confidence in the entire system. Quality gates aren't optional polish; they're foundational to credibility.

5. **Questioning arbitrary numbers is a feature** — 45-day staleness threshold, 70-point score cutoff, 21-column schema — all of these evolved through iteration, not arbitrary specification.

---

*Last updated: 2026-03-03*
*Current week: 4 (completed)*
