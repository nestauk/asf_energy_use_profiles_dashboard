"""
.streamlit/config.toml provides the configuration for the Streamlit app.

Additional configuration options require CSS styling to be applied globally.
This file sets the CSS style for the Streamlit app to center the metrics and
use the Averta font globally and it ensures that all UI elements use this font.
"""

import streamlit as st


def set_css_style():
    """
    This function sets the CSS style for the Streamlit app.
    It applies the Averta font globally and ensures that all UI elements use this font.
    """
    st.markdown(
        """
        <style>
        @font-face {
            font-family: 'Averta';
            src: url('https://github.com/deblynprado/neon/blob/master/fonts/averta/Averta-Regular.woff2') format('woff2');
            font-weight: normal;
            font-style: normal;
        }

        /* Apply Averta font globally to all Streamlit UI elements */
        html, body, .stApp, .stMarkdown,
        .stButton button, .stMetric, .stMarkdown, .stTextInput, .stNumberInput,
        .stSelectbox, .stSidebar, .stHeader, h1, h2, h3, h4, h5, h6, label, div {
            font-family: 'Averta', sans-serif !important;
        }

        /* Extra to make metrics numbers and labels use Averta */
        .stMetric > div:nth-child(1),  /* metric value */
        .stMetric > div:nth-child(2)   /* metric label */ {
            font-family: 'Averta', sans-serif !important;
        }

        [data-testid="stMetric"] {
        text-align: center;
        padding: 15px 0;
        }

        [data-testid="stMetricLabel"] {
        display: flex;
        justify-content: center;
        align-items: center;
        }

        [data-testid="stMetricDeltaIcon-Up"] {
            position: relative;
            left: 15%;
            -webkit-transform: translateX(-50%);
            -ms-transform: translateX(-50%);
            transform: translateX(-50%);
        }

        [data-testid="stMetricDeltaIcon-Down"] {
            position: relative;
            left: 15%;
            -webkit-transform: translateX(-50%);
            -ms-transform: translateX(-50%);
            transform: translateX(-50%);
        }

            </style>
        """,
        unsafe_allow_html=True,
    )
