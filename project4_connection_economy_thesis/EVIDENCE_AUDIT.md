# Evidence Audit: What Is Data-Backed vs. Inferred

**Project:** `project4_connection_economy_thesis`  
**Date:** August 2026  
**Audience:** Research consumers who require literature- and data-backed conclusions, not narrative guesses  
**Verdict upfront:** **No — not everything is equally data-backed.** Macro behavioral trends are well-sourced. Sector-level inferences are moderate. Ticker rankings and 10–20 year stock calls are **analyst judgment (Tier C)** and must not be treated as validated forecasts.

---

## Executive Summary

| Layer | What it covers | Evidence quality | Can we be confident? |
|---|---|---|---|
| **Tier A — Primary data** | Federal surveys (SAMHSA, MTF, CDC), SEC filings, computed stock returns | **Strong** | Yes — reproducible |
| **Tier B — Industry / survey data** | Gallup, NIQ, Piper Sandler, McKinsey, Harris Poll, Arival | **Moderate–Strong** | Yes for sector/cohort; not always ticker-specific |
| **Tier C — Analyst judgment** | Composite scores, sector→ticker mapping, scenario probabilities, "Top 10 picks" | **Weak for prediction** | No — explicitly subjective |

**Professional conclusion:** The **behavioral premise** (Gen Z drinks less, uses AI with rising skepticism, seeks IRL connection, over-indexes on wellness) is **data-backed at Tier A/B**. The **investment conclusion** (these 10 stocks will rise over 10–20 years) is **not data-backed** — it is a structured hypothesis requiring ongoing validation.

---

## 1. Evidence Tier Definitions

### Tier A — Primary / Reproducible
- U.S. federal surveys with published methodology (SAMHSA NSDUH, Monitoring the Future, CDC MMWR)
- Company SEC filings and earnings releases (Live Nation 8-K, Roblox shareholder letter)
- Historical stock returns computed from `yfinance` in `scripts/04_score_genz_alpha_stocks.py`

### Tier B — Reputable Secondary / Industry
- Consumer surveys with documented samples (Gallup, Harris Poll, Piper Sandler, Circana/NCSolutions, McKinsey, NIQ scan data, Arival)
- Peer-reviewed literature (Wang et al. 2023 loneliness meta-analysis)
- Market-size forecasts (Grand View Research, Global Industry Analysts)

**Caveat:** Tier B supports **sector and cohort** claims. Applying B-tier data to a specific ticker (e.g., "AI skepticism → buy CRWD") is an **inference**, which we downgrade to Tier C unless ticker-specific proof exists.

### Tier C — Analyst Judgment / Inference
- The 7-factor composite scores (1–5) in `scripts/04_score_genz_alpha_stocks.py`
- Mapping "energy drinks substitute for alcohol" to MNST/CELH without brand-level substitution data
- Scenario probabilities (50% base case, 25% bear, 25% bull)
- Portfolio tier recommendations
- Any 10–20 year "highest likelihood to increase" language

---

## 2. Macro Behavioral Claims — Audit

All 26 statistics in `data/genz_alpha_behavior_trends.csv` have source URLs. Below we rate **claim strength** using primary-source cross-checks added in this audit.

### 2.1 Alcohol decline — **STRONG (Tier A/B)**

| Claim | Our data | Primary cross-check | Verdict |
|---|---|---|---|
| Gen Z plan to drink less (65%) | Circana/NCSolutions 2025 | Consistent with NCSolutions industry survey | **Supported** |
| U.S. adults under 35 who drink (50%) | Gallup via Penn State synthesis | Gallup long-term trend: down from 72% (2001–03) | **Supported** |
| Young adults 18–25 past-month alcohol use fell | *Not in original CSV* | SAMHSA NSDUH: **50.9% → 47.5% (2021–2024)**, statistically significant | **Stronger than survey-only** |
| Adolescent alcohol use at multi-decade lows | *Not in original CSV* | Monitoring the Future 2024: 12th grade past-year use **41.7%** (vs 75% in 1997) | **Strong (Tier A)** |
| Beer volume decline | *Sector, not in behavior CSV* | NIQ 2024: beer volume **−2.9%** (52 wks ending 12/28/2024) | **Supported (Tier B scan data)** |

**What we cannot claim with confidence:** That Gen Z will **permanently** drink less as they age. NIQ Spend Z notes alcohol may grow as cohorts enter legal drinking years — a documented counter-hypothesis.

### 2.2 AI skepticism — **STRONG (Tier B)**

| Claim | Source | Verdict |
|---|---|---|
| 51% Gen Z weekly gen AI use | Gallup/Walton 2026 | **Supported** — primary poll |
| 31% anger, 22% excitement | Gallup 2026 | **Supported** |
| 48% say AI risks outweigh benefits at work | Walton AI Paradox PDF | **Supported** |
| 67% trust human-only work over AI-assisted | Walton AI Paradox | **Supported** |

