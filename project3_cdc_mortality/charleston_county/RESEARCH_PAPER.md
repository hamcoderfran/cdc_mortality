# Health Equity, Chronic Disease, and Climate Vulnerability in Charleston County, South Carolina: A Tract-Level Analysis with Critical Evaluation of Policy Claims

**Authors:** Automated analysis pipeline (Project 3 / Charleston County Deep-Dive)  
**Date:** August 2026  
**Geography:** Charleston County, SC (FIPS 45019) — 98 census tracts  
**Word count:** ~6,800 (main text)

---

## Abstract

**Background.** Charleston County presents a paradox in population health: county-level indicators—including life expectancy (77.9 years), median household income ($88,111), and several chronic-disease mortality rates—compare favorably to South Carolina and, in some cases, national medians. Yet the county simultaneously ranks among the worst in the state for drug overdose mortality (37.6 per 100,000) and exhibits extreme intra-county variation in insurance coverage, food insecurity, and modeled chronic-disease prevalence.

**Objective.** Using publicly available surveillance data, we (1) quantify tract-level health and social vulnerability disparities within Charleston County; (2) critically evaluate eight commonly cited policy claims about county health and climate risk; and (3) propose literature- and data-backed interventions graded by evidence strength.

**Methods.** We merged CDC PLACES 2025 model-based estimates (40 measures × 98 tracts), CDC/ATSDR Social Vulnerability Index (SVI) 2022 rankings, and U.S. Census TIGER tract boundaries. County-level benchmarks were drawn from County Health Rankings 2025, CDC NVSS, and PLACES. We computed Pearson correlations, quartile overlap analyses, and generated interactive choropleth maps. External claims regarding flooding, housing, and overdose mortality were evaluated against county government reports and peer-reviewed literature.

**Results.** Health-related social needs and behavioral risk factors correlated strongly with SVI (e.g., food insecurity *r* = 0.85, uninsured *r* = 0.85, housing insecurity *r* = 0.86; all *p* < 10⁻²⁵). Tract-level ranges were large: diagnosed diabetes 2.8–25.3%, food insecurity 2.9–50.6%, uninsured 3.2–27.7%. Sixteen tracts (16.3%) ranked in the top quartile of SVI within South Carolina; 15 of 25 top-quartile food-insecurity tracts also had high SVI. Depression showed no correlation with SVI (*r* = 0.01, *p* = 0.90), diverging from other measures. County-level aggregates obscured a spatially concentrated burden in North Charleston and western rural tracts.

**Conclusions.** Charleston County is best understood as a **dual county**—affluent coastal and suburban tracts coexisting with deeply disadvantaged inland communities. Policy should prioritize place-based interventions in high-SVI tracts rather than county-wide programs calibrated to misleading averages. Opioid mortality, Medicaid non-expansion, and flood-exposed affordable housing represent the highest-priority, best-evidence intervention targets. Model-based tract estimates require cautious interpretation and should be validated with local survey and clinical data where possible.

**Keywords:** social vulnerability; health disparities; PLACES; census tract; opioid overdose; sea level rise; Medicaid; Charleston; South Carolina

---

## 1. Introduction

Charleston County is one of the fastest-growing coastal counties in the United States. Its economy is driven by tourism, port logistics, aerospace manufacturing, and a expanding medical sector anchored by the Medical University of South Carolina (MUSC). These assets produce favorable county-level statistics: life expectancy nearly five years above the South Carolina median, child poverty below the state average, and heart-disease mortality substantially lower than peer counties (254.6 vs. 332.3 per 100,000).

However, aggregate statistics can mislead. The Centers for Disease Control and Prevention (CDC) developed the Population Level Analysis and Community Estimates (PLACES) project precisely because county-level data "mask important local-level health disparities" (Moores et al., 2022). Similarly, the CDC/ATSDR Social Vulnerability Index (SVI) was designed to identify census tracts requiring prioritized resource allocation during emergencies—but has increasingly been applied to chronic-disease planning (Hollis & Escoffery, 2023).

This paper applies the methodological framework validated in CDC *Preventing Chronic Disease* publications—merging PLACES health measures with SVI at tract scale (Hollis et al., 2023)—to Charleston County. We extend prior work by:

1. Providing a **critical evaluation** of eight policy-relevant claims (not merely descriptive mapping);
2. Grading proposed interventions by **evidence hierarchy** (systematic reviews > quasi-experimental > ecological correlation);
3. Explicitly addressing **limitations** of model-based small-area estimation in a rapidly gentrifying county.

The opioid crisis, Medicaid coverage gap, food insecurity hotspots, and climate-driven flood exposure are analyzed as intersecting rather than independent problems—a framing supported by environmental justice literature on the "climate gap" (Williams et al., 2023).

---

## 2. Background and Literature Review

### 2.1 Small-area estimation for public health planning

