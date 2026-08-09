# Project 3 — County-Level Mortality vs. Socioeconomic, Pollution & Healthcare-Access Factors

## Goal
For six causes of death / health outcomes, pull real county-level US data and
cross-reference against socioeconomic status, air pollution, and healthcare
access, with interactive maps and statistical correlation/regression
analysis.

## Causes of death / outcomes analyzed
| Outcome | Source | Geography | Notes |
|---|---|---|---|
| **Drug overdose deaths** (age-adj. rate /100k) | County Health Rankings (NVSS) | 2,010 counties | requested cause #1 |
| **Heart disease mortality** (age-adj. rate /100k) | CDC NVSS / Interactive Atlas of Heart Disease & Stroke (`jiwm-ppbh`) | 3,226 counties | requested cause #2 |
| **Diabetes prevalence** (% adults) | CDC PLACES (`i46a-9kgh`, BRFSS-based small-area model) | 3,143 counties | requested cause #3 — see note below |
| **Lung cancer mortality** (age-adj. rate /100k, 2019-2023) | NCI State Cancer Profiles | 3,143 counties | requested cause #4 |
| **Stroke mortality** (age-adj. rate /100k) | CDC NVSS / Interactive Atlas (`vutr-sfkh`) | 3,226 counties | additional cause #1 |
| **Suicide deaths** (age-adj. rate /100k) | County Health Rankings (NVSS) | ~1,960 counties | additional cause #2 |

**Note on diabetes:** county-level *mortality* with diabetes as underlying
cause is suppressed for most US counties (small numbers, NCHS confidentiality
rules) and is not available through any public API. We instead use the CDC
PLACES *diagnosed-diabetes prevalence* (model-based estimate from BRFSS),
which is the standard county-level diabetes indicator and is strongly
correlated with diabetes mortality at the population level. This is clearly
a morbidity, not mortality, measure — flagged throughout.

## Cross-referenced predictors (all from County Health Rankings 2025, itself
sourced from ACS, BRFSS, EPA, and NPPES/AHRF):

| Domain | Variables |
|---|---|
| Socioeconomic | Median household income, income inequality ratio, unemployment %, child poverty %, high-school completion %, broadband access % |
| Healthcare access | Uninsured adults %, population-per-primary-care-physician ratio, population-per-mental-health-provider ratio |
| Pollution / environment | PM2.5 air pollution (µg/m³), drinking water violations, severe housing problems %, long commute (driving alone) % |
| General | Food Environment Index |

## Data sources (all official, public, no auth)
- **County Health Rankings & Roadmaps** — `countyhealthrankings.org` (RWJF / UW Population Health Institute), 2025 national analytic CSV (13 MB).
- **CDC NVSS via data.cdc.gov Socrata API** — Heart Disease Mortality (`jiwm-ppbh`) and Stroke Mortality (`vutr-sfkh`) by county.
- **CDC PLACES via data.cdc.gov** — county GIS-friendly diabetes prevalence (`i46a-9kgh`).
- **NCI State Cancer Profiles** — `statecancerprofiles.cancer.gov` lung & bronchus age-adjusted death rates by county.
- **Plotly US county GeoJSON** (`plotly/datasets`) — county boundary polygons for choropleth maps.

(Direct access to `wonder.cdc.gov` and most of `data.cdc.gov`'s older
resources is blocked by CDC's edge/CDN (Akamai "Access Denied") from this
environment — the datasets above are the subset of CDC/NCI open data that
remain programmatically accessible.)

## Pipeline
1. `scripts/01_download_chr_data.py` — downloads & subsets County Health Rankings CSV
2. `scripts/02_download_cdc_mortality.py` — heart disease, stroke, diabetes via Socrata
3. `scripts/03_download_lung_cancer.py` — lung cancer mortality via NCI State Cancer Profiles
4. `scripts/04_merge_and_correlate.py` — merges on 5-digit FIPS, computes Pearson/Spearman correlations and standardized multivariable OLS regressions
5. `scripts/05_make_maps.py` — interactive Plotly choropleth maps for all 6 outcomes + 3 key predictors

## Results

### Interactive maps
Open `results/maps/index.html` in a browser (links to one HTML map per
variable: all 6 outcomes, plus median household income, PM2.5, and uninsured
rate for visual cross-reference).

### Top univariate correlates per outcome (Pearson r, all p << 0.001 unless noted)

| Outcome | #1 correlate | #2 | #3 |
|---|---|---|---|
| Drug overdose deaths | child poverty % (r=+0.31) | median income (r=−0.27) | income inequality (r=+0.25) |
| Suicide deaths | median income (r=−0.33) | food environment index (r=−0.30) | broadband access (r=−0.28) |
| Heart disease mortality | median income (r=−0.59) | child poverty % (r=+0.57) | food environment index (r=−0.53) |
| Stroke mortality | child poverty % (r=+0.43) | food environment index (r=−0.39) | median income (r=−0.37) |
| Diabetes prevalence | child poverty % (r=+0.82) | HS completion % (r=−0.73) | food environment index (r=−0.67) |
| Lung cancer mortality | median income (r=−0.57) | child poverty % (r=+0.49) | broadband access (r=−0.47) |

Full tables: `results/correlation_pearson.csv`, `results/correlation_spearman.csv`.

### Multivariable (standardized OLS, all 13 predictors together)

