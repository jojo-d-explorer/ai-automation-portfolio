# Technical Setup & Environment

*Current state as of Week 2*

---

## Working Directory

**Primary location:** `/Users/jc3/GitHub/ai-automation-portfolio/`

**Why this location:**

- Out of iCloud Drive (Git + iCloud conflict)
- Local-only storage (faster, more reliable)
- Standard GitHub convention

**Legacy location (DO NOT USE):**

- `/Users/jc3/JobSearch/` - old experimental folder, not tracked by Git

---

## Repository Structure

```
ai-automation-portfolio/
├── .git/                          (Git internals - don't touch)
├── .gitignore                     (Files to ignore)
├── README.md                      (Repository homepage)
│
├── learning_philosophy.md         (My learning style & context)
├── curriculum_plan.md             (12-week roadmap)
├── prompt_engineering_principles.md
├── git_workflows.md
├── technical_setup.md             (this file)
│
├── results/                       (Search outputs)
│   ├── Week_of_2026-01-26/       (Week 1 results)
│   │   ├── LinkedIn_COS_2026-01-28.csv
│   │   ├── Greenhouse_COS_2026-01-29.csv
│   │   └── ...
│   └── Week_of_2026-02-02/       (Week 2 results)
│       ├── Master_List_2026-02-03.csv
│       ├── Top10_New_2026-02-03.csv
│       └── ...
│
├── searches/                      (Prompts & templates)
│   ├── ONE_CLICK_WEEKLY_SEARCH.md (Main automation)
│   ├── prompts/
│   │   ├── daily/                (Quick scans)
│   │   ├── weekly/               (Recurring searches)
│   │   ├── for_others/           (Friend templates)
│   │   └── experiments/          (Testing)
│   └── archive/                  (Old/deprecated)
│
└── learning_log/                 (Documentation)
    ├── week1_insights.md
    ├── week2_reflection.md
    ├── TEMPLATE_weekly_reflection.md
    ├── context_continuation_prompt.md
    └── searches_inventory.csv
```

---

## Tools & Platforms

### Primary Tools (Daily Use)

**CoWork**

- Browser automation via Claude
- Accessed through: claude.ai web interface
- Purpose: Job search automation, web scraping, data extraction

**GitHub Desktop**

- Version: Latest (Mac Apple Silicon)
- Purpose: Git commits, pushes, history
- Why not command line: Easier for non-developers, visual diff

**Claude (Anthropic)**

- Model: Sonnet 4.5
- Subscription: Max (higher usage limits)
- Purpose: Teaching, guidance, prompt engineering, CoWork orchestration

**Mac Computer**

- Chip: Apple Silicon (M-series)
- OS: macOS (latest)
- Why matters: Different from Intel Macs for some software

---

### Supporting Tools

**Finder**

- macOS file manager
- Primary way to navigate file system
- Search: Cmd+Space → Spotlight Search

**TextEdit**

- Default Mac text editor
- Used for: Creating/editing .md, .txt files
- Remember: Format → Make Plain Text for code/markdown

**Numbers**

- Apple's spreadsheet app
- Opens .csv files by default on Mac
- Alternative: Excel, Google Sheets

---

### Accounts & Services

**GitHub**

- Username: jojo-d-explorer
- Repository: ai-automation-portfolio (currently private)
- Plan: Free (sufficient for now)

**Claude.ai**

- Plan: Max
- Purpose: Learning curriculum, CoWork access

---

## File Conventions & Standards

### Date Formats

**Always use ISO 8601:** `YYYY-MM-DD`

**Examples:**

- ✅ `2026-02-04` (unambiguous, sorts correctly)
- ❌ `2-4` (Feb 4? Month 2 day 4?)
- ❌ `02/04/26` (US vs European format confusion)

---

### File Naming

**Pattern:** `[Category]_[Description]_[Date].[extension]`

**Examples:**

- `Master_List_2026-02-03.csv`
- `LinkedIn_COS_Remote_2026-01-30.csv`
- `week2_reflection.md`

**Rules:**

