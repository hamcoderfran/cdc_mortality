"""
Thesis evaluation, step 6: Novel Gen Z/Alpha theses — new stocks, new angles
============================================================================

Builds CSV of underexplored behavioral signals and scores 18 NEW tickers
not in the original Gen Z/Alpha 28-stock basket.

Outputs:
  ../data/novel_thesis_signals.csv  (curated in repo)
  ../data/novel_thesis_stocks.csv
  ../results/novel_thesis_rankings.json
"""

import json
import os
from datetime import datetime

import pandas as pd
import yfinance as yf

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")

# (ticker, company, thesis_id, thesis_name, conviction, evidence_tier, rationale, source_url)
NOVEL_STOCKS = [
    # Thesis 1: Sober Social / Competitive Eatertainment
    ("PLAY", "Dave & Buster's", "sober_social_lbe",
     "The Bar Replacement Thesis",
     "Medium-High", "B",
     "243 NA venues; pivoting to D&B Unlocked ticketed sober nightlife, Store of Future competitive social suites; Harris 73% want alcohol-optional settings",
     "https://theharrispoll.com/wp-content/uploads/2026/07/The-Gen-Z-Weekend-Report-July-2026.pdf"),
    ("MODG", "Topgolf Callaway Brands", "sober_social_lbe",
     "The Bar Replacement Thesis",
     "Medium", "A",
     "Pure-play competitive socializing venue (~$1.8B revenue); Q3 2025 consumer bay SSS +2.4%; pending Topgolf spin-off; ranked #1 fun/atmosphere",
     "https://www.prnewswire.com/news-releases/topgolf-callaway-brands-announces-third-quarter-2025-results-302607773.html"),
    ("FUN", "Six Flags Entertainment", "sober_social_lbe",
     "The Bar Replacement Thesis",
     "Medium", "B",
     "Daytime/summer social destination; Gen Z 54% prefer daytime; Morning Consult -36% clubbing; affordable group outing vs bars",
     "https://www.whitehutchinson.com/news/lenews/2025/september/article105.shtml"),
    # Thesis 2: Pet-as-Family Connection
    ("TRUP", "Trupanion", "pet_connection_economy",
     "The Pet Parent Proxy Thesis",
     "High", "A",
     "1.09M enrolled pets Q4 2025; Chewy partnership; ~70% new pet insurance buyers under 40; Gen Z treats pets as family/pre-parenthood connection",
     "https://www.nasdaq.com/press-release/trupanion-reports-fourth-quarter-full-year-2025-results-2026-02-12"),
    ("CHWY", "Chewy", "pet_connection_economy",
     "The Pet Parent Proxy Thesis",
     "Medium-High", "B",
     "Gen Z 71% vet visits few times/year; premium food, pet sports (30%), parties (24%); digital-native pet parent platform",
     "https://www.rover.com/blog/pet-parenting-trends/"),
    ("IDXX", "Idexx Laboratories", "pet_connection_economy",
     "The Pet Parent Proxy Thesis",
     "Medium", "B",
     "Veterinary diagnostics tailwind from younger cohorts' proactive pet healthcare spending; APPA 94M US pet households",
     "https://insurnest.com/blog/millennial-gen-z-pet-insurance-mga-revenue/"),
    ("ELAN", "Elanco Animal Health", "pet_connection_economy",
     "The Pet Parent Proxy Thesis",
     "Medium", "C",
     "Pet pharma/wellness beneficiary of humanization trend; less direct Gen Z brand proof than TRUP/CHWY",
     ""),
    # Thesis 3: Swipe Fatigue / IRL Dating Infrastructure
    ("MTCH", "Match Group", "swipe_fatigue_pivot",
     "The Anti-Swipe Turnaround (Contrarian)",
     "Medium (high risk)", "A",
     "CONTRARIAN: 79% Gen Z app burnout; 8 quarters paying user declines; Tinder expanding IRL events to 75 cities — pivot or value trap",
     "https://techcrunch.com/2026/08/05/as-gen-z-reconsiders-dating-apps-tinders-irl-events-expand-to-dozens-more-cities/"),
    ("BMBL", "Bumble", "swipe_fatigue_pivot",
     "The Anti-Swipe Turnaround (Contrarian)",
     "Low-Medium", "B",
     "Paying users -16% YoY Q3 2025; Gen Z uncomfortable with AI dating features; friendship/dating app pivot unproven",
     "https://www.thestar.com.my/tech/tech-news/2025/07/15/ai-dating-appfeatures-arent-landing-with-gen-z-new-survey-finds"),
    ("AFRM", "Affirm", "swipe_fatigue_pivot",
     "The Anti-Swipe Turnaround (Contrarian)",
     "Medium", "B",
     "BNPL for experiences — 31% Gen Z used BNPL for concert tickets; enables IRL social when cash-constrained (Harris 85% use cost workarounds)",
     "https://www.emarketer.com/content/2025-will-record-year-concertgoing"),
    # Thesis 4: Analog / Tactile Connection Economy
    ("WMG", "Warner Music Group", "analog_tactile_economy",
     "The Analog Connection Thesis",
     "Medium-High", "A",
     "Vinyl $1.04B US revenue 2025 (+9.3%); Gen Z driving format; 76% buy monthly; 84% shop in-store for community",
     "https://www.billboard.com/pro/riaa-2025-music-report-revenue-streaming-vinyl/"),
    ("SONY", "Sony Group", "analog_tactile_economy",
     "The Analog Connection Thesis",
     "Medium", "A",
     "Music + gaming + imaging (cameras for analog-bag trend); RIAA physical revenue growth; diversified analog-digital paradox play",
     "https://www.billboard.com/pro/riaa-2025-music-report-revenue-streaming-vinyl/"),
    ("HAS", "Hasbro", "analog_tactile_economy",
     "The Analog Connection Thesis",
     "Medium-High", "B",
     "Board game renaissance; 82% Gen Z want IRL self-expression; Playing to Win strategy aging up to 750M fans; D&D/MTG social tabletop",
     "https://newsroom.hasbro.com/node/35406/pdf"),
    # Thesis 5: Sleep Maxxing / Nightlife Exit
    ("TPX", "Tempur Sealy International", "sleep_maxxing",
     "The Sleep Over Nightlife Thesis",
     "Medium", "B",
     "Gen Z 55.9% guilt after disruptive nights; 43% prefer fitness over nightlife; sleep as identity (#earlynight TikTok); mattress/sleep products",
     "https://www.origym.co.uk/blog/why-gen-z-choose-wellness-over-nights-out/"),
    ("RMD", "ResMed", "sleep_maxxing",
     "The Sleep Over Nightlife Thesis",
     "Medium", "B",
     "Sleep health prioritization; wellness-over-nightlife shift; CPAP/sleep tech for health-conscious young adults (longer-term demographic)",
     "https://www.whitehutchinson.com/news/lenews/2025/september/article105.shtml"),
    # Thesis 6: Home-as-Social-Hub
    ("WING", "Wingstop", "home_social_hub",
     "The Home Social Hub Thesis",
     "Medium", "B",
     "Harris 74% staying in, 48% hosting friends; delivery/wings as home-gathering fuel; Gen Z allocates spend to hosting vs bars",
     "https://theharrispoll.com/wp-content/uploads/2026/07/The-Gen-Z-Weekend-Report-July-2026.pdf"),
    ("DPZ", "Domino's Pizza", "home_social_hub",
     "The Home Social Hub Thesis",
     "Medium", "B",
     "Same home-gathering thesis; affordable group food for house hangouts vs $200 dates (Fortune solo-maxxing trend)",
     "https://fortune.com/2026/05/30/why-does-gen-z-not-like-to-date-solo-maxxing-dates-too-expensive-emotionally-draining/"),
    ("NFLX", "Netflix", "home_social_hub",
     "The Home Social Hub Thesis",
     "Medium", "C",
     "71% Gen Z weekend = watching TV/streaming (Harris); shared watch culture at home; co-viewing as low-cost social",
     "https://theharrispoll.com/wp-content/uploads/2026/07/The-Gen-Z-Weekend-Report-July-2026.pdf"),
    # Thesis 7: Young Men Community Seeking (novel demographic split)
    ("SIX", "Six Flags (legacy ticker check)", "young_men_community",
     "The Young Men Community Thesis",
     "Low", "C",
     "Placeholder — see GME/social clubs; Gallup young men 40% monthly religious attendance suggests community-seeking; weak public equity mapping",
     "https://news.gallup.com/poll/708410/rise-young-men-religiosity-realigns-gender-gaps.aspx"),
]

