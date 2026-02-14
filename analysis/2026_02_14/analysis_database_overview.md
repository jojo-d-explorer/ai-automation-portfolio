# Analysis 1: Database Overview & Data Completeness

**Generated:** 2026-02-14
**Source:** master_job_database.csv (119 jobs)
**Purpose:** Establish what analyses are possible with current data

---

## 1. Basic Stats

| Metric | Value |
|--------|-------|
| Total jobs | **119** |
| Unique companies | **111** |
| Unique sectors | **45** (excluding N/A) |
| Date range | **2026-01-29 to 2026-02-09** (12 days) |
| Search batches | **3** weeks of data |

---

## 2. Data Completeness

| Field | Count | % of Total |
|-------|-------|------------|
| Jobs with scores (Score > 0) | **62** | 52.1% |
| Jobs with sector data (not N/A) | **62** | 52.1% |
| Jobs with salary data (not N/A) | **5** | 4.2% |
| Jobs seen multiple times | **0** | 0.0% |
| Jobs with Applied_Date | **0** | 0.0% |

**Interpretation:** The database splits cleanly into two halves — 62 enriched jobs (scored + sector-tagged) and 57 raw/unscored jobs. Salary data is nearly nonexistent (5 jobs). No jobs have been marked as applied, and no jobs have been seen across multiple search batches yet.

---

## 3. Status Breakdown

| Status | Count | % |
|--------|-------|---|
| NEW | **119** | 100.0% |

All 119 jobs remain at NEW status. No applications have been submitted or tracked yet.

---

## 4. Score Distribution (62 scored jobs)

| Metric | Value |
|--------|-------|
| Mean | **82.7** |
| Median | **85** |
| Max | **95** |
| Min | **70** |

| Range | Count | % of Scored |
|-------|-------|-------------|
| 90-100 | **10** | 16.1% |
| 80-89 | **31** | 50.0% |
| 70-79 | **21** | 33.9% |

Scores cluster heavily in the 80-89 range (50%), with no jobs scoring below 70. The scoring model appears to be filtering effectively — everything surfaced is at least a moderate fit.

---

## 5. Search Source Batches

| Batch | Jobs Found |
|-------|------------|
| Week_of_2026-01-26 | **57** |
| Week_of_2026-02-09 | **44** |
| Week_of_2026-02-02 | **18** |

The first batch (Jan 26) was the largest at 57 jobs. Week of Feb 9 added 44 new jobs. Feb 2 was the smallest at 18. This suggests either search refinement or natural variation in posting volume.

---

## 6. Top 10 Sectors

| Sector | Jobs |
|--------|------|
| Fintech | **6** |
| Health Tech | **5** |
| AI/Tech | **4** |
| Crypto/Fintech | **3** |
| Fintech/Payments | **2** |
| Fintech/Fraud Prevention | **2** |
| Blockchain/Web3 | **2** |
| Venture/Accelerator | **1** |
| Sales Tech/SaaS | **1** |
| E-commerce/Sustainability | **1** |

45 distinct sectors across 62 tagged jobs — high granularity, possibly too fragmented for clustering. Related sectors (e.g., Fintech, Crypto/Fintech, Fintech/Payments, Fintech/Fraud Prevention) could be consolidated for clearer trend analysis.

---

## 7. Work Arrangement

| Arrangement | Count | % |
|-------------|-------|---|
| N/A | **57** | 47.9% |
| Remote | **55** | 46.2% |
| Hybrid | **4** | 3.4% |
| In-Office | **3** | 2.5% |

Nearly half the jobs (47.9%) have no work arrangement tagged — these are the unscored batch. Of the tagged jobs, the overwhelming majority are Remote (46.2%), with very few Hybrid (3.4%) or In-Office (2.5%).

---

## What Analyses Are Possible Now

| Analysis | Feasible? | Why |
|----------|-----------|-----|
| Score distribution & ranking | Yes | 62 scored jobs with good spread |
| Sector concentration | Yes | 45 sectors, though fragmented |
| Company patterns | Yes | 111 companies, 7 with 2+ jobs |
| Work arrangement trends | Partial | 47.9% untagged |
| Week-over-week volume | Yes | 3 search batches |
| Salary analysis | No | Only 5 jobs with data (4.2%) |
| Persistence/demand (Times_Seen) | No | All jobs seen exactly once |
| Application funnel | No | Zero applications tracked |
| Score trend over time | Not yet | Need more weekly batches |

---

*Analysis generated from master_job_database.csv (119 jobs, 111 unique companies, 12-day collection window)*