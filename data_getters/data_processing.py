"""
Script to process input data required for the energy-use profiles explorer to run.

This script only needs to be run once to generate the required CSV files, by doing:
python data_getters/data_processing.py
"""

import numpy as np
import pandas as pd
import os
import logging

inputs_path = "s3://asf-energy-use-profiles/2nd_phase_results/inputs/"
outputs_path = "s3://asf-energy-use-profiles/2nd_phase_results/outputs/"


def process_df_distribution_households():
    """
    Processes the 'profiles_numbers_and_percentages.xlsx' file by converting
    the 'profile' values from "Profile X" format to just the number X,
    and saves data as a CSV file to S3.
    """
    profile_info = pd.read_excel(
        os.path.join(inputs_path, "profiles_numbers_and_percentages.xlsx"),
    )

    # convert "profile" values from "Profile X" to just the number X
    profile_info["profile"] = profile_info["profile"].apply(
        lambda x: int(x.split(" ")[1])
    )

    profile_info.to_csv(
        os.path.join(outputs_path, "profiles_numbers_and_percentages.csv"), index=False
    )


def process_df_energy_consumption_metrics_per_profile():
    """
    Processes the 'profiles_mean_usage_Wh_and_std.xlsx' file to calculate
    average annual electricity and gas consumption per profile, and saves
    the results as a CSV file to S3.
    """
    profile_annual_avgs = pd.read_excel(
        os.path.join(inputs_path, "profiles_mean_usage_Wh_and_std.xlsx")
    )
    # (half-hourly avg in Wh) x (48 half-hours per day) x (365 days per year) / (1000 to convert to kWh)
    profile_annual_avgs["avg_annual_elec_consumption_kWh"] = (
        profile_annual_avgs["Mean electricity usage"] * 48 * 365 / 1000
    )
    profile_annual_avgs["avg_annual_gas_consumption_kWh"] = (
        profile_annual_avgs["Mean gas usage"] * 48 * 365 / 1000
    )

    profile_annual_avgs = profile_annual_avgs[
        ["profile", "avg_annual_elec_consumption_kWh", "avg_annual_gas_consumption_kWh"]
    ]

    profile_annual_avgs.to_csv(
        os.path.join(outputs_path, "profiles_avg_annual_usage_per_profile.csv"),
        index=False,
    )


def process_hh_consumption_per_profile(
    energy_type: str = "electricity", season: str = ""
):
    """
    Processes the daily average and standard deviation of energy consumption per profile
    for a specific type of energy (electricity or gas) and season (winter/ summer) or all year
    and saves the results as a CSV file to S3.

    Args:
        type (str, optional): "energy_type" for electricity and "gas" for gas. Defaults to "energy_type".
        season (str, optional): "" for all year, "summer" for summer and "winter" for winter. Defaults to "" (all year).
    """
    if season != "":
        season = f"_{season}"

    energy_type = energy_type[:4]  # Ensure energy_type is in the format 'elec' or 'gas'

    daily_avg = pd.read_excel(
        os.path.join(
            inputs_path, f"profiles_avg_{energy_type}_consumption_day{season}.xlsx"
        )
    )
    daily_std = pd.read_excel(
        os.path.join(
            inputs_path, f"profiles_std_{energy_type}_consumption_day{season}.xlsx"
        )
    )

    # Rename "Read\ntime" and "Read time" to "read_time" for consistency
    daily_avg.rename(
        columns={"Read\ntime": "read_time", "Read time": "read_time"}, inplace=True
    )
    daily_std.rename(
        columns={"Read\ntime": "read_time", "Read time": "read_time"}, inplace=True
    )

    # Merge the average and standard deviation DataFrames on "read_time"
    merged = pd.merge(daily_avg, daily_std, on="read_time", suffixes=("_avg", "_std"))

    # Convert "read_time" to string and remove the last 3 characters to follow the HH:MM format
    merged["read_time"] = merged["read_time"].astype(str).str[:-3]

    # Rename columns to follow the format "profile_X_avg" and "profile_X_std" for each profile X
    merged.columns = [col.replace("cluster ", "profile_") for col in merged.columns]

    merged.to_csv(
        os.path.join(
            outputs_path, f"profiles_{energy_type}_consumption_day{season}.csv"
        ),
        index=False,
    )


