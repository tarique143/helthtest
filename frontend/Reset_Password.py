# frontend/Reset_Password.py

import streamlit as st
from auth.service import set_new_password
import time

st.set_page_config(page_title="Reset Password", page_icon="🔑", layout="centered")

st.title("Create a New Password")

# Get the reset token from the URL query parameters
try:
    token = st.query_params["token"]
except KeyError:
    st.error("Invalid password reset link. The token is missing.")
    st.info("Please request a new password reset link from the 'Forgot Password' page.")
    st.stop()

with st.form("reset_password_form"):
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")
    submitted = st.form_submit_button("Reset Password")

    if submitted:
        if not new_password or not confirm_password:
            st.warning("Please fill in both password fields.")
        elif new_password != confirm_password:
            st.error("Passwords do not match. Please try again.")
        elif len(new_password) < 6:
            st.error("Password must be at least 6 characters long.")
        else:
            with st.spinner("Resetting your password..."):
                is_success, message = set_new_password(token, new_password)
            
            if is_success:
                st.success(message)
                st.info("Redirecting you to the login page...")
                time.sleep(3)
                st.switch_page("Home.py")
            else:
                st.error(message)