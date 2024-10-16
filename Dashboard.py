import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output,State
import matplotlib.pyplot as plt
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate 

## import data from library 

from TablesEPA import main

methane_x_year, methane_vs_company = main()

# Define dropdown options
basin_options = methane_x_year['basin_associated_with_facility'].unique().tolist()
emission_options = methane_vs_company.groupby(['state', 'reporting_category']).agg({'total_reported_ch4_emissions': 'sum'}).reset_index()
#reporting category with more than 0
emission_options = emission_options.loc[emission_options['total_reported_ch4_emissions']>0,'reporting_category'].unique().tolist()
methane_vs_company = methane_vs_company.loc[methane_vs_company['reporting_category'].isin(emission_options),:]


# Create the Dash app
app = dash.Dash(__name__)



# Layout for the Dash app
app.layout = html.Div([

    html.Div([
        
        html.Img(
            src="/assets/images/Tachyus-Logo.png",
            style={
                'height': '200px',  
                'width': 'auto',
                'float': 'left',  
                'margin-right': '20px'  
            }
        ),
        html.Div(
            style={
            'border-left': '1px solid black',
            'height': '250px',
            'display': 'inline-block',
            'margin-right': '20px'
        }
        ),
        # Title
        html.H1(
            "Methane Emissions Dashboard",
            style={
                'display': 'inline-block',
                'vertical-align': 'top',
                'font-family': 'Arial',
                'font-size': '60px'  
            }
        )
    ], style={'display': 'flex', 'align-items': 'center'}),
    html.Div([
    html.H2("Figure 1: Methane Emissions vs. Year (Stacked by Industry Segment)", style={'font-family': 'Arial'})
    ]),   
    html.Div([
        html.H3("Select a start year and finish year", style={'font-family': 'Arial'})
    ]), 
    #dropdowns first figure
    html.Div([
        # Start Year Dropdown
        html.Div([
            dcc.Dropdown(
                id='s-year-dw-1-methane',
                options=[{'label': str(year), 'value': year} for year in methane_x_year['reporting_year'].unique()],
                value=methane_x_year['reporting_year'].min(),  # Default to the earliest year
                clearable=False,
                placeholder="Select Start Year"
            )
        ], style={'width': '48%', 'display': 'inline-block', 'margin-right': '2%'}),  
        
        # End Year Dropdown
        html.Div([
            dcc.Dropdown(
                id='e-year-dw-1-methane',
                options=[{'label': str(year), 'value': year} for year in methane_x_year['reporting_year'].unique()],
                value=methane_x_year['reporting_year'].max(),  # Default to the latest year
                clearable=False,
                placeholder="Select End Year"
            )
        ], style={'width': '48%', 'display': 'inline-block'}) 
    ], style={'display': 'flex', 'flex-direction': 'row'}),

    #Dropdown for selecting basin
    html.H3("Select basin:", style={'font-family': 'Arial'}),
    dcc.Dropdown(
        id='basin-dropdown',
        options=[{'label': basin, 'value': basin} for basin in basin_options],
        value=basin_options,  # Default to all basins
        multi=True,  # Allow multiple selections
        clearable=True,  # Allow clearing the selection
        placeholder="Select a Basin"
    ),
    # Graph component
    dcc.Graph(
        id='methane-emissions-graph',
        
    ),

    html.H2("Figure 2: Methane Emissions vs. Company (Stacked by Emission Source)", style={'font-family': 'Arial'}),
    html.Div([
    html.H3("Select a year to analyse:", style={'font-family': 'Arial'})
    ]),
    dcc.Dropdown(
        id='year-dw-2-methane',
        options=[{'label': str(year), 'value': year} for year in methane_vs_company['reporting_year'].unique()],
        value=methane_vs_company['reporting_year'].min(),  # Default to all years
        multi=False,  # Allow multiple selections
        clearable=True,  # Allow clearing the selection
        placeholder="Select Reporting Year for Company"
    ),
    html.H3("Select basin:", style={'font-family': 'Arial'}),
    dcc.Dropdown(
        id='basin-dw-2-methane',
        options=[{'label': basin, 'value': basin} for basin in methane_vs_company['basin_associated_with_facility'].unique()],
        value=methane_vs_company['basin_associated_with_facility'].unique(),  # Default to all basins
        multi=True,  # Allow multiple selections
        clearable=True,  # Allow clearing the selection
        placeholder="Select a Basin for Company"
    ),
    html.Div("Since there are many company name fields, the report is adjusted to show the 15 company names with the highest emissions according to the year and basin selected in the filters."
             , style={'margin-top': '20px', 'margin-bottom': '20px','font-family': 'Arial'}),
    # Graph for Methane Emissions by Company
    dcc.Graph(
        id='methane-emissions-company-graph'
    ),
    # US Map Heatmap
    html.H2("Figure 3 (optional): Heat map of methane emissions by state", style={'font-family': 'Arial'}),
    
    #optiones
    html.Div([
        dbc.Row([

            # Column for the "Select year" dropdown
            dbc.Col([
                html.H2("Select year:", style={'font-family': 'Arial'}),
                dcc.Dropdown(
                    id='year-dw-heatmap',
                    options=[{'label': str(year), 'value': year} for year in methane_vs_company['reporting_year'].unique()],
                    value=methane_vs_company['reporting_year'].min(),
                    clearable=False,
                    placeholder="Select Year for Heatmap"
                )
            ], width=5),  # Adjust width as needed

            # Column for the "Select Emission Source" dropdown and "Select All" button
            dbc.Col([
                html.H2("Select Emission Source:", style={'font-family': 'Arial'}),
                dcc.Dropdown(
                    id='emission-dw-heatmap',
                    options=[{'label': emission, 'value': emission} for emission in emission_options],
                    value=emission_options,
                    multi=True,
                    clearable=True,
                    placeholder="Select a Source for Heatmap"
                ),
                
                # Add the "Select All" button below the dropdown
                html.Button(
                    "Select All",
                    id='select-all-button',
                    n_clicks=0,  # Initialize click counter
                    style={
                        'margin-top': '10px',
                        'background-color': '#007bff',
                        'color': 'white',
                        'border': 'none',
                        'padding': '10px 20px',
                        'border-radius': '5px',
                        'cursor': 'pointer'
                    }
                )
            ], width=5),  # Adjust width as needed

        ], justify='start')  # Align items to the left
    ]),


    dcc.Graph(id='methane-emissions-heatmap'),
    html.Div(
        "Report created by Luis Fernando Olivero  - luis.oliverom@hotmail.com",
        style={
            'position': 'absolute',
            'font-family': 'Times New Roman, serif',  
            'font-size': '16px', 
            'color': 'black' 
        }
    )
], style={
    'background-image': 'url("/assets/images/background.jpg")',  # Background image from assets
    'background-size': 'cover',  # Ensures the background image covers the entire screen
    'background-position': 'center',  # Center the image
    'background-repeat': 'no-repeat',  # Prevent the image from repeating
    'min-height': '100vh',  # Makes sure the background covers the full viewport height
    'width': '100%'  # Ensures it covers the full width
}
)

