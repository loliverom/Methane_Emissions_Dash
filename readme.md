# Methane Emissions Dashboard

This is a project created as an exercise for the Tachyus application by Junior Data Visualization Analyst - Technical Test. This readme includes the main libraries used, installation guide and repository clone as well as some assumptions and changes that were made to the data in order to work with it.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Approach to the exercise](#Approach-excercise)
- [Data Assumptions](#data-assumptions)
- [Video Recording](#video-recording)

## Requirements

- Python 3.8.13 or above
- Dash
- Pandas
- Numpy
- Plotly
- Matplotlib
- Dash Bootstrap Components
- plotly.express (px)


## Installation

1. **Clone the repository**:
   - Open your terminal or command prompt.

   - Navigate to the directory where you want to clone the repository.

   - Run the following command:
   ```bash
   git clone (https://github.com/loliverom/Methane_Emissions_Dash.git)
2. **Navigate to the Repository Directory**:
Change the directory to the cloned repository:
      ```bash
      cd Methane_Emissions_Dash
3. **Install Dependencies**:
 - Navigate to the directory containing the requirements.txt file.

 - Run the following command to install the required Python packages:
   ```bash
   pip install -r requirements.txt

## Running the Application

 To start the application, run the following command in your terminal:
      ```bash
      python Dashboard.py

This will start the Dash server on http://127.0.0.1:8050/. Open this URL in your web browser to access the application.
**Note:** Ensure the required libraries are installed before running the script.

## Approach to the exercise

The first step in tackling the exercise was obtaining the data through the API. This process was the most complicated because if the REST request did not meet the required specifications, an error would occur, preventing data retrieval. While searching for information about the API, I found a useful website that provided the tables needed for my code. 

Upon testing the API code in a Jupyter notebook and obtaining the source tables, I validated for null values, duplicates, and errors in the columns before proceeding with the data analysis. Duplicate values were removed from the "rlps_ghg_emitter_facilities" table, and the NAN values in the "basin_associated_with_facility" column were filled with "Unknown". The format of the "reporting_year" column was also fixed to display only the year, and the numeric value of the "total_reported_ch4_emissions" column was corrected in the "EF_W_EMISSIONS_SOURCE_GHG" table.

Once the validations were completed, I created two tables: one for the first figure, involving only the "EF_W_EMISSIONS_SOURCE_GHG" table, and another for figures 2 and 3, which will be a union between the "EF_W_EMISSIONS_SOURCE_GHG" and "rlps_ghg_emitter_facilities" tables through the "facility_id" column. An important note about the "facility_id" column is that it contains duplicate entries for each year. To avoid duplicating records before the merge, I removed the duplicate "facility_id" values and different parent_company, keeping only the data from the most recent year. The union between these two tables was performed using the "inner" method.

Upon obtaining the source tables, I decided it was better to encapsulate the code that retrieves the data, and call it within the dashboard. Therefore, the main function was defined to return the values of the two tables when called from the dashboard: methane_x_year, used in Figure 1, and methane_vs_company, used in Figures 2 and 3. Once the tables are loaded into the environment, two lists are created for the drop-down menus: basin_associated_with_facility (used in Figures 1 and 2) and reporting_category (used in Figure 3). Additionally, the methane_vs_company table is filtered to include only reporting categories with total CH4 emissions greater than zero.

After obtaining this information, the header of the dashboard is defined first, featuring the Tachyus company logo and the title "Methane Emissions Dashboard." H2 titles are used for figure titles, and H3 titles for subtitles of each dropdown filter. Each figure has its respective filter.

Figure 1 is an area graph with a year range filter, defaulting to the minimum and maximum years of the entire series. It also includes a Basis filter, which has all available options selected by default.

Figure 2 is a stacked bar graph showing CH4 methane emissions by company, stacked by emission sources with year and basin filters. Due to the large number of companies, only the top 15 companies with the highest emissions are displayed to maintain clear visualization. In this figure, you can select a specific year to filter the information, and all basins are selected by default.

Figure 3 is a heat map of United States emissions. This figure includes interactions between the year filter and the emission sources filter (or "reporting_category" column), displaying only those sources in the selected year with emissions greater than zero. This filter adjusts according to the selected year. Lastly, a small note about the dashboard's author and its background is added to the layout.

## Data Assumptions 

The dashboard has two assumptions. The first assumption, derived from Figure 2, is that only the top 15 companies with the highest emissions need to be displayed based on the selected filters. The second assumption pertains to the "rlps_ghg_emitter_facilities" table, where a summary of the "facility_id" column is created to retain a unique value using the year column, leaving the most recent value of the "parent_company". The union type used should be "inner."

## Video Recording

The video can't be uploaded into github because it is too large. To access the video online, please click on the file **DashboardVideo.url**.