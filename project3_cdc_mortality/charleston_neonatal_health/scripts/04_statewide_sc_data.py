"""
Greater South Carolina neonatal health — step 4: build 46-county dataset
=========================================================================

Transcribes SC DPH Vital Metrics Summary 2023 county tables (infant mortality,
low birthweight) for ALL 46 South Carolina counties, plus March of Dimes
maternity-care-access classifications and County Health Rankings SDOH
covariates. This is the "greater South Carolina" companion to the Charleston-
only indicator file, used for statewide correlation/regression analysis.

Primary sources (every value traceable):
  - SC DPH Vital Metrics Summary 2023 (VMS), Tables F-3 (infant mortality) and
    C-27 (low birthweight), https://dph.sc.gov/sites/scdph/files/2025-11/VMS-2023.pdf
  - County Health Rankings & Roadmaps 2025 (uninsured, poverty, PM2.5, housing,
    food environment, median income) — reused from ../../data/merged_county_data.csv
  - March of Dimes "Where You Live Matters: Maternity Care Deserts in South
    Carolina" (2023) and "Nowhere to Go" (2024) reports
  - USC Institute for Families in Society / SC Birth Outcomes Initiative (SCBOI)
    annual reports — high-need county tertiles, OB unit closures

Outputs:
  ../data/sc_county_infant_mortality.csv
  ../data/sc_county_low_birthweight.csv
  ../data/sc_county_maternity_access.csv
  ../data/sc_statewide_merged.csv
"""

import os

import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
PARENT_DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")
VMS_PDF = "https://dph.sc.gov/sites/scdph/files/2025-11/VMS-2023.pdf"

# Table F-3: Infant Mortality and Infant Mortality Rates, SC DPH VMS 2023, p.100
# columns: county, deaths_2023, imr_2023, deaths_2021_2023, imr_2021_2023, deaths_2018_2020, imr_2018_2020
IMR_ROWS = [
    ("South Carolina", 194, 5.4, 554, 5.0, 499, 4.5),
    ("Abbeville", 0, 0.0, 2, 4.0, 0, 0.0),
    ("Aiken", 8, 6.5, 17, 4.5, 16, 4.3),
    ("Allendale", 0, 0.0, 0, 0.0, 0, 0.0),
    ("Anderson", 10, 5.6, 29, 5.3, 24, 4.6),
    ("Bamberg", 0, 0.0, 0, 0.0, 0, 0.0),
    ("Barnwell", 0, 0.0, 2, 5.0, 1, 2.5),
    ("Beaufort", 8, 6.2, 18, 4.6, 11, 2.6),
    ("Berkeley", 6, 3.1, 24, 4.1, 19, 3.2),
    ("Calhoun", 0, 0.0, 0, 0.0, 2, 9.8),
    ("Charleston", 14, 4.3, 53, 5.2, 33, 3.3),
    ("Cherokee", 2, 4.6, 6, 4.4, 11, 7.8),
    ("Chester", 1, 5.1, 6, 10.7, 6, 10.2),
    ("Chesterfield", 0, 0.0, 5, 5.5, 7, 8.0),
    ("Clarendon", 0, 0.0, 3, 7.0, 1, 2.5),
    ("Colleton", 1, 3.9, 6, 7.7, 6, 7.6),
    ("Darlington", 1, 2.8, 4, 3.6, 9, 8.0),
    ("Dillon", 2, 13.5, 5, 10.5, 3, 5.9),
    ("Dorchester", 4, 3.3, 12, 3.2, 14, 3.8),
    ("Edgefield", 0, 0.0, 1, 2.8, 0, 0.0),
    ("Fairfield", 0, 0.0, 0, 0.0, 3, 14.6),
    ("Florence", 4, 5.7, 14, 6.3, 20, 8.9),
    ("Georgetown", 5, 16.6, 8, 9.0, 7, 7.7),
    ("Greenville", 23, 5.4, 66, 4.8, 51, 3.6),
    ("Greenwood", 3, 7.7, 5, 4.0, 6, 4.2),
    ("Hampton", 0, 0.0, 1, 3.8, 3, 11.6),
    ("Horry", 12, 4.8, 28, 3.8, 35, 4.8),
    ("Jasper", 0, 0.0, 3, 4.6, 4, 5.9),
    ("Kershaw", 2, 3.9, 9, 5.8, 9, 5.7),
    ("Lancaster", 3, 3.6, 9, 3.8, 13, 5.9),
    ("Laurens", 6, 11.9, 11, 7.2, 4, 2.5),
    ("Lee", 0, 0.0, 1, 6.5, 1, 7.0),
    ("Lexington", 11, 5.0, 33, 4.7, 33, 4.5),
    ("McCormick", 0, 0.0, 0, 0.0, 0, 0.0),
    ("Marion", 4, 33.6, 5, 15.3, 0, 0.0),
    ("Marlboro", 0, 0.0, 0, 0.0, 1, 3.0),
    ("Newberry", 1, 4.3, 5, 6.9, 3, 4.1),
    ("Oconee", 6, 10.8, 16, 9.2, 20, 11.0),
    ("Orangeburg", 1, 3.9, 4, 5.0, 3, 3.4),
    ("Pickens", 10, 9.6, 25, 7.8, 16, 5.0),
    ("Richland", 7, 4.0, 22, 4.2, 19, 3.4),
    ("Saluda", 2, 19.4, 5, 11.8, 7, 13.2),
    ("Spartanburg", 21, 6.7, 50, 5.5, 40, 4.6),
    ("Sumter", 1, 1.7, 12, 6.8, 12, 6.1),
    ("Union", 1, 6.4, 2, 4.2, 5, 9.5),
    ("Williamsburg", 1, 11.1, 1, 3.6, 1, 3.9),
    ("York", 13, 6.3, 26, 4.2, 20, 3.3),
]

