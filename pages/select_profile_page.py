"""
Page for selecting and exploring a specific energy-use profile.

The main function is select_profile_page() which sets up the page.
"""

## Package imports
import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

# Local imports
from config.fonts_setup import nestafont, NESTA_COLOURS
from config import configs
from getters import data_getters as dg
from utils.data_vis_utils import (
    create_chart_daily_consumption,
    create_chart_comparing_daily_consumption_summer_winter,
    setup_coloured_bars,
)
from utils.data_handling_utils import (
    check_if_value_exists,
    get_avg_population_value,
    get_value_and_delta,
)
from config.highlights import highlights

# Setting up themes and fonts
alt.themes.register("nestafont", nestafont)
alt.themes.enable("nestafont")

# Loading the data
distribution_households = dg.get_distribution_households()
profile_annual_avgs = dg.get_annual_energy_consumption_avg_per_profile()
elec_hh_data = dg.get_hh_consumption_per_profile(energy_type="electricity")
gas_hh_data = dg.get_hh_consumption_per_profile(energy_type="gas")
elec_hh_data_summer = dg.get_hh_consumption_per_profile(
    energy_type="electricity", season="summer"
)
elec_hh_data_winter = dg.get_hh_consumption_per_profile(
    energy_type="electricity", season="winter"
)
gas_hh_data_summer = dg.get_hh_consumption_per_profile(
    energy_type="gas", season="summer"
)
gas_hh_data_winter = dg.get_hh_consumption_per_profile(
    energy_type="gas", season="winter"
)
contextual_data = dg.get_contextual_information()


def initial_setup() -> int:
    """
    This function sets up the initial configuration for the 'Select a profile' page.

    Returns:
        int: The selected profile number.
    """
    # List of profiles to select from in the format "Profile X: Y% of the population"
    options = [
        f"Profile {i}: {(int(round(distribution_households["perc_of_households"].iloc[i-1])))}% of the population"
        for i in range(1, 11)
    ]

    # Create a selectbox for profile selection centered in the page (making use of columns)
    col_1, profile_selector_col, col_2 = st.columns((1, 2, 1))
    with profile_selector_col:
        profile_selector = st.selectbox(
            label="Choose one energy-use profile", options=options, width=500
        )

    # Extract the profile number from the selected option
    profile_selector = int(
        profile_selector.split()[1].split(":")[0]
    )  # Extract the profile number from the string

    # Provide a paragraph with some highlights about this profile
    st.markdown(
        f"##### Overview: profile {profile_selector} " + highlights[profile_selector]
    )
    return profile_selector


def setup_profile_main_metrics(profile_selector: int):
    """
    Sets up the section for displaying information about the selected energy-use profile
    including:
    - Number and proportion of households in the profile
    - Average annual electricity and gas consumption

    Args:
        profile_selector (int): profile number selected by the user.
    """

    # METRICS AT THE TOP
    profile_nums_filtered = distribution_households[
        distribution_households["profile"] == profile_selector
    ].iloc[0]

    col_1, n_households, perc_households, col_2 = st.columns(4)

    n_households.metric(
        label="Number of households",
        value=str(int(profile_nums_filtered["number_of_households"])),
        border=True,
    )
    perc_households.metric(
        label="Percentage of households",
        value=str(int(profile_nums_filtered["perc_of_households"].round(0))) + "%",
        border=True,
    )

    profile_annual_avgs_filtered = profile_annual_avgs[
        profile_annual_avgs["profile"] == profile_selector
    ].iloc[0]

    col_3, avg_annual_elc, col_4 = st.columns(3)
    avg_annual_elc.metric(
        label="Average annual electricity consumption",
        value=str(
            int(
                profile_annual_avgs_filtered["avg_annual_elec_consumption_kWh"].round(0)
            )
        )
        + " kWh",
        border=True,
    )
    if profile_selector not in configs.profiles_low_gas_count:
        col_5, avg_annual_gas, col_6 = st.columns(3)

        avg_annual_gas.metric(
            label="Average annual gas consumption",
            value=str(
                int(
                    profile_annual_avgs_filtered[
                        "avg_annual_gas_consumption_kWh"
                    ].round(0)
                )
            )
            + " kWh",
            border=True,
        )

    # with st.sidebar:
    #     st.markdown("Profile consumption values in comparison")
    #     elec_color, gas_color = st.columns(2)

    #     with elec_color:
    #         elec_color_chart = setup_coloured_bars(
    #             min_val=profile_annual_avgs["avg_annual_elec_consumption_kWh"].min(),
    #             max_val=profile_annual_avgs["avg_annual_elec_consumption_kWh"].max(),
    #             value=profile_annual_avgs[
    #                 profile_annual_avgs["profile"] == profile_selector
    #             ]["avg_annual_elec_consumption_kWh"].iloc[0],
    #             energy_type="Electricity",
    #         )
    #         st.altair_chart(elec_color_chart, use_container_width=True)

    #     if profile_selector not in configs.profiles_low_gas_count:
    #         with gas_color:
    #             gas_color_chart = setup_coloured_bars(
    #                 min_val=profile_annual_avgs["avg_annual_gas_consumption_kWh"].min(),
    #                 max_val=profile_annual_avgs["avg_annual_gas_consumption_kWh"].max(),
    #                 value=profile_annual_avgs[
    #                     profile_annual_avgs["profile"] == profile_selector
    #                 ]["avg_annual_gas_consumption_kWh"].iloc[0],
    #                 energy_type="Gas",
    #             )
    #             st.altair_chart(gas_color_chart, use_container_width=True)


