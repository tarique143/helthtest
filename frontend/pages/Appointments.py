# frontend/pages/Appointments.py

import streamlit as st
from streamlit_cookies_manager import CookieManager
import pandas as pd
from datetime import datetime, time, date

# Import ALL necessary functions, including delete_appointment
from auth.service import TOKEN_COOKIE_NAME, get_appointments, add_appointment, delete_appointment
from components.sidebar import authenticated_sidebar

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="My Appointments", page_icon="🗓️", layout="wide")

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
st.title("My Appointments 🗓️")
st.markdown("Here you can manage your doctor appointments.")

# --- ADD NEW APPOINTMENT FORM ---
with st.expander("➕ Add a New Appointment", expanded=False):
    with st.form("new_appointment_form", clear_on_submit=True):
        doc_name = st.text_input("Doctor's Name", placeholder="e.g., Dr. Smith")
        
        col1, col2 = st.columns(2)
        with col1:
            appt_date = st.date_input("Date", min_value=date.today())
        with col2:
            appt_time = st.time_input("Time", value=time(10, 30))
        
        appt_location = st.text_input("Location / Clinic Address", placeholder="e.g., City Hospital, 123 Main St")
        appt_purpose = st.text_area("Purpose of Visit", placeholder="e.g., Annual Check-up, Follow-up")

        submitted = st.form_submit_button("Add Appointment")
        if submitted:
            if not doc_name or not appt_date or not appt_time:
                st.warning("Please fill in the Doctor's Name, Date, and Time.")
            else:
                combined_datetime = datetime.combine(appt_date, appt_time)
                iso_datetime_str = combined_datetime.isoformat()

                payload = {
                    "doctor_name": doc_name,
                    "appointment_datetime": iso_datetime_str,
                    "location": appt_location,
                    "purpose": appt_purpose
                }
                is_success, message = add_appointment(token, payload)
                if is_success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

st.markdown("---")

# --- DISPLAY EXISTING APPOINTMENTS ---
st.header("Your Upcoming Appointments")

is_success, data = get_appointments(token)

if not is_success:
    st.error(f"Could not load appointments: {data}")
else:
    if not data:
        st.info("You have not added any appointments yet. Use the form above to add one.")
    else:
        df = pd.DataFrame(data)
        df['appointment_datetime'] = pd.to_datetime(df['appointment_datetime'])
        
        for index, row in df.iterrows():
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(f"Dr. {row['doctor_name']}")
                    st.write(f"**When:** {row['appointment_datetime'].strftime('%A, %B %d, %Y at %I:%M %p')}")
                    if row['location']:
                        st.write(f"**Where:** {row['location']}")
                    if row['purpose']:
                        st.write(f"**Purpose:** {row['purpose']}")
                with col2:
                    # --- THIS IS THE WORKING DELETE BUTTON LOGIC ---
                    if st.button("Delete", key=f"del_appt_{row['id']}", use_container_width=True):
                        is_del_success, del_message = delete_appointment(token, row['id'])
                        if is_del_success:
                            st.success(del_message)
                            st.rerun()
                        else:
                            st.error(del_message)