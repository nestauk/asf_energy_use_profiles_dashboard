"""
Page with overview of results.

The main function is overview_results_page() which sets up the page and its tabs.
"""

# Package imports
import streamlit as st
import altair as alt

# Local imports
from getters import data_getters as dg
from utils.data_vis_utils import (
    plot_distribution_households,
    create_chart_average_annual_consumption,
    create_chart_daily_consumption_multiple_profiles,
    plot_contextual_info,
)
from config.fonts_setup import nestafont, NESTA_COLOURS
from config.highlights import highlights
from config import configs

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

# creates string with "X and Y" where X and Y are the profiles with low gas consumption
off_gas_prof = " and ".join(map(str, configs.profiles_low_gas_count))


def create_overview_tab():
    """
    Creates the overview tab for the 'Explore the results' page.
    """
    st.write("'Explore the results' is organised into the following main sections:")
    st.markdown(
        """
                ##### Overview
                Provides key findings from the analysis of the energy-use profiles.

                ##### Distribution of households
                Shows the distribution of households across different energy-use profiles, allowing you to see how many households fall into each profile.

                ##### Annual energy consumption averages
                Displays the average annual electricity and gas consumption for each energy-use profile.

                ##### Daily energy consumption profiles
                Provides detailed daily energy consumption profiles for selected energy-use profiles, allowing you to see how energy consumption varies throughout the day on average (and in different seasons).

                ##### Contextual information
                Provides additional information about the households in each energy-use profile, including household composition, income, and property type.

                -------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                """
    )

    st.markdown("### 💡 Key findings")
    for key, value in highlights.items():
        st.markdown(f"Profile {key} {value}\n")


def create_distribution_tab():
    """
    Creates the distribution tab for the 'Explore the results' page.
    """
    st.markdown("## 📊 Distribution of households by energy-use profile")

    # Creating a toggle to switch between percentage and number of households
    switch_to_count = st.toggle(
        "Switch on to show number of households (as default it shows percentage of households)",
        key="switch_to_count",
    )

    # Plotting distribution of households in the center of the page by setting it in the middle column
    col1, dist_col, col2 = st.columns([1, 3, 1])
    if switch_to_count:  # if the switch is on, show number of households
        with dist_col:
            perc_chart = plot_distribution_households(
                profile_counts=distribution_households, as_percentage=False
            )
            st.altair_chart(perc_chart, use_container_width=False)
    else:  # if the switch is off, show percentage of households
        with dist_col:
            num_chart = plot_distribution_households(
                profile_counts=distribution_households, as_percentage=True
            )
            st.altair_chart(num_chart, use_container_width=False)

    # Coding numbers that appear in the following paragraph, rather hardcoding
    max_count = distribution_households["number_of_households"].max()
    min_count = distribution_households["number_of_households"].min()
    max_perc = int(round(distribution_households["perc_of_households"].max()))
    min_perc = int(round(distribution_households["perc_of_households"].min()))

    st.markdown(
        f"""
                Results show that households are not evenly distributed, reflecting that different proportions of the population have different energy consumption behaviours.
                The biggest profile covers {max_count} ({max_perc}% of) households, while the smallest one covers {min_count} ({min_perc}% of) households.
Most households in profiles {off_gas_prof} don’t consume gas, while most of the other profiles have households that cook or heat their home with gas.

                """
    )

    st.markdown(
        """
                Households in the Smart Energy Research Lab Observatory Data constitute a representative sample of households with respect to region and income decile.
                The sample in analysis in this dashboard was selected to be representative of the population for region and index of multiple deprivation (as income deciles are not made available).
                """
    )