def setup_daily_consumption_charts(profile_selector: int):
    """
    Sets up the section for displaying daily consumption charts for electricity
    and gas for the selected energy-use profile

    Args:
        profile_selector (int): profile number selected by the user.
    """
    if profile_selector not in configs.profiles_low_gas_count:
        elec_col, gas_col = st.columns(2)

        with gas_col:
            final_chart = create_chart_daily_consumption(
                daily_data=gas_hh_data,
                profile=profile_selector,
                energy_type="gas",
                colour=NESTA_COLOURS[1],
            )
            st.altair_chart(final_chart, use_container_width=True)

        st.markdown(
            "Note that, although graphs are side by side, the range of consumption values might be different for electricity and gas (see y-axis values)."
        )
    else:
        col_1, elec_col, col_2 = st.columns((1, 2, 1))

        st.markdown(
            "Due to the minimal number of on-gas households in this profiles, gas consumption information isn't provided as it wouldn't accurately represent this group."
        )

    with elec_col:
        final_chart = create_chart_daily_consumption(
            daily_data=elec_hh_data,
            profile=profile_selector,
            energy_type="electricity",
            colour=NESTA_COLOURS[0],
        )
        st.altair_chart(final_chart, use_container_width=True)


def setup_seasonal_patterns_expander(profile_selector: int):
    """
    Sets up the section for displaying seasonal patterns of daily consumption

    Args:
        profile_selector (int): profile number selected by the user.
    """
    elec_col, gas_col = st.columns(2)

    with elec_col:
        final_chart = create_chart_comparing_daily_consumption_summer_winter(
            daily_data_summer=elec_hh_data_summer,
            daily_data_winter=elec_hh_data_winter,
            profile=profile_selector,
            energy_type="electricity",
            colour=NESTA_COLOURS[0],
        )
        st.altair_chart(final_chart, use_container_width=True)
    with gas_col:
        if profile_selector not in configs.profiles_low_gas_count:
            final_chart = create_chart_comparing_daily_consumption_summer_winter(
                daily_data_summer=gas_hh_data_summer,
                daily_data_winter=gas_hh_data_winter,
                profile=profile_selector,
                energy_type="gas",
                colour=NESTA_COLOURS[1],
            )
            st.altair_chart(final_chart, use_container_width=True)


def setup_additional_household_info_expander(profile_selector: int):
    """
    Sets up an expander for additional household information metrics,
    if at least one of the household information metrics is missing.
    """
    at_least_one_missing_household_info = not (
        check_if_value_exists(
            contextual_data, profile_selector, "counts_single_occupancy"
        )
        and check_if_value_exists(
            contextual_data, profile_selector, "counts_privately_rented"
        )
    )
    if at_least_one_missing_household_info:
        with st.expander(
            "Expand for more household-related information", width=1000, icon="⬇️"
        ):
            if not check_if_value_exists(
                contextual_data, profile_selector, "counts_single_occupancy"
            ):
                single_pop = get_avg_population_value(
                    contextual_data, "single_occupancy"
                ).round(1)
                st.write(
                    f"Single occupancy data is not available for this profile due to low counts. {single_pop}% of households in the whole dataset are single occupancy."
                )
            if not check_if_value_exists(
                contextual_data, profile_selector, "counts_privately_rented"
            ):
                tenure_pop = get_avg_population_value(
                    contextual_data, "privately_rented"
                ).round(1)
                st.write(
                    f"Tenure data is not available for this profile due to low counts. {tenure_pop}% of households in the whole dataset are privately rented."
                )


