"""
Utility functions for visualising data in the dashboard.
"""

## Package imports
import pandas as pd
import altair as alt
import numpy as np

# Local imports
from config.fonts_setup import NESTA_COLOURS
from config import configs

# Define a mapping of profiles to colours for use in charts
mapping_profiles_to_colours = pd.DataFrame(
    {
        "profile": configs.profile_numbers,
        "color": NESTA_COLOURS[: len(configs.profile_numbers)],
    }
)


def create_chart_comparing_daily_consumption_summer_winter(
    daily_data_summer: pd.DataFrame,
    daily_data_winter: pd.DataFrame,
    profile: int,
    energy_type: str,
    colour: str = NESTA_COLOURS[0],
) -> alt.Chart:
    """
    Creates a chart showing daily average energy consumption for summer and winter,
    for a specific energy type (electricity or gas) and profile.

    Args:
        daily_data_summer (pd.DataFrame): half-hourly energy consumption data for summer
        daily_data_winter (pd.DataFrame): half-hourly energy consumption data for winter
        profile (int): profile number
        energy_type (str): type of energy ('electricity' or 'gas')
        colour (str, optional): colour of the line. Defaults to NESTA_COLOURS[0].

    Returns:
        alt.Chart: An Altair chart object showing the daily average energy consumption for winter and summer
    """
    profile_col = "profile_" + str(profile)

    title = [
        f"Daily average {energy_type} consumption for profile {profile}:",
        "summer and winter",
    ]

    # Add a season column to each dataframe
    daily_data_summer["season"] = "Summer"
    daily_data_winter["season"] = "Winter"

    # Combine the two dataframes
    combined_data = pd.concat([daily_data_summer, daily_data_winter])

    # Plot average consumption for summer and winter, with dashed lines for winter
    daily_avg_consumption_chart = (
        alt.Chart(combined_data, title=alt.TitleParams(text=title, anchor="middle"))
        .mark_line()
        .encode(
            x=alt.X("read_time:O", title="Time of the day"),
            y=alt.Y(f"{profile_col}_avg:Q", title=f"{energy_type} consumption (Wh)"),
            color=alt.value(colour),
            strokeDash=alt.StrokeDash(
                "season:N"
            ),  # Dashed for winter, solid for summer
            tooltip=[
                alt.Tooltip("read_time:O", title="Half hour"),
                alt.Tooltip(f"{profile_col}_avg:Q", title="Mean Value", format=".0f"),
                alt.Tooltip("season:N", title="Season"),
            ],
        )
        .properties(width=600, height=400)
    )
    return daily_avg_consumption_chart


def create_chart_daily_consumption(
    daily_data: pd.DataFrame,
    profile: int,
    energy_type: str,
    season: str = "",
    colour: str = NESTA_COLOURS[0],
    std_band: bool = True,
) -> alt.Chart:
    """
    Creates a chart showing daily average energy consumption for a specific profile and energy type.

    Args:
        daily_data (pd.DataFrame): DataFrame containing daily average energy consumption data.
        profile (int): profile number
        energy_type (str): type of energy ('electricity' or 'gas')
        season (str, optional): season ("" for all year, "summer" for summer and "winter" for winter).
                                Defaults to "" (all year/no season selected)
        colour (str, optional): colour of the line. Defaults to NESTA_COLOURS[0].
        std_band (bool, optional): True to show error band, otherwise False. Defaults to True.

    Returns:
        alt.Chart: An Altair chart object showing the daily average energy consumption for the
        specified profile, energy type and season (and optional error band).
    """
    profile_col = "profile_" + str(profile)

    title = f"Daily average {energy_type} consumption for profile {profile}"
    title = f" in {season}" if season != "" else title

    # Line chart for the mean/average consumption
    avg_line = (
        alt.Chart(daily_data, title=alt.TitleParams(text=title, anchor="middle"))
        .mark_line()
        .encode(
            x=alt.X("read_time:O", title="Time of the day"),
            y=alt.Y(f"{profile_col}_avg:Q", title=f"{energy_type} consumption (in Wh)"),
            color=alt.value(colour),
            tooltip=[
                alt.Tooltip("read_time:O", title="Half hour"),
                alt.Tooltip(
                    f"{profile_col}_avg:Q",
                    title="Average daily profile consumption",
                    format=".0f",
                ),
            ],
        )
    )

    # Calculate y_min and y_max using the mean and the standard deviation
    # y_min defines the bottom of the error band
    daily_data["y_min"] = (
        daily_data[profile_col + "_avg"] - daily_data[profile_col + "_std"]
    )
    # y_max defines the top of the error band
    daily_data["y_max"] = (
        daily_data[profile_col + "_avg"] + daily_data[profile_col + "_std"]
    )
    # Ensure y_min is not negative (as there is no negative consumption)
    daily_data["y_min"] = daily_data["y_min"].clip(lower=0)

    # If std_band is True, we plot the error band around the mean line
    if std_band:
        error_band = (
            alt.Chart(daily_data)
            .mark_area(opacity=0.3)
            .encode(
                x=alt.X("read_time:O", title="Time of the day"),
                y=alt.Y("y_min:Q", title=""),
                y2="y_max:Q",
                color=alt.value(colour),
                tooltip=[
                    alt.Tooltip("read_time:O", title="Half hour"),
                    alt.Tooltip(
                        f"{profile_col}_avg:Q", title="Mean Value", format=".0f"
                    ),
                    alt.Tooltip(
                        "y_min:Q", title="Average - standard deviation", format=".0f"
                    ),
                    alt.Tooltip(
                        "y_max:Q", title="Average + standard deviation", format=".0f"
                    ),
                ],
            )
        )
        final_chart = error_band + avg_line
    else:
        final_chart = avg_line

    final_chart = final_chart.properties(width=600, height=400)

    return final_chart


