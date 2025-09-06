import pandas as pd
import plotly.express as px
import numpy as np

# Load datasets
movies_file = "complete_cleaned_dataset_for maps.csv"  # Update with your movies dataset file path
geocoded_file = "processed_locations.csv"  # Update with your geocoded file path

df_movies = pd.read_csv(movies_file)
df_geo = pd.read_csv(geocoded_file)

# Merge datasets on location_city and location_country
df_merged = df_movies.merge(
    df_geo, 
    left_on=["Shooting location",  ], 
    right_on=["location",], 
    how="left"
)
# breakpoint()

# Select required columns
df_merged = df_merged[[
    "Film Title", "Year of Release", "Disability Represented", "Category of Disability",
    "Latitude", "Longitude", "Shooting location", "Shooting location_city", "Shooting location_state", "Shooting location_country"
]].dropna()

df_merged = df_merged.drop_duplicates(subset=["Film Title","Year of Release" ,"Latitude", "Longitude"])
# Create hover text
df_merged["Hover Info"] = df_merged.apply(
    lambda row: f"🎬 <b>{row['Film Title']}</b> ({row['Year of Release']})<br> <br> 🦽 Disability: {row['Disability Represented']}<br>📌 Category: {row['Category of Disability']} <br>📍 Location: {row['Shooting location']}", axis=1
)


df_merged["Size"] = 8


df_merged["Latitude"] = pd.to_numeric(df_merged["Latitude"], errors='coerce')
df_merged["Longitude"] = pd.to_numeric(df_merged["Longitude"], errors='coerce')


# Add small random jitter to latitude and longitude to prevent overlapping points
df_merged["Latitude"] += np.random.uniform(-0.005, 0.005, df_merged.shape[0])
df_merged["Longitude"] += np.random.uniform(-0.005, 0.005, df_merged.shape[0])

print(len(df_merged))
fig = px.scatter_mapbox(
    df_merged,
    lat="Latitude",
    lon="Longitude",
    # hover_name="Film Title",
    hover_data={"Shooting location": False,"Hover Info": False, "Latitude": False, "Longitude": False, "Size": False},
    hover_name="Hover Info",  # This directly shows formatted info without extra labels
    # hover_data={"Hover Info": False}
    color_discrete_sequence=["#dec104"],  # Gold circles
    size="Size",
    size_max=14,
    opacity=0.9,
    center={"lat": df_merged["Latitude"].mean(), "lon": df_merged["Longitude"].mean()},
)

# Apply styling
# fig.update_traces(marker=dict(opacity=0.8))
fig.update_traces(marker=dict(opacity=0.6, size=8))
# fig.update_traces(cluster=dict(enabled=True, maxzoom=10))

# Update layout with custom colors and styling
fig.update_layout(
    # mapbox_style="carto-positron", # Light minimalistic map
    hoverlabel=dict(bgcolor="#fbf7f4", font_size=10, font_family="Arial"),
    mapbox_style="carto-darkmatter",  # Dark map style
    mapbox_zoom=4,
    mapbox_center={"lat": df_merged["Latitude"].mean(), "lon": df_merged["Longitude"].mean()},
    # mapbox_bounds={"west": -180, "east": 180, "south": -60, "north": 85},
    mapbox_bounds={"west": -180, "east": 180, "south": -90, "north": 90},
  # Avoid duplicate world
    margin={"r":0,"t":0,"l":0,"b":0},
    # paper_bgcolor="#fbf7f4",  # Background color
    # plot_bgcolor="#fbf7f4"
    paper_bgcolor="#000000",  # Black background
    plot_bgcolor="#000000"
)

# Save as an interactive HTML file
html_file = "movie_scatter_map_shooting_locations_final.html"
fig.write_html(html_file)

print(f"HTML map saved as {html_file}")
