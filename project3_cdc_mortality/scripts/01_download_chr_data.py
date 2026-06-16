"""
Project 3, step 1: Download County Health Rankings & Roadmaps data
=====================================================================

County Health Rankings (CHR, www.countyhealthrankings.org -- a collaboration
between the Robert Wood Johnson Foundation and the University of Wisconsin
Population Health Institute) publishes a single annual CSV with ~800 columns
of county-level health, socioeconomic, environmental and healthcare-access
measures for every US county.

This script downloads the 2025 national analytic data file (public CSV, no
authentication) and extracts the subset of columns used by this project:

  Mortality / outcome measures:
    - Drug Overdose Deaths (age-adjusted rate per 100,000)
    - Suicides (age-adjusted rate per 100,000)

  Socioeconomic measures:
    - Median Household Income
    - Income Inequality (ratio of household income at 80th vs 20th pctile)
    - Unemployment (%)
    - Children in Poverty (%)
    - High School Completion (%)
    - Broadband Access (%)

  Healthcare access measures:
    - Uninsured adults (%)
    - Primary Care Physicians (ratio of population per PCP)
    - Mental Health Providers (ratio of population per provider)

  Pollution / environment measures:
    - Air Pollution: Particulate Matter (avg daily PM2.5, ug/m3)
    - Drinking Water Violations (Y/N)
    - Severe Housing Problems (%)

  Other:
    - Food Environment Index
    - Long Commute - Driving Alone (%)

Output: ../data/chr_subset.csv  (one row per county, key columns only,
indexed by 5-digit FIPS)
"""

import os

import pandas as pd
import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CHR_URL = "https://www.countyhealthrankings.org/sites/default/files/media/document/analytic_data2025_v3.csv"
RAW_PATH = os.path.join(DATA_DIR, "chr_analytic_data2025.csv")

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}

COLUMN_MAP = {
    "5-digit FIPS Code": "fips",
    "State Abbreviation": "state",
    "Name": "county_name",
    "Drug Overdose Deaths raw value": "drug_overdose_death_rate",
    "Suicides raw value": "suicide_death_rate",
    "Median Household Income raw value": "median_household_income",
    "Income Inequality raw value": "income_inequality_ratio",
    "Unemployment raw value": "unemployment_pct",
    "Children in Poverty raw value": "child_poverty_pct",
    "High School Completion raw value": "hs_completion_pct",
    "Broadband Access raw value": "broadband_access_pct",
    "Uninsured raw value": "uninsured_pct",
    "Primary Care Physicians raw value": "pop_per_pcp",
    "Mental Health Providers raw value": "pop_per_mental_health_provider",
    "Air Pollution: Particulate Matter raw value": "pm25",
    "Drinking Water Violations raw value": "drinking_water_violation",
    "Severe Housing Problems raw value": "severe_housing_problems_pct",
    "Food Environment Index raw value": "food_environment_index",
    "Long Commute - Driving Alone raw value": "long_commute_pct",
    "Premature Death raw value": "premature_death_rate",
    "Life Expectancy raw value": "life_expectancy",
}


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(RAW_PATH):
        print(f"Downloading {CHR_URL} ...")
        r = requests.get(CHR_URL, headers=HEADERS, timeout=120)
        r.raise_for_status()
        assert r.headers.get("Content-Type", "").startswith(
            ("application/octet-stream", "text/csv", "text/plain")
        ), f"Unexpected content type: {r.headers.get('Content-Type')}"
        with open(RAW_PATH, "wb") as f:
            f.write(r.content)
        print(f"  saved {len(r.content)/1e6:.1f} MB -> {RAW_PATH}")
    else:
        print(f"Using cached {RAW_PATH}")

    # First data row is the national summary row; second row of the file is
    # a units/description row that we skip.
    df = pd.read_csv(RAW_PATH, header=0, skiprows=[1], low_memory=False)
    missing = [c for c in COLUMN_MAP if c not in df.columns]
    if missing:
        raise RuntimeError(f"Expected CHR columns not found: {missing}")

    sub = df[list(COLUMN_MAP.keys())].rename(columns=COLUMN_MAP)
    sub["fips"] = sub["fips"].astype(str).str.zfill(5)
    # Drop the US-wide summary row (fips == "00000") and state-level summary
    # rows (county FIPS == "000")
    sub = sub[~sub["fips"].str.endswith("000")]
    sub = sub.dropna(subset=["drug_overdose_death_rate"], how="all")

    out_path = os.path.join(DATA_DIR, "chr_subset.csv")
    sub.to_csv(out_path, index=False)
    print(f"Wrote {len(sub)} counties -> {out_path}")


if __name__ == "__main__":
    main()