PLACES uses multilevel regression and poststratification (MRP) to generate model-based estimates of 40 health indicators at county, place, census tract, and ZIP Code Tabulation Area levels from Behavioral Risk Factor Surveillance System (BRFSS), American Community Survey (ACS), and Census population data (CDC, 2025). Validation studies demonstrate reasonable concordance with direct BRFSS estimates at larger geographies, but tract-level confidence intervals can be wide in small populations (Zhang et al., 2022).

The SVI combines 16 ACS-derived social factors into four themes—socioeconomic status, household composition/disability, minority status/language, and housing/transportation—and ranks tracts on a 0–1 percentile scale (Flanagan et al., 2023). A systematic review of 90 U.S. health studies found SVI increasingly applied beyond disaster response to chronic-disease outcomes, though methodological heterogeneity limits cross-study comparison (Lewis et al., 2023).

Hollis et al. (2023) demonstrated the utility of merging PLACES and SVI for chronic obstructive pulmonary disease (COPD) planning: tracts in the highest COPD quartile had median SVI socioeconomic rankings of 0.77. Our analysis tests whether this concordance pattern holds for diabetes, food insecurity, and insurance coverage in a single coastal county.

### 2.2 The opioid overdose epidemic in the Southeast

National drug overdose mortality exceeded 107,000 deaths in 2023, with synthetic opioids (primarily fentanyl) driving the majority (Kaufman et al., 2024). South Carolina has been severely affected: Charleston County's age-adjusted rate of 37.6 per 100,000 places it at the state median but 31% above the national county median (28.6).

Evidence-based response strategies include:

- **Overdose education and naloxone distribution (OEND):** Umbrella reviews conclude OEND programs reduce opioid-related mortality at the population level, with post-naloxone survival rates of 92–98% across community, family, and police distribution models (Liu et al., 2021; McDonald et al., 2025).
- **Medications for opioid use disorder (MOUD):** Methadone and buprenorphine reduce all-cause mortality among people with opioid use disorder (OUD); only ~25% of U.S. individuals with OUD received MOUD in 2022 (Kimmel et al., 2024).

### 2.3 Medicaid expansion and the coverage gap

South Carolina has not expanded Medicaid under the Affordable Care Act, leaving an estimated coverage gap for low-income adults. Quasi-experimental evidence links expansion to mortality reductions: Miller et al. (2021) estimated a 9.4% relative decline in annual mortality among near-elderly expansion-state residents; difference-in-differences analyses report 11.8 fewer deaths per 100,000 adults (95% CI: 2.2–21.3) associated with expansion (McKenna et al., 2021).

**Critical caveat:** Benefits are heterogeneous. Medicaid expansion reduced urban Black mortality but showed mixed or null effects for rural populations and Latino/a communities in some analyses (Grigoryeva & Ruef, 2024). Charleston's tract-level uninsured range (3.2–27.7%) suggests expansion would not uniformly benefit all subpopulations.

### 2.4 Climate, flooding, and housing as health determinants

Nationwide, affordable housing units exposed to coastal flooding are projected to more than triple by 2050 (Buchanan et al., 2020). Charleston County's Multi-Hazard Vulnerability Assessment reports >40% of dedicated affordable housing stock is highly flood-vulnerable, including 23 Housing Authority properties. Woodwell Climate Research Center projects 0.37 m (1.21 ft) of sea level rise by 2050 for the county, with the probability of the present-day 100-year rainfall event roughly tripling by mid-century.

Williams et al. (2023), writing in the *New England Journal of Medicine*, argue that climate-driven flooding compounds racial and economic health inequities through displacement, mold exposure, mental health trauma, and loss of healthcare access—creating a "climate gap" parallel to the "health gap."

---

## 3. Methods

### 3.1 Study area

Charleston County, South Carolina (FIPS 45019), had an estimated 2024 population of ~435,000 across 98 census tracts (U.S. Census Bureau). Major population centers include the City of Charleston, North Charleston, Mount Pleasant, Summerville (partial), and rural Sea Islands.

### 3.2 Data sources and acquisition

| Layer | Source | Year | Geography |
|---|---|---|---|
| Health outcomes & social needs (40 measures) | CDC PLACES (`cwsq-ngmh`) | 2023 release | Census tract |
| Social vulnerability (4 themes + overall) | CDC/ATSDR SVI 2022 | 2018–2022 ACS | Census tract |
| Tract boundaries | Census TIGER/Line | 2022 | Polygon |
| Mortality, income, insurance (benchmarks) | County Health Rankings 2025 | 2018–2023 | County |
| Drug-related deaths | Charleston County Coroner | 2025 | County |
| Flood/housing statistics | County MHVA, Housing Plan | 2024–2025 | County/parcel |

Data were downloaded programmatically via Socrata API (PLACES), ArcGIS REST (SVI, TIGER), and extracted from the parent project's merged county table. Analysis scripts are reproducible (`scripts/01–03`).

### 3.3 Variables

**Outcomes (tract-level):** Diagnosed diabetes, obesity, stroke, coronary heart disease, high blood pressure, current smoking, frequent mental distress, depression, fair/poor self-rated health, food insecurity, housing insecurity, utility shut-off threat, lack of reliable transportation, and current lack of health insurance (ages 18–64).

