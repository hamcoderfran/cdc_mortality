"""
Project 3, step 2: Download county-level cause-specific mortality data
=========================================================================

Pulls three additional county-level outcome datasets directly from the
official CDC open-data portal (data.cdc.gov, Socrata API, JSON, no
authentication):

  1. Heart Disease Mortality Data Among US Adults (35+) by County, 2018-2020
     dataset id: jiwm-ppbh   (source: NVSS / CDC Division for Heart Disease
     and Stroke Prevention, Interactive Atlas of Heart Disease and Stroke)

  2. Stroke Mortality Data Among US Adults (35+) by County, 2019-2021
     dataset id: vutr-sfkh   (same source/program)

  3. PLACES: County Data (GIS Friendly Format), 2025 release
     dataset id: i46a-9kgh   (source: CDC PLACES project, model-based
     small-area estimates from BRFSS) -- used here for county-level
     diagnosed-diabetes prevalence, since cause-specific diabetes
     *mortality* is not available at county resolution through any public
     API (small-number suppression).

For (1) and (2) we request only the "Overall" (both sexes, all
races/ethnicities) county-level rows.

Output: ../data/cdc_heart_stroke_diabetes.csv
  columns: fips, heart_disease_death_rate, stroke_death_rate, diabetes_prevalence_pct
"""

import os

import pandas as pd
import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
BASE = "https://data.cdc.gov/resource"


def fetch_all(resource_id, params, page_size=5000):
    rows = []
    offset = 0
    while True:
        p = dict(params)
        p["$limit"] = page_size
        p["$offset"] = offset
        r = requests.get(f"{BASE}/{resource_id}.json", params=p, headers=HEADERS, timeout=60)
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        rows.extend(batch)
        offset += page_size
        if len(batch) < page_size:
            break
    return rows


def heart_or_stroke(resource_id, value_col_name):
    rows = fetch_all(
        resource_id,
        {
            "$select": "locationid,data_value,data_value_type",
            "$where": (
                "geographiclevel='County' AND stratificationcategory1='Sex' AND stratification1='Overall' "
                "AND stratificationcategory2='Race/Ethnicity' AND stratification2='Overall'"
            ),
        },
    )
    df = pd.DataFrame(rows)
    df = df.rename(columns={"locationid": "fips", "data_value": value_col_name})
    df["fips"] = df["fips"].astype(str).str.zfill(5)
    df[value_col_name] = pd.to_numeric(df[value_col_name], errors="coerce")
    return df[["fips", value_col_name]]


def diabetes_prevalence():
    rows = fetch_all(
        "i46a-9kgh",
        {"$select": "countyfips,diabetes_adjprev"},
    )
    df = pd.DataFrame(rows)
    df = df.rename(columns={"countyfips": "fips", "diabetes_adjprev": "diabetes_prevalence_pct"})
    df["fips"] = df["fips"].astype(str).str.zfill(5)
    df["diabetes_prevalence_pct"] = pd.to_numeric(df["diabetes_prevalence_pct"], errors="coerce")
    return df


def main():
    print("Downloading heart disease mortality (jiwm-ppbh)...")
    heart = heart_or_stroke("jiwm-ppbh", "heart_disease_death_rate")
    print(f"  {len(heart)} counties")

    print("Downloading stroke mortality (vutr-sfkh)...")
    stroke = heart_or_stroke("vutr-sfkh", "stroke_death_rate")
    print(f"  {len(stroke)} counties")

    print("Downloading diabetes prevalence (i46a-9kgh, PLACES)...")
    diabetes = diabetes_prevalence()
    print(f"  {len(diabetes)} counties")

    merged = heart.merge(stroke, on="fips", how="outer").merge(diabetes, on="fips", how="outer")
    out_path = os.path.join(DATA_DIR, "cdc_heart_stroke_diabetes.csv")
    merged.to_csv(out_path, index=False)
    print(f"Wrote {len(merged)} counties -> {out_path}")


if __name__ == "__main__":
    main()
