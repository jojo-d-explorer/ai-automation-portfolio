# Analysis 4: Search Evolution & Volume Tracking

**Generated:** 2026-02-14
**Source:** master_job_database.csv (119 jobs across 3 batches)
**Purpose:** Track how search quality is evolving and forecast next batch parameters

---

## 1. Batch Breakdown

| Batch | Jobs | % of Total |
|-------|------|------------|
| Week_of_2026-01-26 | 57 | 47.9% |
| Week_of_2026-02-02 | 18 | 15.1% |
| Week_of_2026-02-09 | 44 | 37.0% |
| **Total** | **119** | **100%** |

Zero overlap between batches — every batch found entirely new jobs. No duplicate URLs or Company+Title combos appeared across batches.

---

## 2. Quality Metrics by Batch

### Jan 26 Batch (57 jobs) — The Raw Baseline

| Metric | Value |
|--------|-------|
| Scored | **0 of 57** (0%) |
| Avg score | N/A |
| Remote % | 60% (34 of 57) |
| Target sector % | 0% (all untagged) |
| CoS roles | 4 (7%) |
| Partnerships roles | 22 (39%) |
| Work arrangements | All N/A (untagged) |
| Geographic spread | Remote 34, Paris 11, Vienna 4, Philippines 3, NYC 2, UK 1 |
| Job boards | Ashby 25, Greenhouse 16, Lever 16 |

**Character:** A wide-net first search. Heavy on partnerships roles (39%) but scattered geographically. Significant European/APAC presence (Paris 11, Vienna 4, Philippines 3). No scoring or sector tagging applied.

### Feb 2 Batch (18 jobs) — The Scoring Starts

| Metric | Value |
|--------|-------|
| Scored | **18 of 18** (100%) |
| Avg score | **73.6** |
| Score tiers | 90+: 0 / 80-89: 1 / 70-79: 17 |
| Remote % | 67% (12 of 18) |
| Target sector % | 89% (16 of 18) |
| CoS roles | 10 (56%) |
| Partnerships roles | 1 (6%) |
| Work arrangements | Remote 12, In-Office 3, Hybrid 3 |
| Geographic spread | Remote 12, NYC 2, LATAM 2, SF 1, UK 1 |
| Job boards | Ashby 7, Greenhouse 7, Lever 4 |
| Top sectors | Fintech 5, AI/Speech Tech 1, Insurtech 1 |

**Character:** A dramatic pivot to CoS roles (56%, up from 7%) and target sectors (89%). Volume dropped sharply (57 → 18) but every job was scored. The problem: scores clustered low — 17 of 18 in the 70s, with zero 90+ matches. This batch found the *right type* of job but not the *best quality* matches.

### Feb 9 Batch (44 jobs) — The Breakthrough

| Metric | Value |
|--------|-------|
| Scored | **44 of 44** (100%) |
| Avg score | **86.5** |
| Score tiers | 90+: **10** / 80-89: 30 / 70-79: 4 |
| Remote % | **93%** (41 of 44) |
| Target sector % | 57% (25 of 44) |
| CoS roles | 19 (43%) |
| Partnerships roles | 13 (30%) |
| Work arrangements | Remote 43, Hybrid 1 |
| Geographic spread | Remote 41, US general 1, NYC 1, DC 1 |
| Job boards | Ashby 17, Greenhouse 16, Lever 11 |
| Top sectors | Health Tech 4, AI/Tech 3, Crypto/Fintech 2, Fintech/Fraud Prevention 2 |

**Character:** The best batch by every metric. Average score jumped 13 points (73.6 → 86.5). Produced all 10 of the database's 90+ matches. Near-perfect remote concentration (93%). Balanced CoS (43%) and partnerships (30%) roles. Geographic scatter essentially eliminated.

---

## 3. Search Parameter Evolution

### What changed between batches

| Dimension | Jan 26 | Feb 02 | Feb 09 |
|-----------|--------|--------|--------|
| **Scoring** | None | Full (avg 73.6) | Full (avg 86.5) |
| **Role focus** | Partnerships-heavy (39%) | CoS-heavy (56%) | Balanced CoS+Ptnr (73%) |
| **Remote %** | 60% | 67% | **93%** |
| **Target sector %** | 0% (untagged) | 89% | 57% |
| **Geographic scatter** | High (6+ regions) | Moderate (5 regions) | **Minimal (Remote + 3)** |
| **90+ jobs** | Unknown | 0 | **10** |
| **Volume** | 57 | 18 | 44 |

### The evolution story in three acts

**Act 1 (Jan 26):** Cast a wide net across job boards. Found 57 jobs but mostly partnerships roles in scattered geographies. No scoring system in place, so no way to rank quality. This was the "see what's out there" phase.

**Act 2 (Feb 2):** Introduced scoring and pivoted hard toward CoS roles. The scoring system worked — it revealed that this batch was mostly 70s-tier matches. Volume cratered (57 → 18) because the search was narrower, but it exposed that simply searching for CoS titles doesn't guarantee high-quality matches. The lesson: role title alone isn't enough.

**Act 3 (Feb 9):** The parameters found their groove. Rebalanced back toward partnerships alongside CoS. Nearly eliminated non-remote results. Average score jumped 13 points. Produced 10 jobs scoring 90+. This is the template going forward.

---

## 4. Efficiency Trend

| Metric | Jan 26 → Feb 02 | Feb 02 → Feb 09 | Overall Trend |
|--------|-----------------|-----------------|---------------|
| Avg score | — → 73.6 | 73.6 → **86.5** | **+12.9 pts** |
| 90+ tier | — → 0 | 0 → **10** | **Breakthrough** |
| Remote % | 60% → 67% | 67% → **93%** | **Converging** |
| Core role % (CoS+Ptnr) | 46% → 61% | 61% → **73%** | **Tightening** |
| Volume | 57 → 18 | 18 → **44** | **Recovering** |

