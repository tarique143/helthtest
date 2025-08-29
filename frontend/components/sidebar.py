# frontend/components/sidebar.py

import streamlit as st
from auth.service import TOKEN_COOKIE_NAME

def authenticated_sidebar(cookies):
    """
    Displays an authenticated sidebar with navigation links and a logout button.
    """
    st.sidebar.title("Navigation")
    st.sidebar.info("Welcome back! You are logged in.")
    
    # --- NAVIGATION LINKS (using standard markdown) ---
    st.sidebar.markdown("---")
    st.sidebar.page_link("pages/Dashboard.py", label="Dashboard", icon="🏠")
    st.sidebar.page_link("pages/Medications.py", label="My Medications", icon="💊")
    st.sidebar.page_link("pages/Appointments.py", label="My Appointments", icon="🗓️")
    st.sidebar.page_link("pages/Emergency_Contacts.py", label="Emergency Contacts", icon="📞")
    st.sidebar.page_link("pages/Profile.py", label="My Profile", icon="👤")
    st.sidebar.markdown("---")
    
    # --- LOGOUT BUTTON ---
    if st.sidebar.button("Logout", use_container_width=True, type="primary"):
        if cookies.get(TOKEN_COOKIE_NAME):
            del cookies[TOKEN_COOKIE_NAME]
        
        st.switch_page("Home.py")