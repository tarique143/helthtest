# frontend/pages/Medications.py

import streamlit as st
from streamlit_cookies_manager import CookieManager
import pandas as pd
from datetime import time, datetime, date

from auth.service import (
    TOKEN_COOKIE_NAME, get_medications, add_medication,
    delete_medication, mark_medication_as_taken
)
from components.sidebar import authenticated_sidebar

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="My Medications", page_icon="💊", layout="wide")

# --- AUTHENTICATION & INITIALIZATION ---
cookies = CookieManager()
if not cookies.ready():
    st.spinner()
    st.stop()

token = cookies.get(TOKEN_COOKIE_NAME)
if not token:
    st.warning("You are not logged in. Please log in to continue.")
    st.switch_page("Home.py")

authenticated_sidebar(cookies)

# Initialize session state for the confirmation dialog
if 'confirming_delete_med_id' not in st.session_state:
    st.session_state.confirming_delete_med_id = None

# --- PAGE HEADER ---
st.title("My Medications 💊")
st.markdown("Manage your medication schedule, and mark them as taken for the day.")

# --- ADD NEW MEDICATION FORM (remains the same) ---
with st.expander("➕ Add a New Medication", expanded=False):
    with st.form("new_medication_form", clear_on_submit=True):
        # ... (form code is unchanged)
        st.write("**Medication Details**")
        med_name = st.text_input("Medication Name", placeholder="e.g., Lisinopril")
        med_dosage = st.text_input("Dosage", placeholder="e.g., 1 tablet, 10mg")
        st.write("**Frequency**")
        med_frequency = st.selectbox("How often?", ("Daily", "As Needed"))
        st.write("**Timing**")
        timing_type = st.radio("Choose a timing method:", ("Meal-Related", "Specific Time"), horizontal=True)
        meal_timing, specific_time = None, None
        if timing_type == "Meal-Related":
            meal_timing = st.selectbox("When to take?", ("Before Breakfast", "After Breakfast", "Before Lunch", "After Lunch", "Before Dinner", "After Dinner", "Bedtime"))
        else:
            specific_time_input = st.time_input("Select a time:", value=time(9, 0))
            specific_time = specific_time_input.isoformat() if specific_time_input else None
        submitted = st.form_submit_button("Add Medication")
        if submitted:
            payload = {
                "name": med_name, "dosage": med_dosage, "frequency": med_frequency,
                "timing_type": timing_type, "meal_timing": meal_timing, "specific_time": specific_time
            }
            is_success, message = add_medication(token, payload)
            if is_success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

st.markdown("---")

# --- DISPLAY EXISTING MEDICATIONS ---
st.header("Your Medication List")

is_success, data = get_medications(token)

if not is_success:
    st.error(f"Could not load medications: {data}")
else:
    if not data:
        st.info("You haven't added any medications yet.")
    else:
        for med in data:
            med_id = med['id']
            
            with st.container(border=True):
                # Check if this medication is the one we are confirming to delete
                if st.session_state.confirming_delete_med_id == med_id:
                    st.warning(f"**Are you sure you want to delete {med['name']}?**")
                    col_confirm, col_cancel, col_spacer = st.columns([1, 1, 3])
                    with col_confirm:
                        if st.button("Yes, Delete", key=f"conf_{med_id}", use_container_width=True, type="primary"):
                            del_success, del_message = delete_medication(token, med_id)
                            st.session_state.confirming_delete_med_id = None # Reset state
                            if del_success:
                                st.success(del_message)
                                st.rerun()
                            else:
                                st.error(del_message)
                    with col_cancel:
                        if st.button("Cancel", key=f"cancel_{med_id}", use_container_width=True):
                            st.session_state.confirming_delete_med_id = None # Reset state
                            st.rerun()
                else:
                    # --- Default Display (with "Mark as Taken" and "Delete") ---
                    last_taken_str = med.get('last_taken_at')
                    taken_today = False
                    if last_taken_str:
                        if datetime.fromisoformat(last_taken_str).date() == date.today():
                            taken_today = True

                    col1, col2, col3 = st.columns([4, 2, 2])
                    with col1:
                        display_timing = med['meal_timing'] or pd.to_datetime(med['specific_time']).strftime('%I:%M %p')
                        st.subheader(f"{med['name']} ({med['dosage']})")
                        st.markdown(f"**Timing:** {display_timing} | **Frequency:** {med['frequency']}")
                    
                    with col2:
                        # This button now SETS the session state to trigger the confirmation
                        if st.button("Delete", key=f"del_{med_id}", use_container_width=True):
                            st.session_state.confirming_delete_med_id = med_id
                            st.rerun()

                    with col3:
                        if taken_today:
                            st.button("✅ Taken Today", key=f"taken_{med_id}", use_container_width=True, disabled=True)
                        else:
                            if st.button("Mark as Taken", key=f"mark_{med_id}", use_container_width=True):
                                mark_success, mark_message = mark_medication_as_taken(token, med_id)
                                if mark_success:
                                    st.success(mark_message)
                                    st.rerun()
                                else:
                                    st.error(mark_message)