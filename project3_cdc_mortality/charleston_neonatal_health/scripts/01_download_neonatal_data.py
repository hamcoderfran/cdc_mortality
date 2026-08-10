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
