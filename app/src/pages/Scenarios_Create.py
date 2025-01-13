import logging
import streamlit as st
import requests
import pandas as pd

# Initialize logger
logger = logging.getLogger(__name__)

# Set up the page layout
st.write("# Create Scenario")

# Authorization
access_token = st.session_state["access_token"]
headers = {
    "Authorization": f"Bearer {access_token}"
}

visibility = st.selectbox("Visibility", ["public", "private"], key="visibility") # TODO implement public vs private functionality
frequency = st.number_input("Frequency", key="frequency")
scenario_type = st.text_input("Scenario Type", key="scenario_type")
map_center_long = st.number_input("Map Center Longitude", format="%.6f", key="map_center_long")
map_center_lat = st.number_input("Map Center Latitude", format="%.6f", key="map_center_lat")
map_size = st.number_input("Map Size", min_value=1, key="map_size")
user_id = st.session_state["user_id"]

# Submit button
submitted = st.button("Submit")

if submitted:
    # Prepare the data
    scenario_data = {
        "visibility": visibility,
        "frequency": frequency,
        "scenario_type": scenario_type,
        "map_center_long": map_center_long,
        "map_center_lat": map_center_lat,
        "map_size": map_size,
        "user_id": user_id
    }

    # Send data to the API
    try:
        response = requests.post('http://web-api-wndt:4000/scenarios/new', headers=headers, json=scenario_data)
        if response.status_code == 201:
            st.success("Scenario created successfully!")
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"Failed to connect to the API: {str(e)}")