"""
Charleston neonatal health — step 1: download tract SDOH + build cited indicator tables
======================================================================================

Pulls census-tract social determinants (CDC PLACES, SVI, TIGER boundaries) and
writes county-level neonatal/MCH indicators with source URL on every row.

Outputs:
  ../data/county_neonatal_indicators.csv
  ../data/sc_state_benchmarks.csv
  ../data/factor_evidence_matrix.csv
  ../data/places_tracts_long.csv
  ../data/svi_tracts.csv
  ../data/tract_boundaries.geojson
"""

import json
import os

import pandas as pd
import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
COUNTY_FIPS = "45019"
STATE_FIPS = "45"
COUNTY_CODE = "019"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CharlestonNeonatalHealth/1.0)"}

PLACES_URL = "https://data.cdc.gov/resource/cwsq-ngmh.json"
SVI_URL = (
    "https://onemap.cdc.gov/onemapservices/rest/services/SVI/"
    "CDC_ATSDR_Social_Vulnerability_Index_2022_USA/FeatureServer/2/query"
)
TIGER_URL = (
    "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
    "tigerWMS_ACS2022/MapServer/6/query"
)

VMS_PDF = "https://dph.sc.gov/sites/scdph/files/2025-11/VMS-2023.pdf"
MOD_BASE = "https://www.marchofdimes.org/peristats/data"
MOD_REPORT = "https://www.marchofdimes.org/peristats/reports/south-carolina/report-card"
MOD_CHARLESTON = f"{MOD_BASE}?creg=45019&lev=1&obj=1&reg=99&slev=6&sreg=45"
SC_DPH_SCAN = "https://apps.dhec.sc.gov/Health/Scan/scan/mch/infantmortality/"
SC_CHP = "https://dataviz.dph.sc.gov/chp/"
CHR = "https://www.countyhealthrankings.org/health-data/south-carolina/charleston"
MUSC_NICU = "https://musckids.org/health-care-services/childrens-health/neonatal-intensive-care"
HP2030 = "https://health.gov/healthypeople/objectives-and-data/browse-objectives/pregnancy-and-childbirth"
SCMMMRC_2026 = "https://dph.sc.gov/sites/scdph/files/Library/00229-ENG-CR.pdf"
SCMMMRC_2025 = "https://www.scstatehouse.gov/reports/DeptofPublicHealth/SCMMMRC%20Legislative%20Report%202025.pdf"
MOD_MCD_SC = "https://www.marchofdimes.org/peristats/assets/s3/reports/mcd/Maternity-Care-Report-SouthCarolina.pdf"
MOD_MCD_2024 = "https://www.marchofdimes.org/peristats/assets/s3/reports/2024-Maternity-Care-Report.pdf"
SCBOI_2022 = "https://schealthviz.sc.edu/media/SCBOI_annual_IFS_011222.pdf"
USC_IMPH_SNAPSHOT = "https://www.schealthviz.sc.edu/media/downloads/SC%20IMPH%20Health%20Policy%20Summit%20-%20MCH%20Data%20Snapshot.pdf"
FIERCE_HEALTHCARE_OB = "https://www.fiercehealthcare.com/providers/most-states-saw-hospital-obstetric-service-shutdowns-2010-2022-rural-states-hit-hardest"
POST_COURIER_LAURENS = "https://www.postandcourier.com/news/rural-hospitals-maternity-care-sc/article_a03a1884-d8eb-11ef-88cd-079658524226.html"
HRSA_TVIS_NAS = "https://mchb.tvisdata.hrsa.gov/Narratives/ExecutiveSummary/a933ee78-b3e1-42ff-bda0-09cba7e29967"
MAIN_SCIENCEDIRECT_NAS = "https://www.sciencedirect.com/science/article/abs/pii/S221307641930274X"
PEDIATRIX_HORRY_NAS = "https://www.pediatrix.com/about/for-media/news/south-carolinas-horry-county-leads-state-in-number-of-drug-dependent-babies"
CDC_BF_REPORT_CARD_2022 = "https://restoredcdc.org/www.cdc.gov/breastfeeding-data/breastfeeding-report-card/index.html"
SC_WIC_BF_FACTSHEET = "https://dph.sc.gov/sites/scdph/files/Library/00112-ENG-CR.pdf"
BLACKHEALTH_SC_DOULA = "https://www.blackhealth.org/medicaid/south-carolina/"
SC_H3108_DOULA_BILL = "https://www.scstatehouse.gov/sess126_2025-2026/bills/3108.htm"
CRADLE_TRIAL_PMC = "https://pmc.ncbi.nlm.nih.gov/articles/PMC9729420/"
CRADLE_TRIAL_REGISTRY = "https://clinicaltrials.gov/study/NCT02640638"
PICKLESIMER_2012_AJOG = "https://www.ajog.org/article/S0002-9378(12)00131-7/fulltext"
GAREAU_2016_CENTERING = "https://centeringhealthcare.org/news/new-study-finds-medicaid-savings-and-better-outcomes-through-centeringpregnancy"
ROBINSON_2018_JWH = "https://doi.org/10.1089/jwh.2018.7469"
COCHRANE_CONTINUOUS_SUPPORT = "https://www.cochrane.org/evidence/CD003766_continuous-support-women-during-childbirth"
NFP_EVIDENCE_SUMMARY = "https://evidencebasedprograms.org/document/nurse-family-partnership-nfp-evidence-summary/"
NFP_PROJECTED_OUTCOMES = "https://pmc.ncbi.nlm.nih.gov/articles/PMC4512284/"