**The critical insight:** You didn't sacrifice volume for quality. The Feb 9 batch found 2.4x more jobs than Feb 2 AND scored 13 points higher on average. This is the ideal trajectory — quality and volume improving simultaneously.

### What drove the improvement

Three factors compounded between Feb 2 and Feb 9:

1. **Role mix rebalance.** Feb 2 over-indexed on CoS (56%) while dropping partnerships to 6%. Feb 9 brought partnerships back to 30% alongside 43% CoS. The partnerships roles scored well (many in the 85-90 range), so reincluding them boosted the average.

2. **Geographic tightening.** Jumping from 67% to 93% remote eliminated the low-scoring non-remote jobs that dragged down the Feb 2 average (all 3 In-Office jobs scored 70-76).

3. **Search refinement.** Whatever search parameters changed between batches — keywords, filters, or board selection — produced dramatically better-fit results. The same three job boards (Ashby, Greenhouse, Lever) were used in all batches, so the improvement came from query refinement, not source changes.

---

## 5. Learning Trajectory

### What Jan 26 taught you
- Partnerships roles are abundant on Ashby, Greenhouse, and Lever
- Without scoring, you can't distinguish a 95 from a 70
- Broad geographic searches pull in European/APAC noise (Paris, Vienna, Manila)
- The baseline: 57 jobs, unknown quality, scattered geography

### How Feb 02 improved
- Introduced scoring — immediately revealed that volume ≠ quality
- Showed that a CoS-only search finds matches, but they cluster in the 70s
- Proved that non-remote jobs consistently score lower
- The lesson: pivoting too hard toward one role type is suboptimal

### How Feb 09 broke through
- Balanced search across CoS + partnerships + strategy
- Near-perfect remote focus eliminated geographic noise
- Produced every 90+ match in the entire database
- Proved that the right parameters exist — now it's about consistency

### What Feb 16 should focus on
1. **Preserve the Feb 9 formula** — don't change what's working
2. **Track overlap** — will Feb 16 re-find any Feb 9 jobs? If so, those are persistent/high-demand roles worth prioritizing
3. **Push volume** — Feb 9 found 44 quality jobs. Can the same parameters find 50-60?
4. **Watch for score drift** — if Feb 16 avg drops below 83, the market may be shifting or the search is pulling in marginal matches

---

## 6. Strategic Forecast

### Recommended Feb 16 search parameters

| Parameter | Setting | Rationale |
|-----------|---------|-----------|
| Role keywords | Chief of Staff, Partnerships, Strategic Initiatives, Business Operations | Matches the Feb 9 mix that produced 86.5 avg |
| Work arrangement | Remote only (or Remote + Hybrid in US) | 93% of best matches were remote |
| Geography | US, Americas | Eliminate Europe/APAC unless specifically targeting those time zones |
| Job boards | Ashby, Greenhouse, Lever | Consistent across all batches; no reason to change |
| Sectors to prioritize | Fintech, Health Tech, AI/Tech, Crypto, B2B SaaS | These produced the highest scores in Feb 9 |

### Prediction for Feb 16

If you run the same parameters as Feb 9:

| Metric | Prediction | Confidence |
|--------|------------|------------|
| Volume | 35–50 new jobs | Medium — depends on posting cadence |
| Avg score | 82–88 | High — parameters are dialed in |
| 90+ jobs | 6–12 | Medium — some variability expected |
| Overlap with previous batches | 3–8 re-found jobs | First real test of Times_Seen tracking |
| New companies | 30–45 | High — 111 unique companies so far with only 7 repeats |

### The bigger trajectory

| Week | Expected Cumulative Jobs | Expected Avg Score |
|------|--------------------------|-------------------|
| Feb 16 (Week 4) | ~155–170 | 83–86 |
| Feb 23 (Week 5) | ~190–220 | 83–86 |
| Mar 02 (Week 6) | ~225–270 | 83–87 |

By Week 6, you should have enough data for persistence analysis (Times_Seen > 1), application funnel tracking (if you start applying), and reliable sector trend identification.

---

## Job Board Performance

All three boards contributed consistently across batches:

| Board | Jan 26 | Feb 02 | Feb 09 | Total | Share |
|-------|--------|--------|--------|-------|-------|
| Ashby | 25 | 7 | 17 | **49** | 41.2% |
| Greenhouse | 16 | 7 | 16 | **39** | 32.8% |
| Lever | 16 | 4 | 11 | **31** | 26.1% |

Ashby is the volume leader (41%) but all three are productive. No board should be dropped.

---

## Salary Data (Sparse but Informative)

Only 5 jobs across all batches included salary data:

| Company | Role | Salary | Batch |
|---------|------|--------|-------|
| Alt | Chief of Staff | $200K–$225K | Feb 02 |
| Twelve Labs | Chief of Staff | $152K–$194K | Feb 02 |
| Firecrawl | Marketing Chief of Staff | $120K–$160K | Feb 02 |
| Covera Health | Chief of Staff to CEO | $155K–$210K | Feb 09 |
| Real | Dir of Biz Ops & Strategy | $165K–$200K | Feb 09 |

All are CoS or strategy roles. Range: $120K–$225K. Median midpoint: ~$175K. Too small a sample for conclusions, but it establishes a rough salary band for the CoS target market.

---

*Analysis generated from master_job_database.csv (119 jobs, 3 search batches, 12-day collection window)*
