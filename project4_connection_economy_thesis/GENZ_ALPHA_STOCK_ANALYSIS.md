# Gen Z & Generation Alpha: A 10–20 Year Stock Alignment Analysis

**Companion to:** `THESIS_EVALUATION.md` (connection economy thesis)  
**Date:** August 2026  
**Horizon:** 2026–2046 (10–20 years)  
**Method:** Behavioral survey synthesis + market forecasts + 7-factor thematic stock scoring + historical performance validation  
**Evidence audit:** See [`EVIDENCE_AUDIT.md`](EVIDENCE_AUDIT.md) — **not all conclusions are equally data-backed**

---

## Evidence Quality (Read First)

| Component | Tier | Confidence |
|---|---|---|
| Macro behavioral trends (alcohol ↓, AI skepticism, loneliness, wellness) | A/B | **High** — federal surveys + cited industry polls |
| Sector headwinds/tailwinds (beer volume, mocktail TAM, experiences market) | B | **Medium–High** — NIQ scan data, industry forecasts |
| Historical stock CAGRs (2019–2026) | A | **High** — computed from Yahoo Finance |
| Per-ticker youth brand affinity (ELF, MNST, RBLX, LYV ops data) | A/B | **Medium–High** — Piper Sandler, SEC filings |
| Composite scores & "Top 10" rankings | C | **Low for prediction** — expert judgment, not backtested |
| 10–20 year "highest likelihood to rise" | C | **Not validated** — thematic hypothesis only |

**Bottom line:** This document is suitable for **thematic screening**, not conviction-weighted stock picking without additional valuation and cohort-revenue analysis.

Per-ticker claim citations: `data/genz_alpha_stock_evidence.csv`

## Executive Summary

Generation Z (born ~1997–2012) and Generation Alpha (born ~2010–2024) will command an estimated **$12 trillion in spending power by 2030** (NIQ) and already influence **$255 billion in U.S. household purchases** (Teneo). Their documented behavioral shifts — declining alcohol consumption, rising AI skepticism, hunger for in-person connection, wellness prioritization, thrift/authenticity values, and gaming-native socialization — create long-horizon tailwinds and headwinds across consumer and healthcare sectors.

This analysis scores **28 publicly traded equities** across eight thematic clusters using seven weighted factors (behavioral fit, demographic tailwind, cultural momentum, alcohol-shift benefit, AI-skepticism benefit, 10-year moat, execution risk). Results are cross-validated against 2019–2026 historical returns.

### Top 10 stocks by composite alignment score (100-point scale)

*Scores are Tier C analyst judgment — see evidence grades in [`EVIDENCE_AUDIT.md`](EVIDENCE_AUDIT.md)*

| Rank | Ticker | Company | Theme | Score | Key driver |
|---:|---|---|---|---:|---|
| 1 | **LYV** | Live Nation | IRL experiences | **89** | Human irreplaceability + concert culture |
| 2 | **PLNT** | Planet Fitness | Wellness social | **82** | Low-cost Third Space; sober socializing |
| 3 | **MNST** | Monster Beverage | NA/functional drinks | **81** | Alcohol substitute in social contexts |
| 4 | **LULU** | Lululemon | Wellness social | **79** | Community fitness + brand cachet |
| 5 | **ELF** | e.l.f. Beauty | Clean beauty/value | **79** | Affordable affluence; TikTok-native |
| 6 | **DUOL** | Duolingo | Human skills | **78** | Skill-building > AI shortcuts |
| 7 | **CELH** | Celsius | Functional beverages | **76** | Wellness drinks over alcohol |
| 8 | **ONON** | On Holding | Wellness social | **76** | Running club culture |
| 9 | **RBLX** | Roblox | Gen Alpha gaming | **76** | Alpha's primary social platform |
| 10 | **ETSY** | Etsy | Authentic/thrift | **76** | Human creators; anti-mass-market |

### Bottom 5 (structural headwinds)

| Ticker | Company | Score | Primary headwind |
|---|---|---:|---|
| TAP | Molson Coors | 40 | Gen Z beer volume collapse |
| BUD | Anheuser-Busch InBev | 43 | Same + weak NA pivot |
| STZ | Constellation Brands | 43 | Spirits/beer exposure |
| SAM | Boston Beer | 57 | Transitional; core still alcoholic |
| VST | Vista Outdoor | 59 | Execution uncertainty |

### Critical nuance upfront

