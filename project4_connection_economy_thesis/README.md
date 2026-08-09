# Connection Economy Thesis — Data & Literature Evaluation

Evaluates the investment thesis:

> **Hospital and experience-based stocks will rise in the coming years as youth increasingly pursue real connections and in-person fulfillment.**

This folder combines **public survey data**, **healthcare utilization forecasts**, **experience-economy market indicators**, and **historical stock performance** with a **critical literature review** to assess whether the thesis is supported, partially supported, or overstated.

## Documents

| File | Description |
|---|---|
| [`THESIS_EVALUATION.md`](THESIS_EVALUATION.md) | Full research paper (~7,500 words): abstract, methods, data results, literature, critical claim evaluation, graded verdict, investment implications |
| [`data/`](data/) | Stock prices, survey stats, sector forecasts (CSV) |
| [`results/thesis_evidence_summary.json`](results/thesis_evidence_summary.json) | Machine-readable evidence summary |

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
```

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
