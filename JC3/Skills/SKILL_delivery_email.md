---
name: job-search-delivery
description: "Draft weekly job search delivery emails for friends. Use this skill whenever Joey asks to draft, write, compose, or create a delivery email, results email, or update email for any friend in the job search service — including Aaron, Phil, Vivienne, Rosalind, or any new friend. Also trigger when Joey says 'email [name]', 'send [name] results', 'package for [name]', 'draft for [name]', or mentions delivering weekly search results. This skill contains the proven email structure, tone principles, and section templates that produced the Phil Tassi 02-26-2026 benchmark delivery."
---

# Job Search Delivery Email Skill

## When to Use
- Joey asks to draft/write/compose a delivery email for any friend
- Joey says "email [name]", "send [name] results", "package for [name]"
- Joey mentions delivering weekly search results to a friend
- Joey asks to create an email with job search findings

## Email Architecture (7 Sections)

Every delivery email follows this structure. Adapt section depth based on whether it's a first-run (Week 1) or recurring (Week 2+) delivery.

### Section 1: Opener + Headline Role
- Personal, warm, 2-3 sentences max
- Lead with the single most compelling role (score, company, why it fits)
- Include the verified job count and the fact that all links are confirmed live

**Example opener:**
"This week's search is in — 13 verified, confirmed-open listings across Greenhouse, Lever, and Ashby. Every link has been checked and is live."

### Section 2: Quick Stats
- Verified open roles count
- Score range and average
- Boards searched
- Roles searched
- Locations searched

### Section 3: Top Roles (3-5 highlighted)
For each role include:
- **Company** — Job Title (Score, Location, Work Arrangement)
- 1-2 sentences on why it fits this specific person's background
- Note if it's new this week or a persistent listing (Times_Seen > 3 = "actively hiring")

End with "Also worth a look:" for roles 6-8 in one sentence.

### Section 4: Funding Intelligence (if available)
- Top 3-5 matches (Score 7+) with company, location, amount, round, and relevance
- "Worth Watching" tier for score 5-6 companies
- VC fund raises deploying into adjacent sectors
- Frame as "companies likely hiring before jobs hit the boards"

### Section 5: System Notes (honest, transparent)
- What changed in the pipeline this week
- Any known limitations or caveats
- Mea culpa if previous deliveries had issues (dead links, stale data)
- Frame improvements as "here's what I fixed and why"

### Section 6: Coming Soon / Roadmap
- 2-3 features in development
- Frame as learning-by-doing projects
- Invite input on which features matter most

### Section 7: Feedback Ask
- Specific questions about roles, companies, boards, newsletters
- Recap current search criteria so friend can verify
- "The system gets smarter each week — your feedback is what makes the difference"

## Tone Principles
- **Honest about limitations** — calling out what doesn't work builds trust faster than overselling
- **Suggestions as questions** — "Should I add eFinancialCareers?" not "I'm adding eFinancialCareers"
- **Lead with the most interesting finding** — not the most data
- **Personal context in role highlights** — connect role requirements to friend's specific resume experience
- **Don't overload** — 3-5 highlighted roles, not 13. The spreadsheet has the full list.

## First-Run vs. Recurring

### First Run (Week 1)
- Include "How the system works" explanation (boards searched, scoring methodology)
- Frame as "calibration run" — invite feedback on whether scoring feels right
- No analysis section (not enough data)
- Include archetype explanation if friend has broad search parameters
- Ask about deal-breakers and adjustments

### Recurring (Week 2+)
- Skip system explanation (they know how it works)
- Lead with what's new vs. repeat
- Include analysis if Week 3+ (score trends, sector breakdown)
- Reference previous feedback if they gave any
- Highlight persistent listings (high Times_Seen = strong hiring signal)

## Attachment Checklist
Remind Joey to attach:
- [ ] xlsx spreadsheet (3 tabs: All Results, Search Summary, LinkedIn Search Links)
- [ ] Dashboard screenshots (if captured)
- [ ] Master database CSV (clean, verified)
- [ ] Analysis PDF (Week 3+ only)

## Output Format
Generate the email as an HTML file that Joey can open in a browser and copy-paste into Gmail. Include:
- Yellow instruction box at top with Subject line, To, Attachments, and "How to use" instructions
- Bordered email content below that's copy-pasteable
- Section headers with emoji markers (📊 ⭐ 💰 🔧 🚀 💬)

## Quality Gates
Before presenting the draft to Joey:
- Job count and score range in email text must match the actual data
- Every company/role mentioned must exist in the attached spreadsheet
- Every URL in the spreadsheet contains a specific job ID (numeric or UUID path segment) — no generic company careers pages (e.g., `jobs.ashbyhq.com/kernel` is NOT a valid job listing)
- Friend's name must be correct throughout
- No placeholder text or [FILL IN] markers left behind

## Anti-Hallucination Rules
- Do not fabricate or estimate job listings. If a search returned zero results for a board/role/location combination, report zero — do not create placeholder entries.
- Do not invent company names, job titles, scores, or URLs. Every data point in the email must trace back to actual search results or newsletter content.
- If funding intel scanning found no matches, say "no strong matches this week" — do not fabricate funding announcements.
- If the data seems thin (e.g., only 3 jobs found), deliver 3 jobs honestly. A small honest delivery builds more trust than a padded one.
