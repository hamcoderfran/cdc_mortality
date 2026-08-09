"""
Thesis evaluation, step 1: Download public-market performance data
==================================================================

Pulls adjusted close prices for two thesis baskets and benchmarks via
Yahoo Finance (no API key):

  Hospital / acute-care operators:  HCA, THC, UHS, CYH, EHC, ACHC
  Experience-based consumer:        LYV, MTN, EXPE, BKNG, RCL, CCL,
                                    PLNT, MSGS, MANU, FUN, DKNG, DIS, NCLH
  Benchmarks:                       SPY, XLV (healthcare ETF), XLY (discretionary)

Outputs:
  ../data/stock_prices_daily.csv
  ../data/stock_performance_summary.csv
  ../data/stock_normalized_indices.csv
"""

import os
from datetime import datetime

import pandas as pd
import yfinance as yf

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

HOSPITAL = ["HCA", "THC", "UHS", "CYH", "EHC", "ACHC"]
EXPERIENCE = [
    "LYV", "MTN", "EXPE", "BKNG", "RCL", "CCL", "PLNT", "MSGS", "MANU",
    "FUN", "DKNG", "DIS", "NCLH",
]
BENCHMARKS = ["SPY", "XLV", "XLY"]

PERIODS = [
    ("2015-01-01", "2015_to_present"),
    ("2019-01-01", "2019_to_present"),
    ("2022-01-01", "2022_to_present"),
]


def performance_stats(prices: pd.DataFrame, start: str) -> pd.DataFrame:
    sub = prices.loc[start:].dropna(how="all")
    if sub.empty:
        return pd.DataFrame()
    norm = sub / sub.iloc[0] * 100
    years = (sub.index[-1] - sub.index[0]).days / 365.25
    rows = []
    for col in norm.columns:
        if norm[col].dropna().empty:
            continue
        last = norm[col].dropna().iloc[-1]
        total_ret = last / 100 - 1
        cagr = (1 + total_ret) ** (1 / years) - 1 if years > 0 else float("nan")
        rows.append(
            {
                "ticker": col,
                "start_date": str(sub.index[0].date()),
                "end_date": str(sub.index[-1].date()),
                "total_return_pct": round(total_ret * 100, 2),
                "cagr_pct": round(cagr * 100, 2),
                "normalized_end": round(last, 2),
            }
        )
    return pd.DataFrame(rows)


def basket_stats(prices: pd.DataFrame, tickers: list, label: str, start: str) -> dict:
    sub = prices.loc[start:, [t for t in tickers if t in prices.columns]].dropna(how="all")
    avail = [c for c in sub.columns if sub[c].notna().any()]
    if not avail:
        return {}
    norm = sub[avail] / sub[avail].iloc[0] * 100
    basket = norm.mean(axis=1)
    years = (sub.index[-1] - sub.index[0]).days / 365.25
    total_ret = basket.iloc[-1] / 100 - 1
    cagr = (1 + total_ret) ** (1 / years) - 1
    return {
        "basket": label,
        "period_start": str(sub.index[0].date()),
        "period_end": str(sub.index[-1].date()),
        "n_tickers": len(avail),
        "tickers": ",".join(avail),
        "total_return_pct": round(total_ret * 100, 2),
        "cagr_pct": round(cagr * 100, 2),
    }


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    all_tickers = sorted(set(HOSPITAL + EXPERIENCE + BENCHMARKS))
    raw = yf.download(all_tickers, start="2015-01-01", progress=False)["Close"]
    if isinstance(raw, pd.Series):
        raw = raw.to_frame()
    raw.index = pd.to_datetime(raw.index)
    raw.to_csv(os.path.join(DATA_DIR, "stock_prices_daily.csv"))
    print(f"Saved daily prices: {raw.shape}")

    norm_all = raw / raw.iloc[0] * 100
    norm_all.to_csv(os.path.join(DATA_DIR, "stock_normalized_indices.csv"))

    perf_rows = []
    basket_rows = []
    for start, label in PERIODS:
        stats = performance_stats(raw, start)
        stats["period_label"] = label
        perf_rows.append(stats)
        for basket_name, tickers in [("hospital", HOSPITAL), ("experience", EXPERIENCE)]:
            b = basket_stats(raw, tickers, f"{basket_name}_{label}", start)
            if b:
                basket_rows.append(b)

    perf = pd.concat(perf_rows, ignore_index=True)
    perf.to_csv(os.path.join(DATA_DIR, "stock_performance_summary.csv"), index=False)
    pd.DataFrame(basket_rows).to_csv(
        os.path.join(DATA_DIR, "basket_performance_summary.csv"), index=False
    )
    print(f"Wrote performance summaries -> {DATA_DIR}")


if __name__ == "__main__":
    main()
