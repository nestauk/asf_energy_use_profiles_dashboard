"""
Utils for handling data in the dashboard.
"""

# Package imports
import pandas as pd


def check_if_value_exists(df: pd.DataFrame, profile: int, col: str) -> bool:
    """
    Checks if a value is non-missing for a given profile and column.

    Args:
        df (pd.DataFrame): DataFrame containing the data
        profile (int): profile number
        col (str): column name

    Returns:
        bool: True if the value is non-missing, False otherwise
    """
    profile = str(profile)    
    if pd.isnull(df[df["profile"] == profile][col].iloc[0]):
        return False
    return True


def get_avg_population_value(df: pd.DataFrame, col: str) -> float:
    """
    Calculates the percentage of households with a certain characteristic.

    Args:
        df (pd.DataFrame): data
        col (str): column name

    Returns:
        float: percentage of households with the characteristic
    """
    return df[f"counts_{col}"].sum() / df["number_households"].sum() * 100


def get_value_and_delta(profile: int, df: pd.DataFrame, col: str) -> tuple:
    """Helper function to get the value and delta for a given profile and column.
    Args:
        profile (int): profile number
        df (pd.DataFrame): DataFrame containing the data
        col (str): column name to get the value and delta for
    Returns:
        tuple: value and delta as strings
    """
    # In the contextual info df, the profile is stored as a string
    profile = str(profile)

    profile_filt = df[df["profile"] == profile].iloc[0]
    value = profile_filt["proportion_" + col]
    diff = value - get_avg_population_value(df, col)

    value = str(int(value.round(0))) + "%"
    diff = str(int(diff.round(0))) + "%"
    return value, diff