@app.callback(
    Output('methane-emissions-graph', 'figure'),
    [
        Input('s-year-dw-1-methane', 'value'),
        Input('e-year-dw-1-methane', 'value'),
        Input('basin-dropdown', 'value')
    ]
)
def figure1(start_year, end_year, selected_basin):
    # Filter the data based on the selected year range
    filtered_df = methane_x_year[
        (methane_x_year['reporting_year'] >= start_year) & 
        (methane_x_year['reporting_year'] <= end_year)
    ]
    
    # Filter by selected basin if any are selected
    if selected_basin:
        filtered_df = filtered_df[
            filtered_df['basin_associated_with_facility'].isin(selected_basin)
        ]
    
    # Create the stacked area plot using Plotly
    fig = px.area(filtered_df, 
                  x='reporting_year', 
                  y='total_reported_ch4_emissions', 
                  color='industry_segment',
                  labels={'reporting_year': 'Year', 'total_reported_ch4_emissions': 'Methane Emissions (CH4)',
                          'industry_segment': 'Industry Segment'},
                  title='Methane Emissions by Industry Segment and Basin')

    # Set the legend to appear below the plot
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        )
    )
    
    return fig

#  Callback for Methane Emissions by Company and Basin
@app.callback(
    Output('methane-emissions-company-graph', 'figure'),
    [
        Input('year-dw-2-methane', 'value'),
        Input('basin-dw-2-methane', 'value')
    ]
)
def figure2(selected_year, selected_basin):
    # Filter the data based on the selected reporting years

    selected_year = [selected_year]
    filtered_df = methane_vs_company[
        methane_vs_company['reporting_year'].isin(selected_year)]
    
    # Filter by selected basin if any are selected
    if selected_basin:
        filtered_df = filtered_df[
            filtered_df['basin_associated_with_facility'].isin(selected_basin)
        ]

    filtered_df.groupby(['parent_company','reporting_category']).sum('total_reported_ch4_emissions')
    filtered_df = filtered_df.dropna()
    filtered_df = filtered_df[filtered_df['total_reported_ch4_emissions']>0]
    filtered_df = filtered_df.sort_values(by='total_reported_ch4_emissions', ascending=False).head(15)
    # Create the stacked bar plot using Plotly
    fig = px.bar(filtered_df,
                 x='parent_company', 
                 y='total_reported_ch4_emissions',
                 color='reporting_category',  # Stacked by emission source
                 labels={'parent_company': 'Company Name', 'total_reported_ch4_emissions': 'Methane Emissions (CH4)'},
                 title='Methane Emissions by Company and Emission Source')

    # Set the legend to appear below the plot
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.2,
            xanchor="center",
            x=0.5
        ),
        barmode='stack' 
    )
    
    return fig
