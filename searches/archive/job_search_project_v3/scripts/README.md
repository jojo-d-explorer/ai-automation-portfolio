# scripts/

Python helpers for the v3.0 pipeline. Copy these in from your existing
v2.x setup — they don't change.

**Used by v3.0:**
- `classify_url.py` — Called per URL during Stage 1 deduplication
- `ats_api_checker_v2.py` — Optional pass before Stage 2
- `check_urls.py` — Run after Stage 2, before applying

**Deprecated in v3.0 (move to ../archive/):**
- `corpus_append.py` — v3.0 doesn't auto-grow a corpus
- `disqualifiers.json` — v3.0 doesn't filter at the corpus level