def _get_raw_contextual_data(name: str):
    """
    Reads the raw contextual data from an Excel file and returns it as a DataFrame.

    Args:
        name (str): The name of the contextual data file to read.

    Returns:
        pd.DataFrame: The raw contextual data.
    """
    return pd.read_excel(os.path.join(inputs_path, f"profiles_{name}_counts.xlsx"))


def _process_contextual_data(
    contextual_data: pd.DataFrame, mapping: dict
) -> pd.DataFrame:
    """
    Processes the contextual data by renaming columns based on a mapping dictionary and
    calculating proportions for each count column relative to the total number of households.

    Args:
        contextual_data (pd.DataFrame): The DataFrame containing the raw contextual data.
        mapping (dict): mapping dictionary where keys are old column names and values are new column names.

    Returns:
        pd.DataFrame: A DataFrame containing the processed contextual data with renamed columns and calculated proportions.
    """
    contextual_data.rename(columns=mapping, inplace=True)

    new_cols = []
    old_cols = []
    for key, value in mapping.items():
        if (value not in ["profile", "number_households"]) and (
            value in contextual_data.columns
        ):
            # Calculate the proportion of each count column relative to the total number of households
            prop_col = f"proportion_{value.split("counts_")[1]}"
            contextual_data[prop_col] = (
                contextual_data[value] / contextual_data["number_households"] * 100
            )

            new_cols.append(prop_col)
            old_cols.append(value)

    all_cols = ["profile", "number_households"] + old_cols + new_cols

    contextual_data = contextual_data[all_cols]
    return contextual_data


def process_contextual_info_imd() -> pd.DataFrame:
    """
    Processes the Index of Multiple Deprivation (IMD) contextual data.

    Returns:
        pd.DataFrame: A DataFrame containing the processed IMD contextual data
    """
    contextual_data = _get_raw_contextual_data("imd")

    mapping = {
        "Cluster": "profile",
        "Total households": "number_households",
        # Index of multiple deprivation (IMD)
        "IMD 1-2": "counts_imd_1_2",
        "IMD 3": "counts_imd_3",
        "IMD 4-5": "counts_imd_4_5",
    }

    contextual_data = _process_contextual_data(contextual_data, mapping)

    return contextual_data


def process_contextual_info_region() -> pd.DataFrame:
    """
    Processes the region contextual data.

    Returns:
        pd.DataFrame: A DataFrame containing the processed region contextual data.
    """
    contextual_data = _get_raw_contextual_data("region")
    mapping = {
        "Cluster": "profile",
        "Total households": "number_households",
        # Region
        "Greater London": "counts_region_greater_london",
        "England (excl. London), Scotland, Wales": "counts_region_other",
    }
    contextual_data = _process_contextual_data(contextual_data, mapping)
    return contextual_data


def process_contextual_info_working_status() -> pd.DataFrame:
    """
    Processes the working status contextual data.

    Returns:
        pd.DataFrame: A DataFrame containing the processed working status contextual data.
    """
    contextual_data = _get_raw_contextual_data("working_status")
    mapping = {
        "Cluster": "profile",
        "Total households": "number_households",
        # Working status
        "All not working": "counts_working_status_all_not_working",
        "All working and/or students": "counts_working_status_all_working_and_or_students",
        "Mix of working and/or students and not working": "counts_working_status_mix",
        "Unknown": "counts_working_status_unknown",
    }
    contextual_data = _process_contextual_data(contextual_data, mapping)
    return contextual_data


def process_contextual_info_single_occupancy() -> pd.DataFrame:
    """
    Processes the single occupancy only contextual data.

    Returns:
        pd.DataFrame: A DataFrame containing the processed single occupancy contextual data.
    """
    contextual_data = _get_raw_contextual_data("single_occupancy")
    mapping = {
        "Cluster": "profile",
        "Total households": "number_households",
        # Single occupancy
        1: "counts_single_occupancy",
    }
    contextual_data = _process_contextual_data(contextual_data, mapping)
    return contextual_data


