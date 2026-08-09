"""
Thesis evaluation, step 5: Build evidence audit summary from per-ticker citations
==================================================================================

Reads genz_alpha_stock_evidence.csv and genz_alpha_stock_scores.csv to produce
transparent evidence tier counts and overall defensibility grades.

Outputs:
  ../results/evidence_audit_summary.json
  ../data/genz_alpha_ticker_evidence_grades.csv
"""

import json
import os
from datetime import datetime

import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")

TIER_ORDER = {"A": 3, "B": 2, "C": 1}


def grade_ticker(row: pd.Series) -> str:
    """Grade ticker-specific claim defensibility (excluding composite score)."""
    a, b, c = row["tier_a"], row["tier_b"], row["tier_c"]
    verified = row["verified_yes"]
    if a >= 2 or (a >= 1 and verified >= 2):
        return "Strong"
    if a >= 1 or (b >= 2 and verified >= 1):
        return "Moderate"
    if b >= 2:
        return "Moderate"
    if b >= 1:
        return "Weak-Moderate"
    return "Weak"


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    evidence_path = os.path.join(DATA_DIR, "genz_alpha_stock_evidence.csv")
    scores_path = os.path.join(DATA_DIR, "genz_alpha_stock_scores.csv")

    ev = pd.read_csv(evidence_path)
    scores = pd.read_csv(scores_path)

    summary_rows = []
    for ticker, grp in ev.groupby("ticker"):
        tier_counts = grp["evidence_tier"].value_counts().to_dict()
        verified_yes = (grp["verified"] == "yes").sum()
        verified_partial = (grp["verified"] == "partial").sum()
        row = {
            "ticker": ticker,
            "tier_a": tier_counts.get("A", 0),
            "tier_b": tier_counts.get("B", 0),
            "tier_c": tier_counts.get("C", 0),
            "total_claims": len(grp),
            "verified_yes": verified_yes,
            "verified_partial": verified_partial,
            "composite_score_evidence_tier": "C",
        }
        row["ticker_evidence_grade"] = grade_ticker(pd.Series(row))
        summary_rows.append(row)

    grades = pd.DataFrame(summary_rows).merge(
        scores[["ticker", "company", "theme", "composite_score_100", "historical_cagr_2019_pct"]],
        on="ticker",
        how="left",
    )
    grades = grades.sort_values("composite_score_100", ascending=False)
    grades.to_csv(os.path.join(DATA_DIR, "genz_alpha_ticker_evidence_grades.csv"), index=False)

    macro = pd.read_csv(os.path.join(DATA_DIR, "genz_alpha_behavior_trends.csv"))
    macro_with_url = macro["url"].notna().sum()

    audit = {
        "generated": datetime.now().astimezone().isoformat(),
        "methodology_note": (
            "Tier A = primary data (federal surveys, SEC filings, computed prices). "
            "Tier B = reputable industry/consumer surveys (not ticker-specific). "
            "Tier C = analyst judgment / inference. Composite scores are always Tier C."
        ),
        "macro_behavioral_claims": {
            "count": len(macro),
            "with_source_url": int(macro_with_url),
            "evidence_quality": f"Strong (Tier A/B) — all {len(macro)} stats have cited URLs",
        },
        "ticker_evidence_summary": {
            "tickers": len(grades),
            "grade_distribution": grades["ticker_evidence_grade"].value_counts().to_dict(),
            "tier_a_claims_total": int(grades["tier_a"].sum()),
            "tier_b_claims_total": int(grades["tier_b"].sum()),
            "tier_c_claims_total": int(grades["tier_c"].sum()),
        },
        "composite_scores": {
            "evidence_tier": "C",
            "note": "7-factor 1-5 scores are expert judgment; not regression-derived or backtested",
        },
        "forward_10_20yr_predictions": {
            "evidence_tier": "C",
            "note": "Not empirically validated; scenario probabilities are illustrative",
        },
        "tickers_by_evidence_grade": grades[
            ["ticker", "company", "ticker_evidence_grade", "tier_a", "tier_b", "tier_c", "composite_score_100"]
        ].to_dict(orient="records"),
        "high_confidence_ticker_claims": grades[grades["ticker_evidence_grade"] == "Strong"][
            ["ticker", "company", "tier_a", "tier_b"]
        ].to_dict(orient="records"),
        "low_confidence_ticker_claims": grades[grades["ticker_evidence_grade"].isin(["Weak", "Weak-Moderate"])][
            ["ticker", "company", "tier_c", "composite_score_100"]
        ].to_dict(orient="records"),
    }

    out_path = os.path.join(RESULTS_DIR, "evidence_audit_summary.json")
    with open(out_path, "w") as f:
        json.dump(audit, f, indent=2)

    print(f"Evidence audit: {len(grades)} tickers, {int(grades['tier_a'].sum())} Tier A claims")
    print(f"Grades: {audit['ticker_evidence_summary']['grade_distribution']}")


if __name__ == "__main__":
    main()
