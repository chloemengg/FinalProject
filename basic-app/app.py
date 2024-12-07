from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load and filter your dataset
data = pd.read_csv("data/Final_Merged_Dataset.csv")
data = data[['State', 'Population', 'Avg Celcius', 'Personal_Income_Millions', 
             'EV_Charging_Stations', 'gas_price_regular']].dropna()

# Function to filter outliers
def filter_outliers(df, column, quantile=0.95):
    threshold = df[column].quantile(quantile)
    return df[df[column] <= threshold]

# Filter data for outliers
filtered_data = filter_outliers(data, 'Population')
filtered_data = filter_outliers(filtered_data, 'EV_Charging_Stations')
filtered_data = filter_outliers(filtered_data, 'gas_price_regular')

# Initialize the Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("United States EV Charging Stations App", style={
        'textAlign': 'center',
        'fontFamily': 'Arial, sans-serif',
        'color': 'black'
    }),
    
    # Scatter plot section
    html.Div([
        html.Label("Select X-axis Variable:", style={'fontFamily': 'Arial, sans-serif', 'color': 'black'}),
        dcc.Dropdown(
            id='x-axis',
            options=[
                {'label': 'Population', 'value': 'Population'},
                {'label': 'Average Temperature', 'value': 'Avg Celcius'},
                {'label': 'Average Annual Personal Income', 'value': 'Personal_Income_Millions'},
                {'label': 'Gas Price (Regular)', 'value': 'gas_price_regular'}
            ],
            value='Population',
            style={'backgroundColor': '#f8f8f8'}
        ),
    ], style={'width': '50%', 'margin': '0 auto'}),
    
    dcc.Graph(id='scatter-plot'),
    
    html.Hr(style={'margin': '40px 0', 'borderColor': 'black'}),
    
    # State statistics section
    html.Div([
        html.Label("Select a State:", style={'fontFamily': 'Arial, sans-serif', 'color': 'black'}),
        dcc.Dropdown(
            id='state-dropdown',
            options=[{'label': state, 'value': state} for state in data['State'].unique()],
            value=data['State'].iloc[0],
            style={'backgroundColor': '#f8f8f8'}
        ),
        html.Div(id='state-stats', style={
            'marginTop': '20px',
            'textAlign': 'center',
            'fontSize': '18px',
            'fontFamily': 'Arial, sans-serif',
            'color': 'black'
        }),
    ], style={'width': '50%', 'margin': '0 auto'})
])

# Callback for scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('x-axis', 'value')
)
def update_scatter_plot(x_axis):
    # Create the scatter plot using filtered data
    fig = px.scatter(
        filtered_data,
        x=x_axis,
        y='EV_Charging_Stations',
        labels={x_axis: x_axis, 'EV_Charging_Stations': 'EV Charging Stations'},
        title=f"EV Charging Stations vs {x_axis}",
        template="plotly_white",
        width=1000,  # Adjust width
        height=600   # Adjust height
    )
    
    # Add axis range for better zoom
    if x_axis == 'Population':
        fig.update_xaxes(range=[0, filtered_data['Population'].max() * 1.1])
        fig.update_yaxes(range=[0, filtered_data['EV_Charging_Stations'].max() * 1.1])
    elif x_axis == 'gas_price_regular':
        fig.update_xaxes(range=[2.5, 3.2])  # Adjust range for gas prices
    return fig

# Callback for state statistics
@app.callback(
    Output('state-stats', 'children'),
    Input('state-dropdown', 'value')
)
def update_state_stats(selected_state):
    # Filter data for the selected state
    state_data = data[data['State'] == selected_state].iloc[0]
    return html.Div([
        html.P(f"State: {selected_state}", style={'fontWeight': 'bold'}),
        html.P(f"Population: {state_data['Population']:,}"),
        html.P(f"Average Temperature (°C): {state_data['Avg Celcius']}"),
        html.P(f"Annual Total Personal Income (Millions): ${state_data['Personal_Income_Millions']:,}"),
        html.P(f"EV Charging Stations: {state_data['EV_Charging_Stations']:,}"),
        html.P(f"Gas Price (Regular): ${state_data['gas_price_regular']:.2f}")
    ])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
