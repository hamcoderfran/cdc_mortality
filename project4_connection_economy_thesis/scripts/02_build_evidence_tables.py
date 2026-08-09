"""
Thesis evaluation, step 2: Curate survey, macro, and sector evidence tables
===========================================================================

Compiles documented statistics from public reports (with source URLs) and
merges with stock performance outputs from step 1.

Outputs:
  ../data/youth_connection_surveys.csv
  ../data/healthcare_utilization_forecasts.csv
  ../data/experience_economy_indicators.csv
  ../results/thesis_evidence_summary.json
"""

import json
import os

import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")

YOUTH_SURVEYS = [
    {
        "source": "Harris Poll Gen Z Weekend Report",
        "year": 2026,
        "sample": "4,100 US adults 18+",
        "metric": "gen_z_weekend_loneliness_pct",
        "value": 51,
        "url": "https://theharrispoll.com/wp-content/uploads/2026/07/The-Gen-Z-Weekend-Report-July-2026.pdf",
    },
    {
        "source": "Harris Poll Gen Z Weekend Report",
        "year": 2026,
        "metric": "gen_z_social_life_more_through_phone_pct",
        "value": 65,
        "url": "https://theharrispoll.com/wp-content/uploads/2026/07/The-Gen-Z-Weekend-Report-July-2026.pdf",
    },
    {
        "source": "Harris Poll Gen Z Weekend Report",
        "year": 2026,
        "metric": "gen_z_wish_online_friendships_became_irl_pct",
        "value": 62,
        "url": "https://theharrispoll.com/wp-content/uploads/2026/07/The-Gen-Z-Weekend-Report-July-2026.pdf",
    },
    {
        "source": "Spotify Culture Next",
        "year": 2024,
        "sample": "7,700 Gen Z/Millennials globally",
        "metric": "gen_z_lonelier_than_10_years_ago_pct",
        "value": 61,
        "url": "https://wwd.com/business-news/business-features/spotify-culture-next-gen-z-in-person-experiences-1236673797/",
    },
    {
        "source": "Spotify Culture Next",
        "year": 2024,
        "metric": "gen_z_attended_concert_live_show_past_year_pct",
        "value": 74,
        "url": "https://wwd.com/business-news/business-features/spotify-culture-next-gen-z-in-person-experiences-1236673797/",
    },
    {
        "source": "Eventbrite Fourth Spaces Report",
        "year": 2025,
        "sample": "2,000 US adults 18-35",
        "metric": "interested_in_irl_events_from_online_interests_pct",
        "value": 95,
        "url": "https://www.eventbrite.com/blog/wp-content/uploads/2025/01/Eventbrite-_-Fourth-Spaces-_-Jan.-2025.pdf",
    },
    {
        "source": "Eventbrite Fourth Spaces Report",
        "year": 2025,
        "metric": "plan_to_attend_live_events_next_6mo_pct",
        "value": 73,
        "url": "https://www.businesswire.com/news/home/20250128081264/en/",
    },
    {
        "source": "Eventbrite Fourth Spaces Report",
        "year": 2025,
        "metric": "formed_close_friend_through_interest_event_pct",
        "value": 84,
        "url": "https://www.businesswire.com/news/home/20250128081264/en/",
    },
    {
        "source": "Arival Event-Driven Traveler",
        "year": 2024,
        "sample": "2,400 US/EU event travelers",
        "metric": "us_18_34_event_major_destination_factor_pct",
        "value": 48,
        "url": "https://www.eventindustrynews.com/news/events-are-the-new-anchor-for-travel-arival-report-reveals-young-travelers-are-planning-trips-around-concerts-matches-and-performances",
    },
    {
        "source": "Bank of America Summer Travel Survey",
        "year": 2025,
        "metric": "gen_z_traveled_for_concert_event_past_2yr_pct",
        "value": 67,
        "url": "https://www.emarketer.com/content/2025-will-record-year-concertgoing",
    },
]

