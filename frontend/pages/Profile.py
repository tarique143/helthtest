# frontend/pages/Profile.py

import streamlit as st
from streamlit_cookies_manager import CookieManager
from datetime import datetime

from auth.service import TOKEN_COOKIE_NAME, get_profile, update_profile
from components.sidebar import authenticated_sidebar

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="My Profile", page_icon="👤", layout="wide")

# --- AUTHENTICATION CHECK ---
cookies = CookieManager()
if not cookies.ready():
    st.spinner()
    st.stop()

token = cookies.get(TOKEN_COOKIE_NAME)
if not token:
    st.warning("You are not logged in. Please log in to continue.")
    st.switch_page("Home.py")

# --- RENDER THE SIDEBAR ---
authenticated_sidebar(cookies)

# --- PAGE HEADER ---
st.title("My Profile 👤")
st.markdown("View and update your personal information here.")

# --- DATA FETCHING ---
is_success, profile_data = get_profile(token)

if not is_success:
    st.error(f"Could not load your profile: {profile_data}")
    st.stop() # Stop execution if profile can't be loaded

# --- DISPLAY AND UPDATE PROFILE ---
col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("Current Information")
    st.info(f"**Email:** {profile_data.get('email')}")
    st.info(f"**Full Name:** {profile_data.get('full_name', 'Not set')}")
    
    dob = profile_data.get('dob')
    display_dob = datetime.strptime(dob, '%Y-%m-%d').strftime('%B %d, %Y') if dob else "Not set"
    st.info(f"**Date of Birth:** {display_dob}")
    
    st.info(f"**Address:** {profile_data.get('address', 'Not set')}")

with col2:
    st.subheader("Update Your Information")
    with st.form("update_profile_form"):
        # Pre-fill the form with existing data
        full_name = st.text_input("Full Name", value=profile_data.get('full_name', ''))
        
        # Convert date string to date object for the date_input
        current_dob = None
        if profile_data.get('dob'):
            current_dob = datetime.strptime(profile_data.get('dob'), '%Y-%m-%d').date()
        
        dob = st.date_input("Date of Birth", value=current_dob)
        
        address = st.text_area("Address", value=profile_data.get('address', ''), height=150)
        
        submitted = st.form_submit_button("Save Changes")
        if submitted:
            # Prepare payload with only the fields that are not empty
            payload = {}
            if full_name:
                payload["full_name"] = full_name
            if dob:
                # Convert date object back to string for the API
                payload["dob"] = dob.isoformat()
            if address:
                payload["address"] = address

            if not payload:
                st.warning("No changes to save.")
            else:
                update_success, update_message = update_profile(token, payload)
                if update_success:
                    st.success(update_message)
                    st.rerun() # Refresh the page to show updated info
                else:
                    st.error(update_message)