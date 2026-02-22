# FUNDING INTELLIGENCE: Proactive Company Prospecting

**Purpose:** Scan funding newsletters in Gmail to identify recently funded companies that match a user's target profile. Surfaces companies likely to hire BEFORE roles are posted.
**Runtime:** 5-10 minutes
**Prerequisites:** Access to Joey's Gmail, user profile (sectors, locations, role types)

---

## CONFIGURATION

**User:** [NAME]
**Target Sectors:** [FROM THEIR ONE_CLICK — e.g., fintech, AI/ML, defense, B2B SaaS]
**Target Locations:** [FROM THEIR ONE_CLICK — e.g., DC, NYC, Lisbon, Remote]
**Target Role Types:** [FROM THEIR ONE_CLICK — e.g., Chief of Staff, Partnerships, BD]
**Seniority Level:** [FROM THEIR ONE_CLICK — e.g., VP/Director, Senior Manager]

---

## STEP 0A: NEWSLETTER SCAN

Search Joey's Gmail for funding newsletters from the past 7 days. Scan ALL four sources:

### Source 1: StrictlyVC
**Search:** `from:connie@strictlyvc.com newer_than:7d`
**Format:** "[Company], a [age] [city] startup that [description], raised [amount] [round] led by [investors]."
**Extract per entry:** Company, City, Amount, Round Type, Sector (from description), Investors

### Source 2: FINSmes
**Search:** `from:info@finsmes.com newer_than:7d`
**Format:** "[Company], a [city]-based [description], raised/received [amount] in [round] funding"
**Extract per entry:** Company, City, Amount, Round Type, Sector (from description)

### Source 3: EU-Startups (Thomas Ohr)
**Search:** `from:thomas.ohr@eu-startups.com newer_than:7d`
**Format:** Organized by emoji-labeled categories (🤖 AI, 💰 VC/Funds, 🔋 GreenTech, 🍎 Health/BioTech, 🛰️ European News). Each entry: "[City]-based [Company] raised €[amount] to [description]."
**Currency:** Amounts in EUR — convert to USD at approximate current rate for consistency.
**Extract per entry:** Company, City/Country, Amount (EUR + USD equivalent), Round Type, Sector (from category header + description)
**Note:** Also extract any VC fund raises from the "💰 VC and Funds on the Move" section — these indicate which investors are deploying fresh capital and in which sectors.

### Source 4: Sunday CET (Dragos Novac)
**Search:** `from:sundaycet@mail.beehiiv.com newer_than:7d`
**Format:** Two parseable sections:
1. **"Signals" section** — structured deal listings organized by:
   - "Interesting early stage deals" — country flag emoji + company name + one-line description
   - "Big numbers" — country flag emoji + company name + amount
   - Deals organized by geography subsections (Nordics, UK, Germany, France, Netherlands, Other)
2. **"Market talk" section** — editorial with deals embedded in narrative. Look for patterns like "[Company] raised [amount]", "at [valuation]", "led by [investor]". Extract any specific deals mentioned.
3. **"Powder" section** — new VC fund raises (indicates fresh capital deployment)
4. **"Exits" section** — acquisitions and secondary transactions (indicates companies with fresh capital post-exit)

**Currency:** Amounts mix EUR and USD — normalize to USD.
**Extract per entry:** Company, Country, Amount, Round Type/Stage, Sector (from description), Lead Investor(s) if mentioned

---

## STEP 0B: BUILD MASTER FUNDING LIST

Combine all extracted companies from all 4 sources into a single list. Deduplicate (same company may appear in multiple newsletters — keep the entry with the most detail).

For each company, record:
| Field | Value |
|-------|-------|
| Company | Name |
| City/Country | Location |
| Amount | USD (converted if needed) |
| Round | Seed / Series A / Series B / etc. |
| Sector | Best classification from description |
| Source | Which newsletter(s) reported it |
| Lead Investor(s) | If mentioned |
| Description | One-line what they do |

---

## STEP 1: FILTER AGAINST USER PROFILE

Apply the following filters against the user's configuration. A company must match on **2 or more** of these criteria to be included:

