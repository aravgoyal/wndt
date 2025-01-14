import logging
import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

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

# Map
def get_scenario():
    api_url = f"http://web-api-wndt:4000/scenarios/view/{scenario_id}"
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching scenario: {e}")
        return []

def get_points():
    api_url = f"http://web-api-wndt:4000/points/scenario/{scenario_id}"
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching points: {e}")
        return []

scenario_info = get_scenario()
center = scenario_info["map_center"]["coordinates"]
size = scenario_info["map_size"]
mapview = folium.Map(location=center, zoom_start=10)
points = get_points()
for point in points:
    folium.Marker(location=point["geom"]["coordinates"], popup=point["name"]).add_to(mapview)
st_folium(mapview, width=700, height=500)

st.write('### Points')
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

deleted = st.button("Delete Scenario")
if deleted:
    confirmed = st.button("Confirm")
    if confirmed:
        api_url = f"http://web-api-wndt:4000/scenarios/delete/{scenario_id}"
        try:
            response = requests.delete(api_url, headers=headers)
            if response.status_code == 200:
                st.success(f"Scenario {scenario_id} deleted!")
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error deleting scenario: {e}")