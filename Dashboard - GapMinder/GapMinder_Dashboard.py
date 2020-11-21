import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv("gapminderDataFiveYear.csv")

app = dash.Dash()

# Creates the year option for dropdown (id = 'year-picker')
year_options = []
for year in df['year'].unique():
    year_options.append({'label':str(year), 'value':year})

# Creates the continent options for dropdown (id = 'continent-picker')
continent_options = []
for continent in df['continent'].unique():
    continent_options.append({'label':str(continent),'value': continent})

# Creates the country options for dropdown (id = 'country-picker')
country_options = []
for country in df['country'].unique():
    country_options.append({'label': str(country), 'value': country})

# App layout
app.layout = html.Div([
    html.H1('Country GDP and Life Expectancy from 1950 - 2000', style = {'textAlign': 'ecenter'}),
    html.Label('GDP vs Life Expectancy'),
    dcc.Graph(id='graph'),
    html.Label('\nYear picker\n'),
    dcc.Dropdown(id='year-picker',options=year_options,value = df['year'].min()),
    html.Br(),
    html.Label('Continent Picker'),
    dcc.Dropdown(id = 'continent-picker', options = continent_options, value = 'Asia'),
    html.Br(),
    html.H2('Additional Information about the country'),
    html.Label('Country Picker'),
    dcc.Dropdown(id = 'country-picker', placeholder = "Select a country"),
    html.Br(),
    html.Div(id = 'statsdiv')
])

# Output for the graph based on inputs from year dropdown (id = year-picker) and continent dropdown (id = continent-picker)
@app.callback(Output('graph', 'figure'),
              [Input('year-picker', 'value'),
              Input('continent-picker','value')])
def update_figure(selected_year, selected_continent):
    filtered_df = df[ (df['year'] == selected_year) & (df['continent'] == selected_continent)]    
    data = [go.Scatter(x = filtered_df['gdpPercap'],
                        y = filtered_df['lifeExp'],
                        text = filtered_df['country'],
                        mode = 'markers',
                        opacity = 0.7,
                        marker = {'size':15})]
    return {
        'data': data,
        'layout': go.Layout(
            xaxis={'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy'},
            hovermode='closest'
        )}

# Output for the country dropdown based on continent
@app.callback(Output('country-picker','options'),
            [Input('continent-picker','value')])
def update_country(selected_continent):
    filtered_list = df[df['continent'] == selected_continent] 
    return [{'label': i, 'value':i } for i in filtered_list['country'].unique()]

            
# Output about additional country shown in the graph 
@app.callback(Output('statsdiv', 'children'),
            [Input('country-picker', 'value'),
            Input('year-picker', 'value')])
def update_output_div(country_name, year):
    filtered = df[(df['country'] == country_name) & (df['year'] == year )]
    pop = str(format(int(filtered['pop'].item()), ","))
    lifeexp = str(int(filtered['lifeExp'].item()))
    gdp = str(format(int(filtered['gdpPercap'].item()),","))
    return "You have selected {} in {}. {} has a population of {}. The average life expectancy is {}, The GDP Per Capita is {}".format(country_name, year, country_name, pop, lifeexp, gdp)

if __name__ == '__main__':
    app.run_server()
