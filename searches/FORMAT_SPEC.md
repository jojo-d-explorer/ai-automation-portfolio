# Output Formatting Specification

*Single source of truth for all friend search deliverables. Referenced by ONE_CLICK files.*
*Location: /Users/jc3/GitHub/ai-automation-portfolio/searches/FORMAT_SPEC.md*

---

## Overview

Every weekly search produces three deliverable types:
1. **Branded .xlsx spreadsheets** (Top 10 + Master List) — every week
2. **Professional PDF analysis** — after 2+ weeks of data (when CONSOLIDATE_TO_MASTER has run)
3. **Raw .csv files** — kept as data backbone for consolidation, not shared with friends

---

## XLSX Formatting Specification

### Title Section (Rows 1-3, above data)

**Row 1 — Document Title:**
- Format: "[First Last] — [Document Type]"
- Examples: "Aaron Kimson — Top 10 New Opportunities", "Phil Tassi — Master Job List"
- Font: Arial/Helvetica Bold, 18pt, color #1F3864 (Navy)
- Merged across all columns

**Row 2 — Subtitle:**
- Format: "Week of [Month Day, Year]  |  Prepared by Joey Clark"
- Font: Arial/Helvetica, 11pt, color #2F5496 (Blue)
- Merged across all columns

**Row 3 — Summary Stats:**
- Format: "[N] jobs  |  Score range: [min]-[max]  |  Avg: [avg]  |  [N] NEW, [N] REPEAT"
- Font: Arial/Helvetica, 10pt, color #595959 (Gray)
- Merged across all columns
- Bottom border: medium weight, color #2F5496

**Row 4 — Blank separator**

**Row 5 — Column headers (data starts here)**

### Column Header Row

