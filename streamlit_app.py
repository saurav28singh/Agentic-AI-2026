"""
Agentic AI Workshop 2026 — Streamlit wrapper.

The website itself is plain HTML, CSS and JavaScript in static/. Streamlit is
used here only as a host: it serves that folder (enableStaticServing in
.streamlit/config.toml) and this script embeds it full-bleed.

Run locally:   streamlit run streamlit_app.py
Deploy:        push to GitHub, then create an app at share.streamlit.io
               pointing at this file.
"""

import streamlit as st

st.set_page_config(
    page_title="Agentic AI Workshop 2026 · IIT Delhi",
    page_icon="static/photos/iitd-crest-red.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Strip Streamlit's own chrome so the site fills the window.
st.markdown(
    """
    <style>
      #MainMenu, header, footer {visibility: hidden;}
      .stAppViewContainer .main .block-container {padding: 0; max-width: 100%;}
      .stAppViewContainer {overflow: hidden;}
      iframe#site {border: 0; width: 100%; height: 100vh; display: block;}
    </style>
    <iframe id="site" src="app/static/index.html" title="Agentic AI Workshop 2026"></iframe>
    """,
    unsafe_allow_html=True,
)
