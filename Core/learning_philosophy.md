# Joey's Learning Philosophy & Context

## Background

- **Current Role:** Former SVP & Principal at Anzu Partners (venture capital)
- **Target Roles:** Chief of Staff, Strategic Operations, Partnerships at growth-stage startups
- **Career Transition:** Banking/VC → Startup operator roles
- **Learning Goal:** Build AI automation skills as differentiator for executive roles

## Learning Style

### What Works Best

- **Conceptual understanding over memorization** - Learning = pattern recognition, not rote memory
- **Real-world applications** - Immediate practical value (job search automation, personal OS, helping friends)
- **Productive struggle** - Embrace challenges but need guidance when genuinely stuck
- **"Why" before "how"** - Understanding principles before implementation details
- **Narrative context** - Connect concepts to business problems and real use cases

### How I Process Information

- Strong strategic thinking and process architecture skills
- Executive function challenges with spatial reasoning and mental variable manipulation
- Need explicit step-by-step guidance for file navigation and technical implementation
- Learn best through iteration and debugging real problems vs theoretical examples

## Teaching Approach That Works

### Session Structure (60-90 min)

- Conceptual explanation first (the "why")
- Hands-on building second (the "how")
- Guide with questions rather than giving immediate answers
- Celebrate productive struggle and learning from mistakes
- Adjust pacing based on feedback

### Communication Preferences

- Point out syntax and coding concepts as we encounter them (e.g., "# means comment")
- Explicit file path guidance (full paths, verify locations)
- Explain trade-offs and decision frameworks
- Connect technical work to business value
- Avoid overwhelming with information - focus on what's needed now

### What to Avoid

- Don't assume I remember implementation details from previous sessions
- Don't skip explaining file system operations (I need the step-by-step)
- Don't present multiple complex options simultaneously (one thing at a time)
- Don't use relative file paths without explaining where I am

## Constraints & Context

### Time Availability

- **Realistic commitment:** 8-12 hours/week
- **Newborn at home** - schedule flexibility needed
- **Occasional travel** - may have gaps between sessions
- **Sustainable pacing > sprint intensity**

### Technical Starting Point (Updated)

- **Competent:** Prompt engineering, Git/GitHub, Python scripting, data pipeline design
- **Building competence in:** Claude API, MCP integrations, tool-calling agents, multi-agent orchestration
- **Comfortable with:** Strategic thinking, systems design, stakeholder management
- **Rusty but familiar:** SQL, Tableau

### Current Setup

- **Phase 1 repo:** `/Users/jc3/GitHub/ai-automation-portfolio/` (production/maintenance)
- **Phase 2 repo:** `/Users/jc3/GitHub/personal-os/` (active development)
- **Tools:** Claude.ai, Claude Code, GitHub Desktop, CoWork
- **Computer:** Mac (Apple Silicon)
- **Active project:** Personal OS (Gmail, Calendar, Notion integrations)
- **Maintenance project:** Job search platform (weekly searches for 5 users)

## Key Insights About My Learning

### Mental Model Shifts

- "Expertise means faster iteration, not perfect recall"
- "Git tracks changes, not just files - every move matters"
- "Automation isn't about replacing work, it's about elevating human judgment"
- "Templates > memorization - build reusable systems"
- "Learning = pattern recognition developing faster over time"

### Phase 1 Insights

- **Trust in automated systems requires verification** — a 33% false-positive rate on URL checks eroded confidence in the entire system. Building check_urls.py wasn't optional polish, it was foundational to the service being credible.
- **Platform-specific edge cases matter** — generic solutions fail. Ashby needs GraphQL API calls, LinkedIn needs to be searched directly, Greenhouse/Lever need content scanning. Each platform has its own failure mode.
- **Scaling decisions have compound effects** — removing LinkedIn from automated search was a design decision driven by pattern recognition across multiple users' data. One architectural change cascaded to 6+ files, a verification script, and a new utility (linkedin_links.py).
- **Real problems don't follow curricula** — Week 3 data consolidation work surfaced Week 7 error handling problems. The skills developed simultaneously, not sequentially.
- **Questioning arbitrary numbers is a feature, not a bug** — applying this to scoring weights, staleness thresholds (45 days), and any system parameter. The numbers need to be consistent and useful, not precise.
- **Know when to ship** — Phase 1 reached production at Week 5. Padding to 12 weeks would have been artificial. Declaring "done" and moving to the next project was the right call.

### Success Indicators

- Can explain concepts to others (teaching = mastery)
- Prompts work on first try more often (80%+ success rate by Phase 1 end)
- Recognize issues before they happen (pattern recognition developing)
- Think "what else could I automate?" (creative application)
- Help others with their automation needs (proof of transferable skills)
- Debug systematically when things break (check_urls.py development process)
- Make architectural decisions with scaling implications (LinkedIn removal, phase transition)

## Goals

### Phase 2 (Personal OS)

- Build a working personal operating system with Gmail, Calendar, and Notion integrations
- Learn Claude API tool-calling and MCP integration patterns
- Demonstrate progression from browser automation (Phase 1) to API-driven agents (Phase 2)
- Create a second portfolio project that maps to Chief of Staff workflow

### Career

- Position AI automation skills as executive differentiator
- Demonstrate technical fluency for startup operator roles
- Prove ability to learn and apply new technical skills independently
- Two public portfolio projects showing real systems, real users, real iteration

### Long-term

- Become valuable in AI-augmented workplace
- Design human-in-the-loop systems for startup operations
- Bridge gap between technical and strategic thinking
- Model continuous learning and adaptation

## How to Use This File

**For Claude:** Read this at conversation start to understand my context, learning style, and constraints. Adjust teaching approach accordingly.

**For me:** Update as I discover new insights about how I learn best. This is a living document.

---

*Last updated: 2026-03-10*
*Active project: Phase 2 (Personal OS)*
