"""
About the energy-use profiles explorer dashboard page.
"""

import streamlit as st


def about_dashboard_page():
    """
    This function will setup an 'About the explorer' page for the energy-use profiles explorer dashboard.
    """
    st.markdown("# :zap: Welcome to the energy-use profiles explorer!")

    st.markdown(
        "#### An interactive tool to explore energy patterns of households in Great Britain"
    )

    st.markdown("## The why")
    st.markdown(
        """
                Analysing smart meter data plays an essential role in reducing carbon emissions and ensuring a **successful energy transition**.
                As low-carbon heating systems such as heat pumps become more widespread, they will place greater demands on the electricity grid.
                Ensuring the effective supply of and demand for energy makes it increasingly important to understand household consumption.
                This requires a clear understanding of how different kinds of households in Great Britain (GB) consume energy, what their daily usage looks like in terms of peaks and falls in consumption, along with what heating systems they own and when they might need to upgrade them.

                [Nesta's sustainable future team](https://www.nesta.org.uk/sustainable-future/) analysed smart meter data to **understand energy consumption in GB households**.
                This was based on the [Smart Energy Research Lab (SERL) dataset](http://doi.org/10.5255/UKDA-SN-8666-8), which offers half-hourly gas and electricity consumption data, along with household survey data, for over 13,000 representative GB households.

                From the 13,000 households available, approximately **6,000 households** with high-quality data spanning **July 2023 to June 2024** were selected for analysis.
                The resulting **energy-use profiles** offer insight into the different ways in which households consume energy, paving the way for more targeted interventions.

        """
    )
    st.markdown("## About the explorer")
    st.markdown(
        """
                The **energy-use profiles explorer** is a tool designed to help you explore the energy-use profiles of different types of households in GB.
                It provides an interactive way to view and compare energy consumption patterns, enabling users to gain insights into household energy usage.

                Use the sidebar to navigate through the different sections of the explorer.

                #### 'Explore the results'
                Provides an overview of results, where all energy-use profiles are displayed and compared across a variety of characteristics.

                #### 'Explore an energy-use profile'
                Provides the ability to explore individual energy-use profiles in more detail, including their energy consumption patterns, heating systems, and other characteristics - and how they compare with the average of the population.

                #### 'About the data'
                Provides information about the data used to create the energy-use profiles, including the methodology and sources.
        """
    )

    st.markdown("## To know more")
    st.markdown(
        """
                This tool was developed by [Nesta](https://www.nesta.org.uk/) to be used by researchers, policymakers, and anyone interested in understanding household energy consumption.

                You can also find insights in our [report](), read the methodology in the [appendix]() and read more about this [Nesta project](https://www.nesta.org.uk/project/using-smart-meters-to-identify-energy-use-profiles/).
                To provide feedback on the explorer please [fill this form](https://docs.google.com/forms/d/19nhqeg0HZlkrk8zWJthrhDjVOkOINRGZtIqqHrUTB8A).
                """
    )
