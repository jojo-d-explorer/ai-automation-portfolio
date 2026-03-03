---
name: funding-intel
description: "Scan funding newsletters from Gmail and match recently funded companies to a friend's job search criteria. Use this skill whenever Joey asks to run funding intel, check funding newsletters, scan for recently funded companies, find funding matches, or generate a funding report — including phrases like 'run funding intel for [name]', 'check newsletters', 'scan StrictlyVC', 'funding matches for [name]', 'what companies just raised', or 'proactive prospecting'. Also trigger when Joey mentions StrictlyVC, FINSmes, EU-Startups, Sunday CET, or any funding newsletter in the context of job searching. This skill contains the Gmail search parameters, newsletter parsing rules, scoring criteria, and output format for the funding intelligence system."
---

# Funding Intelligence Skill

## When to Use
- Joey asks to run funding intel for any friend
- Joey asks to scan newsletters or check for recently funded companies
- Joey mentions StrictlyVC, FINSmes, EU-Startups, or Sunday CET
- Joey asks for "proactive prospecting" or "companies likely to be hiring"
- As part of the weekly delivery pipeline (Phase 5 in the operations playbook)

## The Idea

Companies that just raised funding are about to hire — often before jobs hit the boards. By scanning funding newsletters, we identify companies in a friend's target sector/location and flag them as "worth watching" or "apply proactively." This is the highest-value-add part of the service because friends can't easily do this themselves.

## Newsletter Sources (4 active)

| Source | Sender Email | Frequency | Coverage |
|--------|-------------|-----------|----------|
| StrictlyVC | connie@strictlyvc.com | ~4-5x/week | US/Global VC deals |
| FINSmes | info@finsmes.com | Daily | Global, all stages |
| EU-Startups | thomas.ohr@eu-startups.com | Weekly (Thu) | European startups |
| Sunday CET | sundaycet@mail.beehiiv.com | Weekly (Sun) | European tech ecosystem |

## Gmail Search Parameters

For each newsletter, search Gmail with:

```
StrictlyVC:   from:connie@strictlyvc.com newer_than:7d
FINSmes:      from:info@finsmes.com newer_than:7d
EU-Startups:  from:thomas.ohr@eu-startups.com newer_than:7d
Sunday CET:   from:sundaycet@mail.beehiiv.com newer_than:7d
```

Adjust `newer_than` window based on delivery frequency:
- Weekly deliveries: `newer_than:7d`
- Biweekly: `newer_than:14d`
- First run (catch-up): `newer_than:30d`

## Newsletter Parsing Rules

### StrictlyVC
- Format: Emoji-categorized sections (💰 = funding rounds, 🤝 = partnerships, 📊 = market data)
- Extract from 💰 sections: Company, Amount, Round (Seed/A/B/C/etc.), Sector, Location
- Ignore 🤝 and 📊 sections unless explicitly relevant to friend's search

### FINSmes
- Format: Individual articles per funding announcement
- Extract: Company, Amount, Round, Sector, Location, Lead Investor(s)
- Note: FINSmes covers all stages — filter to Series A+ for most friends unless they're targeting early-stage

### EU-Startups
- Format: Roundup articles with multiple deals per post
- Extract: Company, Amount, Round, Sector, Location (European focus)
- Note: Amounts often in EUR — convert to USD with approximate rate in parentheses

### Sunday CET
- Format: Newsletter with curated European tech news
- Extract: Funding mentions embedded in narrative sections
- Note: Less structured than others — extract what's clearly a funding announcement, skip opinion/analysis

## Scoring Criteria (per friend)

Score each funded company 1-10 based on relevance to the specific friend's search:

**Score 8-10 (Top Match):**
- Sector directly matches friend's target industries
- Location matches friend's target cities
- Company stage matches friend's target company size
- Round size suggests hiring at friend's level (Series B+ for senior roles)

