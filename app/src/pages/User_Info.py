import logging
import streamlit as st
import requests

# Initialize logger
logger = logging.getLogger(__name__)

# Set up the page layout
st.write("# Profile")

# Authorization
access_token = st.session_state["access_token"]
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Get all user info
def get_user_info(api_url):
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching user info: {e}")
        return []
    
user_id = st.session_state["user_id"]
api_url = f"http://web-api-wndt:4000/users/view/{user_id}"
user_info = get_user_info(api_url)
if user_info:
    st.write("First Name: ", user_info["first_name"])
    st.write("Last Name: ", user_info["last_name"])
    st.write("Email: ", user_info["email"])
else:
    st.write("No user info available.")