# Analysis 3: Work Arrangement & Geographic Distribution

**Generated:** 2026-02-14
**Source:** master_job_database.csv (119 jobs)
**Scope:** All jobs (scored + unscored)

---

## 1. Work Arrangement Breakdown

| Arrangement | Jobs | % of Total |
|-------------|------|------------|
| N/A (untagged) | 57 | 47.9% |
| Remote | 55 | 46.2% |
| Hybrid | 4 | 3.4% |
| In-Office | 3 | 2.5% |

The 57 N/A jobs are the entire unscored batch from the Jan 26 search — they were never tagged with work arrangement. Of the 62 enriched jobs, **55 are Remote (88.7%)**, with only 7 non-remote. The search pipeline is overwhelmingly surfacing remote roles.

---

## 2. Remote Dominance

### Scored jobs by arrangement

| Arrangement | Scored Jobs | Avg Score | Range | 90+ Tier | 80-89 Tier | 70-79 Tier |
|-------------|-------------|-----------|-------|----------|------------|------------|
| Remote | 55 | **83.9** | 70–95 | 10 | 30 | 15 |
| Hybrid | 4 | **74.5** | 70–84 | 0 | 1 | 3 |
| In-Office | 3 | **72.7** | 71–76 | 0 | 0 | 3 |

### The score gap is clear and significant

Remote jobs average **83.9** — a full **10+ points higher** than Hybrid (74.5) and In-Office (72.7). Every single 90+ scoring job in the database is Remote. All 3 In-Office jobs are stuck in the 70s.

This isn't random. It reflects two compounding factors: remote roles genuinely tend to be better fits (CoS and partnerships roles at tech companies skew remote), and the scoring model likely rewards the remote alignment built into your search criteria.

**Bottom line:** Remote is not just the majority of your pipeline — it's where all the top-tier matches live.

---

## 3. Location Clustering

### Top locations across all 119 jobs

| Location Category | Jobs | % | Avg Score (where available) |
|-------------------|------|---|---------------------------|
| Remote (any variant) | 87 | 73.1% | 85 |
| Paris | 9 | 7.6% | unscored |
| New York | 5 | 4.2% | 79 |
| UK/London | 4 | 3.4% | 70 (1 scored) |
| Vienna | 4 | 3.4% | unscored |
| Philippines | 3 | 2.5% | unscored |
| US (general) | 2 | 1.7% | 95 (1 scored) |
| Latin America | 2 | 1.7% | 72 |
| San Francisco | 1 | 0.8% | 71 |

### Non-remote locations specifically (Hybrid + In-Office only)

| Location | Jobs | Type | Avg Score |
|----------|------|------|-----------|
| New York City | 2 | In-Office | 74 |
| Washington, DC | 1 | Hybrid | 84 |
| Mexico City - Hybrid | 1 | Hybrid | 73 |
| San Francisco, CA | 1 | In-Office | 71 |
| Mexico City | 1 | Hybrid | 71 |
| London, UK | 1 | Hybrid | 70 |

Washington DC (84) is the only non-remote location that produced an above-average score. NYC In-Office averages just 74. If you must consider non-remote, DC is the only geography worth targeting.

### Location fragmentation problem

"Remote" appears in **17 different string variants** across the database: "Remote", "Remote - US", "Remote US", "Remote U.S.", "Remote - USA", "United States Remote", "Remote (hub in NY)", "SF or Remote", "NYC/LA/SF Remote", etc. This fragmentation makes clean analysis harder. Normalizing these to a single "Remote" tag (or "Remote-US" vs "Remote-Global") would significantly improve future analysis.

---

## 4. Location + Sector Patterns

### Fintech jobs by location

| Sector | Location | Score |
|--------|----------|-------|
| Crypto/Fintech | Remote - US | 94 |
| Fintech | Remote - Americas | 91 |
| Fintech/Payments | Remote | 90 |
| Fintech/Fraud Prevention | Remote | 88 |
| Fintech/Fraud Prevention | Remote | 88 |
| Fintech/Identity | Remote | 88 |
| Fintech/Banking Infrastructure | Remote | 88 |
| Crypto/Fintech | Remote/Hybrid | 79 |
| Fintech | Remote - US | 78 |
| Fintech | Remote - Canada | 78 |
| Fintech/Tax Tech | Remote | 78 |
| Fintech/Alternative Investments | New York City | 76 |
| Fintech | Remote | 75 |
| Fintech | Mexico City - Hybrid | 73 |
| Fintech/Payments | Mexico City - Remote | 73 |
| Crypto/Fintech | Mexico City - Remote | 71 |
| Fintech | Mexico City - Remote | 71 |
| Fintech/Market Intelligence | London, UK | 70 |