- Font: Arial Bold, 10pt, white (#FFFFFF)
- Background: #2F5496 (Blue)
- Alignment: center, wrap text
- Height: 25px

### Standard Column Widths

| Column | Width | Alignment |
|---|---|---|
| Status | 8 | Center |
| Score | 7 | Center |
| Score_Rationale | 40 | Left, wrap |
| Company | 22 | Left |
| Job_Title | 35 | Left |
| Sector | 20 | Left |
| Location | 20 | Left |
| Language_Requirement | 12 | Center |
| Work_Arrangement | 14 | Center |
| Salary_USD | 18 | Left |
| Job_Summary | 45 | Left, wrap |
| URL | 35 | Left |
| URL_Status | 10 | Center |
| Found_On | 12 | Center |

### Score Color Coding

| Score Range | Background Color | Hex | Meaning |
|---|---|---|---|
| 90-100 | Light Green | #C6EFCE | Elite match |
| 80-89 | Light Blue | #D6E4F0 | Strong match |
| 70-79 | Light Yellow | #FFF2CC | Good match |
| Below 70 | Light Red | #F2DCDB | Below threshold |

Apply to the Score column cell only.

### Status Styling

| Status | Font Style |
|---|---|
| NEW | Bold, color #006100 (dark green) |
| REPEAT | Regular, color #808080 (gray) |

### Data Rows

- Font: Arial, 10pt
- Row height: 45px (accommodates wrapped text)
- Alternating row shading: even rows #F2F2F2, odd rows white
- Light grid borders: #D9D9D9, thin

### Features

- Freeze panes below header row (row 5)
- Auto-filter enabled on all columns
- Score_Rationale and Job_Summary columns: wrap text

### Legend Row (below data)

- Position: 2 rows below last data row
- Content: "Score Key:  🟢 90+ Elite  |  🔵 80-89 Strong  |  🟡 70-79 Good  |  🔴 Below 70"
- Font: Arial, 9pt, italic, color #808080

---

## PDF Analysis Formatting Specification

### Page Setup

- Page size: US Letter (8.5" x 11")
- Margins: 0.75" all sides
- Font family: Helvetica (built into all PDF readers)

### Color Palette

| Use | Color | Hex |
|---|---|---|
| Titles, section heads | Navy | #1F3864 |
| Subtitles, accents, table headers | Blue | #2F5496 |
| Body text | Black | #000000 |
| Secondary text, labels | Gray | #595959 |
| Footer text | Medium Gray | #808080 |
| Insights/callouts | Blue italic | #2F5496 |
| Positive/new | Green | #006100 |

### Document Structure

**Title Block:**
- Line 1: "[First Last]" — Helvetica Bold, 18pt, Navy
- Line 2: "Multi-Week Search Intelligence Report" — Helvetica, 11pt, Blue
- Line 3: "Week of [Date]  |  Data: [date range]  |  Prepared by Joey Clark" — Helvetica, 9pt, Gray
- Followed by: 2pt blue horizontal rule

**Stat Dashboard (immediately below title):**
- 5 stat boxes in a single row table
- Each box: number on top (Helvetica Bold, 16pt, Navy), label below (Helvetica, 8pt, Gray)
- Background: #F2F2F2 (Light Gray)
- Stats to show: Total Jobs | Avg Score | Score 80+ | Repeat Jobs | New This Week
- "New This Week" number in green (#006100)
- Individual box borders: 0.5pt, #D9D9D9

**Standard Sections (in order):**
1. Top 10 Highest-Scoring Jobs (table)
2. Score Distribution (color-coded table + insight)
3. Sector Concentration (table + insight)
4. Geographic Distribution (table + insight)
5. Persistent Hiring Signals / Repeat Jobs (table + context)
6. Priority Company Targets (table + insight)
7. [Page break]
8. Strategic Summary (numbered findings, each bold title + body)
9. Recommended Actions (tiered table: Tier 1 green, Tier 2 blue, Tier 3 yellow)

**Footer (last page):**
- Thin gray horizontal rule
- "Analysis: [Date]  |  [N] jobs across [N] batches ([date range])  |  Next analysis: [Date + 7 days]"
- "Prepared by Joey Clark  |  AI-Powered Job Search Automation"
- Helvetica, 8pt, Medium Gray

### Table Styling (all tables)

- Header row: Helvetica Bold, 9pt, white text, #2F5496 background
- Data rows: Helvetica, 9pt (or 8.5pt if columns are tight)
- Alternating rows: white / #F2F2F2
- Grid: 0.5pt, #D9D9D9
- Padding: 3-4pt top/bottom
- Score column: color-coded per Score Color Coding spec above

### Insight Callouts

- Positioned directly below relevant table
- Font: Helvetica Italic, 9.5pt, color #2F5496
- Left indent: 12pt
- Purpose: One-sentence interpretation of the data above

---

## File Naming Convention

### xlsx files:
```
[First_Last]_Master_List_[YYYY-MM-DD].xlsx
[First_Last]_Top10_New_[YYYY-MM-DD].xlsx
```

### PDF files:
```
[First_Last]_Analysis_[YYYY-MM-DD].pdf
```

### Location:
Nested within weekly folder:
```
results/For_Others/[First_Last]/Week_of_[YYYY-MM-DD]/
├── data/
│   ├── Master_List_[YYYY-MM-DD].csv
│   └── Top10_New_[YYYY-MM-DD].csv
└── deliverables/
    ├── [First_Last]_Master_List_[YYYY-MM-DD].xlsx
    ├── [First_Last]_Top10_New_[YYYY-MM-DD].xlsx
    └── [First_Last]_Analysis_[YYYY-MM-DD].pdf  (Week 2+ only, added by MASTER_ANALYSIS)
```

---

## Prompt Language for ONE_CLICK Integration

### Add to OUTPUT FILES section of any ONE_CLICK file:

```
4. **Branded Excel — Master List:**
{RESULTS_PATH}/deliverables/[First_Last]_Master_List_{CURRENT_WEEK}.xlsx

Generate a formatted .xlsx version of the Master List CSV following FORMAT_SPEC.md:
- Title row: "[First Last] — Master Job List"
- Subtitle: "Week of [spelled out date]  |  Prepared by Joey Clark"
- Stats summary row with job count, score range, average, NEW/REPEAT counts
- Blue header row with filters enabled
- Score cells color-coded (green 90+, blue 80-89, yellow 70-79, red <70)
- Status cells styled (NEW = bold green, REPEAT = gray)
- Alternating row shading, frozen header, text wrapping on rationale/summary
- Score key legend below data

5. **Branded Excel — Top 10 New:**
{RESULTS_PATH}/deliverables/[First_Last]_Top10_New_{CURRENT_WEEK}.xlsx

Same formatting as Master List, with title: "[First Last] — Top 10 New Opportunities"
```

**Note:** PDF analysis reports are generated by MASTER_ANALYSIS (not ONE_CLICK) and saved to {RESULTS_PATH}/deliverables/ after consolidation.

---

*Created: 2026-02-17*
*Version: 1.0*
*Updates: Edit this file when formatting changes; all ONE_CLICK files reference it.*
