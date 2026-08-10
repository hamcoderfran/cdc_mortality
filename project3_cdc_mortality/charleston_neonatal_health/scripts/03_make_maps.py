"""
Charleston neonatal health — step 3: tract-level SDOH maps (neonatal risk proxies)
==================================================================================

CDC PLACES and SVI do not publish infant mortality at tract level. These maps show
social determinants strongly linked to adverse birth outcomes in the literature.

Outputs:
  ../results/maps/map_<variable>.html
  ../results/maps/index.html
"""

import json
import os

import pandas as pd
import plotly.express as px

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
MAPS_DIR = os.path.join(RESULTS_DIR, "maps")

MAP_VARIABLES = {
    "neonatal_risk_proxy_score": (
        "Neonatal Risk Proxy Score (SDOH composite, 0–1)",
        "Reds",
    ),
    "RPL_THEMES": ("Social Vulnerability Index (percentile)", "Reds"),
    "food_insecurity_pct": ("Food Insecurity (% adults, 12 mo)", "Purples"),
    "housing_insecurity_pct": ("Housing Insecurity (% adults, 12 mo)", "Purples"),
    "transportation_barrier_pct": ("Lack of Transportation (% adults)", "Blues"),
    "uninsured_pct": ("Uninsured Adults (% ages 18–64)", "Blues"),
    "depression_pct": ("Depression (% adults)", "Reds"),
}


def load_geojson():
    with open(os.path.join(DATA_DIR, "tract_boundaries.geojson")) as f:
        return json.load(f)


def make_map(df, geojson, col, label, scale):
    sub = df[["tract_fips", col]].dropna().copy()
    sub[col] = pd.to_numeric(sub[col], errors="coerce")
    sub = sub.dropna(subset=[col])
    if sub.empty:
        return None

    valid = set(sub["tract_fips"])
    features = [f for f in geojson["features"] if f["properties"]["GEOID"] in valid]
    if not features:
        return None

    filtered = {"type": "FeatureCollection", "features": features}
    fig = px.choropleth(
        sub,
        geojson=filtered,
        locations="tract_fips",
        featureidkey="properties.GEOID",
        color=col,
        color_continuous_scale=scale,
        range_color=(sub[col].min(), sub[col].max()),
        labels={col: label},
        title=f"Charleston County, SC — {label}",
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
    return fig


def main():
    os.makedirs(MAPS_DIR, exist_ok=True)
    tract = pd.read_csv(
        os.path.join(RESULTS_DIR, "tract_neonatal_risk_proxy.csv"),
        dtype={"tract_fips": str},
    )
    geojson = load_geojson()

    links = []
    for col, (label, scale) in MAP_VARIABLES.items():
        if col not in tract.columns:
            continue
        fig = make_map(tract, geojson, col, label, scale)
        if fig is None:
            continue
        fname = f"map_{col}.html"
        path = os.path.join(MAPS_DIR, fname)
        fig.write_html(path, include_plotlyjs="cdn")
        links.append((label, fname))
        print(f"Map -> {path}")

    index_lines = [
        "<!DOCTYPE html><html><head><meta charset='utf-8'>",
        "<title>Charleston Neonatal Health — Tract Maps</title>",
        "<style>body{font-family:system-ui;max-width:800px;margin:2rem auto;padding:0 1rem}",
        "a{display:block;padding:.5rem 0}</style></head><body>",
        "<h1>Charleston County Neonatal Health — SDOH Proxy Maps</h1>",
        "<p>Infant outcomes are county-level only in public SC data. Maps show tract social determinants linked to birth outcomes.</p>",
        "<ul>",
    ]
    for label, fname in links:
        index_lines.append(f"<li><a href='{fname}'>{label}</a></li>")
    index_lines += ["</ul></body></html>"]
    index_path = os.path.join(MAPS_DIR, "index.html")
    with open(index_path, "w") as f:
        f.write("\n".join(index_lines))
    print(f"Index -> {index_path}")


if __name__ == "__main__":
    main()
