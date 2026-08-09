"""
Charleston County deep-dive, step 2: Merge tract data & compute disparities
=============================================================================

Builds a wide-format tract table (one row per census tract) merging PLACES
health measures and CDC SVI, then computes:

  - Tract-level summary statistics (min, max, range, Gini-like spread)
  - Pearson correlations between health measures and SVI themes
  - Ranked lists of highest-burden tracts per issue

Outputs:
  ../data/merged_tract_data.csv
  ../results/tract_summary_stats.csv
  ../results/tract_correlations.csv
  ../results/top_burden_tracts.csv
  ../results/issue_metrics.json   (headline numbers for README)
"""

import json
import os

import numpy as np
import pandas as pd
from scipy import stats

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")

# Key tract-level measures mapped to policy issue domains
KEY_MEASURES = {
    "DIABETES": "diabetes_pct",
    "OBESITY": "obesity_pct",
    "ACCESS2": "uninsured_pct",
    "FOODINSECU": "food_insecurity_pct",
    "HOUSINSECU": "housing_insecurity_pct",
    "MHLTH": "mental_distress_pct",
    "DEPRESSION": "depression_pct",
    "CSMOKING": "smoking_pct",
    "BPHIGH": "high_blood_pressure_pct",
    "CHD": "coronary_heart_disease_pct",
    "STROKE": "stroke_pct",
    "GHLTH": "fair_poor_health_pct",
    "LPA": "physical_inactivity_pct",
    "SHUTUTILITY": "utility_shutoff_threat_pct",
    "LACKTRPT": "transportation_barrier_pct",
    "LONELINESS": "loneliness_pct",
}


def places_wide(places_long: pd.DataFrame) -> pd.DataFrame:
    sub = places_long[places_long["measureid"].isin(KEY_MEASURES.keys())].copy()
    sub = sub.drop_duplicates(subset=["tract_fips", "measureid"], keep="first")
    wide = sub.pivot(index="tract_fips", columns="measureid", values="data_value")
    wide = wide.rename(columns=KEY_MEASURES)
    wide = wide.reset_index()
    return wide


