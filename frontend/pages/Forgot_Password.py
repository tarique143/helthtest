# frontend/pages/Forgot_Password.py

import streamlit as st
from auth.service import request_password_reset

st.set_page_config(page_title="Forgot Password", page_icon="🔑", layout="centered")

st.title("Forgot Your Password?")
st.markdown("No problem. Enter your email address below, and we'll send you a link to reset it.")

with st.form("forgot_password_form"):
    email = st.text_input("Your Email Address", placeholder="Enter your email")
    submitted = st.form_submit_button("Send Reset Link")

    if submitted:
        if not email:
            st.warning("Please enter your email address.")
        else:
            with st.spinner("Sending request..."):
                is_success, message = request_password_reset(email)
            
            # For security, we always show a success message
            st.success("If an account with that email exists, a password reset link has been sent. Please check your inbox.")