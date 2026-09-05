# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# ------------------------------------------------------------
# Flask application
# ------------------------------------------------------------
app = Flask(__name__)

# Load the trained machine learning model
model = joblib.load("best_lead_conversion_model.joblib")


# ------------------------------------------------------------
# Health-check endpoint
# ------------------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    """Return API status."""

    return jsonify({
        "application": "ExtraaLearn Lead Conversion API",
        "status": "running"
    })


# ------------------------------------------------------------
# Prediction endpoint
# ------------------------------------------------------------

@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict whether a lead is likely to convert.

    Expected input:
        JSON object containing the same features used
        during model training.

    Returns:
        Conversion probability and predicted status.
    """

    try:

        # Read JSON request
        data = request.get_json()

        if data is None:
            return jsonify({
                "error": "Request body must contain JSON data."
            }), 400

        # Convert JSON into DataFrame
        input_df = pd.DataFrame([data])

        # Generate probability
        probability = model.predict_proba(
            input_df
        )[0, 1]

        # Generate prediction
        prediction = int(
            probability >= 0.50
        )

        status = (
            "Likely Converted"
            if prediction == 1
            else "Less Likely Converted"
        )

        # Assign business priority
        if probability >= 0.80:
            priority = "Very High"
        elif probability >= 0.60:
            priority = "High"
        elif probability >= 0.30:
            priority = "Medium"
        else:
            priority = "Low"

        return jsonify({
            "predicted_status": status,
            "conversion_probability": round(
                float(probability),
                4
            ),
            "lead_priority": priority
        })

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# ------------------------------------------------------------
# Application entry point
# ------------------------------------------------------------

if __name__ == "__main__":

    # Hugging Face Docker Spaces use port 7860 by default.
    app.run(
        host="0.0.0.0",
        port=7860,
        debug=False
    )