# Weekly Operations Playbook

*Step-by-step guide for running the job search service end-to-end.*
*Created: 2026-02-26 — based on the Phil Tassi "watershed" delivery.*

---

## What This Document Is

This is your operational runbook. Follow it top to bottom for each friend, each week. It captures every step, decision point, and quality gate that produced the Phil 02-26-2026 delivery — the one with 13 verified jobs, funding intel, dashboard screenshots, honest system notes, and a product roadmap.

The goal: **any friend's weekly delivery should be reproducible in 30-45 minutes of active work** (plus ~15 min of CoWork search time where you walk away).

---

## The Weekly Pipeline (Per Friend)

```
SEARCH → VERIFY → CLEAN → CONSOLIDATE → ANALYZE → PACKAGE → DELIVER
  15m      5m       5m        2m            5m        10m       5m
```

**Total: ~45 min active per friend** (search runs unattended)

---

## Phase 1: Run the Search

### Step 1: Open the ONE_CLICK prompt

**Location:** `searches/For_Others/[Name]/ONE_CLICK_[Name].md`

1. Open the file
2. Copy everything from "Calculate today's date..." to the end
3. Open CoWork (claude.ai)
4. Paste the prompt
5. Attach the friend's resume PDF
6. Hit enter
7. **Walk away for 10-15 minutes**

### Step 2: Verify search output

When CoWork finishes, check:

- [ ] CSV files saved to `results/For_Others/[Name]/Week_of_YYYY-MM-DD/`
- [ ] Master List CSV exists with 14 standard columns
- [ ] Top 10 CSV exists
- [ ] Verification summary shows total jobs, score range, board coverage
- [ ] No boards returned zero results (if one did, note it for the email)

**If CoWork saved files to the wrong location:** Move them manually to the correct path. This is a known CoWork quirk — always verify file paths.

---

## Phase 2: Verify URLs

### Step 3: Run check_urls.py

```bash
cd /Users/jc3/GitHub/ai-automation-portfolio
python3 JC3/check_urls.py results/For_Others/[Name]/Week_of_YYYY-MM-DD/Master_List_YYYY-MM-DD.csv
```

**What this does (v2.1):**
- **FIRST:** Checks URL specificity — flags generic company pages (no job ID in path) as GENERIC and auto-removes them. This runs before any HTTP request, saving time and catching CoWork hallucinations.
- Ashby: GraphQL API call for definitive status
- Greenhouse/Lever: HTTP status + content scanning for 23 closed-job phrases
- Detects cross-domain redirects (dead ATS → company careers page)
- Flags jobs >45 days old via JSON-LD datePosted

**What to look for in output:**
- How many jobs survived vs. were removed
- **Generic URLs removed** — these are company career pages without job IDs (the Phil 50→13 problem)
- Any "Error" status (network issues, not necessarily dead)
- Close reasons (helps you understand patterns)

---

## Phase 3: Clean & Consolidate the Master Database

### Decision: Do you need consolidation?

**First run (Week 1):** No consolidation needed. The weekly search output IS the master database. Copy the verified Master List CSV to:
```
results/For_Others/[Name]/Master_Job_Database_[Name].csv
```

**Week 2+:** Run the CONSOLIDATE_TO_MASTER prompt to merge new results into the existing master database. This handles deduplication (Company + Job_Title match) and updates metadata (Times_Seen, Last_Seen_Date).

### Step 5: Consolidate (Week 2+ only)

1. Open `searches/joey/CONSOLIDATE_TO_MASTER.md` (or the universal version)
2. Copy the prompt, adjusting paths for the specific friend
3. Paste into CoWork
4. Verify the output master database:
   - [ ] New jobs added with Status = "NEW"
   - [ ] Repeat jobs updated with incremented Times_Seen
   - [ ] No duplicate entries
   - [ ] Column schema matches standard (16 columns)

### Step 6: Clean the master database

After consolidation, the master may accumulate cruft over time. Periodically check for:

- **Schema drift:** Old rows with different column layouts (map old fields to new)
- **Generic URLs:** Company-level URLs without job IDs (remove)
- **LinkedIn URLs:** Should have been removed from automated search (remove)
- **Stale entries:** Jobs first seen 6+ weeks ago with no "Times_Seen" increase (consider archiving)

