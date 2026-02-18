# CONSOLIDATE WEEKLY SEARCH TO MASTER DATABASE

**Purpose:** Merge latest weekly search results into master job database with deduplication and metadata tracking
**Run after:** ONE_CLICK_WEEKLY_SEARCH completes
**Runtime:** 30-60 seconds

---

## THE PROMPT

Calculate today's date and determine:
- Current week start date (most recent Monday): CURRENT_WEEK

---

**READ LATEST WEEKLY RESULTS:**

File: /Users/jc3/GitHub/ai-automation-portfolio/results/Week_of_CURRENT_WEEK/Master_List_CURRENT_WEEK.csv

This file has 13 columns: Status | Score | Score_Rationale | Company | Job_Title | Sector | Location | Language_Requirement | Work_Arrangement | Salary_USD | Job_Summary | URL | Found_On

---

**READ MASTER DATABASE:**

File: /Users/jc3/GitHub/ai-automation-portfolio/master_job_database.csv

This file has 19 columns (13 above + 6 metadata columns).

---

**DEDUPLICATION & METADATA:**

For each job in weekly results:

1. Check if Company + Job_Title already exists in master database
2. If DUPLICATE (job exists):
   - Increment Times_Seen by 1
   - Update Last_Seen_Date to CURRENT_WEEK date (YYYY-MM-DD format)
   - Append "Week_of_CURRENT_WEEK" to Search_Sources (comma-separated)
   - If Status in weekly = "NEW" but master has different status, keep master status
   - Keep all other fields from master (don't overwrite with weekly data)
3. If UNIQUE (new job):
   - Add all 13 columns from weekly results
   - Add metadata columns:
     - First_Seen_Date = CURRENT_WEEK date (YYYY-MM-DD)
     - Last_Seen_Date = CURRENT_WEEK date (YYYY-MM-DD)
     - Times_Seen = 1
     - Search_Sources = "Week_of_CURRENT_WEEK"
     - Applied_Date = "" (blank)
     - Notes = "" (blank)

---

**SAVE UPDATED MASTER:**

File: /Users/jc3/GitHub/ai-automation-portfolio/master_job_database.csv

All 19 columns, sorted by Score descending (highest scores first).

---

**REPORT SUMMARY:**

Show:
- Jobs in master before consolidation: X
- Jobs in weekly results: Y
- Duplicates found (already in master): Z
- New unique jobs added: W
- Jobs in master after consolidation: X + W

Also show:
- Top 3 jobs by Times_Seen (most frequently appearing jobs)
- Any jobs that went from Status="NEW" to something else

---

*Run every Sunday after weekly search*
