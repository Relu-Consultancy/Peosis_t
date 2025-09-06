import pandas as pd
import plotly.express as px
import numpy as np

# Load datasets
movies_file = "complete_cleaned_dataset_for maps.csv"  # Update with your movies dataset file path
geocoded_file = "movies_geocoded.csv"  # Update with your geocoded file path

df_movies = pd.read_csv(movies_file)
df_geo = pd.read_csv(geocoded_file)

# Merge datasets on location_city and location_country
df_merged = df_movies.merge(
    df_geo, 
    left_on=["Shooting location", "Shooting location_city", "Shooting location_country"], 
    right_on=["location", "location_city", "location_country"], 
    how="left"
)

# Select required columns
df_merged = df_merged[[
    "Film Title", "Year of Release", "Disability Represented", "Category of Disability",
    "Latitude", "Longitude", "Shooting location", "Shooting location_city", "Shooting location_country"
]].dropna()

# Remove duplicates
df_merged = df_merged.drop_duplicates(subset=["Film Title", "Year of Release", "Latitude", "Longitude"])

# Convert to numeric
df_merged["Latitude"] = pd.to_numeric(df_merged["Latitude"], errors='coerce')
df_merged["Longitude"] = pd.to_numeric(df_merged["Longitude"], errors='coerce')

# Add small random jitter to prevent overlapping points
df_merged["Latitude"] += np.random.uniform(-0.005, 0.005, df_merged.shape[0])
df_merged["Longitude"] += np.random.uniform(-0.005, 0.005, df_merged.shape[0])

# Create heatmap
fig = px.density_mapbox(
    df_merged,
    lat="Latitude",
    lon="Longitude",
    z="Year of Release",  # Weighting by year of release
    radius=15,  # Adjust density radius
    mapbox_style="carto-darkmatter",  # Dark map style
    center={"lat": df_merged["Latitude"].mean(), "lon": df_merged["Longitude"].mean()},
    zoom=3,
    opacity=0.6,
    # color_continuous_scale="hot" ,
    # color_continuous_scale=["#fbf7f4", "#dec104", "#592a2e", "#000000"]  # Heatmap color scheme
)

# Update layout
fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    paper_bgcolor="#000000",
    plot_bgcolor="#000000",
    mapbox_bounds={"west": -180, "east": 180, "south": -90, "north": 90},

)

# Save as an interactive HTML file
html_file = "movie_heatmap.html"
fig.write_html(html_file)

print(f"HTML heatmap saved as {html_file}")