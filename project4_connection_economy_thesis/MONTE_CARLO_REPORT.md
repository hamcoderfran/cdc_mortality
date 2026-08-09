# Monte Carlo Exploration: Gen Z / Gen Alpha Cohort Maturity (2026–2041)

**Method:** 10,000 stochastic simulations × 15 years × 47 stocks × 16 behavioral factors  
**Interactive dashboard:** [`results/maps/monte_carlo_dashboard.html`](results/maps/monte_carlo_dashboard.html)  
**Data:** [`data/monte_carlo_stock_results.csv`](data/monte_carlo_stock_results.csv)

---

## Executive Summary

This simulation explores **which stocks are most likely to receive cumulative thematic tailwinds** (lift) vs **headwinds** (crush) as Gen Z enters peak spending (~2030) and Gen Alpha follows (~2036–2040).

**What it models:** Thematic cohort exposure only — not P/E, rates, buybacks, or total returns.

### Headline results

| Category | Top names | Key probability |
|---|---|---|
| **Most likely LIFTED** | TRUP, CHWY, IDXX, MNST, PLNT | TRUP: **75% P(net positive)**, **54% P(top quartile)** |
| **Most likely CRUSHED** | MTCH, BUD, STZ, BMBL, TAP | MTCH: **53% P(bottom quartile)**, median **−3.0%** thematic |
| **Strong but volatile** | NVDA, RBLX | High lift *and* fat left tail (factor volatility) |
| **Surprisingly neutral** | LYV, ELF, WMG, PLAY | Positive median but rarely top-quartile |

---

## 1. What This Simulation Is (and Is Not)

### IS
- A **Monte Carlo exploration** of 16 latent behavioral-economic factors with priors anchored to survey/industry data
- A **relative ranking** tool: which names benefit if documented Gen Z/Alpha trends persist with uncertainty
- A way to stress-test **regime reversals** (8% annual probability each factor flips direction)

### IS NOT
- A forecast of actual stock prices or total returns
- A backtest or econometric factor model (loadings are thematic judgments from research)
- Investment advice

**Lift** = cumulative thematic alpha **> 10%** over 2026–2041  
**Crush** = cumulative thematic alpha **< −10%**  
**Top quartile** = finishes in top 25% of all 47 stocks in that simulation path

---

## 2. Model Architecture

```
Year t (2026…2040):
  ├── Simulate 16 factors via AR(1) with drift + vol + regime flips
  ├── Cohort weight = 0.55 × GenZ(t) + 0.45 × GenAlpha(t)  [logistic ramps]
  └── Stock thematic return = Σ (loading × Δfactor × cohort × execution_quality) + noise

Cumulative thematic alpha = sum of annual thematic returns over 15 years
```

### Sixteen factors (prior annual drift)

| Factor | Drift | Interpretation |
|---|---:|---|
| `pet_connection` | **+7.0%** | Pet insurance, premiumization (fastest tailwind) |
| `ai_infra_paradox` | +6.0% | AI capex cycle (NVDA) |
| `sober_social_venues` | +5.5% | Eatertainment, competitive social |
| `gen_alpha_gaming` | +5.0% | Alpha platform spend |
| `na_functional_bev` | +4.5% | Alcohol substitution drinks |
| `analog_tactile` | +4.0% | Vinyl, board games, crafts |
| `irl_experiences` | +4.0% | Concerts, event travel |
| `wellness_third_space` | +3.5% | Gym/run club social |
| `cybersecurity` | +3.5% | Enterprise security TAM |
| `sleep_wellness` | +3.0% | Sleep-over-nightlife |
| `mental_health_services` | +3.0% | Behavioral health |
| `value_thrift` | +2.5% | Off-price, dupes |
| `home_social_hub` | +2.0% | Stay-in, delivery |
| `ai_platform_sentiment` | **−1.5%** | Gen Z AI anger → platform risk |
| `alcohol_headwind` | **−2.5%** | Beer/spirits volume |
| `swipe_fatigue` | **−5.0%** | Dating app monetization decline |

Each factor also carries volatility and 8%/year regime-flip risk (e.g., Gen Z ages into drinking, AI sentiment normalizes).

---

## 3. Most Likely to Be LIFTED (2026–2041)

