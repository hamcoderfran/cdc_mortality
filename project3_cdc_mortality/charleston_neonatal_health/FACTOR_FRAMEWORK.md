# Factor Framework: Every Domain Affecting Neonatal Health in Charleston

This matrix lists **all major factor domains**, the indicators we track, evidence type, and primary source. Use with `data/factor_evidence_matrix.csv` for machine-readable version.

**Evidence types:**
- **direct** — measured birth/pregnancy outcome or utilization
- **proxy** — community measure linked to birth outcomes in literature
- **context** — environmental/system factor
- **qualitative** — facility/policy description

---

## 1. Clinical birth outcomes

| Factor | Indicators | Charleston data | Source |
|---|---|---|---|
| Preterm birth | preterm_birth_pct, very_preterm_pct | 10.5% (2024) | [March of Dimes](https://www.marchofdimes.org/peristats/data?creg=45019&top=3&stop=60) |
| Low birthweight | low_birthweight_pct, lbw by race | 9.1%; Black 17.3% | [VMS 2023 Table C-27](https://dph.sc.gov/sites/scdph/files/2025-11/VMS-2023.pdf) |
| Very low birthweight | very_low_birthweight_pct | 1.0% | VMS Table C-29 |
| Infant mortality | infant_mortality_rate | 4.3–6.2/1000 (source-dependent) | VMS F-3; PeriStats |
| Neonatal mortality | neonatal_mortality_rate | 2.5/1000 (2023) | VMS Table F-4 |
| Postneonatal mortality | postneonatal rate | 1.9/1000 | VMS Table F-5 |
| Multiple births | multiple_birth_pct | 3.2% | PeriStats |

---

## 2. Prenatal care access

| Factor | Indicators | Charleston data | Source |
|---|---|---|---|
| Timing of care | early / late / no PNC % | 6.2% late/none | PeriStats PNC |
| Adequacy (Kotelchuck) | adequate+, inadequate % | 14.5% inadequate | PeriStats |
| Racial gap in adequacy | kotelchuck by race | Black 36.6% inadequate vs White 16.9% | VMS C-11A |
| Prenatal visit counts | 0, 1–4, 5+ visits | 18 zero visits (White table row) | VMS C-10A |

---

## 3. Insurance & financing

| Factor | Indicators | Charleston data | Source |
|---|---|---|---|
| Medicaid births | medicaid_births_pct | 50.3% overall; Black 70.3% | VMS C-35 |
| Private insurance | private_insurance_pct | 23.9% | VMS C-35 |
| Self-pay / uninsured at delivery | self_pay_births_pct | 22.6% | VMS C-35 |
| Community uninsurance | uninsured_adults_pct | 14.2% | County Health Rankings |

---

## 4. Nutrition & WIC

| Factor | Indicators | Charleston data | Source |
|---|---|---|---|
| WIC in pregnancy | wic_during_pregnancy_pct | 34.6% | VMS C-34 |
| Food environment | food_environment_index | 7.1 | County Health Rankings |
| Tract food insecurity | food_insecurity_pct | 2.9%–50.6% range | CDC PLACES |
| Maternal obesity | maternal_obesity_bmi_pct | ~39% NH White & Black | VMS C-36 |

---

## 5. Maternal demographics & social support

| Factor | Indicators | Charleston data | Source |
|---|---|---|---|
| Teen births | teen_births_under_20_pct | 10.7% | VMS C-19 |
| Unmarried births | unmarried_births_pct | 35.5%; Black 73.1% | VMS C-21 |
| Maternal education | bachelor's degree+ | 27.4% of White births (614/2901) | VMS C-12 |
| Fertility rate | fertility_rate | 56.2/1000 women 15–44 | PeriStats |

---

## 6. Delivery & hospital care

| Factor | Indicators | Charleston data | Source |
|---|---|---|---|
| Cesarean section | cesarean_delivery_pct | 31.9% | PeriStats |
| In-hospital birth | births_in_hospital_pct | 93.7% occurrence | VMS C-14 |
| Regional birth volume | births_occurred_in_county | 7,521 | VMS C-13 |
| Level IV NICU | MUSC | State referral center | MUSC website |
| Other maternity hospitals | Roper, Bon Secours | High-performing | U.S. News |

---

## 7. Maternal safety (state level)

| Factor | Indicators | SC data | Source |
|---|---|---|---|
| Maternal mortality | maternal_mortality_per_100k | 31.5 | March of Dimes Report Card |
| Severe maternal morbidity | SMM per 10k deliveries | 85.9 | Same |
| Low-risk cesarean | low_risk_cesarean_pct | 25.6% | Same |

*Charleston-specific maternal mortality is suppressed in public reports due to small counts.*

---

## 8. Environment & built environment

| Factor | Indicators | Charleston data | Source |
|---|---|---|---|
| Air pollution | pm25_ug_m3 | 8.4 µg/m³ | County Health Rankings |
| Housing stress | severe_housing_problems_pct | 34.2% | Same |
| Tract housing insecurity | housing_insecurity_pct | tract-level | CDC PLACES |
| Climate/flood risk | — | qualitative | Charleston County MHVA report |
| Utility shut-off threat | utility_shutoff_pct | tract-level | CDC PLACES |

---

## 9. Poverty & structural determinants

| Factor | Indicators | Charleston data | Source |
|---|---|---|---|
| Child poverty | child_poverty_pct | 9.7% | County Health Rankings |
| Social Vulnerability Index | RPL_THEMES | 0.01–0.99 across tracts | CDC SVI 2022 |
| Life expectancy | life_expectancy_years | 77.9 | County Health Rankings |
| Transportation barriers | transportation_barrier_pct | tract-level | CDC PLACES |

---

## 10. Racial equity & systemic factors

| Factor | Indicators | Disparity | Source |
|---|---|---|---|
| LBW Black/White | lbw_pct_black / lbw_pct_white | **2.8×** | VMS C-27 |
| IMR Black/White | 13.7 / 5.3 per 1000 | **2.6×** | PeriStats 2021–23 |
| Inadequate PNC | Kotelchuck inadequate | **2.2×** | VMS C-11A |
| Medicaid at birth | 70.3% vs 26.9% | **2.6×** | VMS C-35A |
| Unmarried births | 73.1% vs 14.1% | **5.2×** | VMS C-21 |

**Structural mechanisms (literature):** obstetric racism, hospital segregation, weathering, economic exclusion, environmental injustice.

---

## 11. Policy & programs (research targets)

| Strategy | Status in SC/Charleston | Research angle |
|---|---|---|
| Medicaid expansion | Expanded; 12-month postpartum | First-trimester enrollment gaps |
| WIC | 34.6% penetration | Eligible but not served |
| Doula reimbursement | Limited/pilot | Impact on Black prematurity |
| Perinatal quality collaborative | State MCH bureau | Public race-stratified dashboards |
| Level IV NICU regionalization | MUSC hub | Transport time equity |
| Home visiting (NFP, MIECHV) | Available | Penetration in high-SVI tracts |

---

## Glossary (for papers)

| Term | Definition |
|---|---|
| **Neonatal** | First 0–27 days after birth |
| **Postneonatal** | 28 days through 364 days |
| **Infant mortality** | Death before first birthday |
| **Preterm** | Born before 37 weeks gestation |
| **LBW** | Birthweight under 2,500 grams |
| **VLBW** | Birthweight under 1,500 grams |
| **Kotelchuck index** | Standard measure of prenatal care adequacy |
| **SVI** | CDC Social Vulnerability Index (disaster/health disadvantage) |
| **NICU levels** | I–IV; IV = highest acuity (ECMO, complex surgery) |
| **FIPS 45019** | Federal code for Charleston County, SC |

---

## Data not publicly available (gaps for investigative work)

1. Hospital-specific morbidity/mortality by race and ZIP  
2. Tract- or ZIP-level infant mortality (suppressed)  
3. Maternal mortality county counts  
4. Smoking during pregnancy county tables (collected on birth certificate; not in VMS 2023 tables extracted)  
5. Breastfeeding initiation by race at county level  
6. Average NICU transport time by origin ZIP  

Request via SC DPH records or hospital transparency advocacy.
