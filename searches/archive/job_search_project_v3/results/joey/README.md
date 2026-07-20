# results/joey/

Two hand-maintained files at this level. Everything else is in
per-week subfolders auto-created by Stage 1.

## Hand-maintained

- `named_targets.txt` — Priority companies for Stage 1 Step 2 sweep.
  Currently seeded with `tekever.com`. Add Scenius LATAM newsletter
  names and anything else worth a direct sweep.
- `seen_companies.txt` — Auto-populated dedup list. Don't edit by hand.

## Per-week folders

Created by Stage 1 as `Week_of_YYYY-MM-DD/`. Contains:
- `candidates_YYYY-MM-DD.csv` (Stage 1 output)
- `Master_v3_0_YYYY-MM-DD.csv` (Stage 2 output — the decision-ready list)
- `pre_filter_drops_YYYY-MM-DD.csv` (visibility into what got dropped)
- Optional: `api_verified_YYYY-MM-DD.csv`, `failed_fetches_YYYY-MM-DD.csv`,
  `closed_listings_YYYY-MM-DD.csv`
