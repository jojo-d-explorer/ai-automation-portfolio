# ONE-CLICK WEEKLY SEARCH

Calculate today's date and determine:
- Current week start date (most recent Monday): CURRENT_WEEK
- Previous week start date (Monday before that): PREVIOUS_WEEK

Use these dates for file paths and comparisons below.

---

Search these job boards for roles posted in the last 7 days:
- site:boards.greenhouse.io
- site:jobs.lever.co
- site:jobs.ashbyhq.com

Roles:
- Chief of Staff
- Partnerships
- Strategic Initiatives

Locations:
- Remote
- Mexico City, Mexico
- Panama City, Panama

**Note:** Remote-US roles consistently score 10+ points higher than location-specific roles. Consider focusing searches on Remote unless specifically targeting a city.

For each board/role/location combination, extract up to 20 results (paginate to page 2 if needed).

Show progress matrix as you search each combination.

---

EXTRACT FIELDS (use "N/A" if not available):
- Company
- Company Sector
- Job Title
- Location
- Salary (convert to USD if in other currency)
- Language Requirement (if no language mentioned, use "N/A"; if language other than English mentioned, list the language)
- Work Arrangement (Remote/Hybrid/In-Office)
- Job Summary (2-3 sentences)
- URL

---

**WORK ARRANGEMENT STANDARDIZATION:**
After extracting, normalize the Work_Arrangement field to one of these 5 categories:

- **Remote-US** — Location contains "US", "USA", "U.S.", "United States", any US city/state, or "Remote" with US qualifier
- **Remote-Americas** — Location contains "Americas", "Canada", "LATAM", or a Latin American country with "Remote"
- **Remote-Global** — Generic "Remote" without geographic qualifier, or explicitly non-US (e.g., "Remote EMEA", "Remote Europe")
- **Hybrid** — Any hybrid arrangement, including "Remote/Hybrid" variants
- **In-Office** — Location-specific roles without "Remote" (e.g., "New York, NY", "Paris", "Vienna")

Apply these rules consistently for all extracted jobs. Do not leave Work_Arrangement as generic "Remote" — always classify into the specific category above.

---

DEDUPLICATION:
Eliminate duplicate jobs (same company + same job title across boards). Keep highest-scoring version and list all boards where found in "Found_On" column.

---

SCORING:
Using attached resume (Joey_Clark_Resume_2026.pdf), score each job 1-100 based on:
- Skills fit (40 points)
- Industry alignment (35 points)
- Experience match (25 points)

Provide 1-2 sentence score rationale for each job.

Filter to jobs scoring 70+ only. Rank by score (highest to lowest).

SECTOR FILTERING:
After scoring, apply sector preference adjustments:
- If Sector contains "Healthcare" or "Health Tech": Reduce score by 10 points
- If Sector contains "Crypto" or "Web3": Reduce score by 15 points
- If Sector contains "Fintech": Add 5 bonus points
- If Sector contains "AI" or "ML": Add 5 bonus points
- If Sector contains "Defense" or "Industrial": Add 5 bonus points

Then re-filter to 70+ threshold.

---

NEW JOB DETECTION:
Compare against: /Users/jc3/GitHub/ai-automation-portfolio/results/Week_of_PREVIOUS_WEEK/Master_List_PREVIOUS_WEEK.csv

- If file exists: Mark jobs not in previous file as "NEW"
- If file doesn't exist (first run): Mark all jobs as "NEW"
- Add "Status" column with "NEW" or "Repeat"

---

OUTPUT FILES:

Create folder if doesn't exist: /Users/jc3/GitHub/ai-automation-portfolio/results/Week_of_CURRENT_WEEK/

1. Master List: /Users/jc3/GitHub/ai-automation-portfolio/results/Week_of_CURRENT_WEEK/Master_List_CURRENT_WEEK.csv

Columns: Status | Score | Score_Rationale | Company | Job_Title | Sector | Location | Language_Requirement | Work_Arrangement | Salary_USD | Job_Summary | URL | Found_On

2. Top 10 New: /Users/jc3/GitHub/ai-automation-portfolio/results/Week_of_CURRENT_WEEK/Top10_New_CURRENT_WEEK.csv

Same columns, only top 10 jobs marked "NEW". If <10 new jobs, include all. If zero new jobs, create file with headers and note "No new jobs this week."

3. Save this prompt: /Users/jc3/GitHub/ai-automation-portfolio/searches/prompts/weekly/executed_CURRENT_WEEK.txt

---

**FINAL STEP - REMINDER:**

After showing the summary above, display this message:

⚠️  NEXT STEP REQUIRED ⚠️

Weekly search complete! To add these jobs to your master database, run:

CONSOLIDATE_TO_MASTER.md

This will:
- Deduplicate against your existing jobs
- Update Times_Seen for repeat jobs
- Add [X] new jobs to master database

📋 Copy the CONSOLIDATE_TO_MASTER prompt and run it now (takes 30 seconds)

---

FINAL OUTPUT:
Verify all files saved. Show:
- Final summary table of top results
- Total jobs found, total scoring 70+, total NEW vs REPEAT
- File paths where everything saved

---

### JOB SEARCH TRACKING UPDATE

After all output files are saved, update the tracking spreadsheet:

**File:** /Users/jc3/GitHub/ai-automation-portfolio/Job_Search_Tracking.xlsx
**Sheet:** "Job Search Tracking"

Find the rows for **Joey Clark** (look for name in column A). Add a new continuation row immediately after the last Joey row with:

| Column | Value |
|--------|-------|
| C (Search Ran) | Today's date (YYYY-MM-DD) |
| D (Results 70+) | Total jobs scoring 70+ |
| E (Top Score) | Highest score in this search |
| F (Search Config) | Boards searched \| Roles \| Locations (short summary) |
| G (Next Search) | CURRENT_WEEK + 7 days (YYYY-MM-DD) |
| H (Link to Folder) | Week_of_CURRENT_WEEK/ |

Also mark the previous row's "Next Search" (column G) as completed by appending " ✓".

Save the updated spreadsheet back to the same path.

---

*Run every Sunday. Runtime: 10-15 minutes.*
