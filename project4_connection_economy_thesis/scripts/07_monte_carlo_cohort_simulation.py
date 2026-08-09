"""
Monte Carlo cohort-maturity simulation (Gen Z / Gen Alpha → 2041)
==================================================================

Simulates 10,000 stochastic paths of 12 latent behavioral-economic factors
as Gen Z (peak spending ~2030) and Gen Alpha (peak ~2035–2040) mature.

Each stock has factor loadings derived from thematic research (not price-fit).
Outputs probability of thematic LIFT vs CRUSH relative to neutral exposure.

IMPORTANT: This models *thematic cohort tailwinds/headwinds only* — not full
stock returns, valuation, rates, or idiosyncratic execution. See MONTE_CARLO_REPORT.md.

Outputs:
  ../data/monte_carlo_stock_results.csv
  ../results/monte_carlo_summary.json
  ../results/monte_carlo_factor_paths.csv  (median across sims)
  ../results/maps/monte_carlo_dashboard.html
"""

import json
import os
from datetime import datetime

import numpy as np
import pandas as pd

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

SCRIPT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "data")
RESULTS_DIR = os.path.join(SCRIPT_DIR, "..", "results")
MAPS_DIR = os.path.join(RESULTS_DIR, "maps")

# ── Simulation parameters ─────────────────────────────────────────────
N_SIMS = 10_000
START_YEAR = 2026
END_YEAR = 2041          # 15-year horizon
N_YEARS = END_YEAR - START_YEAR
RNG = np.random.default_rng(42)

# Factor names and priors (annual drift %, annual vol %, AR(1) persistence)
# Drifts anchored to cited research ranges in NOVEL_THESES / behavior CSVs
FACTORS = {
    "alcohol_headwind":       {"drift": -0.025, "vol": 0.015, "rho": 0.85, "note": "Beer/spirits volume; NIQ -2.9% baseline"},
    "na_functional_bev":      {"drift":  0.045, "vol": 0.020, "rho": 0.80, "note": "Mocktail/energy substitution"},
    "sober_social_venues":    {"drift":  0.055, "vol": 0.025, "rho": 0.75, "note": "Competitive social eatertainment"},
    "irl_experiences":        {"drift":  0.040, "vol": 0.030, "rho": 0.70, "note": "Concerts, event travel"},
    "wellness_third_space":   {"drift":  0.035, "vol": 0.025, "rho": 0.75, "note": "Gym/run club social"},
    "pet_connection":         {"drift":  0.070, "vol": 0.030, "rho": 0.80, "note": "Pet insurance + premiumization"},
    "analog_tactile":         {"drift":  0.040, "vol": 0.025, "rho": 0.70, "note": "Vinyl, board games, crafts"},
    "swipe_fatigue":          {"drift": -0.050, "vol": 0.030, "rho": 0.80, "note": "Dating app monetization decline"},
    "gen_alpha_gaming":       {"drift":  0.050, "vol": 0.035, "rho": 0.75, "note": "Alpha platform spend"},
    "value_thrift":           {"drift":  0.025, "vol": 0.020, "rho": 0.70, "note": "Off-price, dupes, resale"},
    "home_social_hub":        {"drift":  0.020, "vol": 0.015, "rho": 0.65, "note": "Stay-in, delivery, hosting"},
    "sleep_wellness":         {"drift":  0.030, "vol": 0.020, "rho": 0.75, "note": "Sleep over nightlife"},
    "ai_infra_paradox":       {"drift":  0.060, "vol": 0.040, "rho": 0.70, "note": "AI capex regardless of sentiment"},
    "ai_platform_sentiment":  {"drift": -0.015, "vol": 0.025, "rho": 0.65, "note": "Gen Z AI anger → platform risk"},
    "cybersecurity":          {"drift":  0.035, "vol": 0.030, "rho": 0.75, "note": "Enterprise security TAM"},
    "mental_health_services": {"drift":  0.030, "vol": 0.025, "rho": 0.70, "note": "Behavioral health demand"},
}

FACTOR_NAMES = list(FACTORS.keys())

