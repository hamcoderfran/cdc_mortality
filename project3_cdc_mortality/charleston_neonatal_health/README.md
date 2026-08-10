# Charleston County Neonatal & Infant Health — Research Foundation Package

**Purpose:** Graduate-level, fully cited analysis of baby and neonatal health in Charleston, South Carolina (FIPS **45019**). Designed as the evidence base for a research paper documenting inequities and gaps in regional perinatal care.

**Audience:** Researchers, journalists, policy advocates, and **high school students** converting this into a formal paper (see [`HIGH_SCHOOL_PAPER_GUIDE.md`](HIGH_SCHOOL_PAPER_GUIDE.md)).

---

## Quick start

1. Read the executive summary in [`RESEARCH_FOUNDATION.md`](RESEARCH_FOUNDATION.md).
2. Look up any statistic in [`DATA_CATALOG.md`](DATA_CATALOG.md) — every value has a source URL.
3. Open interactive maps: [`results/maps/index.html`](results/maps/index.html).
4. Browse raw cited data: [`data/county_neonatal_indicators.csv`](data/county_neonatal_indicators.csv).

### Run the data pipeline

```bash
cd project3_cdc_mortality/charleston_neonatal_health/scripts
python3 01_download_neonatal_data.py
python3 02_analyze_disparities.py
python3 03_make_maps.py
```

Requirements: `pandas`, `requests`, `plotly`, `numpy`.

---

## Email this folder

Zip the entire `charleston_neonatal_health` directory:

```bash
cd project3_cdc_mortality
zip -r charleston_neonatal_health.zip charleston_neonatal_health/
```

The zip includes all markdown reports, cited CSVs, JSON summaries, scripts, and HTML maps (~15–25 MB depending on map generation).

---

## Folder contents

| File / folder | Description |
|---|---|
| `RESEARCH_FOUNDATION.md` | Main graduate-level analysis (~9,000 words) |
| `HIGH_SCHOOL_PAPER_GUIDE.md` | Step-by-step instructions to write a research paper |
| `DATA_CATALOG.md` | Every statistic with citation |
| `FACTOR_FRAMEWORK.md` | All factor domains affecting neonatal health |
| `data/county_neonatal_indicators.csv` | Master indicator table with source URLs |
| `data/factor_evidence_matrix.csv` | Factor → indicator → source mapping |
| `data/sc_state_benchmarks.csv` | Charleston vs South Carolina comparisons |
| `results/disparity_summary.json` | Key findings + top burden tracts |
| `results/racial_disparities.csv` | Black–White disparity ratios |
| `results/tract_neonatal_risk_proxy.csv` | Tract SDOH composite score |
| `results/maps/` | Interactive choropleth maps |
| `scripts/` | Reproducible download and analysis pipeline |

---

## Key findings (Charleston County)

| Indicator | Charleston | SC benchmark | Source |
|---|---|---|---|
| Preterm birth (2024) | **10.5%** (grade D+) | 11.6% (grade F) | [March of Dimes](https://www.marchofdimes.org/peristats/reports/south-carolina/report-card) |
| Low birthweight (2023) | **9.1%** | 9.7% (2024) | [SC DPH VMS 2023](https://dph.sc.gov/sites/scdph/files/2025-11/VMS-2023.pdf) |
| LBW — Black vs White | **17.3% vs 6.1%** (2.8×) | — | VMS Table C-27 |
| Infant mortality (2023, VMS) | **4.3** per 1,000 | 7.0 (state) | VMS Table F-3 |
| Infant mortality trend | **+48%** (2013–2023) | Worsened statewide | [PeriStats](https://www.marchofdimes.org/peristats/data?creg=45019&top=6&stop=91) |
| IMR Black (3-yr avg) | **13.7** per 1,000 | — | PeriStats |
| IMR White (3-yr avg) | **5.3** per 1,000 | — | PeriStats |
| Inadequate prenatal care | **14.5%** | 20.6% inadequate+intermediate gap | PeriStats |
| Medicaid at birth | **50.3%** | 43.1% (state, 2024) | VMS Table C-35 |
| WIC during pregnancy | **34.6%** | — | VMS Table C-34 |

---

## Important limitations

- **No public tract-level infant mortality** exists for South Carolina. Tract maps use CDC PLACES social-needs and SVI as *proxies*, not measured neonatal deaths.
- **Small numbers:** VMS warns rates with ≤20 deaths are unreliable; interpret single-year county race-specific rates cautiously.
- **VMS vs PeriStats:** Residence-based vital statistics (VMS) and linked birth–infant-death files (PeriStats) can differ slightly (e.g., IMR 4.3 vs 6.2 for Charleston 2023).

---

## Related work in this repository

- [`../charleston_county/`](../charleston_county/) — Adult tract-level health & equity analysis (98 tracts)
- [`../README.md`](../README.md) — National/county mortality project overview

---

## Suggested citation

> Charleston County Neonatal Health Research Foundation Package. Data from SC DPH Vital Metrics Summary 2023, March of Dimes PeriStats 2024–2026, CDC PLACES 2025, CDC/ATSDR SVI 2022, County Health Rankings 2025. Compiled August 2026.