def create_annual_consumption_tab():
    """
    Creates the annual energy consumption averages tab for the 'Explore the results' page.
    """
    st.markdown("## 🔋 Average annual energy consumption")

    st.markdown(
        f"""
                The charts below show the average annual electricity and gas consumption for each energy-use profile. It is crucial to note that these values represent a mean across all households within each profile, but variation exists at the individual household level.

                The data shows that consumption varies quite substantially by energy-use profile. These consumption disparities are partly influenced by household composition. While all profiles include a mix of single, double, and larger occupancy homes, the distribution of household occupancy within each profile isn't uniform. You can explore these differences in the contextual information section of the dashboard.

                Off-gas homes are primarily found in profiles {off_gas_prof}. Due to the minimal number of on-gas households in these profiles, average annual gas consumption isn't provided as it wouldn't accurately represent these groups.

    """
    )

    # Show barchart with average annual electricity for each energy-use profile in the center of the page
    col3, elec_annual_col, col4 = st.columns([1, 3, 1])
    with elec_annual_col:
        annual_elec_chart = create_chart_average_annual_consumption(
            profile_annual_avgs=profile_annual_avgs, energy_type="electricity"
        )
        st.altair_chart(annual_elec_chart, use_container_width=True)

    # Show barchart with average annual gas for each energy-use profile in the center of the page
    col5, gas_annual_col, col6 = st.columns([1, 3, 1])
    with gas_annual_col:
        annual_gas_chart = create_chart_average_annual_consumption(
            profile_annual_avgs=profile_annual_avgs,
            energy_type="gas",
            colour=NESTA_COLOURS[1],
        )
        st.altair_chart(annual_gas_chart, use_container_width=True)


def create_household_information_expander():
    """
    Creates an expander for household information in the context tab.
    """
    st.markdown("#### 👥 Household composition")

    # Age of household members
    (
        hc_65p_col,
        hc_adults_child_col,
    ) = st.columns([1, 1])
    with hc_65p_col:
        chart_hc_65p = plot_contextual_info(
            data=contextual_data,
            variable="adults_65_plus_only",
            title="Households 65+ years old only",
        )
        st.altair_chart(chart_hc_65p, use_container_width=True)
    with hc_adults_child_col:
        chart_hc_adults_child = plot_contextual_info(
            data=contextual_data,
            variable="adults_and_children",
            title="Households with adults and children",
        )
        st.altair_chart(chart_hc_adults_child, use_container_width=True)

    # Household size and occupancy
    occ_3more_col, occ_single_col = st.columns([1, 1])
    with occ_3more_col:
        chart_occupancy_3_or_more = plot_contextual_info(
            data=contextual_data,
            variable="3plus_occupants",
            title="Households with 3 or more occupants",
        )
        st.altair_chart(chart_occupancy_3_or_more, use_container_width=True)
    with occ_single_col:
        chart_single_occupancy = plot_contextual_info(
            data=contextual_data,
            variable="single_occupancy",
            title="Households with single occupants only",
        )
        st.altair_chart(chart_single_occupancy, use_container_width=True)

    st.markdown("#### 💰 Working status and income")
    # Working status
    all_not_working_col, all_working_or_students_col, mix_col = st.columns([1, 1, 1])
    with all_not_working_col:
        chart_working_status = plot_contextual_info(
            data=contextual_data,
            variable="working_status_all_not_working",
            title="Households where all members are not working",
        )
        st.altair_chart(chart_working_status, use_container_width=True)
    with all_working_or_students_col:
        chart_working_or_students = plot_contextual_info(
            data=contextual_data,
            variable="working_status_all_working_and_or_students",
            title="Households where all members are working and/or students",
        )
        st.altair_chart(chart_working_or_students, use_container_width=True)
    with mix_col:
        chart_working_status_mix = plot_contextual_info(
            data=contextual_data,
            variable="working_status_mix",
            title="Households with a mix of working and non-working members",
        )
        st.altair_chart(chart_working_status_mix, use_container_width=True)

    # Income
    income_90k_below_col, income_over_90k_col = st.columns([1, 1])
    with income_90k_below_col:
        chart_income_below_90k = plot_contextual_info(
            data=contextual_data,
            variable="income_90k_below",
            title="Households with income £90k or below",
        )
        st.altair_chart(chart_income_below_90k, use_container_width=True)
    with income_over_90k_col:
        chart_income_over_90k = plot_contextual_info(
            data=contextual_data,
            variable="income_above_90k",
            title="Households with income over £90k",
        )
        st.altair_chart(chart_income_over_90k, use_container_width=True)

    st.markdown("#### 🏠 Tenure")
    priv_rented_prop_col, social_rented_prop_col, owner_occup_prop_col = st.columns(
        [1, 1, 1]
    )
    with priv_rented_prop_col:
        chart_privately_rented = plot_contextual_info(
            data=contextual_data,
            variable="privately_rented",
            title="Rented (private) households",
        )
        st.altair_chart(chart_privately_rented, use_container_width=True)
    with social_rented_prop_col:
        chart_social_rented = plot_contextual_info(
            data=contextual_data,
            variable="social_rented",
            title="Rented (social) households",
        )
        st.altair_chart(chart_social_rented, use_container_width=True)

    with owner_occup_prop_col:
        chart_owner_occupiers = plot_contextual_info(
            data=contextual_data,
            variable="owner_occupier_or_unknown_tenure",
            title="Owner occupiers or unknown tenure households",
        )
        st.altair_chart(chart_owner_occupiers, use_container_width=True)