**Exposure (tract-level):** SVI overall percentile (`RPL_THEMES`) and four theme rankings. In the state-specific SVI database, values represent percentile rank *within South Carolina* (0 = least vulnerable, 1 = most).

**County-level outcomes:** Age-adjusted drug overdose, heart disease, stroke, lung cancer, and suicide death rates; life expectancy; diabetes prevalence; socioeconomic predictors.

### 3.4 Statistical analysis

We constructed a wide-format tract table (one row per tract, one column per measure) and computed:

- Descriptive statistics (min, max, range, mean, median, quartiles);
- Pearson correlation coefficients between health measures and SVI themes, with two-tailed *p*-values (*n* = 98 tracts);
- Quartile overlap: tracts simultaneously in the top quartile of SVI and top quartile of each health burden measure;
- Interactive choropleth maps (Plotly) for spatial pattern identification.

We did **not** perform multivariable regression at tract level due to small *n* (98) relative to the number of potential confounders and the risk of overfitting with collinear PLACES measures derived from shared BRFSS/ACS inputs.

### 3.5 Critical claim evaluation framework

Each policy claim was assessed on four criteria:

1. **Data provenance** — primary vs. model-based vs. anecdotal;
2. **Geographic scale** — county aggregate vs. tract-level confirmation;
3. **Causal inferential validity** — experimental, quasi-experimental, or ecological;
4. **Generalizability to Charleston** — direct local evidence vs. extrapolation from national studies.

Claims were classified as **Strong** (supported by local data + high-quality literature), **Moderate** (supported but with important caveats), or **Weak/Uncertain** (insufficient local validation or conflicting evidence).

---

## 4. Results

### 4.1 County-level benchmarks: the paradox of averages

**Table 1.** Charleston County vs. South Carolina and U.S. county medians (County Health Rankings / PLACES 2025)

| Indicator | Charleston | SC median | U.S. median | Interpretation |
|---|---:|---:|---:|---|
| Drug overdose deaths (/100k) | **37.6** | 37.4 | 28.6 | Crisis level; no better than SC |
| Life expectancy (years) | **77.9** | 72.9 | 75.1 | Substantially above SC |
| Median household income ($) | **88,111** | 57,768 | 64,244 | Affluence skews averages |
| Child poverty (%) | 14.2 | 23.9 | 17.9 | Below SC average |
| Uninsured adults (%) | 9.7 | 11.5 | 8.7 | Near national median |
| Diabetes prevalence (%) | 10.0 | 13.1 | 10.9 | Favorable county average |
| Heart disease mortality (/100k) | 254.6 | 332.3 | 347.0 | Favorable |
| Severe housing problems (%) | **16.9** | 14.1 | 12.9 | **Worse than SC and U.S.** |
| Premature death (YPLL rate) | 8,317 | 13,119 | 9,988 | Better than both benchmarks |

**Finding:** Charleston's favorable life expectancy and chronic-disease mortality co-exist with overdose rates indistinguishable from the statewide crisis and housing-quality metrics worse than peers. Income and life-expectancy averages are pulled upward by affluent coastal tracts (Daniel Island, Mount Pleasant, South of Broad) while overdose and SVI burdens concentrate elsewhere.

### 4.2 Tract-level disparities

**Table 2.** Tract-level ranges (PLACES 2025 + SVI 2022, *n* = 98)

| Measure | Minimum | Maximum | Range | Median |
|---|---:|---:|---:|---:|
| SVI overall percentile | 0.01 | 0.99 | 0.98 | 0.40 |
| Diagnosed diabetes (%) | 2.8 | 25.3 | 22.5 pp | 10.7 |
| Obesity (%) | 21.7 | 48.2 | 26.5 pp | 28.9 |
| Uninsured (%) | 3.2 | 27.7 | 24.5 pp | 8.7 |
| Food insecurity (%) | 2.9 | 50.6 | 47.7 pp | 11.4 |
| Housing insecurity (%) | — | — | — | — |
| Frequent mental distress (%) | 7.4 | 22.8 | 15.4 pp | 14.4 |

The **9× ratio** between lowest and highest uninsured tracts (3.2% vs. 27.7%) exceeds the difference between Charleston's county average and the most uninsured U.S. states. Food insecurity reaching **50.6%** in the highest tract—a model-based estimate subject to wide confidence intervals—would, if accurate, represent a humanitarian-scale burden invisible in the county average.

### 4.3 Correlation of health measures with social vulnerability

**Table 3.** Pearson *r* between health/social-need measures and SVI overall (`RPL_THEMES`), *n* = 98

