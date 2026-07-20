# job_search_project — v3.0 layout

This is the lean v3.0 pipeline structure. v2.x artifacts (the corpus
`companies.json`, the disqualifier list, the pending-review stub system)
are intentionally absent — v3.0 stripped them out.

## Folder structure

```
job_search_project/
├── prompts/                              # Versioned prompt files
│   ├── ONE_CLICK_v3.0_stage1_discovery.md
│   ├── ONE_CLICK_v3.0_stage2_scoring.md
│   └── (older v2.x prompts → move to archive/)
│
├── resume/                               # Resume file referenced by prompts
│   └── Joey_Clark_Resume_4-25_FINAL.pdf
│
├── scripts/                              # Python helpers (unchanged from v2.x)
│   ├── classify_url.py                   # URL → {ats, slug, job_id, url_type}
│   ├── ats_api_checker_v2.py             # Optional API freshness pass
│   ├── check_urls.py                     # Closure check before applying
│   └── (corpus_append.py and disqualifiers.json → no longer used in v3.0)
│
├── results/
│   └── joey/
│       ├── seen_companies.txt            # Dedup list, appended each Stage 1 run
│       ├── named_targets.txt             # Priority companies for Step 2 sweep
│       └── Week_of_YYYY-MM-DD/           # Per-week output folder
│           ├── candidates_YYYY-MM-DD.csv
│           ├── Master_v3_0_YYYY-MM-DD.csv
│           ├── pre_filter_drops_YYYY-MM-DD.csv
│           ├── failed_fetches_YYYY-MM-DD.csv      (if any)
│           ├── closed_listings_YYYY-MM-DD.csv     (if any)
│           └── api_verified_YYYY-MM-DD.csv        (if API checker was run)
│
└── archive/                              # Old prompt versions, deprecated files
    └── (move v2.2.x, v2.3.x, companies.json, disqualifiers.json here)
```

## Files you maintain by hand

Two files. That's it.

**`results/joey/named_targets.txt`** — One company domain per line.
Currently seeded with `tekever.com`. Add Scenius LATAM newsletter
companies as you read each issue. Add anything else worth a direct sweep.

**`results/joey/seen_companies.txt`** — Auto-populated by Stage 1. You
don't touch this; it just exists so Stage 2 can mark NEW vs REPEAT.

## Files Stage 1 + Stage 2 produce automatically

All under `results/joey/Week_of_YYYY-MM-DD/`. The week folder is created
by Stage 1 if it doesn't exist. Output files are timestamped by week so
nothing overwrites the previous run.

## Migration from v2.x

When you're ready to switch over:

1. Copy this entire `job_search_v3.0/` directory contents into your
   existing `~/GitHub/ai-automation-portfolio/job_search_project/`
   (the `prompts/` folder will sit alongside any existing v2.x
   structure).
2. Move v2.x prompt files into `archive/` so the active `prompts/`
   folder only has v3.0.
3. Move `companies.json`, `companies.json.bak.*`, and
   `disqualifiers.json` into `archive/` — v3.0 doesn't read them.
4. Move `corpus_append.py` into `archive/` — v3.0 doesn't call it.
5. Keep `classify_url.py`, `ats_api_checker_v2.py`, and `check_urls.py`
   in `scripts/` — v3.0 still uses them.
6. Make sure `resume/Joey_Clark_Resume_4-25_FINAL.pdf` is in `resume/`
   (the prompts reference this path).

## When to run what

**Weekly (Monday morning):**
1. Stage 1 — produces `candidates_YYYY-MM-DD.csv`
2. Stage 2 — produces `Master_v3_0_YYYY-MM-DD.csv`
3. (Optional) Run `ats_api_checker_v2.py` before Stage 2 if you want
   the API freshness signal unioned in
4. Run `check_urls.py` against the Master one last time before
   applying to anything

**Monthly:**
- Review `archive/` for anything worth deleting permanently
- Update `named_targets.txt` based on what's actually been useful

## What v3.0 does NOT do

- No corpus enrichment, no pending-review stubs, no auto-grow logic
- No disqualifier list maintenance
- No warm-route flagging (Joey handles routing manually)
- No Builder Bonus, no six-signal combination library
- No below-threshold diagnostic logging

If you find yourself wanting any of these back, archive a v3.0 file
first so you can compare side-by-side before re-introducing complexity.
