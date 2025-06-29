# Import required libraries
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Read the SpaceX launch data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get the min and max payload for the RangeSlider
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# Create a Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),

    # TASK 1: Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    # TASK 2: Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: RangeSlider
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={i: str(i) for i in range(0, 10001, 2500)},
        value=[min_payload, max_payload]
    ),

    # TASK 4: Scatter plot
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2: Callback for pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
                     names='Launch Site',
                     title='Total Successful Launches by Site')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        site_counts = filtered_df['class'].value_counts().reset_index()
        site_counts.columns = ['class', 'count']
        fig = px.pie(site_counts, values='count',
                     names='class',
                     title=f'Success vs Failure for {entered_site}')
    return fig

# TASK 4: Callback for scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def get_scatter_plot(entered_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)

    if entered_site == 'ALL':
        filtered_df = spacex_df[mask]
        title = "Correlation between Payload and Success for All Sites"
    else:
        filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site) & mask]
        title = f"Correlation between Payload and Success for {entered_site}"

    fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class",
                     color="Booster Version Category",
                     title=title)
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
