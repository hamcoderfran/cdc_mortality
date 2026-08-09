"""
Thesis evaluation, step 4: Score Gen Z/Alpha-aligned thematic stocks
==================================================================

Downloads price history and assigns multi-factor scores (1–5) for each ticker
based on behavioral alignment, demographic tailwinds, and headwinds including
alcohol decline and AI skepticism.

Scoring dimensions (1=weak, 5=strong):
  - behavioral_fit: alignment with documented Gen Z/Alpha behaviors
  - demographic_tailwind: exposure to rising youth spending power 2026–2046
  - cultural_momentum: brand relevance / social currency with youth
  - alcohol_shift_benefit: benefits from sober-curious / NA beverage shift
  - ai_skepticism_benefit: benefits from preference for human/authentic over AI
  - competitive_moat_10yr: durable advantage over 10–20 years
  - execution_risk: inverse score — lower risk = higher number

Outputs:
  ../data/genz_alpha_stock_scores.csv
  ../data/genz_alpha_stock_prices.csv
  ../results/genz_alpha_rankings.json

Note: Composite scores are Tier C (analyst judgment). See EVIDENCE_AUDIT.md and
genz_alpha_stock_evidence.csv for per-ticker Tier A/B citations.
"""

import json
import os
from datetime import datetime

import pandas as pd
import yfinance as yf

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")