def setup_household_info_section(profile_selector: int):
    """
    Sets up the section for displaying household information metrics for the selected energy-use profile,
    including:
    - Household composition metrics
    - Occupancy metrics
    - Working status metrics
    - Income metrics
    - Tenure metrics

    Args:
        profile_selector (int): profile number selected by the user.
    """
    st.markdown("### 👨‍👩‍👧‍👦 Household information")
    st.markdown(
        "In this section you can find information about the households in this profile, such as household composition, occupancy, working status, income and tenure."
    )

    if check_if_value_exists(
        contextual_data, profile_selector, "counts_single_occupancy"
    ):
        # Age of households occupants and number of occupants
        hc_65p_col, hc_adults_child_col, occ_3more_col, occ_single_col = st.columns(
            (1, 1, 1, 1)
        )
        occ_single_value, occ_single_diff = get_value_and_delta(
            profile_selector, contextual_data, "single_occupancy"
        )
        occ_single_col.metric(
            label="Households with single occupants only",
            value=occ_single_value,
            delta=occ_single_diff,
            border=True,
        )
    else:
        hc_65p_col, hc_adults_child_col, occ_3more_col = st.columns((1, 1, 1))

    if check_if_value_exists(  # when missing for privately rented, also missing for other tenures
        contextual_data, profile_selector, "counts_privately_rented"
    ):

        priv_rented_prop_col, social_rented_prop_col, owner_occup_prop_col = st.columns(
            (1, 1, 1)
        )
        priv_rented_value, priv_rented_diff = get_value_and_delta(
            profile_selector, contextual_data, "privately_rented"
        )
        social_rented_value, social_rented_diff = get_value_and_delta(
            profile_selector, contextual_data, "social_rented"
        )
        owner_occup_value, owner_occup_diff = get_value_and_delta(
            profile_selector, contextual_data, "owner_occupier_or_unknown_tenure"
        )

        priv_rented_prop_col.metric(
            label="Rented (private) households",
            value=priv_rented_value,
            delta=priv_rented_diff,
            border=True,
        )
        social_rented_prop_col.metric(
            label="Rented (social) households",
            value=social_rented_value,
            delta=social_rented_diff,
            border=True,
        )
        owner_occup_prop_col.metric(
            label="Owner occupiers or unknown tenure households",
            value=owner_occup_value,
            delta=owner_occup_diff,
            border=True,
        )

    all_not_working_col, all_working_or_students_col, mix_col = st.columns((1, 1, 1))
    col_3, income_90k_below_col, income_over_90k_col, col_4 = st.columns((1, 1, 1, 1))

    hc_65p_value, hc_65p_diff = get_value_and_delta(
        profile_selector, contextual_data, "adults_65_plus_only"
    )
    hc_adults_child_value, hc_adults_child_diff = get_value_and_delta(
        profile_selector, contextual_data, "adults_and_children"
    )
    occ_3more_value, occ_3more_diff = get_value_and_delta(
        profile_selector, contextual_data, "3plus_occupants"
    )

    hc_65p_col.metric(
        label="Households with 65+ year olds only",
        value=hc_65p_value,
        delta=hc_65p_diff,
        border=True,
    )
    hc_adults_child_col.metric(
        label="Households with adults and children",
        value=hc_adults_child_value,
        delta=hc_adults_child_diff,
        border=True,
    )
    occ_3more_col.metric(
        label="Households with 3+ occupants",
        value=occ_3more_value,
        delta=occ_3more_diff,
        border=True,
    )

    all_not_working_value, all_not_working_diff = get_value_and_delta(
        profile_selector, contextual_data, "working_status_all_not_working"
    )
    all_working_or_students_value, all_working_or_students_diff = get_value_and_delta(
        profile_selector, contextual_data, "working_status_all_working_and_or_students"
    )
    mix_value, mix_diff = get_value_and_delta(
        profile_selector, contextual_data, "working_status_mix"
    )

    all_not_working_col.metric(
        label="Households with all not working",
        value=all_not_working_value,
        delta=all_not_working_diff,
        border=True,
    )
    all_working_or_students_col.metric(
        label="Households with all working or students",
        value=all_working_or_students_value,
        delta=all_working_or_students_diff,
        border=True,
    )
    mix_col.metric(
        label="Households with mixed working status",
        value=mix_value,
        delta=mix_diff,
        border=True,
    )

    income_above_90k_value, income_above_90k_diff = get_value_and_delta(
        profile_selector, contextual_data, "income_above_90k"
    )
    income_90k_below_value, income_90k_below_diff = get_value_and_delta(
        profile_selector, contextual_data, "income_90k_below"
    )

    income_90k_below_col.metric(
        label="Households with income of £90k or below",
        value=income_90k_below_value,
        delta=income_90k_below_diff,
        border=True,
    )
    income_over_90k_col.metric(
        label="Households with income above £90k",
        value=income_above_90k_value,
        delta=income_above_90k_diff,
        border=True,
    )

    setup_additional_household_info_expander(profile_selector)