HEALTHCARE_FORECASTS = [
    {
        "source": "Sg2/Vizient Impact of Change 2025",
        "metric": "inpatient_discharge_growth_10yr_pct",
        "value": 5,
        "url": "https://www.vizientinc.com/newsroom/news-releases/2025/sg2-forecasts-18-percent-growth-in-outpatient-care-5-percent-inpatient-care",
    },
    {
        "source": "Sg2/Vizient Impact of Change 2025",
        "metric": "outpatient_volume_growth_10yr_pct",
        "value": 18,
        "url": "https://www.vizientinc.com/newsroom/news-releases/2025/sg2-forecasts-18-percent-growth-in-outpatient-care-5-percent-inpatient-care",
    },
    {
        "source": "Sg2/Vizient Impact of Change 2025",
        "metric": "post_acute_care_growth_10yr_pct",
        "value": 31,
        "url": "https://www.vizientinc.com/newsroom/news-releases/2025/sg2-forecasts-18-percent-growth-in-outpatient-care-5-percent-inpatient-care",
    },
    {
        "source": "Sg2/Vizient Impact of Change 2025",
        "metric": "population_65_plus_growth_10yr_pct",
        "value": 32,
        "url": "https://www.sg2.com/blog/2025/impact-of-change-service-line-insights",
    },
    {
        "source": "CMS/NHE Projections",
        "metric": "nhe_avg_annual_growth_through_2033_pct",
        "value": 5.8,
        "url": "https://www.cms.gov/data-research/projections",
    },
    {
        "source": "CDC MMWR adolescent ED visits",
        "year": 2023,
        "metric": "adolescent_drug_overdose_ed_vs_2019_baseline_vr",
        "value": 1.10,
        "note": "Fall 2022 visit ratio vs 2019 prepandemic baseline (higher)",
        "url": "https://www.cdc.gov/mmwr/volumes/72/wr/mm7219a1.htm",
    },
]

EXPERIENCE_ECONOMY = [
    {
        "source": "Arival/Phocuswright",
        "year": 2025,
        "metric": "global_travel_experiences_market_usd_b",
        "value": 271,
        "url": "https://www.traveldailynews.com/statistics-trends/travel-experiences-market-grows-despite-flat-spending/",
    },
    {
        "source": "Arival/Phocuswright",
        "year": 2025,
        "metric": "travel_experiences_yoy_growth_pct",
        "value": 17,
        "url": "https://www.traveldailynews.com/statistics-trends/travel-experiences-market-grows-despite-flat-spending/",
    },
    {
        "source": "Arival/Phocuswright",
        "year": 2025,
        "metric": "experiences_booked_online_pct",
        "value": 33,
        "url": "https://www.traveldailynews.com/statistics-trends/travel-experiences-market-grows-despite-flat-spending/",
    },
    {
        "source": "Arival/Phocuswright",
        "year": 2029,
        "metric": "projected_travel_experiences_market_usd_b",
        "value": 342,
        "url": "https://www.traveldailynews.com/statistics-trends/travel-experiences-market-grows-despite-flat-spending/",
    },
    {
        "source": "Live Nation",
        "year": 2025,
        "metric": "tickets_sold_ytd_july_millions",
        "value": 130,
        "note": "Up 6% YoY, company record",
        "url": "https://www.emarketer.com/content/2025-will-record-year-concertgoing",
    },
]


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    pd.DataFrame(YOUTH_SURVEYS).to_csv(
        os.path.join(DATA_DIR, "youth_connection_surveys.csv"), index=False
    )
    pd.DataFrame(HEALTHCARE_FORECASTS).to_csv(
        os.path.join(DATA_DIR, "healthcare_utilization_forecasts.csv"), index=False
    )
    pd.DataFrame(EXPERIENCE_ECONOMY).to_csv(
        os.path.join(DATA_DIR, "experience_economy_indicators.csv"), index=False
    )

    basket_path = os.path.join(DATA_DIR, "basket_performance_summary.csv")
    summary = {
        "thesis": (
            "Hospital and experience-based stocks will rise as youth pursue "
            "real connections and in-person fulfillment"
        ),
        "youth_connection_evidence_count": len(YOUTH_SURVEYS),
        "healthcare_forecast_rows": len(HEALTHCARE_FORECASTS),
        "experience_economy_rows": len(EXPERIENCE_ECONOMY),
    }
    if os.path.exists(basket_path):
        baskets = pd.read_csv(basket_path)
        summary["basket_performance"] = baskets.to_dict(orient="records")

    with open(os.path.join(RESULTS_DIR, "thesis_evidence_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print("Wrote evidence tables and thesis_evidence_summary.json")


if __name__ == "__main__":
    main()
