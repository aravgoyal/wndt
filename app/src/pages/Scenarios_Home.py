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

user_id = st.session_state['user_id']

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
            if scenario['visibility'] == 'public' or (scenario['visibility'] == 'private' and scenario['user_id'] == user_id):
                if st.button(f"Scenario {scenario['id']}", key=f"button_{scenario['id']}", type='primary', use_container_width=True):
                    st.session_state.scenario_id = scenario['id']
                    st.switch_page("pages/Scenarios_View.py")

    else:
        st.write("No scenarios available.")

if st.button('Create Scenario', type='secondary'):
    st.switch_page('pages/Scenarios_Create.py')
  
load_scenarios()