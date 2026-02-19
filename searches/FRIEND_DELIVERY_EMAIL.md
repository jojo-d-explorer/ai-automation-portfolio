# FRIEND DELIVERY EMAIL TEMPLATES

*Standardized email templates for delivering weekly search results to friends.*
*Based on tested format (Rosalind, Phil, Aaron deliveries — Feb 2026).*

---

## COWORK PROMPT — AUTO-GENERATE DELIVERY EMAIL

**When to run:** After completing ONE_CLICK search + MASTER_ANALYSIS + FUNDING_INTEL for a friend.

**What to attach/provide to CoWork:**
- The friend's Top10 and Master List results (the .xlsx or .csv files from this week's search)
- The analysis output (if Week 2+)
- The funding intel output (if you ran it)
- This file (FRIEND_DELIVERY_EMAIL.md)

**Paste this into CoWork:**

```
Using the attached search results, analysis, and funding intel for [FRIEND_NAME], generate their delivery email.

Reference the template structure in FRIEND_DELIVERY_EMAIL.md.

Pick the correct variant:
- If this is their FIRST search ever → use Variant A (First-Run Delivery)
- If they have previous weeks of results → use Variant B (Weekly Update)

Fill in every bracketed placeholder using actual data from the attached files:
- Pull scores, counts, averages, and highlighted roles from the search results
- Pull strategic insights from the analysis output
- Pull company matches from the funding intel output
- Write the "honest notes" and "what stood out" sections based on what you observe in the data

Output the completed email as an HTML file saved to:
/Users/jc3/GitHub/ai-automation-portfolio/results/[FRIEND_NAME]/delivery_email_[DATE].html

The HTML should be formatted for direct paste into Gmail:
- Use Arial 14px font
- Bold section headers (not markdown asterisks)
- Clean bullet lists with proper indentation
- No red placeholder text remaining — everything should be filled in
- Keep the same section structure and tone from the template

After saving, show me a preview of the email content so I can review before sending.
```

---
---

## TEMPLATE REFERENCE — VARIANT A: FIRST-RUN DELIVERY (Week 1)

**Use when:** Friend's very first search results are ready
**Attachments:** Top10_[Name].xlsx + Master_List_[Name].xlsx
**Subject line:** Your first job search results are in — Top 10 + Master List attached

---

### Structure & Content

**1. OPENER**

Hey [FIRST_NAME],

Your first weekly search just ran and I've attached two files: the **Top 10 New Opportunities** (the best finds this week) and the **Master List** (everything that scored 70+ out of 100). Both are formatted Excel files — you can sort, filter, and dig into whatever catches your eye.

Here's how this first run went.

---

**2. THE NUMBERS**

I searched across [NUMBER] job boards ([LIST BOARDS]) using your target titles — [LIST TITLES] — filtered for [LOCATION FILTER]. About [TOTAL RAW] jobs came back before filtering. After scoring against your resume and applying the 70+ threshold, **[FINAL COUNT] jobs made the cut**, with scores ranging from [LOW] to [HIGH] and an average of [AVG].

---

**3. HOW SCORING WORKS (first-run only)**