**Gen Z's relationship with AI is a paradox, not a boycott.** 51% use generative AI weekly, yet anger (31%) exceeds excitement (22%) and 48% say risks outweigh benefits at work (Gallup/Walton 2026). The investment implication is **not** "short AI" — it is **long human-authentic layers** (live events, physical wellness, handmade goods, in-person mental health) while recognizing AI infrastructure (NVDA, hyperscalers) may still compound regardless of sentiment.

**Alcohol decline is real but not absolute.** 65% of Gen Z plan to drink less in 2025, yet 50% of under-35s still drink — and NIQ notes alcohol category growth may occur as Gen Z ages into legal drinking. The winning trade is **substitution** (functional/NA beverages), not assuming zero alcohol revenue forever.

---

## 1. Documented Behavioral Shifts (Data Foundation)

### 1.1 The sober-curious generation: alcohol decline

| Statistic | Value | Source |
|---|---:|---|
| Gen Z planning to drink less in 2025 | **65%** | NCSolutions/Circana |
| Gen Z adopting dry lifestyle all year | **39%** | NCSolutions |
| U.S. adults under 35 who drink alcohol | **50%** (down from 72% in 2001–03) | Gallup |
| Gen Z cutting back for mental health | **58%** | Circana |
| Gen Z who tried non-alcoholic spirits | **42%** | Circana |
| Americans trying to drink less (all ages) | **49%** (+44% since 2023) | NCSolutions |

**Mechanism:** Mental health prioritization (86% say mental health as important as physical health when deciding to drink — Circana), financial pressure, and social media normalization of sobriety. Federal data confirms the trend: SAMHSA NSDUH shows young adults 18–25 past-month alcohol use fell from **50.9% (2021) to 47.5% (2024)**; Monitoring the Future shows 12th-grade past-year alcohol use at **41.7%** vs **75% in 1997**.

*Removed:* prior unsourced claim of "20–30% less alcohol per capita vs millennials" — not found in primary literature with that exact figure.

**Market response:** RTD mocktail market projected **$8.3B → $12.2B by 2030** (5.7% CAGR); non-alcoholic spirits **$7.2B → $11.0B** (7.2% CAGR). Retailers expanding dedicated NA shelf space.

**Investment implication:** Long **substitutes** (MNST, CELH, KDP, PEP); underweight **pure-play beer/spirits** (TAP, BUD, STZ) unless NA portfolio transition accelerates.

### 1.2 The AI paradox: adoption without trust

| Statistic | Value | Source |
|---|---:|---|
| Gen Z using generative AI weekly | **51%** (steady) | Gallup 2026 |
| Anger about AI | **31%** (+9 pp YoY) | Gallup 2026 |
| Anxiety about AI | **42%** (steady) | Gallup 2026 |
| Excitement about AI | **22%** (−14 pp YoY) | Gallup 2026 |
| AI risks outweigh benefits (workplace) | **48%** | Walton AI Paradox |
| Trust human-only work over AI-assisted | **67%** | Walton AI Paradox |
| Believe AI helps creativity | **31%** (down from 42%) | Gallup 2026 |

**Mechanism:** Gen Z entered the workforce during AI hype cycle, then experienced AI-generated job displacement anxiety, academic integrity concerns, and degraded social media (AI slop). Anger overtook hopefulness as the dominant secondary emotion after anxiety in 2026.

**Investment implication:**
- **Beneficiaries of distrust:** Cybersecurity (CRWD, PANW), human-verified experiences (LYV), authentic creator marketplaces (ETSY), in-person mental health (ACHC)
- **Paradox plays:** AI infrastructure (NVDA) and platforms (GOOGL) — usage continues despite resentment
- **At risk:** Pure AI-content farms, AI tutoring replacing human instruction without oversight, deepfake-vulnerable social platforms

### 1.3 Connection hunger: IRL over URL

(Cross-reference: `THESIS_EVALUATION.md`)

| Statistic | Value |
|---|---:|
| Gen Z weekend loneliness | 51% |
| Want IRL events from online interests | 95% |
| Attended concert/live show (past year) | 74% |
| Formed close friend through interest event | 84% |

**Beneficiaries:** LYV, PLNT, LULU, ONON, BKNG/EXPE (event travel)

### 1.4 Wellness as identity, not product