def compute_issue_metrics(merged: pd.DataFrame, benchmarks: pd.DataFrame) -> dict:
    n_tracts = len(merged)

    def spread(col):
        s = merged[col].dropna()
        return {
            "min": round(float(s.min()), 1),
            "max": round(float(s.max()), 1),
            "range": round(float(s.max() - s.min()), 1),
            "mean": round(float(s.mean()), 1),
            "median": round(float(s.median()), 1),
        }

    # High-burden tracts: top quartile on measure AND SVI >= 0.75
    high_svi = merged[merged["RPL_THEMES"] >= 0.75]
    high_burden_diabetes = merged[
        merged["diabetes_pct"] >= merged["diabetes_pct"].quantile(0.75)
    ]
    overlap = len(
        set(high_svi["tract_fips"]) & set(high_burden_diabetes["tract_fips"])
    )

    # SVI spread
    svi_spread = spread("RPL_THEMES")

    # County overdose benchmark
    od_row = benchmarks[benchmarks["metric"] == "drug_overdose_death_rate"].iloc[0]

    metrics = {
        "n_tracts": n_tracts,
        "county_fips": "45019",
        "drug_overdose_rate_per_100k": round(float(od_row["charleston"]), 1),
        "drug_overdose_us_median": round(float(od_row["us_median"]), 1),
        "drug_overdose_sc_median": round(float(od_row["sc_median"]), 1),
        "life_expectancy_years": round(
            float(
                benchmarks[benchmarks["metric"] == "life_expectancy"]["charleston"].iloc[0]
            ),
            1,
        ),
        "sc_life_expectancy_median": round(
            float(
                benchmarks[benchmarks["metric"] == "life_expectancy"]["sc_median"].iloc[0]
            ),
            1,
        ),
        "median_household_income": int(
            benchmarks[benchmarks["metric"] == "median_household_income"]["charleston"].iloc[0]
        ),
        "child_poverty_pct": round(
            float(
                benchmarks[benchmarks["metric"] == "child_poverty_pct"]["charleston"].iloc[0]
            )
            * 100,
            1,
        ),
        "uninsured_county_pct": round(
            float(benchmarks[benchmarks["metric"] == "uninsured_pct"]["charleston"].iloc[0])
            * 100,
            1,
        ),
        "severe_housing_problems_pct": round(
            float(
                benchmarks[
                    benchmarks["metric"] == "severe_housing_problems_pct"
                ]["charleston"].iloc[0]
            )
            * 100,
            1,
        ),
        "svi_overall": svi_spread,
        "diabetes_tract_spread": spread("diabetes_pct"),
        "obesity_tract_spread": spread("obesity_pct"),
        "uninsured_tract_spread": spread("uninsured_pct"),
        "food_insecurity_tract_spread": spread("food_insecurity_pct"),
        "mental_distress_tract_spread": spread("mental_distress_pct"),
        "high_svi_tract_count": int(len(high_svi)),
        "high_svi_tract_pct": round(100 * len(high_svi) / n_tracts, 1),
        "diabetes_high_svi_overlap_tracts": overlap,
    }
    return metrics


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    places = pd.read_csv(
        os.path.join(DATA_DIR, "places_tracts_long.csv"), dtype={"tract_fips": str}
    )
    svi = pd.read_csv(os.path.join(DATA_DIR, "svi_tracts.csv"), dtype={"tract_fips": str})
    benchmarks = pd.read_csv(os.path.join(DATA_DIR, "county_benchmarks.csv"))

    wide = places_wide(places)
    wide = wide.merge(svi, on="tract_fips", how="left")
    out_merged = os.path.join(DATA_DIR, "merged_tract_data.csv")
    wide.to_csv(out_merged, index=False)
    print(f"Merged tract table: {len(wide)} tracts, {wide.shape[1]} columns -> {out_merged}")

    issue_metrics = compute_issue_metrics(wide, benchmarks)
    with open(os.path.join(RESULTS_DIR, "issue_metrics.json"), "w") as f:
        json.dump(issue_metrics, f, indent=2)
    print("Wrote issue_metrics.json")

    merged = wide.copy()

    # Summary stats per measure
    stat_rows = []
    for mid, col in KEY_MEASURES.items():
        s = merged[col].dropna()
        stat_rows.append(
            {
                "measure_id": mid,
                "column": col,
                "n": len(s),
                "mean": s.mean(),
                "std": s.std(),
                "min": s.min(),
                "p25": s.quantile(0.25),
                "median": s.median(),
                "p75": s.quantile(0.75),
                "max": s.max(),
            }
        )
    stats_df = pd.DataFrame(stat_rows)
    stats_path = os.path.join(RESULTS_DIR, "tract_summary_stats.csv")
    stats_df.to_csv(stats_path, index=False)
    print(f"Wrote {stats_path}")

    # Correlations: health measures vs SVI themes
    svi_cols = ["RPL_THEMES", "RPL_THEME1", "RPL_THEME2", "RPL_THEME3", "RPL_THEME4"]
    corr_rows = []
    for col in KEY_MEASURES.values():
        for svi_col in svi_cols:
            sub = merged[[col, svi_col]].dropna()
            if len(sub) < 10:
                continue
            r, p = stats.pearsonr(sub[col], sub[svi_col])
            corr_rows.append(
                {
                    "health_measure": col,
                    "svi_theme": svi_col,
                    "pearson_r": r,
                    "p_value": p,
                    "n": len(sub),
                }
            )
    corr_df = pd.DataFrame(corr_rows)
    corr_path = os.path.join(RESULTS_DIR, "tract_correlations.csv")
    corr_df.to_csv(corr_path, index=False)
    print(f"Wrote {corr_path}")

    # Top 10 highest-burden tracts per key measure
    burden_rows = []
    priority = [
        "diabetes_pct",
        "obesity_pct",
        "uninsured_pct",
        "food_insecurity_pct",
        "mental_distress_pct",
        "fair_poor_health_pct",
    ]
    for col in priority:
        top = merged.nlargest(10, col)[
            ["tract_fips", col, "RPL_THEMES", "E_TOTPOP"]
        ].copy()
        top["issue"] = col
        top = top.rename(columns={col: "value", "RPL_THEMES": "svi_percentile"})
        burden_rows.append(top)
    burden_df = pd.concat(burden_rows, ignore_index=True)
    burden_path = os.path.join(RESULTS_DIR, "top_burden_tracts.csv")
    burden_df.to_csv(burden_path, index=False)
    print(f"Wrote {burden_path}")


if __name__ == "__main__":
    main()