1. **Sector match:** Company's sector overlaps with user's target sectors
2. **Location match:** Company is in or near user's target cities, OR company is known to hire remote
3. **Stage match:** Funding round suggests company is at a stage where they'd hire user's target role type (e.g., Series A+ likely hiring COS/BD, Seed may be too early for VP-level)
4. **Role signal:** Company description suggests they'd need someone with user's skill set (e.g., "go-to-market" → partnerships/BD, "scaling operations" → COS/ops)

**Strict filtering:** If a company matches on only 1 criterion, exclude it. This keeps signal high and noise low.

---

## STEP 2: SCORE AND RANK

For companies passing the 2+ filter, assign a relevance score 1-10:
- **9-10:** Perfect sector + location + stage + obvious role need
- **7-8:** Strong match on 3 criteria
- **5-6:** Solid match on 2 criteria
- **Below 5:** Should have been filtered out in Step 1

---

## STEP 3: OUTPUT

### Format: Funding Intelligence Report

**[NAME] — Funding Intelligence | Week of [DATE]**

**Sources scanned:** StrictlyVC ([X] editions), FINSmes ([X] editions), EU-Startups ([X] editions), Sunday CET ([X] editions)
**Total companies extracted:** [X]
**Companies passing filter (2+ criteria match):** [Y]

---

**TOP MATCHES (Score 7+):**

| Company | City | Amount | Round | Sector | Why Relevant | Score |
|---------|------|--------|-------|--------|-------------|-------|
| [Name] | [City] | [Amount] | [Round] | [Sector] | [1-sentence: how this maps to user's profile] | [Score] |

**WORTH WATCHING (Score 5-6):**

| Company | City | Amount | Round | Sector | Why Relevant | Score |
|---------|------|--------|-------|--------|-------------|-------|
| [Name] | [City] | [Amount] | [Round] | [Sector] | [1-sentence] | [Score] |

**VC FUND ACTIVITY (from EU-Startups "VC/Funds" + Sunday CET "Powder" sections):**
List any new VC fund raises that align with user's target sectors. These indicate which investors are actively deploying and may lead their portfolio companies to hire.

| Fund/Investor | Amount | Focus | Relevance |
|--------------|--------|-------|-----------|
| [Name] | [Amount] | [Sector/geo focus] | [Why this matters for user] |

---

**RECOMMENDED ACTIONS:**
1. [Top company] — Check their careers page for [role type]. Recently funded [round] companies typically post within 2-4 weeks.
2. [Company] — Monitor for [specific role]. Their [description] suggests they'll need [user's skill].
3. [Company] — Worth a proactive outreach. [Why timing is good].

---

## NOTES FOR JOEY

### When to run this:
- Every Sunday alongside weekly searches
- Takes 5-10 minutes
- Can run for any user — just swap the CONFIGURATION block

### Source frequency:
- StrictlyVC: ~4-5x/week (highest volume)
- FINSmes: Daily (broad coverage, US-heavy)
- EU-Startups: Weekly on Thursdays (European focus, clean structure)
- Sunday CET: Weekly on Sundays (European VC deep cuts, editorial + structured deals)

### Per-user relevance:
| User | Best sources | Why |
|------|------------|-----|
| Joey | All 4 | DC + Lisbon, broad sectors |
| Aaron | StrictlyVC + FINSmes | US hedge fund/TMT focus |
| Phil | All 4 | DC + London, partnerships |
| Vivienne | All 4 | NYC + DC, defensetech + European exposure |
| Rosalind | EU-Startups + Sunday CET | European D2C/brand strategy |

### Adding new sources:
To add a new newsletter, just add a new "Source N" block in Step 0A with:
- Gmail search query (from: address)
- Format description (how entries are structured)
- Extraction fields

The filter logic in Steps 1-2 is source-agnostic — it works on the combined master list regardless of origin.

---

*Created: 2026-02-19*
*Updated: 2026-02-22 — Added EU-Startups (thomas.ohr@eu-startups.com) and Sunday CET (sundaycet@mail.beehiiv.com)*
*Version: 2.0 — 4 newsletter sources*