**Score 5-7 (Worth Watching):**
- Sector is adjacent (e.g., friend targets fintech, company is payments infrastructure)
- Location is close but not exact (e.g., friend targets NYC, company is in Boston)
- Round is earlier than ideal but company is in a hot space

**Score 1-4 (Low Relevance):**
- Different sector, different location, wrong stage
- Include in the full dataset but don't highlight in the email

## Friend-Specific Filtering

Each friend has different targets. When running funding intel, reference their ONE_CLICK config for:

- **Target sectors** — only match companies in these industries
- **Target locations** — prioritize companies in these cities/regions
- **Target company stage** — Series A friends vs. Series C friends have different needs
- **Role-specific signals** — a company that just raised for "go-to-market expansion" is more relevant for a BD/Partnerships person than for an engineer

### Example: Phil Tassi
- Sectors: Defense tech, fintech, AI/ML, B2B SaaS, climate tech
- Locations: Washington DC, London UK, Remote
- Stage: Growth (Series B+)
- Signal: Partnerships, BD, Chief of Staff mentions in funding announcement

### Example: Aaron Kimson
- Sectors: Finance, fintech, hedge funds, asset management
- Locations: NYC, SF, Chicago, Miami, Boston
- Stage: Any (hedge funds don't follow traditional VC stages)
- Signal: Investment team expansion, new fund launches, AUM growth

## Output Format

### For Email Integration (Section 4 of delivery email)

```markdown
**💰 Funding Intelligence — [Date Range]**

Scanned [X] newsletters, [Y] total deals announced, [Z] matches for your search.

**Top Matches (Score 8-10):**
- **[Company]** ([Location]) — raised $[Amount] [Round] led by [Investor]
  - *Why it matters:* [1 sentence connecting to friend's background]
  - *Signal:* [What in the announcement suggests they're hiring your type of role]

**Worth Watching (Score 5-7):**
- **[Company]** ([Location]) — $[Amount] [Round]
  - *Relevance:* [Brief note]

**Fund Raises (deploying into your sectors):**
- **[VC Fund]** raised $[Amount] focused on [sector/stage]
  - *Implication:* Portfolio companies in [friend's target sector] will receive follow-on capital
```

### For Standalone Report (when running funding intel independently)

Save as CSV with columns:
```
Score | Company | Location | Amount | Round | Lead_Investor | Sector | Signal | Source | Date_Announced
```

Save to: `results/funding_intel/funding_matches_[Name]_YYYY-MM-DD.csv`

## Integration with Weekly Pipeline

Funding intel runs as Phase 5 in the operations playbook, AFTER search results are verified and cleaned. This ensures the email combines both concrete job listings AND proactive company intelligence.

**If running as part of delivery:**
1. Scan all 4 newsletters for the past 7 days
2. Score against the specific friend's config
3. Include Top Matches and Worth Watching in Section 4 of the delivery email
4. Include fund raises that deploy into friend's sectors

**If running standalone:**
1. Scan newsletters
2. Score against friend's config
3. Save standalone CSV report
4. Optionally email friend with just the funding intel

## Quality Checks
- Every company mentioned must have a source newsletter (no fabricated funding announcements)
- Amounts must be from the actual announcement (don't estimate or round)
- If a company appeared in multiple newsletters, note it (stronger signal)
- If a company from funding intel also appears in the job search results, flag it prominently ("They're already hiring!")
- Convert EUR amounts to USD with approximate rate noted

## Anti-Hallucination Rules
- Do not fabricate or estimate funding announcements. Every company, amount, round, and investor must come from an actual newsletter that was scanned.
- If Gmail search returns no newsletters for a source in the date range, report that source as "no issues found" — do not invent deals.
- If zero companies match a friend's criteria, say "no strong matches this week." Do not lower scoring thresholds to manufacture relevance.
- Do not guess amounts, rounds, or lead investors. If the newsletter didn't specify, use "Undisclosed" — not an estimate.