| Statistic | Value | Source |
|---|---:|---|
| Gen Z + millennials' share of U.S. wellness spend | **41%** (vs 36% population share) | McKinsey 2025 |
| Gen Z "mindfulness very high priority" | **42%** | McKinsey |
| U.S. mental health market (2025) | **$33.4B** | Industry est. |
| Gen Z wellness spend focus vs older gens | Discretionary (wearables, apps, self-care) vs basics | eMarketer/McKinsey |

**Beneficiaries:** PLNT, LULU, ONON, CELH, MNST, ELF, HIMS, ACHC

### 1.5 Value, thrift, and authenticity

| Statistic | Value | Source |
|---|---:|---|
| Gen Z more likely to buy secondhand | +8 pp vs average | GWI |
| Plan vintage/upcycled holiday purchases | **63%** | PwC |
| Willing to buy private-label "dupes" | **41%** | PwC |
| Gen Alpha: style/looks top purchase criteria | **50%** | Teneo |

**Beneficiaries:** TJX, ROST, ETSY, ELF (affordable affluence)

**Gen Alpha nuance:** Teneo finds Alpha **less** motivated by sustainability ethics than Gen Z — they prioritize **style, quality, price** (millennial-parent pragmatism). Do not assume Gen Z ESG preferences automatically transfer.

### 1.6 Gaming and Gen Alpha native platforms

| Statistic | Value | Source |
|---|---:|---|
| Gen Z more likely to buy in-game items | +36% vs average | GWI |
| Gen Z digital game purchase preference | +33% vs average | GWI |
| Gen Alpha influencing household entertainment spend | >50% | Teneo/LEK |

**Beneficiaries:** RBLX (Alpha primary), TTWO; **risk:** platform regulation, AI-generated content flooding games

---

## 2. Scoring Methodology

Each stock receives scores of **1–5** on seven dimensions:

| Dimension | Weight | Definition |
|---|---:|---|
| Behavioral fit | 20% | Alignment with documented Gen Z/Alpha behaviors |
| Demographic tailwind | 15% | Exposure to rising youth spending 2026–2046 |
| Cultural momentum | 15% | Brand relevance / social currency with youth |
| Alcohol-shift benefit | 10% | Gains from sober-curious / NA substitution |
| AI-skepticism benefit | 15% | Gains when consumers prefer human/authentic |
| 10-year moat | 15% | Durable competitive advantage |
| Execution risk | 10% | Inverse — operational/regulatory reliability |

Composite score = weighted sum × 20, scaled to **0–100**.

**Limitations:** Scores are expert-judgment informed by data (**Tier C**), not regression output. They do not incorporate current valuation (P/E), balance sheet, or macro rates. A high score ≠ buy recommendation. Several rationales (e.g., MNST as alcohol substitute, CRWD from AI skepticism) are **sector inferences** without ticker-level causal proof — see `data/genz_alpha_stock_evidence.csv`.

Full scores: `data/genz_alpha_stock_scores.csv`

---

## 3. Thematic Deep Dives & Stock Rationale

### Theme A: IRL experiences & wellness social (Highest conviction)

**Thesis:** AI cannot replicate the physiological and social experience of a live concert, a running club, or a gym community. Gen Z's AI anger (+9 pp) correlates with preference for **verified human presence**.

**Top picks:**

**Live Nation (LYV) — Score 89**
- 74% of Gen Z attended a live show; 67% traveled out-of-state for events
- Deferred revenue +25% YoY (2025); 130M tickets sold
- **Moat:** Artist relationships, venue ownership, ticketing infrastructure
- **Risks:** DOJ antitrust action; ticket price affordability backlash; recession discretionary cut

**Planet Fitness (PLNT) — Score 82**
- Harris Poll: 65% of Gen Z feel more socially connected in wellness settings vs nightlife
- $10–25/month = affordable Third Space vs bars
- **Risks:** Historical stock underperformance; churn; GLP-1 body-composition shifts

**Lululemon (LULU) / On Holding (ONON) — Scores 79/76**
- Community-run clubs (Lulu) and running culture (On) convert fitness to social identity
- Gen Z wellness spend over-indexes on discretionary categories

### Theme B: NA & functional beverages (Alcohol substitution)

**Thesis:** 65% of Gen Z plan to drink less; 42% tried NA spirits. Energy and functional drinks capture **social ritual without ethanol**.

**Top picks:**