# (ticker, company, theme, scores dict, rationale)
STOCK_SCORES = [
    # THEME: Non-alcoholic / functional beverages
    ("MNST", "Monster Beverage", "na_functional_beverages",
     {"behavioral_fit": 5, "demographic_tailwind": 4, "cultural_momentum": 5, "alcohol_shift_benefit": 4, "ai_skepticism_benefit": 2, "competitive_moat_10yr": 4, "execution_risk": 4},
     "Energy drinks substitute for alcohol in social settings; top Gen Z beverage brand affinity"),
    ("KDP", "Keurig Dr Pepper", "na_functional_beverages",
     {"behavioral_fit": 4, "demographic_tailwind": 4, "cultural_momentum": 3, "alcohol_shift_benefit": 5, "ai_skepticism_benefit": 2, "competitive_moat_10yr": 3, "execution_risk": 4},
     "Owns NA RTD portfolio; mocktail/functional drink distribution scale"),
    ("PEP", "PepsiCo", "na_functional_beverages",
     {"behavioral_fit": 4, "demographic_tailwind": 4, "cultural_momentum": 4, "alcohol_shift_benefit": 4, "ai_skepticism_benefit": 2, "competitive_moat_10yr": 4, "execution_risk": 4},
     "Gatorade, bubly, NA extensions; snack + beverage Gen Z reach"),
    ("CELH", "Celsius Holdings", "na_functional_beverages",
     {"behavioral_fit": 5, "demographic_tailwind": 4, "cultural_momentum": 5, "alcohol_shift_benefit": 4, "ai_skepticism_benefit": 2, "competitive_moat_10yr": 3, "execution_risk": 3},
     "Fitness-forward functional drinks; wellness + social replacement for drinking"),
    # THEME: Alcohol headwinds (included for contrast — lower composite = avoid)
    ("STZ", "Constellation Brands", "alcohol_headwind",
     {"behavioral_fit": 2, "demographic_tailwind": 2, "cultural_momentum": 2, "alcohol_shift_benefit": 1, "ai_skepticism_benefit": 2, "competitive_moat_10yr": 3, "execution_risk": 3},
     "Beer/spirits portfolio faces Gen Z volume decline; NA pivot partial"),
    ("TAP", "Molson Coors", "alcohol_headwind",
     {"behavioral_fit": 2, "demographic_tailwind": 2, "cultural_momentum": 2, "alcohol_shift_benefit": 1, "ai_skepticism_benefit": 2, "competitive_moat_10yr": 2, "execution_risk": 3},
     "Core beer portfolio structurally challenged by sober-curious cohort"),
    ("BUD", "Anheuser-Busch InBev", "alcohol_headwind",
     {"behavioral_fit": 2, "demographic_tailwind": 2, "cultural_momentum": 2, "alcohol_shift_benefit": 1, "ai_skepticism_benefit": 2, "competitive_moat_10yr": 3, "execution_risk": 3},
     "Global beer giant with Gen Z relevance risk; NA investments lag sentiment shift"),
    # THEME: Human connection / IRL experiences
    ("LYV", "Live Nation", "irl_experiences",
     {"behavioral_fit": 5, "demographic_tailwind": 5, "cultural_momentum": 5, "alcohol_shift_benefit": 3, "ai_skepticism_benefit": 5, "competitive_moat_10yr": 4, "execution_risk": 3},
     "Irreplaceable human live performance; AI cannot replicate stadium experience; antitrust risk"),
    ("PLNT", "Planet Fitness", "irl_wellness_social",
     {"behavioral_fit": 5, "demographic_tailwind": 4, "cultural_momentum": 4, "alcohol_shift_benefit": 4, "ai_skepticism_benefit": 5, "competitive_moat_10yr": 3, "execution_risk": 3},
     "Low-cost 'third space' for Gen Z wellness socializing; Harris: 65% feel more connected in wellness settings"),
    ("LULU", "Lululemon", "irl_wellness_social",
     {"behavioral_fit": 4, "demographic_tailwind": 4, "cultural_momentum": 5, "alcohol_shift_benefit": 3, "ai_skepticism_benefit": 4, "competitive_moat_10yr": 4, "execution_risk": 3},
     "Community-run clubs + premium wellness identity with Gen Z female skew"),
    ("ONON", "On Holding", "irl_wellness_social",
     {"behavioral_fit": 4, "demographic_tailwind": 4, "cultural_momentum": 5, "alcohol_shift_benefit": 3, "ai_skepticism_benefit": 4, "competitive_moat_10yr": 3, "execution_risk": 3},
     "Running club culture; Gen Z fitness-as-social"),
    # THEME: AI skepticism beneficiaries
    ("CRWD", "CrowdStrike", "ai_skepticism_security",
     {"behavioral_fit": 3, "demographic_tailwind": 4, "cultural_momentum": 3, "alcohol_shift_benefit": 1, "ai_skepticism_benefit": 5, "competitive_moat_10yr": 4, "execution_risk": 3},
     "AI proliferation increases cyberattack surface; distrust drives security spend"),
    ("PANW", "Palo Alto Networks", "ai_skepticism_security",
     {"behavioral_fit": 3, "demographic_tailwind": 4, "cultural_momentum": 3, "alcohol_shift_benefit": 1, "ai_skepticism_benefit": 5, "competitive_moat_10yr": 4, "execution_risk": 3},
     "Enterprise + consumer privacy/security infrastructure"),
    ("DUOL", "Duolingo", "human_skills_authentic",
     {"behavioral_fit": 4, "demographic_tailwind": 5, "cultural_momentum": 5, "alcohol_shift_benefit": 1, "ai_skepticism_benefit": 4, "competitive_moat_10yr": 4, "execution_risk": 3},
     "Human skill acquisition; Gen Z distrusts AI for learning but uses gamified human-centric apps"),
    # THEME: Mental health / behavioral services
    ("ACHC", "Acadia Healthcare", "mental_health_services",
     {"behavioral_fit": 4, "demographic_tailwind": 5, "cultural_momentum": 3, "alcohol_shift_benefit": 2, "ai_skepticism_benefit": 4, "competitive_moat_10yr": 3, "execution_risk": 3},
     "Behavioral health facilities; youth MH crisis drives demand for in-person care"),
    ("HIMS", "Hims & Hers", "mental_health_services",
     {"behavioral_fit": 4, "demographic_tailwind": 5, "cultural_momentum": 4, "alcohol_shift_benefit": 2, "ai_skepticism_benefit": 3, "competitive_moat_10yr": 3, "execution_risk": 2},
     "Telehealth mental health + wellness; Gen Z-native brand but AI-adjacent risk"),
    # THEME: Value / thrift / resale
    ("ROST", "Ross Stores", "value_thrift",
     {"behavioral_fit": 4, "demographic_tailwind": 4, "cultural_momentum": 3, "alcohol_shift_benefit": 1, "ai_skepticism_benefit": 3, "competitive_moat_10yr": 4, "execution_risk": 4},
     "Off-price retail aligns with Gen Z dupes/thrift; 63% plan vintage/upcycled"),
    ("TJX", "TJX Companies", "value_thrift",
     {"behavioral_fit": 4, "demographic_tailwind": 4, "cultural_momentum": 3, "alcohol_shift_benefit": 1, "ai_skepticism_benefit": 3, "competitive_moat_10yr": 5, "execution_risk": 4},
     "TJX/TK Maxx; treasure-hunt shopping Gen Z over-indexes"),
    ("ETSY", "Etsy", "value_thrift",
     {"behavioral_fit": 5, "demographic_tailwind": 4, "cultural_momentum": 4, "alcohol_shift_benefit": 1, "ai_skepticism_benefit": 5, "competitive_moat_10yr": 3, "execution_risk": 3},
     "Handmade/authentic; anti-mass-production; human creator economy"),
    # THEME: Gaming / digital-native (paradox: digital but Gen Z core)
    ("RBLX", "Roblox", "gaming_gen_alpha",
     {"behavioral_fit": 5, "demographic_tailwind": 5, "cultural_momentum": 5, "alcohol_shift_benefit": 1, "ai_skepticism_benefit": 2, "competitive_moat_10yr": 4, "execution_risk": 3},
     "Gen Alpha primary platform; social gaming; AI content risk on platform"),
    ("TTWO", "Take-Two Interactive", "gaming_gen_alpha",
     {"behavioral_fit": 4, "demographic_tailwind": 4, "cultural_momentum": 4, "alcohol_shift_benefit": 1, "ai_skepticism_benefit": 2, "competitive_moat_10yr": 4, "execution_risk": 3},
     "GTA/F2P; Gen Z in-game spending 36% above average"),
    # THEME: Clean beauty / Gen Z consumer
    ("ELF", "e.l.f. Beauty", "clean_beauty_value",
     {"behavioral_fit": 5, "demographic_tailwind": 5, "cultural_momentum": 5, "alcohol_shift_benefit": 1, "ai_skepticism_benefit": 4, "competitive_moat_10yr": 3, "execution_risk": 3},
     "Affordable affluence; viral TikTok brand; Gen Z over-indexed"),
    # THEME: Travel / event-driven
    ("EXPE", "Expedia Group", "event_travel",
     {"behavioral_fit": 4, "demographic_tailwind": 4, "cultural_momentum": 3, "alcohol_shift_benefit": 2, "ai_skepticism_benefit": 3, "competitive_moat_10yr": 3, "execution_risk": 3},
     "Event-driven travel booking; experiences attach rate growing"),
    ("BKNG", "Booking Holdings", "event_travel",
     {"behavioral_fit": 4, "demographic_tailwind": 4, "cultural_momentum": 3, "alcohol_shift_benefit": 2, "ai_skepticism_benefit": 3, "competitive_moat_10yr": 5, "execution_risk": 4},
     "Experiences segment; global travel for concerts/events"),
    # THEME: AI infrastructure (headwind from skepticism but adoption continues)
    ("NVDA", "NVIDIA", "ai_infrastructure_paradox",
     {"behavioral_fit": 3, "demographic_tailwind": 4, "cultural_momentum": 4, "alcohol_shift_benefit": 1, "ai_skepticism_benefit": 1, "competitive_moat_10yr": 5, "execution_risk": 3},
     "Gen Z uses AI but resents it; infra layer wins regardless of sentiment"),
    ("GOOGL", "Alphabet", "ai_platform_paradox",
     {"behavioral_fit": 3, "demographic_tailwind": 4, "cultural_momentum": 4, "alcohol_shift_benefit": 1, "ai_skepticism_benefit": 1, "competitive_moat_10yr": 5, "execution_risk": 3},
     "AI-native tools + YouTube creator economy; Gen Z anger at AI poses reputational risk"),
    # THEME: Sober venues / NA spirits pure-play (smaller)
    ("SAM", "Boston Beer", "na_pivot_alcohol",
     {"behavioral_fit": 3, "demographic_tailwind": 3, "cultural_momentum": 3, "alcohol_shift_benefit": 3, "ai_skepticism_benefit": 2, "competitive_moat_10yr": 3, "execution_risk": 3},
     "Twisted Tea/Hard seltzer + NA experiments; transitional play"),
    ("VST", "Vista Outdoor / Revelyst", "outdoor_authentic",
     {"behavioral_fit": 3, "demographic_tailwind": 3, "cultural_momentum": 3, "alcohol_shift_benefit": 2, "ai_skepticism_benefit": 4, "competitive_moat_10yr": 3, "execution_risk": 2},
     "Outdoor recreation; authentic physical activity (note: corporate changes)"),
]