**The master database standard (16 columns):**
```
Score | Company | Job_Title | Location | Work_Arrangement | Sector |
Salary_USD | Job_Summary | URL | Score_Rationale | Times_Seen |
First_Seen_Date | Last_Seen_Date | Status | Found_On | URL_Status
```

---

## Phase 4: Funding Intelligence

### Step 7: Run FUNDING_INTEL.md in CoWork

1. Open `searches/For_Others/FUNDING_INTEL.md`
2. Paste into CoWork
3. CoWork scans Gmail for newsletters from the past 7 days:
   - `from:connie@strictlyvc.com newer_than:7d`
   - `from:info@finsmes.com newer_than:7d`
   - `from:thomas.ohr@eu-startups.com newer_than:7d`
   - `from:sundaycet@mail.beehiiv.com newer_than:7d`
4. Filter results against friend's target sectors and locations
5. Output: ranked list of recently funded companies matching their profile

**What to include in the email:**
- Top 3-5 matches (Score 7+) with company name, location, amount, round, and why it's relevant
- "Worth Watching" section for 5-6 tier with one-line descriptions
- VC fund raises deploying into adjacent sectors (their portfolio companies will hire)

---

## Phase 5: Package the Deliverables

### Step 8: Create the spreadsheet

**Decision: xlsx with multiple tabs (standard) or single CSV?**

For most friends, the xlsx is better — it's filterable, sortable, and professional. The standard format includes three tabs:

**Tab 1 — All Results:** Verified jobs with scores, summaries, rationale, clickable links
**Tab 2 — Search Summary:** Stats, location breakdown, methodology notes
**Tab 3 — LinkedIn Search Links:** Personalized direct search URLs

To generate LinkedIn links:
```bash
python3 JC3/linkedin_links.py [name]
```

### Step 9: Dashboard screenshots (optional but impressive)

```bash
cd /Users/jc3/GitHub/ai-automation-portfolio
python3 JC3/serve.py
```

1. Open `http://localhost:8765`
2. Select the friend from the dropdown
3. Cmd+Shift+4 → capture the dashboard
4. Ctrl+C in Terminal to stop the server
5. Attach screenshots to the email

**Prerequisite:** Friend's master database must be clean and at the expected path:
`results/For_Others/[Name]/Master_Job_Database_[Name].csv`

### Step 10: Draft the delivery email

Use `searches/For_Others/FRIEND_DELIVERY_EMAIL.md` as the template. The email has 7 sections:

**1. Opener + headline role** — Personal, warm, one standout role with context
**2. Quick stats** — Jobs found, score range, boards searched, locations
**3. Top roles** — 3-5 highlighted roles with score, location, and why it fits
**4. Funding intel** — Recently funded companies in their target space
**5. System notes** — Honest about what changed, what's improved, any caveats
**6. Coming soon** — Roadmap items (Google Sheets tracker, personal webpage, LinkedIn integration)
**7. Feedback ask** — Specific questions about boards, newsletters, criteria adjustments

**Tone principles:**
- Honest about limitations (builds trust)
- Frame suggestions as questions (invites engagement)
- Lead with the single most interesting finding
- Include "also worth a look" for roles 6-8 without overloading

### Decision: When to include analysis

| Situation | Include analysis? |
|-----------|------------------|
| Week 1 (first run) | No — not enough data for trends |
| Week 2 | Optional — can note what's new vs. repeat |
| Week 3+ | Yes — run MASTER_ANALYSIS for score trends, sector breakdown, company patterns |

---

## Phase 6: Deliver

### Step 11: Send the email

**Attachments checklist:**
- [ ] xlsx spreadsheet (3 tabs: results, summary, LinkedIn links)
- [ ] Dashboard screenshots (if captured)
- [ ] Master database CSV (clean, verified)
- [ ] Analysis PDF (Week 3+ only)

**Pre-send checklist:**
- [ ] Every URL in the spreadsheet has been verified live
- [ ] No LinkedIn URLs in automated results (LinkedIn links are in Tab 3 only)
- [ ] Score range and job count match what's in the email text
- [ ] Friend's name is correct throughout (don't send Phil's email to Aaron)
- [ ] Attachments are attached (not just referenced)

### Step 12: Git commit

After all deliveries are complete for the week:

```bash
cd /Users/jc3/GitHub/ai-automation-portfolio
# Open GitHub Desktop
# Review changed files
# Group related changes:
#   - "Week of 2026-MM-DD: search results for [names]"
#   - "Clean master databases after URL verification"
#   - "Update ONE_CLICK templates" (if any changes)
# Commit and push
```

