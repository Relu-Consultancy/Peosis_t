from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import logging

# Setup logging 
logging.basicConfig(filename="app.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

app = Flask(__name__)
CORS(app)

DATA_FILE = "movies_with_locations_final.csv"

# Load dataset with error handling
try:
    df = pd.read_csv(DATA_FILE, low_memory=False)
    logging.info("Dataset loaded successfully")
except Exception as e:
    logging.error(f"Error loading dataset: {e}")
    df = pd.DataFrame()

def preview_dataset(n=5):
    """Utility function to provide dataset rows(not used in API)"""
    try:
        logging.info("Previewing dataset")
        return df.head(n)
    except Exception as e:
        logging.error(f"Error previewing dataset: {e}")
        return []

def get_filtered_data():
    """Fetch and return filtered data based on category."""
    try:
        data = request.get_json()
        disability_category = data.get("category")
        disability_represented = data.get("disability")
        logging.info(disability_represented)
        if not disability_category or not disability_represented:
            return jsonify({"error": "Filter parameters required : category and disability"}), 400
        if not isinstance(disability_represented, list) and disability_represented != "All disabilities":
            return jsonify({"error": "disability represented must be either list or of value 'All disabilities'"}), 400

        # Filter dataset based on category
        if disability_category == "All categories":
            filtered_df = df
        else:
            filtered_df = df[df["Category of Disability"] == disability_category]

        if isinstance(disability_represented, list) and disability_represented != "All disabilities":
            # filtered_df = filtered_df[filtered_df["Disability Represented"] == disability_represented]
            filtered_df = filtered_df[filtered_df["Disability Represented"].isin(disability_represented)]

            
        if filtered_df.empty:
            return jsonify({"message": "No records found"}), 200

        # Select relevant columns
        filtered_df = filtered_df.loc[:, ["Film ID", "Film Title", "Year of Release", 
                                          "Disability Represented", "Category of Disability", 
                                          "Final Location", "Latitude", "Longitude"]]

        # Drop rows with missing locations
        filtered_df = filtered_df.dropna(subset=["Final Location", "Latitude", "Longitude"])

        filtered_df = filtered_df.drop_duplicates()

        # Convert to list of dictionaries
        filtered_df[["Year of Release", "Disability Represented", "Category of Disability"]] = \
            filtered_df[["Year of Release", "Disability Represented", "Category of Disability"]].where(pd.notna(filtered_df[["Year of Release", "Disability Represented", "Category of Disability"]]), None)

        results = filtered_df.to_dict(orient="records")
        logging.info(f"Got results: {len(results)}")
        return jsonify(results)

    except Exception as e:
        logging.error(f"Error in get_filtered_data: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

    

@app.route("/locations/", methods=["POST"])
def locations():
    """Fetch locations based on category."""
    return get_filtered_data()

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", debug=True, port=5011)
        #load dataset with error handling
        logging.info("Flask server is up and running")
    except Exception as e:
        logging.error(f"Error starting Flask server: {e}")
