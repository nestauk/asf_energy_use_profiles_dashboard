# ⚡ 🔌 Energy-use profiles explorer

This repository contains the code to create the **Energy-use Profiles Explorer dashboard**, a dashboard for exploring **energy-use profiles**. **Energy-use profiles** are groups of households with similar energy consumption patterns, and they are built using smart meter data from a representative sample of households in Great Britain.

The dashboard is available at: https://energy-use-profiles-explorer.dap-tools.uk/

To know more about the project please refer to the [project page](https://www.nesta.org.uk/project/using-smart-meters-to-identify-energy-use-profiles/).

The dashboard was built using [Streamlit](https://streamlit.io/). To run this dashboard locally or to contribute to its development, follow the instructions in the Setup section.

## 🧩 Data

### Smart Energy Research Lab (SERL) Observatory Data
The analyses presented in this dashboard were conducted using **Smart Energy Research Lab (SERL) observatory data** [1], containing longitudinal smart meter electricity and gas data for over 13,000 households in Great Britain (GB). The data is accessible through the [UK Data Service SecureLab](https://ukdataservice.ac.uk/) by accredited researchers.

The SERL data is a rich source of information, including half-hourly gas and electricity consumption data and household survey data, such as property type, household composition, and income. The data documentation is available on the [data catalogue](https://beta.ukdataservice.ac.uk/datacatalogue/studies/study?id=8666#!/documentation).

[1]: Elam, S., Few, J., McKenna, E., Hanmer, C., Pullinger, M., Zapata-Webborn, E., Oreszczyn, T., Anderson, B., Department for Levelling Up, Housing and Communities, European Centre for Medium-Range Weather Forecasts, Royal Mail Group Limited. (2024). Smart Energy Research Lab Observatory Data, 2019-2024: Secure Access. [data collection]. 8th Edition. UK Data Service. SN: 8666, DOI: http://doi.org/10.5255/UKDA-SN-8666-8

### Number of households in GB

- **England**: 24.7 million households in 2023-24, according to the [English Housing Survey 2023 to 2024](https://www.gov.uk/government/statistics/chapters-for-english-housing-survey-2023-to-2024-headline-findings-on-demographics-and-household-resilience/chapter-1-profile-of-households-and-dwellings)
- **Scotland**: 2.55 million households in 2023, according to the [National Records of Scotland](https://www.nrscotland.gov.uk/publications/households-and-dwellings-in-scotland-2024/)
- **Wales**: 1.38 million households in mid-2023, according to the [Welsh Government](https://www.gov.wales/household-estimates-mid-2012-mid-2023-html)

This leads to an estimated total of **28.63 million households** in **GB**. This value is used to calculate the estimated number of GB households in each energy-use profile, which is displayed in the dashboard.


## 🛠️ Setup

1. Clone this repository:

Navigate to the directory where you want to clone the repository and run:

```
git clone git@github.com:nestauk/asf_energy_use_profiles_dashboard.git
```

2. Create a conda environment and install requirements:

```
cd asf_energy_use_profiles_dashboard
conda create --name asf_energy_use_profiles_dashboard python==3.13
conda activate asf_energy_use_profiles_dashboard
pip install -r requirements.txt
pip install pre-commit
```

3. If new data is made available in the project S3 bucket then run the following to process and save data to S3:

```
export PYTHONPATH=$PWD
python getters/data_processing.py
```

4. Run the dashboard locally with:

```
streamlit run energy_profiles_explorer.py
```

## 🗂️ Repository structure

The repository structure and key scripts are highlighted below:

```
asf_energy_use_profiles_dashboard/
├─ energy_profiles_explorer.py # main dashboard script
├───config/
│    Configuration scripts
│    ├─ configs.py
│    ├─ css_style.py
│    ├─ fonts_setup.py
│    ├─ highlights.py
├───.streamlit/
│    Streamlit specific configuration files
│    ├─ configs.toml
├───getters/
│    Scripts with functions to process and load data from S3
│    ├─ data_getters.py
│    ├─ data_processing.py
├───utils/
│    Utils handling and visualising data
│    ├─ data_handling_utils.py
│    ├─ data_vis_utils.py
├───pages/
│    Dashboard pages setup
│    ├─ about_dashboard_page.py
│    ├─ about_data_page.py
│    ├─ overview_results_page.py
│    ├─ select_profile_page.py
```

## 📢 Contributor guidelines

[Technical and working style guidelines](https://github.com/nestauk/ds-cookiecutter/blob/master/GUIDELINES.md)