# Table C-27: Low Weight Live Births, all races, SC DPH VMS 2023, p.59
# columns: county, lbw_count_2023, lbw_pct_2023
LBW_ROWS = [
    ("South Carolina", 5768, 10.0),
    ("Abbeville", 23, 9.5),
    ("Aiken", 196, 10.3),
    ("Allendale", 9, 12.9),
    ("Anderson", 218, 9.2),
    ("Bamberg", 22, 17.2),
    ("Barnwell", 30, 12.1),
    ("Beaufort", 168, 8.9),
    ("Berkeley", 320, 10.2),
    ("Calhoun", 14, 11.6),
    ("Charleston", 442, 9.1),
    ("Cherokee", 64, 10.2),
    ("Chester", 33, 9.6),
    ("Chesterfield", 51, 10.5),
    ("Clarendon", 34, 12.2),
    ("Colleton", 61, 13.9),
    ("Darlington", 83, 11.6),
    ("Dillon", 58, 16.9),
    ("Dorchester", 187, 9.4),
    ("Edgefield", 31, 14.3),
    ("Fairfield", 22, 12.9),
    ("Florence", 226, 14.5),
    ("Georgetown", 54, 10.9),
    ("Greenville", 554, 8.4),
    ("Greenwood", 87, 11.7),
    ("Hampton", 24, 11.7),
    ("Horry", 286, 8.5),
    ("Jasper", 57, 12.6),
    ("Kershaw", 64, 8.4),
    ("Lancaster", 122, 9.9),
    ("Laurens", 71, 9.5),
    ("Lee", 26, 15.7),
    ("Lexington", 304, 9.7),
    ("McCormick", 8, 14.0),
    ("Marion", 60, 18.4),
    ("Marlboro", 33, 12.8),
    ("Newberry", 39, 9.3),
    ("Oconee", 56, 8.3),
    ("Orangeburg", 105, 13.2),
    ("Pickens", 84, 7.0),
    ("Richland", 545, 12.0),
    ("Saluda", 21, 10.1),
    ("Spartanburg", 391, 8.9),
    ("Sumter", 163, 12.6),
    ("Union", 22, 9.3),
    ("Williamsburg", 38, 14.9),
    ("York", 262, 8.7),
]

