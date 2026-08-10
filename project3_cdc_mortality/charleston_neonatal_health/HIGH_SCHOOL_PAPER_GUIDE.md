# How to Turn This Package Into a Research Paper (High School Guide)

This folder gives you **real data**, **sources**, and **analysis**. Follow these steps to write a polished research paper for science fair, AP Research, English, or social studies.

---

## Step 1: Pick your research question

Choose **one focused question**. Examples:

1. *Why are Black babies in Charleston County more likely to be born low birthweight than White babies?*
2. *Is inadequate prenatal care driving infant mortality trends in Charleston?*
3. *How do food insecurity and housing problems in Charleston tracts relate to neonatal health risk?*

**Tip:** One clear question beats trying to cover everything.

---

## Step 2: Gather your evidence (use our files)

| What you need | Where to find it |
|---|---|
| Statistics with sources | `data/county_neonatal_indicators.csv` or `DATA_CATALOG.md` |
| Main analysis & context | `RESEARCH_FOUNDATION.md` |
| Black–White gaps | `results/racial_disparities.csv` |
| Maps for figures | `results/maps/index.html` (screenshot for appendix) |
| All factor topics | `FACTOR_FRAMEWORK.md` |

**Rule:** Every number in your paper needs a **footnote or in-text citation** with the source URL from the CSV.

---

## Step 3: Standard paper outline

### Title page
- Title (specific, not vague)
- Your name, school, date
- Optional: Charleston County, SC

### Abstract (150–250 words)
Summarize: **problem**, **key data**, **main finding**, **why it matters**.

Example opening:
> In Charleston County, South Carolina, 17.3% of Black infants were born low birthweight in 2023 compared with 6.1% of White infants (SC DPH Vital Metrics Summary, Table C-27)...

### I. Introduction
- Hook: a local story or striking statistic (e.g., 1 in 10 preterm births)
- Background on infant/neonatal health
- Your research question
- Thesis statement (your main argument)

### II. Methods (short)
Explain where data came from:
> This study uses publicly available data from the South Carolina Department of Public Health Vital Metrics Summary 2023 and March of Dimes PeriStats accessed August 2026. Tract-level maps use CDC PLACES 2025 and Social Vulnerability Index 2022 as proxies because infant death counts are not published by census tract.

### III. Results
Organize by sub-topic. Use **tables and figures**.

**Suggested tables:**

| Group | Low birthweight % | Source |
|---|---|---|
| All | 9.1% | VMS 2023 |
| White | 6.1% | VMS 2023 |
| Black | 17.3% | VMS 2023 |

**Suggested figures:**
- Map from `results/maps/map_neonatal_risk_proxy_score.html`
- Bar chart comparing Charleston vs SC preterm rates

### IV. Discussion
- What do the results **mean**?
- Why might disparities exist? (access, poverty, racism, environment — cite `FACTOR_FRAMEWORK.md`)
- Limitations: county vs tract data, small number of deaths per year
- What could improve outcomes? (WIC, doulas, Medicaid, prenatal care)

### V. Conclusion
Restate thesis with evidence. End with a **call to action** (policy, awareness, future research).

### References
Use **APA** or your teacher's format. Example:

```
South Carolina Department of Public Health. (2025). Vital metrics summary 2023. 
  https://dph.sc.gov/sites/scdph/files/2025-11/VMS-2023.pdf

March of Dimes. (2026). Preterm birth rate: Charleston, 2017-2024. PeriStats. 
  https://www.marchofdimes.org/peristats/data?creg=45019&top=3&stop=60
```

---

## Step 4: Citation cheat sheet

| Source type | What to include |
|---|---|
| VMS PDF | SC DPH, year, table number, page if known, URL |
| March of Dimes | "March of Dimes PeriStats," indicator name, year, URL |
| CDC PLACES | CDC PLACES 2025, measure name, URL to data.cdc.gov |
| County Health Rankings | County name, year, measure, countyhealthrankings.org URL |

Copy URLs directly from `data/county_neonatal_indicators.csv` column `source_url`.

---

## Step 5: Strong thesis examples

**Weak:** "Baby health in Charleston is bad."

**Strong:** "Although Charleston County's infant mortality rate (4.3 per 1,000 in 2023) is lower than South Carolina's state average (7.0), racial disparities in low birthweight and prenatal care adequacy reveal a two-tier system of perinatal health that disproportionately harms Black families."

---

## Step 6: Checklist before submitting

- [ ] Research question stated in introduction
- [ ] Thesis in last sentence of introduction
- [ ] At least **8–10 cited statistics** from primary sources
- [ ] At least **one table** and **one figure**
- [ ] Discussion mentions **limitations**
- [ ] References page matches in-text citations
- [ ] No uncited numbers

---

## Step 7: Presentation tips (science fair / class)

1. Open with: **"1 in 10 babies in Charleston is born too soon."** (March of Dimes 2024)
2. Show the **LBW disparity chart** (Black vs White)
3. Show one **tract map** — explain proxies honestly
4. Close with **action**: expand WIC outreach, doula Medicaid reimbursement, etc.

---

## Need help?

- All definitions: see Glossary in `FACTOR_FRAMEWORK.md`
- Every stat: `DATA_CATALOG.md`
- Deep analysis: `RESEARCH_FOUNDATION.md` Sections 2–9

Good luck — you have the same data sources used in graduate public health research.
