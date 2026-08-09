# Charleston County, SC — Tract-Level Health & Equity Deep-Dive

A county-focused companion to the national `project3_cdc_mortality` analysis. This folder maps **98 census tracts** in Charleston County (FIPS **45019**) using official CDC, Census, and County Health Rankings data, documents **eight major county-wide issues** with quantitative evidence, and proposes **evidence-based interventions** for each.

## Quick start — interactive maps

Open **`results/maps/index.html`** in a browser for 15 tract-level choropleth maps:

| Map | Source | What it shows |
|---|---|---|
| Social Vulnerability Index | CDC/ATSDR SVI 2022 | Overall vulnerability percentile (0 = least, 1 = most) |
| Diabetes, Obesity, Stroke, HBP | CDC PLACES 2025 | Model-based adult prevalence by tract |
| Uninsured adults | CDC PLACES 2025 | Lack of health insurance (ages 18–64) |
| Food & housing insecurity | CDC PLACES 2025 | Social needs in past 12 months |
| Mental distress & depression | CDC PLACES 2025 | Frequent mental distress / depression |
| Smoking, physical inactivity | CDC PLACES 2025 | Behavioral risk factors |
| Utility shut-off threat, transportation barriers | CDC PLACES 2025 | Health-related social needs |

---

## Data sources (all public, no authentication)

