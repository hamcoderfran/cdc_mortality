"""
Charleston County deep-dive, step 3: Interactive census-tract choropleth maps
=============================================================================

Builds standalone Plotly HTML maps for key health and vulnerability measures
at the census-tract level within Charleston County, SC.

Outputs:
  ../results/maps/map_<variable>.html
  ../results/maps/index.html
"""

import json
import os

import pandas as pd
import plotly.express as px

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
MAPS_DIR = os.path.join(os.path.dirname(__file__), "..", "results", "maps")

# (column, display label, color scale)
MAP_VARIABLES = {
    "RPL_THEMES": ("Social Vulnerability Index (overall percentile)", "Reds"),
    "diabetes_pct": ("Diagnosed Diabetes (% adults)", "Oranges"),
    "obesity_pct": ("Obesity (% adults)", "Oranges"),
    "uninsured_pct": ("Uninsured Adults (% ages 18-64)", "Blues"),
    "food_insecurity_pct": ("Food Insecurity (% adults, past 12 mo)", "Purples"),
    "housing_insecurity_pct": ("Housing Insecurity (% adults, past 12 mo)", "Purples"),
    "mental_distress_pct": ("Frequent Mental Distress (% adults)", "Reds"),
    "depression_pct": ("Depression (% adults)", "Reds"),
    "smoking_pct": ("Current Smoking (% adults)", "Greys"),
    "high_blood_pressure_pct": ("High Blood Pressure (% adults)", "Reds"),
    "stroke_pct": ("Stroke (% adults)", "Reds"),
    "fair_poor_health_pct": ("Fair/Poor Self-Rated Health (% adults)", "Reds"),
    "physical_inactivity_pct": ("No Leisure-Time Physical Activity (% adults)", "YlOrRd"),
    "utility_shutoff_threat_pct": ("Utility Shut-off Threat (% adults)", "Purples"),
    "transportation_barrier_pct": ("Lack of Reliable Transportation (% adults)", "Blues"),
}


def load_geojson():
    path = os.path.join(DATA_DIR, "tract_boundaries.geojson")
    with open(path) as f:
        return json.load(f)


def make_map(df, geojson, col, label, scale):
    sub = df[["tract_fips", col]].dropna().copy()
    sub[col] = pd.to_numeric(sub[col], errors="coerce")
    sub = sub.dropna(subset=[col])
    if sub.empty:
        return None

    # Match geojson features to data tracts
    valid_geoids = set(sub["tract_fips"])
    features = [
        f
        for f in geojson["features"]
        if f["properties"]["GEOID"] in valid_geoids
    ]
    if not features:
        return None
    tract_geo = {"type": "FeatureCollection", "features": features}

    vmin = sub[col].quantile(0.05)
    vmax = sub[col].quantile(0.95)

    fig = px.choropleth(
        sub,
        geojson=tract_geo,
        locations="tract_fips",
        featureidkey="properties.GEOID",
        color=col,
        color_continuous_scale=scale,
        range_color=(vmin, vmax),
        hover_name="tract_fips",
        labels={col: label},
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        title=f"{label} — Charleston County, SC (census tracts)",
        margin=dict(l=0, r=0, t=50, b=0),
        coloraxis_colorbar=dict(title=label),
    )
    return fig


def main():
    os.makedirs(MAPS_DIR, exist_ok=True)

    df = pd.read_csv(
        os.path.join(DATA_DIR, "merged_tract_data.csv"), dtype={"tract_fips": str}
    )
    df["tract_fips"] = df["tract_fips"].str.zfill(11)
    geojson = load_geojson()

    index_lines = [
        "<!DOCTYPE html>",
        "<html><head>",
        "<meta charset='utf-8'>",
        "<title>Charleston County Health & Vulnerability Maps</title>",
        "<style>",
        "body{font-family:system-ui,sans-serif;max-width:900px;margin:2rem auto;padding:0 1rem;}",
        "h1{color:#1a365d;} li{margin:0.4rem 0;} a{color:#2b6cb0;}",
        ".note{background:#ebf8ff;border-left:4px solid #3182ce;padding:0.75rem 1rem;margin:1rem 0;}",
        "</style></head><body>",
        "<h1>Charleston County — Interactive Tract Maps</h1>",
        "<div class='note'>Census-tract choropleths for Charleston County, SC (FIPS 45019). "
        "Health measures from CDC PLACES 2025 (model-based BRFSS estimates). "
        "Social vulnerability from CDC/ATSDR SVI 2022.</div>",
        "<ul>",
    ]

    for col, (label, scale) in MAP_VARIABLES.items():
        if col not in df.columns:
            continue
        fig = make_map(df, geojson, col, label, scale)
        if fig is None:
            print(f"  skip {col} (no data)")
            continue
        out_path = os.path.join(MAPS_DIR, f"map_{col}.html")
        fig.write_html(out_path, include_plotlyjs="cdn")
        print(f"  wrote {out_path}")
        index_lines.append(f'<li><a href="map_{col}.html">{label}</a></li>')

    index_lines.append("</ul></body></html>")
    index_path = os.path.join(MAPS_DIR, "index.html")
    with open(index_path, "w") as f:
        f.write("\n".join(index_lines))
    print(f"Wrote index -> {index_path}")


if __name__ == "__main__":
    main()
