import logging
import streamlit as st
import requests

# Initialize logger
logger = logging.getLogger(__name__)

scenario_id = st.session_state['scenario_id']

# Authorization
access_token = st.session_state["access_token"]
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Set up the page layout
st.write(f"# Scenario {scenario_id}")

# TODO integrate with leaflet
st.write('Map currently unavailable.')
def get_points():
    api_url = f"http://web-api-wndt:4000/points/scenario/{scenario_id}"
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching points: {e}")
        return []

st.write('### Points')
points = get_points()
for point in points:
    st.write(f"{point['name']}: {point['geom']['coordinates'][0], point['geom']['coordinates'][1]}")

st.write('### Create point')
name = st.text_input("Name", key="name")
latitude = st.number_input("Latitude", format="%.6f", key="latitude")
longitude = st.number_input("Longitude", format="%.6f", key="longitude")
submitted = st.button("Submit")

if submitted:
    if not name:
        st.error("Name is required!")
    elif not latitude:
        st.error("Latitude is required!")
    elif not longitude:
        st.error("Longitude is required!")
    elif not scenario_id:
        st.error("Scenario ID is required!")
    else:
        # Prepare the data
        point_data = {
            "name": name,
            "latitude": latitude,
            "longitude": longitude,
            "scenario_id": scenario_id
        }

        # Send data to the API
        try:
            response = requests.post('http://web-api-wndt:4000/points/new', headers=headers, json=point_data)
            if response.status_code == 201:
                st.success("Point created successfully!")
                # TODO refresh page
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"Failed to connect to the API: {str(e)}")