SCORE_WEIGHTS = {
    "behavioral_fit": 0.20,
    "demographic_tailwind": 0.15,
    "cultural_momentum": 0.15,
    "alcohol_shift_benefit": 0.10,
    "ai_skepticism_benefit": 0.15,
    "competitive_moat_10yr": 0.15,
    "execution_risk": 0.10,
}


def composite_score(scores: dict) -> float:
    return round(sum(scores[k] * SCORE_WEIGHTS[k] for k in SCORE_WEIGHTS) * 20, 1)  # scale to 100


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    rows = []
    tickers = [s[0] for s in STOCK_SCORES]
    prices = yf.download(tickers, start="2019-01-01", progress=False)["Close"]
    if isinstance(prices, pd.Series):
        prices = prices.to_frame()
    prices.to_csv(os.path.join(DATA_DIR, "genz_alpha_stock_prices.csv"))

    years = (prices.index[-1] - prices.index[0]).days / 365.25
    for ticker, company, theme, scores, rationale in STOCK_SCORES:
        comp = composite_score(scores)
        hist_cagr = None
        if ticker in prices.columns and prices[ticker].dropna().shape[0] > 10:
            s = prices[ticker].dropna()
            tr = s.iloc[-1] / s.iloc[0] - 1
            hist_cagr = round(((1 + tr) ** (1 / years) - 1) * 100, 2)
        row = {
            "ticker": ticker,
            "company": company,
            "theme": theme,
            "composite_score_100": comp,
            "rationale": rationale,
            "historical_cagr_2019_pct": hist_cagr,
            **scores,
        }
        rows.append(row)

    df = pd.DataFrame(rows).sort_values("composite_score_100", ascending=False)
    df.to_csv(os.path.join(DATA_DIR, "genz_alpha_stock_scores.csv"), index=False)

    top = df.head(15)[["ticker", "company", "theme", "composite_score_100", "rationale"]].to_dict(orient="records")
    bottom = df.tail(5)[["ticker", "company", "theme", "composite_score_100"]].to_dict(orient="records")
    by_theme = df.groupby("theme")["composite_score_100"].mean().sort_values(ascending=False).round(1).to_dict()

    out = {
        "generated": datetime.now().astimezone().isoformat(),
        "methodology": "Weighted 7-factor scoring (1-5) for Gen Z/Alpha 10-20yr alignment",
        "top_15_stocks": top,
        "bottom_5_stocks": bottom,
        "avg_score_by_theme": by_theme,
        "score_weights": SCORE_WEIGHTS,
    }
    with open(os.path.join(RESULTS_DIR, "genz_alpha_rankings.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"Scored {len(df)} tickers. Top: {df.iloc[0]['ticker']} ({df.iloc[0]['composite_score_100']})")


if __name__ == "__main__":
    main()