def create_property_information_expander():
    """
    Creates an expander for property information in the context tab.
    """
    st.markdown("#### 🏙️ Region and Index of Multiple Deprivation (IMD)")
    # IMD and region (London is the only one we have data for)
    imd_1_2_col, imd_3_col, imd_4_5_col, london_col = st.columns((1, 1, 1, 1))
    with imd_1_2_col:
        chart_imd_1_2 = plot_contextual_info(
            data=contextual_data,
            variable="imd_1_2",
            title="IMD 1-2 (most deprived)",
        )
        st.altair_chart(chart_imd_1_2, use_container_width=True)
    with imd_3_col:
        chart_imd_3 = plot_contextual_info(
            data=contextual_data, variable="imd_3", title="IMD 3"
        )
        st.altair_chart(chart_imd_3, use_container_width=True)
    with imd_4_5_col:
        chart_imd_4_5 = plot_contextual_info(
            data=contextual_data,
            variable="imd_4_5",
            title="IMD 4-5 (least deprived)",
        )
        st.altair_chart(chart_imd_4_5, use_container_width=True)
    with london_col:
        chart_london = plot_contextual_info(
            data=contextual_data,
            variable="region_greater_london",
            title="Households in Greater London",
        )
        st.altair_chart(chart_london, use_container_width=True)

    st.markdown("#### 🏠 Property type and age")
    built_before_1930_col, detached_col, flats_col = st.columns((1, 1, 1))
    with built_before_1930_col:
        chart_property_age = plot_contextual_info(
            data=contextual_data,
            variable="property_built_before_1930",
            title="Properties built before 1930",
        )
        st.altair_chart(chart_property_age, use_container_width=True)
    with detached_col:
        chart_property_detached = plot_contextual_info(
            data=contextual_data,
            variable="property_type_detached",
            title="Detached properties",
        )
        st.altair_chart(chart_property_detached, use_container_width=True)
    with flats_col:
        chart_property_flats = plot_contextual_info(
            data=contextual_data,
            variable="property_type_flats_apartments_maisonettes",
            title="Flats, apartments or maisonettes",
        )
        st.altair_chart(chart_property_flats, use_container_width=True)