def fetch_places_tracts():
    rows, offset, page = [], 0, 5000
    while True:
        params = {
            "$where": f"countyfips='{COUNTY_FIPS}'",
            "$limit": page,
            "$offset": offset,
        }
        r = requests.get(PLACES_URL, params=params, headers=HEADERS, timeout=120)
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        rows.extend(batch)
        offset += page
        if len(batch) < page:
            break
    df = pd.DataFrame(rows)
    df["tract_fips"] = df["locationid"].astype(str).str.zfill(11)
    df["data_value"] = pd.to_numeric(df["data_value"], errors="coerce")
    out = os.path.join(DATA_DIR, "places_tracts_long.csv")
    df.to_csv(out, index=False)
    print(f"PLACES: {len(df)} rows -> {out}")
    return df


def fetch_svi_tracts():
    params = {
        "where": f"STCNTY='{COUNTY_FIPS}'",
        "outFields": (
            "FIPS,RPL_THEMES,RPL_THEME1,RPL_THEME2,RPL_THEME3,RPL_THEME4,"
            "E_TOTPOP,E_POV150,E_UNEMP,E_HBURD,E_UNINSUR,E_NOHSDP"
        ),
        "returnGeometry": "false",
        "f": "json",
    }
    r = requests.get(SVI_URL, params=params, headers=HEADERS, timeout=120)
    r.raise_for_status()
    rows = [f["attributes"] for f in r.json()["features"]]
    df = pd.DataFrame(rows).rename(columns={"FIPS": "tract_fips"})
    df["tract_fips"] = df["tract_fips"].astype(str).str.zfill(11)
    for col in df.columns:
        if col != "tract_fips":
            df[col] = pd.to_numeric(df[col], errors="coerce")
    out = os.path.join(DATA_DIR, "svi_tracts.csv")
    df.to_csv(out, index=False)
    print(f"SVI: {len(df)} tracts -> {out}")
    return df


def fetch_tract_boundaries():
    all_features, offset, page = [], 0, 1000
    while True:
        params = {
            "where": f"STATE='{STATE_FIPS}' AND COUNTY='{COUNTY_CODE}'",
            "outFields": "GEOID,NAME",
            "returnGeometry": "true",
            "outSR": "4326",
            "f": "geojson",
            "resultOffset": offset,
            "resultRecordCount": page,
        }
        r = requests.get(TIGER_URL, params=params, headers=HEADERS, timeout=120)
        r.raise_for_status()
        batch = r.json().get("features", [])
        if not batch:
            break
        all_features.extend(batch)
        offset += page
        if len(batch) < page:
            break
    geojson = {"type": "FeatureCollection", "features": all_features}
    out = os.path.join(DATA_DIR, "tract_boundaries.geojson")
    with open(out, "w") as f:
        json.dump(geojson, f)
    print(f"Boundaries: {len(all_features)} tracts -> {out}")


