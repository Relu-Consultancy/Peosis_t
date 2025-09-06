# 🎬 Disability Film Visualizer

This repository contains a Flask API and Python scripts for processing, filtering, and visualizing a dataset of films related to disability representation. It supports map-based visualization using Plotly and provides a REST API to query location data based on disability categories.

---

## 📌 Requirements

Make sure you have the following installed:

- **Python 3.7+**
- **Flask**
- **Flask-CORS**
- **pandas**
- **plotly**
- **numpy**

---

## 🚀 Getting Started


### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/disability-film-visualizer.git
cd disability-film-visualizer
```
### 2. Install Dependencies
```bash
pip install flask flask-cors pandas plotly numpy
```

## 🌐 Flask API (`app.py`)

### 🔥 Start the Server

```bash
python app.py
```
### 📡 Endpoint: `POST /locations/`

Filter films by disability category and type.

### 📨 Request JSON format:

```json
{
  "category": "Cognitive Disability",
  "disability": ["Autism Spectrum Disorder", "Down Syndrome"]
}
```

You can also use the following to get all films without filtering:

```json

{
  "category": "All categories",
  "disability": "All disabilities"
}
```
---

## 🧪 Example Usage (using curl):
```bash

curl -X POST http://localhost:5011/locations/ \
  -H "Content-Type: application/json" \
  -d '{"category": "All categories", "disability": "All disabilities"}'
```
---
## 🗺️ Scatter Map (`scatter.py`)

Generates a scatter map of shooting locations from the dataset.

### ▶️ Run:

```bash
python scatter.py
```

### 📄 Output:

**`movie_scatter_map_shooting_locations_final.html`**  
An interactive HTML map using Plotly with customized hover details and styling.

---

## 🔥 Heatmap (`new_heatmap.py`)

Creates a density-based heatmap of movie shooting locations, weighted by the year of release.

### ▶️ Run:

```bash
python new_heatmap.py
```
### 📄 Output:

**`movie_heatmap.html`**  

A dark-themed interactive heatmap visualizing geographic clustering of shooting locations.

---
