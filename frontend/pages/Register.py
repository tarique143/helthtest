# frontend/pages/Register.py

import streamlit as st
import re
import time
from auth.service import register_user

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Register Account",
    page_icon="📝",
    layout="centered"
)

# --- EMAIL VALIDATION FUNCTION ---
def is_valid_email(email):
    """Validate the email address using a regular expression."""
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(regex, email):
        return True
    return False

# --- REGISTRATION PAGE LAYOUT ---

st.title("Create a New Account")
st.markdown("Please fill out the form below to create your account.")
st.markdown("---")

with st.form("register_form"):
    st.subheader("Your Personal Details")
    
    full_name = st.text_input("Full Name", placeholder="Your full name")
    email = st.text_input("Email Address", placeholder="Your email address")
    
    st.subheader("Create a Secure Password")
    
    password = st.text_input("Password", type="password", placeholder="Create a strong password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
    
    submitted = st.form_submit_button("Create My Account")

    if submitted:
        # --- Form Validation Logic ---
        if not full_name or not email or not password or not confirm_password:
            st.warning("Please fill out all the fields.")
        elif not is_valid_email(email):
            st.error("Please enter a valid email address.")
        elif password != confirm_password:
            st.error("Passwords do not match. Please try again.")
        elif len(password) < 6:
            st.error("Password should be at least 6 characters long.")
        else:
            with st.spinner("Creating your account..."):
                is_success, message = register_user(full_name, email, password)
            
            if is_success:
                st.success(message)
                st.info("Redirecting you to the login page...")
                time.sleep(2)  # Give the user a moment to read the message
                st.switch_page("Home.py") # <-- THIS IS THE NEW LINE
            else:
                st.error(message)