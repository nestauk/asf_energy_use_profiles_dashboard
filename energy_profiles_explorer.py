"""
This script sets up a Streamlit app 'Energy-use profiles explorer'.

The main function is energy_profiles_explorer() which initializes the app, sets the page configuration, and creates a sidebar menu for navigation. The sidebar allows users to navigate between different pages:
- "About the explorer"
- "Explore the results"
- "Explore an energy-use profile"
- "About the data"

To run this app localy:
streamlit run energy_profiles_explorer.py
"""

## Package imports
import streamlit as st  # For building the web app
import pandas as pd  # For simple data manipulation
from PIL import Image  # For loading images
import altair as alt  # For creating interactive charts with Altair
from streamlit_option_menu import option_menu  # For creating a sidebar menu
import os

# Local imports
from utils.fonts_setup import nestafont, NESTA_COLOURS
from config.css_style import set_css_style
from pages.about_dashboard_page import about_dashboard_page
from pages.overview_results_page import overview_results_page
from pages.select_profile_page import select_profile_page
from pages.about_data_page import about_data_page

# Setting up themes and fonts
alt.themes.register("nestafont", nestafont)
alt.themes.enable("nestafont")
set_css_style()


def set_up_sidebar():
    """
    This function sets up the sidebar with a menu for navigating the app.
    """
    side_bar_options = option_menu(
        menu_title="Energy-use profiles explorer",
        options=[
            "About the explorer",
            "Explore the results",
            "Explore an energy-use profile",
            "About the data",
        ],  # The options to be displayed in the sidebar
        icons=[
            "house",
            "bar-chart",
            "toggles",
            "info-circle",
        ],  # The icons to be displayed next to the options. You can select from: https://icons.getbootstrap.com/
        default_index=0,  # Defaults to the "About this app" page
        orientation="vertical",
        styles={
            "container": {
                "padding": "5!important",
                "background-color": NESTA_COLOURS[12],
            },
            "icon": {"color": NESTA_COLOURS[10], "font-size": "25px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": NESTA_COLOURS[0]},
        },
    )
    return side_bar_options


def energy_profiles_explorer():
    """
    This function will setup a Streamlit app with expanders, sidebar and multiple pages.
    """

    with st.spinner("Loading the Energy-use profiles explorer..."):
        current_dir = os.getcwd()
        favicon = Image.open(f"{current_dir}/images/nesta_favicon.png")
        # Configure your browser tab by adding a title, changing the layout, and adding an icon to appear on your browser tab
        st.set_page_config(
            page_title="Energy-use profiles",
            layout="wide",
            page_icon=favicon,
        )

        with st.sidebar:
            side_bar_options = set_up_sidebar()
        if side_bar_options == "About the explorer":
            nesta_logo = Image.open(f"{current_dir}/images/nesta_logo.png")
            st.image(nesta_logo, width=200)
            about_dashboard_page()
        elif side_bar_options == "Explore the results":
            overview_results_page()
        elif side_bar_options == "Explore an energy-use profile":
            select_profile_page()
        else:
            about_data_page()


energy_profiles_explorer()