**Monster (MNST) — Score 81**
- **Data-backed:** #1 preferred energy drink among U.S. teens (Piper Sandler Fall 2024); teens prefer energy drinks (39%) over coffee (31%)
- **Inferred (Tier C):** Alcohol-substitution thesis — not brand-specific
- Historical price CAGR 18.8% (2019–2026) validates market preference but not forward causality

**Celsius (CELH) — Score 76**
- Fitness-forward positioning; 52% historical CAGR
- **Risk:** Competition intensifying; fad risk

**Keurig Dr Pepper (KDP) — Score 70**
- Distribution scale for NA RTD; lower cultural momentum than MNST/CELH

**Avoid:** TAP (40), BUD (43), STZ (43) — structural volume decline with insufficient NA offset

### Theme C: AI skepticism beneficiaries

**Thesis:** Distrust ≠ non-use. As AI proliferates, Gen Z demands **security, authenticity, and human skill verification**.

**Top picks:**

**CrowdStrike (CRWD) / Palo Alto (PANW) — Score 68 each**
- **Data-backed:** Historical CAGRs 43% / 39% (2019–2026); enterprise security TAM growth
- **Inferred (Tier C):** Gen Z AI anxiety → security spend — buyers are enterprises, not consumers

**Duolingo (DUOL) — Score 78**
- Gamified human skill acquisition; Gen Z doubts AI for learning (46% believe AI helps learning, down 7 pp)
- **Paradox:** DUOL uses AI internally — platform trust depends on perceived human progress

**Etsy (ETSY) — Score 76**
- Handmade/human creator authenticity; anti-AI-slop consumer preference
- 63% of Gen Z plan vintage/upcycled purchases

### Theme D: Mental & behavioral health services

**Thesis:** 51% weekend loneliness; $33B mental health market growing 8%+ CAGR. Gen Z prefers human therapists over AI chatbots for mental health (consistent with 67% human-work trust).

**Acadia Healthcare (ACHC) — Score 71**
- Inpatient/outpatient behavioral facilities
- Youth MH ED visits remain elevated for overdose; structural demand

**Hims & Hers (HIMS) — Score 69**
- Gen Z-native telehealth brand for mental health, dermatology, wellness
- **Risk:** AI-adjacent model; regulatory; competition

### Theme E: Value, thrift, affordable affluence

**Thesis:** PwC: Gen Z cutting spending 13% (2025) but still buying "affordable affluence" — ELF cosmetics, resale sneakers, dupes.

**ELF Beauty (ELF) — Score 79**
- **Data-backed:** #1 cosmetics brand among female teens at 35% share, +6pp YoY (Piper Sandler Fall 2024); maintained #1 through Fall 2025
- 36.7% historical CAGR; TikTok-native distribution

**TJX (TJX) / Ross (ROST) — Scores 71/68**
- Off-price treasure hunt aligns with thrift values
- TJX: 20% historical CAGR; durable moat in off-price retail

### Theme F: Gen Alpha gaming & platforms

**Thesis:** Gen Alpha influences $255B household spend; Roblox is primary social platform for under-13 cohort.

**Roblox (RBLX) — Score 76**
- UBS: 60% of Gen Alpha discovered brands via gaming; 50%+ interact with in-game ads
- **Risks:** −7.7% historical CAGR; platform safety; AI content moderation costs

**Take-Two (TTWO) — Score 66**
- GTA VI cycle; F2P microtransactions (+36% Gen Z in-game spend propensity)

### Theme G: Event-driven travel

**BKNG (73) / EXPE (66)**
- Travel experiences market +17% YoY; 48% of 18–34 plan trips around events
- Experiences online booking only 33% — digital penetration runway

---

## 4. Critical Evaluation: What Could Break This Analysis

### 4.1 Gen Z may age into drinking (NIQ counterpoint)

NIQ's Spend Z report notes alcohol and health as **dynamic growth categories through 2030** as Gen Z ages into peak drinking years. Gallup's 50% under-35 drinking rate could **rise** toward millennial norms — as happened partially with cannabis normalization.

**Mitigation:** Focus on **beverage companies with NA optionality** (PEP, KDP) rather than binary alcohol shorts. Monitor cohort drinking rates annually.

### 4.2 AI skepticism may be a phase, not a permanent preference

Every generation reacts against new technology (television, internet, smartphones) then integrates it. Gen Z still uses AI weekly (51%). By 2035, Alpha — raised entirely with AI — may show **less anger, more normalization**.

**Mitigation:** Own AI infrastructure (NVDA) as hedge; prioritize companies where **human premium persists** regardless of AI adoption (concerts, therapy, handmade goods).

