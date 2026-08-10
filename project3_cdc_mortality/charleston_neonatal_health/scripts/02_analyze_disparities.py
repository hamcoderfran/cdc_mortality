"""
Charleston neonatal health — step 2: disparity analysis & tract SDOH overlay
===========================================================================

Computes racial disparity ratios, Charleston vs SC benchmarks, and correlates
tract-level social needs (PLACES/SVI) with vulnerability rankings.

Outputs:
  ../results/disparity_summary.json
  ../results/tract_neonatal_risk_proxy.csv
  ../results/racial_disparities.csv
"""

import json
import os

import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def load_indicators():
    return pd.read_csv(os.path.join(DATA_DIR, "county_neonatal_indicators.csv"))


def indicator_value(df, name, geo="Charleston County"):
    row = df[(df["indicator"] == name) & (df["geography"] == geo)]
    if row.empty:
        return None
    return float(row.iloc[0]["value"])


def build_racial_disparities(ind):
    pairs = [
        ("low birthweight", "lbw_pct_white_nh", "lbw_pct_black", "Black/White LBW ratio"),
        (
            "infant mortality (3-yr avg)",
            "infant_mortality_white_per_1000",
            "infant_mortality_black_per_1000",
            "Black/White IMR ratio",
        ),
        (
            "Medicaid at birth",
            "medicaid_births_pct_white",
            "medicaid_births_pct_black",
            "Black/White Medicaid coverage ratio",
        ),
        (
            "Inadequate prenatal care (Kotelchuck)",
            "kotelchuck_inadequate_pct_white",
            "kotelchuck_inadequate_pct_black",
            "Black/White inadequate PNC ratio",
        ),
        (
            "Unmarried births",
            "unmarried_births_pct_white",
            "unmarried_births_pct_black",
            "Black/White unmarried birth ratio",
        ),
    ]
    rows = []
    for label, w_key, b_key, desc in pairs:
        w = indicator_value(ind, w_key)
        b = indicator_value(ind, b_key)
        if w and b and w > 0:
            rows.append(
                {
                    "disparity": label,
                    "white_or_reference": w,
                    "black_or_comparison": b,
                    "ratio_black_to_white": round(b / w, 2),
                    "absolute_gap": round(b - w, 2),
                    "description": desc,
                }
            )
    df = pd.DataFrame(rows)
    out = os.path.join(RESULTS_DIR, "racial_disparities.csv")
    df.to_csv(out, index=False)
    print(f"Racial disparities: {len(df)} -> {out}")
    return df


def build_tract_proxy():
    """Tract-level SDOH proxy index — neonatal outcomes are not published at tract level in SC."""
    places = pd.read_csv(os.path.join(DATA_DIR, "places_tracts_long.csv"))
    places["tract_fips"] = places["tract_fips"].astype(str).str.zfill(11)
    svi = pd.read_csv(os.path.join(DATA_DIR, "svi_tracts.csv"), dtype={"tract_fips": str})

    want = {
        "FOODINSECU": "food_insecurity_pct",
        "HOUSINSECU": "housing_insecurity_pct",
        "LACKTRPT": "transportation_barrier_pct",
        "ACCESS2": "uninsured_pct",
        "DEPRESSION": "depression_pct",
    }
    wide = {}
    for mid, col in want.items():
        sub = places[places["measureid"] == mid][["tract_fips", "data_value"]]
        wide[col] = sub.set_index("tract_fips")["data_value"]

    tract = pd.DataFrame(wide).reset_index()
    tract["tract_fips"] = tract["tract_fips"].astype(str).str.zfill(11)
    svi["tract_fips"] = svi["tract_fips"].astype(str).str.zfill(11)
    tract = tract.merge(svi, on="tract_fips", how="left")

    # Simple neonatal risk proxy: mean percentile of social needs + SVI
    risk_cols = list(want.values()) + ["RPL_THEMES"]
    for c in risk_cols:
        tract[f"{c}_pctile"] = tract[c].rank(pct=True)

    tract["neonatal_risk_proxy_score"] = tract[[f"{c}_pctile" for c in risk_cols]].mean(axis=1)
    tract = tract.sort_values("neonatal_risk_proxy_score", ascending=False)

    out = os.path.join(RESULTS_DIR, "tract_neonatal_risk_proxy.csv")
    tract.to_csv(out, index=False)
    print(f"Tract proxy: {len(tract)} tracts -> {out}")
    return tract


def build_summary(ind, racial, tract):
    summary = {
        "county_fips": "45019",
        "county_name": "Charleston County, SC",
        "analysis_date": "2026-08-10",
        "key_findings": {
            "preterm_birth_pct_2024": indicator_value(ind, "preterm_birth_pct"),
            "preterm_grade": "D+",
            "lbw_pct_2023": indicator_value(ind, "low_birthweight_pct"),
            "lbw_black_white_ratio": round(
                indicator_value(ind, "lbw_pct_black")
                / indicator_value(ind, "lbw_pct_white_nh"),
                2,
            ),
            "infant_mortality_vms_2023": indicator_value(ind, "infant_mortality_rate_per_1000"),
            "infant_mortality_periStats_2023": indicator_value(
                ind, "infant_mortality_rate_periStats"
            ),
            "infant_mortality_trend_pct_increase_2013_2023": indicator_value(
                ind, "infant_mortality_pct_change_2013_2023"
            ),
            "inadequate_prenatal_care_pct_2024": indicator_value(
                ind, "prenatal_care_inadequate_pct"
            ),
            "medicaid_births_pct_2023": indicator_value(ind, "medicaid_births_pct_all"),
            "wic_enrollment_pct_2023": indicator_value(ind, "wic_during_pregnancy_pct"),
            "black_infant_mortality_3yr_avg": indicator_value(
                ind, "infant_mortality_black_per_1000"
            ),
            "white_infant_mortality_3yr_avg": indicator_value(
                ind, "white_infant_mortality_per_1000"
            ),
        },
        "charleston_vs_sc": {
            "preterm": {
                "charleston": indicator_value(ind, "preterm_birth_pct"),
                "sc": indicator_value(ind, "preterm_birth_pct", "South Carolina"),
            },
            "infant_mortality": {
                "charleston_vms": indicator_value(ind, "infant_mortality_rate_per_1000"),
                "sc": indicator_value(ind, "infant_mortality_rate_per_1000", "South Carolina"),
            },
        },
        "top_10_highest_risk_tracts": tract.head(10)[
            ["tract_fips", "neonatal_risk_proxy_score", "RPL_THEMES", "food_insecurity_pct"]
        ].to_dict(orient="records"),
        "racial_disparities": racial.to_dict(orient="records"),
        "data_limitations": [
            "Infant/neonatal mortality is published at county level only in SC VMS; tract maps use SDOH proxies.",
            "VMS 2023 and PeriStats linked data may differ slightly due to residence rules and linkage methods.",
            "Rates based on fewer than 20 deaths are flagged unreliable in VMS footnotes.",
        ],
    }
    out = os.path.join(RESULTS_DIR, "disparity_summary.json")
    with open(out, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Summary -> {out}")


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    ind = load_indicators()
    racial = build_racial_disparities(ind)
    tract = build_tract_proxy()
    build_summary(ind, racial, tract)


if __name__ == "__main__":
    main()
