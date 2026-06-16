"""
Project 3, step 3: Download county-level lung cancer mortality data
=======================================================================

Source: NCI/CDC State Cancer Profiles (statecancerprofiles.cancer.gov),
the official NCI tool for cancer statistics. It exposes a CSV export of its
death-rate report covering every US county.

We pull the "Lung & Bronchus" age-adjusted death rate (deaths per 100,000,
2019-2023, all races, both sexes, all ages) for every county.

Output: ../data/lung_cancer_mortality.csv
  columns: fips, lung_cancer_death_rate, lung_cancer_avg_annual_count
"""

import io
import os

import pandas as pd
import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}

URL = "https://statecancerprofiles.cancer.gov/deathrates/index.php"
PARAMS = {
    "statefips": "00",
    "areatype": "county",
    "cancer": "047",  # Lung & Bronchus
    "race": "00",  # All Races (includes Hispanic)
    "sex": "0",  # Both sexes
    "age": "001",  # All ages
    "year": "0",  # latest 5-year average (2019-2023)
    "type": "death",
    "sortVariableName": "rate",
    "sortOrder": "desc",
    "output": "1",
}


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    r = requests.get(URL, params=PARAMS, headers=HEADERS, timeout=120)
    r.raise_for_status()
    assert r.headers.get("Content-Type", "").startswith("text/csv"), (
        f"Unexpected content type from State Cancer Profiles: {r.headers.get('Content-Type')}"
    )

    # The file has 2 title lines, a blank line, then a header row.
    text = r.content.decode("iso-8859-1")
    lines = text.splitlines()
    header_idx = next(i for i, l in enumerate(lines) if l.startswith("County,FIPS"))
    csv_text = "\n".join(lines[header_idx:])
    df = pd.read_csv(io.StringIO(csv_text))

    df["FIPS"] = pd.to_numeric(df["FIPS"], errors="coerce")
    df = df.dropna(subset=["FIPS"])
    df = df[df["FIPS"] != 0]
    df = df.rename(
        columns={
            "FIPS": "fips",
            "Age-Adjusted Death Rate([rate note]) - deaths per 100,000": "lung_cancer_death_rate",
            "Average Annual Count": "lung_cancer_avg_annual_count",
        }
    )
    df["fips"] = df["fips"].astype(int).astype(str).str.zfill(5)
    df["lung_cancer_death_rate"] = pd.to_numeric(
        df["lung_cancer_death_rate"].astype(str).str.strip(), errors="coerce"
    )

    out = df[["fips", "lung_cancer_death_rate", "lung_cancer_avg_annual_count"]]
    out_path = os.path.join(DATA_DIR, "lung_cancer_mortality.csv")
    out.to_csv(out_path, index=False)
    print(f"Wrote {len(out)} counties -> {out_path}")
    print(out.describe())


if __name__ == "__main__":
    main()