**What we cannot claim:** That youth AI sentiment **causes** cybersecurity stock outperformance. CRWD/PANW scores lean on Tier C inference.

### 2.3 IRL connection / loneliness — **MODERATE–STRONG (Tier B)**

| Claim | Source | Verdict |
|---|---|---|
| 51% Gen Z weekend loneliness | Harris Poll 2026 PDF | **Supported** — sponsored survey |
| 95% want IRL events from online interests | Eventbrite 2025 | **Supported** — industry report |
| 74% attended concert in past year | Spotify Culture Next 2024 | **Supported** |

**Peer-reviewed anchor:** Wang et al. (2023) confirms loneliness/isolation mortality risk at population level — but **strongest utilization effects are in older adults**, not youth concert attendance.

### 2.4 Wellness / spending power — **MODERATE (Tier B)**

| Claim | Source | Verdict |
|---|---|---|
| Gen Z + millennials = 41% of U.S. wellness spend | McKinsey 2025 | **Supported** — industry research |
| $12T Gen Z spending power by 2030 | NIQ/World Data Lab | **Supported** — forecast, not observed |
| $255B Gen Alpha household influence | Teneo 2026 | **Supported** — industry survey |

### 2.5 Market forecasts — **MODERATE (Tier B, forward-looking)**

`data/genz_alpha_market_forecasts.csv` cites Grand View Research, Arival, etc. These are **industry TAM/CAGR estimates**, not realized revenue. Use for sector sizing only.

---

## 3. Ticker-Level Claims — Audit

Per-ticker citations: `data/genz_alpha_stock_evidence.csv`  
Summary grades: `data/genz_alpha_ticker_evidence_grades.csv` (generated by `scripts/05_build_evidence_audit.py`)

### 3.1 Ticker evidence grades (composite score ≠ evidence grade)

| Evidence grade | Tickers | Meaning |
|---|---|---|
| **Strong** | ELF, RBLX, LYV, MNST, TAP, BUD | ≥2 Tier A claims or 1 Tier A + multiple verified Tier B |
| **Moderate** | CELH, LULU, PEP, BKNG, TJX, ROST, TTWO, NVDA, CRWD, STZ | Mix of Tier B sector data + some Tier A prices/filings |
| **Weak–Moderate** | PLNT, DUOL, ONON, ETSY, KDP, EXPE, ACHC, PANW | Mostly Tier B sector proxies; limited ticker-specific proof |
| **Weak** | HIMS, GOOGL, SAM, VST | Predominantly Tier C inference |

### 3.2 Examples: what IS vs. IS NOT proven

**ELF (Strong)**  
- **Proven:** #1 cosmetics brand among female teens at 35–38% share (Piper Sandler Fall 2024/Spring 2025, Tier A/B).  
- **Not proven:** That this guarantees 10–20 year outperformance (valuation, competition unmodeled).

**MNST (Strong on brand; Weak on alcohol-substitution thesis)**  
- **Proven:** #1 teen energy drink preference (Piper Sandler). Teens prefer energy drinks over coffee/soda.  
- **Not proven:** Energy drinks **substitute for alcohol** in social settings — inferred from Circana NA-spirits data, not MNST substitution elasticities.

**LYV (Strong on operations; Moderate on Gen Z attribution)**  
- **Proven:** 130M+ tickets sold through July 2025 (+6%); $5.1B deferred revenue (+25%) — Live Nation SEC filings (Tier A).  
- **Not proven:** That Gen Z specifically drives margin expansion — Gen Z concert attendance from Spotify/eMarketer surveys (Tier B), not LYV cohort revenue disclosure.

**TAP / BUD / STZ (Strong on sector headwind)**  
- **Proven:** Beer volume −2.9% (NIQ 2024); craft participation among 21–34 down 7pp since 2019 (CGA/NIQ).  
- **Not proven:** These three issuers cannot pivot via NA/RTD — company-specific.

**CRWD / PANW (Weak on Gen Z causal link)**  
- **Proven:** Historical CAGRs from price data (Tier A). Enterprise security TAM growth (Tier B industry).  
- **Not proven:** Gen Z AI **sentiment** drives incremental security spend — enterprise buyers ≠ Gen Z consumers.

**PLNT (Weak–Moderate)**  
- **Proven:** Harris Poll — 65% feel more connected in wellness vs nightlife (Tier B).  
- **Not proven:** Planet Fitness captures this cohort at scale — no published Gen Z membership share in filings.

---

## 4. Composite Scores — Explicitly NOT Data-Derived

The rankings in `data/genz_alpha_stock_scores.csv` (LYV 89, PLNT 82, etc.) are:

1. Hand-assigned 1–5 sub-scores in Python source code  
2. Weighted and scaled to 0–100  
3. **Not** regression coefficients, factor model loadings, or backtest-optimized weights  
4. **Not** validated against forward returns

**Historical cross-check (Tier A price data):** High composite scores did **not** uniformly predict 2019–2026 CAGRs:

| Ticker | Composite | 2019–2026 CAGR |
|---|---:|---:|
| PLNT | 82 | **−0.9%** |
| RBLX | 76 | **−7.7%** |
| CELH | 76 | +52% |
| TAP | 40 | −0.9% |

This disconnect is expected — scores measure **thematic alignment**, not **investment outcome**.

---

## 5. What a Professional Research Desk Would Label Each Document

| Document | Data-backed portions | Speculative portions |
|---|---|---|
| `THESIS_EVALUATION.md` | Surveys, NHE forecasts, basket CAGRs, peer-reviewed loneliness literature | Forward sector calls |
| `GENZ_ALPHA_STOCK_ANALYSIS.md` | Behavioral tables, some ticker citations | Top 10 picks, scenario probabilities, portfolio tiers |
| `genz_alpha_stock_scores.csv` | `historical_cagr_2019_pct` column only | All 7 factor scores and composite |
| `genz_alpha_behavior_trends.csv` | **Fully sourced** (26/26 URLs) | Interpretation of causality |
| Charleston `RESEARCH_PAPER.md` | CDC PLACES tract data, SVI, computed maps | Intervention cost-effectiveness estimates |

---

## 6. Recommended Use — How to Read This Research

**High confidence (act on for sector research):**
- Youth alcohol consumption is declining on multiple federal and survey measures  
- Beer category volume is falling; RTD/NA categories are growing faster  
- Gen Z reports high loneliness and high demand for IRL events  
- AI adoption coexists with rising skepticism among Gen Z  

**Medium confidence (monitor, do not overweight):**
- Experience-economy TAM growth (Arival, Grand View)  
- Specific brand youth affinity (Piper Sandler for ELF, MNST, CELH)  
- Live Nation operational momentum (SEC filings)  

**Low confidence (treat as hypothesis only):**
- Rank-ordered "Top 10 stocks for 10–20 years"  
- AI skepticism → security stock alpha  
- Energy drinks as alcohol substitutes at brand level  
- Scenario probability weights (50/25/25)  
- Hospital vs. experience causal chain (see `THESIS_EVALUATION.md` — **rejected** for hospitals)  

---

## 7. Primary Sources Added in This Audit

| Source | Key finding | Tier |
|---|---|---|
| SAMHSA NSDUH 2024 Data Brief | Young adult (18–25) past-month alcohol use: 50.9% → 47.5% (2021–2024) | A |
| Monitoring the Future 2024 | 12th grade past-year alcohol: 41.7%; long decline from 75% (1997) | A |
| NIQ 2024 BevAl Review | Beer volume −2.9% (52 wks to 12/28/2024) | B |
| Piper Sandler TSWT Fall 2024 | e.l.f. #1 cosmetics 35%; Monster #1 energy drink | B |
| Live Nation Q2 2025 8-K | 130M tickets; $5.1B deferred revenue +25% | A |
| Roblox Feb 2026 shareholder letter | 35% of age-checked DAUs under 13 | A |
| Wang et al. 2023, *Nature Human Behaviour* | Isolation HR 1.32 mortality; loneliness HR 1.14 | A |

---

## 8. Reproducibility

```bash
cd project4_connection_economy_thesis
pip install yfinance pandas
python scripts/03_build_genz_behavior_data.py
python scripts/04_score_genz_alpha_stocks.py
python scripts/05_build_evidence_audit.py
```

| Output | Description |
|---|---|
| `EVIDENCE_AUDIT.md` | This document |
| `data/genz_alpha_stock_evidence.csv` | 60+ per-ticker claims with tier labels |
| `data/genz_alpha_ticker_evidence_grades.csv` | Ticker-level defensibility grades |
| `results/evidence_audit_summary.json` | Machine-readable audit summary |

---

## 9. Bottom Line for the User

**You asked if everything is data-backed.** The honest answer:

- **Behavioral and macro trends:** ~**85% data-backed** (Tier A/B with citations)  
- **Sector headwinds/tailwinds:** ~**70% data-backed** (industry scan data + surveys)  
- **Individual stock rankings:** ~**30% data-backed** (some ticker proof; scores are judgment)  
- **10–20 year return predictions:** ~**0% empirically validated** (not backtested; not falsifiable yet)

This research meets a **professional desk standard for thematic screening**, not for **conviction-weighted portfolio construction**. For the latter, you would need: ticker-level revenue cohort disclosure, factor backtests, valuation overlays, and falsifiable forward hypotheses with defined review dates.

*Research only. Not investment advice.*
