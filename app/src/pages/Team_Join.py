import logging
import streamlit as st
import requests

# Initialize logger
logger = logging.getLogger(__name__)

# Set up the page layout
st.write("# Join Team")

# Authorization
access_token = st.session_state["access_token"]
headers = {
    "Authorization": f"Bearer {access_token}"
}

user_id = st.session_state["user_id"]

# Form fields
team_id = st.text_input("ID", key="team_id") # TODO show teams instead of manually adding id

# Submit button
submitted = st.button("Submit")

if submitted:

    # Prepare the data
    team_data = {
        "team_id": team_id,
        "user_id": user_id
    }

    # Send data to the API
    try:
        response = requests.post('http://web-api-wndt:4000/teams/join', headers=headers, json=team_data)
        if response.status_code == 201:
            st.success("Team joined successfully!")
            load_team_members()
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"Failed to connect to the API: {str(e)}")