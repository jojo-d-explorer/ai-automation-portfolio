# FUNDING INTELLIGENCE — Proactive Company Prospecting

*Standalone prompt. Run anytime for any person. Also integrated into MASTER_ANALYSIS as Analysis 6.*

---

## CONFIGURATION

**Person:** [FRIEND_NAME]
**Target roles:** [e.g., Chief of Staff, Head of Partnerships, Director of Strategy]
**Target sectors:** [e.g., defense tech, AI/ML, fintech, B2B SaaS]
**Target locations:** [e.g., Washington DC, Remote-US, NYC, Lisbon/EU-Remote]
**Seniority level:** [e.g., Director/VP/C-suite → Series B+ or $30M+]
**Network context (optional):** [e.g., "Connected to Anzu Partners portfolio", "JPM alumni network", "DoD ecosystem"]

---

## STEP 1: GMAIL SCAN

Search my Gmail for funding newsletter emails received in the last 7 days:

1. **StrictlyVC**: from:connie@strictlyvc.com
   - Look for sections labeled: "Massive Fundings", "Big-But-Not-Crazy-Big Fundings", "Smaller Fundings"
   - Also check: "New Funds", "Exits", "Going Public" (for market context)

2. **FINSmes**: from:info@finsmes.com
   - Look for: All entries under "FROM FINSMES.COM" organized by country
   - Also check: "MERGERS AND ACQUISITIONS" (signals active sectors)

From each email, extract ALL funding announcements into a working list:
- Company name
- Location (city, country)
- What they do (1 sentence)
- Stage (Pre-Seed / Seed / Series A / B / C / D+)
- Round size (USD — convert if in EUR/GBP using approximate rates)
- Key investors (lead investor at minimum)
- Source (StrictlyVC / FINSmes / both)

Deduplicate across sources. If a company appears in both, merge the entries and note "both" in source.

Show me the total count: "Found [X] funding announcements across [Y] newsletter emails this week."

---

## STEP 2: STRICT FILTER

Cross-reference the funding list against [FRIEND_NAME]'s criteria above.

**A company must match 2 OR MORE of these criteria to pass the filter:**

### Criterion 1: SECTOR MATCH
Company operates in one of [FRIEND_NAME]'s target sectors, or in an adjacent sector where their skills clearly transfer.
- Direct match = strong signal
- Adjacent match = note the connection explicitly (e.g., "AI infrastructure — adjacent to your AI/ML target")

### Criterion 2: LOCATION MATCH
Company is based in one of [FRIEND_NAME]'s target locations, OR:
- Is known to hire remote in relevant geographies
- Has a secondary office in a target location
- Is headquartered elsewhere but the role type typically sits in a target city (e.g., a SF company that would base its DC government relations team in DC)

### Criterion 3: STAGE MATCH
Company is at a growth stage where [FRIEND_NAME]'s target roles typically get created:
- C-suite / VP roles → Series B+ or $30M+ total raised
- Director / Head-of roles → Series A+ or $15M+ total raised
- Manager / Senior IC roles → Seed+ or $5M+ total raised
- Use the seniority level from CONFIGURATION to determine threshold

### Criterion 4: INVESTOR SIGNAL
Backed by a top-tier firm known for helping portfolio companies build strong leadership teams.
- Tier 1 signal: a16z, Sequoia, Founders Fund, Lightspeed, Accel, General Catalyst, Benchmark, Index, Bessemer, NEA, GIC, Thrive Capital, Iconiq
- Tier 2 signal: Y Combinator, First Round, Felicis, Greylock, Sapphire, Eclipse, Khosla
- Use judgment for firms not listed — the question is "does this investor actively help with exec hiring?"

---

## STEP 3: OUTPUT

### If 0 companies pass the filter:

```
No freshly funded companies this week matched 2+ of [FRIEND_NAME]'s criteria.

This is normal with strict filtering — it means only genuinely relevant companies surface.
The newsletters contained [X] total announcements; none cleared the bar this week.

Check again next week, or loosen to 1 criterion if you want broader coverage.
```

### If 1+ companies pass the filter:

**Present as a ranked table (highest relevance first):**

| # | Company | What They Do | Round | Location | Criteria Matched | Why Relevant |
|---|---------|-------------|-------|----------|-----------------|-------------|
| 1 | [Name] | [1 sentence] | [Stage, $Amount] | [City] | [e.g., Sector ✓ Stage ✓] | [Specific rationale tied to FRIEND_NAME's background] |

**For each company in the table, recommend an action:**

- 🔍 **MONITOR** — Just raised; roles likely not posted yet. Check their careers page in 2-4 weeks. Set a reminder.
- 📨 **REACH OUT** — At a stage where they'd need [FRIEND_NAME]'s role type now. Draft a brief proactive outreach email to the founder/COO/Head of People.
- 🔗 **NETWORK** — A warm intro path likely exists through [specific network from CONFIGURATION]. Identify the connection.

**Format each recommendation as:**
```
[Company Name] → [ACTION EMOJI + LABEL]
Timing: [Now / 2-4 weeks / When they post]
Suggested entry point: [Who to contact — title, not name]
Connection path: [If NETWORK — how to get introduced. If none, say "Cold outreach — use LinkedIn."]
```

---

### PATTERN NOTES (include if useful):

- Sectors showing repeated funding activity this week (market momentum signals)
- Companies appearing in BOTH funding newsletters AND previous job search results (double signal — flag prominently)
- Geographic clusters (e.g., "3 defense tech companies raised in DC this week")
- Investor patterns (e.g., "a16z backed 3 companies in your target sectors this week")

---

## STEP 4: SAVE OUTPUT

Save the complete analysis to:
`/Users/jc3/GitHub/ai-automation-portfolio/results/funding_intel/[FRIEND_NAME]_funding_intel_[TODAY'S DATE].md`

Create the `funding_intel/` folder if it doesn't exist.

Confirm the file was saved and show the file path.

---

## QUICK-START EXAMPLES

### For Joey (personal search):
```
Person: Joey Clark
Target roles: Chief of Staff, Head of Strategic Operations, Head of Partnerships
Target sectors: defense tech, AI/ML, fintech, B2B SaaS, gov tech
Target locations: Washington DC, Remote-US, Lisbon, EU-Remote
Seniority level: Director/Head-of (Series A+ / $15M+)
Network context: Anzu Partners portfolio companies and LP network; JPM startup banking alumni; DoD innovation ecosystem contacts
```

### For Aaron:
```
Person: Aaron Kimson
Target roles: Equity Research Analyst, Portfolio Manager, Investment Analyst
Target sectors: hedge funds (L/S equity), asset management, fintech, financial data
Target locations: NYC, Stamford/Greenwich CT, Remote-US
Seniority level: VP/Director (Series B+ / $30M+)
Network context: JMP Securities / Citizens coverage network
```

### For a new friend (template):
```
Person: [NAME]
Target roles: [ROLES]
Target sectors: [SECTORS]
Target locations: [LOCATIONS]
Seniority level: [LEVEL] ([STAGE THRESHOLD])
Network context: [NETWORKS — or "None specified"]
```

---

## HOW THIS CONNECTS TO MASTER_ANALYSIS

When running the full MASTER_ANALYSIS (for people with 2+ weeks of data), this prompt's logic is embedded as Analysis 6. The difference:

- **Standalone (this file):** Self-contained. Own config. Run anytime for anyone.
- **Inside MASTER_ANALYSIS:** Pulls config from the existing CONFIGURATION block. Runs automatically as part of the 6-analysis sequence. Output folds into the Strategic Summary under "PROACTIVE TARGETS."

You don't need to run both — if you're running MASTER_ANALYSIS with the Analysis 6 insert, it handles everything. Use this standalone version for:
- First-run intelligence (before their first job search)
- Mid-week checks ("anything new funded in Aaron's space?")
- Quick scans for people not yet in the full analysis pipeline

---

*Created: February 18, 2026*
*Sources: StrictlyVC (connie@strictlyvc.com, ~4-5x/week), FINSmes (info@finsmes.com, daily)*
*Filter: Strict (2+ criteria match required)*
