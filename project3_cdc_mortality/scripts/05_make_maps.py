"""
Project 3, step 5: Interactive county-level choropleth maps
===============================================================

Builds standalone interactive HTML choropleth maps (Plotly) for each of the
6 mortality/health outcomes plus 3 key socioeconomic/pollution/healthcare
predictors, using county boundaries from the public Plotly US-counties
GeoJSON (https://github.com/plotly/datasets, FIPS-keyed).

Outputs: ../results/maps/map_<variable>.html  (one per variable)
         ../results/maps/index.html            (links to all maps)
"""

import json
import os

import pandas as pd
import plotly.express as px
import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
MAPS_DIR = os.path.join(RESULTS_DIR, "maps")

GEOJSON_URL = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"

VARIABLES = {
    "drug_overdose_death_rate": ("Drug Overdose Death Rate (per 100,000)", "Reds"),
    "suicide_death_rate": ("Suicide Death Rate (per 100,000)", "Purples"),
    "heart_disease_death_rate": ("Heart Disease Death Rate (per 100,000)", "Reds"),
    "stroke_death_rate": ("Stroke Death Rate (per 100,000)", "Reds"),
    "diabetes_prevalence_pct": ("Diabetes Prevalence (% of adults)", "Oranges"),
    "lung_cancer_death_rate": ("Lung Cancer Death Rate (per 100,000)", "Reds"),
    "median_household_income": ("Median Household Income ($)", "Greens"),
    "pm25": ("Air Pollution: PM2.5 (ug/m3)", "Greys"),
    "uninsured_pct": ("Uninsured Adults (%)", "Blues"),
}


def main():
    os.makedirs(MAPS_DIR, exist_ok=True)

    print("Fetching county GeoJSON...")
    geojson = requests.get(GEOJSON_URL, timeout=60).json()

    df = pd.read_csv(os.path.join(DATA_DIR, "merged_county_data.csv"), dtype={"fips": str})
    df["fips"] = df["fips"].str.zfill(5)

    index_lines = ["<html><head><title>Project 3 Maps</title></head><body>",
                    "<h1>County-level mortality & socioeconomic maps</h1><ul>"]

    for col, (label, scale) in VARIABLES.items():
        sub = df[["fips", "county_name", "state", col]].dropna()
        sub[col] = pd.to_numeric(sub[col], errors="coerce")
        sub = sub.dropna(subset=[col])

        vmin, vmax = sub[col].quantile(0.02), sub[col].quantile(0.98)
        fig = px.choropleth(
            sub,
            geojson=geojson,
            locations="fips",
            color=col,
            color_continuous_scale=scale,
            range_color=(vmin, vmax),
            scope="usa",
            hover_name="county_name",
            hover_data={"state": True, col: ":.2f", "fips": False},
            labels={col: label},
        )
        fig.update_layout(
            title_text=f"{label} by County",
            geo=dict(scope="usa"),
            margin=dict(l=0, r=0, t=40, b=0),
        )
        out_path = os.path.join(MAPS_DIR, f"map_{col}.html")
        fig.write_html(out_path, include_plotlyjs="cdn")
        print(f"  wrote {out_path}")
        index_lines.append(f'<li><a href="map_{col}.html">{label}</a></li>')

    index_lines.append("</ul></body></html>")
    with open(os.path.join(MAPS_DIR, "index.html"), "w") as f:
        f.write("\n".join(index_lines))
    print(f"Wrote index -> {os.path.join(MAPS_DIR, 'index.html')}")


if __name__ == "__main__":
    main()
