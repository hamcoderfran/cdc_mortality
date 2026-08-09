"""
Charleston County deep-dive, step 1: Download tract-level datasets
===================================================================

Pulls census-tract data for Charleston County, SC (FIPS 45019) from:

  1. CDC PLACES 2025 census tract release (data.cdc.gov, cwsq-ngmh)
     — 40 health outcome, behavior, disability, and social-need measures

  2. CDC/ATSDR Social Vulnerability Index 2022 (ArcGIS FeatureServer)
     — overall SVI percentile + four theme rankings

  3. U.S. Census TIGER/Line 2022 tract boundaries (ArcGIS REST → GeoJSON)
     — polygon geometry for choropleth mapping

  4. County-level benchmarks from parent project merged table (45019, SC, US)

Outputs:
  ../data/places_tracts_long.csv
  ../data/svi_tracts.csv
  ../data/tract_boundaries.geojson
  ../data/county_benchmarks.csv
"""

import json
import os

import pandas as pd
import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PARENT_DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")

COUNTY_FIPS = "45019"
STATE_FIPS = "45"
COUNTY_CODE = "019"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; CharlestonCountyAnalysis/1.0)"}

PLACES_URL = "https://data.cdc.gov/resource/cwsq-ngmh.json"
SVI_URL = (
    "https://onemap.cdc.gov/onemapservices/rest/services/SVI/"
    "CDC_ATSDR_Social_Vulnerability_Index_2022_USA/FeatureServer/2/query"
)
TIGER_URL = (
    "https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/"
    "tigerWMS_ACS2022/MapServer/6/query"
)


def fetch_places_tracts():
    rows = []
    offset = 0
    page = 5000
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
    print(f"PLACES: {len(df)} rows, {df['measureid'].nunique()} measures -> {out}")
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
    features = r.json()["features"]
    rows = [f["attributes"] for f in features]
    df = pd.DataFrame(rows)
    df = df.rename(columns={"FIPS": "tract_fips"})
    df["tract_fips"] = df["tract_fips"].astype(str).str.zfill(11)
    for col in df.columns:
        if col != "tract_fips":
            df[col] = pd.to_numeric(df[col], errors="coerce")
    out = os.path.join(DATA_DIR, "svi_tracts.csv")
    df.to_csv(out, index=False)
    print(f"SVI: {len(df)} tracts -> {out}")
    return df


def fetch_tract_boundaries():
    """Paginate Census TIGER REST API (max 1000 features per request)."""
    all_features = []
    offset = 0
    page = 1000
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
        geo = r.json()
        batch = geo.get("features", [])
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
    return geojson


def fetch_county_benchmarks():
    merged = pd.read_csv(
        os.path.join(PARENT_DATA, "merged_county_data.csv"), dtype={"fips": str}
    )
    cc = merged[merged["fips"] == COUNTY_FIPS].iloc[0]
    sc = merged[merged["state"] == "SC"]
    us = merged

    metrics = [
        "drug_overdose_death_rate",
        "heart_disease_death_rate",
        "stroke_death_rate",
        "diabetes_prevalence_pct",
        "lung_cancer_death_rate",
        "suicide_death_rate",
        "life_expectancy",
        "premature_death_rate",
        "median_household_income",
        "child_poverty_pct",
        "uninsured_pct",
        "pm25",
        "severe_housing_problems_pct",
        "food_environment_index",
    ]

    rows = []
    for m in metrics:
        rows.append(
            {
                "metric": m,
                "charleston": cc[m],
                "sc_median": sc[m].median(),
                "us_median": us[m].median(),
            }
        )
    df = pd.DataFrame(rows)
    out = os.path.join(DATA_DIR, "county_benchmarks.csv")
    df.to_csv(out, index=False)
    print(f"Benchmarks: {len(df)} metrics -> {out}")
    return df


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    fetch_places_tracts()
    fetch_svi_tracts()
    fetch_tract_boundaries()
    fetch_county_benchmarks()


if __name__ == "__main__":
    main()
