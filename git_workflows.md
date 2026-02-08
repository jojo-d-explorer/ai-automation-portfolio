# Git Workflows & Best Practices

*Learned through Week 2 - GitHub setup and daily usage*

---

## Core Git Concepts

### Git Tracks Changes, Not Just Files

**Key insight:** Git doesn't just save "current state of files" - it tracks every change you make.

**What Git sees:**

- ✅ File created (green +)
- ✅ File modified (orange dot)
- ✅ File deleted (red -)
- ✅ File moved (red - at old location, green + at new location)

**Implication:** Everything you do in the repo is visible. Account for all changes.

---

### The Three States of Git

```
Working Directory  →  Staging Area  →  Repository
(Your files)          (Ready to commit)   (Git history)
 Finder/TextEdit      GitHub Desktop      GitHub.com
                       checkboxes
```

**Workflow:**

1. Edit files in Finder/TextEdit → Working Directory
2. Check boxes in GitHub Desktop → Staging Area
3. Click "Commit" → Repository (permanent)
4. Click "Push" → GitHub.com (cloud backup)

---

## Daily Workflow (GitHub Desktop)

### End-of-Session Routine

**Time:** 2-3 minutes
**Frequency:** After each work session

**Steps:**

1. **Open GitHub Desktop**
2. **Review changed files** (left sidebar)
3. **Group related changes** (check relevant files)
4. **Write commit message** (summary + description)
5. **Commit to main**
6. **Push origin** (upload to GitHub)

**This becomes muscle memory by Week 3.**

---

## Commit Strategy

### Good Commit Groupings (3-5 per week, not 35)

**Group related changes together:**

**✅ Good examples:**

- "Add one-click automation system" (all automation files together)
- "Archive old experimental prompts" (all moved files together)
- "Week 2 search results" (all CSVs from this week)
- "Update .gitignore for Mac files" (config change alone)

**❌ Bad examples:**

- "Updated stuff" (too vague)
- 35 separate commits for 35 changed files (too granular)
- "Fixed search, updated README, archived files, cleaned data" (mixing unrelated changes)

---

### Commit Message Format

**Structure:**

```
Summary (50 characters max, capitalized, no period)

Description (optional, multiple lines):
- What changed
- Why it changed
- Any context needed
```

**Good examples:**

```
Add one-click weekly search automation

- Created ONE_CLICK_WEEKLY_SEARCH.md with dynamic date handling
- Automatically compares to previous week's results
- Identifies NEW vs REPEAT jobs
- Saves executed prompts for reference
```

```
Week 2: Search results across 3 boards

- 42 total jobs found
- 14 scoring 70+
- All marked NEW (different cities from Week 1)
- Mexico City, Panama City, Remote focus
```

**Bad examples:**

```
updates
```

```
fixed stuff and added files
```

---

### When to Commit

**✅ Good times:**

- Feature complete ("one-click search works")
- Bug fixed ("corrected file path issue")
- Cleanup done ("archived old files")
- End of work session ("saving progress")
- Before trying something risky ("checkpoint before experiment")

**❌ Bad times:**

- Code is broken ("halfway through debugging")
- Mixing unrelated work ("search + README + archive + data cleanup")

---

## File Operations

### How Git Sees File Moves

**When you move a file in Finder:**

**What you see:**

- File disappears from old location
- File appears in new location

**What Git sees:**

- ❌ File deleted from `/old/path/file.csv`
- ✅ File created at `/new/path/file.csv`

**How to commit properly:**

1. **Check BOTH the deletion AND the addition**
2. **Commit them together** in one commit
3. Git recognizes: "This file moved"
4. GitHub history shows: `old/path → new/path` (clean)

**If you only commit one side:**

- The other side stays in changed files
- History is messy (looks like delete + create, not move)

---

### Moving Files: Two Approaches

**Approach 1: Move in Finder, Commit Both Sides**

```
1. Move file in Finder
2. GitHub Desktop shows: red - (old location), green + (new location)
3. Check both boxes
4. Commit with message: "Move X to archive"
```

**Pro:** Intuitive
**Con:** Have to remember to commit both sides

---

**Approach 2: Use Git to Move**

```bash
git mv old/path/file.csv new/path/file.csv
```

**Pro:** Git immediately knows it's a move
**Con:** Requires Terminal/command line

**For your workflow:** Approach 1 is fine. Just remember to check both boxes.

---

