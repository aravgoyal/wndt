import logging
import streamlit as st
import requests

# Initialize logger
logger = logging.getLogger(__name__)

# Set up the page layout
st.write("# Scenarios")

# Authorization
access_token = st.session_state["access_token"]
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Get all scenarios
def get_scenarios(api_url):
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching scenarios: {e}")
        return []

def load_scenarios():
    api_url = "http://web-api-wndt:4000/scenarios/view"
    scenarios = get_scenarios(api_url)
    if scenarios:
        for scenario in scenarios:
            st.button(f"Scenario {scenario['id']}", key=f"button_{scenario['id']}", type='primary', use_container_width=True)
    else:
        st.write("No scenarios available.")

if st.button('Create Scenario', type='secondary'):
    st.switch_page('pages/Scenarios_Create.py')
  
load_scenarios()