def create_chart_daily_consumption_multiple_profiles(
    daily_data: pd.DataFrame, profiles: list, energy_type: str, season: str = ""
) -> alt.Chart:

    data = daily_data.copy()

    # Using melt to reshape the DataFrame to have only one column for consumption and a separate
    # column that identifies the corresponding profile
    data = data.melt(
        id_vars=["read_time"],
        value_vars=[f"profile_{profile}_avg" for profile in profiles],
        var_name="profile",
        value_name="consumption",
    )

    # Creating a column with 'Profile X' for each profile
    data["profile"] = data["profile"].apply(lambda x: int(x.split("_")[1]))

    data.sort_values(by="profile", inplace=True)

    # Mapping profiles to colors
    colors = mapping_profiles_to_colours[
        mapping_profiles_to_colours["profile"].isin(profiles)
    ]["color"].tolist()

    # If the energy type is gas, we remove profiles with low number of gas household
    if energy_type == "gas":
        data = data[~data["profile"].isin(configs.profiles_low_gas_count)]
        colors_to_remove = [
            NESTA_COLOURS[j - 1] for j in configs.profiles_low_gas_count
        ]
        colors = [c for c in colors if c not in colors_to_remove]

    # If the season is not specified or is summer, we use a solid line
    if season == "" or season == "summer":
        chart = alt.Chart(data).mark_line()
    else:  # Dashed line for Winter
        chart = alt.Chart(data).mark_line(strokeDash=[5, 5])

    chart = chart.encode(
        x=alt.X("read_time:O", title="Time of the day"),
        y=alt.Y("consumption:Q", title=f"{energy_type} consumption (in Wh)"),
        color=alt.Color("profile:N", title="Profile", scale=alt.Scale(range=colors)),
        tooltip=[
            alt.Tooltip("read_time:O", title="Half hour"),
            alt.Tooltip(
                f"consumption:Q",
                title=f"{energy_type} consumption (in Wh)",
                format=".0f",
            ),
        ],
    )

    chart_title = (
        f"Daily average {energy_type} consumption"
        if season == ""
        else f"Daily average {energy_type} consumption by season"
    )

    chart = chart.properties(
        title=alt.TitleParams(text=chart_title, anchor="middle"), width=600, height=400
    )

    return chart


def plot_distribution_households(
    profile_counts: pd.DataFrame, as_percentage: bool = False
) -> alt.Chart:
    """
    Create a bar plot showing the number of households per profile.

    Args:
        profile_counts (pd.DataFrame): DataFrame containing profile counts.
        as_percentage (bool): If True, show the counts as percentages of total households.

    Returns:
        alt.Chart: Altair chart object.
    """
    title = "Distribution of households by energy-use profile"

    y_label = (
        "Number of households" if not as_percentage else "Percentage of households (%)"
    )

    y_var = "number_of_households" if not as_percentage else "perc_of_households"

    chart = (
        alt.Chart(profile_counts, title=alt.TitleParams(text=title, anchor="middle"))
        .mark_bar()
        .encode(
            x=alt.X("profile:O", title="Profile", axis=alt.Axis(labelAngle=0)),
            y=alt.Y(f"{y_var}:Q", title=y_label),
            color=alt.value(NESTA_COLOURS[0]),
            tooltip=[
                alt.Tooltip("profile:O", title="Profile"),
                alt.Tooltip(f"{y_var}:Q", title=y_label, format=".0f"),
            ],
        )
        .properties(width=600, height=400)
    )
    return chart


def create_chart_average_annual_consumption(
    profile_annual_avgs: pd.DataFrame, energy_type: str, colour: str = NESTA_COLOURS[0]
) -> alt.Chart:
    """
    Create a bar plot showing the average annual energy consumption per profile.

    Args:
        profile_annual_avgs (pd.DataFrame): DataFrame containing average annual energy consumption per profile.
        energy_type (str): Type of energy ('electricity' or 'gas').

    Returns:
        alt.Chart: Altair chart object showing the average annual energy consumption per profile.
    """
    data = profile_annual_avgs.copy()

    y_col = f"avg_annual_{energy_type[:4]}_consumption_kWh"
    title = f"Average annual {energy_type} consumption"

    if energy_type == "gas":
        data = data[~data["profile"].isin(configs.profiles_low_gas_count)]

    chart = (
        alt.Chart(data, title=alt.TitleParams(text=title, anchor="middle"))
        .mark_bar()
        .encode(
            x=alt.X("profile:O", title="Profile", axis=alt.Axis(labelAngle=0)),
            y=alt.Y(f"{y_col}:Q", title=f"{energy_type} consumption (in kWh)"),
            color=alt.value(colour),
            tooltip=[
                alt.Tooltip("profile:O", title="Profile"),
                alt.Tooltip(f"{y_col}:Q", title=title, format=".0f"),
            ],
        )
        .properties(width=600, height=400)
    )
    return chart