---

## File Saving Conventions

### Where files live

```
results/For_Others/[First_Last]/
├── Master_Job_Database_[First_Last].csv    ← cumulative, clean, verified
├── Week_of_YYYY-MM-DD/
│   ├── data/
│   │   ├── Master_List_YYYY-MM-DD.csv      ← this week's raw results
│   │   └── Top10_New_YYYY-MM-DD.csv        ← top 10 new this week
│   └── deliverables/
│       ├── [Name]_Master_List_YYYY-MM-DD.xlsx
│       └── [Name]_Top10_New_YYYY-MM-DD.xlsx
```

### Naming rules

- Always use `First_Last` format (underscores, no spaces)
- Always use ISO dates: `YYYY-MM-DD`
- Always include file extension
- Master database filename is always: `Master_Job_Database_[First_Last].csv`

---

## Troubleshooting

### Problem: CoWork saves files to wrong location
**Fix:** Verify file paths after every run. Move files manually if needed. The ONE_CLICK prompt specifies absolute paths, but CoWork sometimes ignores them.

### Problem: check_urls.py shows "Error" for working URLs
**Fix:** Network timeouts happen. Re-run the script once. If it persists, manually check the URL in a browser. If it's live, mark URL_Status as "Verified" manually.

### Problem: Master database has schema drift (old columns, mixed formats)
**Fix:** Run the cleanup process:
1. Map old column names to new (Role → Job_Title, Board → Found_On, etc.)
2. Remove generic URLs (no job ID)
3. Remove LinkedIn URLs
4. Drop unused columns (empty tracking columns, legacy fields)
5. Sort by Score descending
6. Save as standard 16-column CSV

### Problem: Too few results from ATS boards
**Possible causes:**
- Industry doesn't post heavily on Greenhouse/Lever/Ashby (finance, defense)
- Search terms too narrow
- Location too restrictive
**Fix:** Supplement with LinkedIn direct search links (Tab 3 in xlsx). Consider adding industry-specific boards (eFinancialCareers for finance, Cleared Jobs for defense).

### Problem: Friend isn't engaging with the emails
**Don't:** Add more features they didn't ask for
**Do:** Ask one specific question in the next email ("Did the Anthropic role resonate? Too senior? Too junior?"). Engagement comes from relevance, not volume.

---

## ONE_CLICK Template Improvements to Consider

Based on the Phil delivery experience, these improvements would reduce manual post-processing:

### Already in templates
- 14-column standard schema
- URL verification and reconstruction
- Source filtering (exclude aggregators)
- Work arrangement standardization
- Score rationale for every job
- NEW/REPEAT detection

### Should add (vertical integration)
- **URL specificity requirement:** ✅ DONE — added to check_urls.py v2.1 (auto-removes generic URLs) and to all three Claude Skills (delivery, cleanup, funding intel).
- **Anti-hallucination language:** ✅ DONE — added to all three Claude Skills. Every skill now explicitly states: do not fabricate listings, report zero if zero found.
- **Automatic LinkedIn link generation:** Add a section at the end of ONE_CLICK that generates personalized LinkedIn search URLs for the friend's roles and locations, formatted for Tab 3 of the xlsx.
- **Funding intel integration:** Add a section that scans Gmail for funding newsletters and matches against the friend's profile. This would eliminate running FUNDING_INTEL.md as a separate step.
- **Dashboard-ready output:** Ensure the weekly CSV and master database CSV are always in the exact format the dashboard expects, so `serve.py` works without manual cleanup.

### Should NOT add (keep separate)
- **Master database cleanup:** This is a periodic maintenance task, not a weekly automation. Baking it into ONE_CLICK would make the prompt too complex and slow.
- **Email drafting:** Keep email composition as a separate step with Claude. The personalization and tone require human judgment — automating the full email would sacrifice the quality that makes the service valuable.

---

## Quality Gates (Non-Negotiable)

Before any email goes out, these must be true:

1. **Every URL has been verified live** — no dead links, no generic company pages
2. **No LinkedIn URLs in automated results** — LinkedIn links go in Tab 3 only
3. **Score and count in email match the spreadsheet** — if you say "13 jobs," there are 13 rows
4. **Friend's name is correct everywhere** — in the email, the xlsx tabs, the subject line
5. **Honest about limitations** — if a board returned zero, say so. If scoring isn't perfect, acknowledge it.