Ranked by **P(top quartile)** across all simulations:

| Rank | Ticker | Company | P(top Q) | P(net +) | Median α | P(lift >10%) |
|---:|---|---|---:|---:|---:|---:|
| 1 | **TRUP** | Trupanion | **53.6%** | 75.3% | +6.2% | 32.4% |
| 2 | **CHWY** | Chewy | 47.5% | 74.5% | +5.0% | 25.2% |
| 3 | **IDXX** | Idexx Labs | 42.4% | 72.5% | +4.3% | 19.7% |
| 4 | **MNST** | Monster Beverage | 37.7% | 72.0% | +3.6% | 14.2% |
| 5 | **PLNT** | Planet Fitness | 34.6% | 68.8% | +3.1% | 13.4% |
| 6 | **NVDA** | NVIDIA | 34.0% | 61.8% | +2.3% | 16.3% |
| 7 | **RBLX** | Roblox | 32.9% | 64.2% | +2.6% | 14.0% |
| 8 | **CELH** | Celsius | 32.2% | 69.1% | +3.0% | 11.2% |
| 9 | **LYV** | Live Nation | 31.3% | 63.0% | +2.3% | 12.6% |
| 10 | **KDP** | Keurig Dr Pepper | 30.5% | 69.1% | +2.7% | 9.2% |

### Interpretation

**Pet economy dominates.** TRUP/CHWY/IDXX win because `pet_connection` has the highest prior drift (+7%) and Gen Z/Alpha pet humanization is the most structurally one-directional trend in the data (Rover 2026, NAPHIA +23% insurance GWP).

**Beverage substitution is #2 cluster.** MNST, CELH, KDP benefit from `na_functional_bev` + negative `alcohol_headwind` exposure.

**Gen Alpha gaming:** RBLX ranks top-10 despite historical stock underperformance — cohort ramp weights Alpha spend heavily post-2032.

**Surprise:** LYV is only #9 — `irl_experiences` factor has high volatility and affordability headwinds in the model dampen consistent top-quartile finishes.

---

## 4. Most Likely to Be CRUSHED (2026–2041)

Ranked by **P(bottom quartile)**:

| Rank | Ticker | Company | P(bottom Q) | P(net +) | Median α | P(crush <−10%) |
|---:|---|---|---:|---:|---:|---:|
| 1 | **MTCH** | Match Group | **52.5%** | 30.3% | **−3.0%** | 12.1% |
| 2 | **BUD** | Anheuser-Busch | 47.6% | 32.5% | −2.4% | 7.1% |
| 3 | **STZ** | Constellation | 46.4% | 34.2% | −2.2% | 6.2% |
| 4 | **BMBL** | Bumble | 46.1% | 34.6% | −2.3% | 8.2% |
| 5 | **TAP** | Molson Coors | 44.6% | 35.4% | −2.0% | 6.1% |
| 6 | **SAM** | Boston Beer | 31.6% | 47.5% | −0.3% | 2.8% |
| 7 | **GOOGL** | Alphabet | 25.5% | 48.9% | +1.2% | 4.8% |

### Interpretation

**Dating apps are the clearest crush.** MTCH loads +0.95 on `swipe_fatigue` (prior drift −5%/yr). Even with Tinder IRL events pivot, the model assigns low execution quality (0.55) — subscriber declines are already in the data.

**Alcohol pure-plays:** BUD, STZ, TAP load +0.90–0.95 on `alcohol_headwind`. SAM survives better (transitional NA portfolio).

**Only ~30% P(net positive) for MTCH** — the simulation says swipe-fatigue is the single most reliable structural headwind.

---

## 5. Sector Heat Map