def process_contextual_info_3plus_occupants() -> pd.DataFrame:
    """
    Processes the 3+ occupants contextual data.

    Returns:
        pd.DataFrame: A DataFrame containing the processed 3+ occupants contextual data.
    """
    contextual_data = _get_raw_contextual_data("3occupants")
    mapping = {
        "Cluster": "profile",
        "Total households": "number_households",
        # 3+ occupants
        "3+": "counts_3plus_occupants",
    }
    contextual_data = _process_contextual_data(contextual_data, mapping)
    return contextual_data


def process_contextual_info_household_composition() -> pd.DataFrame:
    """
    Processes the household composition contextual data.

    Returns:
        pd.DataFrame: A DataFrame containing the processed household composition contextual data.
    """
    contextual_data = _get_raw_contextual_data("household_composition")
    mapping = {
        "Cluster": "profile",
        "Total households": "number_households",
        # Household composition
        "Adult(s) aged 65+ only": "counts_adults_65_plus_only",
        "Adult(s) and child(ren)": "counts_adults_and_children",
    }
    contextual_data = _process_contextual_data(contextual_data, mapping)
    return contextual_data


def process_contextual_info_income(name: str) -> pd.DataFrame:
    """
    Processes the income contextual data based on the specified name.

    Args:
        name (str): The name of the income category to process.

    Returns:
        pd.DataFrame: A DataFrame containing the processed income contextual data.
    """
    contextual_data = _get_raw_contextual_data(name)

    mapping = {
        "Cluster": "profile",
        "Total households": "number_households",
        # Income categories
        "Up to £90,000": "counts_income_90k_below",
        "Above £90,000": "counts_income_above_90k",
        "Up to £30,000": "counts_income_30k_below",
        "£30,000-£90,000": "counts_income_30k_to_90k",
        "Income unknown": "counts_income_unknown",
        "Unknown": "counts_income_unknown",
    }

    contextual_data = _process_contextual_data(contextual_data, mapping)

    return contextual_data


def process_contextual_info_tenure(name) -> pd.DataFrame:
    """
    Processes the tenure contextual data.

    Returns:
        pd.DataFrame: A DataFrame containing the processed tenure contextual data.
    """
    contextual_data = _get_raw_contextual_data(name)
    mapping = {
        "Cluster": "profile",
        "Total households": "number_households",
        # Tenure
        "Rented (private)": "counts_privately_rented",
        "Rented (social)": "counts_social_rented",
        "Owner-occupied, Unknown": "counts_owner_occupier_or_unknown_tenure",
        "Owner-occupied": "counts_owner_occupier",
    }
    contextual_data = _process_contextual_data(contextual_data, mapping)
    return contextual_data


def process_contextual_info_property_built_year() -> pd.DataFrame:
    """
    Processes the property built year contextual data.

    Returns:
        pd.DataFrame: A DataFrame containing the processed property built year contextual data.
    """
    contextual_data = _get_raw_contextual_data("property_built_before_1930")
    mapping = {
        "Cluster": "profile",
        "Total households": "number_households",
        # Property built year
        "Before 1930": "counts_property_built_before_1930",
    }
    contextual_data = _process_contextual_data(contextual_data, mapping)
    return contextual_data


def process_contextual_info_property_type_detached() -> pd.DataFrame:
    """
    Processes the property type contextual data based on the specified name.

    Returns:
        pd.DataFrame: A DataFrame containing the processed property type contextual data.
    """
    contextual_data = _get_raw_contextual_data("property_type_detached")

    mapping = {
        "Cluster": "profile",
        "Total households": "number_households",
        # Property type
        "Detached": "counts_property_type_detached",
    }

    contextual_data = _process_contextual_data(contextual_data, mapping)

    return contextual_data