def create_central_heating_and_tech_expander():
    """
    Creates an expander for central heating and presence of technologies in the context tab.
    """
    st.markdown("#### 🔥 Central heating fuel type and smart heating controls")
    elec_ch_col, gas_ch_col, smart_heating_col = st.columns((1, 1, 1))
    with elec_ch_col:
        chart_ch_electricity = plot_contextual_info(
            data=contextual_data,
            variable="ch_electric_only",
            title="Electric central heating only",
        )
        st.altair_chart(chart_ch_electricity, use_container_width=True)
    with gas_ch_col:
        chart_ch_gas = plot_contextual_info(
            data=contextual_data,
            variable="ch_gas_only",
            title="Gas central heating only",
        )
        st.altair_chart(chart_ch_gas, use_container_width=True)
    st.markdown("#### ❄️ Heat pumps and air conditioning units")
    hp_col, ac_col = st.columns((1, 1))
    with hp_col:
        chart_heat_pump = plot_contextual_info(
            data=contextual_data,
            variable="heat_pumps",
            title="Presence of heat pumps",
        )
        st.altair_chart(chart_heat_pump, use_container_width=True)
    with ac_col:
        chart_ac = plot_contextual_info(
            data=contextual_data,
            variable="ac",
            title="Presence of air conditioning units s",
        )
        st.altair_chart(chart_ac, use_container_width=True)
    with smart_heating_col:
        chart_smart_heating = plot_contextual_info(
            data=contextual_data,
            variable="smart_heating_controls",
            title="Presence of smart heating controls",
        )
        st.altair_chart(chart_smart_heating, use_container_width=True)

    st.markdown("#### 🌞 Solar panels and battery storage")
    solar_col, battery_col = st.columns((1, 1))
    with solar_col:
        chart_solar_panels = plot_contextual_info(
            data=contextual_data,
            variable="solar_panels",
            title="Presence of solar panels",
        )
        st.altair_chart(chart_solar_panels, use_container_width=True)
    with battery_col:
        chart_battery_storage = plot_contextual_info(
            data=contextual_data,
            variable="battery_storage",
            title="Presence of battery storage",
        )
        st.altair_chart(chart_battery_storage, use_container_width=True)

    st.markdown("#### 🚗 Electric vehicles and charging")
    ev_col, ev_charging_col = st.columns((1, 1))
    with ev_col:
        chart_ev = plot_contextual_info(
            data=contextual_data,
            variable="evs",
            title="Households with electric vehicles",
        )
        st.altair_chart(chart_ev, use_container_width=True)
    with ev_charging_col:
        chart_ev_charging = plot_contextual_info(
            data=contextual_data,
            variable="ev_charging",
            title="Presence of EV charging points",
        )
        st.altair_chart(chart_ev_charging, use_container_width=True)


def create_context_tab():
    st.markdown("## 📄 Contextual information")

    st.markdown(
        """
        This section highlights differences between energy-use profiles across a variety of characteristics, including household composition, income, property type and age, central heating fuel type, and presence of technologies.

        The information is presented as bar plots, where each bar represents one energy-use profiles. When a bar is missing, it means the data count for that profile was too low to be shown due to statistical disclosure rules. The line in yellow indicates the average for the population, which is calculated across all households.
        """
    )

    # Create an expander for household information
    with st.expander(label="Household information", icon="👨‍👩‍👧‍👦"):
        create_household_information_expander()

    # Create an expander for property information
    with st.expander(label="Property information", icon="🏘️"):
        create_property_information_expander()

    # Create an expander for central heating and presence of technologies
    with st.expander(label="Central heating and presence of technologies", icon="🔋"):
        create_central_heating_and_tech_expander()