---

## Metrics to Track (For Your Own Learning)

| Metric | Where to find it | Why it matters |
|--------|-----------------|----------------|
| Jobs per search (pre-filter) | CoWork output summary | Search breadth |
| Jobs scoring 70+ (post-filter) | Master List row count | Search quality |
| Dead link rate | check_urls.py output | Pipeline reliability |
| Generic URL rate | URL specificity check | Data quality |
| Friend reply rate | Gmail | Service engagement |
| Time per delivery | Your own tracking | Operational efficiency |

---

## README Update Suggestions

The current README should be updated to reflect the system as it actually works now. Key additions:

### What to add

**1. System overview section:**
"An AI-powered job search intelligence platform that runs weekly automated searches across Greenhouse, Lever, and Ashby for multiple users, with URL verification, funding intelligence from 4 newsletter sources, and branded deliverables."

**2. Architecture diagram:**
```
ONE_CLICK search → URL verification → Master database consolidation
                                              ↓
                                    MASTER_ANALYSIS (PDF)
                                              ↓
Gmail newsletter scan → Funding intel → Delivery email + xlsx + screenshots
```

**3. Key capabilities:**
- Multi-user system (5 users with personalized search configs)
- Platform-specific URL verification (Ashby GraphQL, Greenhouse/Lever content scanning)
- Funding intelligence from 4 newsletter sources
- Branded xlsx deliverables with LinkedIn supplement
- Local web dashboard with per-user views
- Anti-hallucination and anti-aggregator protections

**4. Scripts section:**
- `JC3/check_urls.py` — URL health checker v2.1 with platform-specific detection + URL specificity (auto-removes generic company pages)
- `JC3/linkedin_links.py` — personalized LinkedIn search URL generator
- `JC3/verify_linkedin_removal.py` — dry-run checker for system changes
- `JC3/dashboard.py` — CLI dashboard
- `JC3/serve.py` — local web dashboard server

**5. Lessons learned section:**
- Why LinkedIn was removed from automated search
- Why URL specificity matters (company page ≠ job listing)
- Why honest communication about limitations builds trust
- Why professional packaging (xlsx, PDF, screenshots) changed friend engagement

