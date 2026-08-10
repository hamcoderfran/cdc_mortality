"""
Greater South Carolina neonatal health — step 5: statewide statistical analysis
=================================================================================

Runs correlation and simple linear regression between county-level social
determinants of health (County Health Rankings 2025) and neonatal outcomes
(infant mortality, low birthweight; SC DPH VMS 2023) across up to 43 South
Carolina counties with available data (Allendale, Bamberg, McCormick are
suppressed in the County Health Rankings merged file due to small
population/measure suppression).

This produces genuinely new statistical findings (not present in the original
Charleston-only package): which social/economic factors most strongly predict
county-level neonatal risk across the *whole state*, and which counties are
statistical outliers (worse outcomes than SDOH alone would predict, or vice
versa) — a signal of potential clinical/health-system-specific problems.

Outputs:
  ../results/statewide_correlations.csv
  ../results/statewide_regression_summary.json
  ../results/county_outlier_residuals.csv
"""

import json
import os

import numpy as np
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")

PREDICTORS = [
    "uninsured_pct",
    "child_poverty_pct",
    "median_household_income",
    "pm25",
    "severe_housing_problems_pct",
    "food_environment_index",
    "broadband_access_pct",
    "unemployment_pct",
    "income_inequality_ratio",
]

OUTCOMES = {
    "imr_2021_2023": "3-year average infant mortality rate per 1,000 live births (2021-2023)",
    "lbw_pct_2023": "Low birthweight percent of live births (2023)",
}


def pearson_r(x, y):
    mask = x.notna() & y.notna()
    x, y = x[mask], y[mask]
    if len(x) < 5:
        return None, None, len(x)
    r = np.corrcoef(x, y)[0, 1]
    # two-sided p-value via t-distribution approximation
    n = len(x)
    t_stat = r * np.sqrt((n - 2) / max(1e-9, (1 - r**2)))
    from math import erf, sqrt

    # crude normal approximation for p-value (n>15 reasonably ok); flag as approximate
    p_approx = 2 * (1 - 0.5 * (1 + erf(abs(t_stat) / sqrt(2))))
    return round(r, 3), round(p_approx, 4), n


def simple_ols(x, y):
    mask = x.notna() & y.notna()
    x, y = x[mask].values, y[mask].values
    if len(x) < 5:
        return None
    A = np.vstack([x, np.ones(len(x))]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    pred = slope * x + intercept
    ss_res = np.sum((y - pred) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else None
    return {"slope": round(slope, 4), "intercept": round(intercept, 4), "r_squared": round(r2, 3) if r2 else None}


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    df = pd.read_csv(os.path.join(DATA_DIR, "sc_statewide_merged.csv"))
    df = df[df["county"] != "South Carolina"].copy()

    corr_rows = []
    for outcome, label in OUTCOMES.items():
        for pred in PREDICTORS:
            r, p, n = pearson_r(df[pred], df[outcome])
            if r is None:
                continue
            ols = simple_ols(df[pred], df[outcome])
            corr_rows.append(
                {
                    "outcome": outcome,
                    "outcome_label": label,
                    "predictor": pred,
                    "pearson_r": r,
                    "approx_p_value": p,
                    "n_counties": n,
                    "ols_slope": ols["slope"] if ols else None,
                    "ols_r_squared": ols["r_squared"] if ols else None,
                }
            )
    corr_df = pd.DataFrame(corr_rows).sort_values(
        ["outcome", "pearson_r"], key=lambda s: s.abs() if s.name == "pearson_r" else s, ascending=False
    )
    out_corr = os.path.join(RESULTS_DIR, "statewide_correlations.csv")
    corr_df.to_csv(out_corr, index=False)
    print(f"Correlations: {len(corr_df)} rows -> {out_corr}")

    # Outlier analysis: regress IMR on uninsured_pct + child_poverty_pct (top predictors),
    # find counties with largest positive residuals (worse than predicted) — signals
    # possible clinical/access issues beyond generic poverty/insurance status.
    sub = df.dropna(subset=["imr_2021_2023", "uninsured_pct", "child_poverty_pct"]).copy()
    X = sub[["uninsured_pct", "child_poverty_pct"]].values
    X = np.column_stack([X, np.ones(len(X))])
    y = sub["imr_2021_2023"].values
    coefs, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coefs
    sub["predicted_imr"] = pred
    sub["residual"] = sub["imr_2021_2023"] - sub["predicted_imr"]
    sub_sorted = sub.sort_values("residual", ascending=False)[
        ["county", "imr_2021_2023", "predicted_imr", "residual", "uninsured_pct", "child_poverty_pct", "maternity_access_flag", "high_need_mvi_tertile"]
    ]
    out_resid = os.path.join(RESULTS_DIR, "county_outlier_residuals.csv")
    sub_sorted.to_csv(out_resid, index=False)
    print(f"Residuals: {len(sub_sorted)} counties -> {out_resid}")

    summary = {
        "n_counties_analyzed": int(len(df)),
        "note_on_suppressed_counties": "Allendale, Bamberg, McCormick excluded (County Health Rankings suppresses small-population measures); their infant mortality counts are also too small (<20 deaths/3yr) to be reliable per VMS footnotes.",
        "top_predictors_of_imr": corr_df[corr_df["outcome"] == "imr_2021_2023"].head(5).to_dict(orient="records"),
        "top_predictors_of_lbw": corr_df[corr_df["outcome"] == "lbw_pct_2023"].head(5).to_dict(orient="records"),
        "highest_positive_residual_counties": sub_sorted.head(8).to_dict(orient="records"),
        "lowest_residual_counties": sub_sorted.tail(5).to_dict(orient="records"),
        "methodology_caveats": [
            "n≈43 counties: modest sample size for regression; treat p-values as exploratory, not confirmatory.",
            "P-values approximate (normal approximation to t-distribution), not a substitute for formal hypothesis testing.",
            "3-year average IMR (2021-2023) used to reduce small-number instability, per VMS guidance that single-year county rates with ≤20 deaths are unreliable.",
            "County Health Rankings measures are themselves modeled/lagged estimates (ACS 5-year, BRFSS small-area models), not real-time.",
            "Ecological (county-level) correlation does not establish individual-level causation (ecological fallacy risk).",
        ],
    }
    out_summary = os.path.join(RESULTS_DIR, "statewide_regression_summary.json")
    with open(out_summary, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"Summary -> {out_summary}")


if __name__ == "__main__":
    main()