def plot_contextual_info(data: pd.DataFrame, variable: str, title: str) -> alt.Chart:
    """
    Creates a bar chart comparing the proportion of households with a specific
    characteristic across different profiles.
    It also adds a horizontal dashed line indicating the average value in the population.

    Args:
        data (pd.DataFrame): contextual data
        variable (str): conrextual variable to plot (e.g. "income") withtout "counts_" or "proportion_" prefix
        title (str): title of the chart

    Returns:
        alt.Chart: An Altair chart object showing the proportion of households with the specified characteristic
    """
    # In the contextual info df, the profile is stored as a string
    profiles_as_strings = [str(p) for p in configs.profile_numbers]

    # select only contextual information about profiles by select numbers only
    # (when there are low counts for a number of profiles, contextual information
    # is provided as an aggregate and "profile" might have values such as "All other profiles")
    profiles_specific_data = data[data["profile"].isin(profiles_as_strings)]

    # creating barchart with a bar for each profile
    chart = (
        alt.Chart(
            profiles_specific_data, title=alt.TitleParams(text=title, anchor="middle")
        )
        .mark_bar()
        .encode(
            x=alt.X(
                "profile:N",
                axis=alt.Axis(labelAngle=0),
                sort=[str(i) for i in range(1, 11)],
            ),
            y=alt.Y(f"proportion_{variable}:Q", title="Percentage of households (%)"),
            color=alt.value(NESTA_COLOURS[0]),
            tooltip=[
                alt.Tooltip("profile", title="Profile"),
                alt.Tooltip(
                    f"proportion_{variable}:Q",
                    title="Percentage of households (%)",
                    format=".0f",
                ),
            ],
        )
        .properties(width=600, height=400)
    )

    # adding a horizontal dashed line for average value in population
    avg_population = round(
        data[f"counts_{variable}"].sum() / data["number_households"].sum() * 100, 2
    )
    chart = chart + alt.Chart(
        pd.DataFrame({"avg_population": [avg_population]})
    ).mark_rule(strokeDash=[1, 0], strokeWidth=3, color=NESTA_COLOURS[10]).encode(
        y=alt.Y("avg_population:Q"),
        tooltip=[
            alt.Tooltip("avg_population:Q", title="Population average", format=".2f")
        ],
    )
    return chart


def setup_coloured_bars(
    min_val: float, max_val: float, value: float, energy_type: str
) -> alt.Chart:
    """
    Creates a vertical gradient bar chart with a marker for a specific value.
    The gradient bar represents a range of values from min_val to max_val,
    with a fixed step size of 2000.
    The marker indicates the specific value within this range.
    Args:
        min_val (float): Minimum value for the gradient bar.
        max_val (float): Maximum value for the gradient bar.
        value (float): Specific value to be marked on the gradient bar.
        energy_type (str): Type of energy ('Electricity' or 'Gas').

    Returns:
        alt.Chart: An Altair chart object showing the vertical gradient bar with a marker.
    """
    # presenting rounded values
    value = int(round(value, 0))

    step = 2000
    min_val = min_val - step  # Start one step below the minimum
    max_val = max_val + step  # End one step above the maximum
    min_val = max(min_val, 0)  # Ensure we don't start below 0

    # Generate y values with fixed step
    y_vals = np.round(np.arange(min_val, max_val + step, step), 1)

    gradient_data = pd.DataFrame(
        {"y": y_vals, "color_value": np.linspace(0, 1, len(y_vals))}
    )

    gradient = (
        alt.Chart(gradient_data)
        .mark_rect()
        .encode(
            y=alt.Y(
                "y:Q",
                scale=alt.Scale(domain=[min_val, max_val]),
                axis=alt.Axis(title=f"{energy_type} Consumption"),
            ),
            y2=alt.Y2("y2:Q"),
            x=alt.value(0),
            x2=alt.value(20),
            color=alt.Color(
                "color_value:Q",
                scale=alt.Scale(domain=[0, 1], range=["green", "red"]),
                legend=None,
            ),
            tooltip=[alt.Tooltip("y:Q", title="Consumption Level")],
        )
        .transform_calculate(y2=f"datum.y + {step}")
        .properties(width=30, height=250)
    )

    marker = (
        alt.Chart(pd.DataFrame({"y": [value]}))
        .mark_point(color="black", size=50, shape="circle")
        .encode(
            y=alt.Y("y:Q", scale=alt.Scale(domain=[min_val, max_val])), x=alt.value(10)
        )
    )

    chart = gradient + marker

    return chart
