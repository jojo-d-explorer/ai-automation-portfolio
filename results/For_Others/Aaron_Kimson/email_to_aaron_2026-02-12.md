**Subject: Your Weekly Job Search Results — Week of Feb 9, 2026**

Hey Aaron,

Hope you're doing well. Wanted to walk you through your first weekly job search run and share some findings, plus a few thoughts on how to tune it going forward.

---

**What we did this week**

I ran your job search prompt across all four ATS boards (Greenhouse, Lever, Ashby, and LinkedIn) targeting the four roles you specified — L/S Hedge Fund Analyst, Hedge Fund PM, Director of Equity Research, and Investment Analyst — across New York, San Francisco, Chicago, Miami, and Boston. The search window was the **last 7 days** (Feb 5–12, 2026).

One important modification: LinkedIn's job board requires an authenticated browser session to access full listings (salary, descriptions, requirements), and the automated search tools were getting blocked by the other ATS platforms' anti-scraping protections. So in addition to the standard web-based searches across all four boards, I also ran a live LinkedIn browser session while logged into your account to pull detailed listings. This made a big difference — the top 3 results all came from that authenticated LinkedIn session.

**Boards used:**
- boards.greenhouse.io
- jobs.lever.co
- jobs.ashbyhq.com
- linkedin.com/jobs (authenticated browser + web search)
- Company career pages (Two Sigma, Point72, Verition, etc.)

---

**Results summary**

| Metric | Count |
|--------|-------|
| Total jobs found (pre-filter) | 40 |
| Jobs scoring 70+ (post-filter) | 24 |
| All marked NEW (first run) | 24 |

Your **top 3 matches** are all strong TMT/software equity fits:

1. **J. Goldman & Co.** — Hedge Fund ER Analyst, TMT (Long/Short) — NYC — $175K–$225K *(Score: 97)*
2. **JPMorganChase** — Equity Research, SMid Technology Senior Analyst, VP — NYC — $200K–$285K *(Score: 95)*
3. **Arootah (Client Placement)** — Investment Analyst, L/S Equity (TMT & Consumer) — NYC — $190K–$200K *(Score: 95)*

The J. Goldman role in particular is almost tailor-made — TMT L/S equity, fundamental research, 4+ years experience, reporting directly to a PM. The JPMorgan role is sell-side but at a significant step up in platform and comp ($200K–$285K base), and the description is nearly identical to your current responsibilities.

---

**Output files**

Three files were generated and saved to `ai-automation-portfolio/results/Aaron/Week_of_2026-02-09/`:

1. **Master_List_2026-02-09.csv** — All 24 qualified jobs (score 70+), ranked by fit score, with company, title, salary, location, work arrangement, summary, rationale, URL, and source board
2. **Top10_New_2026-02-09.csv** — Top 10 highest-scoring new jobs
3. **executed_2026-02-09.txt** — Full log of the search parameters, boards, scoring criteria, and methodology (saved to `searches/prompts/for_others/Aaron/`)

---

**Weekly update process**

The plan is to run this same search every week. Each run will:

- Search the same boards, roles, locations, and filters
- Score against your resume using the same rubric
- Compare against the previous week's Master List to flag **NEW** vs. **REPEAT** jobs — so you only need to focus on what's new each week
- Generate a fresh Master List and Top 10 New file

The comparison file path follows the pattern: `results/Aaron/Week_of_[Monday date]/Master_List_[Monday date].csv`. Next week's run will automatically detect this week's file and mark returning listings as REPEAT.

---

**Suggestions for tuning the prompt**

A few things worth considering to sharpen results in future weeks:

1. **Add specific target companies.** If there are hedge funds you're particularly interested in (e.g., Coatue, Viking, Lone Pine, Whale Rock), I can add a targeted company-by-company career page check in addition to the board searches. Many top funds don't post on public ATS boards.

2. **Adjust the seniority filter.** Right now the scoring gives partial credit to roles that are junior (1–3 years experience) since they still represent buy-side opportunities. If you want to filter those out entirely, we can raise the seniority threshold to exclude anything below 5+ years required experience.

3. **Expand or narrow sectors.** The prompt currently searches broadly (hedge fund analyst, investment analyst, etc.). If you want to focus exclusively on TMT/software/fintech coverage roles, we can tighten the search terms. Conversely, if you're open to covering other sectors on the buy side, we can broaden.

4. **Add recruiter firms as a source.** Several of the best results came through recruiter postings (Selby Jennings, Long Ridge Partners, Arootah placements). We could add targeted searches for posts from top finance recruiters like Odyssey Search Partners, Glocap, or SG Partners.

5. **Miami was a blank.** Zero relevant hedge fund or equity research results in Miami across all boards this week. If that city isn't a real option, dropping it would clean up the search matrix. Alternatively, we could add Stamford, CT or Greenwich, CT since several major hedge funds (Point72, AQR, Bridgewater) are based there.

6. **Salary floor filter.** If you want to automatically exclude anything below a certain base (e.g., $130K), I can add a hard salary floor so those don't appear even if the industry/seniority fit is decent.

Let me know if you want to adjust any of these for next week's run. Happy to dial it in.

Best,
Joey
