"""
ExtraaLearn Lead Conversion Prediction Dashboard

Streamlit frontend that collects lead information and
communicates with the Flask prediction API.
"""

import os
import requests
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ExtraaLearn Lead Scoring",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# APPLICATION TITLE
# ============================================================

st.title("🎓 ExtraaLearn Lead Conversion Predictor")

st.markdown(
    """
    Enter the details of a lead to estimate the probability
    that the lead will convert into a paid customer.
    """
)


# ============================================================
# BACKEND API CONFIGURATION
# ============================================================

API_URL = os.getenv(
    "API_URL",
    "https://YOUR_USERNAME-extraalearn-lead-api.hf.space/predict"
)


# ============================================================
# INPUT FORM
# ============================================================

with st.form("lead_prediction_form"):

    st.subheader("Lead Information")

    col1, col2, col3 = st.columns(3)

    with col1:

        age = st.number_input(
            "Age",
            min_value=10,
            max_value=100,
            value=30
        )

        current_occupation = st.selectbox(
            "Current Occupation",
            [
                "Professional",
                "Unemployed",
                "Student"
            ]
        )

        first_interaction = st.selectbox(
            "First Interaction",
            [
                "Website",
                "Mobile App"
            ]
        )

        profile_completed = st.selectbox(
            "Profile Completed",
            [
                "Low",
                "Medium",
                "High"
            ]
        )

    with col2:

        website_visits = st.number_input(
            "Website Visits",
            min_value=0,
            value=3
        )

        time_spent_on_website = st.number_input(
            "Time Spent on Website (seconds)",
            min_value=0,
            value=500
        )

        page_views_per_visit = st.number_input(
            "Page Views per Visit",
            min_value=0.0,
            value=3.0
        )

        last_activity = st.selectbox(
            "Last Activity",
            [
                "Email Activity",
                "Phone Activity",
                "Website Activity"
            ]
        )

    with col3:

        print_media_type1 = st.selectbox(
            "Newspaper Advertisement",
            [0, 1]
        )

        print_media_type2 = st.selectbox(
            "Magazine Advertisement",
            [0, 1]
        )

        digital_media = st.selectbox(
            "Digital Media",
            [0, 1]
        )

        educational_channels = st.selectbox(
            "Educational Channels",
            [0, 1]
        )

        referral = st.selectbox(
            "Referral",
            [0, 1]
        )

    submitted = st.form_submit_button(
        "Predict Lead Conversion"
    )


# ============================================================
# PREDICTION
# ============================================================

if submitted:

    # --------------------------------------------------------
    # Feature engineering
    # Must match the training pipeline.
    # --------------------------------------------------------

    website_engagement_score = (
        __import__("numpy").log1p(website_visits)
        * __import__("numpy").log1p(
            time_spent_on_website
        )
        * __import__("numpy").log1p(
            page_views_per_visit
        )
    )

    marketing_exposure_score = (
        print_media_type1
        + print_media_type2
        + digital_media
        + educational_channels
        + referral
    )

    payload = {
        "age": age,
        "current_occupation": current_occupation,
        "first_interaction": first_interaction,
        "profile_completed": profile_completed,
        "website_visits": website_visits,
        "time_spent_on_website": time_spent_on_website,
        "page_views_per_visit": page_views_per_visit,
        "last_activity": last_activity,
        "print_media_type1": print_media_type1,
        "print_media_type2": print_media_type2,
        "digital_media": digital_media,
        "educational_channels": educational_channels,
        "referral": referral,
        "website_engagement_score":
            website_engagement_score,
        "marketing_exposure_score":
            marketing_exposure_score
    }

    try:

        with st.spinner(
            "Calculating conversion probability..."
        ):

            response = requests.post(
                API_URL,
                json=payload,
                timeout=30
            )

        if response.status_code == 200:

            result = response.json()

            probability = (
                result["conversion_probability"]
            )

            status = result["predicted_status"]

            priority = result["lead_priority"]

            st.success(
                "Prediction generated successfully."
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Conversion Probability",
                    f"{probability * 100:.1f}%"
                )

            with col2:

                st.metric(
                    "Predicted Status",
                    status
                )

            with col3:

                st.metric(
                    "Lead Priority",
                    priority
                )

            # Visual probability bar
            st.progress(
                probability,
                text="Estimated conversion probability"
            )

            # Business recommendation
            if priority == "Very High":

                st.info(
                    "Recommended action: "
                    "Immediate representative follow-up."
                )

            elif priority == "High":

                st.info(
                    "Recommended action: "
                    "Prioritize representative outreach."
                )

            elif priority == "Medium":

                st.info(
                    "Recommended action: "
                    "Continue personalized nurturing."
                )

            else:

                st.info(
                    "Recommended action: "
                    "Use automated/low-cost nurturing."
                )

        else:

            st.error(
                f"API error: {response.text}"
            )

    except requests.exceptions.RequestException as error:

        st.error(
            f"Unable to connect to prediction API: {error}"
        )