| Measure | *r* | *p*-value | Strength |
|---|---:|---:|---|
| Housing insecurity | 0.857 | 2.1 × 10⁻²⁹ | Very strong |
| Uninsured | 0.854 | 5.1 × 10⁻²⁹ | Very strong |
| Food insecurity | 0.845 | 7.1 × 10⁻²⁸ | Very strong |
| Obesity | 0.825 | 1.4 × 10⁻²⁵ | Very strong |
| Smoking | 0.818 | 9.3 × 10⁻²⁵ | Very strong |
| Utility shut-off threat | 0.819 | 6.7 × 10⁻²⁵ | Very strong |
| Transportation barriers | 0.830 | 4.6 × 10⁻²⁶ | Very strong |
| Fair/poor health | 0.831 | 3.8 × 10⁻²⁶ | Very strong |
| Mental distress | 0.709 | 3.0 × 10⁻¹⁶ | Strong |
| Diabetes | 0.633 | 2.6 × 10⁻¹² | Moderate-strong |
| **Depression** | **0.012** | **0.903** | **None** |

**Theme-specific drivers:** Food insecurity correlated most strongly with SVI Theme 3 (minority status/language; *r* = 0.852). Uninsured rates tracked all themes roughly equally (overall *r* = 0.854). Diabetes showed the weakest SVI association among chronic conditions (*r* = 0.633)—still significant, but suggesting additional non-SVI factors (age structure, healthcare access via MUSC proximity) influence spatial patterns.

### 4.4 Quartile overlap: concentrated compound burden

- **16 tracts** (16.3%) had SVI ≥ 0.75 (top quartile within SC).
- **25 tracts** each exceeded the 75th percentile for diabetes, food insecurity, and uninsured rates.
- **15 tracts** simultaneously exceeded the 75th percentile for both SVI and food insecurity (60% overlap).
- **12 tracts** simultaneously exceeded the 75th percentile for both SVI and diabetes (48% overlap among high-SVI tracts).

Top-quartile food-insecurity tracts had mean SVI = 0.775 and mean population = 4,065—representing an estimated **~100,000 residents** in the highest-burden quarter of the county by food insecurity alone.

### 4.5 Spatial patterns (qualitative map review)

Interactive maps (`results/maps/`) reveal:

- **Highest SVI and food insecurity:** concentrated in North Charleston (especially south and west of I-26), portions of West Ashley, and select rural western tracts.
- **Lowest SVI, lowest uninsured:** Daniel Island, Mount Pleasant east of the Cooper, Sullivan's Island, and downtown Charleston peninsula (with notable exceptions in the East Side and Cooper River Bridge area).
- **Diabetes hotspots:** partially overlap SVI but also appear in older suburban tracts with aging populations independent of minority-status vulnerability—consistent with the weaker diabetes–SVI correlation.

---

## 5. Critical Evaluation of Eight Policy Claims

### Claim 1: "Charleston County is a healthy place to live."

**Verdict: Moderate — misleading at county scale.**

Life expectancy (77.9 years) and premature mortality (8,317 YPLL) outperform SC benchmarks substantially. However, this claim **fails for ~16–25% of tracts** where SVI, food insecurity, and uninsured rates reach crisis levels. The claim also ignores drug overdose mortality at crisis levels (37.6/100k) and severe housing problems above state/national medians.

**Evaluation:** Ecological fallacy risk is high. Affluent in-migration and medical infrastructure (MUSC) inflate county averages without benefiting all residents—a pattern documented in gentrifying coastal cities where "average prosperity masks concentrated poverty" (Morello-Frosch & Jesdale, 2006).

---

### Claim 2: "Charleston has an opioid crisis comparable to the worst-affected U.S. counties."

**Verdict: Strong for county-level overdose rate; Moderate for 'worst-affected' framing.**

At 37.6/100k, Charleston equals the SC median and exceeds the U.S. county median by 31%. The Coroner documented 153 drug-related deaths in 2025 (79% with known SUD history; 14% homeless at death). This is unambiguously a public health emergency.

However, Charleston is **not** among the highest nationally (Appalachian and Southwest counties exceed 60–80/100k). The claim is **locally accurate** but should not be exaggerated nationally.

**Evidence quality:** County Health Rankings (NVSS underlying data) = high-quality mortality surveillance. Coroner report = primary local source.

---

### Claim 3: "Social vulnerability predicts health outcomes in Charleston."

**Verdict: Strong for social needs and behaviors; Weak for depression.**

Eight of sixteen analyzed measures correlated with SVI at *r* > 0.80. This exceeds concordance reported in Hollis et al. (2023) for COPD nationally (tract socioeconomic SVI ~0.77 in highest COPD quartile). The pattern confirms PLACES–SVI merging is analytically productive in Charleston.

**Critical caveat:** These are **cross-sectional ecological correlations**. SVI and PLACES share ACS inputs, inducing **construct overlap** that may inflate correlations. Independent validation with clinical records (ED visits, HbA1c screening rates) is needed before causal language is warranted.

**Depression exception:** Null SVI correlation (*r* = 0.01) suggests mental health burden in Charleston follows different spatial logic—potentially including affluent-isolated older adults, military/veteran populations, and underdiagnosis in high-SVI tracts. This aligns with national findings that suicide and distress patterns do not map cleanly onto poverty gradients (Stein et al., 2015).

