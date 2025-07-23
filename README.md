# ⚡ 🔌 Energy-use profiles explorer

This repository contains the code to create the **Energy-use Profiles Explorer dashboard**, a dashboard for exploring energy-use profiles built from GB household smart meter data.

The dashboard is available at: [add website link here]

The dashboard was built using [Streamlit](https://streamlit.io/). To run this dashboard locally or to contribute to its development, follow the instructions in the Setup section.

## 🧩 Data

The analyses presented in this document were conducted using **Smart Energy Research Lab (SERL) observatory data** [1], containing longitudinal smart meter electricity and gas data for over 13,000 households in Great Britain. The data is accessible through the [UK Data Service SecureLab](https://ukdataservice.ac.uk/) by accredited researchers.

The SERL data is a rich source of information, including half-hourly gas and electricity consumption data and household survey data, such as property type, household composition, and income. The data documentation is available on the [data catalogue](https://beta.ukdataservice.ac.uk/datacatalogue/studies/study?id=8666#!/documentation).

[1]: Elam, S., Few, J., McKenna, E., Hanmer, C., Pullinger, M., Zapata-Webborn, E., Oreszczyn, T., Anderson, B., Department for Levelling Up, Housing and Communities, European Centre for Medium-Range Weather Forecasts, Royal Mail Group Limited. (2024). Smart Energy Research Lab Observatory Data, 2019-2024: Secure Access. [data collection]. 8th Edition. UK Data Service. SN: 8666, DOI: http://doi.org/10.5255/UKDA-SN-8666-8

## 🛠️ Setup

1. Clone this repository:

`git clone git@github.com:nestauk/asf_energy_use_profiles_dashboard.git`

2. Create a conda environment and install requirements:

```
conda create --name asf_energy_use_profiles_dashboard python==3.13
conda activate asf_energy_use_profiles_dashboard
pip install -r requirements.txt
pip install pre-commit

```

3. Run the dashboard locally with:

`streamlit run energy_profiles_explorer.py`

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