### What to remove/update
- Any references to 4 boards (it's 3 now — LinkedIn removed)
- Old folder paths if they've changed
- Week references that are no longer current

---

## Skills to Build

These are the capabilities that would make the biggest difference to this system and to your career positioning. Ordered by impact, not difficulty.

### Tier 1: Build Now (Weeks 4-6)

**Python scripting fluency**
You've written check_urls.py, linkedin_links.py, verify_linkedin_removal.py, dashboard.py, and serve.py. You're past "can I write Python?" and into "can I build tools that solve real problems?" The next step is writing scripts from scratch without heavy guidance — taking a problem ("I need to deduplicate across two CSVs") and producing a working script in one sitting. Every script you build is portfolio evidence.

*Practice opportunity:* Run check_urls.py v2.1 against every friend's master database before tomorrow's deliveries. Compare the generic URL counts across users — do some friends have worse data quality than others? That pattern tells you something about which ONE_CLICK prompts need tightening.

**Prompt architecture for multi-step workflows**
Your ONE_CLICK prompts are strong single-step automations. The next level is chaining prompts where the output of one feeds the input of the next — without manual copy-paste in between. This is what "agentic" means in practice: SEARCH → output CSV → VERIFY URLs → output clean CSV → CONSOLIDATE → output master → ANALYZE → output PDF. Right now you're the glue between these steps. The skill is designing prompts that can hand off to each other.

*Practice opportunity:* Design a "FULL_PIPELINE_[Name].md" prompt that runs search + consolidation + funding intel in one CoWork session. Start with Joey's own search where the stakes are low.

**Data quality systems thinking**
The Phil master database disaster (36 columns, two schemas, generic URLs) happened because data quality wasn't designed in from the start — it was bolted on after problems surfaced. The skill here is anticipating data quality issues before they compound. Questions like: "If I merge this week's results with last week's, what could go wrong?" and "What assumptions am I making about the input format?"

*Practice opportunity:* Before running searches for other friends tomorrow, check their master databases for the same issues Phil's had. Are there generic URLs? Schema drift? LinkedIn remnants? Fix them proactively.

### Tier 2: Build Weeks 6-8

**API integration (beyond Ashby GraphQL)**
You've already called Ashby's GraphQL API from check_urls.py. The natural extensions: Google Sheets API (for the shared tracker you teased to Phil), Gmail API (for programmatic newsletter scanning instead of relying on CoWork), and eventually LinkedIn's unofficial endpoints (if you pursue the connection-matching idea).

*Practice opportunity:* Build a script that creates a Google Sheet from a friend's master database CSV and shares it with their email. This is the "Shared Google Sheet — Application Analytics" feature you promised Phil.

**HTML/CSS for email and web**
You're already generating HTML emails and running a local web dashboard. Leveling up means being able to modify dashboard.html confidently — adding a new chart, changing the layout, fixing a display issue without asking Claude to rewrite the whole file. You don't need to become a frontend developer, but reading and editing HTML/CSS/JS is a force multiplier.

*Practice opportunity:* Add a "Funding Intel" section to the dashboard that displays the most recent matches from your newsletter scan. This means modifying serve.py to serve funding data and dashboard.html to render it.

**Claude Code proficiency**
You installed Claude Code in your last session and used it for scripts. The efficiency gain comes from making it your default for file operations, script debugging, and repo management instead of switching between Terminal, TextEdit, and Finder. Claude Code can read your repo, run scripts, edit files, and commit to Git — all from one interface.

*Practice opportunity:* Do tomorrow's entire operations run through Claude Code instead of the CoWork + Terminal + Finder workflow. Note where it's faster and where it's clunkier.

### Tier 3: Build Weeks 9-12 (Portfolio Polish)

**System documentation for public consumption**
Your repo is private now and goes public in Weeks 8-12. The README, this playbook, and your learning philosophy are written for you and Claude. They need to be rewritten for a hiring manager who has 90 seconds to understand what you built and why it matters. The skill is translating "here's my process" into "here's evidence I can build operational systems."

**No-code/low-code tool evaluation**
Weeks 9-10 of your curriculum cover Zapier/Make/n8n. The skill isn't learning those tools — it's being able to evaluate whether they solve a problem better than what you've already built. Can Zapier replace your Gmail newsletter scanning? Probably. Should it? Depends on cost, flexibility, and maintenance burden. The skill is making that call with evidence.

**Interview storytelling**
Every system you've built is an interview answer. "Tell me about a time you built a process from scratch" → the job search pipeline. "How do you handle data quality issues?" → the Phil URL disaster and recovery. "How do you manage multiple stakeholders?" → the multi-user system with personalized configs. The skill is packaging these experiences into concise, compelling narratives.

---

## Claude Efficiencies

Ways to get more out of Claude across your workflow — both in this project chat and in CoWork.

### Project Context (This Chat)

**Use project files strategically.** Your 6 project files (curriculum, learning philosophy, technical setup, prompt engineering principles, git workflows, resume) give Claude persistent context. When you update your system — like removing LinkedIn or adding URL specificity checks — update the relevant project file so every future conversation starts with accurate context. Stale project files cause Claude to give you outdated advice.

**Files to add as project files:**
- This playbook (WEEKLY_OPERATIONS_PLAYBOOK.md) — so Claude knows your current process
- FORMAT_SPEC.md — so Claude knows your column schema without you re-explaining
- friend_search_operations.md — so Claude knows the multi-user architecture

**Files NOT to add:** Friend-specific ONE_CLICK files, weekly results, master databases. These change too often and would eat context window space. Upload them per-conversation when needed.

### Conversation Patterns That Save Time

**"Check [X] chat for [Y]" works now.** You saw this today — Claude can search your past conversations and pull specific deliverables, email drafts, and decisions. Use this instead of re-explaining context. "Check the Phil verification chat for the clean database" is faster than "I had a database with 13 jobs that we cleaned..."

**Front-load your intent.** Instead of "I need to work on Phil's stuff," say "I need to run Phil's weekly search, clean his master database, add funding intel, and draft a delivery email. I have 45 minutes." Claude can then sequence the work and tell you what to do in parallel (start the CoWork search while we draft the email).

**Ask Claude to make decisions, then override.** "What format should this be?" is slower than "I'm thinking xlsx with 3 tabs — does that make sense or is there a better option?" Give Claude something to react to rather than starting from zero.

**Use ask_user_input for structured decisions.** When Claude presents options as clickable choices, you answer faster and Claude gets unambiguous input. If Claude isn't doing this, ask: "Give me options for how to handle X."

### CoWork Efficiencies

**Batch operations across friends.** Instead of running one search, waiting, running the next, you can paste multiple friends' ONE_CLICK prompts into separate CoWork sessions and run them in parallel. Open 2-3 CoWork tabs, kick off searches, come back when they're all done.

**Save executed prompts.** Your ONE_CLICK templates include a "save executed prompt" step that records exactly what was run with the calculated dates. This is your audit trail — if results look wrong, you can compare the executed prompt to the template and spot what diverged.

**CoWork file path verification.** Add this to every ONE_CLICK prompt as the final step: "List all files created during this session with their full paths and sizes." This catches the "CoWork saved to wrong location" issue before you waste time looking for files.

### Claude Code Efficiencies

**Use it for multi-file operations.** When you need to update all ONE_CLICK files (like removing LinkedIn from all of them), Claude Code can read all files, make the changes, and verify them in one session. This is what verify_linkedin_removal.py does, but Claude Code can do it interactively.

**Use it for debugging.** When check_urls.py throws an error or produces unexpected results, paste the error into Claude Code. It can read your script, understand the context, and fix the issue — often faster than describing the problem in chat.

**Use it for Git operations.** Claude Code can stage files, write commit messages, and push — all from the terminal. This is faster than switching to GitHub Desktop for routine commits.

### Memory and Context Management

**Claude remembers across conversations in this project.** Key decisions (LinkedIn removal, 16-column schema, URL specificity requirement) persist through Claude's memory system. You don't need to re-explain these every session. But if Claude seems to have forgotten something, say "check past chats for [topic]" — the search tools will find it.

**Start sessions with state, not history.** Instead of "remember last time we..." say "Phil's master database is clean (13 jobs, 16 columns). I need to run Aaron's search now." Give Claude the current state, not the story of how you got there.

**When to start a new chat vs. continue.** Start new for: different friend's work, different type of task (coding vs. email drafting), sessions more than a few days apart. Continue in same chat for: multi-step work on the same deliverable, follow-up questions about something Claude just produced.

### Prompt Engineering Shortcuts

**Template inheritance saves time.** When onboarding a new friend, don't write their ONE_CLICK from scratch. Copy the template, change the 10-15 lines of config (name, roles, locations, scoring weights), and you're done. The engine is shared; only the config differs.

**Version your prompts.** When you improve a prompt (like adding URL specificity requirements), update the template AND all friend-specific files. Use the `*Template version: X.X | Updated: YYYY-MM-DD*` footer to track which version each friend is running. This prevents "why did Aaron's search include LinkedIn but Phil's didn't?" confusion.

**Test changes on your own search first.** Your personal search is the lowest-stakes environment. When you want to try a new feature (funding intel integration, new board, different scoring weights), run it on your own ONE_CLICK first. If it works, propagate to friends. If it breaks, no one sees it.

### Building Claude Skills (Advanced — Weeks 6-8)

Claude Skills are reusable instruction sets that live in `/mnt/skills/` and get triggered automatically based on task type. Three custom skills have been built for your workflow:

**Built skills (add as project knowledge files now):**
- **Job search delivery skill** (`SKILL_delivery_email.md`) — Triggered when you say "draft a delivery email for [name]." Contains the 7-section email template, tone principles, first-run vs. recurring logic, URL specificity quality gates, and anti-hallucination rules.
- **Master database cleanup skill** (`SKILL_master_db_cleanup.md`) — Triggered when you say "clean [name]'s master database." Contains the 16-column schema mapping, URL specificity check, LinkedIn removal, deduplication logic, and anti-hallucination rules.
- **Funding intel skill** (`SKILL_funding_intel.md`) — Triggered when you say "run funding intel for [name]." Contains Gmail search parameters for all 4 newsletters, scoring criteria, friend-specific filtering, and anti-hallucination rules.

**How to install:** Add the three SKILL.md files as project knowledge in your Claude project settings. Rename them so they're distinguishable. Claude reads them at conversation start and follows the instructions when relevant tasks come up.

---

*This playbook reflects the process as of 2026-02-28.*
*Update it as the system evolves — this is a living document.*