def process_contextual_info_property_type_flats() -> pd.DataFrame:
    """
    Processes the property type contextual data based on the specified name.

    Returns:
        pd.DataFrame: A DataFrame containing the processed property type contextual data.
    """
    contextual_data = _get_raw_contextual_data("property_type_flats")

    mapping = {
        "Cluster": "profile",
        "Total households": "number_households",
        # Property type
        "Flat, apartment, or maisonette": "counts_property_type_flats_apartments_maisonettes",
    }

    contextual_data = _process_contextual_data(contextual_data, mapping)

    return contextual_data


def process_contextual_info_ev() -> pd.DataFrame:
    """
    Processes the electric vehicle (EV) contextual data.

    Returns:
        pd.DataFrame: A DataFrame containing the processed EV contextual data.
    """
    contextual_data = _get_raw_contextual_data("ev")

    mapping = {
        "Cluster": "profile",
        "Total households": "number_households",
        # Electric Vehicle (EV) ownership
        "EV": "counts_evs",
    }

    contextual_data = _process_contextual_data(contextual_data, mapping)

    return contextual_data


def process_contextual_info_ev_charging() -> pd.DataFrame:
    """
    Processes the electric vehicle (EV) charging contextual data.

    Returns:
        pd.DataFrame: A DataFrame containing the processed EV charging contextual data.
    """
    contextual_data = _get_raw_contextual_data("ev_charging")

    mapping = {
        "Cluster": "profile",
        "Total households": "number_households",
        # Electric Vehicle (EV) charging
        "EV charging": "counts_ev_charging",
    }

    contextual_data = _process_contextual_data(contextual_data, mapping)

    return contextual_data


def process_contextual_info_central_heating_fuel() -> pd.DataFrame:
    """
    Processes the central heating fuel contextual data based on the specified name.

    Returns:
        pd.DataFrame: A DataFrame containing the processed central heating contextual data.
    """
    contextual_data = _get_raw_contextual_data("ch_fuel")

    mapping = {
        "Cluster": "profile",
        "Total households": "number_households",
        # Central heating fuel
        "Electric only": "counts_ch_electric_only",
        "Gas only": "counts_ch_gas_only",
    }

    contextual_data = _process_contextual_data(contextual_data, mapping)

    return contextual_data


def process_contextual_info_heat_pumps() -> pd.DataFrame:
    """
    Processes the heat pumps contextual data.

    Returns:
        pd.DataFrame: A DataFrame containing the processed heat pumps contextual data.
    """
    contextual_data = _get_raw_contextual_data("hp")

    mapping = {
        "Cluster": "profile",
        "Total households": "number_households",
        # Heat pumps
        "Heat pump": "counts_heat_pumps",
    }

    contextual_data = _process_contextual_data(contextual_data, mapping)

    return contextual_data


def process_contextual_info_ac() -> pd.DataFrame:
    """
    Processes the air conditioning (AC) contextual data.

    Returns:
        pd.DataFrame: A DataFrame containing the processed AC contextual data.
    """
    contextual_data = _get_raw_contextual_data("ac")

    mapping = {
        "Cluster": "profile",
        "Total households": "number_households",
        # Air conditioning
        "Air conditioning unit": "counts_ac",
    }

    contextual_data = _process_contextual_data(contextual_data, mapping)

    return contextual_data


def process_contextual_info_solar_panels() -> pd.DataFrame:
    """
    Processes the solar panels contextual data.

    Returns:
        pd.DataFrame: A DataFrame containing the processed solar panels contextual data.
    """
    contextual_data = _get_raw_contextual_data("solar_panels")

    mapping = {
        "Cluster": "profile",
        "Total households": "number_households",
        # Solar panels
        "solar panels": "counts_solar_panels",
    }

    contextual_data = _process_contextual_data(contextual_data, mapping)

    return contextual_data