| Dataset | Provider | Geography | URL / API |
|---|---|---|---|
| **PLACES 2025** (40 measures) | CDC | Census tract | `data.cdc.gov` → `cwsq-ngmh` |
| **Social Vulnerability Index 2022** | CDC/ATSDR | Census tract | ArcGIS FeatureServer (layer 2) |
| **Tract boundaries** | U.S. Census TIGER/Line 2022 | Census tract | `tigerweb.geo.census.gov` |
| **County mortality & SES benchmarks** | County Health Rankings 2025 + CDC NVSS + PLACES | County | Parent project `../data/` |
| **Opioid overdose dashboard** | Charleston County Government | County / ZIP | [charlestoncounty.gov/transparency](https://charlestoncounty.gov/transparency.php) |
| **Drug-related deaths report** | Charleston County Coroner | County | [2025 Annual Drug Report (PDF)](https://www.charlestoncounty.gov/departments/coroner/files/annual-report-archive/2025-Annual-Drug-Report.pdf) |
| **Multi-Hazard Vulnerability Assessment** | Charleston County + Woodwell Climate | County / parcel | [County PDF](https://charlestoncounty.gov/ccrs/files/Multi-Hazard-Vulnerability-Assessment-Final-Report-Charleston-County.pdf) |
| **Housing Needs Assessment** | Charleston County Development | County | [Housing Plan PDF](https://www.charlestoncountydevelopment.org/wp-content/uploads/2025/12/HoF-Housing-Plan.pdf) |
| **SC County Health Profile** | SC DPH | County | [dataviz.dph.sc.gov/chp](https://dataviz.dph.sc.gov/chp/) |

---

## Eight data-backed issues in Charleston County

### 1. Opioid & drug overdose crisis — among the worst in South Carolina

**The data:**
- **37.6 drug overdose deaths per 100,000** (County Health Rankings / NVSS 2025) — **31% above the U.S. county median (28.6)** and at the **SC state median (37.4)**.
- Charleston County Coroner: **153 drug-related deaths in 2025** (19% decrease from 2024, but still substantial); **79% had known substance-use history**; **14% were experiencing homelessness** at death.
- County transparency portal publishes a live [Opioid Overdose Dashboard](https://charlestoncounty.gov/transparency.php).

**Why it matters:** Overdose mortality in Charleston tracks the statewide crisis driven by fentanyl penetration. County averages mask hot spots in North Charleston and older suburban tracts with higher SVI.

**Solutions:**
| Intervention | Evidence base |
|---|---|
| Expand **naloxone (Narcan) distribution** via pharmacies, libraries, and EMS leave-behind programs | CDC overdose prevention guidance; Charleston County already tracks overdoses — scale community distribution to match 153 annual deaths |
| **Medication-assisted treatment (MAT)** hub-and-spoke model with low-barrier access in North Charleston | SAMHSA evidence; only 50% of decedents with SUD history had prior treatment interactions (Coroner 2025 report) |
| **Fentanyl test strip** and safer-use supply programs | CDC-endorsed harm reduction; reduces unknowing fentanyl exposure |
| Integrate **911 dispatch + behavioral health co-response** for overdose calls | Reduces repeat ED visits; Charleston ECC already publishes service-level metrics |
| Target **housing-first + SUD treatment** for homeless decedents (14% of 2025 deaths) | HUD Housing First model; addresses dual crisis visible in coroner data |

---

### 2. Extreme within-county health disparities — averages hide a 9× gap

**The data (this analysis, 98 tracts):**

| Measure | Lowest tract | Highest tract | Range |
|---|---|---|---|
| Diagnosed diabetes | 2.8% | 25.3% | **22.5 pp** |
| Uninsured (ages 18–64) | 3.2% | 27.7% | **24.5 pp** |
| Food insecurity | 2.9% | 50.6% | **47.7 pp** |
| Obesity | 21.7% | 48.2% | **26.5 pp** |
| SVI overall percentile | 0.01 | 0.99 | **full spectrum** |

- **16 tracts (16%)** rank in the top quartile of social vulnerability statewide (SVI ≥ 0.75).
- Health burdens correlate strongly with SVI: food insecurity ↔ SVI **r = 0.85**, uninsured ↔ SVI **r = 0.85**, housing insecurity ↔ SVI **r = 0.86** (all p < 10⁻²⁵).

**Why it matters:** Charleston's county-level life expectancy (**77.9 years**) and income (**$88,111** median) look healthy compared to SC (72.9 years, lower income), but tract-level maps reveal a **dual county** — affluent coastal/island tracts alongside deeply disadvantaged inland tracts in North Charleston and rural western areas.

**Solutions:**
| Intervention | Evidence base |
|---|---|
| **Place-based funding** targeting the 16 highest-SVI tracts (e.g., HRSA Health Center expansion, CDC PLACES-informed CHNA priorities) | CDC PLACES designed for this; SVI used by FEMA and EPA Justice40 |
| **Mobile health clinics** and school-based health centers in top-quartile diabetes/uninsured tracts | Reduces transportation barriers (also elevated in high-SVI tracts, r = 0.83) |
| Require **health impact assessments** for new development in high-burden tracts | WHO HIA guidance; aligns with County Comprehensive Plan equity goals |
| Publish an annual **tract-level health equity report card** using this pipeline | Accountability mechanism; mirrors SC DPH County Health Profile but at tract scale |

---

### 3. Food insecurity concentrated in vulnerable tracts

**The data:**
- Tract-level food insecurity ranges from **2.9% to 50.6%** (PLACES 2025, this analysis).
- County tract median: **11.4%**; mean **14.9%**.
- Strongest correlate of SVI among all health measures (r = 0.85).

**Why it matters:** Charleston's tourism-driven economy and high housing costs squeeze food budgets. Food insecurity drives diabetes (tract diabetes range 2.8–25.3%) and mental health burden.

**Solutions:**
| Intervention | Evidence base |
|---|---|
| Expand **SNAP enrollment assistance** and Double Up Food Bucks at farmers markets | USDA evidence; PLACES shows food-stamp receipt varies widely by tract |
| **Community food hubs** in North Charleston food deserts (USDA Food Access Research Atlas) | Increases fresh food access; County Food Environment Index = 8.4 (good) but unevenly distributed |
| Integrate **food security screening** into MUSC Health and FQHC primary care | CMS screening reimbursement; links to diabetes management |
| Support **Lowcountry Food Bank** satellite pantries in tracts with >25% food insecurity | Targeted by tract map (`map_food_insecurity_pct.html`) |

---

### 4. Housing affordability & quality — cost burden meets flood risk

**The data:**
- **16.9%** of county households have severe housing problems (County Health Rankings) — **above SC (14%) and U.S. (13%) medians**.
- Charleston County Housing Needs Assessment: **44% of renters are cost-burdened** (>30% of income on housing).
- Multi-Hazard Vulnerability Assessment: **>40% of dedicated affordable housing** is highly flood-vulnerable (1% annual flood chance); includes **23 Charleston County Housing Authority properties**.
- Only **~12,000 of 57,000 acres** of vacant land lies within the Urban Growth Boundary suitable for development.

**Why it matters:** Housing cost burden forces trade-offs with healthcare, food, and evacuation capacity. Flood-vulnerable affordable units face simultaneous climate and affordability crises.

**Solutions:**
| Intervention | Evidence base |
|---|---|
| **Flood-proof retrofit program** for the 23+ public housing properties in FEMA 1% flood zones | FEMA BRIC grants; County MHVA already identifies properties |
| **Inclusionary zoning** and density bonuses near planned Low Country Rapid Transit stations | County Housing Plan recommendation; reduces sprawl into flood-prone areas |
| Expand **Emergency Rental Assistance** infrastructure (County ERAP dashboard exists) | Prevents displacement cycles that worsen health |
| **Community land trusts** for permanently affordable units on higher ground within the Urban Growth Boundary | Grounded Solutions Network model; 80% of vacant land is outside UGB |

---

### 5. Climate & flood vulnerability — accelerating exposure

**The data (external assessments):**
- Sea level at Charleston has risen **~13 inches** over the past century; projected **+1.2 feet by 2050** and **+4 feet by 2100** (Woodwell Climate / NOAA).
- Woodwell Climate: probability of the **100-year rainfall event will ~triple by mid-century**.
- Climate Central: **>8,000 people and 4,700 homes** at risk of annual flooding by 2050 in Charleston County.
- Charleston recorded **89 flood events in 2019** (~1 every 4 days); thousands of structures remain storm-surge vulnerable.
- Coastal SC ZIP codes among **highest insurance non-renewal rates** nationally (Brookings analysis cited in Floodlight 2024).

**Why it matters:** Flooding intersects with health through mold-related asthma, displacement stress, utility shutoffs (tract range visible in maps), and restricted healthcare access during events.

**Solutions:**
| Intervention | Evidence base |
|---|---|
| Implement **Charleston Rainproof** rain gardens and green infrastructure at scale in high-SVI tracts | City program exists; EPA green infrastructure reduces runoff 40–90% |
| **Managed retreat / buyout** for repeatedly flooded low-income properties | FEMA HMGP; avoids trapping residents in unsellable homes (documented post-Hugo pattern) |
| **Unified sea level rise building standards** county-wide, not just City of Charleston | Woodwell recommends; current patchwork allows risky exurban growth (Long Savannah, 9,000+ homes) |
| Integrate **CDC SVI + FEMA flood layers** into emergency planning (this project's maps are a starting point) | CDC SVI explicitly designed for disaster response prioritization |
| **Community resilience hubs** (cooling, charging, medical) in top-SVI tracts | FEMA Community Lifelines model |

---

### 6. Behavioral health access gaps — mental distress without enough providers

**The data:**
- Tract-level **frequent mental distress: 7.4%–22.8%** (PLACES); county suicide rate **15.4/100k** (near SC median).
- County Health Rankings: **1 mental health provider per 214 residents** (pop-per-provider ratio 0.0047) — access metric varies widely vs. urban specialty concentration.
- Coroner 2025: **10 suicides** among 153 drug-related deaths (intentional overdoses).
- PLACES: **lack of social/emotional support** and **loneliness** vary substantially by tract.

**Solutions:**
| Intervention | Evidence base |
|---|---|
| Expand **988 crisis line** local capacity and mobile crisis teams | SAMHSA 988 model; reduces ED boarding |
| **School-based mental health** in Charleston County School District high-burden tracts | APA evidence; catches adolescent distress early |
| **Telehealth parity** for rural western Charleston tracts (Johns Island, Awendaw, McClellanville) | HRSA rural telehealth; addresses provider maldistribution |
| **Peer recovery support** integrated with MAT for co-occurring SUD + mental health | SAMHSA evidence; Coroner data shows 79% SUD history among decedents |

---

### 7. Chronic disease burden — diabetes & obesity hotspots

**The data:**
- County diabetes prevalence **10.0%** (below SC 13.1%, near U.S. 10.9%) — but tract range **2.8%–25.3%**.
- Obesity tract range **21.7%–48.2%**; physical inactivity correlates with SVI (r = 0.85).
- Heart disease mortality **254.6/100k** (better than SC 332.3 and U.S. 347.0) — but stroke **74.0** is slightly below SC 86.6.
- Parent project found PM₂.₅ (7.1 µg/m³, below U.S. median) is not Charleston's primary driver; **poverty and food environment** matter more at county scale.

**Solutions:**
| Intervention | Evidence base |
|---|---|
| **CDC National Diabetes Prevention Program** sites in top-quartile tracts | 58% risk reduction in RCTs; target tracts with >18% diabetes on map |
| **Complete Streets** and safe walking/biking infrastructure in high-inactivity tracts | Surgeon General's Step It Up! initiative |
| **Healthy food procurement** policies for county government and school cafeterias | CDC sodium/healthy food service guidelines |
| **Tobacco 21 enforcement** and smoke-free multi-unit housing | reduces lung cancer (county rate 28.7 vs U.S. 39.2 — maintain advantage) |

---

### 8. Healthcare access — uninsured pockets despite county average

**The data:**
- County uninsured rate **9.7%** (near U.S. 9%, below SC 11%).
- Tract uninsured range: **3.2%–27.7%** — nearly **9× difference** within one county.
- Uninsured ↔ SVI correlation r = 0.85; transportation barriers ↔ SVI r = 0.83.
- SC has **not expanded Medicaid** — leaving a coverage gap that tract maps make visible.

**Solutions:**
| Intervention | Evidence base |
|---|---|
| Advocate for **Medicaid expansion** — would cover ~100,000+ uninsured South Carolinians | Kaiser Family Foundation estimates; Charleston tract maps identify where need concentrates |
| Expand **FQHC / community health center** capacity in North Charleston high-uninsured tracts | HRSA underserved area designations; sliding-scale care |
| **Enrollment navigators** during ACA open enrollment targeting tracts >15% uninsured | CMS navigator program; ROI in reduced uncompensated care |
| **Low Country Rapid Transit** (planned) with healthcare facility stops | Addresses transportation barrier (PLACES measure correlates r = 0.83 with SVI) |

---

## Key findings from tract-level analysis

1. **Charleston is two counties in one.** Affluent averages (high life expectancy, low child poverty vs. SC) coexist with tracts at the 99th percentile of social vulnerability and 50%+ food insecurity.

2. **Social vulnerability predicts health almost perfectly here.** Eight of sixteen health/social-need measures correlate with SVI at **r > 0.80** — stronger than in many national county-level analyses (parent project R² for most outcomes ≤ 0.51).

3. **Drug overdose is the one county-level metric that is unambiguously bad** (37.6/100k), even while chronic disease mortality looks better than peer counties.

4. **Climate and housing crises compound health disparities** — external assessments confirm that the same high-SVI tracts facing food/insurance gaps also hold the most flood-vulnerable affordable housing.

5. **Depression does not correlate with SVI in Charleston** (r = 0.01, p = 0.90) — suggesting mental health burden cuts across income levels, consistent with national patterns where high-poverty and affluent-isolated tracts both show elevated distress through different mechanisms.

---

## Pipeline & file structure

```
charleston_county/
├── README.md                          ← overview & issue briefs
├── RESEARCH_PAPER.md                  ← full academic paper with critical analysis
├── scripts/
│   ├── 01_download_data.py            ← PLACES, SVI, TIGER boundaries, benchmarks
│   ├── 02_analyze_tracts.py           ← merge, correlations, issue metrics
│   └── 03_make_maps.py                ← 15 interactive Plotly choropleths
├── data/
│   ├── places_tracts_long.csv         ← 3,920 rows (98 tracts × 40 measures)
│   ├── svi_tracts.csv
│   ├── tract_boundaries.geojson
│   ├── merged_tract_data.csv
│   └── county_benchmarks.csv
└── results/
    ├── issue_metrics.json             ← headline numbers
    ├── tract_summary_stats.csv
    ├── tract_correlations.csv
    ├── top_burden_tracts.csv
    └── maps/
        ├── index.html                 ← start here
        └── map_*.html                 ← 15 interactive maps
```

## How to reproduce

```bash
pip install requests pandas numpy scipy plotly
cd project3_cdc_mortality/charleston_county
python scripts/01_download_data.py
python scripts/02_analyze_tracts.py
python scripts/03_make_maps.py
# Open results/maps/index.html
```

**Note:** Step 1 requires network access to CDC and Census APIs. The parent project's county-level data (`../data/merged_county_data.csv`) must exist for county benchmarks — run the parent pipeline first if missing.

---

## Caveats

- **PLACES estimates are model-based** (BRFSS + ACS small-area estimation), not direct survey counts. Confidence intervals are available in the raw data.
- **Ecological fallacy:** tract-level associations do not prove individual-level causation.
- **SVI rankings** in the state-specific database rank tracts against other **South Carolina** tracts, not nationally (values 0–1 percentile within SC).
- **External flood/housing statistics** come from county reports and peer-reviewed assessments, not from this pipeline's automated downloads.
- **Year ranges differ** across sources (PLACES 2023, SVI 2018–2022 ACS, CHR 2018–2023 depending on measure).

---

## Suggested next steps

- Overlay **FEMA flood zones** and **Charleston County Housing Authority properties** on these tract maps (data available from County GIS Hub).
- Add **temporal trend** analysis using PLACES annual releases and Coroner drug reports (2024 vs. 2025 already show 19% decline).
- Link tract FIPS to **Charleston County Council districts** for policy accountability.
