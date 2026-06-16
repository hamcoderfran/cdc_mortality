"""
Project 3, step 4: Merge datasets and compute correlations
==============================================================

Merges the three data sources downloaded in steps 1-3 into a single
per-county table, then for each of the 6 causes of death / health outcomes:

  - Drug Overdose Deaths (age-adjusted rate per 100k)
  - Suicides (age-adjusted rate per 100k)
  - Heart Disease Mortality (age-adjusted rate per 100k)
  - Stroke Mortality (age-adjusted rate per 100k)
  - Diabetes Prevalence (% of adults, PLACES model-based estimate)
  - Lung Cancer Mortality (age-adjusted rate per 100k)

computes:
  - Pearson and Spearman correlations (with p-values) against every
    socioeconomic / healthcare-access / pollution predictor
  - A standardized multivariable OLS regression (all predictors together)
    to show each predictor's independent association

Outputs:
  ../data/merged_county_data.csv          merged per-county table
  ../results/correlation_pearson.csv      outcome x predictor Pearson r, p
  ../results/correlation_spearman.csv     outcome x predictor Spearman rho, p
  ../results/regression_coefficients.csv  standardized OLS betas per outcome
"""

import os

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")

OUTCOMES = [
    "drug_overdose_death_rate",
    "suicide_death_rate",
    "heart_disease_death_rate",
    "stroke_death_rate",
    "diabetes_prevalence_pct",
    "lung_cancer_death_rate",
]

PREDICTORS = [
    "median_household_income",
    "income_inequality_ratio",
    "unemployment_pct",
    "child_poverty_pct",
    "hs_completion_pct",
    "broadband_access_pct",
    "uninsured_pct",
    "pop_per_pcp",
    "pop_per_mental_health_provider",
    "pm25",
    "severe_housing_problems_pct",
    "food_environment_index",
    "long_commute_pct",
]


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    chr_df = pd.read_csv(os.path.join(DATA_DIR, "chr_subset.csv"), dtype={"fips": str})
    cdc_df = pd.read_csv(os.path.join(DATA_DIR, "cdc_heart_stroke_diabetes.csv"), dtype={"fips": str})
    lung_df = pd.read_csv(os.path.join(DATA_DIR, "lung_cancer_mortality.csv"), dtype={"fips": str})

    merged = chr_df.merge(cdc_df, on="fips", how="left").merge(lung_df, on="fips", how="left")
    merged["fips"] = merged["fips"].str.zfill(5)
    merged.to_csv(os.path.join(DATA_DIR, "merged_county_data.csv"), index=False)
    print(f"Merged table: {len(merged)} counties, {merged.shape[1]} columns")

    pearson_rows = []
    spearman_rows = []
    for outcome in OUTCOMES:
        for pred in PREDICTORS:
            sub = merged[[outcome, pred]].apply(pd.to_numeric, errors="coerce").dropna()
            if len(sub) < 30:
                continue
            r, p = stats.pearsonr(sub[outcome], sub[pred])
            rho, p_s = stats.spearmanr(sub[outcome], sub[pred])
            pearson_rows.append(
                {"outcome": outcome, "predictor": pred, "n": len(sub), "pearson_r": r, "p_value": p}
            )
            spearman_rows.append(
                {"outcome": outcome, "predictor": pred, "n": len(sub), "spearman_rho": rho, "p_value": p_s}
            )

    pearson_df = pd.DataFrame(pearson_rows).sort_values(["outcome", "pearson_r"])
    spearman_df = pd.DataFrame(spearman_rows).sort_values(["outcome", "spearman_rho"])
    pearson_df.to_csv(os.path.join(RESULTS_DIR, "correlation_pearson.csv"), index=False)
    spearman_df.to_csv(os.path.join(RESULTS_DIR, "correlation_spearman.csv"), index=False)
    print("Wrote correlation_pearson.csv and correlation_spearman.csv")

    # Standardized multivariable OLS per outcome
    reg_rows = []
    for outcome in OUTCOMES:
        cols = [outcome] + PREDICTORS
        sub = merged[cols].apply(pd.to_numeric, errors="coerce").dropna()
        if len(sub) < 100:
            continue
        y = (sub[outcome] - sub[outcome].mean()) / sub[outcome].std()
        X = sub[PREDICTORS].apply(lambda c: (c - c.mean()) / c.std())
        X = sm.add_constant(X)
        model = sm.OLS(y, X).fit()
        for pred in PREDICTORS:
            reg_rows.append(
                {
                    "outcome": outcome,
                    "predictor": pred,
                    "n": len(sub),
                    "std_beta": model.params[pred],
                    "p_value": model.pvalues[pred],
                    "r_squared_full_model": model.rsquared,
                }
            )

    reg_df = pd.DataFrame(reg_rows)
    reg_df.to_csv(os.path.join(RESULTS_DIR, "regression_coefficients.csv"), index=False)
    print("Wrote regression_coefficients.csv")

    # Print top correlations per outcome for a quick console summary
    for outcome in OUTCOMES:
        sub = pearson_df[pearson_df["outcome"] == outcome].copy()
        sub["abs_r"] = sub["pearson_r"].abs()
        sub = sub.sort_values("abs_r", ascending=False).head(3)
        print(f"\n{outcome} -- top correlates:")
        for _, row in sub.iterrows():
            print(f"  {row['predictor']}: r={row['pearson_r']:.3f} (p={row['p_value']:.2e}, n={row['n']})")


if __name__ == "__main__":
    main()
