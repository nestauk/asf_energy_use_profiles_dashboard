"""
About the data page.
"""

import streamlit as st


def about_data_page():
    """
    This function will setup an 'About the data' page for the energy-use profiles explorer dashboard.
    """
    st.markdown("# About the data")
    st.markdown(
        """The analyses presented in this document were conducted using Smart Energy
Research Lab (SERL) observatory data, containing longitudinal smart meter electricity and gas data for over 13,000 households in Great Britain. The data is
accessible through the [UK Data Service SecureLab](https://ukdataservice.ac.uk/) by accredited researchers.
                """
    )
    st.markdown(
        """The SERL data is a rich source of information, including half-hourly gas and electricity consumption data and household survey data, such as property type, household composition, and income. The data documentation is available on the [data catalogue](https://beta.ukdataservice.ac.uk/datacatalogue/studies/study?id=8666#!/documentation).
                """
    )
    st.markdown(
        """You can find detailed information about the underlying methodology in the [appendix]().
                """
    )

    st.markdown("## Data citation")
    st.markdown(
        """
Elam, S., Few, J., McKenna, E., Hanmer, C., Pullinger, M., Zapata-Webborn, E., Oreszczyn, T., Anderson, B., Department for Levelling Up, Housing and Communities, European Centre for Medium-Range Weather Forecasts, Royal Mail Group Limited. (2024). Smart Energy Research Lab Observatory Data, 2019-2024: Secure Access. [data collection]. 8th Edition. UK Data Service. SN: 8666, DOI: http://doi.org/10.5255/UKDA-SN-8666-8

                """
    )

    st.markdown("## Caveats and limitations of the work")
    with st.expander("Small sample of households & information sharing"):
        st.markdown(
            """The Smart Energy Research Lab (SERL) data contains smart meter and contextual data from over 13,000 households. However, not all of these households met the criteria for inclusion in this analysis. For instance, some were excluded because their data did not span the entire analysis period. Ultimately, to ensure the sample remains representative of Great Britain, we focused our analysis on a smaller, refined sample of approximately 6,000 households.
The process of defining the number of energy profiles is a careful balance of data science insights and expert domain knowledge. It's crucial that these profiles are of an appropriate size – not so small that they prevent us from showing meaningful information due to statistical disclosure rules, nor so large that they lose their usefulness. Our current sample size means some profiles are quite small, which can limit our ability to provide granular breakdowns, such as property type distributions within specific profiles. This issue is further compounded by missing contextual information, given that a proportion of values is unknown for some variables, often requiring us to group unknown categories with known ones due to low counts.
With a larger sample or enhanced synthetic data, we could further refine these profiles to identify ‘true archetypes’ of energy consumption and household characteristics.
                    """
        )
    with st.expander("Extracting actionable insights"):
        st.markdown(
            """Households were clustered using consumption data. Sociodemographic and other contextual information are not well clustered, making it hard to identify ‘true archetypes’ and identify meaningful insight. As an example, wealthy households with solar panels and low-income households might cluster together if both have low electricity consumption (although for different reasons).
"""
        )

    with st.expander("Information gap for low-income and deprived households"):
        st.markdown(
            """We often have less to say about those on low incomes and in more deprived areas, as they typically don’t have technologies such as heat pumps or solar panels installed in the house.
"""
        )

    with st.expander("Inherent bias in data"):
        st.markdown(
            """The data we have access to comes from houses with smart meters; hence, the data is inherently biased to what we can learn from homes with smart meters. Smart meter coverage is still quite low in GB, with the latest statistics showing the number of installations in the UK reached [66% of homes and small businesses, with 39 million smart and advanced meters in operation across Great Britain](https://assets.publishing.service.gov.uk/media/67d95f7c4ba412c67701ed58/Q4_2024_Smart_Meters_Statistics_Report.pdf) as of the end of 2024.
                    """
        )
