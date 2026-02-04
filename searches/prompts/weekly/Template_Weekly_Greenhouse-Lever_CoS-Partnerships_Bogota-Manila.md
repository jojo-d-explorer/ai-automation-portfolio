---
template_name: Weekly Greenhouse/Lever CoS & Partnerships Search
category: weekly
locations: [Bogota, Manila]
roles: [Chief of Staff, Partnerships]
boards: [Greenhouse, Lever]
created: 2026-02-03
last_used: 2026-02-03
author: Joey Clark
reusable: true
note: "Reusable weekly search - update dates before running"
---

# Job Search Template: Bogota & Manila - Partnerships/Chief of Staff

## Instructions
Search the following job boards for roles posted within the last week.

### Job Boards
- boards.greenhouse.io
- jobs.lever.co

### Roles to Search
- Partnerships
- Chief of Staff

### Target Locations
- Manila, Philippines
- Bogota, Colombia

### Results Requirements
- Extract up to **10 results per board/role/location combination**
- Paginate to page 2 if needed to reach 10 results
- Display a **progress matrix** showing results found for each combination as you search

---

## Data Extraction

### Required Fields
Extract the following for each job (use "N/A" if not available):

| Field | Description |
|-------|-------------|
| Company | Company name |
| Company Sector | Industry/vertical |
| Company Funding Status | See funding rules below |
| Job Title | Exact title from listing |
| Location | City, Country |
| Salary | In USD (convert if needed) |
| Language Requirements | Required languages |
| Immigration/Visa Requirements | Sponsorship info |
| Job Description | 1-3 sentence summary |
| In-Office Requirement | Remote / Hybrid / In-Office |
| URL | Direct link to job posting |

### Funding Status Rules
- **Public companies:** Use "Public" + ticker symbol if known
- **Private companies:** Latest funding round (Series A, Seed, etc.) if findable within 30 seconds
- **Unknown:** Use "Private - Unknown"

---

## Deduplication
- Remove duplicate jobs (same company + same job title)
- Keep the highest-scoring version
- Note all boards where the job appeared in a **"Found_On"** column

---

## Scoring Criteria (Total: 100 points)

Score each job based on resume alignment:

| Category | Points | Evaluation Criteria |
|----------|--------|---------------------|
| Industry Alignment | 30 | Match to candidate's industry experience |
| Role Fit | 40 | Alignment with target role responsibilities |
| Experience Level Match | 20 | Seniority level appropriateness |
| Skills Match | 10 | Technical/soft skills overlap |

### Scoring Output
- Provide a **2-sentence rationale** explaining each score
- **Filter to jobs scoring 70+ only**
- Rank all results by score (highest to lowest)

---

## Output Format

### CSV Columns (in this order)
```
Score | Company | Sector | Funding_Status | Job_Title | Location | Salary | Language_Req | Visa_Req | In_Office_Req | Description | Score_Rationale | URL | Found_On
```

### File Naming Convention
```
[Location1]_[Location2]_JobSearch_[M-D].csv
```

### Save Location
```
/Users/jc3/JobSearch/results/
```

---

## Confirmation Requirements
1. Display progress matrix during search
2. Show summary table of filtered results (70+ scores)
3. Confirm exact file path where CSV was saved
4. Provide top recommendation with rationale

---

## Notes for Future Use

### Customization Points
- **Locations:** Update target cities as needed
- **Roles:** Modify search terms for different positions
- **Score Threshold:** Adjust 70+ cutoff based on market conditions
- **Job Boards:** Add/remove boards (e.g., LinkedIn, Indeed, Wellfound)

### Resume Requirement
**Important:** Attach current resume before running this search for accurate scoring.

### Limitations Observed
- Chief of Staff roles are rare in LATAM/SEA markets on Greenhouse/Lever
- Salary data often not disclosed publicly
- Some job boards block direct fetching; browser automation preferred
- Funding status may require additional research time

---

*Template Version: Feb 2026*
*Based on: Bogota/Manila Partnerships & CoS Search*
