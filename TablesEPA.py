import io
import requests
import pandas as pd
import numpy as np

class EPAQuery:
    """
    Esta clase se usa para extraer datos de la EPA directamente en Python.
    """
    def __init__(self, table_name):
        self.base_url = 'https://data.epa.gov/efservice/'
        self.table_name = table_name
        self.desired_output_format = 'CSV'

    def construct_query_URL(self, desired_state=None, desired_county=None, desired_area_code=None, desired_year=None, rows_to_include=None):
        """
        Construye la URL para obtener los datos en función de los parámetros dados.
        """
        query = self.base_url + self.table_name + '/'
        if desired_state:
            query += 'state_abbr/' + desired_state + '/'
        if desired_county:
            query += 'county_name/' + desired_county + '/'
        if desired_area_code:
            query += 'zip_code/' + desired_area_code + '/'
        if desired_year:
            query += 'reporting_year/' + desired_year + '/'
        query += self.desired_output_format
        if rows_to_include:
            query += '/rows/' + rows_to_include
        return query

    def read_query_into_pandas(self, query):
        """
        Toma la URL de la consulta, la obtiene y la convierte en un DataFrame de pandas.
        """
        s = requests.get(query).content
        dataframe = pd.read_csv(io.StringIO(s.decode('utf-8')), engine='python', encoding='utf-8')
        return dataframe

def main():
    table_names = ['EF_W_EMISSIONS_SOURCE_GHG', 'rlps_ghg_emitter_facilities']
    epa_dfs = {}
    table_objects = {}

    for table_name in table_names:
        table_objects[table_name] = EPAQuery(table_name)
        query = table_objects[table_name].construct_query_URL()
        epa_dfs[table_name] = table_objects[table_name].read_query_into_pandas(query)

    # get the tables
    EF_W_EMISSIONS_SOURCE_GHG = epa_dfs['EF_W_EMISSIONS_SOURCE_GHG']
    rlps_ghg_emitter_facilities = epa_dfs['rlps_ghg_emitter_facilities']

    # Nan values handeling
    EF_W_EMISSIONS_SOURCE_GHG['basin_associated_with_facility'] = EF_W_EMISSIONS_SOURCE_GHG['basin_associated_with_facility'].replace(" ", np.nan)
    EF_W_EMISSIONS_SOURCE_GHG['basin_associated_with_facility'] = EF_W_EMISSIONS_SOURCE_GHG['basin_associated_with_facility'].fillna('Unknown')
    #fixing common columns 
    EF_W_EMISSIONS_SOURCE_GHG['reporting_year'] = pd.to_datetime(EF_W_EMISSIONS_SOURCE_GHG['reporting_year'], format='%Y').dt.year
    EF_W_EMISSIONS_SOURCE_GHG['total_reported_ch4_emissions'] = pd.to_numeric(EF_W_EMISSIONS_SOURCE_GHG['total_reported_ch4_emissions'], errors='coerce')
    
    # first figure
    methane_x_year = EF_W_EMISSIONS_SOURCE_GHG.loc[:, ['reporting_year', 'total_reported_ch4_emissions', 'industry_segment', 'basin_associated_with_facility']]
    methane_x_year = methane_x_year.groupby(['reporting_year', 'industry_segment', 'basin_associated_with_facility']).sum('total_reported_ch4_emissions').reset_index()


    ## Second and third figure
    #drop duplicates 
    rlps_ghg_emitter_facilities = rlps_ghg_emitter_facilities.drop_duplicates()

    # leave just 1 facility_id
    df_sorted = rlps_ghg_emitter_facilities.sort_values(by=['facility_id', 'year'], ascending=[True, False])

    # drop duplicates keeping the most recent year
    df_unique1 = df_sorted.drop_duplicates(subset=['facility_id'], keep='first')
    facility_parent_company = df_unique1[['facility_id','parent_company','state']]
    methane_vs_company = pd.merge(EF_W_EMISSIONS_SOURCE_GHG[['reporting_year','basin_associated_with_facility','reporting_category','total_reported_ch4_emissions','facility_id']]
            ,facility_parent_company
            ,how='inner',on='facility_id')
    methane_vs_company = methane_vs_company.groupby(['reporting_year','basin_associated_with_facility','reporting_category','parent_company','state']).sum('total_reported_ch4_emissions').reset_index()


    return methane_x_year, methane_vs_company

if __name__ == '__main__':
    df = main()
    print(df)