def build_county_indicators():
    """Every row includes source_name, source_url, table_or_page, year, geography."""
    rows = [
        # --- Birth volume & demographics ---
        ("live_births", 4856, "count", 2023, "Charleston County", "SC DPH Vital Metrics Summary", VMS_PDF, "Table C-25/C-1"),
        ("live_births", 5094, "count", 2024, "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?reg=45019&top=2&stop=1&lev=3&slev=1&obj=1", "Births"),
        ("fertility_rate_per_1000_women_15_44", 56.2, "rate", 2024, "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?reg=45019&top=2&stop=1&lev=3&slev=1&obj=1", "Births"),
        ("births_pct_white_nh", 59.8, "percent", "2022-2024 avg", "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?reg=45019&top=2&stop=1&lev=3&slev=1&obj=1", "Race distribution"),
        ("births_pct_black", 19.9, "percent", "2022-2024 avg", "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?reg=45019&top=2&stop=1&lev=3&slev=1&obj=1", "Race distribution"),
        ("births_pct_hispanic", 15.8, "percent", "2022-2024 avg", "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?reg=45019&top=2&stop=1&lev=3&slev=1&obj=1", "Race/ethnicity"),
        # --- Preterm & birthweight ---
        ("preterm_birth_pct", 10.5, "percent", 2024, "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?creg=45019&top=3&stop=60", "Preterm birth"),
        ("preterm_birth_count", 537, "count", 2024, "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?creg=45019&top=3&stop=60", "Preterm birth"),
        ("preterm_report_card_grade", "D+", "grade", 2024, "Charleston County", "March of Dimes Report Card", MOD_REPORT, "County grades"),
        ("very_preterm_pct", 1.6, "percent", 2024, "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?creg=45019&top=3&stop=55", "Gestational age"),
        ("moderately_preterm_pct", 9.0, "percent", 2024, "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?creg=45019&top=3&stop=55", "Gestational age"),
        ("low_birthweight_pct", 9.1, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-27"),
        ("low_birthweight_count", 442, "count", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-27"),
        ("lbw_pct_white_nh", 6.1, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-27"),
        ("lbw_pct_black", 17.3, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-27"),
        ("lbw_pct_hispanic", 8.0, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-27"),
        ("lbw_pct_mod_periStats", 9.2, "percent", 2024, "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?creg=45019&top=4&stop=75", "Birthweight"),
        ("lbw_black_white_ratio_periStats", 2.9, "ratio", "2021-2023 avg", "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?creg=45019&top=4&stop=75", "Black 18.9% vs White 6.6%"),
        ("very_low_birthweight_pct", 1.0, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-29"),
        ("very_low_birthweight_count", 48, "count", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-29"),
        # --- Infant & neonatal mortality ---
        ("infant_mortality_rate_per_1000", 4.3, "rate", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table F-3"),
        ("infant_deaths", 14, "count", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table F-3"),
        ("infant_mortality_rate_3yr", 5.2, "rate", "2021-2023", "Charleston County", "SC DPH VMS", VMS_PDF, "Table F-3"),
        ("infant_deaths_3yr", 53, "count", "2021-2023", "Charleston County", "SC DPH VMS", VMS_PDF, "Table F-3"),
        ("infant_mortality_rate_periStats", 6.2, "rate", 2023, "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?creg=45019&top=6&stop=91", "Linked birth-infant death"),
        ("infant_deaths_periStats", 30, "count", 2023, "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?creg=45019&top=6&stop=91", "Linked birth-infant death"),
        ("infant_mortality_pct_change_2013_2023", 48, "percent_change", "2013-2023", "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?creg=45019&top=6&stop=91", "Trend"),
        ("infant_mortality_black_per_1000", 13.7, "rate", "2021-2023 avg", "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?creg=45019&top=5&stop=105", "By race"),
        ("infant_mortality_white_per_1000", 5.3, "rate", "2021-2023 avg", "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?creg=45019&top=5&stop=105", "By race"),
        ("infant_mortality_hispanic_per_1000", 4.7, "rate", "2021-2023 avg", "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?creg=45019&top=5&stop=105", "By race"),
        ("neonatal_mortality_rate_per_1000", 2.5, "rate", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table F-4"),
        ("neonatal_deaths", 8, "count", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table F-4"),
        ("neonatal_mortality_rate_3yr", 4.2, "rate", "2021-2023", "Charleston County", "SC DPH VMS", VMS_PDF, "Table F-4"),
        ("neonatal_mortality_white_2023", 7.4, "rate", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table F-4A White"),
        ("neonatal_mortality_black_2023", 2.5, "rate", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table F-4A Black"),
        ("postneonatal_mortality_rate_2023", 1.9, "rate", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table F-5"),
        # --- Prenatal care ---
        ("prenatal_care_adequate_plus_pct", 80.0, "percent", 2024, "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?creg=45019&top=5&stop=105", "Kotelchuck adequate+"),
        ("prenatal_care_inadequate_pct", 14.5, "percent", 2024, "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?creg=45019&top=5&stop=105", "Kotelchuck inadequate"),
        ("prenatal_care_late_or_none_pct", 6.2, "percent", 2024, "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?creg=45019&top=5&stop=105", "Timing"),
        ("kotelchuck_inadequate_pct_white", 16.9, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-11A White"),
        ("kotelchuck_inadequate_pct_black", 36.6, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-11A Black (293/801)"),
        ("kotelchuck_adequate_plus_pct_white", 44.2, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-11A White (510/1154)"),
        ("kotelchuck_adequate_plus_pct_black", 23.6, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-11A Black (189/801)"),
        # --- Insurance & WIC ---
        ("medicaid_births_pct_all", 50.3, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-35 pay source"),
        ("private_insurance_births_pct", 23.9, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-35"),
        ("self_pay_births_pct", 22.6, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-35"),
        ("medicaid_births_pct_white", 26.9, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-35A White"),
        ("medicaid_births_pct_black", 70.3, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-35A Black"),
        ("wic_during_pregnancy_pct", 34.6, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-34"),
        ("wic_during_pregnancy_count", 1678, "count", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-34"),
        ("medicaid_mothers_at_birth_pct_sc", 43.1, "percent", 2024, "South Carolina", "March of Dimes PeriStats", MOD_REPORT, "State indicator"),
        # --- Social & maternal risk ---
        ("unmarried_births_pct_all", 35.5, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-21"),
        ("unmarried_births_pct_white", 14.1, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-21"),
        ("unmarried_births_pct_black", 73.1, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-21"),
        ("teen_births_under_20_pct", 10.7, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-19"),
        ("teen_births_under_20_count", 522, "count", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-19"),
        ("maternal_obesity_bmi_pct_white", 39.0, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-36 White"),
        ("maternal_obesity_bmi_pct_black", 39.0, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-36 Black"),
        ("maternal_obesity_bmi_pct_all", 15.1, "percent", 2023, "Charleston County", "SC DPH VMS", VMS_PDF, "Table C-36 (438/2901 NH White births in table)"),
        ("cesarean_delivery_pct", 31.9, "percent", 2024, "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?creg=45019&top=8&stop=130", "Delivery method"),
        ("multiple_birth_pct", 3.2, "percent", 2024, "Charleston County", "March of Dimes PeriStats", f"{MOD_BASE}?creg=45019&top=7&stop=120", "Multiples"),
        # --- Hospital / occurrence ---
        ("births_occurred_in_county", 7521, "count", 2023, "Charleston County (occurrence)", "SC DPH VMS", VMS_PDF, "Table C-13/C-14"),
        ("births_in_hospital_pct_occurrence", 93.7, "percent", 2023, "Charleston occurrence", "SC DPH VMS", VMS_PDF, "Table C-14 (7049/7521)"),
        # --- County SDOH (CHR 2025) ---
        ("child_poverty_pct", 9.67, "percent", 2025, "Charleston County", "County Health Rankings", CHR, "Child poverty"),
        ("uninsured_adults_pct", 14.2, "percent", 2025, "Charleston County", "County Health Rankings", CHR, "Uninsured"),
        ("pm25_ug_m3", 8.4, "concentration", 2025, "Charleston County", "County Health Rankings", CHR, "Air quality"),
        ("severe_housing_problems_pct", 34.2, "percent", 2025, "Charleston County", "County Health Rankings", CHR, "Housing"),
        ("food_environment_index", 7.1, "index", 2025, "Charleston County", "County Health Rankings", CHR, "Food environment (higher=better)"),
        ("life_expectancy_years", 77.9, "years", 2025, "Charleston County", "County Health Rankings", CHR, "Life expectancy"),
        ("premature_death_rate_per_100k", 254.6, "rate", 2025, "Charleston County", "County Health Rankings", CHR, "YPLL"),
        # --- State benchmarks (context) ---
        ("preterm_birth_pct", 11.6, "percent", 2024, "South Carolina", "March of Dimes Report Card", MOD_REPORT, "State preterm"),
        ("infant_mortality_rate_per_1000", 7.0, "rate", 2023, "South Carolina", "March of Dimes Report Card", MOD_REPORT, "State infant mortality"),
        ("lbw_pct", 9.7, "percent", 2024, "South Carolina", "March of Dimes PeriStats", MOD_REPORT, "State LBW"),
        ("adequate_prenatal_care_pct", 79.4, "percent", 2024, "South Carolina", "March of Dimes Report Card", MOD_REPORT, "State PNC"),
        ("maternal_mortality_per_100k", 31.5, "rate", 2024, "South Carolina", "March of Dimes Report Card", MOD_REPORT, "State MM"),
        ("severe_maternal_morbidity_per_10k", 85.9, "rate", 2024, "South Carolina", "March of Dimes Report Card", MOD_REPORT, "State SMM"),
        ("low_risk_cesarean_pct", 25.6, "percent", 2024, "South Carolina", "March of Dimes Report Card", MOD_REPORT, "State C-section"),
        # --- HP2030 targets ---
        ("preterm_birth_target_pct", 9.4, "percent", 2030, "US target", "Healthy People 2030", HP2030, "MICH-07"),
        ("infant_mortality_target_per_1000", 5.0, "rate", 2030, "US target", "Healthy People 2030", HP2030, "MICH-01"),
        ("adequate_prenatal_care_target_pct", 80.5, "percent", 2030, "US target", "Healthy People 2030", HP2030, "MICH-08"),
        ("low_risk_cesarean_target_pct", 23.6, "percent", 2030, "US target", "Healthy People 2030", HP2030, "MICH-06"),

        # --- AUDIT ADDITION: Maternal mortality & morbidity review (SCMMMRC) ---
        ("pregnancy_related_mortality_rate_2023", 29.5, "rate_per_100k", 2023, "South Carolina", "SCMMMRC 2026 Legislative Brief", SCMMMRC_2026, "Lowest since surveillance began"),
        ("pregnancy_related_mortality_rate_2021", 47.2, "rate_per_100k", 2021, "South Carolina", "SCMMMRC 2025 Legislative Brief", SCMMMRC_2025, "PRMR"),
        ("pregnancy_related_mortality_nhb_2018_2023_avg", 59.6, "rate_per_100k", "2018-2023", "South Carolina", "SCMMMRC 2026 Legislative Brief", SCMMMRC_2026, "Non-Hispanic Black"),
        ("pregnancy_related_mortality_nhw_2018_2023_avg", 25.3, "rate_per_100k", "2018-2023", "South Carolina", "SCMMMRC 2026 Legislative Brief", SCMMMRC_2026, "Non-Hispanic White"),
        ("pregnancy_related_mortality_hispanic_2018_2023_avg", 24.0, "rate_per_100k", "2018-2023", "South Carolina", "SCMMMRC 2026 Legislative Brief", SCMMMRC_2026, "Hispanic"),
        ("pregnancy_related_mortality_black_white_ratio_2023", 2.0, "ratio", 2023, "South Carolina", "SCMMMRC 2026 Legislative Brief", SCMMMRC_2026, "NHB still 2x NHW in 2023"),
        ("pregnancy_related_mortality_rural_2022_2023", 48.1, "rate_per_100k", "2022-2023", "South Carolina", "SCMMMRC 2026 Legislative Brief", SCMMMRC_2026, "Rural counties"),
        ("pregnancy_related_mortality_urban_2022_2023", 28.7, "rate_per_100k", "2022-2023", "South Carolina", "SCMMMRC 2026 Legislative Brief", SCMMMRC_2026, "Urban counties"),
        ("pregnancy_related_mortality_medicaid_2023", 37.8, "rate_per_100k", 2023, "South Carolina", "SCMMMRC 2026 Legislative Brief", SCMMMRC_2026, "Medicaid payer; down from 51.0 in 2022 after 12-mo extension"),
        ("pregnancy_related_deaths_preventable_pct_2022_2023", 88.2, "percent", "2022-2023", "South Carolina", "SCMMMRC 2026 Legislative Brief", SCMMMRC_2026, "Overall preventability"),
        ("pregnancy_related_deaths_preventable_pct_nhb", 88.9, "percent", "2018-2023", "South Carolina", "SCMMMRC 2026 Legislative Brief", SCMMMRC_2026, "vs 78.6% NHW"),
        ("pregnancy_related_deaths_mh_sud_preventable_pct", 100.0, "percent", "2022-2023", "South Carolina", "SCMMMRC 2026 Legislative Brief", SCMMMRC_2026, "Mental health/SUD, hypertension, hemorrhage all 100% preventable"),
        ("sc_national_maternal_mortality_rank", 8, "rank", 2023, "South Carolina", "SC DPH Pregnancy & Postpartum Health page", "https://dph.sc.gov/health-wellness/family-planning/pregnancy/pregnancy-and-postpartum-health", "8th highest in US"),

        # --- AUDIT ADDITION: Maternity care deserts & OB unit closures ---
        ("maternity_care_desert_pct_counties", 13.0, "percent", 2024, "South Carolina", "March of Dimes Maternity Care Deserts Report", MOD_MCD_SC, "13.0% of SC counties vs 32.6% US"),
        ("counties_no_birth_hospital_pct", 45.7, "percent", 2024, "South Carolina", "March of Dimes Maternity Care Deserts Report", MOD_MCD_SC, "No hospital/birth center offering maternity care"),
        ("births_in_maternity_care_deserts_pct", 2.6, "percent", 2022, "South Carolina", "March of Dimes Maternity Care Deserts Report", MOD_MCD_SC, "1,493 babies born in deserts"),
        ("no_birthing_hospital_30min_pct", 8.7, "percent", 2022, "South Carolina", "March of Dimes Maternity Care Deserts Report", MOD_MCD_SC, "vs 9.7% US"),
        ("rural_over_30min_to_birthing_hospital_pct", 100.0, "percent", 2022, "South Carolina rural", "March of Dimes Maternity Care Deserts Report", MOD_MCD_SC, "vs 8.5% urban"),
        ("avg_distance_to_birthing_hospital_miles", 9.7, "miles", 2022, "South Carolina", "March of Dimes Maternity Care Deserts Report", MOD_MCD_SC, "urban avg; rural avg 25.2 mi"),
        ("inadequate_pnc_pct_mcd_report", 16.7, "percent", 2021, "South Carolina", "March of Dimes Maternity Care Deserts Report", MOD_MCD_SC, "vs 14.8% US"),
        ("chronic_health_burden_pct", 44.5, "percent", 2021, "South Carolina", "March of Dimes Maternity Care Deserts Report", MOD_MCD_SC, "1+ chronic condition, vs 37.8% US"),
        ("chronic_condition_preterm_relative_risk_increase_pct", 54.0, "percent", 2021, "South Carolina", "March of Dimes Maternity Care Deserts Report", MOD_MCD_SC, "Increased PTB likelihood with 1+ chronic condition"),
        ("ob_units_closed_since_2011", 11, "count", 2020, "South Carolina", "SC Birth Outcomes Initiative Annual Report", SCBOI_2022, "Only 4 new units opened in same period"),
        ("birthing_hospitals_2011", 47, "count", 2011, "South Carolina", "SC Birth Outcomes Initiative Annual Report", SCBOI_2022, "Start of SCBOI"),
        ("birthing_hospitals_2020", 38, "count", 2020, "South Carolina", "SC Birth Outcomes Initiative Annual Report", SCBOI_2022, "9-hospital net decline in 9 years"),
        ("labor_delivery_units_closed_since_2012", 13, "count", 2024, "South Carolina", "USC IMPH MCH Data Snapshot", USC_IMPH_SNAPSHOT, "1 in 4 hospitals no longer a birthing facility"),
        ("rural_hospitals_lost_ob_pct_2010_2022", 46.2, "percent", 2022, "South Carolina", "Fierce Healthcare / peer-reviewed OB closures study", FIERCE_HEALTHCARE_OB, "Tied with PA for among worst in US"),
        ("roper_st_francis_mt_pleasant_ob_closed", "December 2020", "event", 2020, "Charleston County (Mount Pleasant)", "SC Birth Outcomes Initiative Annual Report", SCBOI_2022, "OB closure within Charleston metro area"),
        ("georgetown_memorial_ob_closed", "September 2020", "event", 2020, "Georgetown County", "SC Birth Outcomes Initiative Annual Report", SCBOI_2022, "Adjacent Lowcountry county"),
        ("laurens_county_ob_closed", "May 2023", "event", 2023, "Laurens County", "Post and Courier / Prisma Health", POST_COURIER_LAURENS, "Staffing shortage; patients now travel ~1hr to Greenville"),
        ("kershaw_medical_center_ob_closed", "January 2025", "event", 2025, "Kershaw County", "Post and Courier / MUSC", POST_COURIER_LAURENS, "MUSC redirecting to MUSC Northeast, 35 min away"),
        ("high_need_mvi_tertile_counties", "Abbeville, Allendale, Barnwell, Greenwood, Laurens, Lee, McCormick, Williamsburg", "list", 2024, "South Carolina", "USC Institute for Families in Society MCH Data Snapshot", USC_IMPH_SNAPSHOT, "Lowest tertile = highest need"),
        ("sc_maternal_vulnerability_index_rank", "Top 5 nationally", "rank", 2024, "South Carolina", "USC IMPH MCH Data Snapshot / Surgo Maternal Vulnerability Index", USC_IMPH_SNAPSHOT, "Driven by high physical health and SES needs"),

        # --- AUDIT ADDITION: Neonatal abstinence syndrome (NAS) / substance exposure ---
        ("nas_rate_sc_2017_2019", 5.1, "rate_per_1000", "2017-2019", "South Carolina", "HRSA Title V Information System (TVIS)", HRSA_TVIS_NAS, "Up 21.4% from 4.2 in 2014-2016"),
        ("nas_rate_sc_2014_2016", 4.2, "rate_per_1000", "2014-2016", "South Carolina", "HRSA Title V Information System (TVIS)", HRSA_TVIS_NAS, "Baseline period"),
        ("nas_rate_medicaid_2019", 8.2, "rate_per_1000", 2019, "South Carolina", "HRSA Title V Information System (TVIS)", HRSA_TVIS_NAS, "5.5x the private-insurance rate"),
        ("nas_rate_private_insurance_2019", 1.5, "rate_per_1000", 2019, "South Carolina", "HRSA Title V Information System (TVIS)", HRSA_TVIS_NAS, "Comparator"),
        ("nas_rate_horry_county", 8.0, "rate_per_1000", "3-yr trailing", "Horry County", "Pediatrix/MEDNAX news report", PEDIATRIX_HORRY_NAS, "Highest in SC for 3 consecutive years"),
        ("nas_rate_greenville_2000_2014", 8.22, "rate_per_1000", "2000-2014", "Greenville County", "MAiN model study (ScienceDirect)", MAIN_SCIENCEDIRECT_NAS, "2nd highest incidence in SC in period studied"),
        ("nas_region_us_rank", 3, "rank", 2018, "South Atlantic region (incl. SC)", "MAiN model study (ScienceDirect)", MAIN_SCIENCEDIRECT_NAS, "3rd highest NAS rate of US Census regions"),

        # --- AUDIT ADDITION: Breastfeeding ---
        ("breastfeeding_ever_pct_sc", 80.6, "percent", 2022, "South Carolina", "CDC Breastfeeding Report Card 2022", CDC_BF_REPORT_CARD_2022, "Ever breastfed, last CDC report card published"),
        ("breastfeeding_any_6mo_pct_sc", 46.6, "percent", 2022, "South Carolina", "CDC Breastfeeding Report Card 2022", CDC_BF_REPORT_CARD_2022, "Any breastfeeding at 6 months"),
        ("breastfeeding_exclusive_6mo_pct_sc", 26.0, "percent", 2022, "South Carolina", "CDC Breastfeeding Report Card 2022", CDC_BF_REPORT_CARD_2022, "Exclusive breastfeeding at 6 months"),
        ("wic_breastfeeding_rate_sc_2024", 30.0, "percent", 2024, "South Carolina (WIC)", "SC DPH WIC Breastfeeding Rates Fact Sheet", SC_WIC_BF_FACTSHEET, "Highest recorded in recent years, Aug 2024"),
        ("wic_breastfeeding_rate_black_infants", 23.6, "percent", 2024, "South Carolina (WIC)", "SC DPH WIC Breastfeeding Rates Fact Sheet", SC_WIC_BF_FACTSHEET, "Lowest of racial groups in WIC program"),
        ("wic_breastfeeding_rate_asian_infants", 42.6, "percent", 2024, "South Carolina (WIC)", "SC DPH WIC Breastfeeding Rates Fact Sheet", SC_WIC_BF_FACTSHEET, "Highest of racial groups in WIC program"),

        # --- AUDIT ADDITION: Doula policy timeline ---
        ("doula_medicaid_pilot_start", "September 2024", "event", 2024, "South Carolina", "SC Healthy Connections Medicaid / Black Health SC", BLACKHEALTH_SC_DOULA, "24-month pilot under H.3592 (2023); Upstate/Midlands/Lowcountry regions"),
        ("doula_medicaid_pilot_reimbursement_per_package", 1000, "dollars", 2024, "South Carolina", "SC Healthy Connections Medicaid / Black Health SC", BLACKHEALTH_SC_DOULA, "Up to $1,000 per full perinatal package"),
        ("doula_mandate_effective_date", "January 1, 2026", "event", 2026, "South Carolina", "SC Bill 3108 / Bill 42 (2025-2026 session)", SC_H3108_DOULA_BILL, "Mandatory Medicaid + private insurance coverage"),
        ("doula_mandate_minimum_reimbursement", 850, "dollars", 2026, "South Carolina", "SC Bill 3108 (2025-2026 session)", SC_H3108_DOULA_BILL, "Minimum reimbursement per pregnancy, antepartum through 12mo postpartum"),

        # --- AUDIT ADDITION: Group prenatal care evidence (mixed / evolving evidence base) ---
        ("cradle_rct_ptb_group_care_pct", 10.4, "percent", "2016-2021", "South Carolina (CRADLE RCT, Upstate)", "CRADLE Trial (Clemson Univ./Prisma Health), PMC9729420", CRADLE_TRIAL_PMC, "n=1176; NOT significantly different from individual care"),
        ("cradle_rct_ptb_individual_care_pct", 8.7, "percent", "2016-2021", "South Carolina (CRADLE RCT, Upstate)", "CRADLE Trial (Clemson Univ./Prisma Health), PMC9729420", CRADLE_TRIAL_PMC, "n=1174; OR 1.22, 95% CI 0.92-1.63, p=0.17"),
        ("cradle_rct_lbw_black_high_attendance_pct", 8.3, "percent", "2016-2021", "South Carolina (CRADLE RCT, Upstate)", "CRADLE Trial, PMC9729420", CRADLE_TRIAL_PMC, "Per-compliance analysis; benefit only at high attendance"),
        ("picklesimer_2012_ptb_group_pct", 9.8, "percent", "2009-2010", "Greenville County (retrospective cohort)", "Picklesimer et al. 2012, AJOG", PICKLESIMER_2012_AJOG, "33% relative reduction vs traditional care (14.8%)"),
        ("picklesimer_2012_ptb_traditional_pct", 14.8, "percent", "2009-2010", "Greenville County (retrospective cohort)", "Picklesimer et al. 2012, AJOG", PICKLESIMER_2012_AJOG, "Comparator, Medicaid-covered patients"),
        ("gareau_2016_ptb_relative_risk_reduction_pct", 36.0, "percent", "2010-2014", "South Carolina (5-yr Medicaid cohort)", "Gareau et al. 2016, Matern Child Health J / Centering Healthcare Institute", GAREAU_2016_CENTERING, "$22,667 average savings per prevented preterm birth"),
        ("robinson_2018_ptb_risk_ratio", 0.38, "risk_ratio", "2009-2014", "South Carolina (single institution cohort)", "Robinson et al. 2018, J Womens Health", ROBINSON_2018_JWH, "95% CI 0.31-0.47; largest effect among NH White mothers"),
    ]
    cols = [
        "indicator",
        "value",
        "unit",
        "year",
        "geography",
        "source_name",
        "source_url",
        "table_or_page",
    ]
    df = pd.DataFrame(rows, columns=cols)
    out = os.path.join(DATA_DIR, "county_neonatal_indicators.csv")
    df.to_csv(out, index=False)
    print(f"Indicators: {len(df)} rows -> {out}")
    return df


def build_state_benchmarks(indicators_df):
    sc = indicators_df[indicators_df["geography"] == "South Carolina"].copy()
    ch = indicators_df[indicators_df["geography"] == "Charleston County"].copy()
    merged = ch.merge(
        sc,
        on="indicator",
        how="inner",
        suffixes=("_charleston", "_sc"),
    )
    merged["charleston_vs_sc"] = merged.apply(
        lambda r: (
            round(r["value_charleston"] - r["value_sc"], 2)
            if r["unit_charleston"] in ("percent", "rate", "ratio")
            else None
        ),
        axis=1,
    )
    out = os.path.join(DATA_DIR, "sc_state_benchmarks.csv")
    merged.to_csv(out, index=False)
    print(f"Benchmarks: {len(merged)} paired indicators -> {out}")


def build_factor_matrix():
    """Links each neonatal health factor domain to indicators and evidence strength."""
    factors = [
        ("clinical_outcomes", "preterm_birth_pct", "direct", "March of Dimes + VMS", MOD_CHARLESTON),
        ("clinical_outcomes", "low_birthweight_pct", "direct", "SC DPH VMS Table C-27", VMS_PDF),
        ("clinical_outcomes", "infant_mortality_rate_per_1000", "direct", "SC DPH VMS Table F-3", VMS_PDF),
        ("clinical_outcomes", "neonatal_mortality_rate_per_1000", "direct", "SC DPH VMS Table F-4", VMS_PDF),
        ("racial_equity", "lbw_pct_black", "direct", "SC DPH VMS Table C-27", VMS_PDF),
        ("racial_equity", "infant_mortality_black_per_1000", "direct", "March of Dimes PeriStats", MOD_CHARLESTON),
        ("racial_equity", "medicaid_births_pct_black", "direct", "SC DPH VMS Table C-35A", VMS_PDF),
        ("prenatal_access", "prenatal_care_inadequate_pct", "direct", "March of Dimes PeriStats", MOD_CHARLESTON),
        ("prenatal_access", "kotelchuck_inadequate_pct_black", "direct", "SC DPH VMS Table C-11A", VMS_PDF),
        ("insurance_financing", "medicaid_births_pct_all", "direct", "SC DPH VMS Table C-35", VMS_PDF),
        ("insurance_financing", "self_pay_births_pct", "direct", "SC DPH VMS Table C-35", VMS_PDF),
        ("nutrition_wic", "wic_during_pregnancy_pct", "direct", "SC DPH VMS Table C-34", VMS_PDF),
        ("maternal_nutrition", "maternal_obesity_bmi_pct_black", "direct", "SC DPH VMS Table C-36", VMS_PDF),
        ("social_support", "unmarried_births_pct_black", "proxy", "SC DPH VMS Table C-21", VMS_PDF),
        ("adolescent_health", "teen_births_under_20_pct", "direct", "SC DPH VMS Table C-19", VMS_PDF),
        ("delivery_care", "cesarean_delivery_pct", "direct", "March of Dimes PeriStats", MOD_CHARLESTON),
        ("hospital_capacity", "births_occurred_in_county", "context", "SC DPH VMS Table C-14", VMS_PDF),
        ("nicu_access", "level_iv_nicu", "qualitative", "MUSC Children's Health", MUSC_NICU),
        ("environment", "pm25_ug_m3", "proxy", "County Health Rankings", CHR),
        ("housing", "severe_housing_problems_pct", "proxy", "County Health Rankings", CHR),
        ("food_access", "food_environment_index", "proxy", "County Health Rankings", CHR),
        ("insurance_community", "uninsured_adults_pct", "proxy", "County Health Rankings", CHR),
        ("poverty", "child_poverty_pct", "proxy", "County Health Rankings", CHR),
        ("tract_svi", "RPL_THEMES", "proxy", "CDC/ATSDR SVI 2022", "https://www.atsdr.cdc.gov/placeandhealth/svi/index.html"),
        ("tract_food_insecurity", "food_insecurity_pct", "proxy", "CDC PLACES 2025", "https://data.cdc.gov/PLACES"),
        ("tract_transport", "transportation_barrier_pct", "proxy", "CDC PLACES 2025", "https://data.cdc.gov/PLACES"),
        ("state_maternal_safety", "maternal_mortality_per_100k", "context", "March of Dimes Report Card", MOD_REPORT),
        ("state_maternal_safety", "severe_maternal_morbidity_per_10k", "context", "March of Dimes Report Card", MOD_REPORT),
        ("maternal_mortality_review", "pregnancy_related_mortality_rate_2023", "direct", "SCMMMRC 2026 Legislative Brief", SCMMMRC_2026),
        ("maternal_mortality_review", "pregnancy_related_deaths_preventable_pct_2022_2023", "direct", "SCMMMRC 2026 Legislative Brief", SCMMMRC_2026),
        ("maternal_mortality_equity", "pregnancy_related_mortality_black_white_ratio_2023", "direct", "SCMMMRC 2026 Legislative Brief", SCMMMRC_2026),
        ("maternal_mortality_rurality", "pregnancy_related_mortality_rural_2022_2023", "direct", "SCMMMRC 2026 Legislative Brief", SCMMMRC_2026),
        ("maternity_care_access", "maternity_care_desert_pct_counties", "direct", "March of Dimes Maternity Care Deserts SC", MOD_MCD_SC),
        ("maternity_care_access", "ob_units_closed_since_2011", "direct", "SC Birth Outcomes Initiative Annual Report", SCBOI_2022),
        ("maternity_care_access", "rural_hospitals_lost_ob_pct_2010_2022", "direct", "Fierce Healthcare / peer-reviewed study", FIERCE_HEALTHCARE_OB),
        ("maternity_care_access_charleston", "roper_st_francis_mt_pleasant_ob_closed", "qualitative", "SC Birth Outcomes Initiative Annual Report", SCBOI_2022),
        ("substance_exposed_newborns", "nas_rate_sc_2017_2019", "direct", "HRSA TVIS", HRSA_TVIS_NAS),
        ("substance_exposed_newborns", "nas_rate_medicaid_2019", "direct", "HRSA TVIS", HRSA_TVIS_NAS),
        ("breastfeeding", "breastfeeding_ever_pct_sc", "direct", "CDC Breastfeeding Report Card 2022", CDC_BF_REPORT_CARD_2022),
        ("breastfeeding_equity", "wic_breastfeeding_rate_black_infants", "direct", "SC DPH WIC Breastfeeding Fact Sheet", SC_WIC_BF_FACTSHEET),
        ("doula_policy", "doula_medicaid_pilot_start", "qualitative", "SC Healthy Connections Medicaid", BLACKHEALTH_SC_DOULA),
        ("doula_policy", "doula_mandate_effective_date", "qualitative", "SC Bill 3108", SC_H3108_DOULA_BILL),
        ("group_prenatal_care_evidence", "cradle_rct_ptb_group_care_pct", "direct_rct", "CRADLE Trial, PMC9729420", CRADLE_TRIAL_PMC),
        ("group_prenatal_care_evidence", "picklesimer_2012_ptb_group_pct", "direct_cohort", "Picklesimer et al. 2012 AJOG", PICKLESIMER_2012_AJOG),
        ("group_prenatal_care_evidence", "gareau_2016_ptb_relative_risk_reduction_pct", "direct_cohort", "Gareau et al. 2016 MCHJ", GAREAU_2016_CENTERING),
    ]
    df = pd.DataFrame(
        factors,
        columns=[
            "factor_domain",
            "indicator_key",
            "evidence_type",
            "primary_source",
            "source_url",
        ],
    )
    out = os.path.join(DATA_DIR, "factor_evidence_matrix.csv")
    df.to_csv(out, index=False)
    print(f"Factor matrix: {len(df)} rows -> {out}")


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    fetch_places_tracts()
    fetch_svi_tracts()
    fetch_tract_boundaries()
    ind = build_county_indicators()
    build_state_benchmarks(ind)
    build_factor_matrix()


if __name__ == "__main__":
    main()
