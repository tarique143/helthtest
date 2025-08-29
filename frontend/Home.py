# frontend/Home.py

import streamlit as st
from streamlit_cookies_manager import CookieManager
from auth.service import login_user, TOKEN_COOKIE_NAME

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Senior Citizen Support Hub",
    page_icon="assets/icon.png",
    layout="wide",
    initial_sidebar_state="collapsed",
    # theme="auto"
)

# --- INITIALIZE COOKIE MANAGER ---
# This must be initialized at the top of the script.
cookies = CookieManager()

# --- WAIT FOR COOKIES TO BE READY ---
# This is the most important part. The script will wait here until the browser
# has sent its cookies to the Streamlit backend.
if not cookies.ready():
    # Show a spinner and stop execution until cookies are ready
    st.spinner()
    st.stop()

# --- PERSISTENT LOGIN CHECK ---
# Now that we know cookies are ready, we can safely check for the token.
token = cookies.get(TOKEN_COOKIE_NAME)
if token:
    st.switch_page("pages/Dashboard.py")

# --- PAGE LAYOUT ---
# This part of the code will only run if the user is NOT logged in.
st.title("Senior Citizen Medical Reminder & Support Website")
st.markdown("---")

col1, col2 = st.columns([1.5, 1], gap="large")

with col1:
    st.header("Welcome!")
    st.markdown("""
        <div style="font-size: 18px;">
        We are here to help you take care of your health.
        This website acts as your digital assistant, designed to help you remember:
        <ul>
            <li>💊 The right time to take your medications.</li>
            <li>🗓️ Your upcoming appointments with the doctor.</li>
            <li>📞 Your family's contact numbers in case of an emergency.</li>
        </ul>
        Using this platform is very simple. To get started, please log in to your account.
        If you are a new user, you can easily create an account by clicking the 'Register' button.
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.subheader("Login to Your Account")
    
    with st.form("login_form"):
        email = st.text_input("Email Address", placeholder="Enter your email here")
        password = st.text_input("Password", type="password", placeholder="Enter your password here")
        remember_me = st.checkbox("Remember Me")
        submitted = st.form_submit_button("Login")

        if submitted:
            if not email or not password:
                st.warning("Please enter both email and password.")
            else:
                with st.spinner("Logging you in..."):
                    is_success, data = login_user(email, password)
                
                if is_success:
                    # Save the token to the cookie
                    token_data = data.get("access_token")
                    if token_data:
                       cookies[TOKEN_COOKIE_NAME] = token_data
                       
                        
                    
                    st.success("Login Successful!")
                    st.rerun() # Re-run the script. The check at the top will redirect.
                else:
                    st.error(data)

    st.markdown("---")
    st.write("Don't have an account or forgot your password?")
    col_register, col_forgot = st.columns(2)

    with col_register:
        if st.button("New User? Register Here", use_container_width=True):
            st.switch_page("pages/Register.py")
    with col_forgot:
        if st.button("Forgot Password?", use_container_width=True):
            st.switch_page("pages/Forgot_Password.py")