| Outcome | Model R² | Strongest independent predictor |
|---|---|---|
| Drug overdose deaths | 0.27 | Long commute % (β=+0.31) — income & insurance also significant |
| Suicide deaths | 0.24 | HS completion % (β=+0.34, **positive** — see discussion) |
| Heart disease mortality | **0.47** | Severe housing problems % (β=−0.28), child poverty (β=+0.27) |
| Stroke mortality | 0.27 | Child poverty % (β=+0.35); **PM2.5 air pollution independently significant** (β=+0.20, p=3e-21) |
| Diabetes prevalence | **0.77** | Child poverty % (β=+0.50), HS completion % (β=−0.31) |
| Lung cancer mortality | 0.51 | Median income (β=−0.44), severe housing problems % (β=−0.31), long commute % (β=+0.24) |

Full table: `results/regression_coefficients.csv`.

## In-depth findings

1. **Socioeconomic deprivation is the dominant cross-cutting signal.**
   Child poverty rate and median household income are the strongest (or
   among the strongest) correlates for *every one* of the six outcomes.
   Diabetes prevalence shows an exceptionally strong relationship with
   child poverty (r = 0.82) and education (HS completion r = −0.73) —
   together with other predictors these explain 77% of county-level
   variance in diabetes prevalence, by far the best-fit model of the six.

2. **Air pollution (PM2.5) has an independent association with stroke
   mortality.** Even after adjusting for poverty, income, education,
   insurance, and healthcare access, PM2.5 remains a significant
   independent predictor of stroke mortality (standardized β = +0.20,
   p ≈ 3×10⁻²¹) — consistent with a substantial epidemiological literature
   linking fine particulate exposure to cerebrovascular events. PM2.5 was
   not a top independent predictor for the other outcomes once
   socioeconomic factors were accounted for, but it remains correlated with
   most of them in the univariate analysis (likely reflecting that polluted
   counties also tend to be poorer/more urban-industrial).

3. **Heart disease and lung cancer mortality are best explained by this
   predictor set** (R² = 0.47 and 0.51). For lung cancer, "severe housing
   problems" and "long commute (driving alone)" are independently
   significant alongside income — plausible proxies for occupational/
   environmental exposure and for smoking prevalence, which correlates with
   both housing quality and rurality but is not directly measured here.

4. **Drug overdose and suicide are the *least* well explained by these
   variables** (R² = 0.27 and 0.24). This matches the public-health
   consensus that overdose and suicide mortality are driven heavily by
   factors not captured in this dataset — opioid supply/fentanyl
   penetration, social isolation, firearm access, and historical/regional
   economic shocks (e.g., Appalachia, parts of the Rust Belt) — rather than
   "baseline" socioeconomic deprivation alone.

5. **Counterintuitive sign: HS completion % is *positively* associated with
   suicide in the multivariable model** (β = +0.34) despite a *negative*
   univariate correlation with most other outcomes. This is a known pattern
   in US suicide epidemiology — higher-education, higher-income, more rural
   and more White counties (parts of the Mountain West / Northern Plains)
   have *higher* suicide rates than poorer, more urban, more diverse
   counties, even though those same poorer counties have worse outcomes for
   nearly everything else. This is a textbook example of why a variable's
   univariate correlation and its multivariable coefficient can have
   opposite signs (collinearity with urbanicity/race/region).

6. **Healthcare access (population-per-PCP, uninsured %) shows weaker and
   sometimes counterintuitive associations** — e.g., a higher
   population-per-primary-care-physician ratio correlates with *lower*
   heart disease and lung cancer mortality in this data. This is most
   plausibly explained by urban/rural confounding: large metro counties
   often have *more* total physicians but a *higher* population-per-PCP
   ratio (concentration in specialties/hospitals) while also having lower
   smoking rates and better age-adjusted outcomes than rural counties — so
   the access metric is acting partly as an urbanicity proxy here, not a
   clean causal signal.

## Important caveats
- **Ecological correlation**: all variables are county-level aggregates.
  Associations at the county level do not necessarily hold for individuals
  (ecological fallacy).
- **Confounding by urbanicity/region/race** is pervasive and not fully
  adjusted for — see point 5 and 6 above.
- **Diabetes uses prevalence, not mortality** (see note above).
- Different outcome datasets cover slightly different year ranges
  (2018-2023 depending on source) and slightly different county sets due to
  small-number suppression; sample sizes (n) are reported in every results
  table.
- Multiple comparisons: with 6 outcomes × 13 predictors = 78 univariate
  tests, some "significant" p-values are expected by chance, but the
  reported top correlates have p-values many orders of magnitude below any
  reasonable multiple-comparison threshold.

## How to reproduce
```bash
pip install requests pandas numpy scipy statsmodels plotly
python scripts/01_download_chr_data.py
python scripts/02_download_cdc_mortality.py
python scripts/03_download_lung_cancer.py
python scripts/04_merge_and_correlate.py
python scripts/05_make_maps.py
```

## Charleston County deep-dive (companion analysis)

A second folder, **`charleston_county/`**, provides a tract-level analysis of
Charleston County, SC (FIPS 45019) with 15 interactive census-tract maps,
eight data-backed issue briefs (opioids, disparities, food insecurity,
housing, flooding, behavioral health, chronic disease, uninsured pockets),
and evidence-based intervention tables. See
[`charleston_county/README.md`](charleston_county/README.md) and open
[`charleston_county/results/maps/index.html`](charleston_county/results/maps/index.html).