# Stock → factor loadings (−1 to +1). 0 = no exposure.
# Built from GENZ_ALPHA + NOVEL_THESES thematic mapping.
LOADINGS = {
    # Original basket
    "LYV":  {"irl_experiences": 0.95, "sober_social_venues": 0.3, "ai_platform_sentiment": -0.1},
    "PLNT": {"wellness_third_space": 0.90, "sober_social_venues": 0.5, "sleep_wellness": 0.3},
    "MNST": {"na_functional_bev": 0.85, "alcohol_headwind": -0.2},
    "LULU": {"wellness_third_space": 0.75, "value_thrift": -0.2},
    "ELF":  {"value_thrift": 0.70, "gen_alpha_gaming": 0.1},
    "DUOL": {"analog_tactile": 0.2, "ai_platform_sentiment": 0.3, "gen_alpha_gaming": 0.4},
    "CELH": {"na_functional_bev": 0.80, "wellness_third_space": 0.4},
    "ONON": {"wellness_third_space": 0.70, "sober_social_venues": 0.3},
    "RBLX": {"gen_alpha_gaming": 0.95, "ai_platform_sentiment": -0.2},
    "ETSY": {"analog_tactile": 0.60, "value_thrift": 0.50, "ai_platform_sentiment": 0.2},
    "PEP":  {"na_functional_bev": 0.55, "home_social_hub": 0.2},
    "BKNG": {"irl_experiences": 0.70},
    "TJX":  {"value_thrift": 0.85},
    "ACHC": {"mental_health_services": 0.75},
    "KDP":  {"na_functional_bev": 0.65, "alcohol_headwind": -0.15},
    "HIMS": {"mental_health_services": 0.55, "wellness_third_space": 0.4, "ai_platform_sentiment": -0.3},
    "ROST": {"value_thrift": 0.80},
    "PANW": {"cybersecurity": 0.70, "ai_infra_paradox": 0.3},
    "CRWD": {"cybersecurity": 0.75, "ai_infra_paradox": 0.35},
    "TTWO": {"gen_alpha_gaming": 0.80},
    "EXPE": {"irl_experiences": 0.60},
    "NVDA": {"ai_infra_paradox": 0.90},
    "GOOGL":{"ai_infra_paradox": 0.50, "ai_platform_sentiment": -0.45},
    "VST":  {"analog_tactile": 0.3, "wellness_third_space": 0.2},
    "SAM":  {"alcohol_headwind": 0.40, "na_functional_bev": 0.25},
    "STZ":  {"alcohol_headwind": 0.90},
    "BUD":  {"alcohol_headwind": 0.95},
    "TAP":  {"alcohol_headwind": 0.95, "na_functional_bev": 0.1},
    # Novel basket
    "PLAY": {"sober_social_venues": 0.90, "swipe_fatigue": 0.40, "alcohol_headwind": -0.3},
    "MODG": {"sober_social_venues": 0.85, "swipe_fatigue": 0.35, "wellness_third_space": 0.2},
    "FUN":  {"sober_social_venues": 0.60, "home_social_hub": -0.1},
    "TRUP": {"pet_connection": 0.95},
    "CHWY": {"pet_connection": 0.85, "home_social_hub": 0.35},
    "IDXX": {"pet_connection": 0.75},
    "ELAN": {"pet_connection": 0.50},
    "MTCH": {"swipe_fatigue": 0.95, "sober_social_venues": -0.2},
    "BMBL": {"swipe_fatigue": 0.90},
    "AFRM": {"irl_experiences": 0.35, "sober_social_venues": 0.25, "value_thrift": 0.2},
    "WMG":  {"analog_tactile": 0.90},
    "SONY": {"analog_tactile": 0.55, "gen_alpha_gaming": 0.40},
    "HAS":  {"analog_tactile": 0.85, "gen_alpha_gaming": 0.30},
    "TPX":  {"sleep_wellness": 0.80, "wellness_third_space": 0.2},
    "RMD":  {"sleep_wellness": 0.75},
    "WING": {"home_social_hub": 0.75},
    "DPZ":  {"home_social_hub": 0.70},
    "NFLX": {"home_social_hub": 0.55, "ai_platform_sentiment": -0.15},
    "PINS": {"analog_tactile": 0.65, "home_social_hub": 0.2},
}

