"""
Data getters used by the energy-use profiles explorer.
"""

import pandas as pd
import streamlit as st
import os

outputs_path = "s3://nesta-open-data/asf_energy_use_profiles_explorer/"


st.cache_data(show_spinner="Loading data...")


def get_distribution_households() -> pd.DataFrame:
    """
    Get the CSV with distribution of households per profile (numbers and percentages).
    Contains three columns:
       - "profile"
       - "number_of_households"
       - "perc_of_households"

    Returns:
        pd.DataFrame: A DataFrame containing the distribution of households per profile.
    """
    profile_info = pd.read_csv(
        os.path.join(outputs_path, "profiles_numbers_and_percentages.csv")
    )
    return profile_info


st.cache_data(show_spinner="Loading data...")


def get_annual_energy_consumption_avg_per_profile() -> pd.DataFrame:
    """
    Get the CSV with average annual electricity and gas consumption per profile.
    Contains three columns:
        - "profile"
        - "avg_annual_elec_consumption_kWh"
        - "avg_annual_gas_consumption_kWh"

    Returns:
        pd.DataFrame: A DataFrame containing the average annual energy consumption per profile.
    """
    profile_annual_avgs = pd.read_csv(
        os.path.join(outputs_path, "profiles_avg_annual_usage_per_profile.csv")
    )
    return profile_annual_avgs


st.cache_data(show_spinner="Loading data...")


def get_hh_consumption_per_profile(
    energy_type: str = "electricity", season: str = ""
) -> pd.DataFrame:
    """
    Get the daily average and standard deviation of energy consumption per profile
    for a specific type of energy (electricity or gas) and season (winter/ summer) or all year.

    Average and standard deviation data are merged into a single DataFrame, with the following columns:
    - read_time: the time of the day (HH:MM format)
    - profile_X_avg: average consumption for profile X (for all profiles, where X is the profile number) in Wh
    - profile_X_std: standard deviation of consumption for profile X (for all profiles, where X is the profile number)

    Args:
        type (str, optional): "energy_type" for electricity and "gas" for gas. Defaults to "energy_type".
        season (str, optional): "" for all year, "summer" for summer and "winter" for winter. Defaults to "" (all year).

    Returns:
        pd.DataFrame: A DataFrame containing the daily average and standard deviation of energy consumption per profile.
    """
    if season != "":
        season = f"_{season}"

    energy_type = energy_type[:4]  # Ensure energy_type is in the format 'elec' or 'gas'

    daily_data = pd.read_csv(
        os.path.join(
            outputs_path, f"profiles_{energy_type}_consumption_day{season}.csv"
        )
    )

    return daily_data


st.cache_data(show_spinner="Loading data...")


def get_contextual_information() -> pd.DataFrame:
    """
    Get the CSV with contextual information about the profiles.
    Contains columns:
        - "profile"
        - "number_households"
        - proportions and counts for a variety of contextual household and property information

    Returns:
        pd.DataFrame: A DataFrame containing the contextual information about the profiles.
    """
    context_info = pd.read_csv(
        os.path.join(outputs_path, "profiles_contextual_information.csv")
    )
    return context_info
