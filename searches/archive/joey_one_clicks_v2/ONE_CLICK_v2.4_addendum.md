# ONE_CLICK_v2.4_addendum.md — GM Lane Expansion

**Companion to:** `ONE_CLICK_v2.3.1_stage1_discovery.md` and `ONE_CLICK_v2.3_stage2_scoring.md`
**Purpose:** Extend Stage 1 discovery to surface International / Country Manager / Vertical GM roles that v2.3.1's nine role families miss.
**Status:** Drop-in additive update. No schema changes to corpus or Master CSV.

---

## What this adds

Three additive changes to v2.3.1 — none break existing behavior:

1. **Three new role families** added to the existing nine, bringing the family
   count to 12 (and the query budget from 108 to 144: 6 boards × 12 families ×
   2 anchors). Added: `international_gm`, `country_manager`, `vertical_gm`.
2. **Geographic anchor expansion** — Anchor B's location list expanded to
   include the new EMEA and LATAM cities/regions surfaced by the GM corpus
   expansion of 2026-05.
3. **Role family classifier rules** for Step 5 of Stage 1 to tag the new
   families correctly.

---

## CONFIGURATION (additive)

The MODE flag from v2.3.1 still applies. New role families respect MODE the
same way the existing nine do.

---

## NEW ROLE FAMILIES (queries)

Add to the role-families list in Stage 1 Step 1:

10. **`"general manager" OR "GM, EMEA" OR "GM, International"`** — Captures
    senior GM roles for region or international scope. Use this exact
    disjunction to avoid the false positives from "general manager" used in
    retail/restaurant/operations management contexts. The "GM, [Region]"
    pattern is the high-signal version.

11. **`"country manager" OR "head of country" OR "managing director, country"`** —
    Captures Country Manager / Country Lead roles, especially common at US
    companies expanding into single European or LATAM countries (Lisbon,
    Madrid, São Paulo, Mexico City).

12. **`"vertical GM" OR "industry GM" OR "head of industry" OR "GM, financial services"`** —
    Captures vertical/segment GM roles at SaaS companies hiring industry
    leaders (Financial Services, Healthcare, Manufacturing, Energy). Combine
    with stage 2 JD read to filter out roles that turn out to be sales-led
    rather than P&L-leading.

---

## EXPANDED ANCHOR B (geo-specific)

Replace the current Anchor B query template:

**OLD:**
```
[role] "remote" (Lisbon OR Portugal OR Europe OR LATAM OR "Latin America" OR
Brazil OR Mexico OR DC OR "Washington") 2026
```

**NEW:**
```
[role] "remote" (Lisbon OR Portugal OR Madrid OR Spain OR London OR UK OR
"United Kingdom" OR Dublin OR Ireland OR Berlin OR Amsterdam OR Europe OR
EMEA OR LATAM OR "Latin America" OR Brazil OR "São Paulo" OR Mexico OR
"Mexico City" OR Bogotá OR Colombia OR Buenos Aires OR Argentina OR DC OR
"Washington" OR Miami) 2026
```

**Why these locations:**
- **Lisbon, Madrid, London, Dublin, Berlin, Amsterdam:** Major European
  expansion hubs for US tech companies. Lisbon gets first place because
  Joey is moving there.
- **São Paulo, Mexico City, Bogotá, Buenos Aires:** Major LATAM expansion
  hubs. Brazil/São Paulo ranked first for Lusophone exposure.
- **Miami:** US-LATAM bridge city. Many companies post LATAM expansion
  roles here for Spanish-speaking US-based candidates.
- **DC, Washington:** Joey's home base, kept for completeness.

**Note:** The query exceeds Google's typical OR-clause practical limit (~10
items before result quality degrades). Anchor B is therefore split into two
sub-queries when running:
- **Anchor B-EMEA:** `[role] "remote" (Lisbon OR Portugal OR Madrid OR Spain OR London OR UK OR Dublin OR Ireland OR Berlin OR Amsterdam OR EMEA) 2026`
- **Anchor B-LATAM:** `[role] "remote" (LATAM OR Brazil OR "São Paulo" OR Mexico OR "Mexico City" OR Bogotá OR Buenos Aires OR Miami) 2026`

This makes the effective budget at MODE=both: 6 boards × 12 role families × 3
anchor variants (A + B-EMEA + B-LATAM) = 216 queries. Adjust accordingly:
- `both`: 216 queries
- `open_remote`: 72 queries (Anchor A only)
- `geo_locked`: 144 queries (B-EMEA + B-LATAM, no A)