def process_contextual_info_battery_storage() -> pd.DataFrame:
    """
    Processes the battery storage contextual data.

    Returns:
        pd.DataFrame: A DataFrame containing the processed battery storage contextual data.
    """
    contextual_data = _get_raw_contextual_data("battery_storage")

    mapping = {
        "Cluster": "profile",
        "Total households": "number_households",
        # Battery storage
        "Battery storage": "counts_battery_storage",
    }

    contextual_data = _process_contextual_data(contextual_data, mapping)

    return contextual_data


def process_contextual_info_smart_heating_controls() -> pd.DataFrame:
    """
    Processes the smart heating controls contextual data.

    Returns:
        pd.DataFrame: A DataFrame containing the processed smart heating controls contextual data.
    """
    contextual_data = _get_raw_contextual_data("smart_heating_controls")

    mapping = {
        "Cluster": "profile",
        "Total households": "number_households",
        # Smart heating controls
        "Smart heating controls": "counts_smart_heating_controls",
    }

    contextual_data = _process_contextual_data(contextual_data, mapping)

    return contextual_data


def process_contextual_information():
    """
    Processes all contextual information and saves it as a CSV file to S3.
    """

    # Let's start by reading and processing in the IMD data
    contextual_data = process_contextual_info_imd()

    # Now we can process the rest of the contextual information
    region = process_contextual_info_region()
    working_status = process_contextual_info_working_status()
    single_occupancy = process_contextual_info_single_occupancy()
    three_plus_occupants = process_contextual_info_3plus_occupants()
    household_composition = process_contextual_info_household_composition()
    income = process_contextual_info_income("income")
    income_over_90k = process_contextual_info_income("income_over_90k")
    # income_up_to_30k = process_contextual_info_income("income_up_to_30k")
    tenure = process_contextual_info_tenure("tenure")
    owner_occupier = process_contextual_info_tenure("owner_occupier")
    property_built_year = process_contextual_info_property_built_year()
    property_type_detached = process_contextual_info_property_type_detached()
    property_type_flats = process_contextual_info_property_type_flats()
    ev = process_contextual_info_ev()
    ev_charging = process_contextual_info_ev_charging()
    central_heating_fuel = process_contextual_info_central_heating_fuel()
    hp = process_contextual_info_heat_pumps()
    ac = process_contextual_info_ac()
    solar_panels = process_contextual_info_solar_panels()
    batery_storage = process_contextual_info_battery_storage()
    smart_heating_controls = process_contextual_info_smart_heating_controls()

    all_other_data = [
        region,
        working_status,
        single_occupancy,
        three_plus_occupants,
        household_composition,
        income,
        income_over_90k,
        # income_up_to_30k,
        tenure,
        owner_occupier,
        property_built_year,
        property_type_detached,
        property_type_flats,
        ev,
        ev_charging,
        central_heating_fuel,
        hp,
        ac,
        solar_panels,
        batery_storage,
        smart_heating_controls,
    ]

    for df in all_other_data:
        # Remove the "All clusters" lines, as we don't need them
        contextual_data = contextual_data[contextual_data["profile"] != "All clusters"]

        # Ensure the number of households is NaN for the "Count of other clusters" profile
        # Since we already have the number of households in the numbered profiles
        contextual_data["number_households"] = np.where(
            contextual_data["profile"] == "Count of other clusters",
            np.nan,
            contextual_data["number_households"],
        )

        # Merge the data
        contextual_data = pd.merge(
            contextual_data, df, on=["profile", "number_households"], how="outer"
        )

    contextual_data.to_csv(
        os.path.join(outputs_path, "profiles_contextual_information.csv"), index=False
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    logging.info("Starting data processing...")

    process_df_distribution_households()
    process_df_energy_consumption_metrics_per_profile()
    process_hh_consumption_per_profile("electricity")
    process_hh_consumption_per_profile("gas")
    process_hh_consumption_per_profile("electricity", "summer")
    process_hh_consumption_per_profile("electricity", "winter")
    process_hh_consumption_per_profile("gas", "summer")
    process_hh_consumption_per_profile("gas", "winter")
    process_contextual_information()

    logging.info(
        f"Data processing completed successfully. All files saved to S3: {outputs_path}"
    )