def create_daily_consumption_tab():
    """
    Creates the daily energy consumption profiles tab for the 'Explore the results' page.
    """
    st.markdown("## 💡 Daily average energy consumption")
    st.markdown(
        f"""Select a number of energy-use profiles and see how they compare in terms of daily average electricity and gas consumption (on the left hand side).
    You can also select seasons to see how consumption changes in different seasons (on the right hand side).

Off-gas homes are primarily found in profiles {off_gas_prof}. Due to the minimal number of on-gas households in these profiles, daily average gas consumption isn't provided as it wouldn't accurately represent these groups.
                """
    )

    # List of profiles in the format "Profile X" where X is the profile number
    profiles = [f"Profile {i}" for i in configs.profile_numbers]

    # Create a multiselect widget to select profiles to display, defaulting to a few profiles
    options = st.multiselect(
        "Select (or de-select) energy-use profiles to display",
        options=profiles,
        default=["Profile 2", "Profile 3", "Profile 6", "Profile 9"],
    )

    # Create a multiselect widget to select seasons to display on the right hand side, defaulting to "Winter"
    season_options = st.multiselect(
        "Select seasons to display (will only change seasonal plots on the right hand side). Winter is presented with dashed lines.",
        options=["Winter", "Summer"],
        default=["Winter"],
    )

    # Create two columns to display daily (on the left) and seasonal daily (on the right)
    # energy consumption profiles
    daily_col, seasonal_daily_col = st.columns([1, 1])

    with daily_col:
        st.markdown("### 📅 Daily average energy consumption")

        profile_numbers = [int(profile.split(" ")[1]) for profile in options]

        # Show daily average electricity consumption profiles for selected profiles
        chart_daily_elec = create_chart_daily_consumption_multiple_profiles(
            daily_data=elec_hh_data,
            profiles=profile_numbers,
            energy_type="electricity",
        )
        st.altair_chart(chart_daily_elec, use_container_width=True)

        # Show daily average gas consumption profiles for selected profiles
        chart_daily_gas = create_chart_daily_consumption_multiple_profiles(
            daily_data=gas_hh_data,
            profiles=profile_numbers,
            energy_type="gas",
        )
        st.altair_chart(chart_daily_gas, use_container_width=True)

    with seasonal_daily_col:
        st.markdown("### ❄️☀️ Seasonal daily average energy consumption")

        # Show seasonal daily average electricity consumption profiles for selected profiles
        chart_season_elec = None
        if "Winter" in season_options:
            chart_elec_winter = create_chart_daily_consumption_multiple_profiles(
                daily_data=elec_hh_data_winter,
                profiles=profile_numbers,
                energy_type="electricity",
                season="winter",
            )
            if chart_season_elec is None:
                chart_season_elec = chart_elec_winter
        if "Summer" in season_options:
            chart_elec_summer = create_chart_daily_consumption_multiple_profiles(
                daily_data=elec_hh_data_summer,
                profiles=profile_numbers,
                energy_type="electricity",
                season="summer",
            )
            if chart_season_elec is None:
                chart_season_elec = chart_elec_summer
            else:
                chart_season_elec += chart_elec_summer
        st.altair_chart(chart_season_elec, use_container_width=True)

        # Show seasonal daily average gas consumption profiles for selected profiles
        chart_season_gas = None
        if "Winter" in season_options:
            chart_gas_winter = create_chart_daily_consumption_multiple_profiles(
                daily_data=gas_hh_data_winter,
                profiles=profile_numbers,
                energy_type="gas",
                season="winter",
            )
            if chart_season_gas is None:
                chart_season_gas = chart_gas_winter
        if "Summer" in season_options:
            chart_gas_summer = create_chart_daily_consumption_multiple_profiles(
                daily_data=gas_hh_data_summer,
                profiles=profile_numbers,
                energy_type="gas",
                season="summer",
            )
            if chart_season_gas is None:
                chart_season_gas = chart_gas_summer
            else:
                chart_season_gas += chart_gas_summer
        st.altair_chart(chart_season_gas, use_container_width=True)


def overview_results_page():
    """
    This function will setup the 'Explore the results' page for the energy-use profiles explorer dashboard.
    """

    st.markdown("# 🔍 Explore the results")

    # The 'Explore the results' page is organised into the following different tabs
    (
        overview_tab,
        distribution_tab,
        annual_consumption_tab,
        daily_consumption_tab,
        context_tab,
    ) = st.tabs(
        [
            "Overview",
            "Distribution of households",
            "Average annual energy consumption",
            "Daily average energy consumption",
            "Contextual information",
        ]
    )

    # Overview tab
    with overview_tab:
        create_overview_tab()

    # Distribution of households tab
    with distribution_tab:
        create_distribution_tab()

    # Annual energy consumption averages tab
    with annual_consumption_tab:
        create_annual_consumption_tab()

    # Daily energy consumption profiles tab
    with daily_consumption_tab:
        create_daily_consumption_tab()

    # Contextual information tab
    with context_tab:
        create_context_tab()
