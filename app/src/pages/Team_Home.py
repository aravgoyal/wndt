import logging
import streamlit as st
import requests
import pandas as pd

# Initialize logger
logger = logging.getLogger(__name__)

# Set up the page layout
st.write("# Team")

# Authorization
access_token = st.session_state["access_token"]
headers = {
    "Authorization": f"Bearer {access_token}"
}

def get_team_id(api_url):
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()["team_id"]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching team: {e}")
        return []

def get_team_members(api_url):
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching team members: {e}")
        return []

def load_team_members():
    api_url = f"http://web-api-wndt:4000/users/team/{user_id}"
    team_id = get_team_id(api_url)
    team_members = get_team_members(f"http://web-api-wndt:4000/teams/{team_id}/members")
    st.dataframe(team_members, hide_index=True)

user_id = st.session_state["user_id"]
api_url = f"http://web-api-wndt:4000/users/team/{user_id}"
team_id = get_team_id(api_url)
if team_id:
    team_members = get_team_members(f"http://web-api-wndt:4000/teams/view/{team_id}/members")
    if team_members:
        full_names = [st.write(f"### {member['first_name']} {member['last_name']} ({member['email']})") for member in team_members]
else:
    if st.button('Create Team', type='primary', use_container_width=True):
        st.switch_page('pages/Team_Create.py')
        
    if st.button('Join Team', type='primary', use_container_width=True):
        st.switch_page('pages/Team_Join.py')