def setup_additional_property_info_expander(missing_flats_info: bool):
    """
    Sets up an expander for additional property information metrics,
    if at least one of the property information metrics is missing.

    Args:
        missing_flats_info (bool): True if flats, apartments or maisonettes data is missing for the profile.
    """
    with st.expander(
        "Expand for more property-related information", width=1000, icon="⬇️"
    ):
        st.markdown(
            """
                Note on IMD quintiles: The IMD quintile reflects the deprivation of a geographical area, not of an individual household. Therefore, a household in a highly deprived area is not necessarily deprived itself, just as a household in a less deprived area is not necessarily affluent.
                """
        )

        if missing_flats_info:
            flats_pop = get_avg_population_value(
                contextual_data, "property_type_flats_apartments_maisonettes"
            ).round(1)
            st.write(
                f"Flats, apartments or maisonettes data is not available for this profile due to low counts. {flats_pop}% of households in the whole dataset are flats, apartments or maisonettes."
            )


def setup_property_information_section(profile_selector: int):
    """
    Sets up the section for displaying property information metrics for the selected energy-use profile,

    Args:
        profile_selector (int): profile number selected by the user.
    """
    # FIRST LINE OF METRICS
    imd_1_2_col, imd_3_col, imd_4_5_col, london_col = st.columns((1, 1, 1, 1))

    imd_1_2_value, imd_1_2_diff = get_value_and_delta(
        profile_selector, contextual_data, "imd_1_2"
    )
    imd_3_value, imd_3_diff = get_value_and_delta(
        profile_selector, contextual_data, "imd_3"
    )
    imd_4_5_value, imd_4_5_diff = get_value_and_delta(
        profile_selector, contextual_data, "imd_4_5"
    )
    london_value, london_diff = get_value_and_delta(
        profile_selector, contextual_data, "region_greater_london"
    )

    imd_1_2_col.metric(
        label="Properties in IMD 1-2 quintile areas",
        value=imd_1_2_value,
        delta=imd_1_2_diff,
        border=True,
    )
    imd_3_col.metric(
        label="Properties in IMD 3 quintile areas",
        value=imd_3_value,
        delta=imd_3_diff,
        border=True,
    )
    imd_4_5_col.metric(
        label="Properties in IMD 4-5 quintile areas",
        value=imd_4_5_value,
        delta=imd_4_5_diff,
        border=True,
    )
    london_col.metric(
        label="Properties in Greater London",
        value=london_value,
        delta=london_diff,
        border=True,
    )

    if check_if_value_exists(
        contextual_data,
        profile_selector,
        "counts_property_type_flats_apartments_maisonettes",
    ):
        built_before_1930_col, detached_col, flats_col = st.columns((1, 1, 1))
        flats_value, flats_diff = get_value_and_delta(
            profile_selector,
            contextual_data,
            "property_type_flats_apartments_maisonettes",
        )
        flats_col.metric(
            label="Flats, apartments or maisonettes",
            value=flats_value,
            delta=flats_diff,
            border=True,
        )
        missing_flats_info = False
    else:
        col_5, built_before_1930_col, detached_col, col_6 = st.columns((1, 1, 1, 1))
        missing_flats_info = True

    setup_additional_property_info_expander(missing_flats_info=missing_flats_info)

    built_before_1930_value, built_before_1930_diff = get_value_and_delta(
        profile_selector, contextual_data, "property_built_before_1930"
    )

    detached_value, detached_diff = get_value_and_delta(
        profile_selector, contextual_data, "property_type_detached"
    )

    built_before_1930_col.metric(
        label="Properties built before 1930",
        value=built_before_1930_value,
        delta=built_before_1930_diff,
        border=True,
    )
    detached_col.metric(
        label="Detached houses",
        value=detached_value,
        delta=detached_diff,
        border=True,
    )


