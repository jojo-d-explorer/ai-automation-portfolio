---
template_name: Weekly Multi-Board CoS & Partnerships Search
category: weekly
locations: [Buenos Aires, Mexico City]
roles: [Chief of Staff, Partnerships]
boards: [Ashby, Lever, Greenhouse]
created: 2026-02-04
last_used: 2026-02-04
author: Joey Clark
reusable: true
note: "Reusable weekly search - update dates before running"
---

# Weekly Job Search Template: Buenos Aires & Mexico City

## Search Parameters

### Time Frame
Jobs posted within the **last 7 days**

### Job Boards
- site:ashbyhq.com
- site:jobs.lever.co
- site:boards.greenhouse.io

### Roles
- Chief of Staff
- Partnerships

### Locations
- Buenos Aires, Argentina
- Mexico City, Mexico

---

## Deduplication Rules
- Eliminate jobs appearing on multiple job boards (same job title + company)
- Retain highest scoring version
- List all boards where job was found in "Found_On" column

---

## Scoring Criteria (Total: 100 points)

| Category | Points | Description |
|----------|--------|-------------|
| Skills Fit | 40 | Match to candidate's core competencies |
| Industry Alignment | 30 | Sector relevance to candidate's background |
| Remote/Flexibility | 10 | Remote, hybrid, or flexible work options |
| Experience Match | 20 | Seniority level appropriateness |

### Score Threshold
- **70+ = Apply** (include in final results)
- **Below 70 = Do not apply** (exclude from final results)

---

## Data Extraction Fields

Extract the following for each job (use "N/A" if not available):

| Field | Description |
|-------|-------------|
| Score | 1-100 based on scoring criteria |
| Company | Company name |
| Company Sector | Industry/vertical |
| Role | Job title |
| Location | City, Country |
| Salary | In USD (convert if needed) |
| Job Summary | 1-2 sentence description |
| Score Rationale | 1-2 sentence explanation of score |
| URL | Direct link to job posting |
| Found On | Job board(s) where listing appeared |

---

## Output Files

### 1. Master List
- **Filename:** `Master_List_[Month][Day].csv`
- **Location:** `/Users/jc3/JobSearch/results/`
- **Contents:** All jobs found, ranked by score (highest to lowest)

### 2. Current Top 10
- **Filename:** `Current_Top10.csv`
- **Location:** `/Users/jc3/JobSearch/results/`
- **Contents:** Top 10 NEW jobs only (not in previous week's results)

---

## CSV Column Order

```
Score | Company | Sector | Role | Location | Salary | Job_Summary | Score_Rationale | URL | Found_On
```

---

## Comparison Requirement
Compare results against previous week's file to identify truly new jobs:
- **Previous week location:** `/Users/jc3/JobSearch/searches/Week_of_[date]/`
- Flag jobs that appeared in previous search
- Prioritize new listings in Top 10

---

## Verification Checklist
- [ ] Both CSV files saved to correct paths
- [ ] All jobs scored and ranked
- [ ] Duplicates removed across boards
- [ ] Previous week comparison completed
- [ ] File paths confirmed in output

---

## Resume Requirement
**Attach current resume before running search for accurate scoring**

---

*Template Version: February 2026*
*Locations: Buenos Aires, Argentina | Mexico City, Mexico*
