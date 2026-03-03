# Pipeline Quick Reference

| Phase | Tool | Action | Time |
|-------|------|--------|------|
| 1. SEARCH | CoWork | ONE_CLICK + resume | 8-10 min |
| 2. VERIFY | Terminal | `python3 JC3/check_urls.py [weekly.csv]` | 5 min |
| 3. CLEAN | Claude | "Clean [name]'s database" | 3-5 min |
| 4. CONSOLIDATE | CoWork | Merge weekly → master | 3-5 min |
| 5. ANALYZE | CoWork | MASTER_ANALYSIS (Week 3+) | 8-10 min |
| 6. PACKAGE | Manual | XLSX + PDF | 5-8 min |
| 7. DELIVER | Claude | "Draft email for [name]" | 5 min |

## Key Rule

**ONE_CLICK only searches.** URL verification is Phase 2, run separately in Terminal.

## Phase 2 Commands

```bash
# Aaron
python3 JC3/check_urls.py results/For_Others/Aaron_Kimson/Week_of_[DATE]/Aaron_Kimson_[DATE].csv

# Phil
python3 JC3/check_urls.py results/For_Others/Phil_Tassi/Week_of_[DATE]/Phil_Tassi_[DATE].csv

# Vivienne
python3 JC3/check_urls.py results/For_Others/Vivienne_Pham/Week_of_[DATE]/Vivienne_Pham_[DATE].csv

# Rosalind
python3 JC3/check_urls.py results/For_Others/Rosalind_Gahamire/Week_of_[DATE]/Rosalind_Gahamire_[DATE].csv
```

## URL_Status Values

- **Not Checked** — Fresh from search, not verified yet
- **LIVE** — Confirmed working
- **DEAD** — 404 or closed
- **STALE** — Job >45 days old
- **REDIRECT** — Goes to generic careers page

---

*v1.0 | 2026-03-02*
