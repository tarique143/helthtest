# frontend/pages/Dashboard.py

import streamlit as st
from streamlit_cookies_manager import CookieManager
from auth.service import TOKEN_COOKIE_NAME, get_dashboard_data
from components.sidebar import authenticated_sidebar
import time
from datetime import datetime
import pytz
from pathlib import Path
import pandas as pd
import base64 # <-- Import for reading image bytes


# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Dashboard", page_icon="🏠", layout="wide")

# --- AUTHENTICATION & INITIALIZATION ---
cookies = CookieManager()
if not cookies.ready():
    st.spinner("Loading...")
    st.stop()

token = cookies.get(TOKEN_COOKIE_NAME)
if not token:
    st.warning("You are not logged in. Please log in to continue.")
    st.switch_page("Home.py")

authenticated_sidebar(cookies)

# --- DATA FETCHING ---
is_success, data = get_dashboard_data(token)

if not is_success:
    st.error(f"Failed to fetch data: {data}. Your session may be invalid.")
    st.info("Redirecting to login page...")
    if cookies.get(TOKEN_COOKIE_NAME):
        del cookies[TOKEN_COOKIE_NAME]
    st.switch_page("Home.py")

# --- STYLING ---
# (Optional) Add some CSS for better card appearance
st.markdown("""
<style>
    div[data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"] > [data-testid="column"] > div {
        border: 1px solid #999;
        border-radius: 7px;
        padding: 20px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


# --- HEADER SECTION ---

# --- PERMANENT IMAGE FIX ---
# Function to read image as base64
def get_image_as_base64(path):
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        print(f"Error reading image file: {e}")
        return None

# Construct absolute path and get base64 string
image_path = Path(__file__).parent.parent / "assets" / "icon.png"
img_base64 = get_image_as_base64(image_path)


col1, col2, col3 = st.columns([1, 4, 1.5])
with col1:
    if img_base64:
        # Display image using base64 HTML
        st.markdown(f'<img src="data:image/png;base64,{img_base64}" width="100">', unsafe_allow_html=True)

with col2:
    user_name = data.get("user_full_name", "User")
    st.title(f"Welcome, {user_name}!")
    st.subheader("Here is your health summary for today.")

with col3:
    clock_placeholder = st.empty()

st.markdown("---")


# --- MAIN DASHBOARD CONTENT (IMPROVED UI) ---
col_meds, col_appts = st.columns(2, gap="large")

with col_meds:
    st.subheader("Today's Medication Schedule 💊")
    meds_today = data.get("medications_today", [])
    if not meds_today:
        st.info("✅ You have no pending medications for today. Great job!")
    else:
        for med in meds_today:
            st.markdown(f"**• {med['name']}** ({med['dosage']}) - *Take {med['timing']}*")
    
    if st.button("Manage All Medications", use_container_width=True, type="secondary"):
        st.switch_page("pages/Medications.py")
    
    st.markdown("<br>", unsafe_allow_html=True) # Add some vertical space

    st.subheader("Daily Health Tip 💡")
    health_tip = data.get("health_tip", "No tip available today.")
    st.success(f"**Tip:** {health_tip}")


with col_appts:
    st.subheader("Your Next Appointment 🗓️")
    appointment = data.get("next_appointment")
    if not appointment:
        st.warning("You have no upcoming appointments scheduled.")
    else:
        appt_dt = pd.to_datetime(appointment['appointment_datetime'])
        st.markdown(f"#### Dr. {appointment['doctor_name']}")
        st.markdown(f"**On:** {appt_dt.strftime('%A, %B %d, %Y')}")
        st.markdown(f"**At:** {appt_dt.strftime('%I:%M %p')}")

    if st.button("Manage All Appointments", use_container_width=True, type="secondary"):
        st.switch_page("pages/Appointments.py")

    st.markdown("<br>", unsafe_allow_html=True) # Add some vertical space

    st.subheader("Emergency Contacts 📞")
    st.info("Manage your important contacts for quick access in an emergency.")
    if st.button("Manage Contacts", use_container_width=True, type="secondary"):
        st.switch_page("pages/Emergency_Contacts.py")


# --- LIVE CLOCK LOGIC ---
ist = pytz.timezone('Asia/Kolkata')
while True:
    now_ist = datetime.now(ist)
    time_str = now_ist.strftime("%I:%M:%S %p")
    date_str = now_ist.strftime("%A, %B %d, %Y")
    with clock_placeholder.container():
        st.markdown(f"<h3 style='text-align: right; color: #1E90FF;'>{time_str}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: right; margin-top: -10px;'>{date_str}</p>", unsafe_allow_html=True)

    time.sleep(1)
