"""
Thesis evaluation, step 3: Curate Gen Z / Gen Alpha behavioral trend data
=========================================================================

Documents survey-backed behavioral, social, economic, and cultural shifts
with source URLs. Used to score thematic stock baskets for 10–20 year outlook.

Outputs:
  ../data/genz_alpha_behavior_trends.csv
  ../data/genz_alpha_market_forecasts.csv
"""

import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

BEHAVIOR_TRENDS = [
    # Alcohol decline / sober curious
    {"theme": "alcohol_decline", "metric": "gen_z_plan_drink_less_2025_pct", "value": 65, "year": 2025, "source": "NCSolutions/Circana", "url": "https://www.circana.com/post/sober-curious-nation-alcohol-survey"},
    {"theme": "alcohol_decline", "metric": "gen_z_dry_lifestyle_all_year_2025_pct", "value": 39, "year": 2025, "source": "NCSolutions", "url": "https://www.bevindustry.com/articles/97226-new-ncsolutions-survey-shows-americans-plan-to-drink-less-in-2025"},
    {"theme": "alcohol_decline", "metric": "us_adults_under_35_who_drink_pct", "value": 50, "year": 2025, "source": "Gallup", "url": "https://extension.psu.edu/alcoholic-beverage-trends-2025"},
    {"theme": "alcohol_decline", "metric": "gen_z_drink_less_for_mental_health_pct", "value": 58, "year": 2025, "source": "Circana", "url": "https://www.circana.com/post/sober-curious-nation-alcohol-survey"},
    {"theme": "alcohol_decline", "metric": "gen_z_tried_non_alcoholic_spirits_pct", "value": 42, "year": 2024, "source": "Circana", "url": "https://www.circana.com/post/sober-curious-nation-alcohol-survey"},
    # AI skepticism
    {"theme": "ai_skepticism", "metric": "gen_z_weekly_genai_use_pct", "value": 51, "year": 2026, "source": "Gallup/Walton/GSV", "url": "https://news.gallup.com/poll/708224/gen-adoption-steady-skepticism-climbs.aspx"},
    {"theme": "ai_skepticism", "metric": "gen_z_anger_about_ai_pct", "value": 31, "year": 2026, "source": "Gallup/Walton/GSV", "url": "https://news.gallup.com/poll/708224/gen-adoption-steady-skepticism-climbs.aspx"},
    {"theme": "ai_skepticism", "metric": "gen_z_anxiety_about_ai_pct", "value": 42, "year": 2026, "source": "Gallup/Walton/GSV", "url": "https://news.gallup.com/poll/708224/gen-adoption-steady-skepticism-climbs.aspx"},
    {"theme": "ai_skepticism", "metric": "gen_z_ai_risks_outweigh_benefits_work_pct", "value": 48, "year": 2026, "source": "Walton/Gallup AI Paradox", "url": "https://nextgeninsights.waltonfamilyfoundation.org/wp-content/uploads/2026/04/The-AI-Paradox.pdf"},
    {"theme": "ai_skepticism", "metric": "gen_z_excitement_about_ai_pct", "value": 22, "year": 2026, "source": "Gallup", "url": "https://news.gallup.com/poll/708224/gen-adoption-steady-skepticism-climbs.aspx"},
    {"theme": "ai_skepticism", "metric": "gen_z_trust_human_only_work_over_ai_assisted_pct", "value": 67, "year": 2026, "source": "Walton/Gallup", "url": "https://nextgeninsights.waltonfamilyfoundation.org/wp-content/uploads/2026/04/The-AI-Paradox.pdf"},
    # Connection / IRL
    {"theme": "irl_connection", "metric": "gen_z_weekend_loneliness_pct", "value": 51, "year": 2026, "source": "Harris Poll", "url": "https://theharrispoll.com/wp-content/uploads/2026/07/The-Gen-Z-Weekend-Report-July-2026.pdf"},
    {"theme": "irl_connection", "metric": "gen_z_interested_irl_from_online_interests_pct", "value": 95, "year": 2025, "source": "Eventbrite", "url": "https://www.eventbrite.com/blog/wp-content/uploads/2025/01/Eventbrite-_-Fourth-Spaces-_-Jan.-2025.pdf"},
    {"theme": "irl_connection", "metric": "gen_z_attended_concert_past_year_pct", "value": 74, "year": 2024, "source": "Spotify Culture Next", "url": "https://wwd.com/business-news/business-features/spotify-culture-next-gen-z-in-person-experiences-1236673797/"},
    # Wellness / mental health
    {"theme": "wellness", "metric": "gen_z_millennial_share_of_us_wellness_spend_pct", "value": 41, "year": 2025, "source": "McKinsey Future of Wellness", "url": "https://www.mckinsey.com/industries/consumer-packaged-goods/our-insights/future-of-wellness-trends"},
    {"theme": "wellness", "metric": "gen_z_millennial_population_share_pct", "value": 36, "year": 2025, "source": "McKinsey", "url": "https://www.mckinsey.com/industries/consumer-packaged-goods/our-insights/future-of-wellness-trends"},
    {"theme": "wellness", "metric": "gen_z_mindfulness_very_high_priority_pct", "value": 42, "year": 2025, "source": "McKinsey", "url": "https://www.mckinsey.com/industries/consumer-packaged-goods/our-insights/future-of-wellness-trends"},
    {"theme": "wellness", "metric": "us_mental_health_market_2025_usd_b", "value": 33.44, "year": 2025, "source": "Industry estimates", "url": "https://www.gwi.com/blog/gen-z-spending-habits"},
    # Gen Alpha / spending power
    {"theme": "gen_alpha_spending", "metric": "gen_z_spending_power_2030_usd_t", "value": 12, "year": 2030, "source": "NIQ/World Data Lab", "url": "https://nielseniq.com/global/en/landing-page/spend-z/"},
    {"theme": "gen_alpha_spending", "metric": "gen_alpha_us_household_influence_usd_b", "value": 255, "year": 2026, "source": "Teneo", "url": "https://www.teneo.com/app/uploads/2026/01/Gen-Alpha-Consumer-Influence-Study.pdf"},
    {"theme": "gen_alpha_spending", "metric": "gen_alpha_style_most_important_purchase_criteria_pct", "value": 50, "year": 2026, "source": "Teneo", "url": "https://www.teneo.com/app/uploads/2026/01/Gen-Alpha-Consumer-Influence-Study.pdf"},
    # Value / thrift / authenticity
    {"theme": "value_authenticity", "metric": "gen_z_buy_secondhand_more_likely_vs_avg", "value": 8, "year": 2025, "source": "GWI", "note": "percentage points above average", "url": "https://www.gwi.com/blog/gen-z-spending-habits"},
    {"theme": "value_authenticity", "metric": "gen_z_plan_vintage_upcycled_holiday_pct", "value": 63, "year": 2025, "source": "PwC Holiday Outlook", "url": "https://www.pwc.com/us/en/industries/consumer-markets/library/gen-z-consumer-trends.html"},
    {"theme": "value_authenticity", "metric": "gen_z_willing_private_label_pct", "value": 41, "year": 2025, "source": "PwC", "url": "https://www.pwc.com/us/en/industries/consumer-markets/library/gen-z-consumer-trends.html"},
    # Gaming / digital-native
    {"theme": "gaming", "metric": "gen_z_purchased_in_game_item_more_likely_pct", "value": 36, "year": 2025, "source": "GWI", "note": "above average likelihood", "url": "https://www.gwi.com/blog/gen-z-spending-habits"},
    {"theme": "gaming", "metric": "gen_z_digital_game_purchase_more_likely_pct", "value": 33, "year": 2025, "source": "GWI", "url": "https://www.gwi.com/blog/gen-z-spending-habits"},
    # Tier A federal / scan data (added evidence audit)
    {"theme": "alcohol_decline", "metric": "young_adults_18_25_past_month_alcohol_pct", "value": 47.5, "year": 2024, "source": "SAMHSA NSDUH", "note": "Down from 50.9% in 2021", "url": "https://www.samhsa.gov/data/sites/default/files/reports/rpt56978/2024-nsduh-data-brief-young-adult.pdf"},
    {"theme": "alcohol_decline", "metric": "grade_12_past_year_alcohol_use_pct", "value": 41.7, "year": 2024, "source": "Monitoring the Future (NIH/NIDA)", "note": "Down from 75% in 1997", "url": "https://www.nih.gov/news-events/news-releases/reported-use-most-drugs-among-adolescents-remained-low-2024"},
    {"theme": "alcohol_decline", "metric": "us_beer_volume_change_pct_2024", "value": -2.9, "year": 2024, "source": "NIQ Beverage Alcohol Year in Review", "note": "52 weeks ending 12/28/2024", "url": "https://nielseniq.com/global/en/insights/analysis/2025/2024-beverage-alcohol-year-in-review/"},
    {"theme": "brand_affinity", "metric": "elf_num1_cosmetics_female_teens_pct", "value": 35, "year": 2024, "source": "Piper Sandler TSWT Fall 2024", "note": "Up 6pp YoY", "url": "https://www.pipersandler.com/sites/default/files/document/TSWT_Fall24_Infographic.pdf"},
    {"theme": "brand_affinity", "metric": "teens_prefer_energy_over_coffee_pct", "value": 39, "year": 2024, "source": "Piper Sandler TSWT Fall 2024", "note": "vs coffee 31% soda 30%; Monster #1 energy drink", "url": "https://www.pipersandler.com/sites/default/files/document/TSWT_Fall24_Infographic.pdf"},
    {"theme": "company_ops", "metric": "lyv_tickets_sold_through_july_2025", "value": 130_000_000, "year": 2025, "source": "Live Nation Q2 2025 8-K", "note": "Up 6% YoY", "url": "https://www.prnewswire.com/news-releases/live-nation-entertainment-reports-second-quarter-2025-results-302524774.html"},
    {"theme": "company_ops", "metric": "lyv_deferred_concert_revenue_q2_2025_usd_b", "value": 5.1, "year": 2025, "source": "Live Nation Q2 2025 8-K", "note": "Up 25% YoY", "url": "https://content.equisolve.net/livenationentertainment/sec/0001335258-25-000127/for_pdf/lyv-2025q2xex991er.htm"},
    {"theme": "company_ops", "metric": "rblx_age_checked_dau_under_13_pct", "value": 35, "year": 2026, "source": "Roblox shareholder letter", "note": "45% of DAUs age-checked as of Jan 2026", "url": "https://about.roblox.com/newsroom/2026/02/moving-beyond-self-reported-age"},
]