- No spaces (use underscores or hyphens)
- Descriptive (name tells you what's inside)
- Consistent casing (lowercase or CamelCase, pick one)
- Always include extension

---

### File Extensions

**Common ones:**

- `.md` = Markdown (formatted text, renders nicely on GitHub)
- `.txt` = Plain text (no formatting)
- `.csv` = Spreadsheet data (comma-separated values)
- `.pdf` = Documents (Joey_Clark_Resume_2026.pdf)
- `.py` = Python scripts (future use)

**Always specify explicitly** - don't let system guess

---

## File Paths

### Absolute vs Relative

**Absolute path (always use these):**

```
/Users/jc3/GitHub/ai-automation-portfolio/results/file.csv
```

Starts with `/`, full path from root. Works anywhere.

**Relative path (avoid unless you know where you are):**

```
results/file.csv
```

Relative to current directory. Breaks if you're in wrong folder.

---

### Special Paths

**Home directory:**

- Symbol: `~`
- Expands to: `/Users/jc3/`
- Example: `~/GitHub/ai-automation-portfolio/`

**Current directory:**

- Symbol: `.`
- Means: wherever you are now

**Parent directory:**

- Symbol: `..`
- Means: one level up

---

## Typical Workflows

### Creating a New File

**Option 1: Via CoWork**

```
Create file at /Users/jc3/GitHub/ai-automation-portfolio/[path]/[filename]
Content:
[paste content]
Confirm when created.
```

**Option 2: Manually in TextEdit**

1. Applications → TextEdit
2. Format → Make Plain Text
3. Type/paste content
4. Save As → Navigate to exact folder → Enter filename with extension

---

### Running a Search

**Current process:**

1. Open `ONE_CLICK_WEEKLY_SEARCH.md`
2. Copy prompt (from "Calculate today's date..." to end)
3. Paste into CoWork
4. Attach resume: `Joey_Clark_Resume_2026.pdf`
5. Hit enter
6. Wait 10-15 minutes
7. Check `/results/Week_of_[DATE]/` for outputs

---

### Committing Work to GitHub

**Process:**

1. Finish work session
2. Open GitHub Desktop
3. Review changed files (left sidebar)
4. Check boxes for related files
5. Write summary + description
6. Click "Commit to main"
7. Repeat for other logical groups
8. Click "Push origin" when done

**Frequency:** End of each work session

---

## Common File Locations Quick Reference

**Most-used paths:**

```
Search results:
/Users/jc3/GitHub/ai-automation-portfolio/results/Week_of_YYYY-MM-DD/

Main automation:
/Users/jc3/GitHub/ai-automation-portfolio/searches/ONE_CLICK_WEEKLY_SEARCH.md

Prompt templates:
/Users/jc3/GitHub/ai-automation-portfolio/searches/prompts/[category]/

Learning docs:
/Users/jc3/GitHub/ai-automation-portfolio/learning_log/

Resume:
Joey_Clark_Resume_2026.pdf (attached to searches as needed)
```

---

## Known Issues & Quirks

### Issue 1: .DS_Store Files Everywhere

**What:** Mac creates these hidden files in every folder
**Fix:** Added to .gitignore, removed from Git tracking
**Status:** Resolved Week 2

---

### Issue 2: CoWork File Creation Locations

**What:** CoWork sometimes saves to unexpected locations
**Fix:** Always specify full absolute paths with verification
**Status:** Mitigated by being explicit in prompts

---

### Issue 3: CSV Opening in Numbers

**What:** Mac defaults to Numbers app for .csv
**Fix:** Right-click → Open With → Excel/Google Sheets if preferred
**Status:** Not a problem, Numbers works fine

---

## Environment Variables & Settings

**GitHub Desktop:**

- Default editor: Not set (using TextEdit manually)
- Default shell: Not configured
- Ignored files: Managed via .gitignore

**CoWork:**

- No persistent settings
- Each prompt is independent
- Must specify full context each time

---

## Backups & Redundancy

**Where work is stored:**

1. Local: `/Users/jc3/GitHub/ai-automation-portfolio/` (primary)
2. GitHub: github.com/jojo-d-explorer/ai-automation-portfolio (cloud backup)
3. Weekly: Push to GitHub after each session (redundancy)

**Not backed up:**

- `/Users/jc3/JobSearch/` (old location, not in Git)
- Files outside the repo folder

**Recommendation:** Keep all work inside the repo folder

---

## Future Additions (Planned)

**Week 4-5:**

- Python environment setup (for data analysis)
- Possibly: VS Code or similar text editor
- Possibly: Database (SQLite) for master job data

**Week 9-10:**

- Zapier/Make accounts (landscape survey)
- Cursor or Copilot (AI coding assistant)

**Week 12:**

- Make GitHub repo public
- Portfolio polish

---

## Troubleshooting Quick Reference

**File not showing in GitHub Desktop:**

- Check it's inside `/Users/jc3/GitHub/ai-automation-portfolio/`
- Press Cmd+R to refresh
- Verify file actually exists (Finder)

**Can't find file CoWork created:**

- Use Spotlight (Cmd+Space) to search for filename
- Right-click result → Show in Finder
- May be in unexpected location, move to correct folder

**Git push fails:**

- Check internet connection
- Verify GitHub Desktop is signed in
- Try Repository → Refresh

---

*Last updated: 2026-02-06*
*Reflects Week 2 environment*