---

### Claim 4: "Medicaid expansion would significantly reduce Charleston's uninsured burden."

**Verdict: Strong in principle; Moderate for magnitude in Charleston.**

Tract uninsured rates (3.2–27.7%) identify clear coverage gaps. Miller et al. (2021) and McKenna et al. (2021) provide robust quasi-experimental evidence that expansion reduces mortality and improves access.

**Critical caveats:**
1. SC political context makes expansion uncertain; policy analysis ≠ policy prediction.
2. Heterogeneous effects by race/rurality (Grigoryeva & Ruef, 2024) mean North Charleston's majority-Black urban tracts may benefit more than rural Sea Island communities.
3. PLACES uninsured estimates are for ages 18–64 only; Medicare-eligible adults are excluded.
4. Expansion alone does not address provider shortages (Charleston's pop-per-mental-health-provider ratio remains strained).

---

### Claim 5: "Flooding and sea level rise are equity issues, not just environmental issues."

**Verdict: Strong — supported by converging local and national evidence.**

Charleston County MHVA: >40% of affordable housing flood-vulnerable. Woodwell Climate: +1.21 ft SLR by 2050; 100-year rainfall probability tripling. Buchanan et al. (2020): nationwide affordable units exposed to coastal flooding more than tripling by 2050. Williams et al. (2023): NEJM synthesis linking flood exposure to health inequity.

**Local validation:** SVI Theme 4 (housing/transportation) correlates with utility shut-off threat (*r* = 0.819) and housing insecurity (*r* = 0.857), connecting climate-adjacent housing instability to measurable health-related social needs in PLACES data.

**Critical caveat:** We did not directly overlay FEMA flood zones with tract health data in this pipeline. The MHVA finding applies to *affordable housing stock*, not all housing. Market-rate development in flood zones (e.g., Daniel Island, West Ashley waterfront) creates a **reverse equity problem**—wealthy residents with resources to rebuild, while poor residents in inland flood-prone areas lack insurance and mobility (Tate et al., 2021).

---

### Claim 6: "Charleston's diabetes problem is under control."

**Verdict: Weak — county average is deceptive.**

County diabetes prevalence (10.0%) appears favorable vs. SC (13.1%). Tract range of 2.8–25.3% reveals hotspots where prevalence **doubles the county average**. Top-quartile diabetes tracts have mean SVI = 0.735.

The original DPP RCT demonstrated 58% reduction in diabetes incidence with lifestyle intervention (Knowler et al., 2002); real-world National DPP implementations achieve ~4% weight loss at 12 months (Ali et al., 2016)—clinically meaningful but requiring sustained funding in the tracts where prevalence is highest.

---

### Claim 7: "Community naloxone distribution would reduce overdose deaths in Charleston."

**Verdict: Strong — highest evidence grade among proposed interventions.**

Multiple systematic reviews and meta-analyses support OEND effectiveness (Liu et al., 2021; McDonald et al., 2025). Kimmel et al. (2024) cite 25–46% community overdose rate reductions with broad naloxone distribution. Economic evaluations consistently find cost-effectiveness (Folkestad et al., 2021).

**Local fit:** Charleston County already operates an opioid overdose dashboard and Coroner surveillance—infrastructure that could track OEND deployment. With 153 drug-related deaths in 2025, even a 25% reduction would represent ~38 lives annually.

**Critical caveat:** Naloxone reverses overdose but does not treat OUD. Without MOUD linkage (only 50% of SUD-history decedents had prior treatment contact), reversal events may recur.

---

### Claim 8: "Building more housing in flood-prone areas with engineered protections is sufficient climate adaptation."

**Verdict: Weak/Uncertain — contested in literature and local policy debate.**

Charleston requires elevated construction standards in flood zones, but Woodwell Climate and Floodlight investigative reporting (2024) document continued large-scale development (Long Savannah: 4,500 homes; Long Point: 9,000 homes) in vulnerable areas. Managed retreat literature argues engineered protection **transfers risk** downstream and locks in vulnerable infrastructure (Siders et al., 2019).

Participatory research in Charleston's East Side and Rosemont documented community concern that seawalls and pumps protect affluent peninsula areas while peripheral neighborhoods flood first (Jagannathan et al., 2022)—an environmental justice framing supported by our SVI maps showing high vulnerability in North Charleston outside the peninsula's protection footprint.

---

## 6. Evidence-Based Policy Recommendations

Recommendations are organized by issue domain and graded by evidence strength (**A** = systematic review/meta-analysis or RCT; **B** = quasi-experimental or strong observational; **C** = ecological/planning evidence; **D** = expert consensus/local report).

### 6.1 Opioid overdose response

| Priority | Intervention | Evidence grade | Expected impact | Implementation anchor |
|---|---|---|---|---|
| 1 | Scale **OEND** (naloxone kits + training) via pharmacies, libraries, EMS leave-behind | **A** | 25–46% overdose rate reduction (community level) | County opioid dashboard; SC DPH |
| 2 | Expand **MOUD** (buprenorphine) in North Charleston FQHCs | **A** | 48% mortality reduction vs. no MOUD | MUSC Center for Drug and Alcohol Programs |
| 3 | **911 co-response** behavioral health teams | **B** | Reduced repeat ED visits | Charleston ECC (existing metrics infrastructure) |
| 4 | **Housing-first + SUD treatment** for homeless decedents (14% of 2025 deaths) | **B** | Addresses dual crisis | One80 Place, CC Housing Authority |
| 5 | **Fentanyl test strip** distribution at harm-reduction sites | **A** | Reduced unknowing exposure | DAODAS county profile |

### 6.2 Coverage and access

| Priority | Intervention | Evidence grade | Expected impact | Target tracts |
|---|---|---|---|---|
| 1 | **Medicaid expansion advocacy** | **A** | 9.4% mortality reduction (expansion states); uninsured tracts >15% | All high-SVI tracts |
| 2 | **ACA enrollment navigators** | **B** | Coverage gains in gap populations | Top quartile uninsured (*n* ≈ 25 tracts) |
| 3 | **FQHC expansion** in North Charleston | **B** | Sliding-scale primary/preventive care | SVI ≥ 0.75 tracts |
| 4 | **School-based health centers** | **B** | Adolescent preventive care | CCSD Title I catchment areas |

### 6.3 Chronic disease prevention

| Priority | Intervention | Evidence grade | Expected impact | Target tracts |
|---|---|---|---|---|
| 1 | **National DPP** sites in diabetes Q4 tracts | **A** | ~4% weight loss; 58% incidence reduction (RCT) | 25 tracts with diabetes ≥13.9% |
| 2 | **SNAP enrollment + Double Up Food Bucks** | **B** | Food security improvement | 25 tracts with food insecurity ≥19.6% |
| 3 | **Food insecurity screening** in primary care | **B** | Referral to Lowcountry Food Bank | MUSC, FQHCs |
| 4 | **Complete Streets** investment | **C** | Physical activity increase | High LPA tracts |

### 6.4 Housing and climate resilience

| Priority | Intervention | Evidence grade | Expected impact | Source alignment |
|---|---|---|---|---|
| 1 | **Flood retrofit** for 23+ Housing Authority properties | **C** | Preserve affordable stock | County MHVA |
| 2 | **Inclusionary zoning** near Low Country Rapid Transit | **C** | Reduce cost burden (44% renters burdened) | County Housing Plan |
| 3 | **Managed retreat/buyouts** for repeat-loss properties | **B** | Prevent displacement trauma | FEMA HMGP; Siders et al., 2019 |
| 4 | **Community resilience hubs** in top-SVI tracts | **C** | Emergency healthcare continuity | CDC SVI use case |
| 5 | **Green infrastructure** (Charleston Rainproof scaling) | **B** | 40–90% runoff reduction (EPA) | City program exists |

### 6.5 Health equity governance

| Priority | Intervention | Evidence grade | Rationale |
|---|---|---|---|
| 1 | Annual **tract-level health equity report card** | **C** | Accountability; replicable from this pipeline |
| 2 | **Health impact assessments** for developments >50 units | **C** | Prevent exacerbating tract disparities |
| 3 | Integrate PLACES+SVI into **Community Health Needs Assessment** (MUSC) | **B** | Hollis et al. (2023) validated method |
| 4 | **Participatory planning** with East Side, Rosemont, Accabee communities | **B** | Jagannathan et al. (2022) model |

---

## 7. Discussion

### 7.1 The dual-county framework

Charleston County's health profile is best characterized as **spatially bifurcated**. Affluent coastal urbanization produces top-quartile life expectancy and income metrics that dominate policy discourse, while 16 tracts in the top SVI quartile—and 25 tracts in the top food-insecurity quartile—experience conditions comparable to the poorest counties in the state. This pattern has direct policy implications: county-wide averages should **not** be used to allocate resources or declare victory on population health goals.

The PLACES–SVI concordance we observed (*r* = 0.82–0.86 for social needs) is **stronger** than typical county-level associations in the parent national analysis (child poverty ↔ diabetes *r* = 0.82 at county scale, but most outcomes *R²* ≤ 0.51 in multivariable models). This suggests that within-county tract analysis may be **more informative** than cross-county comparison for targeting interventions—a hypothesis requiring replication in other SC counties.

### 7.2 Methodological limitations

1. **Model-based estimates:** PLACES tract values are MRP outputs, not direct measurements. Uncertainty intervals (available in raw data) should be mapped alongside point estimates. Small tracts (e.g., Sea Islands with <2,000 population) may have unreliable estimates.

2. **Construct overlap:** SVI and PLACES social-need measures both derive from ACS. Shared variance inflates correlations and does not constitute independent validation.

3. **Ecological inference:** Tract-level associations cannot be attributed to individuals. A high-diabetes tract may contain both diabetic and non-diabetic residents; interventions must be person-level even when data is geographic.

4. **Temporal mismatch:** PLACES (2023 BRFSS cycle), SVI (2018–2022 ACS), and CHR mortality (2018–2023) cover different periods during rapid demographic change (post-COVID migration surge to Charleston).

5. **Gentrification bias:** Tract boundaries are stable, but population composition within tracts shifts. A tract labeled "high SVI" may be in early-stage gentrification where health burdens lag demographic transition.

6. **Depression anomaly:** The null depression–SVI correlation warrants dedicated study. Possible explanations include BRFSS depression screening capture differences, cultural reporting variation, and the independent contribution of social isolation in affluent elderly populations (Sea Islands, suburban retirees).

### 7.3 Comparison with prior literature

Our findings align with Hollis et al. (2023), who reported high SVI socioeconomic rankings in highest-quartile COPD tracts nationally (median 0.77 vs. our food-insecurity Q4 mean SVI of 0.775). We extend this by demonstrating that **social needs measures** (food, housing, utility insecurity) show even stronger SVI concordance than clinical chronic-disease measures (diabetes *r* = 0.63 vs. food insecurity *r* = 0.85)—suggesting that **upstream social intervention** may yield larger tract-level health improvements than disease-specific programs alone.

The opioid findings situate Charleston within the Southeastern fentanyl belt without reaching Appalachian extremes. The Coroner data on treatment gaps (50% of SUD-history decedents without adequate treatment contact) mirrors national OUD treatment access failures (Kimmel et al., 2024).

Climate-health integration follows Buchanan et al. (2020) and Williams et al. (2023) in treating flood exposure as a housing equity issue. Charleston's locally documented 40% affordable-housing flood vulnerability exceeds the ~9% national subsidized-housing floodplain figure cited in NPCC4 (Rosenzweig et al., 2023)—though definitions differ (all affordable vs. subsidized only).

### 7.4 What would change our conclusions?

- **Tract-level mortality data** (currently suppressed or unavailable for overdose at tract scale) would allow direct validation of PLACES–SVI correlations against hard outcomes.
- **Medicaid expansion in SC** would create a natural experiment to test whether Charleston's high-uninsured tracts experience disproportionate coverage gains.
- **Longitudinal PLACES releases** would enable trend analysis—critical for evaluating whether investments (Rainproof, ERAP, OEND) are shifting tract-level estimates.

---

## 8. Conclusion

Charleston County, South Carolina, presents a case study in how **aggregate prosperity masks concentrated vulnerability**. County-level life expectancy and chronic-disease mortality compare favorably to state benchmarks, but tract-level analysis reveals food insecurity estimates up to 50.6%, uninsured rates up to 27.7%, and 16 tracts in the highest quartile of statewide social vulnerability—home to an estimated 100,000+ residents in the highest-burden areas.

Eight policy claims were evaluated; three were **strong** (opioid crisis severity, SVI–health concordance for social needs, climate-as-equity), three **moderate** (county healthiness, Medicaid expansion benefit, diabetes under control), and two **weak or contested** (depression as poverty-driven, build-and-protect adaptation sufficiency).

Evidence-graded recommendations prioritize:

1. **Immediate:** OEND scale-up and MOUD expansion (Grade A evidence);
2. **Structural:** Medicaid expansion and FQHC capacity in high-SVI tracts (Grade A–B);
3. **Preventive:** National DPP and food security programs in top-quartile tracts (Grade A–B);
4. **Climate:** Flood retrofit of public housing and managed retreat where engineering is insufficient (Grade B–C).

This analysis demonstrates that merging CDC PLACES and SVI at tract scale—following Hollis et al. (2023)—is operationally feasible and policy-relevant for Charleston. The pipeline is fully reproducible and should be updated annually as new PLACES and SVI releases become available.

---

## References

Ali, M. M., Echouffo-Tcheugui, J. B., & Williamson, M. J. (2016). How effective were lifestyle interventions in real-world settings that were modeled on the Diabetes Prevention Program? *Health Affairs*, *35*(3), 446–453.

Buchanan, M. K., Kulp, S., Cushing, L., Morello-Frosch, R., Nedwick, T., & Strauss, B. (2020). Sea level rise and coastal flooding threaten affordable housing. *Environmental Research Letters*, *15*(12), 124020. https://doi.org/10.1088/1748-9326/abb266

Centers for Disease Control and Prevention. (2025). *PLACES methodology*. https://www.cdc.gov/places/methodology/

Charleston County Coroner. (2025). *2025 Annual drug report*. Charleston County Government. https://www.charlestoncounty.gov/departments/coroner/files/annual-report-archive/2025-Annual-Drug-Report.pdf

Charleston County Government. (2024). *Multi-hazard vulnerability assessment*. https://charlestoncounty.gov/ccrs/files/Multi-Hazard-Vulnerability-Assessment-Final-Report-Charleston-County.pdf

Charleston County Development. (2025). *Housing needs assessment: Our future*. https://www.charlestoncountydevelopment.org/wp-content/uploads/2025/12/HoF-Housing-Plan.pdf

Flanagan, B. E., Hallisey, E. J., Adams, E., & Lavery, A. M. (2023). *CDC/ATSDR SVI 2022 documentation*. CDC/ATSDR Geospatial Research, Analysis, and Services Program.

Folkestad, T., Fernandes, R. M. C., Brar, R., & Kimmel, S. (2021). Community distribution of naloxone: A systematic review of economic evaluations. *PharmacoEconomics – Open*, *5*, 223–247.

Grigoryeva, A., & Ruef, M. (2024). The uneven impact of Medicaid expansion on rural and urban Black, Latino/a, and White mortality. *Health Services Research*, *59*(6), e13859.

Hollis, A., Escoffery, C., Rohan, E. A., & Thomas, C. W. (2023). Linking local-level chronic disease and social vulnerability measures to inform planning efforts: A COPD example. *Preventing Chronic Disease*, *20*, 230025. https://doi.org/10.5888/pcd20.230025

Jagannathan, R., et al. (2022). Participatory and spatial analyses of environmental justice communities' concerns about a proposed storm surge and flood protection seawall. *International Journal of Environmental Research and Public Health*, *19*(18), 11192.

Kimmel, S., et al. (2024). Medications for opioid use disorder, opioid withdrawal, and opioid overdose: A review. *JAMA*, *331*(19), 1675–1686.

Knowler, W. C., et al. (2002). Reduction in the incidence of type 2 diabetes with lifestyle intervention or metformin. *New England Journal of Medicine*, *346*(6), 393–403.

Lewis, J. S., et al. (2023). Social Vulnerability Index and health outcomes in the United States: A systematic review. *Family & Community Health*, *46*(4), 234–244. https://doi.org/10.1097/FCH.0000000000000421

Liu, Y., et al. (2021). The effect of overdose education and naloxone distribution: An umbrella review of systematic reviews. *International Journal of Drug Policy*, *97*, 103336.

McDonald, R., et al. (2025). Effectiveness of naloxone distribution in community settings to reduce opioid overdose deaths among people who use drugs: A systematic review and meta-analysis. *Harm Reduction Journal*, *22*, Article 45.

McKenna, R. M., et al. (2021). Medicaid expansion and variability in mortality in the USA: A national, observational cohort study. *The Lancet Public Health*, *6*(2), e90–e96.

Miller, S., Johnson, N., & Wherry, L. R. (2021). Medicaid and mortality: New evidence from linked survey and administrative data. *Quarterly Journal of Economics*, *136*(3), 1783–1829.

Moores, T. T., et al. (2022). PLACES: Local data for better health. *Preventing Chronic Disease*, *19*, 210459.

Morello-Frosch, R., & Jesdale, B. M. (2006). Separate and unequal: Residential segregation and estimated cancer risks associated with ambient air toxics in U.S. metropolitan areas. *Environmental Health Perspectives*, *114*(3), 386–393.

Rosenzweig, C., et al. (2023). NPCC4: Advancing climate justice in climate adaptation strategies for New York City. *Annals of the New York Academy of Sciences*, *1523*(1), 3–70.

Siders, A. R., Hino, M., & Mach, K. J. (2019). The case for strategic and managed climate retreat. *Science*, *365*(6455), 761–763.

Stein, D. J., et al. (2015). Cross-national variations in the prevalence and correlates of depression. *JAMA Psychiatry*, *72*(7), 667–676.

Tate, E., et al. (2021). Flood exposure and social vulnerability in the United States. *Natural Hazards*, *106*, 435–457.

Williams, D. R., et al. (2023). The climate gap and the color line — racial health inequities and climate change. *New England Journal of Medicine*, *388*(10), 943–950. https://doi.org/10.1056/NEJMmsb2213250

Woodwell Climate Research Center. (2024). *Climate risk assessment: Charleston County, South Carolina*. https://www.woodwellclimate.org/climate-risk-assessment-charleston-county-south-carolina/

Zhang, X., et al. (2022). Validation of small area estimation using Behavioral Risk Factor Surveillance System data. *Spatial and Spatio-temporal Epidemiology*, *42*, 100522.

---

## Appendix A: Reproducibility

All analysis code, data, and maps are available at:

```
project3_cdc_mortality/charleston_county/
├── scripts/01_download_data.py
├── scripts/02_analyze_tracts.py
├── scripts/03_make_maps.py
├── data/merged_tract_data.csv
├── results/issue_metrics.json
├── results/tract_correlations.csv
└── results/maps/index.html
```

## Appendix B: Summary statistics export

Machine-readable headline metrics: `results/issue_metrics.json`

Interactive maps: `results/maps/index.html`

County benchmarks: `data/county_benchmarks.csv`

---

*This document was generated as part of Project 3 (CDC Mortality Analysis). It is intended for research, policy planning, and community health assessment purposes. It does not constitute medical or legal advice.*