#callback for All emissions botton
@app.callback(
    Output('emission-dw-heatmap', 'value'),
    [Input('select-all-button', 'n_clicks')],
    [State('emission-dw-heatmap', 'options')]
)
def select_all_emission_sources(n_clicks, options):
    if n_clicks > 0:
        return [option['value'] for option in options]
    return dash.no_update  
#callback for emission options
@app.callback(
    Output('emission-dw-heatmap', 'options'),
    [Input('year-dw-heatmap', 'value')]
)
def update_emission_options(selected_year):
    if selected_year is None:
        raise PreventUpdate  # Si no hay año seleccionado, no hacer nada
    

    filtered_df = methane_vs_company[methane_vs_company['reporting_year'] == selected_year]
    
    filtered_df = filtered_df[filtered_df['total_reported_ch4_emissions'] > 0]

    emission_options_filtered = filtered_df['reporting_category'].unique().tolist()
    
    # Create dropwsdown list
    options = [{'label': emission, 'value': emission} for emission in emission_options_filtered]
    
    return options

# Callback for updating the heatmap
@app.callback(
    Output('methane-emissions-heatmap', 'figure'),
    [
        Input('year-dw-heatmap', 'value'),
        Input('emission-dw-heatmap', 'value')
    ]
)
def figure3_heatmap(selected_year, selected_emissions):
    # Filter the data based on the selected year
    filtered_df = methane_vs_company[methane_vs_company['reporting_year'] == selected_year]
    
    # Filter by selected basins if any are selected
    if selected_emissions:
        filtered_df = filtered_df[filtered_df['reporting_category'].isin(selected_emissions)]

    # Group by state and reporting category, summing the emissions
    heatmap_data = filtered_df.groupby(['state', 'reporting_category']).agg({'total_reported_ch4_emissions': 'sum'}).reset_index()
    heatmap_data = heatmap_data.loc[heatmap_data['total_reported_ch4_emissions']>0,:]

    #Calculate max values in range
    # Get the maximum value of emissions
    max_emissions = heatmap_data['total_reported_ch4_emissions'].max()

    # Calculate the upper limit for the color bar (max value rounded up to nearest 1000)
    max_emissions_rounded = np.ceil(max_emissions / 1000) * 1000
    # Create the heatmap using Plotly
    fig = px.choropleth(
        heatmap_data,
        locations='state',  
        locationmode="USA-states",  
        color='total_reported_ch4_emissions',  # Values for coloring
        hover_name='state', 
        color_continuous_scale='Viridis',  # Color scale
        labels={'total_reported_ch4_emissions': 'Methane Emissions (CH4)'},
        title='Heatmap of Methane Emissions by State',
        scope='usa',
        range_color=[0, max_emissions_rounded]  # Set the range of the color bar
    )
    # Update layout for better sizing
    fig.update_layout(
    geo=dict(
        lakecolor='rgb(255, 255, 255)',  
        projection=dict(type='albers usa')  
    )
    )

    return fig
# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8050) 