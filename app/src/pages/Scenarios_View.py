import logging
import streamlit as st
import requests

# Initialize logger
logger = logging.getLogger(__name__)

scenario_id = st.session_state['scenario_id']

# Set up the page layout
st.write(f"# Scenario {scenario_id}")