# March of Dimes maternity care access + SCBOI/USC IMPH high-need designations.
# access_level from March of Dimes 2023/2024 reports (qualitative synthesis);
# high_need_tertile from USC Institute for Families in Society MCH Data Snapshot
# (2024) "Lowest Tertile (Highest Need)" counties by Maternal Vulnerability Index.
MATERNITY_ACCESS = {
    "Abbeville": ("desert_or_low", True),
    "Allendale": ("desert_or_low", True),
    "Bamberg": ("desert_or_low", False),
    "Barnwell": ("desert_or_low", True),
    "Calhoun": ("desert_or_low", False),
    "Chester": ("desert_or_low", False),
    "Chesterfield": ("desert_or_low", False),
    "Clarendon": ("desert_or_low", False),
    "Colleton": ("desert_or_low", False),
    "Dillon": ("desert_or_low", False),
    "Edgefield": ("desert_or_low", False),
    "Fairfield": ("desert_or_low", False),
    "Greenwood": ("low_access", True),
    "Hampton": ("desert_or_low", False),
    "Jasper": ("desert_or_low", False),
    "Laurens": ("low_access_ob_closed_2023", True),
    "Lee": ("desert_or_low", True),
    "Marion": ("desert_or_low", False),
    "Marlboro": ("desert_or_low", False),
    "McCormick": ("desert_or_low", True),
    "Newberry": ("low_access", False),
    "Saluda": ("desert_or_low", False),
    "Union": ("desert_or_low", False),
    "Williamsburg": ("desert_or_low", True),
    "Kershaw": ("low_access_ob_closed_2025", False),
    "Georgetown": ("low_access_ob_closed_2020", False),
    "Charleston": ("full_access_but_ob_closed_2020_mtpleasant", False),
}


def build_imr():
    df = pd.DataFrame(
        IMR_ROWS,
        columns=[
            "county",
            "infant_deaths_2023",
            "imr_2023",
            "infant_deaths_2021_2023",
            "imr_2021_2023",
            "infant_deaths_2018_2020",
            "imr_2018_2020",
        ],
    )
    df["source"] = "SC DPH VMS 2023, Table F-3"
    df["source_url"] = VMS_PDF
    out = os.path.join(DATA_DIR, "sc_county_infant_mortality.csv")
    df.to_csv(out, index=False)
    print(f"IMR: {len(df)} counties -> {out}")
    return df


def build_lbw():
    df = pd.DataFrame(LBW_ROWS, columns=["county", "lbw_count_2023", "lbw_pct_2023"])
    df["source"] = "SC DPH VMS 2023, Table C-27"
    df["source_url"] = VMS_PDF
    out = os.path.join(DATA_DIR, "sc_county_low_birthweight.csv")
    df.to_csv(out, index=False)
    print(f"LBW: {len(df)} counties -> {out}")
    return df


def build_maternity_access():
    rows = []
    for county, (level, high_need) in MATERNITY_ACCESS.items():
        rows.append(
            {
                "county": county,
                "maternity_access_flag": level,
                "high_need_mvi_tertile": high_need,
                "source": "March of Dimes Maternity Care Deserts SC (2023/2024); USC IFS MCH Data Snapshot (2024); SCBOI Annual Report",
                "source_url": "https://www.marchofdimes.org/peristats/reports/south-carolina/maternity-care-deserts",
            }
        )
    df = pd.DataFrame(rows)
    out = os.path.join(DATA_DIR, "sc_county_maternity_access.csv")
    df.to_csv(out, index=False)
    print(f"Maternity access flags: {len(df)} counties -> {out}")
    return df


def build_merged(imr, lbw, access):
    chr_df = pd.read_csv(
        os.path.join(PARENT_DATA, "merged_county_data.csv"), dtype={"fips": str}
    )
    sc = chr_df[chr_df["state"] == "SC"].copy()
    sc["county"] = sc["county_name"].str.replace(" County", "", regex=False)

    merged = sc.merge(imr, on="county", how="left").merge(
        lbw, on="county", how="left", suffixes=("", "_lbw")
    )
    merged = merged.merge(access, on="county", how="left")
    merged["maternity_access_flag"] = merged["maternity_access_flag"].fillna(
        "full_access_or_not_flagged"
    )
    merged["high_need_mvi_tertile"] = merged["high_need_mvi_tertile"].fillna(False)

    out = os.path.join(DATA_DIR, "sc_statewide_merged.csv")
    merged.to_csv(out, index=False)
    print(f"Statewide merged: {len(merged)} counties, {len(merged.columns)} cols -> {out}")
    return merged


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    imr = build_imr()
    lbw = build_lbw()
    access = build_maternity_access()
    build_merged(imr, lbw, access)


if __name__ == "__main__":
    main()
