# Weekly Operations Playbook v2.0

*Step-by-step guide for running the job search service end-to-end.*
*Updated: 2026-03-01 — reflects ONE_CLICK v3.0, 21-column schema, check_urls inside CoWork.*

---

## What This Document Is

This is your operational runbook. Follow it top to bottom for each friend, each week. The goal: any friend's weekly delivery should be reproducible in ~30 minutes of active work (plus ~15 min of unattended CoWork search time).

The pipeline was redesigned on 2026-03-01 based on the Vivienne delivery debrief. Key changes from v1.0: check_urls.py now runs inside CoWork (not a separate terminal step), Top 10 outputs eliminated, 21-column schema from the start, and parallel operations documented so you're never idle.

---

## The Weekly Pipeline (Per Friend)

```
SEARCH+VERIFY → CONSOLIDATE → FUNDING INTEL → PACKAGE → DELIVER
    20m              3m            5m            10m       5m
```

**Total: ~30 min active per friend** (search runs unattended for 15 of the 20)

**What changed from v1.0:**
- SEARCH and VERIFY merged — check_urls.py runs inside the ONE_CLICK prompt, so CoWork outputs clean, verified data
- CLEAN phase eliminated — 21-column schema means weekly CSVs are master-compatible from birth. No schema upgrade needed.
- Top 10 killed — master list sorted by score IS the top list

---

## Phase 1: Search + Verify (20 min, 15 unattended)

### Step 1: Launch the search

**Location:** `searches/For_Others/[Name]/ONE_CLICK_[Name].md`

1. Open the file
2. Copy everything from "Calculate today's date..." to the end
3. Open CoWork (claude.ai)
4. Paste the prompt
5. Attach the friend's resume PDF
6. Hit enter

**What happens inside CoWork (you walk away):**
- Searches 3 boards × roles × locations
- Scores against resume
- Saves weekly CSV (21 columns)
- Runs `python3 JC3/check_urls.py` on the CSV
- Removes CLOSED, STALE, GENERIC rows
- Generates branded xlsx from clean data
- Updates Job_Search_Tracking.xlsx

### Step 2: Verify output (when you come back)

- [ ] Weekly CSV exists at `results/For_Others/[Name]/Week_of_YYYY-MM-DD/data/`
- [ ] Branded xlsx exists at `results/For_Others/[Name]/Week_of_YYYY-MM-DD/deliverables/`
- [ ] Verification summary shows: raw count, excluded count, final verified count
- [ ] No boards returned zero results (if one did, note it for the email)
- [ ] File paths are correct (CoWork sometimes saves to wrong location)

**If CoWork saved files to the wrong location:** Move them manually. Known quirk — always verify.

---

### ⏱️ WHILE COWORK RUNS (15 min of parallel work)

Don't sit idle. Here's what you can do while the search runs unattended:

**In Terminal / Claude Code:**
- Run `check_urls.py` on a different friend's master database
- Run `linkedin_links.py` for this friend's LinkedIn supplement
- Organize JC3/ folder or clean up old weekly result folders
- Git commit previous session's work

**In Gmail:**
- Pre-scan funding newsletters for this friend's sectors (you'll run the formal scan in Phase 3, but a quick look now means you already know if there are matches)
- Check if any friends replied to last week's delivery