### 4.3 Affordability ceiling

Harris: 85% of Gen Z use cost workarounds for socializing. LYV ticket inflation, LULU premium pricing, and concert travel may hit demand walls. PwC: Gen Z cutting holiday spend 23%.

**Mitigation:** Favor **accessible** Third Spaces (PLNT at $15/mo) over premium (LULU). Monitor BNPL delinquency as leading indicator.

### 4.4 Gen Alpha ≠ Gen Z

Teneo: Alpha cares about **style over sustainability**; less ethical consumption than Gen Z. Mastercard: Alpha will have **$5.5T economic influence by 2029** but through **parental proxy** — different investment pathway (RBLX, DIS, toy/gaming) vs Gen Z direct spend (ELF, LYV).

### 4.5 Historical performance ≠ future alignment

| Stock | Composite Score | 2019–2026 CAGR |
|---|---:|---:|
| CELH | 76 | **+52%** |
| CRWD | 68 | **+43%** |
| ELF | 79 | **+37%** |
| LYV | 89 | +19% |
| PLNT | 82 | **−0.9%** |
| RBLX | 76 | **−7.7%** |
| TAP | 40 | varies |

High alignment scores did not uniformly predict past returns — valuation, timing, and idiosyncratic factors dominate 7-year windows. **10–20 year horizon** is the appropriate test, not yet observable.

### 4.6 Regulatory and antitrust

- **LYV:** DOJ lawsuit risk
- **RBLX:** Child safety regulation
- **HIMS:** Telehealth prescribing rules
- **CRWD/PANW:** Government contract cycles

---

## 5. Scenario Analysis (2036)

*Illustrative hypotheses only (Tier C) — probabilities are not econometrically estimated.*

| Scenario | Probability | Winners | Losers |
|---|---|---|---|
| **Base: "Authentic premium"** | 50% | LYV, PLNT, MNST, ELF, ETSY | TAP, BUD |
| **Bear: Recession + AI normalization** | 25% | TJX, ROST, PEP (staples) | LULU, LYV, CELH |
| **Bull: Alpha supercycle + wellness boom** | 25% | RBLX, ACHC, CELH, ONON | Legacy alcohol, department stores |

---

## 6. Thematic Screening Framework (Illustrative, Not Advice)

*Tier C portfolio construction — for research organization only*

### Tier 1 — Strongest ticker-level evidence + thematic fit
- **LYV** — irreplaceable human experience
- **MNST** — alcohol substitution ritual
- **PLNT** — affordable wellness Third Space
- **ELF** — affordable affluence beauty

### Tier 2 — Strong thematic fit with moderate risk
- **DUOL** — human skill premium
- **ETSY** — authentic creator economy
- **CELH** — functional wellness drinks
- **TJX** — thrift/value alignment

### Tier 3 — Paradox hedges & Gen Alpha optionality
- **RBLX** — Gen Alpha platform exposure
- **CRWD** — AI-security regardless of sentiment
- **ACHC** — youth mental health structural demand

### Underweight / avoid (behavioral headwinds)
- **TAP, BUD, STZ** — alcohol volume decline
- Pure AI-content plays without human verification layer

---

## 7. Conclusion

Gen Z and Gen Alpha are reshaping consumer markets through **simultaneous, sometimes contradictory forces**: drinking less but socializing more (in different venues); using AI but resenting it; spending less overall but splurging on wellness and experiences that feel **authentic and shareable**.

The highest-**evidence** 10–20 year equity themes are:

1. **Human irreplaceability** — live events, physical community, in-person care *(Tier B surveys + Tier A LYV ops data)*
2. **Alcohol substitution at category level** — functional/NA beverages over beer *(Tier A/B: NSDUH, NIQ beer −2.9%)*
3. **Affordable affluence with proven youth share** — ELF (#1 teen cosmetics), off-price retail *(Tier A/B: Piper Sandler, GWI)*
4. **Gen Alpha platform exposure** — RBLX (35% age-checked DAUs under 13) *(Tier A: SEC filing)*

Themes with **weaker ticker-level proof:** AI skepticism → cybersecurity; loneliness → hospital/behavioral chains.

The thesis that these forces will lift **hospital stocks** (per the parent connection-economy analysis) remains weak. **Behavioral health outpatient** (ACHC) has partial alignment; acute hospital operators do not.

**Overall Gen Z/Alpha stock framework grade: B− for thematic screening** — strong macro behavioral data, selective ticker proof, but composite rankings overstate predictive confidence. See [`EVIDENCE_AUDIT.md`](EVIDENCE_AUDIT.md) for full tier breakdown.

---

## References

SAMHSA. (2024). *NSDUH data brief: Trends in substance use among young adults*. https://www.samhsa.gov/data/sites/default/files/reports/rpt56978/2024-nsduh-data-brief-young-adult.pdf

Monitoring the Future / NIH. (2024). *Reported use of most drugs among adolescents remained low in 2024*. https://www.nih.gov/news-events/news-releases/reported-use-most-drugs-among-adolescents-remained-low-2024

NIQ. (2025). *2024 beverage alcohol year in review*. https://nielseniq.com/global/en/insights/analysis/2025/2024-beverage-alcohol-year-in-review/

Piper Sandler. (2024). *Taking Stock With Teens Fall 2024 infographic*. https://www.pipersandler.com/sites/default/files/document/TSWT_Fall24_Infographic.pdf

Circana. (2025). *Sober curious nation alcohol survey*. https://www.circana.com/post/sober-curious-nation-alcohol-survey

Gallup / Walton Family Foundation / GSV Ventures. (2026). *The AI Paradox: Gen Z's relationship with artificial intelligence*. https://news.gallup.com/poll/708224/gen-adoption-steady-skepticism-climbs.aspx

Grand View Research. (2024). *Ready-to-drink mocktails market report*. https://www.grandviewresearch.com/industry-analysis/ready-to-drink-mocktails-market-report

GWI. (2025). *Gen Z spending habits 2025*. https://www.gwi.com/blog/gen-z-spending-habits

Harris Poll. (2026). *The Gen Z Weekend Report*. https://theharrispoll.com/wp-content/uploads/2026/07/The-Gen-Z-Weekend-Report-July-2026.pdf

McKinsey & Company. (2025). *Future of wellness trends*. https://www.mckinsey.com/industries/consumer-packaged-goods/our-insights/future-of-wellness-trends

NIQ. (2025). *Spend Z: Gen Z spending power report*. https://nielseniq.com/global/en/landing-page/spend-z/

NCSolutions. (2025). *Sober curious consumer sentiment survey*. https://www.bevindustry.com/articles/97226-new-ncsolutions-survey-shows-americans-plan-to-drink-less-in-2025

Penn State Extension. (2025). *Alcoholic beverage trends 2025* (Gallup/NCSolutions synthesis). https://extension.psu.edu/alcoholic-beverage-trends-2025

PwC. (2025). *Gen Z consumer trends*. https://www.pwc.com/us/en/industries/consumer-markets/library/gen-z-consumer-trends.html

Teneo. (2026). *Gen Alpha consumer influence study*. https://www.teneo.com/app/uploads/2026/01/Gen-Alpha-Consumer-Influence-Study.pdf

UBS. (2025). *The Alpha consumer*. https://www.ubs.com/global/en/investment-bank/insights-and-data/2025/the-alpha-consumer.html

Wang, F., et al. (2023). Social isolation, loneliness and mortality. *Nature Human Behaviour*, 7, 1307–1319.

---

## Appendix: Reproducibility

```bash
cd project4_connection_economy_thesis
pip install yfinance pandas
python scripts/03_build_genz_behavior_data.py
python scripts/04_score_genz_alpha_stocks.py
python scripts/05_build_evidence_audit.py
```

| File | Description |
|---|---|
| [`EVIDENCE_AUDIT.md`](EVIDENCE_AUDIT.md) | **Evidence tier audit** — what is proven vs inferred |
| `data/genz_alpha_behavior_trends.csv` | 34 survey statistics by theme (all with URLs) |
| `data/genz_alpha_stock_evidence.csv` | Per-ticker claims with Tier A/B/C labels |
| `data/genz_alpha_ticker_evidence_grades.csv` | Ticker defensibility grades |
| `data/genz_alpha_market_forecasts.csv` | Sector TAM/CAGR forecasts |
| `data/genz_alpha_stock_scores.csv` | 28 tickers with 7-factor scores (Tier C) |
| `results/evidence_audit_summary.json` | Machine-readable audit summary |
| `results/genz_alpha_rankings.json` | Top/bottom rankings + theme averages |

*Research only. Not investment advice. Past performance does not guarantee future results.*