MARKET_FORECASTS = [
    {"sector": "rtd_mocktails", "market_2030_usd_b": 12.15, "cagr_pct": 5.7, "source": "Grand View Research", "url": "https://www.grandviewresearch.com/industry-analysis/ready-to-drink-mocktails-market-report"},
    {"sector": "non_alcoholic_spirits_mocktails", "market_2030_usd_b": 11.0, "cagr_pct": 7.2, "source": "Global Industry Analysts", "url": "https://www.giiresearch.com/report/go1794518-non-alcoholic-liquors-mocktails.html"},
    {"sector": "travel_experiences", "market_2025_usd_b": 271, "cagr_pct": 17, "source": "Arival/Phocuswright", "url": "https://www.traveldailynews.com/statistics-trends/travel-experiences-market-grows-despite-flat-spending/"},
    {"sector": "us_mental_health_services", "market_2030_usd_b": 50, "cagr_pct": 8.25, "source": "Industry composite", "url": "https://www.gwi.com/blog/gen-z-spending-habits"},
    {"sector": "global_wellness_economy", "market_2027_usd_b": 7.0, "cagr_pct": 8, "source": "Global Wellness Institute (historical)", "url": "https://www.mckinsey.com/industries/consumer-packaged-goods/our-insights/future-of-wellness-trends"},
]


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    pd.DataFrame(BEHAVIOR_TRENDS).to_csv(
        os.path.join(DATA_DIR, "genz_alpha_behavior_trends.csv"), index=False
    )
    pd.DataFrame(MARKET_FORECASTS).to_csv(
        os.path.join(DATA_DIR, "genz_alpha_market_forecasts.csv"), index=False
    )
    print(f"Wrote {len(BEHAVIOR_TRENDS)} behavior trends, {len(MARKET_FORECASTS)} market forecasts")


if __name__ == "__main__":
    main()