| Sector cluster | Lifted | Crushed | Verdict |
|---|---|---|---|
| **Pet economy** | TRUP, CHWY, IDXX, ELAN | — | **Strongest tailwind** |
| **NA / functional drinks** | MNST, CELH, KDP, PEP | — | **Solid tailwind** |
| **Alcohol** | — | BUD, STZ, TAP | **Structural headwind** |
| **Dating apps** | — | MTCH, BMBL | **Structural headwind** |
| **Sober venues** | PLAY, MODG (mid) | — | Positive median, high variance |
| **IRL experiences** | LYV, BKNG (mid) | — | Positive but not dominant |
| **Analog (vinyl/games)** | HAS, WMG (mid) | — | Moderate; WMG underperforms vs TRUP |
| **Wellness / gym** | PLNT, ONON, LULU | — | PLNT top-5; LULU surprisingly mid |
| **Value / thrift** | TJX, ROST (low-mid) | — | Mild tailwind, not a winner |
| **Home social** | WING, DPZ, NFLX | — | Neutral — low thematic magnitude |
| **AI infra** | NVDA | NVDA (volatility) | High mean, fat tails |
| **Cybersecurity** | CRWD, PANW | — | Mild positive; weak Gen Z causal link |

---

## 6. Fan Chart Insights (10th–90th Percentile)

| Ticker | P10 | Median | P90 | Shape |
|---|---:|---:|---:|---|
| TRUP | −6.4% | +6.2% | +16.5% | Tight upside skew |
| MTCH | −10.6% | −3.0% | +5.0% | Downside skew |
| TAP | −8.5% | −2.0% | +4.8% | Consistent mild crush |
| NVDA | −8.6% | +2.3% | +12.2% | Wide — AI cycle risk |
| RBLX | −6.9% | +2.6% | +11.4% | Alpha optionality |

---

## 7. Scenario Stress: What If Trends Reverse?

The model embeds **regime flips** (8%/year per factor). Stocks with **single-factor concentration** have wider fan charts:

- **MTCH** — crushed unless swipe-fatigue reverses; only 20% P(lift) even in moderate scenarios
- **TRUP** — still 75% P(net positive) because pet humanization flips less often in literature
- **BUD/TAP** — benefit if `alcohol_headwind` flips (Gen Z ages into drinking per NIQ counter-thesis)

To run explicit bull/bear scenarios, modify factor drifts in `scripts/07_monte_carlo_cohort_simulation.py` (e.g., `drift * 0.5` for bear).

---

## 8. Portfolio Construction from Simulation (Illustrative)

### Long thematic basket (highest P(top quartile))
TRUP, CHWY, IDXX, MNST, PLNT, RBLX

### Short / avoid thematic basket (highest P(bottom quartile))
MTCH, BUD, STZ, BMBL, TAP

### Hedge
NVDA (AI infra wins even if Gen Z resents AI — but volatile)

---

## 9. Reproducibility

```bash
cd project4_connection_economy_thesis
pip install numpy pandas plotly
python scripts/07_monte_carlo_cohort_simulation.py
```

| Output | Description |
|---|---|
| `data/monte_carlo_stock_results.csv` | Full probability table per ticker |
| `results/monte_carlo_summary.json` | Machine-readable summary |
| `results/monte_carlo_factor_paths.csv` | Median factor trajectories |
| `results/maps/monte_carlo_dashboard.html` | Interactive scatter + bar charts |

**Seed:** 42 (deterministic — re-running produces identical results)

---

## 10. Limitations (Read Before Trading)

1. **Factor loadings are thematic, not regression-estimated**
2. **No valuation** — TRUP may already price pet tailwind; MTCH may be cheap enough
3. **No correlation to SPY** — thematic alpha is orthogonal to market in this model
4. **Cohort spending $12T by 2030** (NIQ) scales impact but isn't modeled as GDP share
5. **Gen Alpha ≠ Gen Z** — single combined cohort weight is a simplification

---

## 11. Bottom Line

If documented behavioral trends persist with uncertainty, the Monte Carlo ranks:

1. **Pet economy (TRUP, CHWY, IDXX)** — highest probability of sustained lift  
2. **NA beverages (MNST, CELH)** — strong substitution tailwind  
3. **Gen Alpha platforms (RBLX)** — high optionality, moderate median  
4. **Dating apps (MTCH, BMBL)** — highest probability of thematic crush  
5. **Beer/spirits (BUD, STZ, TAP)** — reliable headwind unless cohort reverts to drinking  

The original "obvious" picks **LYV and ELF** land **middle of the pack** — still positive median thematic alpha, but not top-quartile winners in most paths. **Novel thesis picks TRUP and WMG** split: TRUP #1, WMG #22.

*Research only. Not investment advice.*
