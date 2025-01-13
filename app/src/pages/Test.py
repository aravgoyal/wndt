import logging
import streamlit as st
import requests
import pandas as pd

# Initialize logger
logger = logging.getLogger(__name__)

# Set up the page layout
st.write("# View Data: Users, Teams, and Team Members")

# Authorization
access_token = st.session_state.get("access_token", "")
headers = {
    "Authorization": f"Bearer {access_token}"
}

def get_all_users():
    """Fetch all user information."""
    try:
        api_url = "http://web-api-wndt:4000/users/view"
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching all users: {e}")
        return {"error": "Failed to connect to the API"}

def get_all_teams():
    """Fetch all team information."""
    try:
        api_url = "http://web-api-wndt:4000/teams/view"
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching all teams: {e}")
        return {"error": "Failed to connect to the API"}

def get_team_members(team_id):
    """Fetch members of a specific team."""
    try:
        api_url = f"http://web-api-wndt:4000/teams/view/{team_id}/members"
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching team members for team {team_id}: {e}")
        return {"error": "Failed to connect to the API"}

def get_scenarios():
    api_url = "http://web-api-wndt:4000/scenarios/view"
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching scenarios: {e}")
        return []

# Display the scenarios as buttons
scenarios = get_scenarios()

if scenarios:
    df_scenarios = pd.DataFrame(scenarios)
    st.dataframe(df_scenarios)
   
else:
    st.write("No scenarios available.")

# Buttons to fetch data
col1, col2 = st.columns(2)

with col1:
    if st.button("Fetch All Users"):
        with st.spinner("Fetching all user info..."):
            users_data = get_all_users()
            if "error" in users_data:
                st.error(users_data["error"])
            else:
                if users_data:
                    df_users = pd.DataFrame(users_data)
                    st.success("All user info retrieved successfully!")
                    st.dataframe(df_users, hide_index=True)
                else:
                    st.warning("No users found.")

with col2:
    if st.button("Fetch All Teams"):
        with st.spinner("Fetching all team info..."):
            teams_data = get_all_teams()
            if "error" in teams_data:
                st.error(teams_data["error"])
            else:
                if teams_data:
                    df_teams = pd.DataFrame(teams_data)
                    st.success("All team info retrieved successfully!")
                    st.dataframe(df_teams, hide_index=True)
                else:
                    st.warning("No teams found.")

# Input and button for fetching team members
st.write("### View Members of a Specific Team")
team_id = st.number_input("Enter Team ID", min_value=1, step=1, key="team_id_input")

if st.button("Fetch Team Members"):
    with st.spinner(f"Fetching members of team {team_id}..."):
        members_data = get_team_members(team_id)
        if "error" in members_data:
            st.error(members_data["error"])
        else:
            if members_data:
                df_members = pd.DataFrame(members_data)
                st.success(f"Members of Team {team_id} retrieved successfully!")
                st.dataframe(df_members, hide_index=True)
            else:
                st.warning(f"No members found for Team {team_id}.")