# Remove SIX if delisted - use alternative
NOVEL_STOCKS = [s for s in NOVEL_STOCKS if s[0] != "SIX"]

# Add PINS as hobby inspiration / IRL meetup planning
NOVEL_STOCKS.append(
    ("PINS", "Pinterest", "analog_tactile_economy",
     "The Analog Connection Thesis",
     "Medium", "B",
     "Grandmacore/craft/DIY inspiration platform; Gen Z 54% spend on hobby/class/creative; bridges digital discovery to IRL making",
     "https://theharrispoll.com/wp-content/uploads/2026/07/The-Gen-Z-Weekend-Report-July-2026.pdf")
)


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    rows = []
    tickers = [s[0] for s in NOVEL_STOCKS]
    try:
        prices = yf.download(tickers, start="2019-01-01", progress=False)["Close"]
        if isinstance(prices, pd.Series):
            prices = prices.to_frame()
    except Exception:
        prices = pd.DataFrame()

    years = 7.0
    if not prices.empty and len(prices) > 1:
        years = (prices.index[-1] - prices.index[0]).days / 365.25

    for ticker, company, thesis_id, thesis_name, conviction, tier, rationale, url in NOVEL_STOCKS:
        hist_cagr = None
        if not prices.empty and ticker in prices.columns:
            s = prices[ticker].dropna()
            if len(s) > 10:
                tr = s.iloc[-1] / s.iloc[0] - 1
                hist_cagr = round(((1 + tr) ** (1 / years) - 1) * 100, 2)
        rows.append({
            "ticker": ticker,
            "company": company,
            "thesis_id": thesis_id,
            "thesis_name": thesis_name,
            "conviction": conviction,
            "evidence_tier": tier,
            "rationale": rationale,
            "source_url": url,
            "historical_cagr_2019_pct": hist_cagr,
            "in_original_28_basket": False,
        })

    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(DATA_DIR, "novel_thesis_stocks.csv"), index=False)

    by_thesis = {}
    for tid, grp in df.groupby("thesis_id"):
        by_thesis[tid] = {
            "thesis_name": grp.iloc[0]["thesis_name"],
            "tickers": grp["ticker"].tolist(),
            "avg_cagr": round(grp["historical_cagr_2019_pct"].dropna().mean(), 2) if grp["historical_cagr_2019_pct"].notna().any() else None,
        }

    out = {
        "generated": datetime.now().astimezone().isoformat(),
        "description": "18 novel tickers across 6 theses — not in original Gen Z 28-stock basket",
        "theses": by_thesis,
        "top_conviction_picks": df[df["conviction"].str.contains("High", na=False)][["ticker", "thesis_name", "evidence_tier"]].to_dict(orient="records"),
        "contrarian_picks": df[df["thesis_id"] == "swipe_fatigue_pivot"][["ticker", "conviction", "rationale"]].to_dict(orient="records"),
    }
    with open(os.path.join(RESULTS_DIR, "novel_thesis_rankings.json"), "w") as f:
        json.dump(out, f, indent=2)

    print(f"Novel thesis stocks: {len(df)} tickers, {df['thesis_id'].nunique()} theses")


if __name__ == "__main__":
    main()