If 216 is too much per run, fall back to the original two-anchor structure
with the expanded location list as a single Anchor B and accept some recall
loss on the longer OR clause. Document the choice in the run summary.

---

## ROLE FAMILY CLASSIFIER (Step 5 update)

Add three new tags. Each requires both a title-keyword match AND a seniority
signal (Director or above, or "Head of") to avoid false positives from
adjacent roles.

- **`international_gm`** — title contains:
  - "GM, EMEA", "GM, LATAM", "GM, International", "GM, Europe", "GM, APAC"
  - "General Manager, [Region]"
  - "Head of EMEA", "Head of LATAM", "Head of International", "Head of International Expansion"
  - "VP, EMEA", "VP, International", "Managing Director, [Region]"

- **`country_manager`** — title contains:
  - "Country Manager", "Country Lead", "Country Director"
  - "Head of [Country Name]" — e.g., "Head of Brazil", "Head of Portugal"
  - "Managing Director, [Country Name]"
  - "GM, [Country Name]"

- **`vertical_gm`** — title contains:
  - "Vertical GM", "Industry GM", "Segment GM"
  - "GM, [Vertical Name]" — e.g., "GM, Financial Services", "GM, Healthcare"
  - "Head of Industry", "Head of Vertical"
  - "VP, Industry [X]"
  - **Important:** Filter out "GM, Federal" / "GM, Public Sector" /
    "GM, Defense" / "GM, Government" — these fail Joey's international flex
    filter (DC-tethered, in-person federal stakeholder requirements). Tag
    these as `govt_defense` instead of `vertical_gm` so they get scored
    correctly against Joey's known constraints.

---

## STAGE 2 SCORING IMPLICATIONS

No changes to the rubric. But two practical notes for Stage 2 judgment:

### Combination Fit (Dimension 1b) — apply Signal 3 generously

The signal library Signal 3 is "Dual-geographic fluency as core ask (US-EU,
US-LATAM market entry/structuring)." For `international_gm` and
`country_manager` roles, this signal is almost always relevant if the role's
geographic scope matches Joey's bases (EMEA/LATAM/Lisbon).

Joey's combination is genuinely rare for these roles:
- US institutional credibility (DoD, JPM, SVB, Anzu)
- JD/MBA/MPP for regulated/legal/policy navigation
- Currently planning a Lisbon move (gives credibility on EMEA scope)
- Banking + VC + Government background for US-LATAM/EMEA bridging

When scoring `international_gm` or `country_manager` roles in target
geographies, default to 17-20 on Combination Fit unless the role has
specific filters Joey doesn't pass (e.g., "5+ years P&L ownership" hard
requirement).

### Builder Bonus — applies to GM "first in country" roles

`country_manager` and `international_gm` roles for US companies entering a
new market are almost always "first in role" / "build the function" /
"hire the team" type work. Builder Bonus should fire for these whenever
the JD signals stand-up-the-market scope, regardless of the company's
overall stage. A Series E company hiring a "Country Manager, Brazil" is
still a 0-to-1 builder role for that geographic surface.

---

## DISQUALIFIER LIST UPDATE

No new disqualifiers needed for the GM lane, but flag the existing
`govt_defense` filter for review:

For Joey's specific situation, GM roles in **Federal / Defense /
Public Sector** verticals at US companies should be auto-routed to
`pending_human_review` regardless of score, because the international
flex filter applies even when other dimensions are strong. These are not
disqualified outright — they remain valid if Daniel's international
posting timeline is 24+ months out — but they require human judgment that
the rubric can't make.

Add to `scripts/disqualifiers.json` under a new key:

```json
{
  "human_review_required": {
    "vertical_keywords": [
      "GM, Federal",
      "GM, Public Sector",
      "GM, Defense",
      "GM, Government",
      "Head of Federal",
      "Head of Public Sector"
    ],
    "rationale": "DC-tethered roles fail international flex filter. Surface for human judgment, not auto-include."
  }
}
```

---

## RUN ORDER WHEN BOTH v2.3.1 AND v2.4 ADDENDUM ARE ACTIVE

1. Stage 1 discovery: 12 role families × 6 boards × (1 to 3 anchors based on MODE)
2. Standard URL classifier, seniority gate, remote gate
3. Tag role family using the expanded classifier (12 tags + `other`)
4. Auto-grow corpus (no change)
5. Stage 2 scoring proceeds normally with the Combination Fit and Builder
   Bonus notes above as judgment guidance, not new rules

---

*v2.4 addendum, 2026-05-04. Adds GM lane to v2.3.1 without breaking changes.*
