# frontend/pages/Emergency_Contacts.py

import streamlit as st
from streamlit_cookies_manager import CookieManager

from auth.service import TOKEN_COOKIE_NAME, get_contacts, add_contact, delete_contact
from components.sidebar import authenticated_sidebar

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Emergency Contacts", page_icon="📞", layout="wide")

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
st.title("Emergency Contacts 📞")
st.markdown("Manage your important contacts for quick access.")

# --- ADD NEW CONTACT FORM ---
with st.expander("➕ Add a New Contact", expanded=False):
    with st.form("new_contact_form", clear_on_submit=True):
        contact_name = st.text_input("Contact Name", placeholder="e.g., John Doe")
        phone_number = st.text_input("Phone Number", placeholder="e.g., +91 98765 43210")
        relationship = st.text_input("Relationship", placeholder="e.g., Son, Doctor, Neighbor")

        submitted = st.form_submit_button("Add Contact")
        if submitted:
            if not contact_name or not phone_number:
                st.warning("Please fill in the Contact Name and Phone Number.")
            else:
                payload = {
                    "contact_name": contact_name,
                    "phone_number": phone_number,
                    "relationship_type": relationship
                }
                is_success, message = add_contact(token, payload)
                if is_success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

st.markdown("---")

# --- DISPLAY EXISTING CONTACTS ---
st.header("Your Contact List")

is_success, data = get_contacts(token)

if not is_success:
    st.error(f"Could not load contacts: {data}")
else:
    if not data:
        st.info("You have not added any contacts yet. Use the form above to add one.")
    else:
        # Use columns for a card-like layout
        cols = st.columns(3) # Display up to 3 contacts per row
        for i, contact in enumerate(data):
            col = cols[i % 3]
            with col:
                with st.container(border=True):
                    st.subheader(contact['contact_name'])
                    if contact['relationship_type']:
                        st.caption(f"_{contact['relationship_type']}_")
                    
                    # Make the phone number a clickable link
                    st.link_button(f"📞 Call {contact['phone_number']}", f"tel:{contact['phone_number']}")
                    
                    if st.button("Delete", key=f"del_contact_{contact['id']}", use_container_width=True):
                        del_success, del_message = delete_contact(token, contact['id'])
                        if del_success:
                            st.success(del_message)
                            st.rerun()
                        else:
                            st.error(del_message)