import logging
import streamlit as st
import requests

# Initialize logger
logger = logging.getLogger(__name__)

# Set up the page layout
first_name = st.session_state['first_name']
st.write(f"# Welcome back, {first_name}!")

# Navigation buttons
if st.button('Profile', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/User_Info.py')

if st.button('Scenarios', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Scenarios_Home.py')

if st.button('Team', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/Team_Home.py')

if st.button('Test', type='secondary', use_container_width=True):
  st.switch_page('pages/Test.py')

if st.button('Logout', type='primary', use_container_width=True):
    st.session_state["authenticated"] = False
    st.session_state["user_id"] = None
    st.session_state["email"] = None
    st.session_state["first_name"] = None
    st.session_state["access_token"] = None
    st.success("You have been logged out.")
    st.switch_page('Home.py')