**The pattern is unmistakable:** Remote fintech jobs average mid-to-high 80s. The moment fintech goes location-specific (NYC, Mexico City, London), scores drop to low-to-mid 70s. The best fintech matches are remote-first companies, period.

### Remote rate by sector (sectors with 2+ jobs)

| Sector | Total | Remote | Remote % |
|--------|-------|--------|----------|
| Health Tech | 5 | 5 | 100% |
| Crypto/Fintech | 3 | 3 | 100% |
| Fintech/Payments | 2 | 2 | 100% |
| Fintech/Fraud Prevention | 2 | 2 | 100% |
| Blockchain/Web3 | 2 | 2 | 100% |
| Fintech | 6 | 5 | 83% |
| AI/Tech | 4 | 3 | 75% |

Every sector that matters to your search is overwhelmingly remote. The non-remote outliers are consistently the lowest-scoring jobs in each sector.

---

## 5. Search Parameters & Batch Analysis

### Batch-by-batch breakdown

| Batch | Jobs | Work Arrangement | Geographic Spread |
|-------|------|-----------------|-------------------|
| Week_of_2026-01-26 | 57 | **All N/A** (untagged) | 34 Remote-ish, 9 Paris, 4 Vienna, 3 Philippines, 3 UK, 2 NYC |
| Week_of_2026-02-02 | 18 | 12 Remote, 3 In-Office, 3 Hybrid | 12 Remote, 2 NYC, 2 LATAM, 1 SF, 1 UK |
| Week_of_2026-02-09 | 44 | **43 Remote**, 1 Hybrid | 41 Remote, 1 US general, 1 NYC, 1 Other |

### What changed between batches

The first batch (Jan 26) pulled heavily from European locations — Paris (9), Vienna (4), UK (3), Philippines (3). These are all unscored and likely came from broader or less targeted searches.

By the Feb 9 batch, the pipeline had **tightened dramatically**: 43 of 44 jobs were Remote, and the geographic scatter almost completely disappeared. This suggests either intentional search refinement or a job board shift toward remote-tagged roles.

### Unexpected geographies

Paris (9 jobs), Vienna (4), and Philippines (3) stand out as unexpected. All 16 are unscored and from the Jan 26 batch. These likely came from European-focused job boards (possibly Aircall/Qualysoft/Jobgether searches). Whether these are worth scoring depends on whether you're open to European time zones.

---

## 6. Strategic Recommendations

### Should you focus only on Remote?

**Yes — with caveats.**

The data overwhelmingly supports a Remote-first strategy. Remote jobs score 10+ points higher on average, contain all 10 of the 90+ tier matches, and dominate every relevant sector. The scoring model and the job market are both telling you the same thing: the best CoS/partnerships roles at tech companies are remote.

**The caveats:**
- Washington DC hybrid scored 84 — don't auto-filter it out
- "Remote (hub in NY)" and similar variants may require occasional in-person presence. These are effectively hybrid roles dressed as remote
- Some "Remote - US" listings may exclude candidates outside certain time zones

### Should you expand location searches?

**No — narrow them further.**

The Jan 26 batch cast a wide net (Paris, Vienna, Manila) and those 16 jobs remain unscored, which suggests they were deprioritized for a reason. Meanwhile, the Feb 9 batch (tightly focused on remote) produced the highest density of quality matches. The trend line is clear: tighter geographic targeting → better results.

**One exception:** If you're open to LATAM time zones, Mexico City produced 4 jobs. The scores are low (71–73) but there's enough volume to suggest it's an emerging hub for fintech partnerships roles.

### Geographic hubs worth targeting

| Priority | Hub | Rationale |
|----------|-----|-----------|
| 1 | **Remote - US** | Highest volume, highest scores, best fit |
| 2 | **Remote - Americas** | Captures US + LATAM remote roles |
| 3 | **NYC (remote-friendly)** | Good for hybrid-tolerant roles; avoid pure in-office |
| 4 | **Washington DC** | Small sample but scored well (84) |
| 5 | **Drop**: Paris, Vienna, Manila, SF in-office | Low/no scores, geographic mismatch |

### Data quality action items

1. **Normalize location strings** — Consolidate the 17 variants of "Remote" into 3 categories: Remote-US, Remote-Americas, Remote-Global
2. **Score the Jan 26 batch** — 57 unscored jobs include the Paris/Vienna/Manila clusters. Scoring them will either validate dropping those geographies or surface hidden gems
3. **Tag the N/A work arrangements** — All 57 are from Jan 26. Even a quick remote/not-remote tag would improve analysis

---

*Analysis generated from master_job_database.csv (119 jobs, 111 unique companies, 12-day collection window)*