## .gitignore Best Practices

### What It Does

Tells Git: "Ignore these files, don't track them"

**Common patterns:**

```
# Mac system files
.DS_Store
._*

# Log files
*.log

# Temporary files
*.tmp

# Optional: Large data files
results/**/*.csv
```

---

### When to Update .gitignore

**Add patterns BEFORE files appear (proactive):**

- New project → Add .gitignore immediately
- Know you'll generate temp files → Ignore them upfront

**How to remove already-tracked files:**

```bash
git rm --cached filename
```

This removes from Git tracking but keeps the file on your computer.

---

### Common .gitignore Gotcha

**Problem:** File already tracked before .gitignore added
**What happens:** File still shows in changed files
**Fix:** `git rm --cached filename` then commit the deletion

**After that:** Future versions of that file are ignored

---

## GitHub Desktop Specifics

### Understanding the Interface

**Left sidebar:**

- "Changes" tab = Files modified since last commit
- "History" tab = Past commits

**Changed files list:**

- ✅ Green + = New file
- 🟠 Orange dot = Modified file
- ❌ Red - = Deleted file
- Checkbox = Include in next commit

**Bottom panel:**

- Summary = Commit message title (required)
- Description = Commit message body (optional)
- "Commit to main" button

---

### Staging Area (Checkboxes)

**You control what gets committed:**

- Check file → Include in this commit
- Uncheck file → Leave for later commit

**Use case:**

- You changed 10 files
- 7 are related (new automation)
- 3 are unrelated (random cleanup)
- Commit the 7 together, save the 3 for separate commit

**Benefits:**

- Clean commit history
- Logical groupings
- Easy to understand what changed

---

### Push vs Commit

**Commit:** Saves to local Git history (your computer only)
**Push:** Uploads to GitHub.com (cloud backup, visible to others)

**Workflow:**

1. Make 3-5 commits locally
2. Push them all at once
3. GitHub.com updates with all commits

**You can commit many times before pushing** - push when you're done for the day.

---

## Common Git Issues & Solutions

### Issue 1: "Can't Push - Repository Not Found"

**Cause:** GitHub Desktop looking at wrong folder or lost connection

**Fix:**

1. Repository menu → "Open in Finder"
2. Verify you're in the right repo
3. Repository menu → "Repository Settings"
4. Check remote URL is correct

---

### Issue 2: Changes Not Showing in GitHub Desktop

**Cause:** File saved outside the repo folder

**Fix:**

1. Check file location in Finder
2. Move to `/Users/jc3/GitHub/ai-automation-portfolio/`
3. File appears in changed list

---

### Issue 3: Tons of .DS_Store Files

**Cause:** Mac creates these automatically

**Fix:**

1. Add to .gitignore: `.DS_Store`
2. Remove from tracking: `git rm --cached **/.DS_Store`
3. Commit the deletions
4. Future .DS_Store files are ignored

---

### Issue 4: Accidentally Committed Wrong Files

**Fix (if not pushed yet):**

1. History tab → Right-click commit → "Undo commit"
2. Files return to changed list
3. Fix and recommit

**Fix (if already pushed):**

- More complex, ask for help

---

## Best Practices Summary

### Do's ✅

- Commit frequently (end of each session)
- Write clear commit messages
- Group related changes together
- Review what you're committing (don't blindly commit all)
- Push regularly (backup to cloud)
- Use .gitignore to keep repo clean

### Don'ts ❌

- Don't commit broken code (unless it's "WIP checkpoint")
- Don't mix unrelated changes in one commit
- Don't write vague messages ("updates", "fixes")
- Don't wait weeks between commits (you'll forget context)
- Don't commit sensitive data (passwords, API keys)

---

## Measuring Progress

**Week 1:** "What is Git? How do I push?"
**Week 2:** "I understand Git tracks changes. I group commits logically."
**Week 4 target:** "Committing is muscle memory. I do it without thinking."
**Week 8 target:** "I use Git history to review my work. I revert mistakes confidently."

---

## Future Git Topics (Beyond Week 2)

**Not covered yet, but coming later:**

- Branches (working on features separately)
- Pull requests (if collaborating)
- Merge conflicts (if needed)
- Git history navigation (finding old versions)

**For now:** Master the basics (commit, push, .gitignore, file moves). Advanced topics when needed.

---

*Last updated: 2026-02-06*
*Reflects Week 2 learnings*
