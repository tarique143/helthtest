# frontend/components/custom_css.py

import streamlit as st
from pathlib import Path

def load_css():
    """Loads the custom CSS file into the Streamlit app."""
    # Construct the absolute path to the CSS file
    css_file_path = Path(__file__).parent.parent / "assets" / "style.css"
    try:
        with open(css_file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # This can be helpful for debugging if the path is wrong
        st.warning(f"Custom CSS file not found at path: {css_file_path}")