def setup_additional_central_heating_and_technologies_expander(profile_selector: int):
    """
    Sets up an expander for additional central heating and technologies metrics,
    if at least one of the central heating and technologies metrics is missing.

    Args:
        profile_selector (int): profile number selected by the user.
    """

    at_least_one_missing_tech_info = not (
        check_if_value_exists(contextual_data, profile_selector, "counts_ev_charging")
        and check_if_value_exists(
            contextual_data, profile_selector, "counts_heat_pumps"
        )
        and check_if_value_exists(
            contextual_data, profile_selector, "counts_battery_storage"
        )
        and check_if_value_exists(
            contextual_data, profile_selector, "counts_ch_electric_only"
        )
    )

    if at_least_one_missing_tech_info:
        with st.expander(
            "Expand for more technology-related information", width=1000, icon="⬇️"
        ):
            if not check_if_value_exists(
                contextual_data, profile_selector, "counts_ev_charging"
            ):
                ev_pop = get_avg_population_value(contextual_data, "ev_charging").round(
                    1
                )
                st.write(
                    f"EV charging data is not available for this profile due to low counts. {ev_pop}% of households in the whole dataset have EV charging points."
                )
            if not check_if_value_exists(
                contextual_data, profile_selector, "counts_heat_pumps"
            ):
                hp_pop = get_avg_population_value(contextual_data, "heat_pumps").round(
                    1
                )
                st.write(
                    f"Heat pumps data is not available for this profile due to low counts. {hp_pop}% of households in the whole dataset have heat pumps."
                )
            if not check_if_value_exists(
                contextual_data, profile_selector, "counts_battery_storage"
            ):
                battery_pop = get_avg_population_value(
                    contextual_data, "battery_storage"
                ).round(1)
                st.write(
                    f"Battery storage data is not available for this profile due to low counts. {battery_pop}% of households in the whole dataset have battery storage."
                )
            if not check_if_value_exists(
                contextual_data, profile_selector, "counts_ch_electric_only"
            ):
                ch_fuel_pop = get_avg_population_value(
                    contextual_data, "ch_electric_only"
                ).round(1)
                st.write(
                    f"Central heating fuel data is not available for this profile due to low counts. {ch_fuel_pop}% of households in the whole dataset have electric central heating only."
                )


