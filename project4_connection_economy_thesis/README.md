# Connection Economy Thesis — Data & Literature Evaluation

Evaluates the investment thesis:

> **Hospital and experience-based stocks will rise in the coming years as youth increasingly pursue real connections and in-person fulfillment.**

This folder combines **public survey data**, **healthcare utilization forecasts**, **experience-economy market indicators**, and **historical stock performance** with a **critical literature review** to assess whether the thesis is supported, partially supported, or overstated.

## Documents

| File | Description |
|---|---|
| [`EVIDENCE_AUDIT.md`](EVIDENCE_AUDIT.md) | **Evidence quality audit** — Tier A/B/C breakdown; what is proven vs inferred |
| [`THESIS_EVALUATION.md`](THESIS_EVALUATION.md) | Full research paper (~7,500 words): hospital vs experience stock thesis — critical evaluation |
| [`GENZ_ALPHA_STOCK_ANALYSIS.md`](GENZ_ALPHA_STOCK_ANALYSIS.md) | Gen Z/Alpha 10–20yr stock analysis: drinking decline, AI skepticism, wellness, scoring 28 tickers |
| [`NOVEL_THESES.md`](NOVEL_THESES.md) | **NEW: 6 novel theses, 18 new tickers** — pet proxy, bar replacement, swipe fatigue, analog economy |
| [`data/`](data/) | Stock prices, survey stats, sector forecasts, Gen Z/Alpha scores (CSV) |
| [`results/thesis_evidence_summary.json`](results/thesis_evidence_summary.json) | Machine-readable connection-economy summary |
| [`results/genz_alpha_rankings.json`](results/genz_alpha_rankings.json) | Top/bottom Gen Z/Alpha stock rankings |

## Headline verdict

| Component | Verdict | Confidence |
|---|---|---|
| Youth loneliness + desire for IRL connection | **Supported** | High (multiple surveys) |
| Experience economy sector growth | **Supported** | High (market data) |
| Experience stocks will *outperform* because of youth | **Partially supported** | Medium — growth yes, stock causality weak |
| Hospital stocks will rise *because youth seek connection* | **Weak / Rejected as causal mechanism** | High — demographics & acuity dominate |
| Hospital stocks will rise *in absolute terms* | **Partially supported** | Medium — sector grows, but outpatient > inpatient |

**Overall thesis grade: C+ (directionally plausible for experiences; causal link to hospitals unsupported)**

## Quick start

```bash
pip install yfinance pandas
cd project4_connection_economy_thesis
python scripts/01_download_stock_data.py
python scripts/02_build_evidence_tables.py
python scripts/03_build_genz_behavior_data.py
python scripts/04_score_genz_alpha_stocks.py
python scripts/06_build_novel_theses.py
```

## Novel theses (NEW — not in original 28-stock basket)

Six underexplored angles with **18 different tickers**: TRUP, WMG, PLAY, MODG, HAS, MTCH (contrarian), CHWY, AFRM, and more.

| Thesis | Top picks | Key data |
|---|---|---|
| Bar Replacement | PLAY, MODG, FUN | 73% want alcohol-optional settings (Harris) |
| Pet Parent Proxy | TRUP, CHWY, IDXX | 70% of new pet insurance buyers under 40 |
| Swipe Fatigue | Short MTCH, long PLAY/MODG | 79% Gen Z dating app burnout |
| Analog Connection | WMG, HAS, PINS | Vinyl $1.04B; Gen Z drives format |
| Sleep Maxxing | TPX, RMD | 56% guilt after disruptive nights |
| Home Social Hub | WING, DPZ, CHWY | 74% staying in is top weekend activity |

See [`NOVEL_THESES.md`](NOVEL_THESES.md) for full analysis, pair trades, and critical evaluation.

**Not everything is equally data-backed.** See [`EVIDENCE_AUDIT.md`](EVIDENCE_AUDIT.md) for the full audit.

| Layer | Confidence |
|---|---|
| Macro behavioral trends (alcohol ↓, AI skepticism, loneliness) | **High** (Tier A/B — SAMHSA, Gallup, Harris, etc.) |
| Sector data (beer −2.9% volume, mocktail TAM) | **Medium–High** (NIQ, industry forecasts) |
| Historical stock CAGRs | **High** (computed from yfinance) |
| Composite rankings & "Top 10 picks" | **Low for prediction** (Tier C analyst judgment) |
| 10–20 year return forecasts | **Not validated** |

## Gen Z / Gen Alpha stock analysis

**Top scored tickers (100-point scale, Tier C judgment):** LYV (89), PLNT (82), MNST (81), LULU/ELF (79), DUOL (78)

**Strongest ticker-level evidence (Tier A/B):** ELF (#1 teen cosmetics), MNST (#1 teen energy drink), RBLX (35% U13 DAUs), LYV (130M tickets), TAP/BUD (beer volume headwinds)

**Structural avoids:** TAP (40), BUD/STZ (43) — alcohol volume headwinds

**Key behavioral drivers:**
- 65% of Gen Z plan to drink less; 39% dry all year (NCSolutions)
- 31% angry about AI, 22% excited — skepticism rising (Gallup 2026)
- 41% of U.S. wellness spend from Gen Z/millennials (McKinsey)
- $12T Gen Z spending power by 2030 (NIQ)

See [`GENZ_ALPHA_STOCK_ANALYSIS.md`](GENZ_ALPHA_STOCK_ANALYSIS.md) for full thematic deep dives, scenario analysis, and critical caveats.

## Stock baskets analyzed

**Hospital operators:** HCA, THC, UHS, CYH, EHC, ACHC  
**Experience-based:** LYV, MTN, EXPE, BKNG, RCL, CCL, PLNT, MSGS, MANU, FUN, DKNG, DIS, NCLH  
**Benchmarks:** SPY, XLV, XLY

## Key data findings (2019–present)

| Basket | CAGR | Total return |
|---|---:|---:|
| Hospital operators (equal-weight) | 20.6% | +315% |
| Experience-based (equal-weight) | 7.6% | +74% |
| SPY (benchmark) | ~17.7% | ~+246% |

Hospital stocks outperformed experience stocks historically — but largely due to operator-specific turnarounds (e.g., THC) and post-COVID utilization recovery, **not** youth connection demand.

## Disclaimer

This is research and critical analysis, **not investment advice**. Stock performance uses past data; survey statistics come from industry-sponsored and academic sources with varying methodology quality.
