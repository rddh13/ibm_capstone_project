import pandas as pd
import dash
from dash import dcc, html, Output, Input
import plotly.express as px

# Load data
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
df = pd.read_csv(url)
df.columns = df.columns.str.strip()  # Clean whitespace
df['Recession_Label'] = df['Recession'].apply(lambda x: 'Recession' if x == 1 else 'Non-Recession')

# Dash app
app = dash.Dash(__name__)
app.title = "Automobile Sales Dashboard"

# Layout
app.layout = html.Div([
    html.H1("XYZAutomotives Sales Dashboard", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Report Type:"),
        dcc.Dropdown(
            id='report-type',
            options=[
                {'label': 'Recession Report', 'value': 'recession'},
                {'label': 'Yearly Report', 'value': 'yearly'}
            ],
            value='recession'
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    html.Div(id='output-graph')
])

# Callback
@app.callback(
    Output('output-graph', 'children'),
    Input('report-type', 'value')
)
def update_report(report_type):
    if report_type == 'recession':
        # Recession Report: Sales vs Unemployment Rate
        recession_df = df[df['Recession'] == 1]
        fig = px.scatter(
            recession_df,
            x='unemployment_rate',
            y='Automobile_Sales',
            color='Vehicle_Type',
            title="Recession Report: Sales vs Unemployment Rate"
        )
        return dcc.Graph(figure=fig)

    elif report_type == 'yearly':
        # Yearly Report: Total Sales by Year
        yearly_sales = df.groupby('Year')['Automobile_Sales'].sum().reset_index()
        fig = px.line(
            yearly_sales,
            x='Year',
            y='Automobile_Sales',
            markers=True,
            title="Yearly Report: Total Automobile Sales"
        )
        return dcc.Graph(figure=fig)

# Run server
if __name__ == '__main__':
    app.run(debug=True)
