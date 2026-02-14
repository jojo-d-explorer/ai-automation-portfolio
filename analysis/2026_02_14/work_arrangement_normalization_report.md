# Work Arrangement Normalization Report

**Generated:** 2026-02-14
**Source:** master_job_database.csv (118 jobs)
**Action:** Standardized Work_Arrangement field from 3 values to 5 granular categories

---

## Before Standardization

| Value | Count |
|-------|-------|
| Remote | 89 |
| In-Office | 23 |
| Hybrid | 6 |
| **Total unique values** | **3** |

The 89 "Remote" jobs included a wide range: US-only remote, Americas remote, EMEA remote, global remote, and even one that was actually hybrid. No way to distinguish a Remote-US job from a Remote-EMEA job without reading the Location field.

---

## After Standardization

| Value | Count | % | Description |
|-------|-------|---|-------------|
| Remote-Global | 54 | 45.8% | Remote with no US/Americas qualifier, or explicitly global/EMEA/other |
| Remote-US | 29 | 24.6% | Remote with US location indicators (state, city, or "US/USA") |
| In-Office | 23 | 19.5% | Physical office required (unchanged) |
| Hybrid | 7 | 5.9% | Mix of remote and in-office (1 reclassified from Remote) |
| Remote-Americas | 5 | 4.2% | Remote covering Americas region (US + Canada + LATAM) |
| **Total unique values** | **5** | | |

---

## Standardization Rules Applied

### Remote → Remote-US (28 jobs + 1 edge case fix = 29 jobs)
Location contained US indicators: "US", "USA", "U.S.", "United States", "US East", "NYC", "New York", "Manhattan", "SF", "San Francisco", "LA", "Washington", "DC", or "hub in NY"

Examples of Location values mapped to Remote-US:
- "Remote - US" → Remote-US
- "US East Coast" → Remote-US
- "Remote - USA" → Remote-US
- "Remote U.S." → Remote-US
- "United States Remote" → Remote-US
- "SF or Remote" → Remote-US
- "NYC/LA/SF Remote" → Remote-US
- "Remote NYC/LA" → Remote-US
- "Remote (hub in NY)" → Remote-US (edge case: required adding "NY" pattern)
- "New York City" (with WA=Remote) → Remote-US
- "United States" → Remote-US

### Remote → Remote-Americas (5 jobs)
Location contained Americas indicators: "Americas", "Canada", "Mexico", "LATAM"

Specific jobs:
- Jeeves | "Remote - Americas" → Remote-Americas
- KOHO | "Remote - Canada" → Remote-Americas
- dLocal | "Mexico City - Remote" → Remote-Americas
- Binance | "Mexico City - Remote" → Remote-Americas
- Tala | "Mexico City - Remote" → Remote-Americas

### Remote → Remote-Global (54 jobs)
Location was generic "Remote" with no geographic qualifier, or explicitly non-US: "Remote EMEA", "Remote Europe", "Remote Philippines", "Remote Munich HQ", "Paris Oxford Remote"

### Remote → Hybrid (1 job)
- Crypto.com | "Remote/Hybrid" → Hybrid (reclassified from Remote to Hybrid)

### Hybrid → Hybrid (6 jobs, unchanged)
Already correctly tagged: Washington DC, Mexico City - Hybrid, New York Remote Hybrid, London UK, Mexico City, Paris/New York

### In-Office → In-Office (23 jobs, unchanged)
Already correctly tagged for Paris, Vienna, Manila, Manhattan, and other physical locations

---

## Validation

| Check | Result |
|-------|--------|
| Total rows before | 118 |
| Total rows after | **118** |
| Rows changed | 89 |
| Rows unchanged | 29 |
| Sort order (score descending) | **Maintained** |
| All other fields | **Unchanged** |
| Unexpected WA values | **None** |
| All WA values in allowed set | **Yes** |

### Allowed values: Remote-US, Remote-Americas, Remote-Global, Hybrid, In-Office

No N/A values remain — every job now has a classified work arrangement.

---

## What This Enables

With standardized work arrangements, you can now:

1. **Filter by geographic accessibility.** Remote-US (29 jobs) is your primary target pool. Remote-Americas (5) and Remote-Global (54) have timezone considerations.

2. **Score correlation analysis.** Does Remote-US score higher than Remote-Global? (Hypothesis: yes, because the scoring model rewards US alignment.)

3. **Search parameter tuning.** If Remote-Global produces lower average scores, future searches can narrow to Remote-US + Remote-Americas.

4. **Application prioritization.** Remote-US jobs have the fewest barriers to application. In-Office (23) and some Remote-Global jobs may have location requirements that create friction.

---

## Quick Score Check by Normalized Category

| Category | Count | Avg Score | 80+ Jobs |
|----------|-------|-----------|----------|
| Remote-US | 29 | 83.8 | 20 |
| Remote-Americas | 5 | 77.2 | 1 |
| Remote-Global | 54 | 66.7 | 19 |
| Hybrid | 7 | 73.4 | 1 |
| In-Office | 23 | 46.3 | 1 |

Remote-US produces the highest average score (83.8) with the densest concentration of 80+ jobs (20 of 29 = 69%). Remote-Global's average is dragged down by the Jan 26 batch's low-scoring entries. In-Office averages just 46.3 — confirming that non-remote roles are overwhelmingly poor fits.

---

*Normalization applied to 118 jobs. Work_Arrangement field now uses 5 standardized categories. All other fields unchanged. Sort order by score descending maintained.*
