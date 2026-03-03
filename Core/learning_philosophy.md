# Joey's Learning Philosophy & Context

## Background

- **Current Role:** SVP & Principal at Anzu Partners (venture capital)
- **Target Roles:** Chief of Staff, Strategic Operations, Partnerships at growth-stage startups
- **Career Transition:** Banking/VC → Startup operator roles
- **Learning Goal:** Build AI automation skills as differentiator for executive roles

## Learning Style

### What Works Best

- **Conceptual understanding over memorization** - Learning = pattern recognition, not rote memory
- **Real-world applications** - Immediate practical value (job search automation, helping friends)
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

### Technical Starting Point

- **Rusty but familiar:** SQL, Python, Tableau
- **Currently learning:** CoWork, Claude AI, prompt engineering, Git/GitHub, Claude Code
- **Building competence in:** Python scripting (check_urls.py, linkedin_links.py), API calls (Ashby GraphQL), data pipelines
- **Comfortable with:** Strategic thinking, systems design, stakeholder management

### Current Setup

- **Primary working directory:** `/Users/jc3/GitHub/ai-automation-portfolio/`
- **Tools:** CoWork, Claude Code, GitHub Desktop, Claude Sonnet 4.5
- **Computer:** Mac (Apple Silicon)
- **Real project:** Job search automation (own use + 5-user service for friends)

## Key Insights About My Learning

### Mental Model Shifts

- "Expertise means faster iteration, not perfect recall"
- "Git tracks changes, not just files - every move matters"
- "Automation isn't about replacing work, it's about elevating human judgment"
- "Templates > memorization - build reusable systems"
- "Learning = pattern recognition developing faster over time"

### Week 3+ Insights

- **Trust in automated systems requires verification** — a 33% false-positive rate on URL checks eroded confidence in the entire system. Building check_urls.py wasn't optional polish, it was foundational to the service being credible.
- **Platform-specific edge cases matter** — generic solutions fail. Ashby needs GraphQL API calls, LinkedIn needs to be searched directly, Greenhouse/Lever need content scanning. Each platform has its own failure mode.
- **Scaling decisions have compound effects** — removing LinkedIn from automated search was a design decision driven by pattern recognition across multiple users' data. One architectural change cascaded to 6+ files, a verification script, and a new utility (linkedin_links.py).
- **Real problems don't follow curricula** — Week 3 data consolidation work surfaced Week 7 error handling problems. The skills developed simultaneously, not sequentially.
- **Questioning arbitrary numbers is a feature, not a bug** — applying this to scoring weights, staleness thresholds (45 days), and any system parameter. The numbers need to be consistent and useful, not precise.

### Success Indicators

- Can explain concepts to others (teaching = mastery)
- Prompts work on first try more often (70-80% success rate by Week 2)
- Recognize issues before they happen (pattern recognition developing)
- Think "what else could I automate?" (creative application)
- Help others with their automation needs (proof of transferable skills)
- Debug systematically when things break (check_urls.py development process)
- Make architectural decisions with scaling implications (LinkedIn removal)

## Goals for This Learning Journey

### Short-term (12 weeks)

- Build 8-10 working automations solving real problems
- Develop strong prompt engineering skills
- Create public GitHub portfolio demonstrating capabilities
- Master one tool ecosystem deeply (Claude/CoWork) before surveying others

### Medium-term (Resume/career)

- Position AI automation skills as executive differentiator
- Demonstrate technical fluency for startup operator roles
- Build "job search as a service" offering for network
- Prove I can learn and apply new technical skills independently

### Long-term (Professional development)

- Become valuable in AI-augmented workplace
- Design human-in-the-loop systems for startup operations
- Bridge gap between technical and strategic thinking
- Model continuous learning and adaptation

## How to Use This File

**For Claude:** Read this at conversation start to understand my context, learning style, and constraints. Adjust teaching approach accordingly.

**For me:** Update as I discover new insights about how I learn best. This is a living document.

---

*Last updated: 2026-02-26*
*Current week: 3 (in progress)*