def setup_central_heating_and_technologies_section(profile_selector: int):
    """
    Sets up the section for displaying central heating and presence of technologies metrics
    for the selected energy-use profile, including:
    - Central heating fuel metrics
    - Presence of smart heating controls
    - Presence of solar panels
    - Presence of electric vehicles
    - Presence of air conditioning
    - Presence of heat pumps
    - Presence of battery storage
    - Presence of EV charging points

    Args:
        profile_selector (int): profile number selected by the user.
    """

    # We create 3 lines of metrics
    smart_heating_col, solar_col, ev_col, ac_col = st.columns((1, 1, 1, 1))
    if check_if_value_exists(
        contextual_data, profile_selector, "counts_battery_storage"
    ) and check_if_value_exists(contextual_data, profile_selector, "counts_heat_pumps"):
        battery_col, hp_col, ev_charging_col, col_7 = st.columns((1, 1, 1, 1))
    elif check_if_value_exists(
        contextual_data, profile_selector, "counts_battery_storage"
    ):
        battery_col, ev_charging_col, hp_col, col_7 = st.columns((1, 1, 1, 1))
    else:
        hp_col, ev_charging_col, battery_col, col_7 = st.columns((1, 1, 1, 1))

    smart_heating_c_value, smart_heating_c_diff = get_value_and_delta(
        profile_selector, contextual_data, "smart_heating_controls"
    )
    elec_ch_col, gas_ch_col, col_8, col_9 = st.columns((1, 1, 1, 1))

    solar_value, solar_diff = get_value_and_delta(
        profile_selector, contextual_data, "solar_panels"
    )
    ev_value, ev_diff = get_value_and_delta(profile_selector, contextual_data, "evs")
    ac_value, ac_diff = get_value_and_delta(profile_selector, contextual_data, "ac")

    smart_heating_col.metric(
        label="Presence of smart heating controls",
        value=smart_heating_c_value,
        delta=smart_heating_c_diff,
        border=True,
    )
    solar_col.metric(
        label="Presence of solar panels",
        value=solar_value,
        delta=solar_diff,
        border=True,
    )
    ev_col.metric(
        label="Presence of electric vehicles",
        value=ev_value,
        delta=ev_diff,
        border=True,
    )
    ac_col.metric(
        label="Presence of air conditioning",
        value=ac_value,
        delta=ac_diff,
        border=True,
    )

    if check_if_value_exists(contextual_data, profile_selector, "counts_ev_charging"):
        ev_charging_value, ev_charging_diff = get_value_and_delta(
            profile_selector, contextual_data, "ev_charging"
        )
        ev_charging_col.metric(
            label="Presence of EV charging points",
            value=ev_charging_value,
            delta=ev_charging_diff,
            border=True,
        )

    if check_if_value_exists(contextual_data, profile_selector, "counts_heat_pumps"):
        hp_value, hp_diff = get_value_and_delta(
            profile_selector, contextual_data, "heat_pumps"
        )
        hp_col.metric(
            label="Presence of heat pumps",
            value=hp_value,
            delta=hp_diff,
            border=True,
        )

    if check_if_value_exists(
        contextual_data, profile_selector, "counts_battery_storage"
    ):
        battery_value, battery_diff = get_value_and_delta(
            profile_selector, contextual_data, "battery_storage"
        )
        battery_col.metric(
            label="Presence of battery storage",
            value=battery_value,
            delta=battery_diff,
            border=True,
        )

    if check_if_value_exists(
        contextual_data, profile_selector, "counts_ch_electric_only"
    ):  # when missing for electric central heating only, also missing for gas central heating only
        elec_ch_value, elec_ch_diff = get_value_and_delta(
            profile_selector, contextual_data, "ch_electric_only"
        )
        gas_ch_value, gas_ch_diff = get_value_and_delta(
            profile_selector, contextual_data, "ch_gas_only"
        )
        elec_ch_col.metric(
            label="Electric central heating only",
            value=elec_ch_value,
            delta=elec_ch_diff,
            border=True,
        )
        gas_ch_col.metric(
            label="Gas central heating only",
            value=gas_ch_value,
            delta=gas_ch_diff,
            border=True,
        )

    setup_additional_central_heating_and_technologies_expander(profile_selector)


def select_profile_page():
    """
    This function sets up the 'Select a profile' page for the energy-use profiles explorer dashboard.
    """

    st.markdown("# Explore an energy-use profile")

    st.markdown(
        "In this page you can select one specific energy-use profile and explore its characteristics and energy consumption patterns."
    )

    profile_selector = initial_setup()

    st.markdown("## 🔌 Profiles and their energy consumption")
    st.markdown(
        "In this section you can find information number and proportion of the population covered by this profile, and respective energy consumption patterns."
    )

    setup_profile_main_metrics(profile_selector)
    setup_daily_consumption_charts(profile_selector)
    with st.expander(label="Expand to explore seasonal patterns", icon="⬇️"):
        setup_seasonal_patterns_expander(profile_selector)

    st.markdown("## 📄 Contextual information")
    st.markdown(
        "The sections below provide contextual information about the households in this profile and their properties, for example household composition, property type and presence of heat pumps. The metrics are compared to the average across all households in the analysis, as presented by the values accompanying the green and red arrows. A green arrow indicates that the value for this profile is higher than the average, while a red arrow indicates that the value for this profile is lower than the average."
    )

    setup_household_info_section(profile_selector)

    st.markdown("### 🏘️ Property information")
    st.markdown(
        "In this section you can find information about the properties in this profile, such as property age, type, region and LSOA IMD quintiles."
    )
    setup_property_information_section(profile_selector)

    st.markdown("### 🔋 Central heating and presence of technologies")
    st.markdown(
        "In this section you can find information about the properties' central heating fuel, presence of smart heating controls, solar panels, electric vehicles, air conditioning, heat pumps, battery storage and EV charging points."
    )
    setup_central_heating_and_technologies_section(profile_selector)
