import streamlit as st
import requests
import logging

# Set up logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask API base URL
BASE_URL = "http://web-api-wndt:4000"

# Set up the page layout
st.set_page_config(layout="wide")

# Initialize session state for authentication if not already initialized
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Function to handle user login
def login_user(email, password):
    try:
        response = requests.post(f"{BASE_URL}/users/login", json={"email": email, "password": password})
        if response.status_code == 200:
            user_info = response.json()
            st.session_state["authenticated"] = True
            st.session_state["user_id"] = user_info["user_id"]
            st.session_state["email"] = email
            st.session_state["first_name"] = user_info["first_name"]
            st.session_state["access_token"] = user_info["access_token"]
            st.success("Login successful!")
            st.switch_page('pages/Dashboard.py')
            return True
        else:
            st.error("Invalid email or password. Please try again.")
            return False
    except Exception as e:
        st.error(f"Error: {e}")
        return False

# Function to handle user registration
def register_user(first_name, last_name, email, password):
    try:
        response = requests.post(f"{BASE_URL}/users/register", json={
            "first_name": first_name, "last_name": last_name,
            "email": email, "password": password
        })
        if response.status_code == 201:
            st.success("User registered successfully! You can now log in.")
        else:
            st.error("Registration failed. The email might already exist.")
    except Exception as e:
        st.error(f"Error: {e}")

# If the user is authenticated, show a welcome message
if st.session_state["authenticated"]:
    st.write(f"Welcome back, {st.session_state['first_name']}!")

    # Show a dashboard button
    if st.button("Go to Dashboard"):
        st.experimental_rerun()

else:
    # Main page for users who aren't logged in
    st.title("WNDT DASHBOARD")
    st.write("\n\n")
    st.write("### Please log in or register")

    # Tabs for login and registration forms
    tab = st.radio("Select an option", ["Login", "Register"])

    # Login Form
    if tab == "Login":
        st.write("### Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if email and password:
                login_user(email, password)
            else:
                st.error("Please enter both email and password.")

    # Register Form
    elif tab == "Register":
        st.write("### Register")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if password != confirm_password:
            st.error("Passwords do not match!")

        if st.button("Register"):
            if first_name and last_name and email and password:
                register_user(first_name, last_name, email, password)
            else:
                st.error("Please fill out all fields.")