Every job gets scored out of 100 based on the priorities you gave me. Since you ranked [#1 PRIORITY] first, that carries the most weight ([X] points) — [1-2 sentences explaining how #1 priority is applied]. [#2 PRIORITY] is your #2 ([X] points), so [1-2 sentences on how it's applied]. [#3 PRIORITY] is #3 ([X] points) — [brief explanation]. [REMAINING PRIORITIES] round out the last [X] points. Each job has a Score Rationale column explaining exactly why it scored where it did.

---

**4. WHAT STOOD OUT**

Your top result is a **[TITLE]** role at [COMPANY] ([SCORE]) — [1-2 sentences on why it's a strong match and any caveats].

Additional highlights:
- **[COMPANY]** ([SCORE]) — [Why it fits + any flags]
- **[COMPANY]** ([SCORE]) — [Why it fits + any flags]
- **[COMPANY]** ([SCORE]) — [Why it fits + any flags]

---

**5. HONEST NOTES**

[Include 1-3 observations about search limitations or market patterns. Examples:]
- Title X returned zero direct results — the market uses different language for that work. We're covering it with Title Y and Z.
- Location X's startup ecosystem skews toward Sector A, so the strongest pipeline comes from Remote roles at companies in Sector B.
- Most jobs don't list salary — only X of Y included compensation info. We score conservatively when salary is missing.

---

**6. FUNDING INTEL (optional — include if FUNDING_INTEL was run)**

I also scanned this week's funding newsletters (StrictlyVC + FINSmes — about [X] announcements total) and filtered for companies that match your profile. [NUMBER] passed:

- **[COMPANY]** ([CITY]) just raised [AMOUNT] [ROUND] backed by [KEY INVESTORS]. [1 sentence on relevance]. [Suggested action].
- **[COMPANY]** ([CITY]) raised [AMOUNT] from [INVESTOR]. [Relevance + action].
- **[COMPANY]** ([CITY]) raised [AMOUNT]. [Relevance + action].

For [TOP 1-2 COMPANIES] especially — it might be worth reaching out directly to see if they have openings, even if nothing's posted yet. Companies right after a raise are often hiring before roles hit the boards.

---

**7. WHAT HAPPENS NEXT + FEEDBACK**

I'll run this same search again on Sunday. The system will compare against this week's results and mark jobs as NEW or REPEAT — repeat jobs are actually a strong signal (companies that keep posting are actively hiring, not just filling a pipeline). After two weeks of data I'll also generate a strategic analysis: score distributions, sector breakdowns, company hiring patterns, and recommendations based on the trends.

**This gets better with your feedback.** The first search is calibration — now I need to hear from you:

- Do the scores feel right? Are the [80+] jobs actually the ones you'd click on?
- Should I weight [RELEVANT PRIORITY] even higher, or are you open to [ADJACENT CATEGORY]?
- Any of these companies excite you or feel off? That helps me tune.
- Want me to add any supplementary boards? [SUGGEST 1-2 IF APPLICABLE]
- Are titles like "[ADJACENT TITLE]" in your strike zone, or should I narrow to [CORE TITLES]?

Happy to change anything — the scoring weights, the title list, the location filters, the industry preferences. Just tell me what felt right and what didn't, and next week's search will be sharper.

Talk soon,
Joey

---
---

## TEMPLATE REFERENCE — VARIANT B: WEEKLY UPDATE (Week 2+)

**Use when:** Friend already has at least one week of results
**Attachments:** Top10_[Name].xlsx + Master_List_[Name].xlsx + Analysis_[Name].pdf (if 2+ weeks)
**Subject line:** Week [N] Search Results [+ Strategic Analysis]

---

### Structure & Content

**1. OPENER + HEADLINE**

Hey [FIRST_NAME],

This week's search is in — **[TOTAL] jobs found, [NEW COUNT] new**. Top 10 new roles attached, plus your updated master list.

[1-2 SENTENCE HEADLINE FINDING — the single most interesting thing this week.]

---

**2. QUICK STATS**

- [NEW COUNT] new jobs (not seen before)
- [REPEAT COUNT] repeat jobs (persistent hiring signal)
- [TOTAL MASTER] total in your master database
- Score range this week: [LOW]–[HIGH], average [AVG]
- [ANY OTHER NOTABLE STAT]

---

**3. TOP NEW ROLES**

- **[COMPANY]** — [TITLE] ([SCORE]). [Why it fits + any caveats]
- **[COMPANY]** — [TITLE] ([SCORE]). [Why it fits + any caveats]
- **[COMPANY]** — [TITLE] ([SCORE]). [Why it fits + any caveats]

---

**4. STRATEGIC ANALYSIS (optional — include if analysis PDF is attached)**

Now that we have [N] weeks of data, I ran a full analysis. The big takeaways:

- [KEY INSIGHT 1]
- [KEY INSIGHT 2]
- [KEY INSIGHT 3]

The full report has score distributions, sector breakdowns, company hiring patterns, and geographic analysis. Worth a 5-minute read if you want to sharpen your focus.

---

**5. FUNDING INTEL (optional — include if FUNDING_INTEL was run)**

- **[COMPANY]** ([CITY]) — [AMOUNT] [ROUND]. [1 sentence relevance + action].
- **[COMPANY]** ([CITY]) — [AMOUNT] [ROUND]. [Relevance + action].

---

**6. CLOSE**

If certain roles or companies aren't landing, just let me know and I'll tune the search. The system gets smarter each week.

Best,
Joey

---
---

## QUICK REFERENCE

### What to attach

| Delivery Type | Attachments |
|---|---|
| First run (Week 1) | Top10_[Name].xlsx + Master_List_[Name].xlsx |
| Weekly (Week 2, no analysis) | Top10_[Name].xlsx + Master_List_[Name].xlsx |
| Weekly (Week 2+, with analysis) | Top10_[Name].xlsx + Master_List_[Name].xlsx + Analysis_[Name].pdf |

### Tone notes

- **Personal opener:** Warm but brief. Match their energy.
- **Honest notes:** Don't oversell. Calling out limitations builds trust.
- **Funding intel:** Frame as "worth watching" not "you should apply."
- **Feedback ask:** Critical for first 2-3 weeks. After that, only if making changes.

### HTML formatting spec (for CoWork output)

CoWork generates the HTML file with these specs so it pastes cleanly into Gmail:
- Font: Arial, 14px, #222 text color
- Section headers: Bold, same size as body text (not larger)
- Bullet lists: Standard HTML ul/li with 24px left padding
- Line height: 1.6
- Max width: 680px
- No background colors, borders, or styling that Gmail strips

---

*Created: 2026-02-19*
*Based on: Rosalind first-run delivery, Phil Week 3 delivery, Aaron/Phil analysis teasers*