**In this Claude chat:**
- Start drafting the delivery email opener (you know the friend's profile)
- Review previous week's master database for patterns
- Plan next week's search adjustments based on friend feedback

---

## Phase 2: Consolidate (3 min)

### Decision: Is this Week 1 or Week 2+?

**Week 1 (first run):** No consolidation needed. The weekly CSV IS the master database. Copy it:
```
cp results/For_Others/[Name]/Week_of_YYYY-MM-DD/data/Results_YYYY-MM-DD.csv \
   results/For_Others/[Name]/Master_Job_Database_[Name].csv
```

**Week 2+:** Run the CONSOLIDATE_TO_MASTER prompt in CoWork.

### Step 3: Consolidate (Week 2+ only)

1. Open `searches/joey/CONSOLIDATE_TO_MASTER.md`
2. Adjust paths for the specific friend
3. Paste into CoWork
4. Verify output:
   - [ ] New jobs added with Status = "NEW"
   - [ ] Repeat jobs updated: Times_Seen incremented, Last_Seen_Date updated
   - [ ] No duplicate entries (Company + Job_Title match)
   - [ ] Column schema is 21 columns

**Why consolidation is simpler now:** Weekly CSVs already have all 21 columns with metadata pre-filled (Times_Seen=1, First_Seen_Date, Last_Seen_Date). Consolidation is a merge + dedup, not a schema upgrade.

---

## Phase 3: Funding Intelligence (5 min)

### Step 4: Run funding intel

**Skill trigger:** Say "run funding intel for [Name]" in this Claude chat.

The funding intel skill scans Gmail for newsletters from the past 7 days:
- `from:connie@strictlyvc.com newer_than:7d` (StrictlyVC)
- `from:info@finsmes.com newer_than:7d` (FINSmes)
- `from:thomas.ohr@eu-startups.com newer_than:7d` (EU-Startups)
- `from:sundaycet@mail.beehiiv.com newer_than:7d` (Sunday CET)

Scores matches against the friend's target sectors, locations, and company stage.

**Output for the email:**
- Top 3-5 matches (Score 8-10) with company, amount, round, and why it fits
- "Worth Watching" tier (Score 5-7)
- VC fund raises deploying into the friend's sectors

**If no matches this week:** Say so honestly. Don't lower thresholds to manufacture relevance.

---

## Phase 4: Package (10 min)

### Step 5: Generate LinkedIn links

```bash
python3 JC3/linkedin_links.py [name]
```

Output: formatted links for the friend's roles × locations with past-week filter. These go in Tab 3 of the xlsx (already generated by ONE_CLICK v3.0) and in the delivery email.

### Step 6: Dashboard screenshots (optional but impressive)

```bash
cd /Users/jc3/GitHub/ai-automation-portfolio
python3 JC3/serve.py
```

1. Open `http://localhost:8765`
2. Select the friend from the dropdown
3. Cmd+Shift+4 → capture
4. Ctrl+C in Terminal to stop
5. Attach screenshots to email

**Prerequisite:** Friend's master database must be at the canonical path:
`results/For_Others/[Name]/Master_Job_Database_[Name].csv`

### Step 7: Draft the delivery email

**Skill trigger:** Say "draft delivery email for [Name]" in this Claude chat.

The delivery email skill produces a 7-section email:
1. Opener + headline role
2. Quick stats
3. Top 3-5 roles with personalized context
4. Funding intelligence
5. System notes (honest about changes/limitations)
6. Coming soon / roadmap
7. Feedback ask

**First-run vs. recurring:** The skill adjusts automatically — Week 1 includes "how the system works" explanation and calibration framing. Week 2+ leads with what's new vs. repeat.

### Decision: When to include analysis

| Situation | Include analysis? |
|-----------|------------------|
| Week 1 | No — not enough data |
| Week 2 | Optional — note what's new vs. repeat |
| Week 3+ | Yes — run MASTER_ANALYSIS for PDF report |

---

## Phase 5: Deliver (5 min)

### Step 8: Send the email

**Attachments checklist:**
- [ ] xlsx spreadsheet (3 tabs: All Results, Search Summary, LinkedIn Search Links)
- [ ] Dashboard screenshots (if captured)
- [ ] Analysis PDF (Week 3+ only)

**Pre-send checklist:**
- [ ] Every URL has been verified (check_urls ran inside CoWork)
- [ ] No LinkedIn URLs in Tab 1 (LinkedIn links in Tab 3 only)
- [ ] Score range and job count in email text match the spreadsheet
- [ ] Friend's name is correct throughout (email, xlsx tabs, subject line)
- [ ] Attachments are actually attached

### Step 9: Git commit

After all deliveries are complete for the week:

1. Open GitHub Desktop
2. Review changed files
3. Group related changes:
   - "Week of 2026-MM-DD: search results for [names]"
   - "Update master databases after consolidation"
   - "Template updates" (if any)
4. Commit and push

---

## Skill Triggers (Quick Reference)

These replace verbose step-by-step instructions. Say these phrases in this Claude chat and the corresponding skill activates:

| Phrase | What it does |
|--------|-------------|
| "draft delivery email for [Name]" | 7-section email with tone principles, quality gates |
| "clean [Name]'s database" | 21-column schema mapping, URL specificity, dedup, LinkedIn removal |
| "run funding intel for [Name]" | Scan 4 newsletters, score against friend's config |

**Skills are installed as project knowledge files.** Claude reads them at conversation start. You don't need to explain the template, schema, or newsletter sources — the skills contain all of it.

---

## Parallel Operations Map

The biggest efficiency gain is never being idle. Here's what can happen simultaneously:

### During ONE_CLICK search (15 min unattended)

| You're in... | Do this... |
|---|---|
| Terminal / Claude Code | `check_urls.py` on another friend's master DB |
| Terminal / Claude Code | `linkedin_links.py` for current friend |
| Terminal / Claude Code | Git commit previous session's work |
| Gmail | Pre-scan funding newsletters |
| Gmail | Check for friend replies to last delivery |
| This Claude chat | Start drafting email opener |
| This Claude chat | Review friend's previous master DB for patterns |

### During CONSOLIDATE (3 min in CoWork)

| You're in... | Do this... |
|---|---|
| This Claude chat | Draft delivery email body |
| Terminal | Prepare dashboard screenshots |
| Gmail | Pull funding intel matches for email Section 4 |

### During MASTER_ANALYSIS (5 min in CoWork, Week 3+ only)

| You're in... | Do this... |
|---|---|
| This Claude chat | Finalize delivery email |
| Terminal | Verify attachment file sizes / paths |
| Gmail | Queue email as draft with attachments |

### Batching across friends

Run 2-3 friends' ONE_CLICK searches in parallel CoWork tabs. Come back when all are done. Then consolidate, package, and deliver sequentially (each takes only 10-15 min of active work once search is done).

---

## File Saving Conventions

### Where files live

```
results/For_Others/[First_Last]/
├── Master_Job_Database_[First_Last].csv    ← cumulative, clean, verified
├── Week_of_YYYY-MM-DD/
│   ├── data/
│   │   └── Results_YYYY-MM-DD.csv          ← this week's verified results
│   └── deliverables/
│       └── [Name]_Jobs_YYYY-MM-DD.xlsx     ← branded spreadsheet
```

### Naming rules

- Always `First_Last` format (underscores, no spaces)
- Always ISO dates: `YYYY-MM-DD`
- Always include file extension
- Master database: `Master_Job_Database_[First_Last].csv`
- Weekly results: `Results_YYYY-MM-DD.csv`
- Branded xlsx: `[First_Last]_Jobs_YYYY-MM-DD.xlsx`

### Schema (21 columns, fixed order)

```
FRIEND-FACING:  Score | Company | Job_Title | Location | Score_Rationale |
                Work_Arrangement | Sector | Salary_USD | Job_Summary | URL

SYSTEM:         Status | URL_Status | Found_On | Times_Seen |
                First_Seen_Date | Last_Seen_Date

TRACKING:       Interest_Level | Applied_Date | Application_Method |
                Response_Status | Notes
```

---

## Troubleshooting

### Problem: CoWork saves files to wrong location
**Fix:** Verify file paths after every run. Move files manually. ONE_CLICK specifies absolute paths, but CoWork sometimes ignores them.

### Problem: check_urls.py fails inside CoWork
**Fix:** CoWork may not have network access for the HTTP checks. If check_urls fails, run it manually after CoWork completes:
```bash
cd /Users/jc3/GitHub/ai-automation-portfolio
python3 JC3/check_urls.py results/For_Others/[Name]/Week_of_YYYY-MM-DD/data/Results_YYYY-MM-DD.csv
```
Then regenerate the xlsx from the cleaned CSV.

### Problem: check_urls.py shows "Error" for working URLs
**Fix:** Network timeouts happen. Re-run once. If it persists, check the URL manually in a browser. If it's live, mark URL_Status as "Verified" manually.

### Problem: Master database has schema drift (old columns from v1.0)
**Fix:** Say "clean [Name]'s database" — the master DB cleanup skill handles column mapping from any previous schema to the current 21-column standard.

### Problem: Too few results from ATS boards
**Possible causes:** Industry doesn't post heavily on Greenhouse/Lever/Ashby (finance, defense), search terms too narrow, location too restrictive.
**Fix:** Supplement with LinkedIn direct search links (Tab 3). Consider industry-specific boards (eFinancialCareers for finance, Cleared Jobs for defense).

### Problem: Friend isn't engaging with the emails
**Don't:** Add more features they didn't ask for.
**Do:** Ask one specific question ("Did the Anthropic role resonate? Too senior?"). Engagement comes from relevance, not volume.

---

## Quality Gates (Non-Negotiable)

Before any email goes out, these must be true:

1. **Every URL has been verified live** — check_urls ran inside CoWork. No dead links, no generic company pages.
2. **No LinkedIn URLs in Tab 1** — LinkedIn links go in Tab 3 only.
3. **Score and count in email match the spreadsheet** — if you say "13 jobs," there are 13 rows.
4. **Every URL contains a specific job ID** — no `jobs.ashbyhq.com/kernel` without a UUID. URL specificity is enforced at three layers: ONE_CLICK prompt, check_urls.py, and the master DB cleanup skill.
5. **Friend's name is correct everywhere** — email, xlsx tabs, subject line.
6. **Honest about limitations** — if a board returned zero, say so. If scoring isn't perfect, acknowledge it.

---

## Metrics to Track

| Metric | Where to find it | Why it matters |
|--------|-----------------|----------------|
| Jobs per search (pre-filter) | CoWork verification summary | Search breadth |
| Jobs scoring 70+ (post-filter) | Weekly CSV row count | Search quality |
| Exclusion rate (check_urls) | CoWork verification summary | Data quality |
| Generic URL rate | CoWork verification summary | Prompt quality |
| Time per delivery | Job_Search_Tracking.xlsx | Operational efficiency |
| Friend reply rate | Gmail | Service engagement |

---

## Skills to Build

Ordered by impact, not difficulty. Updated to reflect what's already been built (through Week 3).

### Tier 1: Build Now (Weeks 4-6)

**Python scripting fluency**
You've written check_urls.py, linkedin_links.py, verify_linkedin_removal.py, dashboard.py, and serve.py. You're past "can I write Python?" and into "can I build tools that solve real problems?" The next step is writing scripts from scratch without heavy guidance — taking a problem ("I need to deduplicate across two CSVs") and producing a working script in one sitting. Every script you build is portfolio evidence.

*Practice opportunity:* Run check_urls.py v2.1 against every friend's master database before next week's deliveries. Compare generic URL counts across users — do some friends have worse data quality than others? That pattern tells you which ONE_CLICK prompts need tightening.

**Prompt architecture for multi-step workflows**
ONE_CLICK v3.0 already chains search + URL verification + xlsx generation in one CoWork session. The next level is chaining more steps: SEARCH+VERIFY → CONSOLIDATE → FUNDING_INTEL → PACKAGE in a single prompt. Right now you're the glue between consolidation, funding intel, and packaging. The skill is designing prompts that hand off to each other.

*Practice opportunity:* Design a "FULL_PIPELINE_[Name].md" prompt that runs search + consolidation + funding intel in one CoWork session. Start with your own search where the stakes are low.

**Data quality systems thinking**
The Phil master database disaster (36 columns, two schemas, generic URLs) happened because data quality wasn't designed in from the start. The v3.0 architecture fixes this with 21 columns from birth and check_urls inside CoWork. The skill is anticipating the *next* data quality issue before it compounds. What happens when a friend's scoring weights change mid-stream? What if a new ATS board gets added?

*Practice opportunity:* Audit every friend's master database for v1.0 schema remnants. Use the cleanup skill to standardize them all to 21 columns before next week's consolidation runs.

### Tier 2: Build Weeks 6-8

**API integration (beyond Ashby GraphQL)**
Natural extensions: Google Sheets API (for the shared tracker you promised Phil), Gmail API (for programmatic newsletter scanning instead of CoWork), and Google Calendar API (for interview tracking if friends start applying).

*Practice opportunity:* Build a script that creates a Google Sheet from a friend's master database CSV and shares it with their email.

**HTML/CSS for email and web**
You're generating HTML emails and running a local web dashboard. Leveling up means modifying dashboard.html confidently — adding a chart, changing the layout, fixing a display issue without asking Claude to rewrite the whole file.

*Practice opportunity:* Add a "Funding Intel" section to the dashboard that displays recent matches from newsletter scans.

**Claude Code proficiency**
Make Claude Code your default for file operations, script debugging, and repo management. It can read your repo, run scripts, edit files, and commit to Git — all from one interface.

*Practice opportunity:* Do an entire operations run through Claude Code. Note where it's faster and where it's clunkier.

### Tier 3: Build Weeks 9-12 (Portfolio Polish)

**System documentation for public consumption**
Your repo goes public in Weeks 8-12. This playbook and your learning philosophy are written for you and Claude. They need to be rewritten for a hiring manager who has 90 seconds to understand what you built and why it matters.

**No-code/low-code tool evaluation**
Weeks 9-10 cover Zapier/Make/n8n. The skill isn't learning those tools — it's evaluating whether they solve a problem better than what you've already built.

**Interview storytelling**
Every system you've built is an interview answer. "Tell me about a time you built a process from scratch" → the job search pipeline. "How do you handle data quality issues?" → the Phil URL disaster and recovery. "How do you manage multiple stakeholders?" → the multi-user system with personalized configs.

---

## Claude Efficiencies

### Project Context (This Chat)

**Use project files strategically.** Your project files give Claude persistent context. When you update your system, update the relevant project file so every conversation starts with accurate context. Stale project files cause Claude to give outdated advice.

**Files to add as project files:**
- This playbook (WEEKLY_OPERATIONS_PLAYBOOK.md)
- The three SKILL.md files (delivery email, master DB cleanup, funding intel)
- FORMAT_SPEC.md (column schema)

**Files NOT to add:** Friend-specific ONE_CLICK files, weekly results, master databases. These change too often. Upload them per-conversation when needed.

### Conversation Patterns That Save Time

**"Check [X] chat for [Y]" works.** Claude can search past conversations. "Check the Phil verification chat for the clean database" is faster than re-explaining context.

**Front-load your intent.** "I need to run Phil's weekly search, clean his master database, add funding intel, and draft a delivery email. I have 45 minutes." Claude sequences the work and tells you what to do in parallel.

**Give Claude something to react to.** "I'm thinking xlsx with 3 tabs — does that make sense?" is faster than "What format should this be?"

### CoWork Efficiencies

**Batch searches across friends.** Open 2-3 CoWork tabs, kick off searches in parallel. Come back when all are done.

**Save executed prompts.** ONE_CLICK v3.0 saves the executed prompt with calculated dates. This is your audit trail.

**File path verification is built in.** The verification summary at the end of every ONE_CLICK run shows all files created with full paths.

### Claude Code Efficiencies

**Multi-file operations.** When updating all ONE_CLICK files to v3.0, Claude Code can read all files, make changes, and verify in one session.

**Debugging.** When check_urls.py throws an error, paste it into Claude Code. It reads your script and fixes the issue.

**Git operations.** Claude Code can stage, commit, and push — faster than switching to GitHub Desktop for routine commits.

### Memory and Context Management

**Claude remembers across conversations in this project.** Key decisions (LinkedIn removal, 21-column schema, URL specificity, pipeline reorder) persist through memory. You don't need to re-explain every session.

**Start sessions with state, not history.** "Phil's master database is clean (13 jobs, 21 columns). I need to run Aaron's search now." Current state, not the story of how you got there.

**When to start a new chat vs. continue.** New: different friend's work, different task type, sessions days apart. Continue: multi-step work on same deliverable, follow-up questions.

### Skill Triggers (Already Built)

Three custom skills are installed as project knowledge:

| Skill | Trigger phrase | What it does |
|---|---|---|
| Delivery email | "draft delivery email for [Name]" | 7-section email, tone principles, quality gates |
| Master DB cleanup | "clean [Name]'s database" | 21-column schema, URL specificity, dedup |
| Funding intel | "run funding intel for [Name]" | 4 newsletters, scoring, friend-specific filtering |

These eliminate re-explaining templates, schemas, and processes every session.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-02-26 | Initial playbook from Phil watershed delivery |
| v2.0 | 2026-03-01 | Pipeline reorder (check_urls inside CoWork), 21-column schema, Top 10 killed, parallel ops, skill triggers, simplified phases |

---

*This playbook reflects the process as of 2026-03-01.*
*Update it as the system evolves — this is a living document.*
