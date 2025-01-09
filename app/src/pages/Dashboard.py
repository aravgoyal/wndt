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