# Execution / moat dampener (0.5–1.0) — reduces realized thematic capture
EXECUTION_QUALITY = {
    "LYV": 0.85, "PLNT": 0.70, "RBLX": 0.75, "PLAY": 0.65, "MODG": 0.72,
    "MTCH": 0.55, "BMBL": 0.50, "TAP": 0.60, "BUD": 0.65, "STZ": 0.62,
    "TRUP": 0.88, "CHWY": 0.78, "WMG": 0.82, "HAS": 0.75, "NVDA": 0.92,
    "CELH": 0.68, "HIMS": 0.60, "VST": 0.55,
}
DEFAULT_EXEC = 0.78

# Gen Z / Gen Alpha cohort spending influence weights by year (sum to 1 max each year)
def cohort_weights(years: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Logistic ramps for Gen Z (peak ~2032) and Gen Alpha (peak ~2038)."""
    gen_z = 1 / (1 + np.exp(-0.9 * (years - 2030)))
    gen_alpha = 1 / (1 + np.exp(-0.7 * (years - 2036)))
    gen_z /= gen_z.max()
    gen_alpha /= gen_alpha.max()
    combined = 0.55 * gen_z + 0.45 * gen_alpha
    combined /= combined.max()
    return gen_z, gen_alpha, combined


def simulate_factors(n_sims: int, n_years: int) -> np.ndarray:
    """Shape: (n_sims, n_factors, n_years) — cumulative factor index levels."""
    n_f = len(FACTOR_NAMES)
    paths = np.zeros((n_sims, n_f, n_years))
    for j, fname in enumerate(FACTOR_NAMES):
        p = FACTORS[fname]
        drift, vol, rho = p["drift"], p["vol"], p["rho"]
        level = np.zeros(n_sims)
        for t in range(n_years):
            shock = RNG.normal(drift, vol, n_sims)
            # 15% probability per year of regime flip (trend reversal) — epistemic uncertainty
            flip = RNG.random(n_sims) < 0.08
            shock = np.where(flip, -shock * 1.5, shock)
            level = rho * level + shock
            paths[:, j, t] = level
    return paths


def stock_thematic_returns(
    factor_paths: np.ndarray,
    loadings: dict,
    cohort: np.ndarray,
) -> dict[str, np.ndarray]:
    """
    Returns dict ticker → (n_sims,) cumulative thematic log-return over horizon.
    factor_paths: (n_sims, n_factors, n_years)
    cohort: (n_years,) combined cohort weight
    """
    n_sims, n_f, n_years = factor_paths.shape
    f_idx = {name: i for i, name in enumerate(FACTOR_NAMES)}
    results = {}

    for ticker, loads in loadings.items():
        exec_q = EXECUTION_QUALITY.get(ticker, DEFAULT_EXEC)
        annual = np.zeros((n_sims, n_years))
        for fname, beta in loads.items():
            if fname not in f_idx:
                continue
            j = f_idx[fname]
            # year-over-year change in factor level × loading
            delta = np.diff(factor_paths[:, j, :], axis=1, prepend=0)
            for t in range(n_years):
                annual[:, t] += beta * delta[:, t] * cohort[t] * exec_q
        # Idiosyncratic thematic noise (execution, competition)
        annual += RNG.normal(0, 0.012, (n_sims, n_years))
        cum = annual.sum(axis=1)
        results[ticker] = cum
    return results


def classify_outcomes(cum_returns: np.ndarray) -> dict:
    """Probability metrics for one stock's simulated cumulative thematic returns."""
    return {
        "p_net_positive": float(np.mean(cum_returns > 0)),
        "p_lift": float(np.mean(cum_returns > 0.10)),       # >10% cumulative thematic alpha
        "p_strong_lift": float(np.mean(cum_returns > 0.20)),
        "p_moderate_lift": float(np.mean(cum_returns > 0.05)),
        "p_neutral": float(np.mean((cum_returns >= -0.05) & (cum_returns <= 0.05))),
        "p_moderate_crush": float(np.mean(cum_returns < -0.05)),
        "p_crush": float(np.mean(cum_returns < -0.10)),
        "p_severe_crush": float(np.mean(cum_returns < -0.20)),
        "median_cum": float(np.median(cum_returns)),
        "p10_cum": float(np.percentile(cum_returns, 10)),
        "p90_cum": float(np.percentile(cum_returns, 90)),
        "mean_cum": float(np.mean(cum_returns)),
        "std_cum": float(np.std(cum_returns)),
    }


def build_dashboard(
    stock_df: pd.DataFrame,
    factor_median: pd.DataFrame,
    top_tickers: list,
    bottom_tickers: list,
    out_path: str,
):
    if not HAS_PLOTLY:
        return
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            "P(Thematic Lift) vs P(Crush) — all stocks",
            "Median cumulative thematic return (2026–2041)",
            "Factor paths (median simulation)",
            "Top 10 lift probability",
        ),
        specs=[[{"type": "scatter"}, {"type": "bar"}], [{"type": "scatter"}, {"type": "bar"}]],
        vertical_spacing=0.12,
        horizontal_spacing=0.08,
    )

    fig.add_trace(
        go.Scatter(
            x=stock_df["p_crush"] * 100,
            y=stock_df["p_lift"] * 100,
            mode="markers+text",
            text=stock_df["ticker"],
            textposition="top center",
            marker=dict(
                size=10,
                color=stock_df["median_cum_thematic"],
                colorscale="RdYlGn",
                showscale=True,
                colorbar=dict(title="Median α", x=1.02),
            ),
            hovertemplate="%{text}<br>P(lift): %{y:.1f}%<br>P(crush): %{x:.1f}%<extra></extra>",
        ),
        row=1, col=1,
    )
    fig.update_xaxes(title_text="P(Crush) %", row=1, col=1)
    fig.update_yaxes(title_text="P(Lift) %", row=1, col=1)

    sorted_df = stock_df.sort_values("median_cum_thematic", ascending=True)
    colors = ["#d62728" if x < 0 else "#2ca02c" for x in sorted_df["median_cum_thematic"]]
    fig.add_trace(
        go.Bar(
            x=sorted_df["median_cum_thematic"] * 100,
            y=sorted_df["ticker"],
            orientation="h",
            marker_color=colors,
            hovertemplate="%{y}: %{x:.1f}% cumulative thematic<extra></extra>",
        ),
        row=1, col=2,
    )
    fig.update_xaxes(title_text="Median cumulative thematic return (%)", row=1, col=2)

    for col in factor_median.columns:
        fig.add_trace(
            go.Scatter(
                x=factor_median.index,
                y=factor_median[col] * 100,
                mode="lines",
                name=col,
                showlegend=False,
            ),
            row=2, col=1,
        )
    fig.update_xaxes(title_text="Year", row=2, col=1)
    fig.update_yaxes(title_text="Cumulative factor index (%)", row=2, col=1)

    top10 = stock_df.nlargest(10, "p_lift")
    fig.add_trace(
        go.Bar(
            x=top10["ticker"],
            y=top10["p_lift"] * 100,
            marker_color="#2ca02c",
            hovertemplate="%{x}: P(lift)=%{y:.1f}%<extra></extra>",
        ),
        row=2, col=2,
    )
    fig.update_yaxes(title_text="P(Lift) %", row=2, col=2)

    fig.update_layout(
        height=900,
        title_text="Gen Z / Gen Alpha Cohort Maturity — Monte Carlo (10,000 paths, 2026–2041)",
        template="plotly_white",
    )
    fig.write_html(out_path, include_plotlyjs="cdn")


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    years = np.arange(START_YEAR, END_YEAR)
    _, _, cohort = cohort_weights(years.astype(float))

    print(f"Running {N_SIMS:,} simulations, {N_YEARS} years, {len(LOADINGS)} stocks, {len(FACTOR_NAMES)} factors...")
    factor_paths = simulate_factors(N_SIMS, N_YEARS)
    thematic = stock_thematic_returns(factor_paths, LOADINGS, cohort)

    rows = []
    all_cum = []
    tickers = sorted(thematic.keys())
    for ticker in tickers:
        cum = thematic[ticker]
        all_cum.append(cum)
        stats = classify_outcomes(cum)
        stats = {("median_cum_thematic" if k == "median_cum" else
                  "mean_cum_thematic" if k == "mean_cum" else k): v
                 for k, v in stats.items()}
        rows.append({"ticker": ticker, **stats})

    df = pd.DataFrame(rows)
    all_cum_arr = np.array(all_cum)

    # Relative rank: probability of finishing top-quartile vs bottom-quartile across sims
    ranks = np.argsort(np.argsort(all_cum_arr, axis=0), axis=0).astype(float)
    n = len(tickers)
    df["p_top_quartile"] = (ranks >= n * 0.75).mean(axis=1)
    df["p_bottom_quartile"] = (ranks < n * 0.25).mean(axis=1)

    # Merge company names
    names = {}
    for path in ["genz_alpha_stock_scores.csv", "novel_thesis_stocks.csv"]:
        p = os.path.join(DATA_DIR, path)
        if os.path.exists(p):
            sub = pd.read_csv(p)
            for _, r in sub.iterrows():
                names[r["ticker"]] = r.get("company", r["ticker"])

    df["company"] = df["ticker"].map(names).fillna(df["ticker"])
    df = df.sort_values("p_lift", ascending=False)
    df.to_csv(os.path.join(DATA_DIR, "monte_carlo_stock_results.csv"), index=False)

    # Factor path medians for reporting
    factor_cum = factor_paths.cumsum(axis=2)
    median_paths = {}
    for j, fname in enumerate(FACTOR_NAMES):
        median_paths[fname] = np.median(factor_cum[:, j, :], axis=0)
    factor_df = pd.DataFrame(median_paths, index=years)
    factor_df.to_csv(os.path.join(RESULTS_DIR, "monte_carlo_factor_paths.csv"))

    top_lift = df.head(15)[["ticker", "company", "p_lift", "p_crush", "median_cum_thematic"]].to_dict(orient="records")
    top_crush = df.nlargest(15, "p_crush")[["ticker", "company", "p_lift", "p_crush", "median_cum_thematic"]].to_dict(orient="records")

    summary = {
        "generated": datetime.now().astimezone().isoformat(),
        "methodology": {
            "n_simulations": N_SIMS,
            "horizon": f"{START_YEAR}–{END_YEAR}",
            "n_stocks": len(tickers),
            "n_factors": len(FACTOR_NAMES),
            "lift_definition": "Cumulative thematic alpha > 10% over horizon",
            "crush_definition": "Cumulative thematic alpha < -10% over horizon",
            "disclaimer": (
                "Thematic component only. Excludes valuation, rates, buybacks, "
                "M&A, and general market beta. Factor drifts are priors from survey "
                "research, not econometric estimates. 8% annual regime-flip probability."
            ),
        },
        "factor_priors": FACTORS,
        "cohort_model": "Logistic Gen Z peak ~2030, Gen Alpha peak ~2036; combined weight scales factor impact",
        "top_lift_candidates": df.head(15).to_dict(orient="records"),
        "top_crush_candidates": df.nlargest(15, "p_crush").to_dict(orient="records"),
        "highest_median_themetic_alpha": df.nlargest(10, "median_cum_thematic")[["ticker", "median_cum_thematic", "p_lift"]].to_dict(orient="records"),
        "lowest_median_themetic_alpha": df.nsmallest(10, "median_cum_thematic")[["ticker", "median_cum_thematic", "p_crush"]].to_dict(orient="records"),
    }
    with open(os.path.join(RESULTS_DIR, "monte_carlo_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    dash_path = os.path.join(MAPS_DIR, "monte_carlo_dashboard.html")
    build_dashboard(
        df,
        factor_df,
        df.head(10)["ticker"].tolist(),
        df.nlargest(10, "p_crush")["ticker"].tolist(),
        dash_path,
    )

    print(f"\nTop 5 P(Lift): {', '.join(df.head(5)['ticker'])}")
    print(f"Top 5 P(Crush): {', '.join(df.nlargest(5, 'p_crush')['ticker'])}")
    print(f"Wrote {os.path.join(DATA_DIR, 'monte_carlo_stock_results.csv')}")
    if HAS_PLOTLY:
        print(f"Dashboard: {dash_path}")


if __name__ == "__main__":
    main()
